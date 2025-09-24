import datetime
import os
import hmac
import hashlib
from flask import Flask, request, abort

app = Flask(__name__)

# Set this to your webhook secret (keep it safe!)
GITHUB_WEBHOOK_SECRET = os.environ.get("GITHUB_WEBHOOK_SECRET")
REPOSITORY_PATH = os.environ.get("REPOSITORY_PATH")
WEB_INSTALL_PATH = os.environ.get("WEB_INSTALL_PATH")
LOGS_PATH = os.environ.get("LOGS_PATH")

if (not LOGS_PATH):
    raise RuntimeError("LOGS_PATH is not set")

if (not GITHUB_WEBHOOK_SECRET):
    raise RuntimeError("GITHUB_WEBHOOK_SECRET is not set")

if (not REPOSITORY_PATH):
    raise RuntimeError("WEB_INSTALL_PATH is not set")

if (not WEB_INSTALL_PATH):
    raise RuntimeError("WEB_INSTALL_PATH is not set")

def verify_signature(payload, signature):
    """Verify GitHub webhook signature."""
    if not signature:
        return False
    sha_name, signature = signature.split('=')
    if sha_name != 'sha256':
        return False
    mac = hmac.new(GITHUB_WEBHOOK_SECRET.encode(), msg=payload, digestmod=hashlib.sha256)
    return hmac.compare_digest(mac.hexdigest(), signature)

@app.route("/deploy/webhook", methods=["POST"])
def webhook():
    # GitHub sends the signature header as 'X-Hub-Signature-256'
    signature = request.headers.get('X-Hub-Signature-256')
    payload = request.get_data()
    if not verify_signature(payload, signature):
        abort(403, "Invalid signature.")
    event = request.headers.get("X-GitHub-Event", "")
    if event != "deployment":
        return "Ignored", 200

    # Optionally, validate action in payload JSON
    data = request.json
    # You could check more about deployment here, e.g., environment, branch, etc.

    timestamp = datetime.now().strftime("%Y_%m_%d__%H_%M_%S")
    logs_path = os.path.join(LOGS_PATH, f"{timestamp}.log")

    # Execute the rebuild.sh script (ensure it is secure)
    exit_code = os.system(f"bash ./rebuild.sh > {logs_path}")
    if exit_code != 0:
        return f"rebuild.sh failed with exit code {exit_code}", 500
    return "Deployment handled and rebuild.sh executed.", 200

if __name__ == "__main__":
    # For production, use a WSGI server instead!
    app.run(host="0.0.0.0", port=8001)
