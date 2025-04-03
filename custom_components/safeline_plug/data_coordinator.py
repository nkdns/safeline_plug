"""雷池数据获取模块"""
import asyncio
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
            update_interval = None
        )
        self.safelinedata = SafelineData(config["host"], config["api_token"])
        self._qps_update_interval = timedelta(seconds=5)
        self._other_data_update_interval = timedelta(seconds=30)
        self._qps_task = None
        self._other_data_task = None

    async def _async_update_qps(self):
        """每 5 秒更新 QPS"""
        while True:
            try:
                qps_data = await self.safelinedata.get_qps_data()
                self.async_set_updated_data(qps_data)  # 只更新 QPS
            except Exception as e:
                _LOGGER.error("获取 QPS 失败: %s", e, exc_info=True)
            await asyncio.sleep(self._qps_update_interval.total_seconds())

    async def _async_update_other_data(self):
        """每 30 秒更新其他数据"""
        while True:
            try:
                other_data = await self.safelinedata.get_other_data()  # 获取全部数据
                self.async_set_updated_data(other_data)
            except Exception as e:
                _LOGGER.error("获取其他数据失败: %s", e, exc_info=True)
            await asyncio.sleep(self._other_data_update_interval.total_seconds())

    async def _async_update_data(self):
        """首次加载时获取所有数据"""
        _LOGGER.info("首次加载数据")
        try:
            return await self.safelinedata.get_data()
        except Exception as e:
            _LOGGER.error("从雷池API获取数据失败: %s", e, exc_info=True)
            raise

    async def async_start(self):
        """启动任务"""
        # 首次获取所有数据
        await self.async_refresh()

        # 启动定时任务
        if self._qps_task is None:
            self._qps_task = asyncio.create_task(self._async_update_qps())

        if self._other_data_task is None:
            self._other_data_task = asyncio.create_task(self._async_update_other_data())

    async def async_stop(self):
        """停止任务"""
        if self._qps_task:
            self._qps_task.cancel()
            self._qps_task = None
        if self._other_data_task:
            self._other_data_task.cancel()
            self._other_data_task = None
