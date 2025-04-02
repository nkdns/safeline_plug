"""雷池传感器配置"""
import logging
from urllib.parse import urlparse
from datetime import timedelta
import aiohttp
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import EntityDescription
from .const import DOMAIN, SENSOR_TYPES, API_TIMEOUT

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(seconds=5)

async def async_setup_entry(hass, entry, async_add_entities):
    config = entry.data
    api = SafelineAPI(config["host"], config["api_token"])
    sensors = []
    for sensor in SENSOR_TYPES:
        sensors.append(SafelineSensor(api,sensor))

    async_add_entities(sensors, update_before_add=True)

class SafelineSensor(SensorEntity):
    '''定义雷池传感器'''
    def __init__(self, api, sensor):
        self._api = api
        self._safelinesensor = sensor
        self._path = SENSOR_TYPES[self._safelinesensor]['path']
        self.entity_description = EntityDescription(
            key= SENSOR_TYPES[self._safelinesensor]['key'],
            name= SENSOR_TYPES[self._safelinesensor]['name']
        )
        self._parsed_url = urlparse(self._api.host)
        self._attr_unique_id = (
            f"{DOMAIN}_{SENSOR_TYPES[self._safelinesensor]['key']}"
            f"_{self._parsed_url.netloc}"
        )
        self.entity_id = f"sensor.{SENSOR_TYPES[self._safelinesensor]['key']}"
        self._attr_name = SENSOR_TYPES[self._safelinesensor]['name']
        self._attr_icon = SENSOR_TYPES[self._safelinesensor]['icon']
        self._attr_native_unit_of_measurement = SENSOR_TYPES[self._safelinesensor]['unit']
        self._state = None
        self._attr_available = False
        self._key = SENSOR_TYPES[self._safelinesensor]['key']

    async def async_update(self):
        '''跟新传感器数据的方法'''
        try:
            # 获取原始数据
            if self._key == "qps":
                raw_data = await self._api.fetch_data()
                qpslist = raw_data.get("data", {}).get("nodes", [])
                value = 0
                if "0.0.0.0:0" in qpslist[-1]:
                    value = qpslist[-1]["0.0.0.0:0"]  # 根据实际API响应结构调整
            else:
                raw_data = await self._api.fetch_stats()
                value = raw_data.get("data", {}).get(self._key)
            # 数据有效性检查
            if value is None:
                self._attr_available = False
                return
            self._attr_native_value = value
            self._attr_available = True
        except Exception as e:
            self._attr_available = False
            _LOGGER.error("更新传感器失败: %s", str(e))

class SafelineAPI:
    '''API请求类'''
    def __init__(self, host, token):
        self.host = host
        self.token = token

    async def fetch_data(self, endpoint):
        '''发送请求'''
        url = f"{self.host}{endpoint}"
        headers = {"X-SLCE-API-TOKEN": self.token}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=API_TIMEOUT) as resp:
                resp.raise_for_status()
                return await resp.json()
