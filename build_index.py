import os, re, json, datetime, html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
POSTS_DIR = ROOT / "posts"
SITE_URL = os.getenv("SITE_URL", "").rstrip("/")

def parse_post(md_path: Path):
    text = md_path.read_text(encoding="utf-8")
    fm = {}
    m = re.match(r"^---\s*(.*?)\s*---\s*", text, flags=re.S)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k,v = line.split(":",1)
                fm[k.strip()] = v.strip()
        body = text[m.end():]
    else:
        body = text
    title = fm.get("title") or (re.search(r"^# (.+)$", body, flags=re.M).group(1) if re.search(r"^# (.+)$", body, flags=re.M) else md_path.stem)
    date = fm.get("date") or datetime.date.today().isoformat()
    excerpt = fm.get("excerpt","")
    slug = md_path.stem
    tags = fm.get("tags","")
    tags = [t.strip() for t in tags.split(",") if t.strip()] if tags else []
    return {
        "slug": slug,
        "title": title,
        "date": date,
        "excerpt": excerpt,
        "tags": tags
    }

def build_posts_json(posts):
    (ROOT / "posts.json").write_text(json.dumps(posts, ensure_ascii=False, indent=2), encoding="utf-8")

def rfc2822(datestr):
    try:
        dt = datetime.datetime.strptime(datestr, "%Y-%m-%d")
    except ValueError:
        # fallback: now
        dt = datetime.datetime.utcnow()
    return dt.strftime("%a, %d %b %Y %H:%M:%S +0000")

def build_rss(posts):
    items = []
    for p in posts:
        link = f"{SITE_URL}/#/post/{p['slug']}" if SITE_URL else f"#/post/{p['slug']}"
        item = (
f"""  <item>
    <title>{html.escape(p['title'])}</title>
    <link>{html.escape(link)}</link>
    <guid>{html.escape(link)}</guid>
    <pubDate>{rfc2822(p['date'])}</pubDate>
    <description><![CDATA[{p.get('excerpt','')}]]></description>
  </item>""")
        items.append(item)
    rss = (
f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
  <title>letsdiveintoweb</title>
  <link>{html.escape(SITE_URL or '')}</link>
  <description>yo lets just explore the most intertwined world wide web…</description>
  <language>en</language>
{os.linesep.join(items)}
</channel>
</rss>""")
    (ROOT / "rss.xml").write_text(rss, encoding="utf-8")

def main():
    posts = [parse_post(p) for p in sorted(POSTS_DIR.glob("*.md"))]
    posts.sort(key=lambda x: x["date"], reverse=True)
    build_posts_json(posts)
    build_rss(posts)

if __name__ == "__main__":
    main()
