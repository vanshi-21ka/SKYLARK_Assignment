# 🛸 Skylark Drones — Executive BI & AI Agent

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://YOUR-APP-NAME.streamlit.app)
![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![Groq](https://img.shields.io/badge/AI-Groq%20Llama--3.1--8b-indigo)
![License](https://img.shields.io/badge/license-MIT-green.svg)

> **Live Demo:** [Skylark Executive Command Center](https://YOUR-APP-NAME.streamlit.app) *(Replace with your live Streamlit Cloud link)*

---

## 📌 Executive Summary

The **Skylark Executive BI Agent** is an enterprise-grade business intelligence dashboard and real-time operational telemetry platform. Designed specifically for drone operations and field service management, it seamlessly bridges data ingestion from **Monday.com** with fast AI inference powered by **Groq (Llama-3.1-8b-instant)**.

It replaces static reporting with an interactive **AI Decision Workspace**, allowing executives to query field risks, revenue pipelines, and operational bottlenecks using natural language.

---

## ✨ Key Features

* **🛸 Real-Time Monday.com Ingestion:** Dynamically fetches deals and work order boards via Monday.com's GraphQL v2 API.
* **🤖 Groq-Powered AI Executive Assistant:** Low-latency streaming answers to natural language business queries (e.g., *"Which work orders are currently delayed?"*).
* **📈 Dynamic KPI & Telemetry Dashboard:** Automated calculation of pipeline metrics, deal distributions, and real-time risk flags.
* **🎨 Glassmorphism SaaS UI/UX:** Dark-mode executive command center built with custom CSS, interactive quick-prompt pills, and glowing live-status telemetry indicators.
* **🔍 Vectorized Filtering & CSV Export:** Search across all board attributes instantly and download filtered operational datasets with a single click.

---
Open_API: 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
API_Token: eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjY4NjY0Mzc2MywiYWFpIjoxMSwidWlkIjoxMTE1MDk3NzIsImlhZCI6IjIwMjYtMDctMjdUMDQ6NDg6MjkuNDAxWiIsInBlciI6Im1lOndyaXRlIiwiYWN0aWQiOjM2MjI0NTE2LCJyZ24iOiJhcHNlMiJ9.iETAdcQMj9JjXiMkpby1U-ae1n3mnTCb4x327D0rVYI

## 🏗️ Tech Stack & Architecture

* **Frontend / Dashboard Framework:** [Streamlit](https://streamlit.io/)
* **AI Inference / LLM:** [Groq API](https://groq.com/) (`llama-3.1-8b-instant`)
* **API Ingestion:** GraphQL v2 API (`requests`)
* **Data Processing & Analytics:** `pandas`, `plotly`
