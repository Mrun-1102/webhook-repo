from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv
import pytz


# Load .env
load_dotenv()

# Flask App
app = Flask(__name__)

# MongoDB Setup
client = MongoClient(os.getenv("MONGO_URI"))
db = client.github_webhooks
collection = db.events

@app.route('/')
def index():
    events = collection.find().sort("timestamp", -1)
    return render_template("index.html", events=events)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    event_type = request.headers.get('X-GitHub-Event')
    
    author = data.get('sender', {}).get('login')
    
    timestamp = datetime.utcnow().replace(tzinfo=pytz.UTC).strftime('%d %B %Y - %I:%M %p UTC')

    if event_type == "push":
        to_branch = data.get("ref", "").split("/")[-1]
        action = "PUSH"
        event = {
            "author": author,
            "action": action,
            "from_branch": None,
            "to_branch": to_branch,
            "timestamp": timestamp
        }

    elif event_type == "pull_request":
        pr = data.get("pull_request", {})
        from_branch = pr.get("head", {}).get("ref") or "unknown"
        to_branch = pr.get("base", {}).get("ref") or "unknown"
        action = "PULL_REQUEST"
        event = {
            "author": author,
            "action": action,
            "from_branch": from_branch,
            "to_branch": to_branch,
            "timestamp": timestamp
        }

    elif event_type == "merge_group":
        from_branch = data.get("pull_request", {}).get("head", {}).get("ref") or "unknown"
        to_branch = data.get("pull_request", {}).get("base", {}).get("ref") or "unknown"
        action = "MERGE"
        event = {
            "author": author,
            "action": action,
            "from_branch": from_branch,
            "to_branch": to_branch,
            "timestamp": timestamp
        }

    else:
        return jsonify({"msg": "Unsupported event"}), 400

    collection.insert_one(event)
    return jsonify({"status": "saved"}), 200

if __name__ == '__main__':
    app.run(debug=True)
    