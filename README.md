<p align="center">
  <img src="https://raw.githubusercontent.com/hypercubian/ha-lexent-polperro/master/images/logo.png" alt="Lexent" width="200">
</p>

<h1 align="center">
  Lexent Polperro Integration<br>
  for <a href="https://www.home-assistant.io/"><img src="https://brands.home-assistant.io/homeassistant/logo.png" height="28" alt="Home Assistant"></a>
</h1>

<p align="center">
  <img src="https://raw.githubusercontent.com/hypercubian/ha-lexent-polperro/master/images/polperro-white.png" alt="Lexent Polperro 30L - Gloss White" width="200">
</p>

<p align="center">
  Custom <a href="https://www.home-assistant.io/">Home Assistant</a> integration for local-network control of the <a href="https://www.lexent.co.uk/products/polperro-air-purifier-dehumidifier">Lexent Polperro 30L</a> dehumidifier / air purifier via the Gree WiFi protocol.<br>
  No cloud dependency - all communication stays on your LAN.
</p>

<p align="center">
  <a href="https://github.com/hypercubian/ha-lexent-polperro/releases"><img src="https://img.shields.io/github/v/release/hypercubian/ha-lexent-polperro?filter=*&style=for-the-badge" alt="Release"></a>
  <a href="https://github.com/hypercubian/ha-lexent-polperro/releases"><img src="https://img.shields.io/github/downloads/hypercubian/ha-lexent-polperro/total?style=for-the-badge" alt="Downloads"></a>
  <a href="https://github.com/hypercubian/ha-lexent-polperro/stargazers"><img src="https://img.shields.io/github/stars/hypercubian/ha-lexent-polperro?style=for-the-badge" alt="Stars"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/hypercubian/ha-lexent-polperro?style=for-the-badge" alt="License"></a>
</p>
<p align="center">
  <a href="https://hacs.xyz/"><img src="https://img.shields.io/badge/HACS-Custom-41BDF5?style=for-the-badge" alt="HACS Custom"></a>
  <img src="https://img.shields.io/badge/HA-%3E%3D%202024.8-41BDF5?style=for-the-badge" alt="Home Assistant 2024.8+">
  <a href="https://github.com/hypercubian/ha-lexent-polperro/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/hypercubian/ha-lexent-polperro/ci.yml?branch=master&style=for-the-badge&label=CI" alt="CI"></a>
  <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000?style=for-the-badge" alt="Code style: black"></a>
  <a href="https://mypy-lang.org/"><img src="https://img.shields.io/badge/type%20checked-mypy-blue?style=for-the-badge" alt="Type checked: mypy"></a>
</p>

<br>
<br>
<br>
<p align="center">
  <a href="https://my.home-assistant.io/redirect/hacs_repository/?owner=hypercubian&repository=ha-lexent-polperro&category=integration">
    <img src="https://my.home-assistant.io/badges/hacs_repository.svg" alt="Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.">
  </a>
</p>

<br>
<br>
<br>

<p align="right">
  <a href="https://github.com/hypercubian"><img src="https://raw.githubusercontent.com/hypercubian/ha-lexent-polperro/master/images/hypercubian.png" height="60" alt="by Hypercubian"></a>
</p>

---

## Device

| Feature | Detail                                                    |
|---------|-----------------------------------------------------------|
| **Product** | Lexent Polperro 30L Dehumidifier / Air Purifier          |
| **Model** | Gree 13805 (LT-GDN30W)                                    |
| **Protocol** | Gree WiFi - AES-128-ECB encrypted JSON over UDP port 7000 |
| **Connectivity** | Local network only, no cloud                              |

## Installation

### HACS (Recommended)

> **Don't have HACS?** Follow the [official HACS installation guide](https://hacs.xyz/docs/use/download/download/) first.

1. Open HACS in your Home Assistant instance
2. Go to **Integrations** > three-dot menu > **Custom repositories**
3. Add `https://github.com/hypercubian/ha-lexent-polperro` with category **Integration**
4. Search for "Lexent Polperro" and install
5. Restart Home Assistant

### Manual

1. Copy the `custom_components/lexent_polperro` directory into your Home Assistant `config/custom_components/` folder
2. Restart Home Assistant

## Configuration

1. Go to **Settings** > **Devices & Services** > **Add Integration**
2. Search for **Lexent Polperro**
3. Enter the device's IP address

The integration validates connectivity by connecting to the device, reading its state, and discovering its MAC address automatically.

## Entities

### Humidifier (primary)

| Platform | Entity | Description |
|----------|--------|-------------|
| **Humidifier** | Dehumidifier | Power on/off, mode (dehumidify / laundry / purify), target humidity (30–80% in 5% steps), current humidity readout |

### Sensors

| Platform | Entity | Device Class | Description |
|----------|--------|-------------|-------------|
| **Sensor** | Humidity | humidity | Ambient humidity (%) |
| **Sensor** | Temperature | temperature | Ambient temperature (°C) |
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
- **Polling:** 30-second update interval via `DataUpdateCoordinator`
- **Library:** [lexent-polperro-py](https://github.com/hypercubian/lexent-polperro-py) - async Python client for the Polperro dehumidifier

## Contributing

1. Clone the repo
2. Install dependencies: `poetry install`
3. Install pre-commit hooks: `poetry run pre-commit install`
4. Run tests: `poetry run pytest tests/unit/`

## License

[MIT](LICENSE)
