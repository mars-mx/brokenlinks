import re
from typing import List
from model.page import Page

RELATIVE_URL_REGEX = r"^/.*"


def get_links(page: Page) -> List[str]:
    """_summary_
    Extract all the links from the given page content.

    Args:
        page (Page): _description_ to extract links from

    Returns:
        List[str]: _description_ of all the links in the page content
    """
    links = []
    for link in page.content.find_all("a"):
        href = link.get("href")
        if href:
            links.append(href)
    return links


def is_relative(url) -> bool:
    """_summary_
    Check if a URL is relative.

    Args:
        url (_type_): _description_ to check

    Returns:
        _type_: _description_ of the result
    """
    return bool(re.match(RELATIVE_URL_REGEX, url))


def get_absolute_url(base_url: str, url: str) -> str:
    """_summary_
    Convert a relative URL to an absolute URL.

    Args:
        base_url (str): _description_ of the base URL
        url (str): _description_ of the URL to convert

    Returns:
        str: _description_ of the absolute URL
    """
    if is_relative(url):
        return f"{base_url}{url}"
    return url


def is_anchor(url: str) -> bool:
    """_summary_
    Check if a URL is an anchor.

    Args:
        url (str): _description_ to check

    Returns:
        bool: _description_ of the result
    """
    return url.startswith("#")


def get_root_url(url: str) -> str:
    """_summary_
    Get the root URL of a given URL.

    Args:
        url (str): _description_ to get the root URL from

    Returns:
        str: _description_ of the root URL
    """
    url = url.replace("http://", "https://")
    if not url.startswith("https"):
        url = f"https://{url}"
    parts = url.split("/")
    return f"{parts[0]}//{parts[2]}"


def is_internal(url: str, root_url: str) -> bool:
    """_summary_
    Check if a URL is internal to the root URL.

    Args:
        url (str): _description_ to check
        root_url (str): _description_ of the root URL

    Returns:
        bool: _description_ of the result
    """
    return url.startswith(root_url) or is_relative(url) or is_anchor(url)


def is_external(url: str, root_url: str) -> bool:
    """_summary_
    Check if a URL is external to the root URL.

    Args:
        url (str): _description_ to check
        root_url (str): _description_ of the root URL

    Returns:
        bool: _description_ of the result
    """
    return not is_internal(url, root_url)
