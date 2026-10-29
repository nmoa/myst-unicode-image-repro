# MyST / Sphinx: Unicode image filenames reproduction

A minimal reproducer for a suspected bug where **a standard Markdown image link
with non-ASCII path components** is percent-encoded by the Markdown parser and
Sphinx does not find/copy the referenced file into the built static site.

This repository is a **test case**, not a claim that every listed version is affected.
The GitHub Actions matrix records the actual behavior, including whether the issue
has been fixed.

## Inputs

All three images are valid PNG files and are referenced using the *same*
standard Markdown syntax, `![alt](path)`:

| Case | Markdown source | Intended result |
| --- | --- | --- |
| ASCII control | `![ASCII control](images/diagram.png)` | Copied and displayed |
| Japanese filename | `![Japanese filename](images/構成図.png)` | Copied and displayed |
| Japanese directory | `![Japanese directory](図面/diagram.png)` | Copied and displayed |

No custom image directive, `html_extra_path`, manual copy, or URL rewriting is used:
those could mask the issue being tested.

## Run locally (Python 3.12+)

```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
sphinx-build -E -a -b html docs _build/html
python scripts/check_output.py _build/html/index.html
```

The pinned local configuration is **MyST-Parser 5.1.0 + Sphinx 9.2.0**.
GitHub Actions tests **Sphinx 9.1.1 and 9.2.0** with MyST-Parser 5.1.0.

## How to interpret results

- **PASS (ASCII)** and **FAIL (Japanese)**: the Unicode image path issue is reproduced.
- **PASS (all three)**: not reproduced with that dependency combination.
- **FAIL (ASCII)**: the setup itself is broken; investigate before filing an upstream bug.

The verifier inspects rendered `<img src="...">` values, URL-decodes the browser-facing
path, and checks whether the referenced file actually exists under `_build/html`.
It also prints copied PNG paths. The GitHub Actions job intentionally returns a
non-zero exit status if an expected Unicode asset is missing and uploads the HTML
and build log regardless of the result.

## Publishing as your own GitHub repository

Unzip/download these files, change into this directory, and run:

```bash
git init -b main
git add .
git commit -m "Add minimal Sphinx/MyST Unicode image reproducer"
gh repo create myst-unicode-image-repro --public --source=. --remote=origin --push
```

Choose `--private` instead of `--public` if you do not want a public repository.
GitHub CLI (`gh`) must be authenticated first (`gh auth login`).

## Upstream bug-report pointers

- MyST-Parser: https://github.com/executablebooks/MyST-Parser/issues/new/choose
- Sphinx: https://github.com/sphinx-doc/sphinx/issues/new/choose

Include the failing workflow's Sphinx/MyST versions, build warnings, generated HTML
`src` attributes, and asset file list. Those establish whether the image was not
copied (asset handling) versus copied under the wrong path (URI handling).
