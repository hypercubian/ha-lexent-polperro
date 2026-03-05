"""Humidifier platform for Lexent Polperro integration."""

from __future__ import annotations

from typing import Any

from homeassistant.components.humidifier import (
    HumidifierDeviceClass,
    HumidifierEntity,
    HumidifierEntityDescription,
    HumidifierEntityFeature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from polpero import Mode  # type: ignore[attr-defined]

from . import PolperoConfigEntry
from .coordinator import PolperoCoordinator
from .entity import PolperoEntity

MODE_MAP: dict[str, Mode] = {
    "dehumidify": Mode.DEHUMIDIFY,
    "laundry": Mode.LAUNDRY,
    "purify": Mode.PURIFY,
}

MODE_REVERSE: dict[Mode, str] = {v: k for k, v in MODE_MAP.items()}

HUMIDIFIER_DESCRIPTION = HumidifierEntityDescription(
    key="dehumidifier",
    translation_key="dehumidifier",
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: PolperoConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Polperro humidifier entity."""
    coordinator = entry.runtime_data
    async_add_entities([PolperoHumidifier(coordinator)])


class PolperoHumidifier(PolperoEntity, HumidifierEntity):
    """Representation of the Polperro dehumidifier."""

    entity_description = HUMIDIFIER_DESCRIPTION
    _attr_device_class = HumidifierDeviceClass.DEHUMIDIFIER
    _attr_available_modes = list(MODE_MAP.keys())
    _attr_min_humidity = 30
    _attr_max_humidity = 80
    _attr_supported_features = HumidifierEntityFeature.MODES

    def __init__(self, coordinator: PolperoCoordinator) -> None:
        super().__init__(coordinator, HUMIDIFIER_DESCRIPTION.key)
        self.entity_description = HUMIDIFIER_DESCRIPTION

    @property
    def is_on(self) -> bool | None:
        """Return True if the dehumidifier is on."""
        state = self.coordinator.data
        if state is None:
            return None
        return state.power

    @property
    def mode(self) -> str | None:
        """Return the current operating mode."""
        state = self.coordinator.data
        if state is None:
            return None
        return MODE_REVERSE.get(state.mode)

    @property
    def target_humidity(self) -> int | None:
        """Return the target humidity."""
        state = self.coordinator.data
        if state is None:
            return None
        return state.target_humidity

    @property
    def current_humidity(self) -> int | None:
        """Return the current humidity."""
        state = self.coordinator.data
        if state is None:
            return None
        return state.current_humidity

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the dehumidifier on."""
        await self.coordinator.client.set_power(True)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the dehumidifier off."""
        await self.coordinator.client.set_power(False)
        await self.coordinator.async_request_refresh()

    async def async_set_humidity(self, humidity: int) -> None:
        """Set the target humidity, rounded to nearest 5."""
        rounded = round(humidity / 5) * 5
        rounded = max(30, min(80, rounded))
        await self.coordinator.client.set_target_humidity(rounded)
        await self.coordinator.async_request_refresh()

    async def async_set_mode(self, mode: str) -> None:
        """Set the operating mode."""
        if mode in MODE_MAP:
            await self.coordinator.client.set_mode(MODE_MAP[mode])
            await self.coordinator.async_request_refresh()
