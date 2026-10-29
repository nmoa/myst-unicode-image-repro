# MyST / Sphinx Unicode image path reproduction

Minimal reproducer for a suspected issue: a normal Markdown image reference
containing non-ASCII path components is percent-encoded, and the corresponding
image may not be copied to the Sphinx HTML output.

This is a **test case**, not a claim that every version is affected.

## Test cases

| Case | Markdown | Expected |
| --- | --- | --- |
| ASCII control | `![ASCII control](images/diagram.png)` | Image copied and displayed |
| Japanese filename | `![Japanese filename](images/構成図.png)` | Image copied and displayed |
| Japanese directory | `![Japanese directory](図面/diagram.png)` | Image copied and displayed |

All three references use ordinary Markdown image syntax, without a custom
directive or manual asset-copy workaround.

## Run locally

Requires Python 3.12+.

```sh
python -m pip install -r requirements.txt
sphinx-build -E -a -b html docs _build/html
python scripts/check_output.py _build/html/index.html
```

## GitHub Actions

The workflow tests MyST-Parser 5.1.0 against Sphinx 9.1.1 and 9.2.0.
It reports whether each referenced image exists at the browser-resolved
location, and uploads the generated HTML and Sphinx build log.

- ASCII PASS / Japanese FAIL: suspected Unicode path bug reproduced.
- All PASS: issue not reproduced in that environment.
- ASCII FAIL: the baseline itself is broken.

A failed Unicode case intentionally fails CI, while the workflow still
uploads diagnostic artifacts.

## Reporting upstream

- MyST-Parser: https://github.com/executablebooks/MyST-Parser/issues
- Sphinx: https://github.com/sphinx-doc/sphinx/issues

Include the failing dependency versions, HTML image `src`, generated image
files, and build log when reporting.
