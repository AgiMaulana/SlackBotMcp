import pytest
import sys
sys.path.insert(0, ".")

from server import send_message


def test_send_message_returns_dict(mock_slack_api):
    result = send_message(channel_id="C123", message="Hello")
    assert isinstance(result, dict), f"Expected dict, got {type(result).__name__}"


def test_send_message_contains_expected_keys(mock_slack_api):
    result = send_message(channel_id="C123", message="Hello")
    assert "message_link" in result
    assert "ts" in result
    assert "channel" in result


def test_send_message_link_format(mock_slack_api):
    result = send_message(channel_id="C123", message="Hello")
    assert result["message_link"].startswith("https://slack.com/archives/")
    assert result["ts"] == "1234567890.123456"
    assert result["channel"] == "C123456"