import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urldefrag


IMPORTANT_KEYWORDS = {
    "about",
    "product",
    "products",
    "service",
    "services",
    "solution",
    "solutions",
    "contact",
    "pricing",
    "company",
}


EXCLUDED_KEYWORDS = {
    "login",
    "signin",
    "sign-in",
    "signup",
    "sign-up",
    "register",
    "privacy",
    "terms",
    "cookie",
    "career",
    "careers",
    "blog",
    "news",
    "press",
    "support",
    "help",
}


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}


def normalize_url(url):
    """
    Remove fragments and trailing slashes for duplicate detection.
    """

    url, _ = urldefrag(url)

    return url.rstrip("/")


def get_domain(url):
    """
    Extract the domain from a URL.
    """

    return urlparse(url).netloc.lower().replace("www.", "")


def is_same_domain(url, base_url):
    """
    Check whether a URL belongs to the company website.
    """

    return get_domain(url) == get_domain(base_url)


def is_relevant_page(url):
    """
    Determine whether a discovered URL is useful for company research.
    """

    path = urlparse(url).path.lower()

    if any(keyword in path for keyword in EXCLUDED_KEYWORDS):
        return False

    return any(keyword in path for keyword in IMPORTANT_KEYWORDS)


def clean_page_content(html):
    """
    Extract meaningful readable text from HTML.
    """

    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(
        [
            "script",
            "style",
            "noscript",
            "svg",
            "iframe",
            "form",
            "nav",
            "footer",
        ]
    ):
        tag.decompose()

    text = soup.get_text(separator=" ", strip=True)

    return " ".join(text.split())


def fetch_page(url):
    """
    Download and extract clean content from one webpage.
    """

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=15,
            allow_redirects=True,
        )

        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "")

        if "text/html" not in content_type:
            return None

        return {
            "url": response.url,
            "html": response.text,
            "text": clean_page_content(response.text),
        }

    except requests.exceptions.RequestException:
        return None


def discover_pages(base_url, html):
    """
    Discover useful internal pages from the homepage.
    """

    soup = BeautifulSoup(html, "html.parser")

    discovered_urls = set()

    for link in soup.find_all("a", href=True):

        absolute_url = urljoin(base_url, link["href"])

        normalized_url = normalize_url(absolute_url)

        if not normalized_url.startswith(("http://", "https://")):
            continue

        if not is_same_domain(normalized_url, base_url):
            continue

        if is_relevant_page(normalized_url):
            discovered_urls.add(normalized_url)

    return list(discovered_urls)


def crawl_website(base_url, max_pages=8):
    """
    Crawl the homepage and important company pages.
    """

    visited_urls = set()
    crawled_pages = []

    homepage = fetch_page(base_url)

    if not homepage:
        raise RuntimeError(
            f"Unable to access company website: {base_url}"
        )

    homepage_url = normalize_url(homepage["url"])

    visited_urls.add(homepage_url)

    crawled_pages.append(
        {
            "url": homepage_url,
            "text": homepage["text"],
        }
    )

    discovered_pages = discover_pages(
        homepage_url,
        homepage["html"],
    )

    for url in discovered_pages:

        if len(crawled_pages) >= max_pages:
            break

        normalized_url = normalize_url(url)

        if normalized_url in visited_urls:
            continue

        visited_urls.add(normalized_url)

        page = fetch_page(normalized_url)

        if not page:
            continue

        if len(page["text"]) < 100:
            continue

        crawled_pages.append(
            {
                "url": normalized_url,
                "text": page["text"],
            }
        )

    return crawled_pages


if __name__ == "__main__":

    website = input("Enter company website: ")

    print("\nCrawling website...\n")

    pages = crawl_website(website)

    print(f"Successfully crawled {len(pages)} pages.\n")

    for page in pages:

        print("URL:", page["url"])

        print(
            "Content Preview:",
            page["text"][:300],
        )

        print("-" * 70)