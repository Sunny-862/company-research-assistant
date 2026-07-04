from urllib.parse import urlparse


def is_valid_url(value):
    """
    Check whether the user input is a website URL.
    """

    try:
        parsed = urlparse(value.strip())

        return (
            parsed.scheme in ("http", "https")
            and bool(parsed.netloc)
        )

    except Exception:
        return False


def normalize_website_url(value):
    """
    Normalize a website URL by removing fragments
    and trailing slashes.
    """

    value = value.strip()

    parsed = urlparse(value)

    return f"{parsed.scheme}://{parsed.netloc}"