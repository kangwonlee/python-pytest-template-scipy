# python-pytest-template
Template for grader image builders for python assignments

## Purpose

* To provide a template for creating a grader image for python assignments
* To automate the programming assignment grading process so that educators can focus more on teaching

## Setup & Customization
1. Fork this repository.
1. Edit `tests/test_syntax.py` to define the allowed modules and functions
1. Customize `tests/test_results.py` to define the expected results
1. Push to GitHub : `build.yml` builds your image and pushes to GHCR.
* `script_path` fixture will be available if your test script in the `tests/` folder imports `pytest`.
* Customize `requirements.txt` to include additional dependencies or change the test command.

## CI/CD Workflow

- `build.yml`: Builds and pushes a multi-arch grader image to GHCR.
- Uses GHCR for privacy and GitHub integration—swap to Docker Hub by updating `registry` and `tags` if preferred.
- Requires `Dockerfile` in repo root (see [Dockerfile docs](#)). Set `BUILDER_PAT` in secrets for optional dispatch.

## Dockerfile

- Builds a lightweight grader image with `pytest`.
- Installs dependencies from `requirements.txt`.
- Optional: Uncomment lines to include `gemini-python-tutor` (public repo) for LLM-generated test feedback—see [github.com/kangwonlee/gemini-python-tutor](https://github.com/kangwonlee/gemini-python-tutor).
- Customize `CMD` to run your tests (e.g., `python3 -m pytest tests/`).

## Notes

- A non-docker version would be available soon.
