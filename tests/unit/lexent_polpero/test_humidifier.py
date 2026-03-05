"""Unit tests for the humidifier platform."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from polpero import FanSpeed, Mode  # type: ignore[attr-defined]

from custom_components.lexent_polpero.const import CONF_HOST, CONF_MAC
from custom_components.lexent_polpero.coordinator import PolperoCoordinator
from custom_components.lexent_polpero.humidifier import (
    MODE_MAP,
    MODE_REVERSE,
    PolperoHumidifier,
    async_setup_entry,
)
from tests.conftest import _make_device_state


def _make_coordinator(
    mock_client: MagicMock | None = None,
) -> PolperoCoordinator:
    hass = MagicMock()
    entry = MagicMock()
    entry.data = {CONF_HOST: "192.168.2.8", CONF_MAC: "502cc626e9a5"}
    entry.unique_id = "502cc626e9a5"
    entry.title = "Polperro (192.168.2.8)"

    client = mock_client or MagicMock()
    client.mac = "502cc626e9a5"

    with patch(
        "custom_components.lexent_polpero.coordinator.PolperoClient",
        return_value=client,
    ):
        return PolperoCoordinator(hass, entry)


class TestModeMapping:
    """Tests for mode mapping dicts."""

    def test_mode_map_has_three_modes(self) -> None:
        assert set(MODE_MAP.keys()) == {"dehumidify", "laundry", "purify"}

    def test_mode_reverse_is_inverse(self) -> None:
        for name, enum_val in MODE_MAP.items():
            assert MODE_REVERSE[enum_val] == name


class TestPolperoHumidifierProperties:
    """Tests for humidifier entity properties."""

    def test_is_on_true(self) -> None:
        coordinator = _make_coordinator()
        coordinator.data = _make_device_state(power=True)
        entity = PolperoHumidifier(coordinator)
        assert entity.is_on is True

    def test_is_on_false(self) -> None:
        coordinator = _make_coordinator()
        coordinator.data = _make_device_state(power=False)
        entity = PolperoHumidifier(coordinator)
        assert entity.is_on is False

    def test_is_on_none_when_no_data(self) -> None:
        coordinator = _make_coordinator()
        coordinator.data = None
        entity = PolperoHumidifier(coordinator)
        assert entity.is_on is None

    def test_mode_dehumidify(self) -> None:
        coordinator = _make_coordinator()
        coordinator.data = _make_device_state(mode=Mode.DEHUMIDIFY)
        entity = PolperoHumidifier(coordinator)
        assert entity.mode == "dehumidify"

    def test_mode_laundry(self) -> None:
        coordinator = _make_coordinator()
        coordinator.data = _make_device_state(mode=Mode.LAUNDRY)
        entity = PolperoHumidifier(coordinator)
        assert entity.mode == "laundry"

    def test_mode_purify(self) -> None:
        coordinator = _make_coordinator()
        coordinator.data = _make_device_state(mode=Mode.PURIFY)
        entity = PolperoHumidifier(coordinator)
        assert entity.mode == "purify"

    def test_mode_none_when_no_data(self) -> None:
        coordinator = _make_coordinator()
        coordinator.data = None
        entity = PolperoHumidifier(coordinator)
        assert entity.mode is None

    def test_target_humidity(self) -> None:
        coordinator = _make_coordinator()
        coordinator.data = _make_device_state(target_humidity=55)
        entity = PolperoHumidifier(coordinator)
        assert entity.target_humidity == 55

    def test_target_humidity_none_when_no_data(self) -> None:
        coordinator = _make_coordinator()
        coordinator.data = None
        entity = PolperoHumidifier(coordinator)
        assert entity.target_humidity is None

    def test_current_humidity(self) -> None:
        coordinator = _make_coordinator()
        coordinator.data = _make_device_state(current_humidity=72)
        entity = PolperoHumidifier(coordinator)
        assert entity.current_humidity == 72

    def test_current_humidity_none_when_no_data(self) -> None:
        coordinator = _make_coordinator()
        coordinator.data = None
        entity = PolperoHumidifier(coordinator)
        assert entity.current_humidity is None


class TestPolperoHumidifierCommands:
    """Tests for humidifier entity async commands."""

    @pytest.mark.asyncio
    async def test_turn_on(self) -> None:
        mock_client = AsyncMock()
        mock_client.mac = "502cc626e9a5"
        mock_client.set_power = AsyncMock()

        coordinator = _make_coordinator(mock_client)
        coordinator.async_request_refresh = AsyncMock()
        entity = PolperoHumidifier(coordinator)

        await entity.async_turn_on()

        mock_client.set_power.assert_called_once_with(True)
        coordinator.async_request_refresh.assert_called_once()

    @pytest.mark.asyncio
    async def test_turn_off(self) -> None:
        mock_client = AsyncMock()
        mock_client.mac = "502cc626e9a5"
        mock_client.set_power = AsyncMock()

        coordinator = _make_coordinator(mock_client)
        coordinator.async_request_refresh = AsyncMock()
        entity = PolperoHumidifier(coordinator)

        await entity.async_turn_off()

        mock_client.set_power.assert_called_once_with(False)
        coordinator.async_request_refresh.assert_called_once()

    @pytest.mark.asyncio
    async def test_set_humidity_rounds_to_nearest_5(self) -> None:
        mock_client = AsyncMock()
        mock_client.mac = "502cc626e9a5"
        mock_client.set_target_humidity = AsyncMock()

        coordinator = _make_coordinator(mock_client)
        coordinator.async_request_refresh = AsyncMock()
        entity = PolperoHumidifier(coordinator)

        await entity.async_set_humidity(53)
        mock_client.set_target_humidity.assert_called_with(55)

    @pytest.mark.asyncio
    async def test_set_humidity_rounds_down(self) -> None:
        mock_client = AsyncMock()
        mock_client.mac = "502cc626e9a5"
        mock_client.set_target_humidity = AsyncMock()

        coordinator = _make_coordinator(mock_client)
        coordinator.async_request_refresh = AsyncMock()
        entity = PolperoHumidifier(coordinator)

        await entity.async_set_humidity(52)
        mock_client.set_target_humidity.assert_called_with(50)

    @pytest.mark.asyncio
    async def test_set_humidity_clamps_min(self) -> None:
        mock_client = AsyncMock()
        mock_client.mac = "502cc626e9a5"
        mock_client.set_target_humidity = AsyncMock()

        coordinator = _make_coordinator(mock_client)
        coordinator.async_request_refresh = AsyncMock()
        entity = PolperoHumidifier(coordinator)

        await entity.async_set_humidity(10)
        mock_client.set_target_humidity.assert_called_with(30)

    @pytest.mark.asyncio
    async def test_set_humidity_clamps_max(self) -> None:
        mock_client = AsyncMock()
        mock_client.mac = "502cc626e9a5"
        mock_client.set_target_humidity = AsyncMock()

        coordinator = _make_coordinator(mock_client)
        coordinator.async_request_refresh = AsyncMock()
        entity = PolperoHumidifier(coordinator)

        await entity.async_set_humidity(99)
        mock_client.set_target_humidity.assert_called_with(80)

    @pytest.mark.asyncio
    async def test_set_mode(self) -> None:
        mock_client = AsyncMock()
        mock_client.mac = "502cc626e9a5"
        mock_client.set_mode = AsyncMock()

        coordinator = _make_coordinator(mock_client)
        coordinator.async_request_refresh = AsyncMock()
        entity = PolperoHumidifier(coordinator)

        await entity.async_set_mode("laundry")

        mock_client.set_mode.assert_called_once_with(Mode.LAUNDRY)
        coordinator.async_request_refresh.assert_called_once()

    @pytest.mark.asyncio
    async def test_set_mode_invalid_is_noop(self) -> None:
        mock_client = AsyncMock()
        mock_client.mac = "502cc626e9a5"
        mock_client.set_mode = AsyncMock()

        coordinator = _make_coordinator(mock_client)
        coordinator.async_request_refresh = AsyncMock()
        entity = PolperoHumidifier(coordinator)

        await entity.async_set_mode("nonexistent")

        mock_client.set_mode.assert_not_called()
        coordinator.async_request_refresh.assert_not_called()


class TestAsyncSetupEntry:
    """Tests for humidifier async_setup_entry."""

    @pytest.mark.asyncio
    async def test_setup_adds_one_entity(self) -> None:
        coordinator = _make_coordinator()
        entry = MagicMock()
        entry.runtime_data = coordinator
        added: list = []

        await async_setup_entry(MagicMock(), entry, added.extend)

        assert len(added) == 1
        assert isinstance(added[0], PolperoHumidifier)
