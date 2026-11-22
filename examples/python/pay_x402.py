"""Pay for one read on x402: PayGo, per call, in USDC (first) or Open USD (second), both on Base.

Prices: https://allooloo.io/x402/pricing.json (the offer itself also names the price).

    pip install -r requirements.txt
    python pay_x402.py TSX:SHOP                 # asks for the offer and prints it; nothing is paid
    PAYER_KEY=... python pay_x402.py TSX:SHOP    # pays in USDC
    PAYER_KEY=... python pay_x402.py TSX:SHOP --open-usd

PAYER_KEY is the private key of the wallet that pays. Keep it in your environment or a secret store; never commit it.
A call is paid only when it asks: the header x402-pay: 1 asks for the offer, and the x402 client answers it with a PAYMENT-SIGNATURE.
"""
import asyncio
import base64
import json
import os
import sys

import httpx

MCP = "https://mcp.getissuer.ai/mcp"
PRICES = "https://allooloo.io/x402/pricing.json"
BASE = "eip155:8453"
USDC = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
OPEN_USD = "0xB2000000000000000000002fEb517dFeC7415344"
BASE_RPC = os.environ.get("BASE_RPC", "https://mainnet.base.org")
HEADERS = {
    "User-Agent": os.environ.get("AGENT_NAME", "my-agent/0.1"),
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
    "x402-pay": "1",
}


def body(identifier: str) -> dict:
    return {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "get_record", "arguments": {"identifier": identifier}}}


def answer(r: httpx.Response) -> dict:
    """The JSON-RPC answer, whether it came as JSON or as one server-sent event."""
    t = r.text
    if t.lstrip().startswith("event:") or t.lstrip().startswith("data:"):
        t = [line[5:] for line in t.splitlines() if line.startswith("data:")][-1]
    return json.loads(t)


async def offer(identifier: str) -> None:
    async with httpx.AsyncClient(timeout=60) as c:
        r = await c.post(MCP, json=body(identifier), headers=HEADERS)
    print("HTTP", r.status_code)
    required = r.headers.get("PAYMENT-REQUIRED")
    o = json.loads(base64.b64decode(required)) if required else r.json()
    for a in o.get("accepts", []):
        name = "USDC" if a["asset"].lower() == USDC.lower() else "Open USD" if a["asset"].lower() == OPEN_USD.lower() else a["asset"]
        print(f"accepts {name} on {a['network']} ({a['scheme']}), pay to {a['payTo']}")


async def pay(identifier: str, open_usd: bool) -> None:
    from eth_account import Account
    from x402.client import x402Client
    from x402.http.clients.httpx import x402HttpxClient
    from x402.mechanisms.evm.exact.client import ExactEvmScheme
    from x402.mechanisms.evm.signers import EthAccountSigner, EthAccountSignerWithRPC

    account = Account.from_key(os.environ["PAYER_KEY"])
    if open_usd:   # Open USD settles through Permit2; the signer reads the chain to prepare it
        price = httpx.get(PRICES, follow_redirects=True, timeout=30).json()["price"]["amount"]   # the cap is the price of record, read from the price list
        pick = lambda version, reqs: [r for r in reqs if str(getattr(r, "asset", "")).lower() == OPEN_USD.lower()][0]
        client = x402Client(pick).register(BASE, ExactEvmScheme(EthAccountSignerWithRPC(account, BASE_RPC))).set_spend_controls(
            {"allowed_assets": [{"network": BASE, "asset": OPEN_USD, "max_amount_per_payment": price}]})
    else:          # USDC is the first entry of the offer
        client = x402Client().register(BASE, ExactEvmScheme(EthAccountSigner(account)))
    async with x402HttpxClient(client, timeout=120) as c:
        r = await c.post(MCP, json=body(identifier), headers=HEADERS)
    print("HTTP", r.status_code)
    if r.status_code != 200:
        print(r.text[:500])
        return
    result = answer(r)["result"]
    record = result.get("structuredContent") or json.loads(result["content"][0]["text"])
    print("company:", record["identity"]["name"]["value"], "| record:", record["cmr"], "as of", record["as_of"])
    settled = r.headers.get("PAYMENT-RESPONSE")
    if settled:
        print("settlement:", json.loads(base64.b64decode(settled)))


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    identifier = args[0] if args else "TSX:SHOP"
    if os.environ.get("PAYER_KEY"):
        asyncio.run(pay(identifier, "--open-usd" in sys.argv))
    else:
        asyncio.run(offer(identifier))
