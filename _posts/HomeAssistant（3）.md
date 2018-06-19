---
title: HomeAssistant（3）
date: 2018-06-18 20:18:44
tags:
	- HomeAssistant

---



现在开始看代码。

入口代码流程已经看懂了。

现在看一个组件的，就以天气的为例。

我之前有把yweather插件的弄出效果来。

这个是简单的一个组件。

所有相关的代码都在这里。

```
pi@raspberrypi:~/work/hass/hass/homeassistant/components/weather$ tree
.
├── bom.py
├── buienradar.py
├── darksky.py
├── demo.py
├── ecobee.py
├── __init__.py
├── metoffice.py
├── openweathermap.py
├── yweather.py
└── zamg.py
```

我们从yweather.py开始看。

`__init__.py`是入口。



```
core.py

HomeAssistant
EventBus
Event

State
ServiceRegistry

StateMachine
Config
CoreState
```

