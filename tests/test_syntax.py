import ast
import logging
import os
import pathlib

from typing import Tuple

import pytest


file_path = pathlib.Path(__file__)
test_folder = file_path.parent.absolute()
proj_folder = pathlib.Path(
    os.getenv(
        'STUDENT_CODE_FOLDER',
        test_folder.parent.absolute()
    )
)

logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)


def py_files() -> Tuple[pathlib.Path]:
    return tuple(proj_folder.glob("*.py"))


@pytest.mark.parametrize("py_file", py_files())
def test_syntax(py_file:pathlib.Path):

    code = py_file.read_text(encoding="utf-8")

    try:
        ast.parse(code)
    except SyntaxError as e:
        pytest.fail(f"Syntax error in file: {py_file.relative_to(proj_folder)}\n{e}")


@pytest.mark.parametrize("py_file", py_files())
def test_module(py_file:pathlib.Path):

    code = py_file.read_text(encoding="utf-8")

    tree = ast.parse(code)

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                logger.info(f"Import: {alias.name}")
                if "numpy" == alias.name:
                    pytest.fail(f"Import of numpy in {py_file.relative_to(proj_folder)}")
        elif isinstance(node, ast.ImportFrom):
            if node.module == "numpy":
                pytest.fail(f"Import of numpy in {py_file.relative_to(proj_folder)}")
