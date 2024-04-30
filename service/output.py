import logging
from typing import List
import csv

from model.page import ExternalPage, Page

LOG = logging.getLogger("brokenlinks")


def _get_not_found(page, visited):
    if not page:
        return []
    if isinstance(page, ExternalPage):
        return []
    if page.url in [p.url for p in visited]:
        return []
    if page.status_code == 404:
        return [page]
    visited.append(page)
    not_found = []
    for child in page.children:
        not_found.extend(_get_not_found(child, visited))
    return not_found


def get_not_found(page: Page) -> List[Page]:
    result = _get_not_found(page, [])
    return result


def _get_external(page: Page, visited: List[Page], root_url: str):
    if not page:
        return []
    if isinstance(page, ExternalPage):
        return []
    idx = [i for i, p in enumerate(visited) if p.url == page.url]
    if idx:
        return visited[idx[0]].external
    result = []
    for link in page.external:
        result.append(link)
    visited.append(page)
    for child in page.children:
        result.extend(_get_external(child, visited, root_url))
    return list(set(result))


def get_external_links(page: Page, root_url: str) -> List[ExternalPage]:
    result = _get_external(page, [], root_url)
    return result


def to_csv(page: Page, path: str, root_url: str):
    headers = ["url", "status_code", "parent", "type"]
    external = get_external_links(page, root_url)
    not_found = get_not_found(page)
    LOG.info("Found %s external links", len(external))
    LOG.info("Found %s not found links", len(not_found))
    with open(path, "w") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for page in not_found:
            writer.writerow(
                [
                    page.url,
                    page.status_code,
                    page.parent if page.parent else "root",
                    "not_found",
                ]
            )
        for page in external:
            writer.writerow([page.url, "-", page.parent, "external"])
        LOG.info("Wrote output to %s", path)
