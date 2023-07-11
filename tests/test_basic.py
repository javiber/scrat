import logging
import time

import pytest_mock

import elephant as el

logging.basicConfig(level=logging.INFO)


def test_one(mocker: pytest_mock.MockerFixture):
    counter = 0

    def f():
        nonlocal counter
        counter += 1
        return counter

    cached_func = el.remember()(f)

    assert cached_func() == 1
    assert cached_func() == 1
    assert counter == 1
