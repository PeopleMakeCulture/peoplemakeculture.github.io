from bs4 import BeautifulSoup
import os
import csv
from uuid import uuid4
import requests
from time import sleep

CAPTURES = "scripts/imagecaptures.csv"
mime = {"image/png": "png", "image/jpeg": "jpg"}

images_to_archive: list[dict[str, str]] = []
try:
    with open(CAPTURES) as f:
        for row in csv.DictReader(f):
            images_to_archive.append(
                {
                    "article": row["article"],
                    "url": row["url"],
                    "uuid": row["uuid"],
                    "extension": row["extension"],
                }
            )
except:
    pass


def write_to_archive():
    with open(CAPTURES, "w") as f:
        writer = csv.DictWriter(f, fieldnames=["article", "url", "uuid", "extension"])
        writer.writeheader()
        for row in images_to_archive:
            writer.writerow(row)


for filename in os.listdir("."):
    if not filename.endswith(".html"):
        continue
    print(f"Inspecting {filename}")

    base = filename[:-5]
    with open(filename) as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    for img_tag in soup.find_all("img"):
        url = img_tag.get("src")
        if any(
            [base == row["article"] and url == row["url"] for row in images_to_archive]
        ):
            continue
        new_row: dict[str, str] = {
            "article": base,
            "url": url,
            "uuid": str(uuid4()),
            "extension": "",
        }
        images_to_archive.append(new_row)

        print(base, url)

    write_to_archive()


for row in images_to_archive:
    article = row["article"]
    url = row["url"]
    uuid = row["uuid"]
    extension = row["extension"]
    if extension != "":
        continue

    if url[0] == "/":
        url = f"https://wayback.archive-it.org{url}"

    print(f"reading {url}...")
    response = requests.get(url)
    extension = mime[response.headers["content-type"]]
    if not os.path.isdir(f"images/{article}"):
        os.mkdir(f"images/{article}")
    with open(f"images/{article}/{uuid}.{extension}", "wb") as fb:
        fb.write(response.content)

    row["extension"] = extension
    write_to_archive()
    print(f"done.")
    sleep(30)
