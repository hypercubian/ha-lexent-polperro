"""Unit tests for sensor platform runtime behaviour."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from polpero import AirQuality  # type: ignore[attr-defined]

from custom_components.lexent_polpero.const import CONF_HOST, CONF_MAC
from custom_components.lexent_polpero.coordinator import PolperoCoordinator
from custom_components.lexent_polpero.sensor import SENSORS, PolperoSensor, async_setup_entry
from tests.conftest import _make_device_state


def _make_coordinator() -> PolperoCoordinator:
    hass = MagicMock()
    entry = MagicMock()
    entry.data = {CONF_HOST: "192.168.2.8", CONF_MAC: "502cc626e9a5"}
    entry.unique_id = "502cc626e9a5"
    entry.title = "Polperro (192.168.2.8)"

    mock_client = MagicMock()
    mock_client.mac = "502cc626e9a5"

    with patch(
        "custom_components.lexent_polpero.coordinator.PolperoClient",
        return_value=mock_client,
    ):
        return PolperoCoordinator(hass, entry)


def _get_desc(key: str):
    return next(d for d in SENSORS if d.key == key)


class TestSensorNativeValue:
    """Tests for PolperoSensor.native_value."""

    def test_string_value_fn_reads_attr(self) -> None:
        coordinator = _make_coordinator()
        coordinator.data = _make_device_state(current_humidity=68)
        entity = PolperoSensor(coordinator, _get_desc("current_humidity"))
        assert entity.native_value == 68

    def test_temperature_value(self) -> None:
        coordinator = _make_coordinator()
        coordinator.data = _make_device_state(temperature=25)
        entity = PolperoSensor(coordinator, _get_desc("temperature"))
        assert entity.native_value == 25

    def test_callable_value_fn_pm25(self) -> None:
        coordinator = _make_coordinator()
        coordinator.data = _make_device_state(pm25=AirQuality.GOOD)
        entity = PolperoSensor(coordinator, _get_desc("pm25_quality"))
        assert entity.native_value == "good"

    def test_callable_value_fn_air_quality(self) -> None:
        coordinator = _make_coordinator()
        coordinator.data = _make_device_state(air_quality=AirQuality.BAD)
        entity = PolperoSensor(coordinator, _get_desc("air_quality"))
        assert entity.native_value == "bad"

    def test_timer_value(self) -> None:
        coordinator = _make_coordinator()
        coordinator.data = _make_device_state(timer=4)
        entity = PolperoSensor(coordinator, _get_desc("timer"))
        assert entity.native_value == 4

    def test_error_code_value(self) -> None:
        coordinator = _make_coordinator()
        coordinator.data = _make_device_state(error_code=3)
        entity = PolperoSensor(coordinator, _get_desc("error_code"))
        assert entity.native_value == 3

    def test_filter_status_value(self) -> None:
        coordinator = _make_coordinator()
        coordinator.data = _make_device_state(filter_status=1)
        entity = PolperoSensor(coordinator, _get_desc("filter_status"))
        assert entity.native_value == 1

    def test_none_when_no_data(self) -> None:
        coordinator = _make_coordinator()
        coordinator.data = None
        entity = PolperoSensor(coordinator, _get_desc("current_humidity"))
        assert entity.native_value is None


class TestSensorSetupEntry:
    """Tests for sensor async_setup_entry."""

    @pytest.mark.asyncio
    async def test_setup_adds_seven_sensors(self) -> None:
        coordinator = _make_coordinator()
        entry = MagicMock()
        entry.runtime_data = coordinator
        added: list = []

        await async_setup_entry(MagicMock(), entry, added.extend)

        assert len(added) == 7
        assert all(isinstance(e, PolperoSensor) for e in added)
