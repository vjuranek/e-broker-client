import os

import pytest

from ebroker.Config import Config


@pytest.fixture
def config():
    config = Config(os.path.join(os.path.dirname(__file__), "resources/main.conf"))
    return config


def test_credentials(config):
    credentials = config.credentials()
    assert credentials.login == "test_login"
    assert credentials.password == "test_password"


def test_db_config(config):
    db_conf = config.sqlite_options()
    assert db_conf.db_file == "test_location"
