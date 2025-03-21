import os
import pathlib

from typing import Tuple


import pytest


file_path = pathlib.Path(__file__)
test_folder = file_path.parent.absolute()
proj_folder = pathlib.Path(os.getenv('STUDENT_CODE_FOLDER', test_folder.parent.absolute()))


def py_files() -> Tuple[pathlib.Path]:
    return tuple(
        filter(
            lambda s:'sample.py' != s.name,
            proj_folder.glob('*.py')
        )
    )


def pytest_generate_tests(metafunc):
    if "py_file" in metafunc.fixturenames:
        metafunc.parametrize("py_file", py_files())
