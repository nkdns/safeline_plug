"""雷池集成常量"""
from homeassistant.components.sensor import SensorStateClass
DOMAIN = "safeline_plug"
API_TIMEOUT = 10

# API 定义
TEST_API="/api/stat/qps"

# 传感器定义
SENSOR_TYPES = {
    # /stat/qps
    "safeline_qps": {
        "icon": "mdi:speedometer",
        "name": "实时qps",
        "key": "qps",
        "unit": "次/秒",
        "state_class": SensorStateClass.MEASUREMENT
    },
    # /stat/basic/attack
    "safeline_attack_ip": {
        "icon": "mdi:shield-alert",
        "name": "今日攻击IP",
        "key": "attack_ip",
        "unit": "个",
        "state_class": SensorStateClass.TOTAL
    },
    "safeline_intercept": {
        "icon": "mdi:shield-remove",
        "name": "今日拦截",
        "key": "intercept",
        "unit": "次",
        "state_class": SensorStateClass.TOTAL
    },
    # /dashboard/user/counts
    "safeline_today_pv": {
        "icon": "mdi:chart-line",
        "name": "今日请求",
        "key": "today_pv",
        "unit": "次",
        "state_class": SensorStateClass.TOTAL
    },
    "safeline_today_uv": {
        "icon": "mdi:account-group",
        "name": "今日独立访客",
        "key": "today_uv",
        "unit": "个",
        "state_class": SensorStateClass.TOTAL
    },
    "safeline_today_ip": {
        "icon": "mdi:ip-network",
        "name": "今日独立IP",
        "key": "today_ip",
        "unit": "个",
        "state_class": SensorStateClass.TOTAL
    },
    # /stat/basic/error_status_code
    "safeline_error_4xx": {
        "icon": "mdi:alert",
        "name": "今日4xx响应",
        "key": "error_4xx",
        "unit": "次",
        "state_class": SensorStateClass.TOTAL
    },
    "safeline_error_5xx": {
        "icon": "mdi:alert-circle",
        "name": "今日5xx响应",
        "key": "error_5xx",
        "unit": "次",
        "state_class": SensorStateClass.TOTAL
    },
    # /stat/advance/attack
    "safeline_attack_ip24": {
        "icon": "mdi:shield-alert",
        "name": "24小时攻击IP",
        "key": "attack_ip24",
        "unit": "个",
        "state_class": SensorStateClass.TOTAL
    },
    "safeline_intercept24": {
        "icon": "mdi:shield-remove",
        "name": "24小时拦截",
        "key": "intercept24",
        "unit": "次",
        "state_class": SensorStateClass.TOTAL
    },
    # /stat/advance/access
    "safeline_pv24": {
        "icon": "mdi:chart-line",
        "name": "24小时请求",
        "key": "pv24",
        "unit": "次",
        "state_class": SensorStateClass.TOTAL
    },
    "safeline_uv24": {
        "icon": "mdi:account-group",
        "name": "24小时独立访客",
        "key": "uv24",
        "unit": "个",
        "state_class": SensorStateClass.TOTAL
    },
    "safeline_ip24": {
        "icon": "mdi:ip-network",
        "name": "24小时独立IP24",
        "key": "ip24",
        "unit": "个",
        "state_class": SensorStateClass.TOTAL
    },
    # /stat/advance/error_status_code
    "safeline_error_4xx24": {
        "icon": "mdi:alert",
        "name": "24小时4xx响应",
        "key": "error_4xx24",
        "unit": "次",
        "state_class": SensorStateClass.TOTAL
    },
    "safeline_error_5xx24": {
        "icon": "mdi:alert-circle",
        "name": "24小时5xx响应",
        "key": "error_5xx24",
        "unit": "次",
        "state_class": SensorStateClass.TOTAL
    }
}
