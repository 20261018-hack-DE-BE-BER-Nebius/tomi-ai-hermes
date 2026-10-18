"""Run the pinned Hermes framework in an isolated process with one read-only evidence tool."""

import json
import subprocess
import sys

from tomi_ai_hermes.config import Config
from tomi_ai_hermes.domain.evidence import DependencyUnavailable, EvidenceError


class HermesAgent:
    def __init__(self, config: Config):
        self.config = config

    def compare(self, question: str, locale: str, evidence: dict) -> dict:
        payload = {
            "question": question,
            "locale": locale,
            "evidence": evidence,
            "config": {
                name: str(getattr(self.config, name))
                for name in (
                    "core_url",
                    "core_token",
                    "agent_model",
                    "max_iterations",
                    "data_dir",
                    "timeout_seconds",
                )
            },
        }
        try:
            completed = subprocess.run(
                [sys.executable, "-m", "tomi_ai_hermes.infrastructure.agent_worker"],
                input=json.dumps(payload),
                text=True,
                capture_output=True,
                check=False,
                timeout=self.config.timeout_seconds * 3,
                env=self._environment(),
            )
        except subprocess.TimeoutExpired:
            raise DependencyUnavailable("hermes", "Agent exceeded bounded execution deadline") from None
        if completed.returncode != 0:
            raise DependencyUnavailable(
                "hermes", "Framework execution failed; inspect configured model access"
            )
        try:
            result = json.loads(completed.stdout)
        except ValueError:
            raise EvidenceError("Hermes worker returned invalid JSON") from None
        if result.get("error"):
            raise DependencyUnavailable("hermes", result["error"])
        return result

    def _environment(self) -> dict:
        profile = (self.config.data_dir / "hermes-profile").resolve()
        profile.mkdir(parents=True, exist_ok=True)
        (profile / "config.yaml").write_text(
            "model:\n  streaming: false\ntools:\n  tool_search:\n    enabled: off\n"
        )
        return {
            "HERMES_HOME": str(profile),
            "HOME": str(profile),
            "PATH": str(sys.executable.rsplit("/", 1)[0]),
            "PYTHONIOENCODING": "utf-8",
            "NO_COLOR": "1",
        }
