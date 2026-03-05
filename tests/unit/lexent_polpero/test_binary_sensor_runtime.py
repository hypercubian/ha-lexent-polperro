"""Unit tests for binary sensor platform runtime behaviour."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from custom_components.lexent_polpero.binary_sensor import (
    BINARY_SENSORS,
    PolperoBinarySensor,
    async_setup_entry,
)
from custom_components.lexent_polpero.const import CONF_HOST, CONF_MAC
from custom_components.lexent_polpero.coordinator import PolperoCoordinator
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


class TestBinarySensorIsOn:
    """Tests for PolperoBinarySensor.is_on."""

    def test_water_full_true(self) -> None:
        coordinator = _make_coordinator()
        coordinator.data = _make_device_state(water_full=True)
        desc = BINARY_SENSORS[0]
        entity = PolperoBinarySensor(coordinator, desc)
        assert entity.is_on is True

    def test_water_full_false(self) -> None:
        coordinator = _make_coordinator()
        coordinator.data = _make_device_state(water_full=False)
        desc = BINARY_SENSORS[0]
        entity = PolperoBinarySensor(coordinator, desc)
        assert entity.is_on is False

    def test_none_when_no_data(self) -> None:
        coordinator = _make_coordinator()
        coordinator.data = None
        desc = BINARY_SENSORS[0]
        entity = PolperoBinarySensor(coordinator, desc)
        assert entity.is_on is None


class TestBinarySensorSetupEntry:
    """Tests for binary_sensor async_setup_entry."""

    @pytest.mark.asyncio
    async def test_setup_adds_one_entity(self) -> None:
        coordinator = _make_coordinator()
        entry = MagicMock()
        entry.runtime_data = coordinator
        added: list = []

        await async_setup_entry(MagicMock(), entry, added.extend)

        assert len(added) == 1
        assert isinstance(added[0], PolperoBinarySensor)
