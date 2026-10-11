# Building and publishing documentation

The source of this site is `docs/` in the Git repository. Markdown is parsed by MyST and rendered by Sphinx. The same content is used locally and on Read the Docs.

## Build locally

From the repository root, in a documentation environment:

```bash
python -m pip install -r docs/requirements.txt
python -m sphinx -W --keep-going -b html docs docs/_build/html
```

Open `docs/_build/html/index.html`. Warnings fail the build so broken internal references and missing images must be fixed before publishing. The build does not read `xsdir`, private `user_db`, or import the application.

## Read the Docs

1. Connect the repository to your Read the Docs account and import the project.
2. Use the repository's `.readthedocs.yaml`: it sets the build environment, installs documentation dependencies, and points to `docs/conf.py`.
3. Build the intended branch and inspect its build log.
4. Verify the home page, navigation, formulas, figures, and download/source links.
5. Keep release documentation associated with the corresponding code version. Do not label an arbitrary branch as a validated release.

A successful local build or GitHub push does not by itself establish that the hosted project is connected or that its build succeeded. The hosted build log is the authority for that result.

See the official [Sphinx deployment guide](https://docs.readthedocs.com/platform/stable/intro/sphinx.html) and [configuration reference](https://docs.readthedocs.com/platform/stable/config-file/v2.html).

## GitHub checks and content policy

The Documentation workflow builds HTML on pushes and pull requests. Build products remain artifacts, not source-controlled pages. Keep screenshots in `docs/_static/images`, runnable teaching scripts in `examples/`, and user-facing topics in separate pages linked from the table of contents.

Do not commit `xsdir`, private overrides, saved scientific sessions, credentials, virtual environments, or local build outputs. Public documentation is in English. Local Russian material is maintained separately and is excluded from this site's build.
