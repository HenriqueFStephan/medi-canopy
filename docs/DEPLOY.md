# Deploy Medi Canopy — step-by-step (you do this; ~15 minutes)

I **cannot** log into GitHub, Render, or Netlify on your machine. Follow these steps exactly.

---

## Step 0 — Push code to GitHub

### 0a. Create repo on GitHub

1. Open **https://github.com/new**
2. Repository name: `medi-canopy`
3. **Private** or Public — your choice
4. Do **not** add README (we already have one)
5. Click **Create repository**

### 0b. Push from your PC (PowerShell)

```powershell
cd "c:\Users\henri\OneDrive\Área de Trabalho\Leisure\VSC\medi-canopy"

git init
git add .
git commit -m "Initial Medi Canopy demo — frontend, backend, deploy config"

git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/medi-canopy.git
git push -u origin main
```

Replace `YOUR_USERNAME/medi-canopy` with your repo URL.

> If Git asks for login, use a **Personal Access Token** as password:  
> GitHub → Settings → Developer settings → Personal access tokens

---

## Step 1 — Deploy backend on Render

1. Open **https://dashboard.render.com** → log in (or sign up with GitHub)
2. Click **New +** → **Blueprint**
3. Connect your GitHub account if prompted
4. Select the **medi-canopy** repository
5. Render detects `render.yaml` → click **Apply**
6. Wait for deploy (~3–5 min)
7. Copy your service URL, e.g. `https://cannahub-api.onrender.com`

### Test API

Open in browser:

```
https://cannahub-api.onrender.com/health
```

Expected: `{"status":"ok","version":"0.1.0","environment":"production"}`

API docs: `https://cannahub-api.onrender.com/docs`

### First deploy CORS note

`render.yaml` has a placeholder `FRONTEND_URL`. That is OK for step 1. You will fix it in step 3.

---

## Step 2 — Deploy frontend on Netlify

1. Open **https://app.netlify.com** → log in (or sign up with GitHub)
2. **Add new site** → **Import an existing project** → **GitHub**
3. Authorize Netlify → select **medi-canopy** repo
4. Netlify reads `netlify.toml` automatically. Verify:

   | Field | Value |
   |-------|-------|
   | Base directory | `frontend` |
   | Build command | `npm ci && npm run build:ci` |
   | Publish directory | `frontend/dist/medi-canopy` |

5. **Before deploy** → **Site configuration** → **Environment variables** → **Add variable**:

   | Key | Value |
   |-----|-------|
   | `NG_APP_API_URL` | `https://cannahub-api.onrender.com/api/v1` |

   Use **your** Render URL from step 1.

6. Click **Deploy site**
7. Wait ~2–3 min → copy site URL, e.g. `https://random-name-123.netlify.app`

### Optional: rename site

Netlify → **Domain management** → **Options** → change to `medi-canopy` → `https://medi-canopy.netlify.app`

---

## Step 3 — Fix CORS on Render

1. Back to **https://dashboard.render.com**
2. Open **cannahub-api** service
3. **Environment** → edit `FRONTEND_URL`:
   - Set to your Netlify URL, e.g. `https://medi-canopy.netlify.app`
   - **No trailing slash**
4. Click **Save Changes** → Render redeploys automatically (~2 min)

---

## Step 4 — Verify end-to-end

1. Open your Netlify URL
2. Go to **Notícias** — articles should load
3. Go to **Blog** — posts should load
4. Submit **Contato** form — should succeed

If news/blog show “Não foi possível carregar”:

- Open browser DevTools → **Network** → look for red requests to `onrender.com`
- Usually means `FRONTEND_URL` mismatch or API still waking up (wait 60 s and refresh)

---

## Step 5 — Message for the author

Copy/paste:

```
Olá! Segue o preview do hub:

🌐 Site: https://YOUR-SITE.netlify.app

Nota: o servidor free “dorme” após ~15 min sem acesso.
A primeira visita do dia pode demorar até 1 minuto — é normal.

Instagram continua em: https://www.instagram.com/papiroebers
```

---

## Quick reference — where to log in

| Step | URL | Action |
|------|-----|--------|
| GitHub repo | https://github.com/new | Create repo |
| Render | https://dashboard.render.com | Blueprint from repo |
| Netlify | https://app.netlify.com | Import from GitHub |
| Test API | `https://YOUR-API.onrender.com/health` | Browser |

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Render build fails | Check **Logs** — usually missing `requirements.txt` path; confirm rootDir is `backend` |
| Netlify build fails | Set `NODE_VERSION=18` in env; check build log |
| CORS error in browser | `FRONTEND_URL` on Render must exactly match Netlify URL |
| Slow first load | Render free tier cold start — normal |
| Empty news/blog | Wake API first: open `/health`, then refresh site |

---

## Alternative: Cloudflare Pages instead of Netlify

1. https://dash.cloudflare.com → **Workers & Pages** → **Create** → **Pages** → Connect Git
2. Build command: `cd frontend && npm ci && npm run build:ci`
3. Output: `frontend/dist/medi-canopy`
4. Env: `NG_APP_API_URL` = your Render API + `/api/v1`
5. Add `_redirects` or SPA rule: `/* /index.html 200`

Then set `FRONTEND_URL` on Render to your `*.pages.dev` URL.
