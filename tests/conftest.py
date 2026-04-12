import pytest
from unittest.mock import patch, MagicMock


@pytest.fixture
def mock_slack_api(monkeypatch):
    def mock_api(method: str, payload: dict) -> dict:
        return {"ok": True, "ts": "1234567890.123456", "channel": "C123456"}

    def mock_get(method: str, params: dict) -> dict:
        return {"ok": True, "messages": []}

    monkeypatch.setattr("server._slack_api", mock_api)
    monkeypatch.setattr("server._slack_get", mock_get)