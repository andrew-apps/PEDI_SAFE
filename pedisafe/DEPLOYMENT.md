# 🚀 PediSafe Deployment Guide

## Quick Deploy to Streamlit Cloud (Recommended)

### Step 1: Prepare Your Repository

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Required Files** (already included):
   - `app.py` - Main application
   - `requirements.txt` - Python dependencies
   - `.streamlit/config.toml` - Theme configuration
   - `runtime.txt` - Python version (3.12)

### Step 2: Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"New app"**
3. Connect your GitHub account (if not already)
4. Select your repository: `your-username/pedisafe`
5. Set the main file path: `pedisafe/app.py`
6. Click **"Deploy!"**

### Step 3: Configure Secrets (Optional)

The app comes with a **default Cerebras API key** for demo purposes.
For production, add your own keys:

1. In Streamlit Cloud dashboard, go to your app
2. Click **"Settings"** → **"Secrets"**
3. Add your secrets:
   ```toml
   CEREBRAS_API_KEY = "csk-your-key-here"
   # Or for OpenAI:
   # OPENAI_API_KEY = "sk-your-key-here"
   ```
4. Click **"Save"**

### Step 4: Access Your App

Your app will be available at:
```
https://[your-app-name].streamlit.app
```

---

## Alternative: Deploy to Other Platforms

### Heroku

1. Create `Procfile`:
   ```
   web: streamlit run pedisafe/app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. Deploy:
   ```bash
   heroku create your-app-name
   heroku config:set CEREBRAS_API_KEY=csk-your-key
   git push heroku main
   ```

### Railway

1. Connect GitHub repository
2. Add environment variable: `CEREBRAS_API_KEY`
3. Deploy automatically

### Docker

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY pedisafe/ .
RUN pip install -r requirements.txt

EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `CEREBRAS_API_KEY` | No* | Cerebras API key (FREE) |
| `OPENAI_API_KEY` | No | OpenAI API key (paid) |

*The app includes a default demo key for Cerebras.

---

## Production Checklist

- [ ] Code pushed to GitHub
- [ ] All dependencies in `requirements.txt`
- [ ] `.streamlit/config.toml` configured
- [ ] (Optional) Custom API keys in secrets
- [ ] App deployed and tested
- [ ] Custom domain configured (optional)

---

## Troubleshooting

### "Module not found" Error
- Ensure all dependencies are in `requirements.txt`
- Check Python version compatibility (3.9+)

### "API Key Invalid" Error
- Verify your Cerebras/OpenAI key is correct
- Check if key is properly set in Streamlit secrets

### Slow First Load
- First load downloads Hugging Face embeddings (~80MB)
- Subsequent loads are faster (cached)

### Memory Issues
- Streamlit Cloud free tier has 1GB RAM limit
- Consider upgrading for production use

---

## Support

- **GitHub Issues**: Report bugs and feature requests
- **Cerebras API**: [cloud.cerebras.ai](https://cloud.cerebras.ai)
- **Streamlit Docs**: [docs.streamlit.io](https://docs.streamlit.io)

---

**Built with ❤️ for Alameda Hacks 2026**
