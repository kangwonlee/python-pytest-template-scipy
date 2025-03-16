import os
import pathlib
import random
import sys

from typing import List, Tuple


import numpy as np
import numpy.random as nr
import pandas as pd
import pytest


file_path = pathlib.Path(__file__)
test_folder = file_path.parent.absolute()
proj_folder = pathlib.Path(
    os.getenv(
        'STUDENT_CODE_FOLDER',
        test_folder.parent.absolute()
    )
)


sys.path.insert(
    0,
    str(proj_folder)
)


import exercise


random.seed()


@pytest.fixture
def n() -> int:
    return random.randint(5, 8)


@pytest.fixture
def a() -> float:
    return (random.random() - 0.5) * 4


@pytest.fixture
def expected(n) -> np.ndarray:
    return (nr.randint(-32, 31, (n,)) * 1.0)


@pytest.fixture
def x(expected:np.ndarray, a:float) -> Tuple[float]:
    return tuple((expected / a).tolist())


@pytest.fixture
def result(a:float, x:Tuple[float]) -> List[float]:
    return exercise.mul_list_num(a, x)


def test_is_return_none(result:List[int]):
    assert result is not None, f"return value is None"


def test_return_value_size(result:List[int], n:int):
    assert (len(result) == n), f"return value size={len(result)}, expected size = {n}"


def test_isclose(result:List[int], a:Tuple[int], x:Tuple[int], expected:int):
    df = pd.DataFrame(
        data={'result': result, 'expected': expected},
        columns=['result', 'expected']
    )
    df['is close'] = np.isclose(df['result'], df['expected'])

    assert all(df['is close']), (
        f"Some elements in the result are not close enough to the expected values when a={a} and x={x}:\n"
        f"결과의 요소 중 a={a} x={x} 인 경우는 예상 값과 충분히 가깝지 않음.\n\n"
        f"{df[~df['is close']].to_markdown(numalign='left', stralign='left', index=False)}\n\n"
        "Please double-check your calculations for these elements.\n"
        "이 요소들에 대한 계산을 다시 확인하기 바랍니다.\n"
    )
