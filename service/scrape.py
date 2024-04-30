import copy
import logging
import re
from typing import List
from bs4 import BeautifulSoup
import requests

from model.page import ExternalPage, Page
from service.parse import (
    get_absolute_url,
    get_links,
    is_anchor,
    is_external,
    is_internal,
    is_relative,
)

LOG = logging.getLogger("brokenlinks")


def _perform_request(url, retries=3, timeout=5) -> requests.Response:
    """_summary_
    Perform a GET request to the given URL. Retry up to `retries` times if the request fails
    with a `requests.exceptions.RequestException`. Raise the exception if the request fails
    after all retries.

    Args:
        url (_type_): _description_. URL to fetch
        retries (int, optional): _description_. Defaults to 3.
        timeout (int, optional): _description_. Defaults to 5.

    Raises:
        e: _description_ if the request fails after all retries

    Returns:
        requests.Response: _description_ if the request is successful
    """
    for i in range(retries):
        try:
            r = requests.get(url, timeout=timeout)
            return r
        except requests.exceptions.RequestException as e:
            if i == retries - 1:
                raise e
            else:
                LOG.warning(f"Failed to fetch {url}. Retrying...")


def load_page(page: Page, retries=5, timeout=10) -> Page:
    """_summary_
    Load the content of a page by fetching the URL and parsing the HTML content.

    Args:
        page (Page): _description_ to load
        retries (int, optional): _description_. Defaults to 5.
        timeout (int, optional): _description_. Defaults to 10.

    Returns:
        Page: _description_ with the content and status code of the fetched page
    """
    response = _perform_request(page.url, retries=retries, timeout=timeout)
    page.status_code = response.status_code
    raw_text = response.text
    page.content = BeautifulSoup(raw_text, "html.parser")
    return page


def load_url(url: str, retries=5, timeout=10) -> Page:
    """
    Load the content of a url by fetching the URL and parsing the HTML content.

    Args:
        url (str): _description_ to load
        retries (int, optional): _description_. Defaults to 5.
        timeout (int, optional): _description_. Defaults to 10.

    Returns:
        Page: _description_ with the content and status code of the fetched page
    """
    page = Page(url)
    if not page.is_secure():
        page.make_secure()
    return load_page(page, retries=retries, timeout=timeout)


def scrape_page(
    url: str, visited: List[Page], root_url: str, parent: str, ignore: str = None
) -> Page:
    """
    Scrape the content of a page by fetching the URL and parsing the HTML content.

    Args:
        url (str): _description_ to scrape
        visited (List[Page]): _description_ of pages that have already been visited
        root_url (str): _description_ of the root URL
        ignore (str, optional): _description_. Defaults to None. Regex Patterns to ignore in url

    Returns:
        Page: _description_ with the content and status code of the fetched page
    """
    ignore_patterns = ignore.split(",") if ignore else []
    if any(re.match(pattern, url) for pattern in ignore_patterns):
        return None
    if url.endswith("/"):
        url = url[:-1]
    if is_relative(url):
        url = get_absolute_url(root_url, url)
    if not url or is_anchor(url):
        return None
    idx = [i for i, page in enumerate(visited) if page.url == url]
    if idx:
        element = visited[idx[0]]
        element = copy.copy(element)
        element.parent = parent
        return element
    LOG.info("Scraping page: %s", url)
    page = load_url(url)
    page.parent = parent
    visited.append(page)
    links = get_links(page)
    children_links = [link for link in links]
    children_links = [link for link in links if link not in visited]
    children_links = [link for link in links if is_internal(link, root_url)]
    children_links = list(set(children_links))
    children = [
        scrape_page(link, visited, root_url, url, ignore=ignore)
        for link in children_links
    ]
    external = [link for link in links if is_external(link, root_url)]
    external = [
        ExternalPage(link, parent=page) for link in external if link is not None
    ]
    page.children = children
    page.external = external
    return page
