# Lexent Polperro for Home Assistant

[![HACS](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://hacs.xyz/)
[![GitHub Release](https://img.shields.io/github/v/release/hypercubian/ha-lexent-polpero?filter=*&style=for-the-badge)](https://github.com/hypercubian/ha-lexent-polpero/releases)

Home Assistant custom integration for the **Lexent Polperro 30L dehumidifier/air purifier** (Gree model 13805). Communicates over the local network using the Gree WiFi protocol (AES-128-ECB encrypted UDP).

## Installation

### HACS (recommended)

1. Add this repository as a custom repository in HACS
2. Search for "Lexent Polperro" and install
3. Restart Home Assistant
4. Add the integration via **Settings > Devices & Services > Add Integration > Lexent Polperro**

### Manual

Copy `custom_components/lexent_polpero/` to your Home Assistant `custom_components/` directory and restart.

## Configuration

Enter your device's IP address. The integration will discover the MAC address automatically and bind to the device.

## Entities

| Platform | Entity | Description |
|----------|--------|-------------|
| Humidifier | Dehumidifier | Power, mode (dehumidify/laundry/purify), target humidity (30-80%) |
| Sensor | Current humidity | Ambient humidity percentage |
| Sensor | Temperature | Ambient temperature (Celsius) |
| Sensor | PM2.5 quality | PM2.5 air quality level |
| Sensor | Air quality | Overall air quality level |
| Sensor | Timer | Active timer (hours) |
| Sensor | Error code | Device error code (diagnostic) |
| Sensor | Filter status | Filter status (diagnostic) |
| Binary Sensor | Water full | Water tank full warning |
| Switch | Light | Display backlight |
| Switch | Swing | Louver swing |
| Switch | UVC | UVC sterilisation |
| Switch | Ioniser | Negative ion generator |
| Switch | Child lock | Panel lock |
| Switch | Quiet | Quiet/mute mode |
| Switch | Turbo | Turbo mode |
| Select | Fan speed | Auto / Low / Medium / High |

## Requirements

- Device must be on the same local network as Home Assistant
- UDP port 7000 must be reachable
