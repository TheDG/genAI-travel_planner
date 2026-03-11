import json
import os
from http.server import BaseHTTPRequestHandler
import urllib.request
import urllib.error

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
WORKFLOW_ID = os.environ.get("CHATKIT_WORKFLOW_ID") or os.environ.get("VITE_CHATKIT_WORKFLOW_ID")


class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        if not OPENAI_API_KEY:
            return self._json(500, {"error": "Missing OPENAI_API_KEY"})
        if not WORKFLOW_ID:
            return self._json(500, {"error": "Missing workflow ID env var"})

        try:
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length) if length > 0 else b"{}"
            incoming = json.loads(raw.decode("utf-8") or "{}")
        except Exception:
            incoming = {}

        user = incoming.get("user", "user-demo")

        payload = {
            "workflow": {"id": WORKFLOW_ID},
            "user": user,
        }

        req = urllib.request.Request(
            "https://api.openai.com/v1/chatkit/sessions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {OPENAI_API_KEY}",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(req) as resp:
                body = resp.read().decode("utf-8")
                return self._raw(resp.status, body)
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8")
            return self._raw(e.code, body)
        except Exception as e:
            return self._json(500, {"error": str(e)})

    def _raw(self, status, body):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))

    def _json(self, status, obj):
        self._raw(status, json.dumps(obj))
