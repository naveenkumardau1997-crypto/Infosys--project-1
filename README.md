# 🛡️ Online Exam Monitoring & Integrity Analytics Platform

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0.3-black?logo=flask)
![Streamlit](https://img.shields.io/badge/Streamlit-1.36-red?logo=streamlit)
![OpenCV](https://img.shields.io/badge/OpenCV-4.9-green?logo=opencv)
![LangChain](https://img.shields.io/badge/LangChain-0.2-purple)
![SQLite](https://img.shields.io/badge/SQLite-3-blue?logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-yellow)

**An AI-powered, webcam-based examination monitoring system combining Computer Vision, Data Science, and Natural Language Generation to ensure academic integrity in online assessments.**

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Technology Stack](#-technology-stack)
- [Installation Guide](#-installation-guide)
- [Running the Project](#-running-the-project)
- [Folder Structure](#-folder-structure)
- [Screenshots](#-screenshots)
- [API Overview](#-api-overview)
- [Database Schema](#-database-schema)
- [AI Workflow](#-ai-workflow)
- [Analytics Workflow](#-analytics-workflow)
- [Future Improvements](#-future-improvements)
- [Contributors](#-contributors)
- [License](#-license)

---

## 🧭 Overview

The **Online Exam Monitoring & Integrity Analytics Platform** is a Python-based intelligent examination monitoring system designed to assist educational institutions in conducting secure, transparent, and integrity-focused online assessments.

The platform combines **Computer Vision**, **Artificial Intelligence**, **Data Science**, and **Web Technologies** to help invigilators monitor examination sessions in real time and generate meaningful insights rather than making automated disciplinary decisions.

### What it does:
- 🎥 **Webcam-based face presence monitoring** using OpenCV Haar Cascade classifiers
- 🌐 **Browser activity tracking** — detects focus loss and tab switching in real time
- 📊 **Suspicious event recording** with a rule-based integrity scoring engine
- 🤖 **Natural language integrity reports** powered by LangChain and LLM integration
- 📈 **Cohort-level analytics** — clustering, heatmaps, event distributions, and risk profiling
- 📤 **JSON and CSV export** for reporting and audit trails

---

## ✨ Features

### 1. 🔐 Candidate Authentication & Session Management
- **Registration** — Candidates register with name, email, mobile, and password
- **Photo Capture** — Webcam-based photo is taken and saved at registration time
- **Secure Login** — Passwords are hashed using Werkzeug's PBKDF2 algorithm
- **Session Lifecycle** — Flask sessions maintain the active exam state with a live timer

### 2. 🎥 Face Presence Monitoring
- **Webcam Detection** — Captures a webcam frame every 3 seconds using the browser's `MediaDevices` API
- **OpenCV Haar Cascade** — Frames are sent to the Flask backend, decoded from base64, and analyzed using `haarcascade_frontalface_default.xml`
- **Face Absence Logging** — If no face is detected in a frame, a `Face Absence` event is recorded to the database with a timestamp

### 3. 🌐 Browser Activity Logging
- **Focus Loss Detection** — Fires when the exam window loses focus (e.g., Alt-Tab)
- **Tab Switching Detection** — Uses the `Page Visibility API` to detect when the candidate navigates away
- **Timestamp Logging** — All browser events are persisted to `incident_logs` with ISO timestamps via the `/api/log_event` REST endpoint

### 4. ⚠️ Suspicious Event Detection
- **Rule-Based Threshold Engine** — The candidate dashboard displays live counters for Focus Losses, Tab Switches, and Face Absences
- **Colour-coded Status** — Green (clean), Yellow (low activity), Red (high activity) — giving immediate visual feedback
- **Backend Storage** — All events are stored in SQLite for later analytics

### 5. 📊 Integrity Scoring
- **Weighted Scoring** — Starts at 100, deducts points per event:
  - Face Absence: **-15 pts**
  - Tab Switch: **-10 pts**
  - Focus Loss: **-5 pts**
- **Risk Labels**:
  - 🟢 **Low** — Score ≥ 75
  - 🟡 **Medium** — Score 50–74
  - 🔴 **High** — Score < 50
- Exposed via `/api/integrity/<candidate_id>` REST endpoint

### 6. 🤖 AI Integrity Report
- **LangChain Integration** — Uses `LLMChain` with a structured `PromptTemplate` to generate professional integrity reports
- **OpenAI/LLM Support** — If `OPENAI_API_KEY` is set in environment, uses OpenAI GPT for generation
- **Automatic Fallback** — If no API key is present, generates a detailed, rule-based structured report covering Executive Summary, Key Findings, and Recommendations
- Reports are saved to the `integrity_reports` table and can be exported as JSON

### 7. 📈 Data Science Analytics (Streamlit Dashboard)
- **Integrity Score Distribution** — Histogram of score spread across the cohort
- **Risk Pie Chart** — Visual breakdown of Low / Medium / High risk candidates
- **Event Distribution Bar Chart** — Count of each suspicious event type across the session
- **Heatmaps** — Seaborn heatmap showing suspicious events by hour of day vs candidate name
- **K-Means Clustering** — Groups candidates into 3 risk clusters using scikit-learn with StandardScaler normalisation; visualised as a scatter plot
- **Risk Profiling Table** — Full candidate table with scores, risk labels, cluster assignments, and event counts

### 8. 🗂️ Alert & Evidence Storage
- **Screenshot Storage** — Candidate registration photos stored in `static/uploads/`
- **Incident Logs** — All events stored in `incident_logs` table with candidate ID, event type, description, and timestamp

### 9. 🖥️ Streamlit Invigilator Dashboard
- **Live Monitoring** — KPI cards showing total candidates, total logs, average score, and high-risk count
- **Demo Data Generator** — Faker-powered button to populate the database with realistic test data
- **Cohort View** — All analytics charts on one page
- **Candidate View** — Individual integrity profile with full log history and AI report generation
- **Exports** — CSV and JSON downloads directly from the UI

### 10. 📤 Reporting
- **JSON Export** — Per-candidate JSON report with identity, score, risk label, AI narrative, and full event log
- **CSV Export** — Cohort-level CSV with all candidates' scores, risks, and event counts

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    CANDIDATE BROWSER                     │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐  │
│  │  Login Page  │  │  Register    │  │  Exam Dashboard│  │
│  │  index.html  │  │  register    │  │  dashboard     │  │
│  │              │  │  .html       │  │  .html         │  │
│  └──────┬───────┘  └──────┬───────┘  └───────┬────────┘  │
│         │                 │                  │            │
│         │      Webcam Frames (base64)         │            │
│         │      Browser Events (JSON)          │            │
└─────────┼─────────────────┼──────────────────┼────────────┘
          │                 │                  │
          ▼                 ▼                  ▼
┌─────────────────────────────────────────────────────────┐
│                   FLASK BACKEND (app.py)                  │
│                                                          │
│  /          /register   /login   /dashboard   /logout    │
│  /api/monitor           /api/log_event                   │
│  /api/integrity/<id>    /api/logs/<id>                   │
│                                                          │
│  ┌─────────────────┐   ┌──────────────────────────────┐  │
│  │  OpenCV Face    │   │  Werkzeug Password Hashing    │  │
│  │  Detection      │   │  Flask Sessions               │  │
│  │  (Haar Cascade) │   │                              │  │
│  └────────┬────────┘   └──────────────────────────────┘  │
└───────────┼─────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────┐
│                   SQLITE DATABASE                         │
│                                                          │
│  candidates │ incident_logs │ integrity_reports          │
└─────────────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────┐
│              STREAMLIT DASHBOARD (dashboard.py)           │
│                                                          │
│  Cohort Analytics          Candidate Detail              │
│  ─────────────────          ─────────────────            │
│  Score Distribution         Candidate Profile            │
│  Risk Pie Chart             Incident Logs Table          │
│  Event Bar Chart            Integrity Score              │
│  Seaborn Heatmap            LangChain AI Report          │
│  K-Means Clustering         JSON/CSV Export              │
└─────────────────────────────────────────────────────────┘
```

---

## 💻 Technology Stack

| Layer | Technology | Version | Purpose |
|---|---|---|---|
| **Backend** | Python | 3.11 | Core language |
| **Backend** | Flask | 3.0.3 | REST API and HTML rendering |
| **Backend** | Werkzeug | 3.0.3 | Password hashing, WSGI utilities |
| **Computer Vision** | OpenCV | 4.9.0 | Face detection via Haar Cascade |
| **AI** | LangChain | 0.2.6 | LLM orchestration and prompt templates |
| **AI** | LangChain Community | 0.2.6 | LLM provider integrations |
| **Database** | SQLite | Built-in | Candidate records and incident logs |
| **Dashboard** | Streamlit | 1.36.0 | Invigilator analytics interface |
| **Data Science** | Pandas | 2.2.2 | Tabular data manipulation |
| **Data Science** | NumPy | 1.26.4 | Numerical computation |
| **Data Science** | Matplotlib | 3.9.0 | Chart and plot rendering |
| **Data Science** | Seaborn | 0.13.2 | Statistical heatmaps |
| **Data Science** | Scikit-learn | 1.5.0 | K-Means clustering |
| **Utilities** | Faker | 26.0.0 | Demo data generation |
| **Utilities** | langdetect | 1.0.9 | Language detection utility |
| **Dev Tools** | Black | 24.4.2 | Code formatting |
| **Dev Tools** | isort | 5.13.2 | Import sorting |

---

## 📦 Installation Guide

### Prerequisites

- Python 3.11 or higher
- pip (comes with Python)
- Git (to clone the repository)
- A webcam (for face monitoring during exams)

### Step 1: Clone the Repository

```bash
git clone https://github.com/jatin009v/Infosys-project-1
cd Infosys-project-1
```

### Step 2: Create a Virtual Environment

```bash
# Windows
python -m venv venv

# macOS / Linux
python3 -m venv venv
```

### Step 3: Activate the Virtual Environment

```bash
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Windows (Command Prompt)
.\venv\Scripts\activate.bat

# macOS / Linux
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Fix Haar Cascade (one-time setup)

The Haar Cascade XML is automatically sourced from OpenCV's installed data directory. If you ever need to refresh it:

```bash
python -c "import cv2, shutil; shutil.copy(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml', 'data/haarcascades/haarcascade_frontalface_default.xml')"
```

### Step 6: (Optional) Set LLM API Key

To enable AI-generated reports using an LLM instead of the built-in rule-based generator:

```bash
# Windows PowerShell
$env:OPENAI_API_KEY = "sk-..."

# macOS / Linux
export OPENAI_API_KEY="sk-..."
```

> If no key is set, the system automatically uses the built-in structured report generator — no configuration required.

---

## 🚀 Running the Project

### Initialize the Database

The database is automatically initialized when Flask starts. No manual step needed.

To verify manually:

```bash
python -c "import app; print('Database initialized OK')"
```

### Start the Flask Backend

```bash
# Make sure venv is activated
.\venv\Scripts\Activate.ps1

python app.py
```

Flask will start at: **http://localhost:5000**

### Start the Streamlit Dashboard (new terminal)

```bash
# Make sure venv is activated
.\venv\Scripts\Activate.ps1

streamlit run dashboard.py
```

Streamlit will start at: **http://localhost:8501**

### Quick Start (Both Simultaneously)

Open **two PowerShell terminals**, activate the venv in both, and run:

- **Terminal 1:** `python app.py`
- **Terminal 2:** `streamlit run dashboard.py`

---

## 📁 Folder Structure

```
Infosys--project-1-main/
│
├── app.py                          # Flask backend (main application)
├── dashboard.py                    # Streamlit invigilator dashboard
├── database.db                     # SQLite database file
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
│
├── data/
│   └── haarcascades/
│       └── haarcascade_frontalface_default.xml   # OpenCV face detector
│
├── static/
│   ├── css/
│   │   └── style.css               # Glassmorphism UI styles
│   ├── js/
│   │   └── script.js               # Frontend interactivity
│   └── uploads/                    # Candidate registration photos
│
├── templates/
│   ├── index.html                  # Login page
│   ├── register.html               # Candidate registration page
│   └── dashboard.html              # Candidate exam dashboard
│
└── venv/                           # Python virtual environment (not committed)
```

---

## 📸 Screenshots

> The following screenshots demonstrate the platform's key interfaces.

### Login Page
![Login Page](static/uploads/screenshot_login.png)

> *AI-powered secure authentication with animated glassmorphism UI.*

### Candidate Registration
![Registration Page](static/uploads/screenshot_register.png)

> *Candidate registration with live webcam photo capture.*

### Exam Dashboard
![Exam Dashboard](static/uploads/screenshot_dashboard.png)

> *Real-time monitoring dashboard with face detection status, live counters, and session timer.*

### Streamlit Analytics
![Streamlit Analytics](static/uploads/screenshot_analytics.png)

> *Cohort analytics with integrity score distributions, heatmaps, and K-Means clustering.*

---

## 🔌 API Overview

All APIs require an active Flask session (candidate must be logged in).

### Authentication Routes

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Home / login page |
| `GET` | `/register` | Candidate registration form |
| `POST` | `/register` | Submit registration (with photo) |
| `POST` | `/login` | Authenticate candidate |
| `GET` | `/dashboard` | Candidate exam dashboard |
| `GET` | `/logout` | Clear session and redirect |

### Monitoring APIs

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/api/monitor` | ✅ Session | Send webcam frame for face detection |
| `POST` | `/api/log_event` | ✅ Session | Log a browser event |
| `GET` | `/api/integrity/<candidate_id>` | ✅ Session | Get integrity score |
| `GET` | `/api/logs/<candidate_id>` | ✅ Session | Get all incident logs |

### Request / Response Examples

#### `POST /api/monitor`
```json
// Request
{ "frame": "data:image/png;base64,iVBORw0KGgo..." }

// Response
{ "face_detected": true, "face_count": 1 }
```

#### `POST /api/log_event`
```json
// Request
{ "event_type": "Tab Switch", "description": "Candidate switched tabs" }

// Response
{ "status": "logged" }
```

#### `GET /api/integrity/1`
```json
{ "candidate_id": 1, "score": 75.0, "risk_label": "Low" }
```

---

## 🗄️ Database Schema

### Table: `candidates`

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique candidate ID |
| `fullname` | TEXT | — | Full name |
| `email` | TEXT | UNIQUE | Email address (used for login) |
| `mobile` | TEXT | — | Mobile number |
| `password` | TEXT | — | PBKDF2 hashed password |
| `photo` | TEXT | — | Path to registration photo |

### Table: `incident_logs`

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Log entry ID |
| `candidate_id` | INTEGER | FOREIGN KEY → candidates.id | Associated candidate |
| `event_type` | TEXT | — | `Face Absence`, `Tab Switch`, `Focus Loss` |
| `description` | TEXT | — | Human-readable event detail |
| `timestamp` | TEXT | — | ISO format datetime string |

### Table: `integrity_reports`

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Report entry ID |
| `candidate_id` | INTEGER | FOREIGN KEY → candidates.id | Associated candidate |
| `integrity_score` | REAL | — | Computed score (0–100) |
| `risk_label` | TEXT | — | `Low`, `Medium`, or `High` |
| `report_text` | TEXT | — | Full AI-generated report text |
| `generated_at` | TEXT | — | Report generation timestamp |

---

## 🤖 AI Workflow

### How LangChain Generates Integrity Reports

```
Incident Logs (SQLite)
        │
        ▼
Event Aggregation
  ┌─────────────────────────────────────┐
  │  Face Absences:  N × (-15 pts)      │
  │  Tab Switches:   N × (-10 pts)      │
  │  Focus Losses:   N × (-5 pts)       │
  └─────────────────────────────────────┘
        │
        ▼
Integrity Score Calculation
  score = max(0, 100 - total_deductions)
  risk_label = Low / Medium / High
        │
        ▼
LangChain PromptTemplate
  ┌──────────────────────────────────────────────────────┐
  │  Input Variables:                                     │
  │    - candidate name                                   │
  │    - integrity score                                  │
  │    - risk label                                       │
  │    - face_absences, tab_switches, focus_losses        │
  │                                                      │
  │  Template: Professional exam integrity analyst prompt │
  └──────────────────────────────────────────────────────┘
        │
        ├── If OPENAI_API_KEY set ──► OpenAI GPT LLM
        │                              (langchain_community.llms.OpenAI)
        │
        └── If no API key ──────────► Rule-Based Structured Generator
                                       (built-in fallback, no API needed)
        │
        ▼
Integrity Report Text
  ┌──────────────────────────────────────────────────────┐
  │  - Executive Summary                                  │
  │  - Key Findings (per event type with point impact)    │
  │  - Recommendation                                     │
  └──────────────────────────────────────────────────────┘
        │
        ▼
Saved to integrity_reports table + available for JSON export
```

---

## 📊 Analytics Workflow

### Integrity Score Calculation

Each candidate starts with a perfect score of **100**. For each suspicious event recorded during their session, a weighted deduction is applied:

| Event | Deduction per occurrence |
|---|---|
| Face Absence | -15 pts |
| Tab Switch | -10 pts |
| Focus Loss | -5 pts |

The final score is clamped to a minimum of **0** and mapped to a risk label:
- `score ≥ 75` → 🟢 **Low Risk**
- `50 ≤ score < 75` → 🟡 **Medium Risk**
- `score < 50` → 🔴 **High Risk**

### Heatmaps

The suspicious events heatmap uses **Seaborn's `sns.heatmap`** to visualise event frequency across:
- **Y-axis** — candidate first names
- **X-axis** — hour of day (0–23)

This helps invigilators identify peak suspicious activity periods and individual outliers.

### K-Means Clustering

1. A **feature matrix** is built for each candidate with three dimensions:
   - `face_absence_count`
   - `tab_switch_count`
   - `focus_loss_count`
2. Features are **standardised** using `sklearn.preprocessing.StandardScaler`
3. **K-Means** (`n_clusters=3`, `random_state=42`) partitions candidates into 3 groups
4. Cluster centroids are ranked by **overall severity** (sum of standardised centroid values) and mapped to **Low Risk / Medium Risk / High Risk** labels
5. Visualised as a 2D scatter plot (Tab Switches vs Face Absences)

### Risk Profiling

The final risk profile for each candidate combines:
- Computed integrity score
- Rule-based risk label (Low / Medium / High)
- K-Means cluster assignment
- Full event log table

This multi-dimensional profile is displayed in the Streamlit Candidate Detail page and exported to JSON.

---

## 🔮 Future Improvements

1. **Multiple Face Detection** — Flag when multiple faces appear (potential impersonation)
2. **Audio Monitoring** — Detect background noise or conversation during exams
3. **Gaze Tracking** — Use eye-tracking to detect off-screen gaze direction
4. **Real-Time Push Alerts** — WebSocket-based live alerts to invigilator dashboard
5. **Role-Based Access** — Separate admin and invigilator roles with permission control
6. **LLM Model Selection** — UI control to switch between OpenAI, Gemini, or local models
7. **PDF Report Generation** — Export formatted PDF reports using `reportlab` or `WeasyPrint`
8. **Exam Question Engine** — Integrate a question bank with timed exam delivery
9. **Containerisation** — Docker + Docker Compose for one-command deployment
10. **Cloud Deployment** — AWS/GCP/Heroku deployment guide with environment configuration
11. **Email Alerts** — Automated alerts to invigilators when a candidate reaches high-risk threshold
12. **Audit Log Export** — Signed, tamper-evident CSV exports for institutional records

---

## 👥 Contributors

### Jatin Gupta
GitHub: [github.com/jatin009v](https://github.com/jatin009v)

### Naveen Kumar
GitHub: [github.com/naveenkumardau1997](https://github.com/naveenkumardau1997)

---

## 📄 License

```
MIT License

Copyright (c) 2024 Jatin Gupta, Naveen Kumar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
