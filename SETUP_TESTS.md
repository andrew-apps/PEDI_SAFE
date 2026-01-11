# 🧪 Instructions to Recreate PediSafe Testing Environment

This document explains step by step how to configure and run PediSafe's automated test suite.

---

## 📋 Prerequisites

- **Python 3.12** or higher
- **Git** installed
- **Internet connection** (to download dependencies)
- **~2GB free space** (for PyTorch dependencies)

---

## 🚀 Initial Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd 1_ALAMEDA_HACKS
```

### 2. Create Virtual Environment (VENV)

#### On Windows:
```powershell
# Create venv
python -m venv venv

# Activate venv
venv\Scripts\activate

# Verify you're in the venv (you should see (venv) in the prompt)
```

#### On Linux/Mac:
```bash
# Create venv
python3 -m venv venv

# Activate venv
source venv/bin/activate
```

### 3. Install Base Dependencies

```bash
# Update pip
python -m pip install --upgrade pip

# Install main dependencies
pip install -r pedisafe/requirements.txt
```

### 4. Install Testing Dependencies

```bash
# Install testing tools
pip install pytest pytest-html

# Install LangChain components
pip install langchain-text-splitters langchain-core langchain-community langchain-openai

# Install embeddings and vectorstore
pip install sentence-transformers faiss-cpu
```

**Note:** Installing `sentence-transformers` will download ~110MB of PyTorch. This is normal and may take several minutes.

---

## ⚙️ API Key Configuration

### Option 1: Environment Variable (Recommended)

#### Windows:
```powershell
# Temporary (this session only)
$env:CEREBRAS_API_KEY="your-api-key-here"

# Permanent
setx CEREBRAS_API_KEY "your-api-key-here"
```

#### Linux/Mac:
```bash
# Add to ~/.bashrc or ~/.zshrc
export CEREBRAS_API_KEY="your-api-key-here"

# Load the change
source ~/.bashrc
```

### Option 2: .env File

```bash
# Create .env file in pedisafe/ folder
echo "CEREBRAS_API_KEY=your-api-key-here" > pedisafe/.env
```

**Note:** The default API key in tests is: `csk-59knkfwehxxxckxcdw8f56mjxj3v8f6hm3239rtnxwf6cmjf`

---

## 🧪 Run Tests

### Option 1: Direct Command

```bash
# Make sure you're in the project root
cd d:\PROYECTOS\HACKATONES\1_DEVPOST\1_ALAMEDA_HACKS

# Activate venv (if not activated)
venv\Scripts\activate

# Run all tests
venv\Scripts\python.exe -m pytest pedisafe/test_pedisafe.py -v

# Run only critical tests
venv\Scripts\python.exe -m pytest pedisafe/test_pedisafe.py -v -m critical

# Generate HTML report
venv\Scripts\python.exe -m pytest pedisafe/test_pedisafe.py -v --html=pedisafe/report.html --self-contained-html
```

### Option 2: Batch Script (Windows)

```bash
# Run the provided script
RUN_TESTS.bat
```

### Option 3: Makefile (Linux/Mac)

```bash
# Create a simple Makefile
make test
```

---

## 📊 Interpret Results

### Test States

- ✅ **PASSED** - Successful test
- ❌ **FAILED** - Failed test (see details in output)
- ⏭️ **SKIPPED** - Skipped test (usually due to missing configuration)

### Output Example

```
============================================== test session starts ==============================================
platform win32 -- Python 3.12.1, pytest-9.0.2, pluggy-1.6.0
collected 16 items

pedisafe\test_pedisafe.py::test_critical_cases[Fever <3 months] PASSED                                    [  6%]
pedisafe\test_pedisafe.py::test_critical_cases[Red flag symptom] PASSED                                   [ 12%]
...
============================= 13 passed, 2 failed, 1 skipped in 38.25s ==============================
```

### HTML Report

After running with `--html=pedisafe/report.html`, open the file in a browser:

```bash
# Windows
start pedisafe/report.html

# Linux
xdg-open pedisafe/report.html

