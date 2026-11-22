// Connect to the Allooloo MCP, list the markets, and read one listed company.
//
//   npm install
//   npx tsx read-company.ts TSX:SHOP
//
// Any ticker, ISIN or LEI works as the identifier.
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";

const MCP = "https://mcp.getissuer.ai/mcp";
// Name your agent: the name travels as the User-Agent of every call.
const headers = { "User-Agent": process.env.AGENT_NAME ?? "my-agent/0.1" };

// The tool's answer as an object (structured content, or the JSON text).
function data(result: any): any {
  if (result.structuredContent) return result.structuredContent;
  return JSON.parse(result.content[0].text);
}

async function main(identifier: string) {
  const client = new Client({ name: "my-agent", version: "0.1.0" });
  await client.connect(new StreamableHTTPClientTransport(new URL(MCP), { requestInit: { headers } }));

  const nodes = data(await client.callTool({ name: "list_nodes", arguments: {} }));
  console.log("markets live:", nodes.live_nodes.join(", "));

  const record = data(await client.callTool({ name: "get_record", arguments: { identifier } }));
  const name = record.identity.name;
  console.log("company:", name.value);
  console.log("record:", record.cmr, "as of", record.as_of, "served by", record.node);
  console.log("name read from:", name.source_url);
  console.log("signed:", Boolean(record.signature));

  await client.close();
}

main(process.argv[2] ?? "TSX:SHOP").catch((e) => {
  console.error(e);
  process.exit(1);
});
