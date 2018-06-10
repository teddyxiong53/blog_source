---
title: HomeAssistant（1）
date: 2018-06-10 12:18:17
tags:
	- HomeAssistant
typora-root-url:..\
---



HomeAssistant是一个成熟完整的基于Python的智能家居系统。简称HA。

1、设备支持度高。

2、支持自动化。

3、支持群组化。

4、支持ui定制。

5、社区活跃。

6、可以跟HomeBridge这个平台打通连接。

整套系统的框架是这样的。

![](/images/HomeAssistant（1）-整体框架.png)





Homebridge本身可以接入部分原生不支持Apple HomeKit的设备。Homebridge简称为HB。

HA作为一个独立的平台，有能力集成大量量产或者DIY的智能家居设备，并且拥有独立的控制前端。

在层级上是跟Apple Home平台平起平坐的大boss。



#安装方法

HA支持大部分平台，包括docker，macos，linux、windows等。

只要支持Python的都可以。

下面以树莓派为例。

在树莓派上安装HA的方式有这么几种：

1、在Raspbian上自己手动安装软件。

2、安装集成了HA的Hassbian系统。

3、一个中文版的Mossbian系统。

4、基于docker的Hass.io。



第三种方法是最简单的，也最适合入门的中国用户。

我们先看看第三种方法。

Mossbian的镜像在这里。

https://pan.baidu.com/s/14eiAEr0odPKWDVjkhedG8Q#list/path=%2FMossbian

作者是http://cxlwill.cn

但是这个在我这里的安装不顺利。

我现在不知道作者设置的启动过程是怎样的。

安装软件也特别慢。

不知道作者说的第一次开机后的下载行为是哪里控制的。

反正我是没有看到有下载。

此路不通。

我看看hass.io的docker的方式。



算了。我还是采取手动安装的方式来做吧。



```
sudo apt install python3-pip
```

```
sudo python3 -m pip install homeassistant
```

```
sudo pip3 install homeassistant
```

看到报错。

```
homeassistant requires Python '>=3.5.3' but the running Python is 3.5.2
```

这个可以安装成功。

```
python3 -m pip install --user homeassistant
```

但是这样会报错。

```
sudo pip3 install homeassistant
```

打开。

```
hass --open-ui
```



# 设备接入

HA的配置系统非常混乱。

系统架构不清晰也是HA最大的缺点。

我们先看看HA的配置框架。

configuration.yaml是核心配置文件。

这里你可以配置时区、度量单位、开发者模式、主题选择等基础配置。

最重要的是，你在这个文件里完成所有设备的接入。

HA的运行基础是一个个相对独立的组件component。

例如，米家平台就可以看做一个component。



#参考资料

1、Home Assistant + 树莓派：强大的智能家居系统 · 安装篇

https://sspai.com/post/38849

2、Home Assistant + 树莓派：强大的智能家居系统 · 设备接入篇

https://sspai.com/post/40075

3、Home Assistant + 树莓派：强大的智能家居系统 · 小米篇

https://sspai.com/post/40113

中文论坛

https://bbs.hassbian.com/forum.php

打造属于自己的智能家居 篇二：智能中枢Hass.io ( Home-assistant ) 的基本部署与使用

https://post.smzdm.com/p/631892/

在Linux（树莓派）中安装Python3和HomeAssistant

https://www.hachina.io/docs/355.html