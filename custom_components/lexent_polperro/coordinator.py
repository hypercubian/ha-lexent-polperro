"""Data update coordinator for Lexent Polperro devices."""

from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from polperro import DeviceState, PolperroClient  # type: ignore[attr-defined]

from .const import CONF_HOST, CONF_MAC, DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


class PolperroCoordinator(DataUpdateCoordinator[DeviceState]):
    """Coordinator that polls a Polperro dehumidifier for state updates."""

    config_entry: ConfigEntry

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self.client = PolperroClient(
            host=entry.data[CONF_HOST],
            mac=entry.data.get(CONF_MAC, ""),
        )
        self._connected = False

        super().__init__(
            hass,
            _LOGGER,
            config_entry=entry,
            name=f"{DOMAIN}_{entry.unique_id or entry.data[CONF_HOST]}",
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )

    async def _async_update_data(self) -> DeviceState:
        """Fetch state from the device."""
        try:
            if not self._connected:
                await self.client.connect()
                self._connected = True
            return await self.client.get_state()
        except Exception as err:
            self._connected = False
            try:
                await self.client.disconnect()
            except Exception:  # noqa: BLE001
                pass
            raise UpdateFailed(f"Error communicating with device: {err}") from err

    async def async_shutdown(self) -> None:
        """Disconnect from the device on shutdown."""
        await super().async_shutdown()
        if self._connected:
            await self.client.disconnect()
            self._connected = False
