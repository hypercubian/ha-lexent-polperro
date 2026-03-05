"""Constants for the Lexent Polperro integration."""

DOMAIN = "lexent_polpero"

CONF_HOST = "host"
CONF_MAC = "mac"

PLATFORMS: list[str] = [
    "binary_sensor",
    "humidifier",
    "select",
    "sensor",
    "switch",
]

DEFAULT_SCAN_INTERVAL = 30
