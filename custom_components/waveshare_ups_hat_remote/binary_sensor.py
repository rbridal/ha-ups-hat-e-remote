"""Binary sensors for Waveshare UPS HAT (E) Remote."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import RemoteUpsCoordinator


@dataclass(frozen=True, kw_only=True)
class WaveshareBinarySensorEntityDescription(BinarySensorEntityDescription):
    value_fn: Callable[[dict[str, Any]], bool]


BINARY_SENSORS: tuple[WaveshareBinarySensorEntityDescription, ...] = (
    WaveshareBinarySensorEntityDescription(
        key="power_switch",
        name="Power switch",
        device_class=BinarySensorDeviceClass.POWER,
        value_fn=lambda d: bool(d.get("online")),
    ),
    WaveshareBinarySensorEntityDescription(
        key="charging",
        name="Charging",
        device_class=BinarySensorDeviceClass.BATTERY_CHARGING,
        value_fn=lambda d: bool(d.get("is_charging")),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: RemoteUpsCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        RemoteUpsBinarySensor(coordinator, entry, description)
        for description in BINARY_SENSORS
    )


class RemoteUpsBinarySensor(CoordinatorEntity[RemoteUpsCoordinator], BinarySensorEntity):
    entity_description: WaveshareBinarySensorEntityDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: RemoteUpsCoordinator,
        entry: ConfigEntry,
        description: WaveshareBinarySensorEntityDescription,
    ) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.unique_id}_{description.key}"
        self._attr_suggested_object_id = description.key
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=entry.title,
            manufacturer="Waveshare",
            model="UPS HAT (E)",
        )

    @property
    def is_on(self) -> bool | None:
        if self.coordinator.data is None:
            return None
        return self.entity_description.value_fn(self.coordinator.data)
