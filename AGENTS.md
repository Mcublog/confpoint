# AGENTS.md

Confpoint is a Python package providing command-line tools for publishing
Markdown to Confluence and uploading/downloading files to/from SharePoint.
Keep documentation, code comments, CLI help and commit messages in English.
Follow the user's preferred language when communicating with them.

## Repository layout

- `src/confpoint/publisher/` — Confluence publisher; `push.py` contains the CLI
  and publication flow, `mermaid.py` implements local diagram rendering.
- `src/confpoint/uploader/` and `src/confpoint/downloader/` — SharePoint CLIs.
- `src/confpoint/utils.py` and `image_tag.py` — image discovery, Confluence
  attachment markup and shared helpers.
- `src/confpoint/shareup.py` — SharePoint integration.
- `src/confpoint/version.py` — package version; `setup.cfg` reads `VERSION`
  through `version = attr: confpoint.version.VERSION`.
- `setup.cfg` — package metadata, runtime dependencies and console entry points.
  `pyproject.toml` defines the setuptools build backend.
- `requirements.txt` — runtime dependencies and development/build tools.
- `test_dir/` — tests and manual test assets; `doc/` — documentation assets.

## Development and checks

- Use an available Python interpreter with the project dependencies installed,
  preferably in a virtual environment. Do not assume `python` exists; use
  `python3` or the virtual environment's interpreter as appropriate.
- Install for development with `python3 -m pip install -e .`.
- Run from source without reinstalling with `PYTHONPATH=src`, for example:
  `PYTHONPATH=src python3 -m confpoint.publisher --help`.
- Console entry points are `confpoint-publisher`, `confpoint-uploader` and
  `confpoint-downloader`; each also supports `python3 -m confpoint.<module>`.
- Run the isolated Mermaid tests without network access:
  `PYTHONPATH=src python3 -m unittest discover -s test_dir -p 'test_mermaid.py' -v`.
- Check whitespace with `git diff --check`. No repository-wide lint or type
  checking tool is configured; do not introduce one as an unrelated change.
- `setup.cfg` currently declares Python >=3.7, while existing code uses newer
  language features. Do not silently change the supported Python range or
  assume that the declared minimum has been verified.

## Build and release

- Build distributions with `python3 -m build`; output goes to `dist/`.
- Read `py2bin.ps1` / `py2exe.ps1` before using executable build workflows.
- `update_and_upload_test.sh` and `update_and_upload_test.ps1` upload artifacts
  to TestPyPI; they are publishing scripts, not local test commands.
- Build or upload artifacts only when requested. Never publish to PyPI,
  TestPyPI or another external registry as a side effect of validation.
- Bump `src/confpoint/version.py` and update `CHANGELOG.md` only when explicitly
  requested. Do not change unrelated dependency versions during a version bump.
- Do not commit virtual environments, `dist/`, `build/`, `bin/`, `*.spec`,
  bytecode, package metadata or generated diagram files.

## Publication and security

- Confluence and SharePoint operations modify remote content. Run live upload,
  update or delete checks only with explicit user authorization for the target.
  Prefer mocked tests for routine validation.
- Never commit or print API tokens, passwords or environment dumps. Pass
  credentials from the environment or another user-approved secret source.
- Markdown is the source of truth. Mermaid rendering must not modify the source
  document or require checked-in generated Markdown/images.
- Mermaid uses a local `mmdc` installation; documents without diagrams must not
  require Node.js or Chromium. Do not silently download tools or send diagram
  content to third-party rendering services.
- Keep Chromium sandbox enabled by default. `--mermaid-no-sandbox` is an
  explicit opt-in for trusted diagrams only. Preserve rendering timeouts.
- Keep temporary images available until attachment uploads finish, and clean
  them up on success and failure. Rendering errors must stop publication before
  remote page changes.
- Page updates and attachment uploads are not atomic. Do not claim transactional
  publication or automatically delete obsolete remote attachments.
- Existing image paths are resolved relative to the working directory, with
  leading `/` interpreted as repository-relative via `./`. Do not silently
  change these semantics while modifying Mermaid support.

## Coding and collaboration conventions

- Follow the surrounding code style and keep changes focused on the request.
- Place Python imports at module scope. Function-local imports should be an
  exceptional, justified choice agreed with the user beforehand.
- Preserve existing CLI options and non-Mermaid publication behavior.
- Agree on new tests and their scope with the user before adding or expanding
  them; running existing local tests is encouraged.
- Do not overwrite or discard unrelated user changes.
- The user makes commits and pushes. Do not commit, push, tag or create releases
  automatically; suggest a commit message when useful.

## Commit messages

- Write messages in English and describe the actual change concisely.
- History uses mixed styles: plain descriptions (`added printing link when push;`)
  and Conventional Commit-style messages (`feat: ...`, `fix(Onedownloader): ...`).
  Do not impose the component-prefix convention from `kkt_tools` on this project.
- Prefer `feat: <description>`, `fix: <description>`, `docs: <description>` or
  `test: <description>` for new messages. Add a component scope when helpful,
  for example `feat(publisher): render Mermaid diagrams as attachments`.
- Plain descriptive subjects remain acceptable for small maintenance changes,
  for example `Bump version to 1.3.0`.
- Emoji and a trailing semicolon appear in history but are not required.
  Avoid vague subjects such as `upd` or `update` without explaining what changed.
- Mention an issue key only when one is provided; do not invent Jira prefixes,
  branch names or release workflow requirements.
