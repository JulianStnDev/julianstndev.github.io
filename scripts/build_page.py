import os
import json
import html
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

INTRO = (
    "Product Manager building hands-on AI product skills. This portfolio documents "
    "projects I built myself with Claude Code \u2013 from structured output and "
    "evaluation to RAG, agents with MCP, and a deployed agent with human-in-the-loop "
    "approval. Each project answers a product question with measured quality, cost "
    "and latency, not just a demo."
)

def card_html(entry):
    e = html.escape
    tags = ", ".join(entry.get("tags", []))
    metrics = "".join(f"<li>{e(m)}</li>" for m in entry.get("metrics", []))
    links = [f'<a href="{e(entry["url"])}">Repository</a>']
    demo = entry.get("demo")
    if demo:
        note = f' ({e(demo["note"])})' if demo.get("note") else ""
        links.append(f'<a href="{e(demo["url"])}">Live demo</a>{note}')
    shot = ""
    if entry.get("screenshot_url"):
        shot = (f'<a href="{e(entry["screenshot_url"])}"><img src="{e(entry["screenshot_url"])}" '
                f'alt="Screenshot of {e(entry.get("title", ""))}" loading="lazy"></a>')
    return f"""
    <div class="card">
      <h2>{e(entry.get('title', entry['url']))}</h2>
      <span class="status">{e(entry.get('status','unknown'))}</span>
      <p>{e(entry.get('summary',''))}</p>
      {f'<ul class="metrics">{metrics}</ul>' if metrics else ''}
      {shot}
      <p class="links">{" · ".join(links)}</p>
      <p class="tags">{e(tags)}</p>
    </div>"""

STATUS_RANK = {"done": 0, "active": 1, "planned": 2}

def sort_key(entry):
    """Reihenfolge der Karten auf der Portfolio-Seite.

    Zuerst nach Status (done, active, planned; Unbekanntes ans Ende),
    bei gleichem Status nach Repo-Name, also in UC-Reihenfolge (ai-uc-01, ai-uc-02, ...).
    """
    rank = STATUS_RANK.get(entry.get("status", ""), len(STATUS_RANK))
    return (rank, entry["repo"].lower())

def main():
    repos = search_repos()
    entries = []
    for repo in repos:
        meta = fetch_meta(repo["full_name"], repo["default_branch"])
        if meta is None:
            continue
        meta["url"] = repo["html_url"]
        meta["repo"] = repo["name"]
        if meta.get("screenshot"):
            meta["screenshot_url"] = (f"https://raw.githubusercontent.com/{repo['full_name']}/"
                                      f"{repo['default_branch']}/{meta['screenshot']}")
        entries.append(meta)

    cards = [card_html(e) for e in sorted(entries, key=sort_key)]

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI Product Manager Portfolio</title>
<style>
  body {{ font-family: sans-serif; max-width: 800px; margin: 40px auto; padding: 0 16px; }}
  .card {{ border: 1px solid #ddd; border-radius: 8px; padding: 16px; margin-bottom: 16px; }}
  .status {{ font-size: 0.8em; padding: 2px 8px; border-radius: 4px; background: #eee; }}
  .tags {{ color: #666; font-size: 0.9em; }}
  .intro {{ font-size: 1.05em; line-height: 1.5; }}
  .metrics {{ padding-left: 20px; }}
  img {{ max-width: 100%; border: 1px solid #ddd; border-radius: 4px; }}
</style>
</head>
<body>
<h1>AI Product Manager Portfolio</h1>
<p class="intro">{INTRO}</p>
{"".join(cards) if cards else "<p>No projects published yet.</p>"}
</body>
</html>"""

    with open("index.html", "w") as f:
        f.write(html)

if __name__ == "__main__":
    main()
