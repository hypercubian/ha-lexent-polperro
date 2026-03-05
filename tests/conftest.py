"""Shared test fixtures for Lexent Polperro integration tests."""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest
from polperro import (  # type: ignore[attr-defined]
    AirQuality,
    DeviceState,
    FanSpeed,
    Mode,
)


def _make_device_state(**overrides: object) -> DeviceState:
    """Create a DeviceState with sensible defaults."""
    defaults = {
        "power": True,
        "mode": Mode.DEHUMIDIFY,
        "target_humidity": 50,
        "fan_speed": FanSpeed.AUTO,
        "water_full": False,
        "light": True,
        "swing": False,
        "uvc_enabled": False,
        "quiet": False,
        "pm25": AirQuality.EXCELLENT,
        "air_quality": AirQuality.GOOD,
        "current_humidity": 65,
        "child_lock": False,
        "timer": 0,
        "error_code": 0,
        "filter_status": 0,
        "ioniser_enabled": False,
        "turbo": False,
        "temperature": 22,
        "temp_unit_fahrenheit": False,
    }
    defaults.update(overrides)
    return DeviceState(**defaults)


@pytest.fixture
def mock_device_state() -> DeviceState:
    """Return a default DeviceState for testing."""
    return _make_device_state()


@pytest.fixture
def mock_polperro_client(mock_device_state: DeviceState) -> AsyncMock:
    """Return a mocked PolperroClient."""
    client = AsyncMock()
    client.host = "192.168.2.8"
    client.mac = "502cc626e9a5"
    client.is_connected = True
    client.connect = AsyncMock()
    client.disconnect = AsyncMock()
    client.get_state = AsyncMock(return_value=mock_device_state)
    client.set_power = AsyncMock()
    client.set_mode = AsyncMock()
    client.set_target_humidity = AsyncMock()
    client.set_fan_speed = AsyncMock()
    client.set_uvc = AsyncMock()
    client.set_ioniser = AsyncMock()
    client.set_child_lock = AsyncMock()
    client.set_light = AsyncMock()
    client.set_swing = AsyncMock()
    client.set_quiet = AsyncMock()
    client.set_turbo = AsyncMock()
    return client
