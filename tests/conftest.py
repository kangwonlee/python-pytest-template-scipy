# begin conftest.py

import os
import pathlib

import pytest


@pytest.fixture
def file_path() -> pathlib.Path:
    p = pathlib.Path(__file__)
    assert p.exists()
    assert p.is_file()
    return p


@pytest.fixture
def my_test_folder(file_path:pathlib.Path) -> pathlib.Path:
    p = file_path.parent.resolve()
    assert p.exists()
    assert p.is_dir()
    return p


@pytest.fixture
def proj_folder(my_test_folder:pathlib.Path) -> pathlib.Path:
    p = pathlib.Path(
        os.getenv(
            'STUDENT_CODE_FOLDER',
            my_test_folder.parent.resolve()
        )
    )
    assert p.exists()
    assert p.is_dir()
    return p


@pytest.fixture
def script_path(proj_folder:pathlib.Path) -> pathlib.Path:
    '''
    Automatically discover ex??.py file
    Force only one ex??.py file in the project folder at the moment
    '''
    exercise_files = tuple(proj_folder.glob('ex*.py'))

    result = None
    if len(exercise_files) == 0:
        raise FileNotFoundError("No Python file starting with 'ex' found in the project folder.")
    elif len(exercise_files) > 1:
        raise ValueError("Multiple Python files starting with 'ex' found in the project folder. Please ensure there is only one.")
    else:
        result = exercise_files[0]

    return result

# end conftest.py
