"""Unit tests for entity description completeness."""

from __future__ import annotations

from custom_components.lexent_polpero.binary_sensor import BINARY_SENSORS
from custom_components.lexent_polpero.select import SELECTS
from custom_components.lexent_polpero.sensor import SENSORS
from custom_components.lexent_polpero.switch import SWITCHES


class TestEntityCounts:
    """Validate entity description counts match the plan."""

    def test_sensor_count(self) -> None:
        """Seven sensors: humidity, temp, pm25, air quality, timer, error, filter."""
        assert len(SENSORS) == 7

    def test_binary_sensor_count(self) -> None:
        """One binary sensor: water_full."""
        assert len(BINARY_SENSORS) == 1

    def test_switch_count(self) -> None:
        """Seven switches: light, swing, uvc, ioniser, child_lock, quiet, turbo."""
        assert len(SWITCHES) == 7

    def test_select_count(self) -> None:
        """One select: fan_speed."""
        assert len(SELECTS) == 1


class TestUniqueKeys:
    """All entity keys must be unique."""

    def test_sensor_keys_unique(self) -> None:
        """Sensor keys are unique."""
        keys = [d.key for d in SENSORS]
        assert len(keys) == len(set(keys))

    def test_switch_keys_unique(self) -> None:
        """Switch keys are unique."""
        keys = [d.key for d in SWITCHES]
        assert len(keys) == len(set(keys))

    def test_binary_sensor_keys_unique(self) -> None:
        """Binary sensor keys are unique."""
        keys = [d.key for d in BINARY_SENSORS]
        assert len(keys) == len(set(keys))

    def test_select_keys_unique(self) -> None:
        """Select keys are unique."""
        keys = [d.key for d in SELECTS]
        assert len(keys) == len(set(keys))


class TestSensorDescriptions:
    """Validate sensor description details."""

    def test_humidity_sensor_has_device_class(self) -> None:
        """Humidity sensor uses humidity device class."""
        desc = next(d for d in SENSORS if d.key == "current_humidity")
        assert desc.device_class is not None

    def test_temperature_sensor_has_unit(self) -> None:
        """Temperature sensor reports in Celsius."""
        desc = next(d for d in SENSORS if d.key == "temperature")
        assert desc.native_unit_of_measurement is not None

    def test_pm25_sensor_is_enum(self) -> None:
        """PM2.5 sensor is an enum with correct options."""
        desc = next(d for d in SENSORS if d.key == "pm25_quality")
        assert desc.options == ["excellent", "good", "bad"]

    def test_air_quality_sensor_is_enum(self) -> None:
        """Air quality sensor is an enum with correct options."""
        desc = next(d for d in SENSORS if d.key == "air_quality")
        assert desc.options == ["excellent", "good", "bad"]

    def test_diagnostic_sensors_have_entity_category(self) -> None:
        """Error code and filter status are diagnostic entities."""
        for key in ("error_code", "filter_status"):
            desc = next(d for d in SENSORS if d.key == key)
            assert desc.entity_category is not None


class TestSwitchDescriptions:
    """Validate switch description details."""

    def test_all_switches_have_set_fn(self) -> None:
        """Every switch has a set_fn for commanding the device."""
        for desc in SWITCHES:
            assert desc.set_fn, f"Switch {desc.key} missing set_fn"

    def test_all_switches_have_value_fn(self) -> None:
        """Every switch has a value_fn for reading state."""
        for desc in SWITCHES:
            assert desc.value_fn, f"Switch {desc.key} missing value_fn"


class TestSelectDescriptions:
    """Validate select description details."""

    def test_fan_speed_options(self) -> None:
        """Fan speed select has correct options."""
        desc = next(d for d in SELECTS if d.key == "fan_speed")
        assert desc.options == ["auto", "low", "medium", "high"]
