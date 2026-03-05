"""Unit tests for select platform runtime behaviour."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from polperro import FanSpeed  # type: ignore[attr-defined]

from custom_components.lexent_polperro.const import CONF_HOST, CONF_MAC
from custom_components.lexent_polperro.coordinator import PolperroCoordinator
from custom_components.lexent_polperro.select import SELECTS, PolperroSelect, async_setup_entry
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


class TestSelectCurrentOption:
    """Tests for PolperroSelect.current_option."""

    def test_auto(self) -> None:
        coordinator = _make_coordinator()
        coordinator.data = _make_device_state(fan_speed=FanSpeed.AUTO)
        entity = PolperroSelect(coordinator, SELECTS[0])
        assert entity.current_option == "auto"

    def test_low(self) -> None:
        coordinator = _make_coordinator()
        coordinator.data = _make_device_state(fan_speed=FanSpeed.LOW)
        entity = PolperroSelect(coordinator, SELECTS[0])
        assert entity.current_option == "low"

    def test_medium(self) -> None:
        coordinator = _make_coordinator()
        coordinator.data = _make_device_state(fan_speed=FanSpeed.MEDIUM)
        entity = PolperroSelect(coordinator, SELECTS[0])
        assert entity.current_option == "medium"

    def test_high(self) -> None:
        coordinator = _make_coordinator()
        coordinator.data = _make_device_state(fan_speed=FanSpeed.HIGH)
        entity = PolperroSelect(coordinator, SELECTS[0])
        assert entity.current_option == "high"

    def test_none_when_no_data(self) -> None:
        coordinator = _make_coordinator()
        coordinator.data = None
        entity = PolperroSelect(coordinator, SELECTS[0])
        assert entity.current_option is None

    def test_non_fanspeed_value_returns_str(self) -> None:
        """If value_fn returns a non-FanSpeed value, it's cast to str."""
        coordinator = _make_coordinator()
        coordinator.data = _make_device_state(fan_speed=99)
        entity = PolperroSelect(coordinator, SELECTS[0])
        assert entity.current_option == "99"


class TestSelectCommand:
    """Tests for PolperroSelect.async_select_option."""

    @pytest.mark.asyncio
    async def test_select_high(self) -> None:
        mock_client = AsyncMock()
        mock_client.mac = "502cc626e9a5"
        mock_client.set_fan_speed = AsyncMock()

        coordinator = _make_coordinator(mock_client)
        coordinator.async_request_refresh = AsyncMock()
        entity = PolperroSelect(coordinator, SELECTS[0])

        await entity.async_select_option("high")

        mock_client.set_fan_speed.assert_called_once_with(FanSpeed.HIGH)
        coordinator.async_request_refresh.assert_called_once()

    @pytest.mark.asyncio
    async def test_select_invalid_is_noop(self) -> None:
        mock_client = AsyncMock()
        mock_client.mac = "502cc626e9a5"
        mock_client.set_fan_speed = AsyncMock()

        coordinator = _make_coordinator(mock_client)
        coordinator.async_request_refresh = AsyncMock()
        entity = PolperroSelect(coordinator, SELECTS[0])

        await entity.async_select_option("turbo_max")

        mock_client.set_fan_speed.assert_not_called()
        coordinator.async_request_refresh.assert_not_called()


class TestSelectSetupEntry:
    """Tests for select async_setup_entry."""

    @pytest.mark.asyncio
    async def test_setup_adds_one_entity(self) -> None:
        coordinator = _make_coordinator()
        entry = MagicMock()
        entry.runtime_data = coordinator
        added: list = []

        await async_setup_entry(MagicMock(), entry, added.extend)

        assert len(added) == 1
        assert isinstance(added[0], PolperroSelect)
