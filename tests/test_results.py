# begin tests/test_results.py
import subprocess
import pathlib

from typing import Callable, Tuple


import pytest


Run = Callable[[str], Tuple[str]]


@pytest.fixture
def separator() -> str:
    return ('-'*10) + '\n'


@pytest.fixture
def run_script(script_path: pathlib.Path, separator: str) -> Run:
    def _run(input_data: str) -> Tuple[str]:
        result = subprocess.run(
            ['python', str(script_path)],
            input=input_data,
            text=True,
            capture_output=True,
            timeout=5  # Prevent infinite loops
        )
        if result.returncode != 0:
            raise RuntimeError(f"Script failed: {result.stderr}")
        return tuple(result.stdout.strip().split(separator)[-1].splitlines())
    return _run


# Sample test - educators should replace with their own logic
def test_sample_output(run_script: Run):
    input_data = "42"  # Example input
    output = run_script(input_data)
    expected = ("42",)  # Example expected output
    assert output == expected, f"Expected {expected}, got {output}"


if __name__ == "__main__":
    pytest.main(['--verbose', __file__])

# end tests/test_results.py
