import datetime
import time
import logging
import subprocess
import os
import hmac
import hashlib
import sys
from .git import Git
from flask import Flask, request, abort

LOG_SIZE = 1 * 1024 * 1024
LOG_COUNT = 5

last_build = 0

app = Flask(__name__)

# Set this to your webhook secret (keep it safe!)
GITHUB_WEBHOOK_SECRET = os.environ.get("GITHUB_WEBHOOK_SECRET")
REPOSITORY_PATH = os.environ.get("REPOSITORY_PATH")
WEB_INSTALL_PATH = os.environ.get("WEB_INSTALL_PATH")
LOGS_PATH = os.environ.get("LOGS_PATH")

if (not LOGS_PATH):
    raise RuntimeError("LOGS_PATH is not set")

os.makedirs(LOGS_PATH, exist_ok=True)
logHandler = logging.handlers.RotatingFileHandler(
            filename=f"{LOGS_PATH}/deployment.log",
            mode="a",
            encoding="utf-8",
            maxBytes=LOG_SIZE,
            backupCount=LOG_COUNT,
        )
logHandler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)-s] %(message)s", "%Y-%m-%d %H:%M:%S"))
logging.getLogger().addHandler(logHandler)

outHandler = logging.StreamHandler(sys.stdout)
outHandler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)-s] %(message)s", "%Y-%m-%d %H:%M:%S"))
logging.getLogger().addHandler(outHandler)

logging.captureWarnings(True)

logging.getLogger().setLevel(logging.INFO)

if (not GITHUB_WEBHOOK_SECRET):
    raise RuntimeError("GITHUB_WEBHOOK_SECRET is not set")

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

def rebuild(url, revision):
    timestamp = datetime.datetime.now().strftime("%Y_%m_%d__%H_%M_%S")
    git = Git(timestamp, "boneca", revision)
    if not git.clone(url, revision):
        raise RuntimeError(f"git clone ({url} @ {revision} to {git.getPath()}) failed")
    logs_path = os.path.join(LOGS_PATH, f"{timestamp}.log")
    env = os.environ.copy()
    logging.info(f"webkook: build in: {git.getPath()}")
    _p = subprocess.Popen([f"exec ./rebuild.sh {git.getPath()} 2>&1 | tee {logs_path}"], shell=True, preexec_fn=os.setsid, env=env)

@app.route("/deploy/webhook", methods=["POST"])
def webhook():
    global last_build
    # GitHub sends the signature header as 'X-Hub-Signature-256'
    signature = request.headers.get('X-Hub-Signature-256')
    payload = request.get_data()
    if not verify_signature(payload, signature):
        logging.info("webkook: invalid signature")
        abort(403, "Invalid signature.")
    event = request.headers.get("X-GitHub-Event", "")
    logging.info(f"webkook: event: {event}")
    if event != "push":
        return "Ignored", 200

    now = time.time()
    if last_build - now < 60:
        logging.info(f"webkook: too early")
        return "Too early", 200
    last_build = now

    logging.info(f"webkook: building")
    try:
        data = request.json
        url = data["repository"]["ssh_url"]
        rev = data["after"]
        logging.info(f"webkook: push: {url} @ {rev}")
        rebuild(url, rev)
    except Exception as e:
        logging.error(f"webkook: exception: {e}")
        return f"Deployment failed: {e}", 500
    return "Deployment handled and rebuild.sh executed.", 200
