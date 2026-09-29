# ⚡ VoltFlow — Backend API Service

FastAPI REST backend with SQLAlchemy ORM, Pydantic validation, and SQLite/PostgreSQL support for the VoltFlow Electricity Board Connection & Utility Service Platform.

---

## 🚀 Quickstart

### 1. Set up Virtual Environment
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Seed Database
```bash
python -m backend.app.database.seed_data --force
```

### 4. Run Development Server
```bash
uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

### 5. Interactive API Documentation
Open your browser at:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- **System Health**: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

---

## 🧪 Testing
```bash
pytest tests/ -v
```
