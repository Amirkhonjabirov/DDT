import pytest


def pytest_addoption(parser):
    parser.addoption('--url', action='store', default='https://ya.ru/')
    parser.addoption('--status_code', action='store', default='200')


@pytest.fixture
def base_url(request) -> str:
    return request.config.getoption('--url')


@pytest.fixture
def status_code(request) -> int:
    return int(request.config.getoption('--status_code'))