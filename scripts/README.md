# Scripts for peoplemakeculture.com

## Wayback Machine Repair

Initial setup:

```
python3 -m venv venv
source venv/bin/activate
pip install -r dev/requirements.txt
```

The `capture_assets.py` script finds and collects assets in wayback-downloaded files `./{article_name}.html`. The `rewrite_articles.py` rewrites said articles and moves them to `./archive/{article_name}/index.html`, at which point the original html file can be deleted.

```
source venv/bin/activate
python scripts/capture_assets.py
python scripts/rewrite_articles.py
```

The two scripts use the CSV scripts/assetcapture.csv as persistent storage. If the "extension" column is empty, the `capture_assets.py` script assumes it has _not_ downloaded the image and needs to. Using the extension `n/a` indicates that as URL should not be messed with (see line 62 of imagecaptures.csv for an example).
