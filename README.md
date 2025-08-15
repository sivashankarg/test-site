# letsdiveintoweb

Static blog with:
- Single-file UI (`index.html`)
- Markdown posts in `/posts`
- Auto-built `posts.json` + `rss.xml` via GitHub Actions
- SVG logo + favicon set in `/assets`

## Local edit
- Add a new post: create `posts/<your-slug>.md` with frontmatter:
```
---
title: My Post
date: 2025-08-15
excerpt: one-liner summary
tags: web, notes
---
# My Post
Content...
```
- Commit & push. The GitHub Action will regenerate `posts.json` and `rss.xml`.
