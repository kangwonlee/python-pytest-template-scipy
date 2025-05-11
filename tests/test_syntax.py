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
    return ('numpy', 'pandas', 'matplotlib', 'scipy')


def test_allowed_imports(script_path:pathlib.Path, proj_folder:pathlib.Path, allowed_modules:Tuple[str]):
    for node in ast.walk(parse_code(script_path, proj_folder)):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            module_name = node.module if isinstance(node, ast.ImportFrom) else node.names[0].name
            if not is_module_allowed(allowed_modules, module_name):
                pytest.fail(
                    f"Import of disallowed module '{module_name}' in {str(script_path.relative_to(proj_folder))}\n"
                    f"{str(script_path.relative_to(proj_folder))} 파일에서 '{module_name}' 모듈을 import 않기 바랍니다."
                )


def is_module_allowed(allowed_modules:Tuple[str], module_name:str) -> bool:
    """
    Check if the module is allowed based on the allowed modules list.

    If 'scipy' is allowed, 'scipy.stats' is also allowed.
    """
    if '.' in module_name:
        # Check if the module is a submodule of an allowed module
        base_module_name = module_name.split('.')[0]
        b_allowed = base_module_name in allowed_modules
    else:
        b_allowed = module_name in allowed_modules

    return b_allowed


if __name__ == "__main__":
    pytest.main(['--verbose', __file__])

# end tests/test_syntax.py
