# HA Waveshare UPS HAT (E) Remote

Home Assistant custom integration for a Pi running [ups-hat-e-remote](https://github.com/rbridal/ups-hat-e-remote).

Same device page as the local Waveshare UPS HAT (E) integration: system state, battery, pack and cell voltages, charge/discharge current, AC adapter V/A/W, remaining capacity, runtime, time to full, power switch, charging.

Domain is `waveshare_ups_hat_remote` so it can sit next to the local `waveshare_ups_hat` integration on shop-ha.

## Related repositories

Rule of thumb: HAT on the HA box → use the local integration; HAT on a different Pi → install the remote service on that Pi and the remote integration in Home Assistant.

- [homeassistant_waveshare_ups_hat_e](https://github.com/rbridal/homeassistant_waveshare_ups_hat_e) — Home Assistant integration for a UPS HAT (E) attached directly to the HA host (I2C).
- [ha-ups-hat-e-remote](https://github.com/rbridal/ha-ups-hat-e-remote) — Home Assistant integration that displays a remote UPS HAT (E) over MQTT. **This repo.**
- [ups-hat-e-remote](https://github.com/rbridal/ups-hat-e-remote) — Companion service that runs on the Pi with the HAT, reads I2C, and publishes status over MQTT.

## Config

Needs the MQTT integration (Mosquitto). Add this repo in HACS as a custom repository, or copy `custom_components/waveshare_ups_hat_remote` into HA config.

Config flow asks for:

- device id (must match the Pi `device_id`, default `shop-dash`)
- display name (default `Shop Dash UPS`)
- state topic (default `ups-hat-e/{device_id}/state`)

Availability is `{prefix}/availability`. No message for 90 seconds, or `offline`, marks the device unavailable.
