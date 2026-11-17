#!/usr/bin/env python3
"""Build a dependency-free academic homepage from data/profile.json."""
import json
from hashlib import sha256
from pathlib import Path
from html import escape as e

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / 'data/profile.json').read_text())
css_version = sha256((ROOT / 'assets/style.css').read_bytes()).hexdigest()[:12]
pubs = data['publications']
by_id = {p['id']: p for p in pubs}
by_id['fashion-fine']['links']['code'] = 'https://github.com/seun9wanjin/Fashion-FINE'
by_id['label-aware']['links']['code'] = 'https://github.com/Hanyang-HCC-Lab/LAHN'
by_id['triple-aaai']['links']['project'] = 'https://yestaehyung.github.io/aaai26-triple/'

def link(url, text, cls=''):
    return f'<a href="{e(url, quote=True)}"' + (f' class="{cls}"' if cls else '') + f'>{text}</a>'

def topic(p):
    if p['area'] in ['Longitudinal personalization', 'Mental health & well-being']:
        return 'personal'
    if p['area'] == 'Multimodal & interpretable AI':
        return 'multimodal'
    return 'interaction'

def publication(p):
    authors = []
    for idx, author in enumerate(p['authors']):
        rendered = f'<strong>{e(author)}</strong>' if author == 'Seungwan Jin' else e(author)
        if p['role'] == 'co-first' and idx < 2:
            rendered += '<sup>*</sup>'
        authors.append(rendered)
    links = ' '.join(link(url, {'paper':'Paper', 'doi':'DOI', 'code':'Code', 'project':'Project', 'record':'Publication record'}[key]) for key, url in p['links'].items())
    note = p.get('note', '')
    if note.startswith('Equal contribution'):
        note = ''  # A single legend explains all asterisks.
    if p['id'] == 'icev2':
        note = 'Online publication: November 2024'
    is_award = 'Award' in note
    title_url = p['links'].get('paper') or p['links'].get('doi') or p['links'].get('project')
    title = link(title_url, e(p['title'])) if title_url else e(p['title'])
    note_html = f'<span class="pub-note {"award" if is_award else ""}">{e(note)}</span>' if note else ''
    accepted = ' <span class="status">To appear</span>' if p['status'] == 'accepted' else ''
    return f'''<li class="publication" id="paper-{p['id']}">
      <h3>{title}</h3><p class="authors">{', '.join(authors)}</p>
      <p class="pub-venue">{e(p['venue'])} {p['year']}{accepted}</p>
      <div class="pub-bottom"><div class="pub-links">{links}</div>{note_html}</div>
    </li>'''

main_pubs = sorted((p for p in pubs if p['type'] in ['conference', 'journal']), key=lambda p: -p['year'])
companion_pubs = sorted((p for p in pubs if p['type'] in ['companion', 'workshop']), key=lambda p: -p['year'])
publications = '\n'.join(publication(p) for p in main_pubs)
companion_publications = '\n'.join(publication(p) for p in companion_pubs)
books_reports = '\n'.join(f'<li><h3>{link(b["links"]["report"], e(b["title"]))}</h3><p>{e(b["publisher"])}, {b["year"]}.</p><p class="book-credit">{e(b["type"])} (in {e(b["language"])}). {e(b["user_role"])}.</p></li>' for b in data.get('books_reports', []))
grants = '\n'.join(f'<li><h3>{e(g["program"])}</h3><p class="grant-title">{e(g["title"])}</p><p><strong>{e(g["role"])}</strong> · {e(g["funder"])}</p><p class="grant-details">{e(g["dates"])} · {e(g["funding"])}</p></li>' for g in data['grants'])
reviewers = '\n'.join(f'<li>Reviewer, {e(v["venue"])} ({e(v["years"])})</li>' for v in data['service']['reviewer'])

