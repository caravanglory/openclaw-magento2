"""
Shared Magento 2 REST API client — OAuth 1.0a auth, JSON helpers, pagination.
All other scripts import MagentoClient from here.
"""

import os
import sys
import json
import logging
import urllib.parse
from typing import Any

try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util import Retry
    from requests_oauthlib import OAuth1
except ImportError:
    sys.exit("Missing dependencies. Run: uv pip install requests requests-oauthlib")


# Set up basic logging to stderr for internal debugging if MAGENTO_DEBUG is set
if os.environ.get("MAGENTO_DEBUG"):
    logging.basicConfig(level=logging.DEBUG, stream=sys.stderr, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("magento_client")


class MagentoAPIError(Exception):
    def __init__(self, status: int, message: str, url: str = ""):
        self.status = status
        self.url = url
        super().__init__(message)

    def to_json(self) -> str:
        return json.dumps({"error": f"{self.status}", "message": str(self), "url": self.url})


class MagentoClient:
    def __init__(self):
        self.base_url = self._require_env("MAGENTO_BASE_URL").rstrip("/")
        self.timeout = int(os.environ.get("MAGENTO_TIMEOUT", "30"))
        self.auth = OAuth1(
            client_key=self._require_env("MAGENTO_CONSUMER_KEY"),
            client_secret=self._require_env("MAGENTO_CONSUMER_SECRET"),
            resource_owner_key=self._require_env("MAGENTO_ACCESS_TOKEN"),
            resource_owner_secret=self._require_env("MAGENTO_ACCESS_TOKEN_SECRET"),
            signature_method="HMAC-SHA256",
        )
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json", "Accept": "application/json"})

        # Setup retries for transient errors
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    @staticmethod
    def _require_env(name: str) -> str:
        value = os.environ.get(name)
        if not value:
            sys.exit(json.dumps({"error": "missing_env", "message": f"Environment variable {name!r} is not set.", "url": ""}))
        return value

    def _url(self, path: str) -> str:
        # We must encode path segments (especially SKUs) that might contain spaces or slashes.
        # Magento expects slashes within a SKU to be encoded (e.g., %2F).
        # Split by / and encode each part, then join.
        # If the path already starts with /rest/ then we don't prepend /rest/V1/
        if path.startswith("/rest/"):
             return f"{self.base_url}{path}"
        
        parts = [urllib.parse.quote(p, safe="") for p in path.lstrip("/").split("/")]
        return f"{self.base_url}/rest/V1/{'/'.join(parts)}"

    def _raise_for_status(self, resp: requests.Response) -> None:
        if not resp.ok:
            try:
                body = resp.json()
                message = body.get("message", resp.text)
            except Exception:
                message = resp.text
            raise MagentoAPIError(resp.status_code, message, resp.url)

    def get(self, path: str, params: dict | None = None) -> Any:
        resp = self.session.get(self._url(path), params=params, auth=self.auth, timeout=self.timeout)
        self._raise_for_status(resp)
        return resp.json()

    def post(self, path: str, body: dict) -> Any:
        resp = self.session.post(self._url(path), json=body, auth=self.auth, timeout=self.timeout)
        self._raise_for_status(resp)
        return resp.json()

    def put(self, path: str, body: dict) -> Any:
        resp = self.session.put(self._url(path), json=body, auth=self.auth, timeout=self.timeout)
        self._raise_for_status(resp)
        return resp.json()

    def delete(self, path: str) -> Any:
        resp = self.session.delete(self._url(path), auth=self.auth, timeout=self.timeout)
        self._raise_for_status(resp)
        return resp.json()

    def search(
        self,
        resource: str,
        filters: list[dict | list[dict]] | None = None,
        page_size: int = 20,
        current_page: int = 1,
        sort_field: str | None = None,
        sort_dir: str = "DESC",
    ) -> dict:
        """
        Build a Magento search criteria query and GET the resource.

        filters: list of (dict or list of dicts).
        Each top-level element is a filterGroup (ANDed).
        If an element is a list, its contents are filters within that group (ORed).
        """
        params: dict[str, Any] = {
            "searchCriteria[pageSize]": page_size,
            "searchCriteria[currentPage]": current_page,
        }

        if sort_field:
            params["searchCriteria[sortOrders][0][field]"] = sort_field
            params["searchCriteria[sortOrders][0][direction]"] = sort_dir

        for i, group in enumerate(filters or []):
            if not isinstance(group, list):
                group = [group]
            for j, f in enumerate(group):
                params[f"searchCriteria[filterGroups][{i}][filters][{j}][field]"] = f["field"]
                params[f"searchCriteria[filterGroups][{i}][filters][{j}][value]"] = f["value"]
                params[f"searchCriteria[filterGroups][{i}][filters][{j}][conditionType]"] = f.get("condition_type", "eq")

        resp = self.session.get(self._url(resource), params=params, auth=self.auth, timeout=self.timeout)
        self._raise_for_status(resp)
        return resp.json()


def print_error_and_exit(err: MagentoAPIError) -> None:
    print(err.to_json(), file=sys.stderr)
    sys.exit(1)


def get_client() -> MagentoClient:
    """Convenience factory — call this at the top of each script."""
    return MagentoClient()