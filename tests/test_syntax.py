# begin tests/test_syntax.py
import ast
import functools
import pathlib
from typing import Tuple

import pytest


@functools.lru_cache()
def read_code(script_path:pathlib.Path) -> str:
    return script_path.read_text(encoding="utf-8")


@functools.lru_cache()
def parse_code(script_path:pathlib.Path, proj_folder:pathlib.Path) -> ast.AST:
    try:
        tree = ast.parse(read_code(script_path))
    except SyntaxError as e:
        pytest.fail(f"Syntax error in file: {script_path.relative_to(proj_folder)}\n{e}")
    return tree


def test_syntax_validity(script_path:pathlib.Path, proj_folder:pathlib.Path):
    parse_code(script_path, proj_folder)


@pytest.fixture(scope="session")  # Session scope to share the allowed modules across tests
def allowed_modules() -> Tuple[str]:
    return tuple()


def test_allowed_imports(script_path:pathlib.Path, proj_folder:pathlib.Path, allowed_modules:Tuple[str]):
    for node in ast.walk(parse_code(script_path, proj_folder)):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            module_name = node.module if isinstance(node, ast.ImportFrom) else node.names[0].name
            if module_name not in allowed_modules:
                pytest.fail(
                    f"Import of disallowed module '{module_name}' in {str(script_path.relative_to(proj_folder))}\n"
                    f"{str(script_path.relative_to(proj_folder))} 파일에서 '{module_name}' 모듈을 import 않기 바랍니다."
                )


ALLOWED_FUNCTIONS = {'print', 'input', 'int',}


class FunctionChecker(ast.NodeVisitor):
    def __init__(self):
        self.disallowed = []

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id not in ALLOWED_FUNCTIONS:
            self.disallowed.append((node.func.id, node.lineno))
        self.generic_visit(node)


def test_allowed_functions(script_path:pathlib.Path, proj_folder:pathlib.Path):
    checker = FunctionChecker()
    checker.visit(parse_code(script_path, proj_folder))
    if checker.disallowed:
        pytest.fail(
            f"The {str(script_path.relative_to(proj_folder))} code calls function(s) {checker.disallowed} "
            f"but allowed functions are {ALLOWED_FUNCTIONS}\n"
            f"{str(script_path.relative_to(proj_folder))} 파일에서 허용되지 않은 함수 {checker.disallowed}를 사용했습니다. "
            f"허용된 함수: {ALLOWED_FUNCTIONS}"
        )


class ControlStatementChecker(ast.NodeVisitor):
    def __init__(self):
        self.for_loops = []
        self.if_statements = []
        self.while_loops = []

        self.lookup = {
            'for': self.for_loops,
            'if': self.if_statements,
            'while': self.while_loops,
        }

    def visit_For(self, node):
        self.for_loops.append(node.lineno)
        self.generic_visit(node)

    def visit_If(self, node):
        self.if_statements.append(node.lineno)
        self.generic_visit(node)

    def visit_While(self, node):
        self.while_loops.append(node.lineno)
        self.generic_visit(node)

    def found(self, keyword:str) -> Tuple[int]:
        return tuple(self.lookup[keyword])


@pytest.fixture
def control_checker(
    script_path: pathlib.Path,
    proj_folder: pathlib.Path
) -> ControlStatementChecker:
    checker = ControlStatementChecker()
    checker.visit(parse_code(script_path, proj_folder))
    return checker


@pytest.mark.parametrize(
    "keyword_not_allowed",
    (
        "for",
        "if",
        "while",
    ),
)
def test_control_statements(control_checker:ControlStatementChecker, script_path: pathlib.Path, proj_folder: pathlib.Path, keyword_not_allowed: str):
    lines = control_checker.found(keyword_not_allowed)
    if lines:
        pytest.fail(
            f"'{keyword_not_allowed}' keyword detected in {str(script_path.relative_to(proj_folder))} at lines {lines}.\n"
            f"Please refrain from using '{keyword_not_allowed}' in this assignment."
        )


if __name__ == "__main__":
    pytest.main(['--verbose', __file__])

# end tests/test_syntax.py
