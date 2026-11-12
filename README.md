# Junha Ham — Academic homepage

Website: [junhaham.github.io](https://junhaham.github.io/)

A responsive academic homepage with publications, research experience, education, a downloadable CV, and a profile photo. Built with HTML, CSS, JavaScript, and a small Python renderer; no third-party runtime dependencies.

## Edit content

- `content.json`: contact details, publications, abstracts, research experience, and the profile photo path.
- `src/homepage.html.in`: biography, education, activities, and page structure.
- `assets/style.css`: typography, layout, and photo framing.
- `assets/profile-conference.jpg`: profile photo. Displayed as a 160px circle on desktop and a 144px circle on mobile, framed from the head through the arms.
- `assets/pdf/Junha_Ham_CV.pdf`: downloadable CV.

After editing, rebuild the homepage:

```sh
python3 scripts/build.py
```

Open `index.html` for the complete page. The legacy `src/template.html` address redirects to it.

## Preview locally

```sh
python3 -m http.server 4173 --bind 127.0.0.1
```

Visit [127.0.0.1:4173](http://127.0.0.1:4173/).

## Publish

The `Publish academic website` workflow builds and deploys pushes to `main` through GitHub Pages. The repository's Pages publishing source should be **GitHub Actions**. It can also be run manually from the Actions tab.

The deployed artifact contains the generated pages and assets. Source templates and editing metadata remain in the repository.
