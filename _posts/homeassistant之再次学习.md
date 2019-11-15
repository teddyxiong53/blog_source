---
title: homeassistant之再次学习
date: 2019-11-09 15:26:49
tags:
	- python

---

1

基于venv来进行学习使用。

从github下载代码。

进入到代码目录，创建一个名为venv的环境。

```
python3 -m venv venv
```

激活venv。

```
source ./venv/bin/activate
```

安装所有依赖：

```
pip install -r requirements_all.txt
```

安装总是在apcaccess这个地方卡住了，换了豆瓣和阿里的源都是如此。

我把这个包先注释掉看看。

还有一些包是从github下载的。

依赖的东西真的是非常多。

在googlemaps这一步又卡住了。

网上查了一下，你在安装A的时候，A需要自动安装B，B这个的下载，还是走pypi的通路，而不是走国内源。

所以，解决办法是，修改你的venv的package_index.py文件。

把这个index_url默认值改成阿里的。

```
class PackageIndex(Environment):
    """A distribution index that scans web pages for download URLs"""

    def __init__(
            self, index_url="http://mirrors.aliyun.com/pypi/simple", hosts=('*',),
```

再试一次看看。

还是一样的卡住。

不是改参数默认值，在到下面再赋值一次为阿里的源。

这样就可以了。

执行homeassistant的安装：

```
python setup.py install
```

提示了错误。

```
sudo apt-get install python-dev
```

```
‘libpython3.6-dev’ 找到任何软件包
```

可以看到是在安装yarl这一步出错的。

```
pip install yarl
```

这样安装就可以了。

然后hass启动就可以了。

默认是启动在8123端口，但是我的电脑上这个端口给了polipo了。不能通过传递参数来指定端口。

所以我把polipo 停掉。

现在可以启动homeassistant了。



现在策略改为，实现功能为主，先尽量不要看代码。

```
hass.io
用来把你的树莓派变成一个智能家居中心。
你可以专注于集成你的设备和编写自动化。

hass.io的优势
1、免费开源。
2、针对树莓派优化。
3、100%的本地自动化。
4、易于安装和更新。基于hassos和docker。
5、有管理web界面。
6、容易创建备份。
7、一键安装大量流行的插件。
```

hassos是基于buildroot构建的。地址在这里。

https://github.com/home-assistant/hassos/releases

```
安装方法
把下载的镜像烧录到sd卡。对于树莓派，建议SD卡至少32GB。
	
可选操作
设置wifi信息或者设置静态ip。
在配置分区里，network/my-network文件里进行配置。

网络配置方法
hassos使用NetworkManager来控制网络。
在后面的版本，你可以通过ui来配置。
当前还只能通过配置文件来做。

一个my-network文件的模板是这样
[connection]
id=my-network
uuid=72111c67-4a5d-4d5c-925e-f8ee26efb3c3
type=802-11-wireless

[802-11-wireless]
mode=infrastructure
ssid=MY_SSID
# Uncomment below if your SSID is not broadcasted
#hidden=true

[802-11-wireless-security]
auth-alg=open
key-mgmt=wpa-psk
psk=MY_WLAN_SECRET_KEY

[ipv4]
method=auto

[ipv6]
addr-gen-mode=stable-privacy
method=auto
```

```
第一次开机，hassos会自动下载homeassistant的最新版本。
这个时间可能要20分钟左右。
你可以选择运行指定版本的homeassistant
hassio ha update --version=0.xx.x

```



```
missing environment variable: bootfile
Retrieving file: pxelinux.cfg/default-arm-bcm283x
Waiting for Ethernet connection... done.
*** ERROR: `serverip' not set
missing environment variable: bootfile
Retrieving file: pxelinux.cfg/default-arm
Waiting for Ethernet connection... done.
*** ERROR: `serverip' not set
missing environment variable: bootfile
Retrieving file: pxelinux.cfg/default
Waiting for Ethernet connection... done.
*** ERROR: `serverip' not set
Config file not found
Waiting for Ethernet connection... done.
BOOTP broadcast 1
BOOTP broadcast 2
BOOTP broadcast 3
BOOTP broadcast 4
BOOTP broadcast 5
```

最后停在了这里：

```
Retry time exceeded; starting again
HassOS> 
HassOS> 
```

这个其实是uboot的。

配置怎么写呢？

需要另外一个U盘，格式化为FAT32，卷标设置为config。

然后在这个U盘下，新建一个network的目录，network目录下新建一个名为system-connections的文件。

我当前使用的就是从U盘启动的。我直接把当前的FAT分区的卷标改为CONFIG。

然后新建好配置文件。

重新开机。还是不行。

这种方式行不通。

我还是用Raspbian自己安装的方式来做吧。

通过pip的方式来安装homeassistant。

安装python：

```
sudo apt-get install python3 python3-venv python3-pip
```

添加一个homeassistant的用户。

```
sudo useradd -rm homeassistant
cd /srv
sudo mkdir homeassistant
sudo chown homeassistant:homeassistant homeassistant
```

创建并进入到 homeassistant 虚拟环境

```
 sudo su -s /bin/bash homeassistant
 cd /srv/homeassistant
 python3 -m venv .
 source bin/activate
