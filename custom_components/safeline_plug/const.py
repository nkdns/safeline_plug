"""雷池集成常量"""
from homeassistant.components.sensor import SensorStateClass
DOMAIN = "safeline_plug"
API_TIMEOUT = 10

# API 定义
TEST_API="/api/stat/qps"

# 传感器定义
SENSOR_TYPES = {
    "safeline_qps": {
        # used
        "icon": "mdi:speedometer",
        # used
        "name": "实时qps",
        # used
        "key": "qps",
        "path": "/api/stat/qps",
        # used
        "unit": "次/秒",
        # used
        "state_class": SensorStateClass.MEASUREMENT
    }
}
