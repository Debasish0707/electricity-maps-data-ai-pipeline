from __future__ import annotations
import random
import time
from dataclasses import dataclass
import requests

TRANSIENT_STATUS = {408, 425, 429, 500, 502, 503, 504}

@dataclass(frozen=True)
class ApiResponse:
    payload: dict
    url: str
    status_code: int
    attempts: int

class ElectricityMapsClient:
    """Bounded, retryable HTTP client. Secrets are supplied only at runtime."""
    def __init__(self, base_url: str, api_key: str, timeout: int = 30,
                 max_retries: int = 4, backoff_seconds: float = 1.0):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_seconds = backoff_seconds

    def get(self, path: str, params: dict) -> ApiResponse:
        url = f"{self.base_url}/{path.lstrip('/')}"
        headers = {"auth-token": self.api_key, "Accept": "application/json"}
        last_error: Exception | None = None
        for attempt in range(1, self.max_retries + 2):
            try:
                response = requests.get(url, params=params, headers=headers, timeout=self.timeout)
                if response.status_code == 200:
                    return ApiResponse(response.json(), response.url, response.status_code, attempt)
                if response.status_code not in TRANSIENT_STATUS:
                    response.raise_for_status()
                last_error = RuntimeError(f"Transient HTTP {response.status_code}")
            except requests.RequestException as exc:
                last_error = exc
            if attempt <= self.max_retries:
                retry_after = 0.0
                try:
                    retry_after = float(response.headers.get("Retry-After", "0"))
                except Exception:
                    pass
                delay = max(retry_after, self.backoff_seconds * (2 ** (attempt - 1)))
                time.sleep(delay * (0.75 + random.random() * 0.5))
        raise RuntimeError(f"Electricity Maps request failed after retries: {last_error}")
