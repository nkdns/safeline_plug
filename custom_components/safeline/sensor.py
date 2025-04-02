"""雷池传感器配置"""
import logging
import aiohttp
from datetime import timedelta
from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN, API_GET_QPS, API_TIMEOUT

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(seconds=2)

async def async_setup_entry(hass, entry, async_add_entities):
    config = entry.data
    api = SafelineAPI(config["host"], config["api_token"])
    sensors = [
        SafelineSensor(api, "实时QPS", "qps", "mdi:speedometer")
    ]
    
    async_add_entities(sensors, update_before_add=True)

class SafelineSensor(SensorEntity):
    def __init__(self, api, name, key, icon):
        self._api = api
        self._attr_name = name
        self._attr_icon = icon
        self._attr_unique_id = f"safeline_{key}"
        self._attr_native_unit_of_measurement = "次/秒"
        self._state = None
        self._attr_available = False
        self._key = key

    async def async_update(self):
        try:
            # 获取原始数据
            if self._key == "qps":
                raw_data = await self._api.fetch_qps()
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
    def __init__(self, host, token):
        self.host = host
        self.token = token

    async def fetch_qps(self):
        return await self._fetch_data(API_GET_QPS)

    async def _fetch_data(self, endpoint):
        url = f"{self.host}{endpoint}"
        headers = {"X-SLCE-API-TOKEN": self.token}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=API_TIMEOUT) as resp:
                resp.raise_for_status()
                return await resp.json()