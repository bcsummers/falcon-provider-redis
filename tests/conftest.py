# -*- coding: utf-8 -*-
"""Testing conf module."""
# third-party
import pytest
from falcon import testing

from .app import app_hook, app_middleware


@pytest.fixture
def client_hook():
    """Create testing client fixture for hook app"""
    return testing.TestClient(app_hook)


@pytest.fixture
def client_middleware():
    """Create testing client fixture for middleware app"""
    return testing.TestClient(app_middleware)
