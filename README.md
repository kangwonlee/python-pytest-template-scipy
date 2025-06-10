# python-pytest-template

Template for grader image builders for python assignments

## Purpose

* To provide a template for creating a grader image for python assignments
* To automate the programming assignment grading process so that educators can focus more on teaching

## Setup & Customization
1. Fork this repository.
1. Go to the `Settings` tab of your repository and click on `Actions` on the left sidebar.
    1. Click on `General` and go to `Workflow permissions`.
    1. Choose `Read and write permissions` and <kbd>Save</kbd>.
1. Edit `tests/test_syntax.py` to set allowed modules and functions.
1. Customize `tests/test_results.py` to define the expected results.
1. Push to GitHub : `build.yml` builds your image and pushes to GHCR (GitHub Container Repository).
* `script_path` fixture will be available if your test script in the `tests/` folder imports `pytest`.
* Currently `requirements.txt` is for documentation purpose.

## CI/CD Workflow

- `build.yml`: Builds and pushes a multi-arch grader image to GHCR.
- Uses GHCR for privacy and GitHub integration—swap to Docker Hub by updating `registry` and `tags` if preferred.
- Requires `Dockerfile` in repo root (see [Dockerfile docs](#)). Set `BUILDER_PAT` in secrets for optional dispatch.

## Dockerfile

- Builds a lightweight grader image with `pytest`.
- Installs dependencies from `requirements.txt`.
- Customize `CMD` to run your tests (e.g., `python3 -m pytest tests/`).

## Notes

- This template is registered as a part of #C-2025-016393 in the Korea Copyright Commission.
