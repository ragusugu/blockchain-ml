# 📁 Project Structure & Organization Guide

## Complete Directory Tree

```
blockchain-ml/
│
├── 📄 README Files (Root Level - Start Here)
│   ├── install.sh              # Quick installation script
│   ├── requirements.txt        # Python dependencies
│   └── .gitignore              # Git ignore rules
│
├── 🐳 Docker & Infrastructure (Root Level)
│   ├── Dockerfile              # Container image definition
│   ├── docker-compose.yml      # Services orchestration
│   └── .dockerignore           # Docker ignore rules
│
├── 📂 src/ (Source Code - Core Logic)
│   ├── extract.py              # Phase 1: Extract blockchain data
│   ├── transform.py            # Phase 2: Transform & validate
│   ├── fetch_and_store.py      # Simple ETL runner
│   ├── main_etl.py             # Batch ETL orchestration
│   ├── scheduler.py            # Automated cron scheduler
│   └── test_etl.py             # Validation test suite
│
├── 📚 docs/ (Documentation)
│   ├── START_HERE.md           # 👈 Read this first!
│   ├── README.md               # Project overview
│   ├── QUICKSTART.md           # 60-second setup
│   ├── SCHEDULING_GUIDE.md     # Automation options
│   ├── ETL_PIPELINE.md         # Technical deep-dive
│   ├── ARCHITECTURE.md         # System design & flows
│   ├── DEPLOYMENT_GUIDE.md     # Production deployment
│   ├── PROJECT_COMPLETE.md     # Project status
│   └── IMPLEMENTATION_CHECKLIST.md  # Feature list
│
├── ⚙️ config/ (Configuration & Scripts)
│   ├── requirements.txt        # Dependencies (copy at root)
│   ├── .env                    # Environment variables
│   ├── .dockerignore           # Docker ignore (copy at root)
│   ├── Dockerfile              # Container definition (copy at root)
│   ├── docker-compose.yml      # Services config (copy at root)
│   └── install.sh              # Setup script (copy at root)
│
└── 🔄 venv/ (Virtual Environment)
    └── [Python packages]
```

---

## 📋 File Organization by Purpose

### 1. **Getting Started** (Start Here First!)
```
Root Level:
├── install.sh              → Run: bash install.sh
├── README.md               → Overview & quick links
├── QUICKSTART.md           → 60-second setup
└── START_HERE.md           → Portfolio-ready quick ref
```

### 2. **Source Code** (All Python Logic)
```
src/
├── extract.py              → Get blockchain data
├── transform.py            → Clean & validate data
├── fetch_and_store.py      → Single-block ETL
├── main_etl.py             → Batch orchestration
├── scheduler.py            → Automated scheduler
└── test_etl.py             → Validation tests
```

### 3. **Documentation** (Understanding the System)
```
docs/
├── ETL_PIPELINE.md         → How ETL works (technical)
├── ARCHITECTURE.md         → System design (diagrams)
├── DEPLOYMENT_GUIDE.md     → Production deployment
├── SCHEDULING_GUIDE.md     → Automation setup
└── PROJECT_COMPLETE.md     → Status & checklist
```

### 4. **Configuration** (Settings & Deployment)
```
config/
├── requirements.txt        → Python packages
├── .env                    → Environment variables
├── Dockerfile              → Container image
├── docker-compose.yml      → Multi-container setup
└── install.sh              → Installation script
```

---

## 🚀 Quick Navigation

| Need | Location | Command |
|------|----------|---------|
| **Get Started** | `docs/START_HERE.md` | Read first |
| **Install** | `install.sh` | `bash install.sh` |
| **Run ETL** | `src/main_etl.py` | `python src/main_etl.py` |
| **Schedule** | `src/scheduler.py` | `python src/scheduler.py` |
| **Docker** | Root level | `docker-compose up` |
| **Tests** | `src/test_etl.py` | `python src/test_etl.py` |
| **Config** | `config/.env` | Edit settings |
| **Docs** | `docs/` | Read guides |

---

## 📊 File Statistics

| Category | Files | Type | Purpose |
|----------|-------|------|---------|
| **Source Code** | 6 | `.py` | Core ETL logic |
| **Documentation** | 9 | `.md` | Guides & references |
| **Configuration** | 6 | Various | Settings & deployment |
| **Total** | 21 | Mixed | Complete project |

---

## 🔐 .gitignore Structure

```
Root .gitignore:
├── venv/                   # Virtual environment
├── __pycache__/            # Python cache
├── .env                    # Local secrets
├── *.log                   # Log files
└── .vscode/                # IDE settings
```

---

## 📦 Copy-At-Root Pattern

**Why some files are at both root and config/**:

```
Docker needs these at root:
├── Dockerfile              ✓ At root (Docker reads from root)
├── docker-compose.yml      ✓ At root (Docker reads from root)
└── .dockerignore           ✓ At root (Docker reads from root)

Also in config/:
├── Dockerfile              (backup)
├── docker-compose.yml      (backup)
├── .dockerignore           (backup)
└── install.sh              (to update paths easily)
```

---

## 🎯 Working with the Structure

### Running Locally
```bash
cd /home/sugangokul/Desktop/blockchain-ml

# Setup once
bash install.sh

# Run ETL
python src/main_etl.py

# Or schedule it
python src/scheduler.py

# Or test
python src/test_etl.py
```

### Using Docker
```bash
cd /home/sugangokul/Desktop/blockchain-ml

# Build & run
docker-compose up --build

# View logs
docker-compose logs -f scheduler
```

### Reading Documentation
```bash
cd /home/sugangokul/Desktop/blockchain-ml/docs

# Start with:
cat START_HERE.md

# Then read:
cat QUICKSTART.md
cat SCHEDULING_GUIDE.md
```

### Modifying Code
```bash
cd /home/sugangokul/Desktop/blockchain-ml/src

# Edit any Python file
nano extract.py
nano transform.py
nano main_etl.py

# Changes work immediately
python main_etl.py
```

---

## 🔄 Import Paths

**Inside src/ files:**
```python
# These work automatically:
from extract import extract_block
from transform import transform_data
from main_etl import BlockchainETL
```

**From root level:**
```bash
# Add to PYTHONPATH:
export PYTHONPATH=/path/to/src:$PYTHONPATH
python -c "from extract import extract_block"
```

---

## 📝 Adding New Files

**Adding new Python module:**
```bash
# Put in src/
src/new_module.py
```

**Adding new documentation:**
```bash
# Put in docs/
docs/TOPIC.md
```

**Adding new config:**
```bash
# Put in config/
config/new_config.yml
```

---

## ✅ Organization Benefits

✓ **Clear separation** - Code, docs, config in separate folders  
✓ **Easy navigation** - Know exactly where to find things  
✓ **Docker ready** - Root level has what Docker needs  
✓ **Scalable** - Easy to add more files without clutter  
✓ **Professional** - Looks like a real project  
✓ **Maintainable** - Everyone knows the structure  

---

## 📞 Quick Reference

```
STRUCTURE SUMMARY:

ROOT/
├── Executable scripts (install.sh)
├── Docker files (Dockerfile, docker-compose.yml)
├── Python deps (requirements.txt)
│
├── src/          → 6 Python files (core logic)
├── docs/         → 9 Markdown files (documentation)
└── config/       → Configuration & backups

Total: ~21 files, fully organized
```

---

This structure is **production-ready**, **easy to navigate**, and **perfect for portfolio** 🚀
