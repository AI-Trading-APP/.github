from __future__ import annotations

import importlib
import json
import logging

import pytest
import structlog

import ai_trading_common.logging_config as logging_config


@pytest.fixture(autouse=True)
def reset_logging_state(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("LOG_LEVEL", raising=False)
    monkeypatch.delenv("LOG_FORMAT", raising=False)

    root_logger = logging.getLogger()
    for handler in list(root_logger.handlers):
        root_logger.removeHandler(handler)
        handler.close()

    logging_config._CURRENT_SERVICE_NAME = None
    structlog.reset_defaults()

    yield

    root_logger = logging.getLogger()
    for handler in list(root_logger.handlers):
        root_logger.removeHandler(handler)
        handler.close()

    logging_config._CURRENT_SERVICE_NAME = None
    structlog.reset_defaults()


def _reload_module() -> object:
    return importlib.reload(logging_config)


def _setup_logger(
    monkeypatch: pytest.MonkeyPatch,
    *,
    log_level: str | None = None,
    log_format: str | None = None,
    service_name: str = "test-service",
):
    if log_level is not None:
        monkeypatch.setenv("LOG_LEVEL", log_level)
    if log_format is not None:
        monkeypatch.setenv("LOG_FORMAT", log_format)

    module = _reload_module()
    module.setup_logging(service_name)
    return module, module.get_logger()


def _read_single_log_line(capsys: pytest.CaptureFixture[str]) -> str:
    captured = capsys.readouterr()
    lines = [line for line in captured.err.splitlines() if line.strip()]
    assert lines, "Expected log output on stderr"
    return lines[-1]


def test_setup_logging_initializes_without_exception(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _reload_module()
    module.setup_logging("orders-service")

    assert module._CURRENT_SERVICE_NAME == "orders-service"
    assert logging.getLogger().handlers


def test_get_logger_returns_working_logger(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    _, logger = _setup_logger(monkeypatch, log_format="json", service_name="watchlist")

    logger.info("logger-ready", extra_field="ok")

    output = json.loads(_read_single_log_line(capsys))
    assert output["event"] == "logger-ready"
    assert output["extra_field"] == "ok"
    assert output["service_name"] == "watchlist"


def test_pii_masking_replaces_sensitive_values(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    _, logger = _setup_logger(monkeypatch, log_format="json", service_name="security")

    logger.info(
        "mask-me",
        password="mypassword",
        token="abc123",
        email="user@gmail.com",
    )

    output = json.loads(_read_single_log_line(capsys))
    assert output["password"] == "***"
    assert output["token"] == "***"
    assert output["email"] == "***"


def test_nested_pii_masking_masks_nested_dictionaries_and_lists(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    _, logger = _setup_logger(monkeypatch, log_format="json", service_name="profile")

    logger.info(
        "nested",
        user={"email": "user@gmail.com"},
        records=[{"ssn": "111-22-3333"}, {"details": {"cookie": "abc"}}],
    )

    output = json.loads(_read_single_log_line(capsys))
    assert output["user"]["email"] == "***"
    assert output["records"][0]["ssn"] == "***"
    assert output["records"][1]["details"]["cookie"] == "***"


def test_partial_key_matching_masks_access_token_reset_password_and_api_token(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    _, logger = _setup_logger(monkeypatch, log_format="json", service_name="auth")

    logger.info(
        "partial-match",
        access_token="abc123",
        reset_password="new-password",
        api_token="secret-token",
    )

    output = json.loads(_read_single_log_line(capsys))
    assert output["access_token"] == "***"
    assert output["reset_password"] == "***"
    assert output["api_token"] == "***"


def test_log_level_debug_emits_debug_logs(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    _, logger = _setup_logger(
        monkeypatch, log_level="DEBUG", log_format="json", service_name="debugger"
    )

    logger.debug("debug-event", payload="visible")

    output = json.loads(_read_single_log_line(capsys))
    assert output["event"] == "debug-event"
    assert output["payload"] == "visible"
    assert output["level"] == "debug"


def test_log_format_json_produces_json_output(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    _, logger = _setup_logger(monkeypatch, log_format="json", service_name="jsonsvc")

    logger.info("json-event", status="ok")

    output = json.loads(_read_single_log_line(capsys))
    assert output["event"] == "json-event"
    assert output["status"] == "ok"
    assert output["service_name"] == "jsonsvc"


def test_log_format_text_produces_console_output(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    _, logger = _setup_logger(monkeypatch, log_format="text", service_name="textsvc")

    logger.info("text-event", status="ok")

    output = _read_single_log_line(capsys)
    assert "text-event" in output
    assert "service_name='textsvc'" in output
    assert "status='ok'" in output
    assert not output.lstrip().startswith("{")


def test_invalid_environment_values_fall_back_to_safe_defaults(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    _, logger = _setup_logger(
        monkeypatch, log_level="TRACE", log_format="xml", service_name="fallback"
    )

    logger.info("fallback-event", details=("alpha", {"password": "secret"}))

    output = json.loads(_read_single_log_line(capsys))
    assert output["event"] == "fallback-event"
    assert output["details"][1]["password"] == "***"
    assert output["service_name"] == "fallback"
