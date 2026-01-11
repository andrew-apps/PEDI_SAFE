# 🐳 Docker Deployment Guide

## Quick Start with Docker

### Step 1: Create .env file

```bash
# In pedisafe/ folder
echo "CEREBRAS_API_KEY=csk-your-key-here" > .env
```

### Step 2: Build and Run

```bash
# Option 1: Docker Compose (Recommended)
docker-compose up --build

# Option 2: Direct Docker
docker build -t pedisafe .
docker run -p 8501:8501 --env-file .env pedisafe
```

### Step 3: Access

Open your browser at: **http://localhost:8501**

---

## Useful Commands

```bash
# View logs
docker-compose logs -f

# Stop
docker-compose down

# Rebuild after changes
docker-compose up --build

# Clean everything
docker-compose down -v
docker system prune -a
```

---

## Production Deployment

### Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

### Render

1. Connect GitHub repo
2. Select "Docker"
3. Add variable: `CEREBRAS_API_KEY`
4. Automatic deploy

---

## Troubleshooting

**Error: "Port already in use"**
```bash
# Change port in docker-compose.yml
ports:
  - "8502:8501"  # Use 8502 instead of 8501
```

**Error: "API Key not found"**
```bash
# Verify .env
cat .env

# Rebuild with variables
docker-compose up --build
```

**Embeddings very slow on first load**
- Normal: downloads Hugging Face model (~80MB)
- Subsequent loads are instant (cached)
