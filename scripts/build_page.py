import os
import json
import urllib.request

GH_USER = os.environ["GH_USER"]
GH_TOKEN = os.environ["GH_TOKEN"]

def gh_get(url):
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {GH_TOKEN}",
        "Accept": "application/vnd.github+json",
        "User-Agent": GH_USER,
    })
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

def search_repos():
    url = f"https://api.github.com/search/repositories?q=user:{GH_USER}+topic:ai-pm-portfolio"
    return gh_get(url)["items"]

def fetch_meta(full_name, branch):
    url = f"https://raw.githubusercontent.com/{full_name}/{branch}/meta.json"
    req = urllib.request.Request(url, headers={"User-Agent": GH_USER})
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except Exception:
        return None

def card_html(entry):
    tags = ", ".join(entry.get("tags", []))
    return f"""
    <div class="card">
      <h2><a href="{entry['url']}">{entry.get('title', entry['url'])}</a></h2>
      <span class="status">{entry.get('status','unknown')}</span>
      <p>{entry.get('summary','')}</p>
      <p class="tags">{tags}</p>
    </div>"""

STATUS_RANK = {"done": 0, "active": 1, "planned": 2}

def sort_key(entry):
    """Reihenfolge der Karten auf der Portfolio-Seite.

    Zuerst nach Status (done, active, planned; Unbekanntes ans Ende),
    bei gleichem Status alphabetisch nach Titel.
    """
    rank = STATUS_RANK.get(entry.get("status", ""), len(STATUS_RANK))
    return (rank, entry.get("title", "").lower())

def main():
    repos = search_repos()
    entries = []
    for repo in repos:
        meta = fetch_meta(repo["full_name"], repo["default_branch"])
        if meta is None:
            continue
        meta["url"] = repo["html_url"]
        entries.append(meta)

    cards = [card_html(e) for e in sorted(entries, key=sort_key)]

    html = f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<title>AI Product Manager Portfolio</title>
<style>
  body {{ font-family: sans-serif; max-width: 800px; margin: 40px auto; padding: 0 16px; }}
  .card {{ border: 1px solid #ddd; border-radius: 8px; padding: 16px; margin-bottom: 16px; }}
  .status {{ font-size: 0.8em; padding: 2px 8px; border-radius: 4px; background: #eee; }}
  .tags {{ color: #666; font-size: 0.9em; }}
</style>
</head>
<body>
<h1>AI Product Manager Portfolio</h1>
{"".join(cards) if cards else "<p>Noch keine Use-Case-Repos veröffentlicht.</p>"}
</body>
</html>"""

    with open("index.html", "w") as f:
        f.write(html)

if __name__ == "__main__":
    main()
