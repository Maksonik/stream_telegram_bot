import pytest

from tests.constants import TESTSERVER_HOST


@pytest.fixture(scope='module')
def vcr_config():
    return {
        "filter_headers": [('authorization', 'DUMMY')],
        "ignore_hosts": [TESTSERVER_HOST],
        "record_on_exception": False,
    }