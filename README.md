# HA Waveshare UPS HAT (E) Remote

Home Assistant custom integration for a Pi running [ups-hat-e-remote](https://github.com/rbridal/ups-hat-e-remote).

Same device page as the local Waveshare UPS HAT (E) integration: system state, battery, pack and cell voltages, charge/discharge current, AC adapter V/A/W, remaining capacity, runtime, time to full, power switch, charging.

Domain is `waveshare_ups_hat_remote` so it can sit next to the local `waveshare_ups_hat` integration on shop-ha.

## Config

Needs the MQTT integration (Mosquitto). Add this repo in HACS as a custom repository, or copy `custom_components/waveshare_ups_hat_remote` into HA config.

Config flow asks for:

- device id (must match the Pi `device_id`, default `shop-dash`)
- display name (default `Shop Dash UPS`)
- state topic (default `ups-hat-e/{device_id}/state`)

Availability is `{prefix}/availability`. No message for 90 seconds, or `offline`, marks the device unavailable.
