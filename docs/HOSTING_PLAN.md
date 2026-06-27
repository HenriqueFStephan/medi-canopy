# Hosting Plan — CanaHub (Free Tier)

**Goal:** Let the author preview the demo online at zero cost.  
**Stack:** Angular static build + FastAPI API (separate hosts).

---

## Recommended setup (pick this unless you prefer one vendor)

| Layer | Platform | Why |
|-------|----------|-----|
| **Frontend** | **Netlify** or **Cloudflare Pages** | Free, fast CDN, auto-deploy from GitHub, perfect for Angular `dist/` |
| **Backend** | **Render** | Free Python web service, simple FastAPI deploy, HTTPS out of the box |
| **Git repo** | **GitHub** | Connects both platforms; optional Actions for agents later |
| **Agents (later)** | **GitHub Actions** | Free scheduled cron; not needed for author preview |

**Alternative (single vendor):** Both on **Render** — Static Site (frontend) + Web Service (backend).

---

## Architecture in production

```
Author browser
      │
      ▼
┌─────────────────────┐
│  Netlify / CF Pages │  https://cannahub.netlify.app
│  (Angular static)   │
└──────────┬──────────┘
           │ HTTPS  GET /api/v1/*
           ▼
┌─────────────────────┐
│  Render Web Service │  https://cannahub-api.onrender.com
│  (FastAPI + uvicorn)│
└─────────────────────┘
           │
           ▼
    JSON seed data (demo)
    review_queue.json
```

CORS on the backend must allow the frontend URL.  
The frontend must call the **full API URL** (not `/api/v1` relative path).

---

## Platform comparison

### Frontend options

| Platform | Free tier | Pros | Cons |
|----------|-----------|------|------|
| **Netlify** | 100 GB bandwidth/mo | Easiest UX, env vars at build, SPA redirects | Build minutes limited |
| **Cloudflare Pages** | Generous | Very fast CDN, unlimited bandwidth feel | Slightly more config for SPA |
| **Vercel** | Hobby free | Great DX, preview URLs | Optimized for Next.js; Angular works fine |
| **Render Static** | Free | Same dashboard as API | Fewer frontend-specific features |
| **GitHub Pages** | Free | Simple | Awkward for Angular routing without `_redirects` |

**Recommendation:** **Netlify** (simplest for author handoff) or **Cloudflare Pages** (best performance in Brazil via CDN).

### Backend options

| Platform | Free tier | Pros | Cons |
|----------|-----------|------|------|
| **Render** | 750 hrs/mo, sleeps after 15 min idle | Zero-config Python, HTTPS | Cold start 30–60 s after sleep |
| **Fly.io** | Small VM allowance | Always-on possible, global regions | More CLI/setup |
| **Railway** | ~$5 trial credit/mo | Easy deploy | Not truly free long-term |
| **Koyeb** | 1 free web service | Similar to Render | Smaller community/docs |
| **PythonAnywhere** | 1 web app | Python-native | Restricted outbound HTTP on free tier |

**Recommendation:** **Render** for the demo — minimal setup, author can hit `/docs` to verify API.

### Not recommended for this project (free tier)

| Platform | Reason |
|----------|--------|
| **Vercel serverless** | FastAPI + local JSON files ≠ good fit for serverless |
| **Netlify Functions alone** | Would require rewriting backend |
| **Heroku** | No meaningful free tier anymore |

---

## Known limitations (author preview is still fine)

1. **Render free sleeps** — First visit after ~15 min idle may take up to ~1 min. Tell the author to wait once.
2. **Ephemeral disk** — JSON data in `backend/data/` may reset on redeploy. Demo seed files reload automatically; contact form submissions may not persist forever.
3. **No custom domain required** — `*.netlify.app` + `*.onrender.com` URLs are enough for preview.
4. **Agents** — Skip for preview, or run manually via GitHub Actions later.

---

## Prerequisites checklist

Before deploying, you need:

- [ ] Code pushed to a **GitHub** repository (public or private)
- [ ] Accounts on chosen frontend + backend hosts
- [ ] Node 18+ for Netlify/Render builds (they provide this in CI)
- [ ] Two URLs after deploy — fill in the table below

| Variable | Example | Your value |
|----------|---------|------------|
| `FRONTEND_URL` | `https://cannahub.netlify.app` | __________ |
| `API_PUBLIC_URL` | `https://cannahub-api.onrender.com` | __________ |

---

## Step-by-step: Backend on Render

