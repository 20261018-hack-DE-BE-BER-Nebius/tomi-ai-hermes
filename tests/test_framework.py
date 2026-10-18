"""Actual Hermes framework with a local transport fixture; never a Nemotron success claim."""

import importlib.util
import json
import threading
from dataclasses import replace
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest

from tomi_ai_hermes.config import Config
from tomi_ai_hermes.infrastructure.agent import HermesAgent


@pytest.mark.skipif(
    importlib.util.find_spec("run_agent") is None, reason="Hermes editable runtime not installed"
)
def test_real_hermes_calls_only_evidence_tool(tmp_path):
    calls = []

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def do_GET(self):
            self.reply({"object": "list", "data": [{"id": "fixture-model", "object": "model"}]})

        def do_POST(self):
            body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            calls.append(body)
            used_tool = any(message.get("role") == "tool" for message in body["messages"])
            message = {
                "role": "assistant",
                "content": '{"answer":"No evidence","abstained":true,"claims":[]}',
            }
            finish = "stop"
            if not used_tool:
                message = {
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [
                        {
                            "id": "fixture-call",
                            "type": "function",
                            "function": {"name": "tomi_evidence", "arguments": "{}"},
                        }
                    ],
                }
                finish = "tool_calls"
            self.reply(
                {
                    "id": "fixture-response",
                    "object": "chat.completion",
                    "created": 1,
                    "model": "fixture-model",
                    "choices": [{"index": 0, "message": message, "finish_reason": finish}],
                    "usage": {"prompt_tokens": 10, "completion_tokens": 10, "total_tokens": 20},
                }
            )

        def reply(self, value):
            body = json.dumps(value).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        config = replace(
            Config(),
            core_url=f"http://127.0.0.1:{server.server_port}",
            core_token="fixture-only",
            agent_model="fixture-model",
            data_dir=tmp_path,
            timeout_seconds=20,
        )
        result = HermesAgent(config).compare("Compare the two sources", "en", {"documents": []})
        assert result["tool_calls"][0]["tool"] == "tomi_evidence"
        assert json.loads(result["final_response"])["abstained"] is True
        assert all(
            {tool["function"]["name"] for tool in call.get("tools", [])} <= {"tomi_evidence"}
            for call in calls
        )
    finally:
        server.shutdown()
        server.server_close()
