"""Unit tests for __init__.py (setup/unload entry)."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.exceptions import ConfigEntryNotReady

from custom_components.lexent_polpero import async_setup_entry, async_unload_entry
from custom_components.lexent_polpero.const import CONF_HOST, CONF_MAC, PLATFORMS


def _make_entry() -> MagicMock:
    entry = MagicMock()
    entry.data = {CONF_HOST: "192.168.2.8", CONF_MAC: "502cc626e9a5"}
    entry.unique_id = "502cc626e9a5"
    entry.runtime_data = None
    return entry


class TestAsyncSetupEntry:
    """Tests for async_setup_entry."""

    @pytest.mark.asyncio
    async def test_setup_entry_success(self) -> None:
        """Successful setup creates coordinator and forwards platforms."""
        hass = MagicMock()
        hass.config_entries = MagicMock()
        hass.config_entries.async_forward_entry_setups = AsyncMock()
        entry = _make_entry()

        mock_coordinator = MagicMock()
        mock_coordinator.async_config_entry_first_refresh = AsyncMock()
        mock_coordinator.async_shutdown = AsyncMock()

        with patch(
            "custom_components.lexent_polpero.PolperoCoordinator",
            return_value=mock_coordinator,
        ):
            result = await async_setup_entry(hass, entry)

        assert result is True
        mock_coordinator.async_config_entry_first_refresh.assert_called_once()
        assert entry.runtime_data is mock_coordinator
        hass.config_entries.async_forward_entry_setups.assert_called_once_with(
            entry, PLATFORMS
        )

    @pytest.mark.asyncio
    async def test_setup_entry_first_refresh_fails(self) -> None:
        """When first refresh fails, shutdown coordinator and raise ConfigEntryNotReady."""
        hass = MagicMock()
        entry = _make_entry()

        mock_coordinator = MagicMock()
        mock_coordinator.async_config_entry_first_refresh = AsyncMock(
            side_effect=Exception("connection timeout")
        )
        mock_coordinator.async_shutdown = AsyncMock()

        with (
            patch(
                "custom_components.lexent_polpero.PolperoCoordinator",
                return_value=mock_coordinator,
            ),
            pytest.raises(ConfigEntryNotReady, match="Unable to connect"),
        ):
            await async_setup_entry(hass, entry)

        mock_coordinator.async_shutdown.assert_called_once()


class TestAsyncUnloadEntry:
    """Tests for async_unload_entry."""

    @pytest.mark.asyncio
    async def test_unload_entry_success(self) -> None:
        """Successful unload disconnects coordinator."""
        hass = MagicMock()
        hass.config_entries = MagicMock()
        hass.config_entries.async_unload_platforms = AsyncMock(return_value=True)

        mock_coordinator = MagicMock()
        mock_coordinator.async_shutdown = AsyncMock()

        entry = _make_entry()
        entry.runtime_data = mock_coordinator

        result = await async_unload_entry(hass, entry)

        assert result is True
        mock_coordinator.async_shutdown.assert_called_once()

    @pytest.mark.asyncio
    async def test_unload_entry_failure_skips_shutdown(self) -> None:
        """When platform unload fails, skip coordinator shutdown."""
        hass = MagicMock()
        hass.config_entries = MagicMock()
        hass.config_entries.async_unload_platforms = AsyncMock(return_value=False)

        mock_coordinator = MagicMock()
        mock_coordinator.async_shutdown = AsyncMock()

        entry = _make_entry()
        entry.runtime_data = mock_coordinator

        result = await async_unload_entry(hass, entry)

        assert result is False
        mock_coordinator.async_shutdown.assert_not_called()
