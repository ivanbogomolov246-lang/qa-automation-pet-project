from urllib.parse import urljoin

import requests


class ApiClient:
    """Simple client wrapper for API tests."""

    def __init__(self, base_url: str, timeout: int = 10) -> None:
        self.base_url = base_url.rstrip("/") + "/"
        self.timeout = timeout
        self.session = requests.Session()

    def get(self, path: str, **kwargs) -> requests.Response:
        return self.session.get(self._build_url(path), timeout=self.timeout, **kwargs)

    def post(self, path: str, **kwargs) -> requests.Response:
        return self.session.post(self._build_url(path), timeout=self.timeout, **kwargs)

    def close(self) -> None:
        self.session.close()

    def _build_url(self, path: str) -> str:
        return urljoin(self.base_url, path.lstrip("/"))
