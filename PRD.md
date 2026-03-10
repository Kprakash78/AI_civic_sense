# Product Requirements Document (PRD)
**Project:** Rakshita - Smart Civic Grievance & Prioritization Engine

## 1. Executive Summary
Rakshita is an intelligent civic complaint management system. It replaces traditional FIFO (First-In-First-Out) ticket queues with an AI-driven Prioritization Engine. The system evaluates the severity and credibility of citizen reports in real-time, assigning actionable priority levels and routing them to the correct ward officers via a Geo-Mapping Dashboard.

## 2. User Personas & Flows
* **The Citizen:** Submits a complaint via a clean web form. Requires zero login. Provides text, category, and ward selection. 
* **The Civic Officer:** Logs into a secure dashboard. Views a sorted, mapped list of complaints for their specific ward. Needs to see *why* a complaint was prioritized (Explainability).

## 3. Core Features
* **Intelligent Intake:** A public-facing POST endpoint that ingests complaints and triggers the ML pipeline synchronously or asynchronously.
* **The Prioritization Engine:** The core brain that fuses ML-derived Severity, ML/Rule-derived Credibility, and computes a final Priority Score.
* **System-Level Explainability:** Every processed complaint must output a human-readable JSON payload explaining the SHAP-derived keyword triggers and rule-based penalties applied.
* **Geo-Mapping Dashboard (Vanilla JS):** A fast, lightweight frontend using HTML/CSS/Vanilla JS, Chart.js, and mapping tools (e.g., Leaflet/Stitch integrations). No heavy JS frameworks. 
* **Role-Based Access Control (RBAC):** JWT-secured endpoints ensuring officers only mutate state for their assigned jurisdictions.

## 4. State Management (Complaint Lifecycle)
Complaints strictly follow this state machine:
`PENDING` -> `ASSIGNED` -> `IN_PROGRESS` -> `RESOLVED`
Invalid state transitions must be blocked by the backend service layer.