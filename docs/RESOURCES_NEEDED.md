# Resources Needed — External Services & APIs

Report for project owner: items to activate for production agents and integrations.

## Critical (for live agents)

| Resource | Purpose | Placeholder in | Est. cost |
|----------|---------|----------------|-----------|
| **LLM API** (OpenAI / Anthropic) | News search synthesis, paper summaries | `debt.txt` → `OPENAI_API_KEY` | Usage-based |
| **SMTP** (SendGrid, AWS SES, Gmail app password) | Research digest emails to author | `SMTP_*` in debt.txt | Free tier available |

## Scientific Paper Access

| API | Purpose | Key needed? | Notes |
|-----|---------|-------------|-------|
| [Semantic Scholar](https://www.semanticscholar.org/product/api) | Paper metadata & abstracts | Optional API key for higher rate limits | `SEMANTIC_SCHOLAR_API_KEY` |
| [PubMed E-utilities](https://www.ncbi.nlm.nih.gov/home/develop/api/) | Medical cannabis research | Optional `PUBMED_API_KEY` | Free, rate-limited |
| [Crossref](https://www.crossref.org/documentation/retrieve-metadata/rest-api/) | DOI resolution | Mailto only | `CROSSREF_MAILTO` |
| [OpenAlex](https://openalex.org/) | Open scholarly graph | No key | Alternative to Semantic Scholar |

**Recommendation:** Start with OpenAlex + PubMed (no keys), add Semantic Scholar key if rate limits hit.

## Instagram (blog seed)

| Resource | Purpose | Notes |
|----------|---------|-------|
| Meta Graph API | Import posts from @papiroebers | Requires Facebook Developer app, Business/Creator account linkage |
| Manual fallback | Demo uses `backend/data/seed/instagram_posts.json` | Curated placeholders mimicking IG content |

**Placeholder:** `INSTAGRAM_API_TOKEN` in debt.txt

## Infrastructure (scale phases)

| Service | Phase | Purpose |
|---------|-------|---------|
| PostgreSQL | 2 | Replace SQLite |
| Redis | 3 | Agent job queue |
| Object storage (S3/R2) | 3 | Images, assets |
| CDN | 4 | Static assets |

## MCP Servers (designed, not implemented)

See `.cursor/mcp/README.md`:

- `cannahub-news-mcp` — wrapped news search tools
- `cannahub-research-mcp` — scholarly API tools

## Domain & Hosting

- Domain registrar
- SSL certificate (Let's Encrypt)
- Hosting: VPS, Railway, Fly.io, or Azure (author preference)

## Legal / Compliance

- Privacy policy for contact form data (LGPD Brazil)
- Cookie consent if analytics added
- Content disclaimer for medical information

## Summary Checklist

- [ ] LLM provider account + API key
- [ ] SMTP for research digest
- [ ] Author email in `RESEARCH_DIGEST_TO`
- [ ] (Optional) Semantic Scholar API key
- [ ] (Optional) Instagram Graph API for auto-sync
- [ ] Production database when leaving demo phase
