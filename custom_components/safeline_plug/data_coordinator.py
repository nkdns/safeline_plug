"""雷池数据获取模块"""
import logging
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from .data_fetcher import SafelineData

_LOGGER = logging.getLogger(__name__)

class SafelineDataUpdateCoordinator(DataUpdateCoordinator):
    """自定义数据协调器,统一管理雷池API数据更新"""
    def __init__(self, hass, config):
        super().__init__(
            hass,
            _LOGGER,
            name="Safeline Coordinator",
            update_interval = timedelta(seconds=5)
        )
        self.safelinedata = SafelineData(config["host"], config["api_token"])

    async def _async_update_data(self):
        """核心方法：获取最新数据并统一格式"""
        try:
            return self.safelinedata.get_data()
        except Exception as e:
            _LOGGER.error("从雷池API获取数据失败: %s", e)
            raise
