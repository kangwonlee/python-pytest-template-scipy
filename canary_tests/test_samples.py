import pathlib
import shutil
import subprocess
import sys

import pytest


canary_tests_folder = pathlib.Path(__file__).parent.resolve()
proj_folder = canary_tests_folder.parent.resolve()
tests_folder = proj_folder / 'tests'


def discover_samples():
    """Auto-discover sample scripts under sample*/ folders.

    Scripts whose stem ends with '-pass' are expected to pass.
    Scripts whose stem ends with '-fail' are expected to fail.
    """
    for sample_dir in sorted(canary_tests_folder.glob('sample*')):
        if not sample_dir.is_dir():
            continue
        for script in sorted(sample_dir.glob('*.py')):
            if script.name.startswith('test_') or script.name == '__init__.py':
                continue
            stem = script.stem
            if stem.endswith('-pass'):
                expect_pass = True
            elif stem.endswith('-fail'):
                expect_pass = False
            else:
                continue
            yield pytest.param(script, expect_pass, id=f"{sample_dir.name}/{script.name}")


def run_grader(script_path, tmp_path):
    """Copy all sample files to tmp_path, rename script to exercise.py, and run grader tests."""
    sample_dir = script_path.parent
    for f in sample_dir.iterdir():
        if f == script_path:
            shutil.copy2(f, tmp_path / 'exercise.py')
        elif f.is_file():
            shutil.copy2(f, tmp_path / f.name)

    return subprocess.run(
        [sys.executable, '-m', 'pytest', str(tests_folder), '-v',
         '-k', 'not git_log and not window_capture'],
        env={
            'PATH': subprocess.os.environ.get('PATH', ''),
            'STUDENT_CODE_FOLDER': str(tmp_path),
        },
        capture_output=True,
        text=True,
        timeout=30,
    )


@pytest.mark.parametrize('script_path,expect_pass', discover_samples())
def test_sample(script_path, expect_pass, tmp_path):
    """Run grader tests against a sample submission."""
    result = run_grader(script_path, tmp_path)

    if expect_pass:
        assert result.returncode == 0, (
            f"{script_path.name} should pass all tests.\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )
    else:
        assert result.returncode != 0, (
            f"{script_path.name} should fail at least one test.\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )
