import logging
import click

from config.logger import setup_logging
from service.output import to_csv
from service.parse import get_root_url
from service.scrape import scrape_page

LOG = logging.getLogger("brokenlinks")


def _preflight():
    setup_logging()


@click.command()
@click.option("--url", help="The URL to scrape.", required=True)
@click.option("--ignore", help="Regex pattern in URLs to ignore.", default=None)
@click.option("--output", help="Output file path.", default="output.csv")
def scrape(url: str, ignore: str = None, output: str = "output.csv"):
    LOG.info("Loading page: %s", url)
    root_url = get_root_url(url)
    visited = []
    page = scrape_page(url, visited, root_url=root_url, parent=None, ignore=ignore)
    to_csv(page, output, root_url)


if __name__ == "__main__":
    _preflight()
    scrape()
