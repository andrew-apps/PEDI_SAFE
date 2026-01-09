# 🩺 PediSafe - Pediatric Fever Triage Assistant

> **Alameda Hacks 2026** | Track: Social Good + ML/AI

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40-red.svg)](https://streamlit.io)
[![LangChain](https://img.shields.io/badge/LangChain-0.3-green.svg)](https://langchain.com)

## 🎯 Problem Statement

**Emergency Department Overcrowding** is a global healthcare crisis. Parents, especially first-time caregivers, often rush to the ER for common symptoms like fever due to anxiety and lack of reliable guidance. This leads to:
- Overwhelmed emergency services
- Long wait times for truly urgent cases
- Unnecessary healthcare costs
- Parental stress and anxiety

## 💡 Solution

**PediSafe** is an AI-powered triage assistant that helps parents make informed decisions about pediatric fever. Using Retrieval-Augmented Generation (RAG) with validated clinical guidelines from AAP (American Academy of Pediatrics) and NHS, it provides:

- **Color-coded urgency levels** (🔴 RED / 🟠 ORANGE / 🟡 YELLOW / 🟢 GREEN)
- **Clear action steps** tailored to the child's age and symptoms
- **Red flag detection** for immediate escalation
- **Source citations** for transparency and trust

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🤖 RAG-based AI | Uses clinical guidelines as knowledge base |
| 🔒 Safety First | Deterministic red-flag detection layer |
| 🌐 BYOK Support | Bring Your Own API Key for cost efficiency |
| 📱 Responsive UI | Clean, mobile-friendly Streamlit interface |
| 📚 Cited Sources | All recommendations include source references |
| 🌍 Spanish/English | Bilingual support |

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     User Interface                       │
│                   (Streamlit + CSS)                      │
├─────────────────────────────────────────────────────────┤
│                    Safety Layer (A)                      │
│            Deterministic Red Flag Detection              │
├─────────────────────────────────────────────────────────┤
│                     RAG Layer (B)                        │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐  │
│  │  Knowledge  │→ │    FAISS     │→ │   GPT-4o-mini  │  │
│  │    Base     │  │  (Vectors)   │  │   + LangChain  │  │
│  └─────────────┘  └──────────────┘  └────────────────┘  │
├─────────────────────────────────────────────────────────┤
│                   Clinical Sources                       │
│        AAP HealthyChildren.org | NHS UK Guidelines       │
└─────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- OpenAI API Key ([Get one here](https://platform.openai.com/api-keys))

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/pedisafe.git
cd pedisafe

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate
# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

```bash
# Copy environment file
cp .env.example .env

# Edit .env and add your OpenAI API Key
# OPENAI_API_KEY=sk-your-key-here
```

### Run the App

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 💰 Cost Optimization

PediSafe is designed for **minimal cost**:

| Component | Model/Service | Cost |
|-----------|---------------|------|
| Embeddings | text-embedding-3-small | $0.02/1M tokens |
| LLM | GPT-4o-mini | $0.15/$0.60 per 1M tokens |
| Vector Store | FAISS (local) | **FREE** |
| Hosting | Streamlit Community | **FREE** |

**Estimated cost per conversation:** ~$0.001-0.005 (less than 1 cent!)

## 📊 Triage Levels

| Level | Meaning | Action |
|-------|---------|--------|
| 🔴 RED | Emergency | Call 911 or go to ER immediately |
| 🟠 ORANGE | High Priority | Contact pediatrician today |
| 🟡 YELLOW | Monitor | Home care with close observation |
| 🟢 GREEN | Low Risk | Comfort measures appropriate |

## 📚 Knowledge Sources

All clinical information comes from **public, validated sources**:

1. **AAP HealthyChildren.org**
   - [Fever and Your Baby](https://www.healthychildren.org/English/health-issues/conditions/fever/Pages/Fever-and-Your-Baby.aspx)
   - [When to Call the Pediatrician](https://www.healthychildren.org/English/health-issues/conditions/fever/Pages/When-to-Call-the-Pediatrician.aspx)
   - [Fever Without Fear](https://www.healthychildren.org/English/health-issues/conditions/fever/Pages/Fever-Without-Fear.aspx)

2. **NHS UK**
   - [High temperature in children](https://www.nhs.uk/symptoms/fever-in-children/)

## 🛡️ Safety & Disclaimers

- ⚠️ PediSafe is **NOT a diagnostic tool**
- ⚠️ Does NOT replace professional medical advice
- ⚠️ Always consult a pediatrician when in doubt
- ⚠️ For emergencies, call your local emergency number

## 🎬 Demo Video

[Link to 3-minute demo video on YouTube/Loom]

## 👥 Team

- [Your Name] - Developer

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

---

**Built with ❤️ for Alameda Hacks 2026**

*Empowering parents with knowledge, one consultation at a time.*
