import time
import requests
import re
from urllib.parse import urlparse, parse_qs

import time, requests, re

def fetch_all_screens(appid, delay=1.0, browsefilter="toprated"):
    import time, requests, re

    session = requests.Session()
    session.headers.update({
        "User-Agent":       "Mozilla/5.0 (X11; Linux x86_64)",
        "Referer":          f"https://steamcommunity.com/app/{appid}/screenshots/?browsefilter={browsefilter}",
        "X-Requested-With": "XMLHttpRequest",
        "Accept-Language":  "en-US,en;q=0.9",
    })

    seen = set()
    page = 1

    # reset urls.txt
    open("urls.txt", "w").close()

    # regex to catch the base UGC path (no query)
    pattern = re.compile(r'(https://images\.steamusercontent\.com/ugc/[A-Za-z0-9/]+/)')

    while True:
        resp = session.get(
            f"https://steamcommunity.com/app/{appid}/screenshots/render",
            params={"browsefilter": browsefilter, "p": page, "l": "english"}
        )
        resp.raise_for_status()

        bases = set(pattern.findall(resp.text))
        new_bases = [b for b in bases if b not in seen]
        if not new_bases:
            break

        with open("urls.txt", "a", encoding="utf-8") as f:
            for base in new_bases:
                seen.add(base)
                max_url = (
                    base
                    + "?imw=5000&imh=5000&ima=fit"
                    + "&impolicy=Letterbox&imcolor=%23000000&letterbox=false"
                )
                f.write(max_url + "\n")

        print(f"Page {page}: +{len(new_bases)} screenshots (total {len(seen)})")
        page += 1
        time.sleep(delay)

    print(f"Done: collected {len(seen)} screenshots")
    return seen



if __name__ == "__main__":
    urls = fetch_all_screens(1222670)

