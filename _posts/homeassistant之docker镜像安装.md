---
title: homeassistant之docker镜像安装
date: 2019-01-14 16:44:59
tags:
	- homeassistant
---



homeassistant对python版本有要求，所以安装起来也是比较麻烦。

docker就是为了解决环境问题而存在的。

所以docker是解决这个问题的很好的方案。

安装docker。

```
curl -sSL https://get.docker.com | sh
```

下载对应的镜像。要配置国内加速docker。

```
mkdir /home/pi/hass/config -p

sudo docker run -d --name="home-assistant" -v /home/pi/hass/config:/config -v /etc/localtime:/etc/localtime:ro --net=host homeassistant/raspberrypi3-homeassistant:0.72.0
```

运行：

```
sudo docker run -v /home/pi/hass/config:/config homeassistant/raspberrypi3-homeassistant:0.72.0
```

然后在pc上访问地址：

```
http://192.168.0.100:8123
```

配置文件在/home/pi/hass/config目录下，可以修改这些yml文件。



我还是觉得homeassistant这个系统没有实用价值。



参考资料

1、Installation Home Assistant on Docker

https://www.cnblogs.com/dream-2017/p/9497497.html