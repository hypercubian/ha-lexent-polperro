"""Unit tests for the base PolperoEntity."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

from custom_components.lexent_polpero.const import CONF_HOST, CONF_MAC, DOMAIN
from custom_components.lexent_polpero.coordinator import PolperoCoordinator
from custom_components.lexent_polpero.entity import PolperoEntity


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


class TestPolperoEntity:
    """Tests for PolperoEntity base class."""

    def test_unique_id_combines_mac_and_key(self) -> None:
        """unique_id is MAC_key."""
        coordinator = _make_coordinator()
        entity = PolperoEntity(coordinator, "test_key")
        assert entity.unique_id == "502cc626e9a5_test_key"

    def test_has_entity_name(self) -> None:
        """Entity uses HA entity name pattern."""
        coordinator = _make_coordinator()
        entity = PolperoEntity(coordinator, "test_key")
        assert entity._attr_has_entity_name is True

    def test_device_info(self) -> None:
        """device_info returns correct identifiers and metadata."""
        coordinator = _make_coordinator()
        entity = PolperoEntity(coordinator, "test_key")

        info = entity.device_info
        assert (DOMAIN, "502cc626e9a5") in info["identifiers"]
        assert info["name"] == "Polperro (192.168.2.8)"
        assert info["manufacturer"] == "Lexent"
        assert info["model"] == "Polperro 30L"
