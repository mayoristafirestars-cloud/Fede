"""Pydantic schemas for pipeline I/O contracts."""

from typing import Literal

from pydantic import BaseModel, Field

Intent = Literal["informational", "commercial", "transactional", "navigational"]


class KeywordResearchInput(BaseModel):
    client_id: str
    domain: str
    seed_topic: str
    target_audience: str
    existing_posts: list[str] = Field(default_factory=list)
    target_post_count: int = 1


class KeywordCandidate(BaseModel):
    keyword: str
    search_volume: int | None = None
    keyword_difficulty: int | None = None
    intent: Intent


class SecondaryKeyword(KeywordCandidate):
    pass


class KeywordCluster(BaseModel):
    cluster_name: str
    primary_keyword: KeywordCandidate
    secondary_keywords: list[SecondaryKeyword]
    paa_questions: list[str]
    competitor_urls: list[str]
    content_gap_notes: str
    recommended_angle: str = Field(
        description="One-line recommendation for how to differentiate from competitors"
    )
