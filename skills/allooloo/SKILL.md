---
name: allooloo
description: Read the signed record of listed companies from Allooloo over MCP. Use when a task needs facts about a listed company (who the issuer is, its identifiers, its dated filings and news, its auditor, whether a security may be ordered for a client, its target market, or its record on a past date) with the source and date of every fact.
---

# Allooloo

Allooloo serves the signed record of listed companies to AI agents over MCP. Every answer carries its source, its date, a signature and a receipt. Quote the source and the date with any fact you use.

## When to use it

- The task names a listed company, a ticker, an ISIN or an LEI, and needs facts about it.
- The task asks what a company has filed or released, or what changed since a date.
- The task asks whether a security may be ordered for a category of client, or for its target market.
- The task needs a company's record as it stood on a past date, its auditor, or the company behind a ticker.

Do not use it for prices, quotes or advice: Allooloo serves records, not prices or views.

## How to call it

Start here: `https://mcp.getissuer.ai/mcp` (streamable HTTP, no sign-in).

1. `resolve_issuer` with a ticker, ISIN or LEI: finds the company and its home market.
2. `get_record` with the same identifier: the full signed record, served by the home market.
3. `list_nodes`: the markets on the roster and which are live.

Each product also has its own MCP address, serving its product call:

| Product call | Use it for | MCP address |
|---|---|---|
| `get_issuer` | The signed record of a listed company | `https://mcp.getissuer.ai/mcp` |
| `get_issuer_news` | Dated news: `list_filings` (newest first), `get_delta` (what is new since your last read), `get_row` | `https://mcp.getissuernews.ai/mcp` |
| `get_orderability` | Whether a security may be ordered for a client category | `https://mcp.getorderability.ai/mcp` |
| `get_target_market` | The manufacturer's target market statement | `https://mcp.gettargetmarket.ai/mcp` |
| `get_as_of` | The record as it stood on a date | `https://mcp.getasof.ai/mcp` |
| `get_filings` | Disclosures in a date range | `https://mcp.getfilings.ai/mcp` |
| `get_ticker` | The company behind a ticker | `https://mcp.getticker.ai/mcp` |
| `get_auditor` | The auditor and every dated change | `https://mcp.getauditor.ai/mcp` |
| `get_research` | The research page, written from the signed record | `https://mcp.getresearch.ai/mcp` |

Also: `get_counterparty`, the Counterparty MCP. The regulator's record of every licensed capital markets firm, read by any agent in one call. MCP address `https://mcp.getcounterparty.ai/mcp`. Repository: https://github.com/allooloo/getcounterparty

Read each tool's own description from `tools/list` before calling it; it names the arguments.

## Paying per call

Calls are free unless you ask to pay. To pay: PayGo on x402, per call, in USDC or Open USD on Base (`eip155:8453`). Send the header `x402-pay: 1`; the MCP answers HTTP 402 with its offer (USDC first, Open USD second); answer it with a `PAYMENT-SIGNATURE` header on the same call. Prices: https://allooloo.io/x402/pricing.json. Pay only when your user has given you a wallet and a limit for it.

## Good practice

- Name your agent in the User-Agent header.
- Keep the receipt id that comes with an answer; it proves what was read and when (https://rco-records.ai).
- If a field's state is not `sourced`, say so when you use it.
