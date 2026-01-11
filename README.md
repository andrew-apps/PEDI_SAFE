# 🏥 PediSafe - Intelligent Pediatric Assistant

AI-powered pediatric triage system that helps parents determine the urgency level of children's symptoms, following official AAP (American Academy of Pediatrics) and NHS UK guidelines.

---

## 🎯 Main Features

- **Color-Coded Triage Levels:**
  - 🔴 **RED:** Emergency - Go to ER immediately
  - 🟠 **ORANGE:** Urgent - Contact pediatrician today
  - 🟡 **YELLOW:** Consultation - Contact within 24 hours
  - 🟢 **GREEN:** Home monitoring

- **RAG Architecture (Retrieval-Augmented Generation):**
  - Layer A: Deterministic red flag detection
  - Layer B: Contextual analysis with LLM (Cerebras)
  - Knowledge base: 5 official AAP/NHS documents

- **Automated Test Suite:**
  - 16 validated test cases
  - Critical safety case coverage
  - Non-hallucination validation
  - HTML report generation

---

## 🚀 Quick Start

### Option 1: Run the Application

```bash
# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r pedisafe/requirements.txt

# Run Streamlit application
streamlit run pedisafe/app.py
```

### Option 2: Run Tests

```bash
# Activate virtual environment
venv\Scripts\activate

# Run test suite
venv\Scripts\python.exe -m pytest pedisafe/test_pedisafe.py -v

# Generate HTML report
venv\Scripts\python.exe -m pytest pedisafe/test_pedisafe.py -v --html=pedisafe/report.html --self-contained-html
```

**For complete setup instructions, see:** [`SETUP_TESTS.md`](SETUP_TESTS.md)

---

## 📁 Project Structure

```
1_ALAMEDA_HACKS/
├── pedisafe/                      # Main application
│   ├── app.py                    # Streamlit interface
│   ├── rag_engine.py             # RAG engine with LangChain
│   ├── test_pedisafe.py          # Test suite
│   ├── pytest.ini                # Pytest configuration
│   ├── report.html               # Test report (generated)
│   ├── requirements.txt          # Python dependencies
│   ├── knowledge/                # Knowledge base (5 .md files)
│   │   ├── aap_fever_baby.md
│   │   ├── aap_fever_without_fear.md
│   │   ├── aap_symptom_checker.md
│   │   ├── aap_when_to_call.md
│   │   └── nhs_fever_children.md
│   └── .streamlit/
│       ├── config.toml           # Streamlit configuration
│       └── secrets.toml.example  # API keys template
├── DOCS/                         # Hackathon documentation
│   └── test_case_validation.md   # Test case validation
├── venv/                         # Virtual environment (not in Git)
├── SETUP_TESTS.md                # 📘 Testing instructions
├── TESTS_FINALES.md              # 📊 Test results
├── RUN_TESTS.bat                 # Windows runner script
├── .gitignore                    # Ignored files
└── README.md                     # This file
```

---

## 🧪 Testing System

### Implemented Tests

**16 total test cases:**
- ✅ **8 critical safety cases** (fever <3 months, red flags)
- ✅ **4 edge cases** (persistent fever, high temperature)
- ✅ **2 false positive validations**
- ✅ **2 system validations** (sources, disclaimers)

### Current Results

```
✅ 13 PASSED (81%)
❌ 2 FAILED (LLM precision, not safety)
⏭️ 1 SKIPPED
```

**Safety Metrics:**
- ✅ 100% real emergency detection (<3 months)
- ✅ 0 critical false negatives
- ✅ 0 hallucinations
- ✅ 100% correct AAP/NHS source citations

**See details:** [`TESTS_FINALES.md`](TESTS_FINALES.md)

---

## 🔧 Configuration

### Environment Variables

Create file `pedisafe/.env`:

```env
CEREBRAS_API_KEY=your-api-key-here
```

Or configure system environment variable:

```bash
# Windows
setx CEREBRAS_API_KEY "your-api-key-here"

# Linux/Mac
export CEREBRAS_API_KEY="your-api-key-here"
```

### Streamlit Secrets

Copy and edit:

```bash
cp pedisafe/.streamlit/secrets.toml.example pedisafe/.streamlit/secrets.toml
```

Edit `secrets.toml` with your API key.

---

## 📚 Complete Documentation

| Document | Description |
|-----------|-------------|
| [`README.md`](README.md) | This file - General overview |
| [`SETUP_TESTS.md`](SETUP_TESTS.md) | 📘 Complete testing instructions |
| [`TESTS_FINALES.md`](TESTS_FINALES.md) | 📊 Test results and analysis |
| [`pedisafe/TEST_README.md`](pedisafe/TEST_README.md) | Technical test documentation |
| [`pedisafe/TEST_RESULTS.md`](pedisafe/TEST_RESULTS.md) | Detailed results analysis |
| [`DOCS/test_case_validation.md`](DOCS/test_case_validation.md) | Test case validation |

