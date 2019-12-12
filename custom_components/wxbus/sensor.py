"""
文件名：sensor.py.

文件位置：HomeAssistant配置目录/custom_components/wxbus/sensor.py
演示程序，构建一个真正的温度传感器.

"""

# 因为京东万象的数据是以http方式提供的json数据，所以引入一些处理的库
import json
from urllib import request, parse

import logging
import voluptuous as vol

# 引入sensor下的PLATFORM_SCHEMA
from homeassistant.components.sensor import PLATFORM_SCHEMA
# 在homeassistant.const中定义了一些常量，我们在程序中会用到
from homeassistant.const import (
    ATTR_ATTRIBUTION, ATTR_FRIENDLY_NAME, TEMP_CELSIUS)
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

# 配置文件中平台下的两个配置项
CONF_LONG = "longitude"
CONF_LATI = "latitude"

ATTR_CROWD = "路况"
# 定义实体的OBJECT_ID与一些属性值
OBJECT_ID = "mccree_wxbus"
ICON = "mdi:bus"
ATTRIBUTION = "来自强无敌的第一个插件"

# 扩展基础的SCHEMA。在我们这个platform上，城市与京东万象的APPKEY是获得温度必须要配置的项
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_LONG): cv.string,
    vol.Required(CONF_LATI): cv.string,
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    """配置文件在sensor域下出现wxbus平台时，会自动调用wxbus目录下sensor.py中的setup_platform函数."""
    _LOGGER.info("setup platform sensor.mccree_wxbus...")

    # config仅仅包含配置文件中此平台下的内容
    # 定义输入参数，初始化需要的sensor对象
    sensor = mccree_wxbus(
        config.get(CONF_LONG),
        config.get(CONF_LATI))
    # 定义一个设备组，在其中装入sensor
    dev = []
    dev.append(sensor)
# 将设备加载入系统中
    add_devices(dev, True)


class mccree_wxbus(Entity):
    """定义一个传感器的类，继承自HomeAssistant的Entity类."""

    def __init__(self, longitude, latitude):
        """初始化."""
        self._state = None
        self._crowd = None
        self._unit_of_measurement = "站"
        self._url = 'https://wxms.wxbus.com.cn/BusService/Query_CrowdBySegmentID' + '?SegmentID=-33485204&' + 'Longitude=' + longitude + '&Latitude=' + latitude

    """返回实体的名字。通过python装饰器@property，使访问更自然（方法变成属性调用，可以直接使用xxx.name）."""
    @property
    def name(self):
        """返回实体的名字."""
        return OBJECT_ID

    @property
    def state(self):
        """返回当前的状态."""
        return self._state

    @property
    def registry_name(self):
        """返回实体的friendly_name属性."""
        return FRIENDLY_NAME

    @property
    def icon(self):
        """返回icon属性."""
        return ICON

    @property
    def unit_of_measurement(self):
        """返回unit_of_measuremeng属性."""
        return self._unit_of_measurement

    @property
    def device_state_attributes(self):
        """设置其它一些属性值."""
        if self._state is not None:
            return {
                ATTR_ATTRIBUTION: ATTRIBUTION,
                # 增加updatetime作为属性，表示温度数据的时间
                ATTR_CROWD: self._crowd
            }

    def update(self):
        """更新函数，在sensor组件下系统会定时自动调用（时间间隔在配置文件中可以调整，缺省为30秒）."""
        # update更新_state和_updatetime两个变量
        _LOGGER.info("Update the state...")

        # 通过HTTP访问，获取需要的信息
        infomation_file = request.urlopen(
            self._url)

        content = infomation_file.read()
        result = json.loads(content.decode('utf-8'))

        if result is None:
            _LOGGER.error("Request api Error")
            return
        elif result["message"] != "success":
            _LOGGER.error("Error API return, info=%s",
                          result["message"])
            return

        # 根据http返回的结果，更新_state和_updatetime
        all_result = result["items"]
        self._state = all_result[6]["forecastStation"]
        self._crowd = all_result[5]["crowdToNext"]
        if self._crowd == 0:
          self._crowd = '畅通'
        elif self._crowd == 1:
          self._crowd = '拥堵'
        elif self._crowd == 2:
          self._crowd = '超级拥堵'
        else :
          self._crowd = '无路况信息' 