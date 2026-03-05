"""Binary sensor platform for Lexent Polperro integration."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import PolperoConfigEntry
from .coordinator import PolperoCoordinator
from .entity import PolperoEntity


@dataclass(frozen=True, kw_only=True)
class PolperoBinarySensorDescription(BinarySensorEntityDescription):
    """Describe a Polperro binary sensor entity."""

    value_fn: str


BINARY_SENSORS: tuple[PolperoBinarySensorDescription, ...] = (
    PolperoBinarySensorDescription(
        key="water_full",
        translation_key="water_full",
        device_class=BinarySensorDeviceClass.PROBLEM,
        icon="mdi:water-alert",
        value_fn="water_full",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: PolperoConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Polperro binary sensor entities."""
    coordinator = entry.runtime_data
    async_add_entities(
        PolperoBinarySensor(coordinator, desc) for desc in BINARY_SENSORS
    )


class PolperoBinarySensor(PolperoEntity, BinarySensorEntity):
    """Representation of a Polperro binary sensor."""

    entity_description: PolperoBinarySensorDescription

    def __init__(
        self,
        coordinator: PolperoCoordinator,
        description: PolperoBinarySensorDescription,
    ) -> None:
        super().__init__(coordinator, description.key)
        self.entity_description = description

    @property
    def is_on(self) -> bool | None:
        """Return True if the binary sensor is on."""
        state = self.coordinator.data
        if state is None:
            return None
        return getattr(state, self.entity_description.value_fn, None)
