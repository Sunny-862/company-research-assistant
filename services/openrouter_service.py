import json
import os

import requests
from dotenv import load_dotenv

from utils.prompts import COMPANY_ANALYSIS_SYSTEM_PROMPT


load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def build_research_context(
    company_name,
    website,
    crawled_pages,
    search_results,
):
    """
    Combine website content and Serper results into AI context.
    """

    website_content = []

    for page in crawled_pages:
        website_content.append(
            f"""
PAGE URL: {page['url']}
CONTENT:
{page['text'][:5000]}
"""
        )

    search_content = []

    for result in search_results[:15]:
        search_content.append(
            f"""
TITLE: {result['title']}
URL: {result['link']}
SNIPPET: {result['snippet']}
"""
        )

    context = f"""
COMPANY PROVIDED BY USER:
{company_name}

OFFICIAL WEBSITE:
{website}

WEBSITE CONTENT:
{''.join(website_content)}

PUBLIC SEARCH INFORMATION:
{''.join(search_content)}
"""

    return context


def analyze_company(
    company_name,
    website,
    crawled_pages,
    search_results,
    model="openai/gpt-4o-mini",
):
    """
    Analyze company research using OpenRouter.
    """

    if not OPENROUTER_API_KEY:
        raise ValueError(
            "OPENROUTER_API_KEY was not found. Check your .env file."
        )

    research_context = build_research_context(
        company_name,
        website,
        crawled_pages,
        search_results,
    )

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": COMPANY_ANALYSIS_SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": research_context,
            },
        ],
        "temperature": 0.2,
    }

    try:
        response = requests.post(
            OPENROUTER_URL,
            headers=headers,
            json=payload,
            timeout=60,
        )

        response.raise_for_status()

        response_data = response.json()

        ai_content = response_data[
            "choices"
        ][0]["message"]["content"]

        ai_content = ai_content.strip()

        if ai_content.startswith("```json"):
            ai_content = ai_content[7:]

        if ai_content.startswith("```"):
            ai_content = ai_content[3:]

        if ai_content.endswith("```"):
            ai_content = ai_content[:-3]

        return json.loads(ai_content.strip())

    except requests.exceptions.Timeout:
        raise RuntimeError(
            "OpenRouter request timed out."
        )

    except requests.exceptions.RequestException as error:
        raise RuntimeError(
            f"OpenRouter API request failed: {error}"
        )

    except (
        KeyError,
        IndexError,
        json.JSONDecodeError,
    ) as error:
        raise RuntimeError(
            f"Unable to process OpenRouter response: {error}"
        )