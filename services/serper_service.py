import os
import re
from urllib.parse import urlparse, urlunparse

import requests
import streamlit as st
from dotenv import load_dotenv


load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY") or st.secrets.get("SERPER_API_KEY")
SERPER_SEARCH_URL = "https://google.serper.dev/search"


# Domains that should never be treated as an official company website.
OFFICIAL_WEBSITE_EXCLUDED_DOMAINS = {
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
    "bloomberg.com",
    "reuters.com",
    "forbes.com",
    "businessinsider.com",
    "techcrunch.com",
    "medium.com",
    "github.com",
    "yelp.com",
    "pitchbook.com",
    "zoominfo.com",
    "tracxn.com",
    "owler.com",
    "gsa.gov",
    "britannica.com",
    "yahoo.com",
}


# Domains we do not want to show as public research sources.
#
# NOTE:
# We intentionally do NOT exclude every third-party website here.
# Reliable news/business sources can still be useful research sources.
RESEARCH_EXCLUDED_DOMAINS = {
    "facebook.com",
    "instagram.com",
    "twitter.com",
    "x.com",
    "youtube.com",
    "reddit.com",
    "tiktok.com",
    "pinterest.com",
    "quora.com",
    "medium.com",
    "github.com",
    "glassdoor.com",
    "indeed.com",
    "yelp.com",
    "news.ycombinator.com",
}


COMPANY_SUFFIXES = {
    "private",
    "limited",
    "pvt",
    "ltd",
    "inc",
    "incorporated",
    "corporation",
    "corp",
    "llc",
    "plc",
    "company",
}


