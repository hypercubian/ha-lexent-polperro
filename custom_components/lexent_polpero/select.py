"""Select platform for Lexent Polperro integration."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.select import SelectEntity, SelectEntityDescription
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from polpero import FanSpeed  # type: ignore[attr-defined]

from . import PolperoConfigEntry
from .coordinator import PolperoCoordinator
from .entity import PolperoEntity

FAN_SPEED_MAP: dict[str, FanSpeed] = {
    "auto": FanSpeed.AUTO,
    "low": FanSpeed.LOW,
    "medium": FanSpeed.MEDIUM,
    "high": FanSpeed.HIGH,
}

FAN_SPEED_REVERSE: dict[FanSpeed, str] = {v: k for k, v in FAN_SPEED_MAP.items()}


@dataclass(frozen=True, kw_only=True)
class PolperoSelectDescription(SelectEntityDescription):
    """Describe a Polperro select entity."""

    value_fn: str
    set_fn: str


SELECTS: tuple[PolperoSelectDescription, ...] = (
    PolperoSelectDescription(
        key="fan_speed",
        translation_key="fan_speed",
        icon="mdi:fan",
        options=list(FAN_SPEED_MAP.keys()),
        value_fn="fan_speed",
        set_fn="set_fan_speed",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: PolperoConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Polperro select entities."""
    coordinator = entry.runtime_data
    async_add_entities(PolperoSelect(coordinator, desc) for desc in SELECTS)


class PolperoSelect(PolperoEntity, SelectEntity):
    """Representation of a Polperro select."""

    entity_description: PolperoSelectDescription

    def __init__(
        self,
        coordinator: PolperoCoordinator,
        description: PolperoSelectDescription,
    ) -> None:
        super().__init__(coordinator, description.key)
        self.entity_description = description

    @property
    def current_option(self) -> str | None:
        """Return the current selected option."""
        state = self.coordinator.data
        if state is None:
            return None
        value = getattr(state, self.entity_description.value_fn, None)
        if isinstance(value, FanSpeed):
            return FAN_SPEED_REVERSE.get(value)
        return str(value) if value is not None else None

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        if option in FAN_SPEED_MAP:
            await self.coordinator.client.set_fan_speed(FAN_SPEED_MAP[option])
            await self.coordinator.async_request_refresh()
