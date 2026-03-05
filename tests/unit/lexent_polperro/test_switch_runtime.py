"""Unit tests for switch platform runtime behaviour."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from custom_components.lexent_polperro.const import CONF_HOST, CONF_MAC
from custom_components.lexent_polperro.coordinator import PolperroCoordinator
from custom_components.lexent_polperro.switch import (
    SWITCHES,
    PolperroSwitch,
    async_setup_entry,
)
from tests.conftest import _make_device_state


def _make_coordinator(
    mock_client: MagicMock | None = None,
) -> PolperroCoordinator:
    hass = MagicMock()
    entry = MagicMock()
    entry.data = {CONF_HOST: "192.168.2.8", CONF_MAC: "502cc626e9a5"}
    entry.unique_id = "502cc626e9a5"
    entry.title = "Polperro (192.168.2.8)"

    client = mock_client or MagicMock()
    client.mac = "502cc626e9a5"

    with patch(
        "custom_components.lexent_polperro.coordinator.PolperroClient",
        return_value=client,
    ):
        return PolperroCoordinator(hass, entry)


def _get_desc(key: str):
    return next(d for d in SWITCHES if d.key == key)


class TestSwitchIsOn:
    """Tests for PolperroSwitch.is_on."""

    def test_light_on(self) -> None:
        coordinator = _make_coordinator()
        coordinator.data = _make_device_state(light=True)
        entity = PolperroSwitch(coordinator, _get_desc("light"))
        assert entity.is_on is True

    def test_light_off(self) -> None:
        coordinator = _make_coordinator()
        coordinator.data = _make_device_state(light=False)
        entity = PolperroSwitch(coordinator, _get_desc("light"))
        assert entity.is_on is False

    def test_uvc_reads_uvc_enabled(self) -> None:
        coordinator = _make_coordinator()
        coordinator.data = _make_device_state(uvc_enabled=True)
        entity = PolperroSwitch(coordinator, _get_desc("uvc"))
        assert entity.is_on is True

    def test_ioniser_reads_ioniser_enabled(self) -> None:
        coordinator = _make_coordinator()
        coordinator.data = _make_device_state(ioniser_enabled=True)
        entity = PolperroSwitch(coordinator, _get_desc("ioniser"))
        assert entity.is_on is True

    def test_none_when_no_data(self) -> None:
        coordinator = _make_coordinator()
        coordinator.data = None
        entity = PolperroSwitch(coordinator, _get_desc("light"))
        assert entity.is_on is None


class TestSwitchCommands:
    """Tests for switch turn_on/turn_off."""

    @pytest.mark.asyncio
    async def test_turn_on_calls_set_fn_true(self) -> None:
        mock_client = AsyncMock()
        mock_client.mac = "502cc626e9a5"
        mock_client.set_light = AsyncMock()

        coordinator = _make_coordinator(mock_client)
        coordinator.async_request_refresh = AsyncMock()
        entity = PolperroSwitch(coordinator, _get_desc("light"))

        await entity.async_turn_on()

        mock_client.set_light.assert_called_once_with(True)
        coordinator.async_request_refresh.assert_called_once()

    @pytest.mark.asyncio
    async def test_turn_off_calls_set_fn_false(self) -> None:
        mock_client = AsyncMock()
        mock_client.mac = "502cc626e9a5"
        mock_client.set_swing = AsyncMock()

        coordinator = _make_coordinator(mock_client)
        coordinator.async_request_refresh = AsyncMock()
        entity = PolperroSwitch(coordinator, _get_desc("swing"))

        await entity.async_turn_off()

        mock_client.set_swing.assert_called_once_with(False)
        coordinator.async_request_refresh.assert_called_once()

    @pytest.mark.asyncio
    async def test_turn_on_quiet(self) -> None:
        mock_client = AsyncMock()
        mock_client.mac = "502cc626e9a5"
        mock_client.set_quiet = AsyncMock()

        coordinator = _make_coordinator(mock_client)
        coordinator.async_request_refresh = AsyncMock()
        entity = PolperroSwitch(coordinator, _get_desc("quiet"))

        await entity.async_turn_on()

        mock_client.set_quiet.assert_called_once_with(True)

    @pytest.mark.asyncio
    async def test_turn_on_turbo(self) -> None:
        mock_client = AsyncMock()
        mock_client.mac = "502cc626e9a5"
        mock_client.set_turbo = AsyncMock()

        coordinator = _make_coordinator(mock_client)
        coordinator.async_request_refresh = AsyncMock()
        entity = PolperroSwitch(coordinator, _get_desc("turbo"))

        await entity.async_turn_on()

        mock_client.set_turbo.assert_called_once_with(True)


class TestSwitchSetupEntry:
    """Tests for switch async_setup_entry."""

    @pytest.mark.asyncio
    async def test_setup_adds_seven_switches(self) -> None:
        coordinator = _make_coordinator()
        entry = MagicMock()
        entry.runtime_data = coordinator
        added: list = []

        await async_setup_entry(MagicMock(), entry, added.extend)

        assert len(added) == 7
        assert all(isinstance(e, PolperroSwitch) for e in added)
