# Allooloo for AI agents

Allooloo gives an AI agent the signed record of listed companies: who the issuer is, what it has filed and released, and whether a security may be ordered for a client. Every answer carries its source, its date, a signature and a receipt. Agents call it over MCP, free, or pay per call on x402.

**Start here: `https://mcp.getissuer.ai/mcp`**

## The products

The nine products, each with the MCP address that serves it. The start address answers `resolve_issuer`, `get_record` and `list_nodes` and forwards to the market that holds the record; each product's own address serves its product call.

| Product call | What it answers | MCP address |
|---|---|---|
| `get_issuer` | The signed record of a listed company (`resolve_issuer`, `get_record`, `list_events_since`, `list_aliases`, `get_signal`) | `https://mcp.getissuer.ai/mcp` |
| `get_issuer_news` | Dated news of listed companies, each line with its source (`resolve_issuer`, `list_filings`, `get_delta`, `get_row`) | `https://mcp.getissuernews.ai/mcp` |
| `get_orderability` | Whether a listed security may be ordered for a category of client | `https://mcp.getorderability.ai/mcp` |
| `get_target_market` | The manufacturer's target market statement for a security | `https://mcp.gettargetmarket.ai/mcp` |
| `get_as_of` | The record of a listed company as it stood on a date | `https://mcp.getasof.ai/mcp` |
| `get_filings` | The disclosures of a listed company in a date range | `https://mcp.getfilings.ai/mcp` |
| `get_ticker` | The listed company behind a ticker | `https://mcp.getticker.ai/mcp` |
| `get_auditor` | The auditor of a listed company and every dated change | `https://mcp.getauditor.ai/mcp` |
| `get_research` | The research page of a listed company, written from the signed record | `https://mcp.getresearch.ai/mcp` |

## Setup

**Claude Code** ([setup/claude-code.sh](setup/claude-code.sh))

```bash
claude mcp add --transport http allooloo https://mcp.getissuer.ai/mcp
claude mcp add --transport http allooloo-news https://mcp.getissuernews.ai/mcp
```

**Cursor**: `~/.cursor/mcp.json`, or `.cursor/mcp.json` in your project ([setup/cursor.mcp.json](setup/cursor.mcp.json))

```json
{
  "mcpServers": {
    "allooloo": { "url": "https://mcp.getissuer.ai/mcp" },
    "allooloo-news": { "url": "https://mcp.getissuernews.ai/mcp" }
  }
}
```

**VS Code**: `.vscode/mcp.json` in your workspace ([setup/vscode.mcp.json](setup/vscode.mcp.json))

```json
{
  "servers": {
    "allooloo": { "type": "http", "url": "https://mcp.getissuer.ai/mcp" },
    "allooloo-news": { "type": "http", "url": "https://mcp.getissuernews.ai/mcp" }
  }
}
```

Add any other product the same way, with its address from the table. `python setup/check_setup.py` connects to every server the two JSON files name and lists its tools.

## Examples

Both connect to the start address, call `list_nodes`, and read one listed company with `get_record`.

**Python** ([examples/python/read_company.py](examples/python/read_company.py))

```bash
cd examples/python
pip install -r requirements.txt
python read_company.py TSX:SHOP
```

**TypeScript** ([examples/typescript/read-company.ts](examples/typescript/read-company.ts))

```bash
cd examples/typescript
npm install
npx tsx read-company.ts TSX:SHOP
```

Any ticker, ISIN or LEI works as the identifier. Set `AGENT_NAME` to name your agent; it travels as the User-Agent of every call.

## Paying per call on x402

PayGo on x402, per call, in USDC (first) or Open USD (second), both on Base (`eip155:8453`). A call is paid only when it asks: send the header `x402-pay: 1` and the MCP answers HTTP 402 with its offer; answer it with a `PAYMENT-SIGNATURE` header on the same call. The price list: https://allooloo.io/x402/pricing.json

[examples/python/pay_x402.py](examples/python/pay_x402.py) uses the x402 Python SDK:

```bash
python pay_x402.py TSX:SHOP                    # prints the offer; nothing is paid
PAYER_KEY=... python pay_x402.py TSX:SHOP       # pays in USDC
PAYER_KEY=... python pay_x402.py TSX:SHOP --open-usd
```

`PAYER_KEY` is the private key of the wallet that pays. Keep it in your environment or a secret store; never commit it.

## The agent skill

[skills/allooloo/SKILL.md](skills/allooloo/SKILL.md) tells an AI agent when to use Allooloo and how to call it. Copy the `allooloo` folder into your agent's skills folder (for Claude Code: `~/.claude/skills/` or `.claude/skills/` in your project).

## More

- Allooloo: https://allooloo.io · Agent tools and SDKs: https://allooloo.io/agent-tools
- Receipts of every answer: https://rco-records.ai
- Contact: Matthew Keddy, CEO · mk@allooloo.io

MIT licence. Allooloo Technologies Corp.