```

接下来的操作，在homeassistant这个venv里进行。

```
python3 -m pip install wheel
pip3 install homeassistant
```

为了加快速度，先到/home/homeassistant/.pip/pip.conf，配置为阿里云的源。

再进行安装。

发现版本低了。

```
homeassistant requires Python '>=3.6.1' but the running Python is 3.5.3
```

现在这个是网上找的Ubuntu版本的升级方式。我是排斥使用编译的方式的。

```
sudo apt-get install software-properties-common

sudo add-apt-repository ppa:jonathonf/python-3.6 
sudo apt-get update 
sudo apt-get install python3.6
```

知乎上找到一个方法，看到行不行。

```
wget http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-armv7l.sh
```

然后执行这个脚本，会有写配置会提示你填写。

尽量按默认的来。

miniconda都说很久没有更新了。不可靠。

最好是找一个deb包来安装。

但是找不到。算了，还是编译吧。

```
./configure --enable-optimizations
make -j2
sudo make altinstall
```



自己写一个组件

在~/.homeassistant目录下，新建custom_components目录。目录下新建一个hachina.py的文件。

内容如下：

```
def setup(hass, config):
	hass.states.set("hachina.hello_world", "太棒了")
	return True
```

然后在configuration.yml里，增加一行：

```
hachina:
```

然后重启hass。

就可以看到组件生效了。

然后我们看增加设备的属性值。

安装hass的标准做法，将域在组件程序的开头定义。

```
DOMAIN = 'hachina'

def setup(hass, config):
	attr = {
		"icon": "mdi: yin-yang",
		"friendly_name": "迎接新世界",
		"slogon": "积木构建智慧空间"
	}
	hass.states.set(DOMAIN + ".hello_world", "太棒了", attributes=attr)
	return True
	
```

接下来我们看看如何注册一个服务。

```
import logging

DOMAIN = 'hachina'
ENTITY_ID = DOMAIN + ".hello_world"

_LOGGER = logging.getLogger(__name__)

def setup(hass, config):
	attr = {
		"icon": "mdi: yin-yang",
		"friendly_name": "迎接新世界",
		"slogon": "积木构建智慧空间"
	}
	hass.states.set(ENTITY_ID, "太棒了", attributes=attr)
	
	def change_state(call):
		_LOGGER.info("hachina's change_state service is called")
		if hass.states.get(ENTITY_ID).state == '太棒了':
			hass.states.set(ENTITY_ID, '真好', attributes=attr)
		else:
			hass.states.set(ENTITY_ID, '太棒了', attributes=attr)
			
	hass.services.register(DOMAIN, 'change_state', change_state)
	return True
```

接下来看看读取配置文件的内容。

在Configuration.yml里，hachina下面加上属性：

```
hachina:
  name_tobe_displayed: 我的新名字
  slogon: 阳光照耀大地
```

修改hachina.py；

```
import logging
import voluptuous as vol
import homeassistant.helpers.config_validation as cv


DOMAIN = 'hachina'
ENTITY_ID = DOMAIN + ".hello_world"

CONF_NAME_TOBE_DISPLAYED = 'name_tobe_displayed'
CONF_SLOGON = 'slogon'

DEFAULT_SLOGON = '积木构建智慧空间'
_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema(
	{
		DOMAIN: vol.Schema(
			{
				vol.Required(CONF_NAME_TOBE_DISPLAYED): cv.string,
				vol.Optional(CONF_SLOGON, default=DEFAULT_SLOGON): cv.string
			}
		)
	},
	extra = vol.ALLOW_EXTRA
)

