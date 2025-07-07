# Webhook Receiver App (Flask + MongoDB)

This Flask application listens to GitHub Webhook events (Push, Pull Request, Merge) and stores them in MongoDB. The events are then displayed on a clean, auto-refreshing UI every 15 seconds.

### 🔧 Tech Stack
- Python + Flask
- MongoDB (via PyMongo)
- HTML (Jinja2 Templates)
- GitHub Webhooks
- Ngrok (for local webhook testing)

### 📦 Features
- Receives `push`, `pull_request`, and `merge` events from GitHub
- Stores necessary details in MongoDB with minimal schema
- Displays events on a UI: auto-refreshes every 15 seconds
- Logs author name, branch info, and formatted timestamp

### 📁 MongoDB Schema
```json
{
  "author": "Mrunmai",
  "action": "PUSH / PULL_REQUEST / MERGE",
  "from_branch": "feature-xyz",
  "to_branch": "main",
  "timestamp": "07 July 2025 - 10:45 AM UTC"
}
```
## 🚀 Run Locally
### Clone the repo

Create a .env file with:
```bash
MONGO_URI=mongodb://localhost:27017
```
Install requirements:
```bash
pip install -r requirements.txt
```
Start the Flask app:
```bash
python app.py
```
Use Ngrok to expose it:
```bash
ngrok http 5000
```

🌐 Webhook Endpoint
POST /webhook

📄 UI Preview
Visit: http://localhost:5000

## Screenshots

![App Screenshot](![webhook ss](https://github.com/user-attachments/assets/a001fb8b-87d0-4d0e-94a8-6a194d80da69)

