"""Bounded requests without redirect-based credential forwarding or raw error leakage."""

import time

import httpx

from tomi_ai_hermes.domain.evidence import DependencyUnavailable, EvidenceError


class JSONClient:
    def __init__(self, base_url: str, timeout: float, token: str = ""):
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        self.client = httpx.Client(
            base_url=base_url.rstrip("/") + "/",
            timeout=timeout,
            headers=headers,
            follow_redirects=False,
            trust_env=False,
        )

    def request(self, method: str, path: str, **kwargs) -> dict:
        for attempt in range(3):
            try:
                response = self.client.request(method, path.lstrip("/"), **kwargs)
            except httpx.HTTPError as error:
                raise DependencyUnavailable("http", type(error).__name__) from None
            if response.status_code in {429, 503} and attempt < 2:
                retry = response.headers.get("Retry-After", "")
                time.sleep(min(float(retry) if retry.isdigit() else 2**attempt, 10))
                continue
            if response.status_code >= 300:
                raise DependencyUnavailable(path, f"HTTP {response.status_code}")
            try:
                result = response.json()
            except ValueError:
                raise EvidenceError("Endpoint did not return JSON") from None
            if not isinstance(result, dict):
                raise EvidenceError("Endpoint JSON must be an object")
            return result
        raise DependencyUnavailable(path, "Retry budget exhausted")

    def close(self):
        self.client.close()
