"""Lexent Polperro integration for Home Assistant."""

from __future__ import annotations

from typing import TypeAlias

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import PLATFORMS
from .coordinator import PolperroCoordinator

PolperroConfigEntry: TypeAlias = ConfigEntry[PolperroCoordinator]


async def async_setup_entry(hass: HomeAssistant, entry: PolperroConfigEntry) -> bool:
    """Set up Lexent Polperro from a config entry."""
    coordinator = PolperroCoordinator(hass, entry)
    try:
        await coordinator.async_config_entry_first_refresh()
    except Exception as err:
        await coordinator.async_shutdown()
        raise ConfigEntryNotReady(
            f"Unable to connect to Polperro device: {err}"
        ) from err
    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: PolperroConfigEntry) -> bool:
    """Unload a Lexent Polperro config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        await entry.runtime_data.async_shutdown()
    return unload_ok
