# 🚀 VoltFlow Deployment Guide

Complete step-by-step instructions for deploying VoltFlow to staging and production cloud environments.

---

## Architecture

```
                    INTERNET / CLIENTS
                            │
                            ▼
              ┌───────────────────────────┐
              │  FRONTEND (Vercel/Netlify)│
              │   HTML5 / CSS3 / ES6 JS   │
              └─────────────┬─────────────┘
                            │ HTTPS REST Calls
                            ▼
              ┌───────────────────────────┐
              │  BACKEND (Render/Railway) │
              │   FastAPI + Uvicorn       │
              └─────────────┬─────────────┘
                            │ SQL / Pool
                            ▼
              ┌───────────────────────────┐
              │ POSTGRESQL / SUPABASE DB  │
              └───────────────────────────┘
```

---

## 1. Backend Deployment (Render.com / Railway / Koyeb)

### Option A: Render.com (Web Service)
1. Fork or push the codebase to your GitHub/GitLab repository.
2. Log into [Render Dashboard](https://dashboard.render.com/) and click **New > Web Service**.
3. Connect your repository.
4. Set the following settings:
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
5. Configure Environment Variables:
   - `DEBUG`: `False`
   - `ENVIRONMENT`: `production`
   - `DATABASE_URL`: Your production PostgreSQL connection string (or leave default SQLite file volume).
6. Click **Create Web Service**.

---

## 2. Production PostgreSQL Database Setup

### Option A: Render Managed PostgreSQL
1. On Render, click **New > PostgreSQL Database**.
2. Copy the **Internal Database URL** or **External Database URL**.
3. Set the `DATABASE_URL` environment variable on your backend service:
   ```env
   DATABASE_URL=postgresql://user:password@hostname:5432/voltflow_db
   ```
4. When the backend service boots up, SQLAlchemy automatically creates the required tables and executes baseline seeding.

---

## 3. Frontend Deployment (Vercel / Netlify / GitHub Pages)

### Option A: Vercel
1. Install Vercel CLI or link GitHub repository on [Vercel Dashboard](https://vercel.com).
2. Set Root Directory to `frontend`.
3. Ensure `frontend/js/config.js` is updated with your production backend API URL:
   ```javascript
   get API_BASE_URL() {
       if (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1") {
           return "http://127.0.0.1:8000/api/v1";
       }
       return "https://your-backend.onrender.com/api/v1";
   }
   ```
4. Deploy!

### Option B: Unified Single-Container Deployment (Docker)
VoltFlow is configured out of the box to serve the static frontend from the FastAPI server directly at `/` and `/static`.

Run with Docker:
```bash
docker build -t voltflow .
docker run -p 8000:8000 -e ENVIRONMENT=production voltflow
```

Or with Docker Compose:
```bash
docker-compose up -d
```
Access the complete full-stack portal at `http://localhost:8000`.

---

## 4. CORS Configuration in Production

In `backend/app/config.py`, make sure your deployed frontend domain is included in `CORS_ORIGINS`:
```python
CORS_ORIGINS = [
    "https://your-voltflow-portal.vercel.app",
    "https://your-voltflow-portal.netlify.app",
    "http://localhost:3000",
    "http://127.0.0.1:8000"
]
```

---

## 5. Verification Checklist

- [ ] Backend responds with `200 OK` on `/health`.
- [ ] Swagger documentation loads at `/docs`.
- [ ] Frontend loads and displays initial KPI statistics on Dashboard.
- [ ] New connection application submission works and persists in database.
- [ ] Meter allocation and grievance submission flows execute smoothly.
