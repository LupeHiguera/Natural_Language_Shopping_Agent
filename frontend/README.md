# ShoeHub

A React 19 + Vite + Tailwind portfolio shopping demo, backed by FastAPI, DynamoDB, and AWS Bedrock Agents. The site supports product browsing, shareable filters, sorting, product details, and natural language search. Purchases and payments are not implemented.

## Local development

```bash
npm install
npm run dev
```

Start the backend from `backend/` in another terminal:

```bash
venv/bin/python -m uvicorn app.main:app --reload --port 8000
```

The API defaults to `http://localhost:8000`. Set `VITE_API_GATEWAY_URL` in `.env.local` for a different backend. Vite exposes `VITE_` values to the browser; only put the public API URL there.

## Validation

```bash
npm run lint
npm run build
```

From `backend/`, run the backend tests without live AWS credentials:

```bash
AWS_ACCESS_KEY_ID=testing AWS_SECRET_ACCESS_KEY=testing AWS_EC2_METADATA_DISABLED=true venv/bin/python -m pytest -q
```

## Search and demo behavior

- Local mode uses the same four sample products for search, browsing, and detail pages. Product photos are illustrative and load from Unsplash; unavailable product images use a local styled fallback.
- Local search supports style, color, brand, US size, and price constraints such as “under $100” and “between $90 and $100”. It is a keyword parser, with no conversation memory.
- Live mode preserves Bedrock sessions and reads product records from action-group trace output alongside the agent’s text. Structured JSON completions with `response` (or `agent_response`) and `products` are also supported, including JSON split across chunks and UTF-8 boundaries. Live failures show an error instead of silently substituting demo inventory. The search input allows up to 200 characters.
- Clearing or replacing a search cancels pending requests. Escape, outside clicks, and navigation dismiss results.
- Browse filters are stored in query parameters, so refresh and browser back/forward preserve them. Sorting is local to the page.

## Production configuration

Set the public API URL before building. Configure backend `CORS_ORIGINS_STR` as a comma-separated list containing the exact deployed frontend origin, for example `https://shop.higuera.io,http://localhost:5173`. Upload `dist/` through your existing deployment flow and configure CloudFront/S3 routing to serve `index.html` for client-side routes.

## Audit follow-ups

The September 2026 refresh fixed unsupported navigation categories, inconsistent stock fields, stale requests, filter synchronization, placeholder branding, nonfunctional checkout/newsletter controls, Bedrock stream parsing and trace compatibility, zero-price filters, and unrestricted CORS.

Before deploying, validate the live Bedrock action group and structured responses with the deployed DynamoDB catalog, confirm the frontend URL and CORS origin, and verify CloudFront deep links. Live AWS infrastructure was not exercised by local validation. For a larger catalog, replace full-table DynamoDB scans with a suitable indexed query strategy. Dependency upgrades and AWS deployment are separate follow-up work.
