import ast
import functools
import os
import pathlib
import sys


from typing import Tuple


import pytest


file_path = pathlib.Path(__file__)
test_folder = file_path.parent.resolve()
proj_folder = test_folder.parent.resolve()


student_code_folder = pathlib.Path(os.getenv('STUDENT_CODE_FOLDER', proj_folder))
sys.path.insert(0, str(student_code_folder))


@functools.lru_cache()
def read_code(file_path:pathlib.Path) -> str:
    assert file_path.exists()
    assert file_path.is_file()
    return file_path.read_text(encoding="utf-8")


@functools.lru_cache()
def parse_code(file_path:pathlib.Path) -> ast.AST:
    try:
        tree = ast.parse(read_code(file_path))
    except SyntaxError as e:
        pytest.fail(f"Syntax error in file: {file_path.relative_to(proj_folder)}\n{e}")
    return tree


def test_syntax_validity(script_path:pathlib.Path):
    parse_code(script_path)


@pytest.fixture(scope="session")  # Session scope to share the allowed modules across tests
def allowed_modules() -> Tuple[str]:
    return tuple()


def test_allowed_imports(script_path:pathlib.Path, allowed_modules:Tuple[str]):
    for node in ast.walk(parse_code(script_path)):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            module_name = node.module if isinstance(node, ast.ImportFrom) else node.names[0].name
            if module_name not in allowed_modules:
                pytest.fail(
                    f"Import of disallowed module '{module_name}' in {script_path}\n"
                    f"{script_path.relative_to(proj_folder)} 파일에서 '{module_name}' 모듈을 import 않기 바랍니다."
                )


ALLOWED_FUNCTIONS = {'map', 'list',}

class FunctionChecker(ast.NodeVisitor):
    def __init__(self):
        self.disallowed = []

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id not in ALLOWED_FUNCTIONS:
            self.disallowed.append((node.func.id, node.lineno))
        self.generic_visit(node)


def test_allowed_functions(script_path:pathlib.Path):
    checker = FunctionChecker()
    checker.visit(parse_code(script_path))
    if checker.disallowed:
        pytest.fail(
            f"The {script_path} code calls function(s) {checker.disallowed} "
            f"but allowed functions are {ALLOWED_FUNCTIONS}\n"
        )


if __name__ == "__main__":
    pytest.main([__file__])
