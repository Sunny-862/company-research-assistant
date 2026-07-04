import json
import os
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv

from services.serper_service import search_serper


load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


EXCLUDED_DOMAINS = {
    "linkedin.com",
    "facebook.com",
    "instagram.com",
    "twitter.com",
    "x.com",
    "youtube.com",
    "wikipedia.org",
    "crunchbase.com",
    "reddit.com",
    "glassdoor.com",
    "indeed.com",
    "forbes.com",
    "bloomberg.com",
    "g2.com",
    "capterra.com",
}


def get_domain(url):
    """
    Extract a clean domain from a URL.
    """

    try:
        parsed_url = urlparse(url)

        return (
            parsed_url.netloc
            .lower()
            .replace("www.", "")
        )

    except Exception:
        return ""


def is_excluded_domain(url):
    """
    Check whether URL belongs to an irrelevant platform.
    """

    domain = get_domain(url)

    return any(
        domain == excluded
        or domain.endswith("." + excluded)
        for excluded in EXCLUDED_DOMAINS
    )


def suggest_competitor_names(
    company_name,
    industry,
    country,
    products_services,
    model="openai/gpt-4o-mini",
):
    """
    Ask OpenRouter to suggest relevant direct competitors.
    """

    if not OPENROUTER_API_KEY:
        raise ValueError(
            "OPENROUTER_API_KEY was not found."
        )

    product_text = ", ".join(products_services[:6])

    prompt = f"""
Identify 7 direct competitors of the following company.

Company: {company_name}
Industry: {industry}
Country: {country}
Products and Services: {product_text}

Requirements:
- Competitors should operate in the same or closely related industry.
- Prefer companies offering similar products or services.
- Consider the company's country and market presence.
- Do not include the original company.
- Return only valid JSON.
- Do not include explanations.
- Do not include markdown code fences.

Return exactly:

{{
    "competitors": [
        "Company One",
        "Company Two"
    ]
}}
"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
        "temperature": 0.2,
    }

    response = requests.post(
        OPENROUTER_URL,
        headers=headers,
        json=payload,
        timeout=60,
    )

    response.raise_for_status()

    response_data = response.json()

    content = response_data[
        "choices"
    ][0]["message"]["content"].strip()

    if content.startswith("```json"):
        content = content[7:]

    if content.startswith("```"):
        content = content[3:]

    if content.endswith("```"):
        content = content[:-3]

    parsed_content = json.loads(content.strip())

    return parsed_content.get("competitors", [])


def find_official_competitor_website(
    competitor_name,
):
    """
    Find the likely official website of a competitor using Serper.
    """

    query = f"{competitor_name} official company website"

    search_data = search_serper(
        query,
        num_results=5,
    )

    organic_results = search_data.get(
        "organic",
        [],
    )

    for result in organic_results:

        link = result.get("link", "")

        if not link:
            continue

        if is_excluded_domain(link):
            continue

        return link

    return None


def find_competitors(
    company_name,
    company_website,
    industry,
    country,
    products_services,
    max_competitors=5,
    model="openai/gpt-4o-mini",
):
    """
    Generate competitor suggestions with AI and
    validate their official websites using Serper.
    """

    suggested_names = suggest_competitor_names(
        company_name=company_name,
        industry=industry,
        country=country,
        products_services=products_services,
        model=model,
    )

    original_domain = get_domain(company_website)

    competitors = []

    seen_domains = set()

    for competitor_name in suggested_names:

        try:

            website = find_official_competitor_website(
                competitor_name
            )

            if not website:
                continue

            competitor_domain = get_domain(website)

            if not competitor_domain:
                continue

            if competitor_domain == original_domain:
                continue

            if competitor_domain in seen_domains:
                continue

            seen_domains.add(competitor_domain)

            competitors.append(
                {
                    "company_name": competitor_name,
                    "website": website,
                }
            )

            if len(competitors) >= max_competitors:
                break

        except Exception:
            continue

    return competitors