# Mac
open pedisafe/report.html
```

---

## 📁 Testing File Structure

```
1_ALAMEDA_HACKS/
├── pedisafe/
│   ├── test_pedisafe.py          # Main test suite
│   ├── test_rag_simple.py        # Simple diagnostic test
│   ├── pytest.ini                # Pytest configuration
│   ├── report.html               # Generated HTML report
│   ├── TEST_README.md            # Test documentation
│   └── TEST_RESULTS.md           # Results and analysis
├── RUN_TESTS.bat                 # Windows execution script
├── TESTS_FINALES.md              # Results summary
└── SETUP_TESTS.md                # This file
```

---

## 🔍 Included Test Cases

### Critical Safety Tests (8 cases)

1. **Fever in babies <3 months** (3 variants)
   - 2 months, 38.2°C → Must be RED
   - 1 month, 38.0°C → Must be RED
   - 10 weeks → Must be RED

2. **Emergency red flags**
   - Difficulty breathing → RED
   - Seizure → RED
   - High fever + dehydration → ORANGE

3. **Moderate/low fever**
   - 6-12 months without alarm signs → YELLOW
   - 5 years old with low fever → GREEN

### Edge Cases (4 cases)

- Persistent fever >72 hours
- High temperature with good behavior
- Altered behavior
- Non-blanching rash

### False Positive Validation (2 cases)

- 37.8°C is NOT fever → GREEN
- 37.5°C normal temperature → GREEN

### System Validation (2 cases)

- AAP/NHS source citations
- Presence of disclaimers

---

## ⚠️ Common Issues and Solutions

### Error: "No module named 'langchain_text_splitters'"

**Solution:**
```bash
venv\Scripts\python.exe -m pip install langchain-text-splitters langchain-core
```

### Error: "No module named 'sentence_transformers'"

**Solution:**
```bash
venv\Scripts\python.exe -m pip install sentence-transformers
```

### Error: "Could not initialize RAG engine"

**Possible causes:**
1. API key not configured
2. No Internet connection
3. Missing knowledge base files

**Verify:**
```bash
# Verify .md files exist in knowledge/
dir pedisafe\knowledge\*.md

# Should list 5 files:
# - aap_fever_baby.md
# - aap_fever_without_fear.md
# - aap_symptom_checker.md
# - aap_when_to_call.md
# - nhs_fever_children.md
```

### Error: "pytest: command not found"

**Solution:**
```bash
# Use Python module instead of direct command
venv\Scripts\python.exe -m pytest ...
```

### Tests very slow (>2 minutes)

**Causes:**
- First run downloading embedding models
- FAISS index generation

**Solution:** First run is slow. Subsequent runs will be faster.

---

## 🔄 Update Dependencies

```bash
# Activate venv
venv\Scripts\activate

# Update all dependencies
pip install --upgrade -r pedisafe/requirements.txt
pip install --upgrade pytest pytest-html sentence-transformers

# Verify installed versions
pip list
```

---

## 🧹 Clean and Recreate Environment

### If something goes wrong, recreate from scratch:

```bash
# 1. Deactivate venv
deactivate

# 2. Remove venv
rmdir /s /q venv

# 3. Recreate venv
python -m venv venv
venv\Scripts\activate

# 4. Reinstall everything
pip install --upgrade pip
pip install -r pedisafe/requirements.txt
pip install pytest pytest-html
pip install langchain-text-splitters langchain-core langchain-community langchain-openai
pip install sentence-transformers faiss-cpu

# 5. Run tests
venv\Scripts\python.exe -m pytest pedisafe/test_pedisafe.py -v
```

---

## 📊 Success Criteria

To consider the system ready:

✅ **Minimum 80% tests passing** (13/16 or better)  
✅ **100% critical <3 months tests passing** (0 false negatives)  
✅ **0 hallucinations detected**  
✅ **AAP/NHS sources correctly cited**

---

## 📝 Additional Notes

### Git Ignore

The `.gitignore` file is already configured to ignore:
- `venv/`
- `__pycache__/`
- `.pytest_cache/`
- `*.pyc`
- `.env`

### Expected Runtime

- **First run:** 50-90 seconds (model download)
- **Subsequent runs:** 30-40 seconds
- **Critical tests only:** 15-20 seconds

### System Resources

- **RAM:** ~2GB during test execution
- **Disk space:** ~1.5GB for venv with all dependencies
- **CPU:** Normal usage (no GPU required)

---

## 🆘 Support

If you encounter problems:

1. Verify venv is activated
2. Confirm all dependencies are installed
3. Review complete error logs
4. Check `TEST_README.md` for test details
5. Review `TESTS_FINALES.md` for expected results

---

## ✅ Verification Checklist

Before reporting tests are working:

- [ ] Venv created and activated
- [ ] All dependencies installed without errors
- [ ] API key configured
- [ ] 5 .md files present in `knowledge/` (AAP: 4, NHS: 1)
- [ ] Tests running without import errors
- [ ] At least 13/16 tests passing
- [ ] `report.html` generated correctly
- [ ] Report opens in browser and shows results

---

**Last updated:** 2026-01-09  
**Tested Python version:** 3.12.1  
**Tested platform:** Windows 10  
**Status:** ✅ Working
