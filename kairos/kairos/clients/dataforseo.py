"""DataForSEO client wrapper with mock fallback for offline development."""

from __future__ import annotations

import base64
import os
from dataclasses import dataclass

import httpx


@dataclass
class KeywordData:
    keyword: str
    search_volume: int | None
    keyword_difficulty: int | None


class DataForSEOClient:
    """Thin wrapper over DataForSEO's labs + SERP endpoints."""

    BASE_URL = "https://api.dataforseo.com/v3"

    def __init__(self, login: str | None = None, password: str | None = None):
        self.login = login or os.getenv("DATAFORSEO_LOGIN", "")
        self.password = password or os.getenv("DATAFORSEO_PASSWORD", "")
        if not (self.login and self.password):
            raise ValueError(
                "DataForSEO credentials missing. Set DATAFORSEO_LOGIN / DATAFORSEO_PASSWORD."
            )
        token = base64.b64encode(f"{self.login}:{self.password}".encode()).decode()
        self._headers = {"Authorization": f"Basic {token}", "Content-Type": "application/json"}

    def keyword_suggestions(self, seed: str, limit: int = 50) -> list[KeywordData]:
        endpoint = f"{self.BASE_URL}/dataforseo_labs/google/keyword_suggestions/live"
        payload = [{"keyword": seed, "language_code": "en", "location_code": 2840, "limit": limit}]
        with httpx.Client(timeout=30.0) as client:
            resp = client.post(endpoint, json=payload, headers=self._headers)
            resp.raise_for_status()
            data = resp.json()
        items = data.get("tasks", [{}])[0].get("result", [{}])[0].get("items", [])
        return [
            KeywordData(
                keyword=item["keyword"],
                search_volume=item.get("keyword_info", {}).get("search_volume"),
                keyword_difficulty=item.get("keyword_properties", {}).get("keyword_difficulty"),
            )
            for item in items
        ]

    def serp_top_urls(self, keyword: str, top_n: int = 10) -> list[str]:
        endpoint = f"{self.BASE_URL}/serp/google/organic/live/advanced"
        payload = [{"keyword": keyword, "language_code": "en", "location_code": 2840, "depth": top_n}]
        with httpx.Client(timeout=30.0) as client:
            resp = client.post(endpoint, json=payload, headers=self._headers)
            resp.raise_for_status()
            data = resp.json()
        items = data.get("tasks", [{}])[0].get("result", [{}])[0].get("items", [])
        return [i["url"] for i in items if i.get("type") == "organic"][:top_n]


class MockDataForSEOClient:
    """Deterministic mock for offline development and testing."""

    def keyword_suggestions(self, seed: str, limit: int = 50) -> list[KeywordData]:
        base = seed.lower().strip()
        variants = [
            f"{base}",
            f"{base} software",
            f"{base} tools",
            f"{base} platform",
            f"best {base}",
            f"{base} for saas",
            f"{base} checklist",
            f"{base} automation",
            f"{base} examples",
            f"how to {base}",
            f"{base} guide",
            f"{base} best practices",
            f"{base} process",
            f"{base} workflow",
            f"{base} strategy",
            f"{base} templates",
            f"{base} vs manual",
            f"{base} roi",
            f"{base} metrics",
            f"{base} benchmark",
        ][:limit]
        return [
            KeywordData(
                keyword=v,
                search_volume=max(80, 1200 - i * 50),
                keyword_difficulty=max(10, 20 + (i % 6) * 5),
            )
            for i, v in enumerate(variants)
        ]

    def serp_top_urls(self, keyword: str, top_n: int = 10) -> list[str]:
        slug = keyword.replace(" ", "-")
        return [
            f"https://competitor{i + 1}.com/blog/{slug}"
            for i in range(min(top_n, 10))
        ]


def get_client(use_mock: bool = True) -> DataForSEOClient | MockDataForSEOClient:
    if use_mock:
        return MockDataForSEOClient()
    return DataForSEOClient()