def setup(hass, config):
	conf = config[DOMAIN]
	friendly_name = conf.get(CONF_NAME_TOBE_DISPLAYED)
	slogon = conf.get(CONF_SLOGON)
	_LOGGER.info("get the config :{}, {}".format(friendly_name, slogon))
	attr = {
		"icon": "mdi: yin-yang",
		"friendly_name": friendly_name,
		"slogon": slogon
	}
	hass.states.set(ENTITY_ID, '太棒了', attributes=attr)
	return True
```



hachina也有自己的树莓派镜像。

我后续还是以这个为基础吧。



# hachina镜像

1、烧录。

就使用SD卡。我有一张32G的SD卡。不用U盘是因为我手里的U盘质量都不行。写文件多了就开始出问题。

2、登陆。

```
HAchina树莓派镜像预安装以下软件并设置自启动：

1、Home Assistant，8123端口,包含红点
2、Jupyter Notebook，8888端口
3、Mosquitto，端口1883
4、Samba
5、HADashboard，端口5050

账号名均为：pi
密码均为：hachina
```

3、有3个主要的服务。默认都是起来的。

分别是：home-assistant、jupyter-noetbook、appdaemon。对应下面的xxx。

有三种操作：restart、enable、disable。对应下面的yyy。

```
sudo systemctl yyy xxx@pi
```

4、先访问ip:8123。会提示你配置一些基本信息。

5、访问ip:5050。这个只有一个组件，显示时间的。

6、hachina还提供了一个外网访问的地址。

http://xat6wacozi.hachina.802154.com

虽然速度很慢，但是是可以通的。

我自己在阿里云服务器上搭建了一个frp反向代理，现在可以走自己的通路了。



现在自己一点点来添加。

先从Internet信息加起。

因为这个不需要任何硬件。

airvisual

这个是查看空气质量的。

https://www.airvisual.com/

创建一个key。

然后在configuration.yml里添加：

```
sensor:
  - platform: airvisual
    api_key: xxx
    monitored_conditions:
      - cn
    city: shenzhen
    state: guangdong
    country: china
```

然后重启hass就可以了。

这个看起来并不直观。尽量还是选择国内的相关服务。

使用京东万象云。

也是第一次接触京东云服务器。

通过对“京东万象”的开放气象API的调用，我们实现温度、湿度、PM2.5三个传感器设备。

这个需要另外写代码才能实现。

在~/.homeassistant/custom_components/sensor/hachina.py里。

```

```

然后在Configuration.yml里添加配置。

```

```

但是这个添加会失败。

```
2019-11-12 17:20:30 ERROR (MainThread) [homeassistant.config] Platform error: sensor
```

```
ModuleNotFoundError: No module named 'custom_components.hachina.sensor'; 'custom_components.hachina' is not a package
```

暂时跳过这个。

试一下和风天气的，也不行。

我直接放到/usr/local/lib/python3.7/dist-packages/homeassistant/components/sensor目录下也不行。



现在应该是自定义组件的写法跟现在的版本对不上了。

这里有一个演示。看看一个配置实用的是什么样子。

https://demo.home-assistant.io



看这篇文章，虽然没有出来，但是没报错。

https://www.hachina.io/15020.html

过了一天，再刷新试一下。

现在报错了。但是好歹不是找不到模块的错误了。

```
Error([('SSL routines', 'tls_process_server_certificate', 'certificate verify failed')])")))
```

那我就测试一下用python直接访问和风天气的，看看如何。

```
# -*- coding: utf-8 -*-
import urllib2,json

#调用和风天气的API city可以通过https://cdn.heweather.com/china-city-list.txt城市列表获取
url = 'https://free-api.heweather.com/v5/weather?city=CN101230201&key=8a439a7e0e034cdcb4122c918f55e5f3'
#用urllib2创建一个请求并得到返回结果
req = urllib2.Request(url)
resp = urllib2.urlopen(req).read()
# print resp
# print type(resp)