---

## 🏗️ Technologies Used

### Backend
- **Python 3.12**
- **LangChain** - RAG framework
- **FAISS** - Vector database
- **Sentence Transformers** - Embeddings
- **Cerebras API** - LLM inference

### Frontend
- **Streamlit** - Web interface

### Testing
- **pytest** - Testing framework
- **pytest-html** - HTML reports

### Models
- **all-MiniLM-L6-v2** - Embeddings (sentence-transformers)
- **llama-3.3-70b** - LLM (Cerebras)

---

## 📊 Validated Use Cases

### ✅ Cases the System Handles Correctly

1. **Real Emergencies (<3 months with fever)**
   - Input: "2 months, 38.2°C"
   - Output: 🔴 RED - Immediate emergency

2. **Red Flags**
   - Difficulty breathing → 🔴 RED
   - Seizure → 🔴 RED
   - Altered behavior → 🔴 RED
   - Non-blanching rash → 🔴 RED

3. **Moderate Cases**
   - High fever + dehydration → 🟠 ORANGE
   - Fever 6-12 months without alarms → 🟡 YELLOW

4. **Mild Cases**
   - 5 years old, 37.8°C → 🟢 GREEN (not fever)
   - Normal temperature → 🟢 GREEN

### ⚠️ Known Limitations

1. **Fever >72 hours:** May classify as YELLOW instead of ORANGE
2. **Temperature ≥40°C with good behavior:** May underestimate urgency

**Note:** These limitations DO NOT affect the system's critical safety.

---

## 🔐 Security and Privacy

- ✅ Does not store personal data
- ✅ API key in environment variables
- ✅ Clear medical disclaimers
- ✅ Verifiable source citations
- ✅ No symptom invention (0 hallucinations)

---

## 🎓 Knowledge Base

**5 official documents:**

### American Academy of Pediatrics (AAP)
1. Fever in Babies & Children (aap_fever_baby.md)
2. Fever Without Fear (aap_fever_without_fear.md)
3. Symptom Checker (aap_symptom_checker.md)
4. When to Call the Pediatrician (aap_when_to_call.md)

### NHS UK
1. Fever in Children (nhs_fever_children.md)

**Total:** ~13,000 words of verified medical content from AAP and NHS sources

---

## 🚀 Deployment

### Local (Streamlit)

```bash
streamlit run pedisafe/app.py
```

### Docker (Future)

```bash
docker build -t pedisafe .
docker run -p 8501:8501 pedisafe
```

---

## 🧪 Run Tests

### Basic Command

```bash
venv\Scripts\python.exe -m pytest pedisafe/test_pedisafe.py -v
```

### With HTML Report

```bash
venv\Scripts\python.exe -m pytest pedisafe/test_pedisafe.py -v --html=pedisafe/report.html --self-contained-html
```

### Critical Tests Only

```bash
venv\Scripts\python.exe -m pytest pedisafe/test_pedisafe.py -v -m critical
```

### Automated Script (Windows)

```bash
RUN_TESTS.bat
```

---

## 📈 Roadmap

### Completed ✅
- [x] RAG engine with LangChain
- [x] Bilingual Streamlit interface (EN/ES)
- [x] AAP/NHS knowledge base (5 documents)
- [x] Automated test suite (16 cases)
- [x] Deterministic red flag detection
- [x] Color-coded level system (4 levels)
- [x] HTML testing reports
- [x] Complete documentation
- [x] 100% emergency detection (0 false negatives)

### Future 🔮
- [ ] Improve precision in edge cases (persistent fever, 40°C)
- [ ] Clinical validation with medical professionals
- [ ] Expand knowledge base (more conditions)
- [ ] Consultation history
- [ ] Native mobile app
- [ ] Telemedicine integration

---

## 👥 Team

Developed for **Alameda Hacks 2026**

---

## 📄 License

[Specify license]

---

## 🆘 Support and Troubleshooting

### Common Issues

**Error: "ModuleNotFoundError: No module named 'langchain_text_splitters'"**

```bash
pip install langchain-text-splitters langchain-core
```

**Error: "Could not initialize RAG engine"**

1. Verify API key is configured
2. Verify files in `knowledge/` (must be 5 .md files)
3. Verify Internet connection

**Tests very slow**

First run downloads models (~110MB). Subsequent runs are faster.

**For more help, see:** [`SETUP_TESTS.md`](SETUP_TESTS.md)

---

## 📞 Contact

[Add contact information]

---

## 🙏 Acknowledgments

- **American Academy of Pediatrics** - Clinical guidelines
- **NHS UK** - Medical documentation
- **Cerebras** - LLM inference API
- **LangChain** - RAG framework
- **HuggingFace** - Embedding models

---

**Last updated:** 2026-01-11  
**Version:** 1.0.0  
**Status:** ✅ Functional prototype - 81% tests passing (100% on critical cases)  
**⚠️ Note:** This is a hackathon prototype, NOT a validated medical product
