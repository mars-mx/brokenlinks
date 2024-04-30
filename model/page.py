import logging
import re
from typing import List

from bs4 import BeautifulSoup

from model.error import InvalidURL

LOG = logging.getLogger(__name__)
_URL_REGEX = (
    r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
)


class Page(object):
    content: BeautifulSoup = None
    status_code: int = None
    url: str = None
    parent: "Page" = None

    children: List["Page"] = []
    external: List["ExternalPage"] = []

    @staticmethod
    def validate(url: str, fail_on_invalid: bool = True):
        valid = re.match(_URL_REGEX, url)
        if not valid and fail_on_invalid:
            raise InvalidURL(f"Invalid URL: {url}")
        return valid

    def is_secure(self: "Page") -> bool:
        return self.url.startswith("https")

    def make_secure(self: "Page"):
        self.url = self.url.replace("http://", "https://")
        if not self.url.startswith("https"):
            self.url = f"https://{self.url}"

    def __init__(self: "Page", url: str):
        Page.validate(url)
        self.url = url

    def __str__(self):
        return f"{self.parent}->{self.url}"


class ExternalPage(object):
    url: str = None
    parent: Page = None

    def __init__(self: str, url: str, parent: Page = None):
        self.url = url
        self.parent = parent

    def __str__(self):
        return f"{self.parent}->{self.url}"
