"""Keyword Researcher — Agente #1 del pipeline Kairos.

Dado un seed topic y un dominio cliente, produce un cluster de keywords
priorizado con intención de búsqueda, PAA y gap de contenido.
"""

from __future__ import annotations

import json

import anthropic

from kairos.clients import DataForSEOClient, MockDataForSEOClient, get_client
from kairos.schemas import KeywordCluster, KeywordResearchInput


SYSTEM_PROMPT = """You are a senior SEO strategist specializing in SaaS B2B content.

Your job: given a seed topic, a client domain, and raw keyword data from DataForSEO,
produce a tight, publishable keyword cluster that prioritizes:

1. Traffic potential (prefer search volume > 200 when KD is reasonable)
2. Realistic difficulty (prefer KD < 40 for young domains; KD < 60 otherwise)
3. Intent alignment with the target audience
4. Differentiation from the top 3 ranked competitors

Rules:
- Never invent search volume or KD numbers. Use only what the user provides.
- Pick exactly ONE primary keyword per cluster. Prefer informational+commercial blend.
- Pick 5-10 secondary keywords that share search intent with the primary.
- Extract People Also Asked (PAA) style questions from the cluster's intent.
- Flag content gaps: what do competitors miss that this client could own?
- Recommend ONE sharp editorial angle (one sentence) to beat the SERP."""


USER_PROMPT_TEMPLATE = """Brief:
- Client domain: {domain}
- Seed topic: {seed_topic}
- Target audience: {target_audience}
- Existing client posts (do NOT overlap): {existing_posts}

Keyword data from DataForSEO (top candidates, sorted by relevance):
{keyword_data_json}

Top ranking competitor URLs for the seed topic:
{competitor_urls_json}

Produce a keyword cluster. Return ONLY valid JSON matching the provided schema.
Do not include any explanatory text outside the JSON."""


class KeywordResearcher:
    """Agent #1: turns a seed topic into a publishable keyword cluster."""

    def __init__(
        self,
        anthropic_client: anthropic.Anthropic | None = None,
        data_client: DataForSEOClient | MockDataForSEOClient | None = None,
        model: str = "claude-opus-4-7",
    ):
        self.client = anthropic_client or anthropic.Anthropic()
        self.data = data_client or get_client(use_mock=True)
        self.model = model

    def research(self, input_data: KeywordResearchInput) -> KeywordCluster:
        raw_keywords = self.data.keyword_suggestions(input_data.seed_topic, limit=30)
        competitor_urls = self.data.serp_top_urls(input_data.seed_topic, top_n=5)

        keyword_data_json = json.dumps(
            [
                {
                    "keyword": k.keyword,
                    "search_volume": k.search_volume,
                    "keyword_difficulty": k.keyword_difficulty,
                }
                for k in raw_keywords
            ],
            indent=2,
        )

        user_prompt = USER_PROMPT_TEMPLATE.format(
            domain=input_data.domain,
            seed_topic=input_data.seed_topic,
            target_audience=input_data.target_audience,
            existing_posts=json.dumps(input_data.existing_posts),
            keyword_data_json=keyword_data_json,
            competitor_urls_json=json.dumps(competitor_urls, indent=2),
        )

        response = self.client.messages.parse(
            model=self.model,
            max_tokens=16000,
            thinking={"type": "adaptive"},
            system=[
                {
                    "type": "text",
                    "text": SYSTEM_PROMPT,
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            messages=[{"role": "user", "content": user_prompt}],
            output_config={"format": KeywordCluster},
        )

        cluster = response.parsed_output
        if cluster is None:
            raise RuntimeError(
                "Keyword Researcher returned no parsed output. "
                f"stop_reason={response.stop_reason}"
            )
        return cluster
