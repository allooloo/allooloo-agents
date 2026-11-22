"""Connect to the Allooloo MCP, list the markets, and read one listed company.

    pip install -r requirements.txt
    python read_company.py TSX:SHOP

Any ticker, ISIN or LEI works as the identifier.
"""
import asyncio
import json
import os
import sys

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

MCP = "https://mcp.getissuer.ai/mcp"
# Name your agent: the name travels as the User-Agent of every call.
HEADERS = {"User-Agent": os.environ.get("AGENT_NAME", "my-agent/0.1")}


def data(result):
    """The tool's answer as a dict (structured content, or the JSON text)."""
    if result.structuredContent:
        return result.structuredContent
    return json.loads(result.content[0].text)


async def main(identifier: str) -> None:
    async with streamablehttp_client(MCP, headers=HEADERS) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()

            nodes = data(await session.call_tool("list_nodes", {}))
            print("markets live:", ", ".join(nodes["live_nodes"]))

            record = data(await session.call_tool("get_record", {"identifier": identifier}))
            name = record["identity"]["name"]
            print("company:", name["value"])
            print("record:", record["cmr"], "as of", record["as_of"], "served by", record["node"])
            print("name read from:", name["source_url"])
            print("signed:", bool(record.get("signature")))
            if record.get("receipt"):
                print("receipt:", record["receipt"].get("id"))


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1] if len(sys.argv) > 1 else "TSX:SHOP"))
