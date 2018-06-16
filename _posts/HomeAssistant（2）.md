---
title: HomeAssistant（2）
date: 2018-06-15 23:16:42
tags:
	- HomeAssistant

---



https://www.home-assistant.io/demo/



hass.io是一站式的解决方案，把你的树莓派3B变成家庭控制中心。







搭建开发环境

1、安装Python3 。

还是要保证升级到Python3.6版本先。

```
sudo apt-get install python3-pip python3-dev python3-venv
sudo apt-get install libssl-dev libxml2-dev libxslt1-dev libjpeg-dev libffi-dev libudev-dev zlib1g-dev
```

进入到HomeAssistant目录下。

```
python3 -m venv .
source bin/activate
script/setup
```

输入hass命令。触发安装。

```
(home-assistant-dev) hlxiong@hlxiong-VirtualBox:~/work/study/home-assistant-dev$ hass
Unable to find configuration. Creating default one in /home/hlxiong/.homeassistant
```

等几分钟。可以看到8123有程序用了的时候，就可以从网页访问到了。

```
hlxiong@hlxiong-VirtualBox:~$ sudo netstat -apn | grep 8123
tcp        0      0 0.0.0.0:8123            0.0.0.0:*               LISTEN      10250/python3   
```

http://192.168.56.101:8123/config/cloud/register

