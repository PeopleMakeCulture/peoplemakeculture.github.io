import csv
import os

CAPTURES = "scripts/imagecaptures.csv"
with open(CAPTURES) as f:
    images_to_archive: list[tuple[str, str, str, str]] = [
        (row["article"], row["url"], row["uuid"], row["extension"])
        for row in csv.DictReader(f)
    ]

archived_articles = set([article for (article, _, _, _) in images_to_archive])
for article in archived_articles:
    old_filename = f"./{article}.html"
    new_filename = f"./archive/{article}/index.html"
    if not os.path.isfile(old_filename):
        continue
    print(f"Inspecting {article}.html")

    # Read old file
    with open(old_filename) as f:
        old_contents = f.read()

    # If a new file exists, read it
    archived_new_contents = ""
    try:
        with open(new_filename) as f:
            archived_new_contents = f.read()
    except:
        pass

    # Perform all rewrites
    new_contents = old_contents
    for row_article, url, uuid, extension in images_to_archive:
        if article != row_article:
            continue
        if extension == "" or extension == "n/a":
            continue
        new_contents = new_contents.replace(
            f"'{url}'", f"'/images/{article}/{uuid}.{extension}'"
        ).replace(f'"{url}"', f'"/images/{article}/{uuid}.{extension}"')

    if new_contents == archived_new_contents:
        print("No changes.")
        continue
    if not os.path.isdir(f"archive"):
        os.mkdir("archive")
    if not os.path.isdir(f"archive/{article}"):
        os.mkdir(f"archive/{article}")
    with open(new_filename, "w") as f:
        f.write(new_contents)
    print(f"Wrote {new_filename}")
