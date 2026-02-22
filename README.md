his project is an autonomous AIOps (Artificial Intelligence for IT Operations) tool that monitors system metrics (CPU) in real-time and generates technical analysis reports using a local AI (Gemma 2) during critical incidents.

🌟 Key Features
Real-Time Monitoring: System load tracking via Prometheus and Node Exporter.

Intelligent Analysis: Metric interpretation using the Gemma 2:2b LLM model running on Ollama.

Autonomous Alerting System: Automated email delivery of AI-generated troubleshooting recipes when critical thresholds are exceeded.

Log Management: All AI analyses are logged in a professional engineering notebook format.

Security: Protection of sensitive data (API passwords, etc.) using .env and .gitignore.

🛠 Tech Stack
Monitoring & Visualization: Prometheus, Grafana

Artificial Intelligence: Ollama (Gemma 2:2b Model)

Language & Libraries: Python 3.10+, Requests, Smtplib, Python-dotenv

Infrastructure: Docker & Docker Compose

🏗 Architecture
Data Collection: Node Exporter collects system data, and Prometheus stores these metrics.

Analysis Layer: The Python service queries CPU data via the Prometheus API.

AI Decision Engine: If CPU usage exceeds the threshold, raw data is sent to the Gemma 2 model to receive a "how to intervene?" response.

Notification: The generated technical report is forwarded to the administrator via SMTP.

🚀 Installation (Local Development)
Start Docker Services:

Bash
cd infrastructure
docker-compose up -d

Setup the Python Environment:

Bash
cd src/Brain_AI
python -m venv venv
source venv/bin/activate  # For Windows: .\venv\Scripts\activate
pip install -r requirements.txt

