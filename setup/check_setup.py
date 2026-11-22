"""Check the setup files: connect to every MCP server that cursor.mcp.json and vscode.mcp.json name, over streamable HTTP (as those
editors do), and list its tools.

    pip install mcp
    python check_setup.py
"""
import asyncio
import json
import os
import pathlib

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

HERE = pathlib.Path(__file__).parent
HEADERS = {"User-Agent": os.environ.get("AGENT_NAME", "my-agent/0.1")}


def servers():
    for f, key in (("cursor.mcp.json", "mcpServers"), ("vscode.mcp.json", "servers")):
        for name, s in json.loads((HERE / f).read_text(encoding="utf-8"))[key].items():
            yield f, name, s["url"]


async def check(f, name, url):
    async with streamablehttp_client(url, headers=HEADERS) as (read, write, _):
        async with ClientSession(read, write) as session:
            info = await session.initialize()
            tools = [t.name for t in (await session.list_tools()).tools]
    print(f"{f}  {name}  {url}  ->  {info.serverInfo.name}: {', '.join(tools)}")


async def main():
    for f, name, url in servers():
        await check(f, name, url)


if __name__ == "__main__":
    asyncio.run(main())
