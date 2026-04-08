# 🌍 TerraLogic

**An agentic AI system that validates and corrects stale location data in the Overture Maps Places dataset**

---

## 📋 Overview

Open map data is only as powerful as it is accurate but businesses close, move, and change faster than any dataset can keep up with. TerraLogic solves this.

TerraLogic is an **agentic AI pipeline** that autonomously pulls Places data from the Overture Maps Foundation dataset, cross references each location against live web sources, and flags or proposes corrections for stale, incorrect, or outdated entries surfacing everything in a clean human-review dashboard.

This directly addresses one of Overture's own stated challenges: *"No one in mapping has fully solved the challenge of ensuring accurate, up-to-date data on places."*

---

## 👥 Team Members

| Name | GitHub |
|------|--------|
| Preetam Donepudi | @pdonepud |
| Devesh | @d-vesh |
| Ashmita | @duashmita |

---

## 🌟 Features

### 🤖 Agentic Validation Pipeline
- **Overture Places ingestion** — queries GeoParquet data via DuckDB or the Overture Python CLI for a target city/region
- **AI-powered cross-referencing** — an LLM agent checks each place against live web sources to detect closures, moved locations, wrong hours, or name changes
- **Confidence scoring** — each flagged entry receives a staleness score (0–1) with source citations
- **Correction proposals** — the agent generates structured, Overture-compatible correction suggestions

### 🖥️ Human-Review Dashboard
- **Web interface** for reviewing flagged locations on an interactive map
- **Approve / reject / skip** correction proposals with one click
- **Filter by confidence score**, category, or region
- **Export validated corrections** in GeoJSON / GeoParquet format for potential upstream contribution to Overture

### 📊 Analytics
- Track validation coverage over time
- Breakdown of error types (closed, moved, wrong name, wrong category)
- Per-region accuracy heatmaps

---

## 📁 Project Structure

```
terra-pulse/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
│
├── pipeline/
│   ├── ingest.py                # Pull Places data from Overture via DuckDB
│   ├── agent.py                 # AI validation agent (LLM + web search)
│   ├── scorer.py                # Confidence scoring logic
│   └── exporter.py              # Output corrections in Overture-compatible format
│
├── backend/
│   ├── api.py                   # FastAPI backend
│   ├── models.py                # Database models
│   └── requirements.txt         # Backend dependencies
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx              # Main React app
│   │   ├── components/          # Dashboard UI components
│   │   └── pages/               # Map view, review queue, analytics
│   └── package.json
│
└── docs/
    ├── index.html               # GitHub Pages landing page
    └── ARCHITECTURE.md          # System architecture and data flow
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- DuckDB

### 1. Clone the repo

```bash
git clone https://github.com/project-terraforma/terra-pulse.git
cd terra-pulse
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the validation pipeline

```bash
# Download Places data for a bounding box (example: San Francisco)
python pipeline/ingest.py --bbox="-122.51,37.70,-122.36,37.81"

# Run the AI validation agent
python pipeline/agent.py --input data/places.geojson

# View results
python pipeline/exporter.py --output results/flagged_places.geojson
```

### 4. Start the dashboard

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn api:app --reload

# Frontend (in a new terminal)
cd frontend
npm install
npm run dev
```

---

## 🛠️ Tech Stack

| Layer | Tools |
|---|---|
| Map Data | Overture Maps (GeoParquet, DuckDB, Python CLI) |
| AI Agent | Claude API (reasoning + web search tool) |
| Backend | Python / FastAPI |
| Frontend | React + Leaflet / MapLibre GL |
| Database | PostgreSQL + PostGIS |
| Deployment | Vercel (frontend) · Railway (backend) |

---

## 🗺️ How It Works

```
Overture Maps Places Data (GeoParquet)
            │
            ▼
    ┌─────────────────┐
    │  Ingest Module  │  ← Query via DuckDB / overturemaps CLI
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │   AI Agent      │  ← LLM cross-references each place against live web sources
    │  (Claude API)   │     (business status, hours, address, name)
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ Confidence      │  ← Scores each entry 0–1 for staleness
    │ Scorer          │     with source citations
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ Review Dashboard│  ← Human approves / rejects corrections
    └────────┬────────┘
             │
             ▼
    Overture-Compatible Correction Output (GeoJSON / GeoParquet)
```

---

## 📈 Roadmap

### Phase 1 — Core Pipeline ✅ (In Progress)
- [ ] Overture Places ingestion via DuckDB
- [ ] AI agent with web search cross-referencing
- [ ] Basic confidence scoring
- [ ] GeoJSON export

### Phase 2 — Dashboard 🚧
- [ ] React frontend with map view
- [ ] Review queue (approve / reject / skip)
- [ ] FastAPI backend + PostgreSQL
- [ ] Filter by region / confidence / category

### Phase 3 — Polish & Contribution 🔮
- [ ] Overture-compatible GeoParquet output
- [ ] Analytics & heatmaps
- [ ] GitHub Pages landing page
- [ ] Performance benchmarking vs known ground truth

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | System architecture and data flow |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to contribute |

---

## 🤝 Built For

This project was built for the **[Overture Maps Foundation](https://overturemaps.org)** as part of **Project Terraforma**, Spring 2026.

Overture Maps provides open, interoperable map data standardized across six themes — Addresses, Buildings, Places, Divisions, Transportation, and Base — and powers map products used by hundreds of millions of people worldwide.

---

## 📄 License

This project is licensed under the **Apache 2.0 License** — see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- **Overture Maps Foundation** for open, production-ready geospatial data
- **Project Terraforma** for the course framework and community
- **Anthropic** for the Claude API powering the validation agent

---

*Last Updated: April 2026*
