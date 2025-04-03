"""雷池传感器配置"""
import logging
from urllib.parse import urlparse
from datetime import timedelta
from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, SENSOR_TYPES

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(seconds=5)

async def async_setup_entry(hass, entry, async_add_entities):
    '''入口函数'''
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    hass.loop.create_task(coordinator.async_start())

    sensors = [
        SafelineSensor(coordinator, sensor)
        for sensor in SENSOR_TYPES
    ]

    async_add_entities(sensors, update_before_add=True)

class SafelineSensor(CoordinatorEntity,SensorEntity):
    '''定义雷池传感器'''
    def __init__(self, coordinator, safelinesensor):
        super().__init__(coordinator)
        self._safelinesensor = safelinesensor
        self._setup_entity()

    def _setup_entity(self):
        sensor_config = SENSOR_TYPES[self._safelinesensor]
        self.entity_description = SensorEntityDescription(
            key = sensor_config['key'],
            name = sensor_config['name'],
            icon = sensor_config['icon'],
            native_unit_of_measurement = sensor_config['unit'],
            state_class = sensor_config['state_class']
        )
        parsed_url = urlparse(self.coordinator.safelinedata.host)
        self._attr_unique_id = (
            f"{DOMAIN}_{sensor_config['key']}_{parsed_url.netloc}"
        )
        self._key = sensor_config['key']
        self.entity_id = f"sensor.{sensor_config['key']}"

    @property
    def native_value(self):
        """从协调器缓存数据中解析数值"""
        return self.coordinator.data.get(self._key)

    @property
    def available(self) -> bool:
        """实体可用性 -> 协调器最近一次更新是否成功 -> 是否包含数据字典"""
        return (
            super().available
            and self.coordinator.last_update_success
            and self._key in self.coordinator.data
        )

    async def async_update(self):
        '''更新传感器数据的方法'''