1. Push repo to GitHub.
2. [Render Dashboard](https://dashboard.render.com) → **New → Web Service**.
3. Connect the GitHub repo.
4. Settings:

   | Field | Value |
   |-------|-------|
   | **Root Directory** | `backend` |
   | **Runtime** | Python 3 |
   | **Build Command** | `pip install -r requirements.txt` |
   | **Start Command** | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
   | **Instance Type** | Free |

5. **Environment variables:**

   | Key | Value |
   |-----|-------|
   | `APP_ENV` | `production` |
   | `FRONTEND_URL` | `https://YOUR-FRONTEND-URL` (set after frontend deploy) |
   | `LLM_PROVIDER` | `placeholder` |

6. Deploy → note URL: `https://cannahub-api.onrender.com`
7. Test: `https://cannahub-api.onrender.com/health` → `{"status":"ok",...}`

Optional: add `render.yaml` at repo root (see below).

---

## Step-by-step: Frontend on Netlify

1. [Netlify Dashboard](https://app.netlify.com) → **Add new site → Import from Git**.
2. Select the repo.
3. Settings:

   | Field | Value |
   |-------|-------|
   | **Base directory** | `frontend` |
   | **Build command** | `npm ci && npm run build` |
   | **Publish directory** | `frontend/dist/cannahub` |

4. **Environment variables** (build time):

   | Key | Value |
   |-----|-------|
   | `NG_APP_API_URL` | `https://cannahub-api.onrender.com/api/v1` |

   > Requires a small code change so `environment.prod.ts` reads this at build time (see “Code changes required”).

5. **SPA redirect** — add `frontend/public/_redirects` or `netlify.toml`:

   ```toml
   # netlify.toml (repo root or frontend/)
   [build]
     base = "frontend"
     publish = "dist/cannahub"
     command = "npm ci && npm run build"

   [[redirects]]
     from = "/*"
     to = "/index.html"
     status = 200
   ```

6. Deploy → note URL: `https://something.netlify.app`
7. Go back to Render → set `FRONTEND_URL` to this URL → redeploy backend (CORS).

---

## Step-by-step: Frontend on Cloudflare Pages (alternative)

1. [Cloudflare Dashboard](https://dash.cloudflare.com) → **Workers & Pages → Create → Pages → Connect Git**.
2. Build settings:

   | Field | Value |
   |-------|-------|
   | **Framework preset** | None |
   | **Build command** | `cd frontend && npm ci && npm run build` |
   | **Build output** | `frontend/dist/cannahub` |

3. Env var: `NG_APP_API_URL` = backend URL + `/api/v1`
4. **SPA routing:** `_redirects` file or Cloudflare **Single Page Application** rule:

   ```
   /*    /index.html   200
   ```

---

## Step-by-step: Both on Render (single vendor)

1. **Web Service** — same as backend steps above.
2. **Static Site** → New → Static Site → connect repo:

   | Field | Value |
   |-------|-------|
   | **Root Directory** | `frontend` |
   | **Build Command** | `npm install && npm run build` |
   | **Publish Directory** | `dist/cannahub` |

3. Set env + CORS same as Netlify flow.

---

## Code changes required (before deploy)

These are **not done yet** — implement when you confirm platforms:

### 1. Frontend API URL at build time

`environment.prod.ts` currently uses `/api/v1` (same-origin). For split hosting:

```typescript
export const environment = {
  production: true,
  apiUrl: 'https://cannahub-api.onrender.com/api/v1', // or NG_APP_API_URL injection
  instagramUrl: 'https://www.instagram.com/papiroebers',
  siteName: 'CanaHub',
};
```

Better: inject via `NG_APP_API_URL` in Netlify/Render build env.

### 2. CORS — allow production frontend

Backend reads `FRONTEND_URL` from env. Set it on Render to the exact Netlify/Pages URL (no trailing slash).

### 3. Seed data on first boot

Ensure `backend/data/` seed copies run on deploy if JSON files missing (already handled by `JsonStore`).

### 4. Optional: `render.yaml` (Infrastructure as code)

```yaml
services:
  - type: web
    name: cannahub-api
    runtime: python
    rootDir: backend
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: APP_ENV
        value: production
      - key: LLM_PROVIDER
        value: placeholder
      - key: FRONTEND_URL
        sync: false  # set manually after frontend URL known
```

---

## Agents on free tier (optional, post-preview)

| Option | Cost | How |
|--------|------|-----|
| **GitHub Actions** | Free (public repo) | Cron workflow calling `python -m agents.run` |
| **Render Cron Job** | Paid on Render | Not free |
| **Manual** | Free | You run `run-agents.ps1` locally |

For author preview, **skip agents** — seeded news/blog is enough.

---

## Suggested decision flow

```
Do you have GitHub? ──no──► Create repo first
        │
       yes
        ▼
Prefer one dashboard? ──yes──► Render (API + static)
        │
       no
        ▼
Frontend: Netlify or Cloudflare Pages
Backend:  Render
        ▼
Deploy backend → get API URL
Deploy frontend with API URL → get site URL
Set FRONTEND_URL on backend → redeploy
Send author both links
```

---

## What to send the author

```
Site:  https://YOUR-FRONTEND.netlify.app
API:   https://YOUR-API.onrender.com/docs  (optional, for dev curiosity)

Nota: o servidor free “dorme” após 15 min sem uso.
A primeira visita pode demorar ~1 minuto.
```

---

## Account checklist (fill in)

| Service | Have account? | Used for |
|---------|---------------|----------|
| GitHub | ☐ | Source + deploy trigger |
| Render | ☐ | Backend API |
| Netlify | ☐ | Frontend (option A) |
| Cloudflare | ☐ | Frontend (option B) |
| Vercel | ☐ | Frontend (option C) |
| Fly.io | ☐ | Backend (alternative) |

**Reply with which boxes you have checked** and we'll implement the deploy config + env injection in the next step.