html = '''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Seungwan Jin | Human-Centered AI · KAIST</title>
  <meta name="description" content="Seungwan Jin is a postdoctoral researcher and Jang Young Sil Fellow at KAIST. His research spans longitudinal personalization, digital health, multimodal AI, and human–AI interaction.">
  <meta name="theme-color" content="#155e63">
  <link rel="canonical" href="https://seun9wanjin.github.io/">
  <meta property="og:type" content="profile">
  <meta property="og:title" content="Seungwan Jin | Human-Centered AI">
  <meta property="og:description" content="Postdoctoral Researcher and Jang Young Sil Fellow at KAIST. Longitudinal personalization, digital health, and human–AI interaction.">
  <meta property="og:url" content="https://seun9wanjin.github.io/">
  <meta property="og:image" content="https://seun9wanjin.github.io/assets/images/seungwan-jin-formal.png">
  <meta name="twitter:card" content="summary">
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="assets/style.css?v=__CSS_VERSION__">
  <script type="application/ld+json">{"@context":"https://schema.org","@type":"Person","name":"Seungwan Jin","url":"https://seun9wanjin.github.io/","image":"https://seun9wanjin.github.io/assets/images/seungwan-jin-formal.png","jobTitle":"Postdoctoral Researcher","affiliation":{"@type":"Organization","name":"KAIST"},"email":"seungwan@kaist.ac.kr","sameAs":["https://scholar.google.com/citations?user=OYYoqS0AAAAJ","https://github.com/seun9wanjin","https://www.linkedin.com/in/seungwanjin/"]}</script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<main id="main" class="wrap page-layout">
<aside class="profile-sidebar" aria-label="Profile">
  <img class="profile-photo" src="assets/images/seungwan-jin-formal.png" width="893" height="1200" alt="Seungwan Jin" fetchpriority="high">
  <nav class="profile-links" aria-label="Profiles and curriculum vitae">
    <a href="assets/docs/CV-Seungwan-Jin.pdf">CV</a>
    <a href="https://scholar.google.com/citations?user=OYYoqS0AAAAJ">Google Scholar</a>
    <a href="https://www.linkedin.com/in/seungwanjin/">LinkedIn</a>
    <a href="https://github.com/seun9wanjin">GitHub</a>
  </nav>
  <div class="profile-info"><h1>Seungwan Jin</h1><p class="profile-email">seungwan (at) kaist.ac.kr</p><p>Postdoctoral Researcher<br>Jang Young Sil Fellow<br><a href="https://www.kaist.ac.kr/en/">KAIST</a></p></div>
</aside>
<div class="main-content">
<section id="about" class="about" aria-labelledby="about-heading">
  <h2 id="about-heading">About Me</h2>
  <p>I am a postdoctoral researcher and Jang Young Sil Fellow (Excellence Track) at <a href="https://www.kaist.ac.kr/en/">KAIST</a>, working with <a href="https://ic.kaist.ac.kr/">Uichin Lee</a> in the <a href="https://ic.kaist.ac.kr/">Interactive Computing Lab</a>.</p>
  <p>My goal is to advance human–computer interaction and build <strong>human-centered AI that understands people and that people can understand</strong>. I combine multimodal learning, models of human behavior, and human-centered evaluation to study AI across mental health, everyday behavior, and online social interaction.</p>
  <p>My current interests follow two connected directions. <strong>(1) Longitudinal personalization:</strong> I study how personal AI can learn from everyday records, maintain and update memory, and adapt as people change.</p>
  <p><strong>(2) User simulation for agent evaluation and learning:</strong> I am interested in user digital twins and behavior-grounded simulation for evaluating and training personal agents. This includes reinforcement-learning environments informed by longitudinal user data, as well as representations that users can inspect and revise.</p>
  <p>I received my Ph.D. in Artificial Intelligence from Hanyang University, advised by <a href="https://hcc.hanyang.ac.kr/">Kyungsik Han</a>. From August 2019 to February 2020, I was a visiting scholar in the <a href="https://pike.psu.edu/">PIKE Lab</a> at Pennsylvania State University, working with <a href="https://pike.psu.edu/dongwon/">Dongwon Lee</a>.</p>
</section>

<section class="news" aria-labelledby="news-heading"><h2 id="news-heading">Recent News</h2><ul>
  <li><time datetime="2026">2026</time><p>Our paper on <a href="https://ic.kaist.ac.kr/publications/papers/jin2026dynamic.pdf">longitudinal mental health monitoring</a> was accepted to <strong>NeurIPS 2026</strong>. I will present it in Sydney in December.</p></li>
  <li><time datetime="2026-10">Oct 2026</time><p><a href="https://ic.kaist.ac.kr/publications/papers/yoo2026sonju.pdf">Sonju</a> received the <a class="news-award" href="https://www.ubicomp.org/ubicomp-iswc-2026/awards-all/">People’s Choice Student Challenge Award</a> at UbiComp / ISWC 2026. I co-advised the project with Uichin Lee.</p></li>
  <li><time datetime="2026">2026</time><p>Selected for the <strong>NRF Basic Research Program B (Inclusive Track)</strong> as Principal Investigator.</p></li>
  <li><time datetime="2026-04">Apr 2026</time><p>Joined KAIST as a <strong>Jang Young Sil Fellow (Excellence Track)</strong>.</p></li>
</ul></section>

<section id="publications" class="section" aria-labelledby="publications-heading">
  <div class="section-heading"><h2 id="publications-heading">Publications</h2></div>
  <p class="publication-caption"><sup>*</sup> Equal Contribution.</p>
  <h3 class="publication-group">Conference &amp; Journal Papers</h3>
  <ol id="publication-list" class="publication-list" reversed start="''' + str(len(main_pubs)) + '''">''' + publications + '''</ol>
  <h3 class="publication-group">Workshop, Demo &amp; Companion Papers</h3>
  <ol id="companion-list" class="publication-list" reversed start="''' + str(len(companion_pubs)) + '''">''' + companion_publications + '''</ol>
</section>

<section id="books" class="section books" aria-labelledby="books-heading">
  <div class="section-heading"><h2 id="books-heading">Books &amp; Reports</h2></div>
  <ol class="book-list" reversed>''' + books_reports + '''</ol>
</section>

<section id="grants" class="section grants" aria-labelledby="grants-heading">
  <div class="section-heading"><h2 id="grants-heading">Research Grants</h2></div>
  <ul class="grant-list">''' + grants + '''</ul>
</section>

<section id="service" class="section service" aria-labelledby="service-heading"><h2 id="service-heading">Academic Services</h2>
  <ul class="service-list">''' + reviewers + '''<li>Student Volunteer, CHI (2020)</li></ul>
</section>
<section id="teaching" class="section teaching" aria-labelledby="teaching-heading"><h2 id="teaching-heading">Teaching</h2>
  <ul class="service-list"><li>Teaching Fellow, Human-Computer Interaction (Fall 2025)</li><li>Co-lecturer, Creative Software Design (Fall 2021, 2022, 2023)</li><li>Co-lecturer, Introduction to Software Design (Spring 2022, 2023)</li></ul>
</section>
</div>
</main>
<footer class="site-footer wrap"><p>© 2026 Seungwan Jin</p><p>Updated November 2026 <span aria-hidden="true">·</span> <a href="https://github.com/seun9wanjin/seun9wanjin.github.io">Source</a></p></footer>
</body>
</html>
'''
(ROOT / 'index.html').write_text(html.replace('__CSS_VERSION__', css_version))
print(f'Built index.html with {len(pubs)} publications.')
