"""
文件名：mccree.py.
 
"""
import logging

# 引入这两个库，用于配置文件格式校验
import voluptuous as vol
import homeassistant.helpers.config_validation as cv

 # HomeAssistant的惯例，会在组件程序中定义域，域与组件程序名相同
DOMAIN = "mccree"
ENTITYID = DOMAIN + ".test"

# 预定义配置文件中的key值
CONF_NAME = "name"
CONF_SLOGON = "slogon"

# 预定义缺省的配置值
DEFAULT_SLOGON = "默认描述！"

# 在python中，__name__代表模块名字
_LOGGER = logging.getLogger(__name__)

'''
def setup(hass, config):
    """HomeAssistant在配置文件中发现hachina域的配置后，会自动调用hachina.py文件中的setup函数."""
        # 准备一些属性值，在给实体设置状态的同时，设置实体的这些属性
    attri = {"icon": "mdi:yin-yang",
            "friendly_name": "迎接新世界",
            "slogon": "积木构建智慧空间！"}
    # 设置实体hachina.Hello_World的状态。
    # 注意1：实体并不需要被创建，只要设置了实体的状态，实体就自然存在了
    # 注意2：实体的状态可以是任何字符串
    hass.states.set(ENTITYID, "太棒了！",attributes=attri)
    def change_state(call):
        """change_state函数切换改变实体的状态."""
        # 记录info级别的日志
        _LOGGER.info("hachina's change_state service is called.")
        # 切换改变状态值
        if hass.states.get(ENTITYID).state == '不好':
            hass.states.set(ENTITYID, '真好', attributes=attri)
        else:
            hass.states.set(ENTITYID, '不好', attributes=attri)
    # 注册服务hachina.change_state
    hass.services.register(DOMAIN, 'change_state', change_state)
    # 返回True代表初始化成功
    return True
'''
# 配置文件的样式
CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                # “name”在配置文件中是必须存在的（Required），否则报错，它的类型是字符串
                vol.Required(CONF_NAME): cv.string,
                # “slogon”在配置文件中可以没有（Optional），如果没有缺省值为“默认描述！”，它的类型是字符串
                vol.Optional(CONF_SLOGON, default=DEFAULT_SLOGON): cv.string,
            }),
    },
    extra=vol.ALLOW_EXTRA)


def setup(hass, config):
    """HomeAssistant在配置文件中发现hachina域的配置后，会自动调用hachina.py文件中的setup函数."""
    # config[DOMAIN]代表这个域下的配置信息
    conf = config[DOMAIN]
    # 获得具体配置项信息
    name = conf.get(CONF_NAME)
    slogon = conf.get(CONF_SLOGON)
 
    _LOGGER.info("Get the configuration %s=%s; %s=%s",
                 CONF_NAME, name,
                 CONF_SLOGON, slogon)
 
        # 准备一些属性值，设置实体的这些属性
    attr = {"icon": "mdi:yin-yang",
            "friendly_name": name,
            "slogon": slogon}
    # 设置实体DOMAIN.test的状态。
    # 注意1：实体并不需要被创建，只要设置了实体的状态，实体就自然存在了
    # 注意2：实体的状态可以是任何字符串
    hass.states.set(ENTITYID, '太棒了', attributes=attr)
    def change_state(call):
        """change_state函数切换改变实体的状态."""
        # 记录info级别的日志
        _LOGGER.info("hachina's change_state service is called.")
        # 切换改变状态值
        if hass.states.get(ENTITYID).state == '不好':
            hass.states.set(ENTITYID, '真好', attributes=attri)
        else:
            hass.states.set(ENTITYID, '不好', attributes=attri)
    # 注册服务hachina.change_state
    hass.services.register(DOMAIN, 'change_state', change_state)
    
    return True