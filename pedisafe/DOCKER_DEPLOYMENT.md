# 🐳 Docker Deployment Guide

## Quick Start con Docker

### Paso 1: Crear archivo .env

```bash
# En la carpeta pedisafe/
echo "CEREBRAS_API_KEY=csk-tu-key-aqui" > .env
```

### Paso 2: Build y Run

```bash
# Opción 1: Docker Compose (Recomendado)
docker-compose up --build

# Opción 2: Docker directo
docker build -t pedisafe .
docker run -p 8501:8501 --env-file .env pedisafe
```

### Paso 3: Acceder

Abre tu navegador en: **http://localhost:8501**

---

## Comandos Útiles

```bash
# Ver logs
docker-compose logs -f

# Detener
docker-compose down

# Rebuild después de cambios
docker-compose up --build

# Limpiar todo
docker-compose down -v
docker system prune -a
```

---

## Deployment en Producción

### Railway

```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login y deploy
railway login
railway init
railway up
```

### Render

1. Conectar GitHub repo
2. Seleccionar "Docker"
3. Agregar variable: `CEREBRAS_API_KEY`
4. Deploy automático

---

## Troubleshooting

**Error: "Port already in use"**
```bash
# Cambiar puerto en docker-compose.yml
ports:
  - "8502:8501"  # Usa 8502 en lugar de 8501
```

**Error: "API Key not found"**
```bash
# Verificar .env
cat .env

# Rebuild con variables
docker-compose up --build
```

**Embeddings muy lentos en primera carga**
- Normal: descarga modelo de Hugging Face (~80MB)
- Siguientes cargas son instantáneas (cached)
