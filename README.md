# Seungwan Jin — Academic homepage

Personal academic website: **https://seun9wanjin.github.io/**

A responsive, dependency-free static site. GitHub Pages publishes the root of the `main` branch. No package installation or build service is required to serve the site.

## Update content

- Publication records, education, experience, honors, and service: `data/profile.json`
- Biography, news, and research summaries: `scripts/build.py`
- Layout and responsive styling: `assets/style.css`
- Downloadable public CV: `assets/docs/CV-Seungwan-Jin.pdf`

After editing content, regenerate the static page:

```sh
python3 scripts/build.py
```

Commit the updated source **and** `index.html`, then push to `main`. GitHub Pages will publish the changes.

## Local preview

```sh
python3 -m http.server 8000
```

Open http://localhost:8000. All content is static HTML; no JavaScript is required.

## Assets and attribution

The profile photograph is the author-provided formal portrait. The design and implementation are original, informed by the academic websites supplied as references.

The downloadable CV is the author's original PDF. Replace `assets/docs/CV-Seungwan-Jin.pdf` with the latest approved file and rebuild; the CV link includes a content version so visitors receive the updated PDF.