def search_serper(query, num_results=10):
    """
    Search the web using Serper.dev.
    """

    if not SERPER_API_KEY:
        raise ValueError(
            "SERPER_API_KEY was not found. Check your .env file."
        )

    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json",
    }

    payload = {
        "q": query,
        "num": num_results,
    }

    try:
        response = requests.post(
            SERPER_SEARCH_URL,
            headers=headers,
            json=payload,
            timeout=15,
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.Timeout:
        raise RuntimeError(
            "Serper request timed out."
        )

    except requests.exceptions.RequestException as error:
        raise RuntimeError(
            f"Serper API request failed: {error}"
        )


def get_domain(url):
    """
    Extract a clean domain from a URL.
    """

    try:
        parsed_url = urlparse(url)

        domain = parsed_url.netloc.lower()

        if domain.startswith("www."):
            domain = domain[4:]

        return domain

    except Exception:
        return ""


def get_domain_name(url):
    """
    Extract the main domain name.

    stripe.com -> stripe
    microsoft.com -> microsoft
    reluconsultancy.in -> reluconsultancy
    """

    domain = get_domain(url)

    if not domain:
        return ""

    return domain.split(".")[0]


def normalize_url(url):
    """
    Normalize URLs to improve duplicate detection.
    """

    if not url:
        return ""

    try:
        parsed = urlparse(url)

        scheme = parsed.scheme.lower() or "https"
        netloc = parsed.netloc.lower()

        if netloc.startswith("www."):
            netloc = netloc[4:]

        path = parsed.path.rstrip("/")

        return urlunparse(
            (
                scheme,
                netloc,
                path,
                "",
                "",
                "",
            )
        )

    except Exception:
        return url


def normalize_text(text):
    """
    Convert text into lowercase alphanumeric
    characters for safer comparison.
    """

    if not text:
        return ""

    return re.sub(
        r"[^a-z0-9]",
        "",
        text.lower(),
    )


def get_company_words(company_name):
    """
    Extract meaningful words from a company name.
    """

    if not company_name:
        return []

    cleaned_name = re.sub(
        r"[^a-z0-9\s]",
        " ",
        company_name.lower(),
    )

    words = cleaned_name.split()

    return [
        word
        for word in words
        if word not in COMPANY_SUFFIXES
        and len(word) >= 2
    ]


def normalize_company_name(company_name):
    """
    Normalize company name by removing common
    legal company suffixes.
    """

    return "".join(
        get_company_words(company_name)
    )


def domain_matches_excluded_list(url, excluded_domains):
    """
    Check whether a URL belongs to an excluded domain.
    """

    domain = get_domain(url)

    if not domain:
        return True

    return any(
        domain == excluded
        or domain.endswith("." + excluded)
        for excluded in excluded_domains
    )


def is_excluded_domain(url):
    """
    Reject domains that should not be considered
    official company websites.
    """

    return domain_matches_excluded_list(
        url,
        OFFICIAL_WEBSITE_EXCLUDED_DOMAINS,
    )


def is_valid_company_website(company_name, result):
    """
    Validate whether a search result is likely
    to represent the official company website.
    """

    link = result.get("link", "")
    title = result.get("title", "")
    snippet = result.get("snippet", "")

    if not link:
        return False

    if is_excluded_domain(link):
        return False

    domain_name = get_domain_name(link)

    if not domain_name:
        return False

    company_normalized = normalize_company_name(
        company_name
    )

    domain_normalized = normalize_text(
        domain_name
    )

    title_normalized = normalize_text(
        title
    )

    snippet_normalized = normalize_text(
        snippet
    )

    if not company_normalized:
        return False

    if not domain_normalized:
        return False

    # Exact company/domain match.
    #
    # Microsoft -> microsoft.com
    if company_normalized == domain_normalized:
        return True

    # Company name appears inside domain.
    #
    # Relu Consultancy -> reluconsultancy.com
    if (
        len(company_normalized) >= 4
        and company_normalized in domain_normalized
    ):
        return True

    # Domain appears inside company name only when
    # supported by the result title.
    if (
        len(domain_normalized) >= 5
        and domain_normalized in company_normalized
        and company_normalized in title_normalized
    ):
        return True

    evidence_score = 0

    if company_normalized in title_normalized:
        evidence_score += 1

    if company_normalized in snippet_normalized:
        evidence_score += 1

    if company_normalized in domain_normalized:
        evidence_score += 2

    return evidence_score >= 3


def find_official_website(company_name):
    """
    Find and validate the most likely official
    company website.

    Returns None when no reliable website
    can be identified.
    """

    if not company_name:
        return None

    company_name = company_name.strip()

    if len(company_name) < 2:
        return None

    if not re.search(r"[a-zA-Z]", company_name):
        return None

    query = f'"{company_name}" official website'

    try:
        search_data = search_serper(
            query,
            num_results=10,
        )

    except RuntimeError:
        return None

    organic_results = search_data.get(
        "organic",
        [],
    )

    if not organic_results:
        return None

    for result in organic_results:

        if is_valid_company_website(
            company_name,
            result,
        ):
            return result.get("link")

    return None


def is_relevant_research_result(company_name, result):
    """
    Check whether a search result is sufficiently
    relevant to the requested company.
    """

    title = result.get("title", "")
    snippet = result.get("snippet", "")
    link = result.get("link", "")

    if not link:
        return False

    if domain_matches_excluded_list(
        link,
        RESEARCH_EXCLUDED_DOMAINS,
    ):
        return False

    company_normalized = normalize_company_name(
        company_name
    )

    title_normalized = normalize_text(title)
    snippet_normalized = normalize_text(snippet)
    domain_normalized = normalize_text(
        get_domain_name(link)
    )

    combined_text = (
        title_normalized
        + snippet_normalized
        + domain_normalized
    )

    if not company_normalized:
        return False

    # Strong direct company-name match.
    if company_normalized in combined_text:
        return True

    # Support companies with multiple words where
    # formatting may differ between the company name,
    # search result title, and snippet.
    company_words = get_company_words(
        company_name
    )

    if not company_words:
        return False

    matched_words = sum(
        1
        for word in company_words
        if normalize_text(word) in combined_text
    )

    # For one-word company names such as Microsoft,
    # Stripe, NVIDIA, etc.
    if len(company_words) == 1:
        return matched_words == 1

    # For multi-word company names, require at least
    # half of the meaningful words to appear.
    required_matches = max(
        1,
        (len(company_words) + 1) // 2,
    )

    return matched_words >= required_matches


def research_company_search(company_name):
    """
    Collect relevant public company information
    while filtering low-quality and duplicate sources.
    """

    if not company_name:
        return []

    queries = [
        f'"{company_name}" company information',
        f'"{company_name}" products services',
        f'"{company_name}" headquarters contact',
    ]

    research_results = []

    seen_links = set()

    for query in queries:

        try:
            data = search_serper(
                query,
                num_results=5,
            )

            organic_results = data.get(
                "organic",
                [],
            )

            for result in organic_results:

                link = result.get(
                    "link",
                    "",
                )

                title = result.get(
                    "title",
                    "",
                )

                snippet = result.get(
                    "snippet",
                    "",
                )

                if not link:
                    continue

                normalized_link = normalize_url(
                    link
                )

                if normalized_link in seen_links:
                    continue

                if not is_relevant_research_result(
                    company_name,
                    result,
                ):
                    continue

                seen_links.add(
                    normalized_link
                )

                research_results.append(
                    {
                        "title": title,
                        "link": link,
                        "snippet": snippet,
                    }
                )

        except RuntimeError:
            continue

    return research_results


if __name__ == "__main__":

    company = input(
        "Enter company name: "
    ).strip()

    print(
        "\nSearching for official website..."
    )

    website = find_official_website(
        company
    )

    if website:

        print(
            f"\nOfficial Website: {website}"
        )

        print(
            "\nCollecting public research..."
        )

        research = research_company_search(
            company
        )

        print(
            f"\nFound {len(research)} "
            "filtered research results.\n"
        )

        for result in research[:10]:

            print(
                "Title:",
                result["title"],
            )

            print(
                "URL:",
                result["link"],
            )

            print(
                "Snippet:",
                result["snippet"],
            )

            print("-" * 60)

    else:

        print(
            "\nNo reliable official company "
            "website could be identified."
        )