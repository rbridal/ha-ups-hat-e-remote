"""MQTT coordinator for a remote UPS HAT (E)."""
from __future__ import annotations

import json
import logging
import time
from datetime import timedelta
from typing import Any

from homeassistant.components import mqtt
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import CONF_STATE_TOPIC, DOMAIN, STALE_SECONDS

_LOGGER = logging.getLogger(__name__)


class RemoteUpsCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Holds the latest retained snapshot from ups-hat-e-remote."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=30),
            config_entry=entry,
        )
        self.entry = entry
        self.state_topic = entry.data[CONF_STATE_TOPIC]
        self.avail_topic = self.state_topic.rsplit("/", 1)[0] + "/availability"
        self._unsubs: list[Any] = []
        self._last = 0.0
        self._online = False

    async def async_start(self) -> None:
        self._unsubs.append(
            await mqtt.async_subscribe(self.hass, self.state_topic, self._on_state, qos=1, encoding="utf-8")
        )
        self._unsubs.append(
            await mqtt.async_subscribe(self.hass, self.avail_topic, self._on_avail, qos=1, encoding="utf-8")
        )

    async def async_stop(self) -> None:
        for unsub in self._unsubs:
            unsub()
        self._unsubs.clear()

    @callback
    def _on_state(self, msg) -> None:
        try:
            payload = json.loads(msg.payload)
        except json.JSONDecodeError:
            _LOGGER.warning("bad UPS payload on %s", self.state_topic)
            return
        if not isinstance(payload, dict):
            return
        self._last = time.monotonic()
        self._online = True
        self.async_set_updated_data(payload)

    @callback
    def _on_avail(self, msg) -> None:
        self._online = str(msg.payload).strip().lower() == "online"
        if not self._online:
            self.async_set_update_error(UpdateFailed("agent offline"))

    async def _async_update_data(self) -> dict[str, Any]:
        if self._last == 0:
            raise UpdateFailed("waiting for agent")
        if time.monotonic() - self._last > STALE_SECONDS:
            raise UpdateFailed("snapshot stale")
        if not self._online:
            raise UpdateFailed("agent offline")
        if self.data is None:
            raise UpdateFailed("waiting for snapshot")
        return self.data
