from io import TextIOWrapper

from sqlalchemy import select
from common.models import Site, CategorySiteRelation
import click
from server.manager.db import _SqlSession  # type: ignore


def add_site(name: str, urls: list[str]) -> int:
    with _SqlSession() as db:
        existed = db.scalar(
            select(Site.id).where((Site.name == name) | (Site.url == urls))
        )
        if existed:
            return existed
        site = Site(name=name, url=urls)
        db.add(site)
        db.commit()
        db.flush()
        return site.id


def link_site_to_category(site_id: int, category_id: int) -> None:
    with _SqlSession() as db:
        if db.scalar(
            select(CategorySiteRelation)
            .where(CategorySiteRelation.site_id == site_id)
            .where(CategorySiteRelation.category_id == category_id)
        ):
            return
        relation = CategorySiteRelation(site_id=site_id, category_id=category_id)
        db.add(relation)
        db.commit()
        db.flush()


@click.command()
@click.option(
    "--csv",
    type=click.File("r", encoding="utf-8"),
    help="CSV file containing sites to add",
)
@click.option(
    "--category",
    "-c",
    default=None,
    type=int,
    help="add these sites to a specific category",
)
def main(csv: TextIOWrapper, category: int | None):
    if not csv:
        print("No CSV file provided.")
        return
    # parse
    print("Parsing CSV file...")
    sites: list[tuple[str, list[str]]] = []
    for line in csv.readlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split(",")
        if len(parts) < 2:
            print(f"Skipping invalid line: {line}")
            continue
        name = parts[0].strip()
        url = [u.strip() for u in parts[1:]]
        sites.append((name, url))
    print(f"Found {len(sites)} sites to add.")

    # add sites
    print("Adding sites...")
    for name, urls in sites:
        site_id = add_site(name, urls)
        if not site_id:
            print(f"Add site {name} failed.")
            return
        if category:
            link_site_to_category(site_id, category)
    print("All sites added successfully.")


if __name__ == "__main__":
    main()
