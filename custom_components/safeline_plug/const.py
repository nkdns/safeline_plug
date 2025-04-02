"""雷池集成常量"""
DOMAIN = "safeline_plug"
API_TIMEOUT = 10

# API 定义
API_GET_QPS="/api/stat/qps"

# 传感器定义
SENSOR_TYPES = {
    "safeline_qps": {
        "icon": "mdi:speedometer",
        "name": "实时qps",
        "key": "qps",
        "path": "/api/stat/qps",
        "unit": "次/秒"
    }
}
