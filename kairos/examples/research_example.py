"""Ejemplo: correr Keyword Researcher desde código."""

from dotenv import load_dotenv

from kairos.agents import KeywordResearcher
from kairos.schemas import KeywordResearchInput

load_dotenv()


def main():
    researcher = KeywordResearcher()
    input_data = KeywordResearchInput(
        client_id="acme-saas",
        domain="acme.com",
        seed_topic="customer onboarding automation",
        target_audience="SaaS customer success managers",
        existing_posts=[
            "https://acme.com/blog/why-onboarding-matters",
        ],
    )

    cluster = researcher.research(input_data)

    print(f"Cluster: {cluster.cluster_name}")
    print(f"Primary KW: {cluster.primary_keyword.keyword}")
    print(f"Angle: {cluster.recommended_angle}")
    print(f"\nFull cluster JSON:")
    print(cluster.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
