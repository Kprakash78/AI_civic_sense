# System Architecture & API Contracts

## 1. Tech Stack & Infrastructure
* **Backend:** FastAPI (Python 3.10+)
* **Database:** PostgreSQL (accessed via SQLAlchemy ORM)
* **Validation:** Pydantic
* **Intelligence:** Scikit-learn, XGBoost, SHAP (encapsulated in `/ml`)
* **Deployment:** Docker, Docker Compose, AWS EC2 (Ubuntu).

## 2. Directory Structure (Enforced)
```text
/rakshita-backend
├── /api
│   ├── routes_complaints.py
│   ├── routes_auth.py
├── /core
│   ├── security.py (JWT logic)
│   ├── config.py
├── /db
│   ├── models.py (SQLAlchemy schema)
│   ├── database.py (Connection pooling)
├── /ml (Strict ML/Data Science boundary)
│   ├── severity_model.py
│   ├── credibility_model.py
│   ├── preprocessor.py
├── /services
│   ├── priority_engine.py (Fuses DB and ML)
│   ├── complaint_service.py
├── /static (Frontend assets - Vanilla JS, CSS, HTML)
├── main.py
└── docker-compose.yml