#将JSON转化为Python的数据结构
json_data = json.loads(resp)
city_data=json_data['HeWeather5'][0]
hourly_data= json_data['HeWeather5'][0]['hourly_forecast']
daily_data = json_data['HeWeather5'][0]['daily_forecast']
print json_data
print u'当前时间：' + daily_data[0]['date']
print u'城市：' + city_data['basic']['city']
print u'PM指数：' + city_data['aqi']['city']['pm25']
print u'白天天气：' + daily_data[0]['cond']['txt_d']
print u'夜间天气：' + daily_data[0]['cond']['txt_n']
print u'今天{0}: 气温：{1}°/{2}°'.format(str(daily_data[0]['date']),daily_data[0]['tmp']['min'],daily_data[0]['tmp']['max'])
print u'未来小时天气：{0} {1}'.format(str(hourly_data[0]['date']).split()[1],hourly_data[0]['cond']['txt'])
print u'未来小时天气：{0} {1}'.format(str(hourly_data[1]['date']).split()[1],hourly_data[1]['cond']['txt'])
print u'未来小时天气：{0} {1}'.format(str(hourly_data[2]['date']).split()[1],hourly_data[2]['cond']['txt'])
print u'未来{0} 天气：{1}°/{2}°'.format(daily_data[1]['date'],daily_data[1]['tmp']['min'],daily_data[1]['tmp']['max'])
print u'未来{0} 天气：{1}°/{2}°'.format(daily_data[2]['date'],daily_data[1]['tmp']['min'],daily_data[2]['tmp']['max'])
print u'穿衣建议：' + json_data['HeWeather5'][0]['suggestion']['drsg']['txt']

```

这个也会报ssl错误。网上找到需要加上这两行。

```
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
```

加上后的确ssl的错误没有了。

但是我给sensor.py加上这两行，还是一样的错误。



```
Unable to connect to HeWeather
```

正常应该是这么放的。所有后续信息的自定义组件，都拷贝这个来改就好了。其他的我试了都不行的。

```
pi@raspberrypi:~/homeassistant/custom_components/HeWeather$ tree
.
├── manifest.json
├── sensor.py
```

这样至少是可以加载运行的。只是目前json数据对不上，有错误。

```
Traceback (most recent call last):
  File "/home/pi/.homeassistant/custom_components/HeWeather/sensor.py", line 357, in update
    con = self.now()
  File "/home/pi/.homeassistant/custom_components/HeWeather/sensor.py", line 335, in now
    con = now_weather.json()
  File "/usr/local/lib/python3.7/dist-packages/requests/models.py", line 897, in json
    return complexjson.loads(self.text, **kwargs)
  File "/usr/lib/python3/dist-packages/simplejson/__init__.py", line 518, in loads
    return _default_decoder.decode(s)
  File "/usr/lib/python3/dist-packages/simplejson/decoder.py", line 370, in decode
    obj, end = self.raw_decode(s)
  File "/usr/lib/python3/dist-packages/simplejson/decoder.py", line 400, in raw_decode
    return self.scan_once(s, idx=_w(s, idx).end())
simplejson.errors.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

这里是因为采用了post请求，而且api网址也有变化。

要改成get请求。

虽然没有报错了。但是还是没有显示。

知道了。就是因为lovelace这个ui默认不会显示。切换到states ui就可以看到了。

把改后的内容，我自己上传到自己的github目录保存。



hachina提供了一个叫redpoint的配置界面，需要使用hachina的账号登陆。

这个可以直接通过界面来配置



```
ip摄像头
	验证正常。
	手机上安装对应的app。默认在8080端口。
owntracks
	这个需要谷歌服务才行。
	暂时不用了。

```



```
smtplib.SMTPNotSupportedError: STARTTLS extension not supported by server.
```



```
# How long we wait for the result of a service call
SERVICE_CALL_LIMIT = 10  # seconds
等待一个服务调用的时间，是10秒。

ENTITY_ID_PATTERN = re.compile(r"^(\w+)\.(\w+)$")
实体id的格式是xx.yy。只有一个点。

def valid_state(state: str) -> bool:
    """Test if a state is valid."""
    return len(state) < 256
state是否合法，就是看长度。


```





参考资料

1、

https://home-assistant.cc/installation/general/

2、pip install 卡住不动的解决方案

https://blog.csdn.net/weixin_41579863/article/details/81568060

3、树莓派安装 HomeAssistant

https://www.jianshu.com/p/8f77a3f46f4d

4、Installing Python 3.6.2 on raspberry pi (raspbian)

https://tutorials.technology/tutorials/67-Installing-python-36-on-raspberrypi.html