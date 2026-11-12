#!/usr/bin/env python3
"""Render the academic homepage using only the Python standard library."""
import hashlib
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / 'content.json').read_text())
e = html.escape

def authors(names):
    parts = []
    for name in names:
        mark = name[-1] if name[-1] in '*†' else ''
        plain = name[:-1] if mark else name
        part = e(plain)
        if plain == data['name']:
            part = '<strong>' + part + '</strong>'
        if mark:
            part += '<sup>' + e(mark) + '</sup>'
        parts.append(part)
    return ', '.join(parts[:-1]) + ', and ' + parts[-1]

def bibtex(p):
    names = []
    for author in p['authors']:
        words = author.rstrip('*†').split()
        names.append(words[-1] + ', ' + ' '.join(words[:-1]))
    category = 'unpublished' if p['status'] == 'Under review' else 'inproceedings'
    venue_key = 'note' if category == 'unpublished' else 'booktitle'
    return ('@' + category + '{ham' + str(p['year']) + p['id'].replace('-', '') + ',\n'
            + '  title = {' + p['title'] + '},\n'
            + '  author = {' + ' and '.join(names) + '},\n'
            + '  year = {' + str(p['year']) + '},\n'
            + '  ' + venue_key + ' = {' + p['venue'] + '}'
            + (',\n  url = {' + p['url'] + '}' if p.get('url') else '') + '\n}')

pubs = []
for p in data['publications']:
    title = e(p['title'])
    if p.get('url'):
        title = '<a href="' + e(p['url'], quote=True) + '" target="_blank" rel="noopener noreferrer">' + title + '</a>'
    paper_link = ('<a class="paper-link" href="' + e(p['url'], quote=True) + '" target="_blank" rel="noopener noreferrer">OpenReview</a>') if p.get('url') else ''
    venue = e(p['venue']) + (', ' + str(p['year']) if p['status'] == 'Under review' else '')
    pubs.append(f'''<article class="publication" id="{e(p['id'])}" aria-labelledby="title-{e(p['id'])}">
  <h3 class="pub-title" id="title-{e(p['id'])}">{title}</h3>
  <p class="pub-authors">{authors(p['authors'])}</p>
  <p class="pub-venue">{venue}</p>
  <div class="pub-actions">{paper_link}
    <details class="pub-details"><summary>Abstract</summary><p class="abstract-text">{e(p['abstract'])}</p></details>
    <details class="pub-details"><summary>BibTeX</summary><pre class="citation-code">{e(bibtex(p))}</pre><button type="button" class="copy-button" data-copy>Copy citation</button></details>
  </div>
</article>''')
experiences = []
for item in data['research']:
    advisor = (' · Advisor: <a href="' + e(item['advisor_url'], quote=True) + '" target="_blank" rel="noopener noreferrer">Prof. ' + e(item['advisor']) + '</a>') if item.get('advisor') else ''
    experiences.append(f'''<article class="entry">
  <div class="entry-heading"><h3>{e(item['title'])}<span class="entry-organization">, {e(item['organization'])}</span></h3><p class="dates">{e(item['date'])}</p></div>
  <p class="role">{e(item['role'])}{advisor}</p>
  <ul>{''.join('<li>' + e(point) + '</li>' for point in item['points'])}</ul>
</article>''')
schema = {'@context': 'https://schema.org', '@type': 'Person', 'name': data['name'], 'url': data['url'] + '/', 'email': 'mailto:' + data['email'], 'jobTitle': 'Undergraduate Researcher', 'affiliation': {'@type': 'Organization', 'name': 'Seoul National University'}, 'sameAs': ['https://github.com/' + data['github']], 'knowsAbout': ['Causal machine learning', 'Causal foundation models', 'World models', 'Robot learning and perception']}
photo_path = data.get('profile_photo')
if photo_path:
    photo_file = (ROOT / photo_path).resolve()
    if not photo_file.is_relative_to(ROOT) or not photo_file.is_file():
        raise ValueError('profile_photo must name an existing image inside the website folder.')
    profile_photo = f'<img src="{e(photo_path, quote=True)}" alt="{e(data["name"])}" width="160" height="160">'
else:
    profile_photo = '<div class="photo-placeholder" role="img" aria-label="Profile photo placeholder"><span>Profile photo</span></div>'
page = (ROOT / 'src/homepage.html.in').read_text()
values = {'URL': e(data['url']), 'EMAIL': e(data['email']), 'GITHUB': e(data['github']), 'YEAR': str(data['year']), 'UPDATED': e(data['updated']), 'SCHEMA': json.dumps(schema, ensure_ascii=False).replace('<', '\\u003c'), 'PUBLICATIONS': '\n'.join(pubs), 'EXPERIENCE': '\n'.join(experiences), 'PROFILE_PHOTO': profile_photo, 'STYLE_VERSION': hashlib.sha256((ROOT / 'assets/style.css').read_bytes()).hexdigest()[:12]}
for key, value in values.items():
    page = page.replace('__' + key + '__', value)
(ROOT / 'index.html').write_text(page)
(ROOT / 'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: ' + data['url'] + '/sitemap.xml\n')
(ROOT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>' + data['url'] + '/</loc></url></urlset>\n')
print(f"Built homepage: {len(pubs)} publications, {len(experiences)} research entries.")
