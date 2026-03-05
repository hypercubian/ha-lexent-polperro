"""Switch platform for Lexent Polperro integration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import PolperoConfigEntry
from .coordinator import PolperoCoordinator
from .entity import PolperoEntity


@dataclass(frozen=True, kw_only=True)
class PolperoSwitchDescription(SwitchEntityDescription):
    """Describe a Polperro switch entity."""

    value_fn: str
    set_fn: str


SWITCHES: tuple[PolperoSwitchDescription, ...] = (
    PolperoSwitchDescription(
        key="light",
        translation_key="light",
        icon="mdi:lightbulb",
        value_fn="light",
        set_fn="set_light",
    ),
    PolperoSwitchDescription(
        key="swing",
        translation_key="swing",
        icon="mdi:arrow-up-down",
        value_fn="swing",
        set_fn="set_swing",
    ),
    PolperoSwitchDescription(
        key="uvc",
        translation_key="uvc",
        icon="mdi:lightbulb-fluorescent-tube",
        value_fn="uvc_enabled",
        set_fn="set_uvc",
    ),
    PolperoSwitchDescription(
        key="ioniser",
        translation_key="ioniser",
        icon="mdi:atom",
        value_fn="ioniser_enabled",
        set_fn="set_ioniser",
    ),
    PolperoSwitchDescription(
        key="child_lock",
        translation_key="child_lock",
        icon="mdi:lock",
        value_fn="child_lock",
        set_fn="set_child_lock",
    ),
    PolperoSwitchDescription(
        key="quiet",
        translation_key="quiet",
        icon="mdi:volume-off",
        value_fn="quiet",
        set_fn="set_quiet",
    ),
    PolperoSwitchDescription(
        key="turbo",
        translation_key="turbo",
        icon="mdi:fan-plus",
        value_fn="turbo",
        set_fn="set_turbo",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: PolperoConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Polperro switch entities."""
    coordinator = entry.runtime_data
    async_add_entities(PolperoSwitch(coordinator, desc) for desc in SWITCHES)


class PolperoSwitch(PolperoEntity, SwitchEntity):
    """Representation of a Polperro switch."""

    entity_description: PolperoSwitchDescription

    def __init__(
        self,
        coordinator: PolperoCoordinator,
        description: PolperoSwitchDescription,
    ) -> None:
        super().__init__(coordinator, description.key)
        self.entity_description = description

    @property
    def is_on(self) -> bool | None:
        """Return True if the switch is on."""
        state = self.coordinator.data
        if state is None:
            return None
        return getattr(state, self.entity_description.value_fn, None)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        await getattr(self.coordinator.client, self.entity_description.set_fn)(True)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        await getattr(self.coordinator.client, self.entity_description.set_fn)(False)
        await self.coordinator.async_request_refresh()
