"""Sensor platform for Lexent Polperro integration."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import EntityCategory, UnitOfTemperature, UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from polperro import AirQuality  # type: ignore[attr-defined]

from . import PolperroConfigEntry
from .coordinator import PolperroCoordinator
from .entity import PolperroEntity

_QUALITY_MAP: dict[AirQuality, str] = {
    AirQuality.EXCELLENT: "excellent",
    AirQuality.GOOD: "good",
    AirQuality.BAD: "bad",
}


@dataclass(frozen=True, kw_only=True)
class PolperroSensorDescription(SensorEntityDescription):
    """Describe a Polperro sensor entity."""

    value_fn: str | Callable[[Any], Any]


SENSORS: tuple[PolperroSensorDescription, ...] = (
    PolperroSensorDescription(
        key="current_humidity",
        translation_key="current_humidity",
        device_class=SensorDeviceClass.HUMIDITY,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement="%",
        value_fn="current_humidity",
    ),
    PolperroSensorDescription(
        key="temperature",
        translation_key="temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        value_fn="temperature",
    ),
    PolperroSensorDescription(
        key="pm25_quality",
        translation_key="pm25_quality",
        device_class=SensorDeviceClass.ENUM,
        options=["excellent", "good", "bad"],
        icon="mdi:blur",
        value_fn=lambda s: _QUALITY_MAP.get(s.pm25),
    ),
    PolperroSensorDescription(
        key="air_quality",
        translation_key="air_quality",
        device_class=SensorDeviceClass.ENUM,
        options=["excellent", "good", "bad"],
        icon="mdi:air-filter",
        value_fn=lambda s: _QUALITY_MAP.get(s.air_quality),
    ),
    PolperroSensorDescription(
        key="timer",
        translation_key="timer",
        icon="mdi:timer",
        native_unit_of_measurement=UnitOfTime.HOURS,
        value_fn="timer",
    ),
    PolperroSensorDescription(
        key="error_code",
        translation_key="error_code",
        icon="mdi:alert-circle",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn="error_code",
    ),
    PolperroSensorDescription(
        key="filter_status",
        translation_key="filter_status",
        icon="mdi:air-filter",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn="filter_status",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: PolperroConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Polperro sensor entities."""
    coordinator = entry.runtime_data
    async_add_entities(PolperroSensor(coordinator, desc) for desc in SENSORS)


class PolperroSensor(PolperroEntity, SensorEntity):
    """Representation of a Polperro sensor."""

    entity_description: PolperroSensorDescription

    def __init__(
        self,
        coordinator: PolperroCoordinator,
        description: PolperroSensorDescription,
    ) -> None:
        super().__init__(coordinator, description.key)
        self.entity_description = description

    @property
    def native_value(self) -> Any:
        """Return the sensor value."""
        state = self.coordinator.data
        if state is None:
            return None
        value_fn = self.entity_description.value_fn
        if callable(value_fn):
            return value_fn(state)
        return getattr(state, value_fn, None)
