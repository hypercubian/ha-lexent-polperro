"""Base entity for Lexent Polperro integration."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import PolperoCoordinator


class PolperoEntity(CoordinatorEntity[PolperoCoordinator]):
    """Base class for all Polperro entities."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: PolperoCoordinator, key: str) -> None:
        super().__init__(coordinator)
        mac = coordinator.client.mac
        self._attr_unique_id = f"{mac}_{key}"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info for the device registry."""
        client = self.coordinator.client
        return DeviceInfo(
            identifiers={(DOMAIN, client.mac)},
            name=self.coordinator.config_entry.title,
            manufacturer="Lexent",
            model="Polperro 30L",
        )
