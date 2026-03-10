# Rakshita - Smart Civic Grievance & Prioritization Engine

## Overview

Rakshita is an intelligent civic complaint management system designed to replace traditional FIFO (First-In-First-Out) ticket queues with an AI-driven Prioritization Engine. It evaluates the severity and credibility of citizen reports in real-time, assigning actionable priority levels, and routes them to the correct ward officers via a Geo-Mapping Dashboard.

## Key Features

- **Intelligent Intake:** Public-facing endpoints that ingest complaints and trigger the ML pipeline synchronously or asynchronously.
- **Prioritization Engine:** The core system brain that fuses ML-derived Severity and ML/Rule-derived Credibility to compute a final Priority Score.
- **System-Level Explainability:** Generates human-readable JSON payloads explaining SHAP-derived keyword triggers and rule-based penalties applied.
- **Geo-Mapping Dashboard:** A fast, lightweight frontend using HTML/CSS/Vanilla JS, Chart.js, and mapping tools for civic officers.
- **Role-Based Access Control (RBAC):** JWT-secured endpoints ensuring officers only access and mutate state for their assigned jurisdictions.

## Tech Stack

- **Backend:** FastAPI (Python 3.10+)
- **Database:** PostgreSQL (accessed via SQLAlchemy ORM)
- **Data Validation:** Pydantic
- **Machine Learning / Intelligence:** Scikit-learn, XGBoost, SHAP
- **Frontend:** HTML, CSS, Vanilla JS
- **Deployment:** Docker, Docker Compose, AWS EC2 (Ubuntu)

## Project Structure

```text
/rakshita-backend
├── /api               # API routing (e.g., routes_complaints.py, routes_auth.py)
├── /core              # Core configurations and security (JWT logic)
├── /db                # Database configurations and SQLAlchemy models
├── /ml                # ML functions and predictive models (Severity, Credibility, Preprocessor)
├── /services          # Business logic and the Priority Engine
├── /static            # Frontend assets (Vanilla JS, CSS, HTML)
├── main.py            # FastAPI application entry point
└── docker-compose.yml # Containerization setup
```

## State Management

Complaints strictly follow this lifecycle:
`PENDING` -> `ASSIGNED` -> `IN_PROGRESS` -> `RESOLVED`

## ML Logic & Prioritization

The Priority Engine evaluates complaints based on two primary models:
1. **Severity Model:** Detects danger or threat level (0.0 to 1.0).
2. **Credibility Model:** Evaluates structural coherence and detail richness using NLP and rule-based penalties for spam.

**Standard Priority Formula:**
`Priority = (0.7 * Severity) + (0.3 * Credibility)`

*(An Emergency Override applies if Severity > 0.85, setting Priority to 0.95)*
