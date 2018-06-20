---
title: HomeAssistant（4）斐讯插座接入
date: 2018-06-20 21:06:56
tags:
	- HomeAssistant
typora-root-url:..\
---



搭建了HA，但是没有只能音箱可以接入的，看到斐讯的有个插座可以接入，就买了，反正是零元购。



参考https://bbs.hassbian.com/forum.php?mod=viewthread&tid=2612&highlight=%E6%96%90%E8%AE%AF

这篇文章做。

做完后，我的目录情况。

```
pi@raspberrypi:~/.homeassistant$ tree
.
├── automations.yaml
├── config
│   └── phicomm_token.txt
├── configuration.yaml
├── custom_components
│   ├── hello_event.py
│   ├── hello_world.py
│   ├── __pycache__
│   │   └── hello_world.cpython-36.pyc
│   ├── sensor
│   │   ├── heweather_hourlyforecast.py
│   │   ├── heweather.py
│   │   ├── lifesuggestion.py
│   │   ├── PhicommTokenGetter.py：增加这个文件。
│   │   └── __pycache__
│   │       └── PhicommTokenGetter.cpython-36.pyc
│   ├── switch
│   │   ├── PhicommDC1.py
│   │   └── __pycache__
│   │       └── PhicommDC1.cpython-36.pyc
│   └── weather
│       └── heweather_forecast.py
├── customize.yaml
├── deps
├── groups.yaml
├── home-assistant.log
├── home-assistant_v2.db
├── packages ：增加这个目录。
│   ├── phicomm_dc1.yaml
│   └── phicomm_token.yaml
├── scripts.yaml
├── secrets.yaml
└── tts
```

phicomm_dc1.yaml

这个文件里改mac地址。

phicomm_token.yaml

这个文件里，把用户账号和密码改成你自己的。

configuration.yaml

这个里面加入：

```
homeassistant:
  # Name of the location where Home Assistant is running
  name: Home
  # Location required to calculate the time the sun rises and sets
  latitude: 39.9289
  longitude: 116.3883
  # Impacts weather/sunrise data (altitude above sea level in meters)
  elevation: 0
  # metric for Metric, imperial for Imperial
  unit_system: metric
  # Pick yours from here: http://en.wikipedia.org/wiki/List_of_tz_database_time_zones
  time_zone: Asia/Shanghai
  # Customization file
  customize: !include customize.yaml
  packages: !include_dir_named packages #就加了这一行，要加在HomeAssistant这个下面。
```

另外出现tokenPath: '/config/phicomm_token.txt'这个的地方，我都统一改成：

```
tokenPath: '/home/pi/.homeassistant/config/phicomm_token.txt'
```





```
2018-06-20 21:25:20 ERROR (MainThread) [homeassistant.helpers.entity] Update for switch.dc1 fails
```

```
FileNotFoundError: [Errno 2] No such file or directory: '/config/phicomm_token.txt'
```



运行效果：

![](/images/HomeAssistant（4）-运行效果.png)





# 代码分析

数据的流转是：

访问了斐讯的服务器上的信息的。

服务器是搭建在tomcat上的。所以规模应该不是很大。

搭建也不是很完善。

https://smartplug.phicomm.com/

