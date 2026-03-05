"""Unit tests for Polperro coordinator."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

from custom_components.lexent_polpero.const import CONF_HOST, CONF_MAC, DOMAIN
from custom_components.lexent_polpero.coordinator import PolperoCoordinator


class TestPolperoCoordinator:
    """Tests for PolperoCoordinator."""

    def _make_entry(self) -> MagicMock:
        """Create a mock config entry."""
        entry = MagicMock()
        entry.data = {
            CONF_HOST: "192.168.2.8",
            CONF_MAC: "502cc626e9a5",
        }
        entry.unique_id = "502cc626e9a5"
        return entry

    def test_coordinator_creates_client(self) -> None:
        """Coordinator creates a PolperoClient with correct params."""
        hass = MagicMock()
        entry = self._make_entry()
        mock_cls = MagicMock()

        with patch(
            "custom_components.lexent_polpero.coordinator.PolperoClient",
            mock_cls,
        ):
            PolperoCoordinator(hass, entry)

        mock_cls.assert_called_once_with(
            host="192.168.2.8",
            mac="502cc626e9a5",
        )

    def test_coordinator_name_includes_unique_id(self) -> None:
        """Coordinator name contains the unique ID for logging."""
        hass = MagicMock()
        entry = self._make_entry()

        with patch(
            "custom_components.lexent_polpero.coordinator.PolperoClient",
            MagicMock(),
        ):
            coordinator = PolperoCoordinator(hass, entry)

        assert "502cc626e9a5" in coordinator.name

    def test_coordinator_starts_disconnected(self) -> None:
        """Coordinator starts in disconnected state."""
        hass = MagicMock()
        entry = self._make_entry()

        with patch(
            "custom_components.lexent_polpero.coordinator.PolperoClient",
            MagicMock(),
        ):
            coordinator = PolperoCoordinator(hass, entry)

        assert coordinator._connected is False

    def test_coordinator_falls_back_to_host_for_name(self) -> None:
        """When no unique_id, coordinator uses host in name."""
        hass = MagicMock()
        entry = self._make_entry()
        entry.unique_id = None

        with patch(
            "custom_components.lexent_polpero.coordinator.PolperoClient",
            MagicMock(),
        ):
            coordinator = PolperoCoordinator(hass, entry)

        assert "192.168.2.8" in coordinator.name
