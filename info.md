![Lexent](https://raw.githubusercontent.com/hypercubian/ha-lexent-polperro/master/images/logo.png)

# Lexent Polperro Integration for Home Assistant

![Lexent Polperro 30L](https://raw.githubusercontent.com/hypercubian/ha-lexent-polperro/master/images/polperro-white.png)

Custom Home Assistant integration for local-network control of the [Lexent Polperro 30L](https://www.lexent.co.uk/products/polperro-air-purifier-dehumidifier) dehumidifier / air purifier via the Gree WiFi protocol. No cloud dependency - all communication stays on your LAN.

[![Release](https://img.shields.io/github/v/release/hypercubian/ha-lexent-polperro?filter=*&style=for-the-badge)](https://github.com/hypercubian/ha-lexent-polperro/releases)
[![License](https://img.shields.io/github/license/hypercubian/ha-lexent-polperro?style=for-the-badge)](LICENSE)
[![HACS Custom](https://img.shields.io/badge/HACS-Custom-41BDF5?style=for-the-badge)](https://hacs.xyz/)

---

## Device

| Feature | Detail |
|---------|--------|
| **Product** | Lexent Polperro 30L Dehumidifier / Air Purifier |
| **Model** | Gree 13805 (LT-GDN30W) |
| **Protocol** | Gree WiFi - AES-128-ECB encrypted JSON over UDP port 7000 |
| **Connectivity** | Local network only, no cloud |

## Configuration

1. Go to **Settings** > **Devices & Services** > **Add Integration**
2. Search for **Lexent Polperro**
3. Enter the device's IP address

The integration validates connectivity by connecting to the device, reading its state, and discovering its MAC address automatically.

## Entities

### Humidifier (primary)

| Platform | Entity | Description |
|----------|--------|-------------|
| **Humidifier** | Dehumidifier | Power on/off, mode (dehumidify / laundry / purify), target humidity (30-80% in 5% steps), current humidity readout |

### Sensors

| Platform | Entity | Device Class | Description |
|----------|--------|-------------|-------------|
| **Sensor** | Humidity | humidity | Ambient humidity (%) |
| **Sensor** | Temperature | temperature | Ambient temperature |
| **Sensor** | PM2.5 quality | enum | PM2.5 level: excellent / good / bad |
| **Sensor** | Air quality | enum | Overall air quality: excellent / good / bad |
| **Sensor** | Timer | - | Active timer (hours) |
| **Sensor** | Error code | - | Device error code (diagnostic) |
| **Sensor** | Filter status | - | Filter status (diagnostic) |
| **Binary Sensor** | Water full | problem | Water tank full warning |

### Controls

| Platform | Entity | Description |
|----------|--------|-------------|
| **Switch** | Display light | Backlight on/off |
| **Switch** | Swing | Louver swing on/off |
| **Switch** | UVC | UVC sterilisation on/off |
| **Switch** | Ioniser | Negative ion generator on/off |
| **Switch** | Child lock | Panel lock on/off |
| **Switch** | Quiet mode | Quiet/mute on/off |
| **Switch** | Turbo mode | Turbo on/off |
| **Select** | Fan speed | Auto / Low / Medium / High |

## Technical Details

- **Communication:** Gree WiFi protocol via [polperro](https://github.com/hypercubian/lexent-polperro-py) - local UDP, AES-128-ECB encrypted
- **Connection:** Bind handshake on connect, automatic reconnection on errors
- **Polling:** 30-second update interval via DataUpdateCoordinator
- **Library:** [lexent-polperro-py](https://github.com/hypercubian/lexent-polperro-py) - async Python client for the Polperro dehumidifier

---

[![by Hypercubian](https://raw.githubusercontent.com/hypercubian/ha-lexent-polperro/master/images/hypercubian.png)](https://github.com/hypercubian)
