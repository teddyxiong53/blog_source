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

# 重新安装

前面的过程比较混乱。

我现在已经看过HomeAssistant的代码，其实就是一个Python写的应用。

文件较多，有1300个文件左右。

我直接在原始的树莓派系统上进行手动安装。

主要参考英文官网上的内容。

如何建立开发环境。

https://developers.home-assistant.io/docs/en/development_environment.html

1、从github上下载源代码。

https://github.com/home-assistant/home-assistant

2、建立Python3的环境。

```
sudo apt-get install python3-pip python3-dev python3-venv
```

我这些操作在我的虚拟机里没有问题。

但是在树莓派上有问题。

我还是先升级我的树莓派的Python3到3.6版本。

但是apt-get最多只能安装到3.4版本。

我选择下载Python3.6.5的，进行编译安装。

https://www.python.org/ftp/python/3.6.5/

3、安装一些依赖的内容。

```
 sudo apt-get install libssl-dev libxml2-dev libxslt1-dev libjpeg-dev libffi-dev libudev-dev zlib1g-dev
```

4、创建一个venv，为了避免破坏你的整体的环境。

```
pi@raspberrypi:~/work/hass/hass$ python3 -m venv .
pi@raspberrypi:~/work/hass/hass$ source bin/activate
(hass) pi@raspberrypi:~/work/hass/hass$ script/se
server  setup   
(hass) pi@raspberrypi:~/work/hass/hass$ script/se
server  setup   
(hass) pi@raspberrypi:~/work/hass/hass$ script/setup 
Installing test dependencies...
Collecting tox
下面是一些下载安装的过程。

```

5、运行。

```
hass
```

等一会儿，就可以在浏览器访问树莓派的网址，端口号是8123 。



报了一些错误。

```
2018-06-16 23:31:11 ERROR (Recorder) [homeassistant.components.recorder] Error during connection setup: No module named '_sqlite3' (retrying in 3 seconds)
2018-06-16 23:31:14 ERROR (Recorder) [homeassistant.components.recorder] Error during connection setup: No module named '_sqlite3' (retrying in 3 seconds)
2018-06-16 23:31:14 INFO (MainThread) [homeassistant.setup] Setup of domain recorder took 33.1 seconds.
2018-06-16 23:31:14 ERROR (MainThread) [homeassistant.setup] Setup failed for recorder: Component failed to initialize.
```



```
2018-06-16 23:31:14 INFO (MainThread) [homeassistant.core] Bus:Handling <Event service_executed[L]: service_call_id=1968945520-3>
2018-06-16 23:31:14 ERROR (MainThread) [homeassistant.setup] Unable to setup dependencies of history. Setup failed for dependencies: recorder
2018-06-16 23:31:14 ERROR (MainThread) [homeassistant.setup] Setup failed for history: Could not setup all dependencies.
```

Python3真的是各种问题都有。

网上看了不少的方法，都是要重新编译Python3.6的。

先安装sqlite的东西。

```
sudo apt-get install libsqlite3-dev
```

再重新配置Python3的。

```
./configure --enable-loadable-sqlite-extensions && make -j4 && sudo make install
```

可以先去忙别的了。

hass启动过程，也有一些安装，在树莓派上，这个过程显得更加长了。

不过还是成功了。



日志的格式分析。

```
2018-06-17 00:14:11 INFO (MainThread) [homeassistant.setup] Setting up discovery
```



# helloworld

先写一个helloworld程序接入到HA里。

1、在你的配置目录下，默认是/home/pi/.homeassistant。

新建一个名字叫custom_components的目录。

HA的api分为两种：异步的和同步的。

我们先看同步的。

2、我们在custom_components目录下，新建一个hello_world.py文件。

里面内容如下：

```
DOMAIN = "hello_world"

def setup(hass, config):
	hass.states.set('hello_world.Hello_World', 'Works')
	return True
```

3、在configuration.yaml文件里，加入：

```
# helloworld
hello_world:
```

然后停止hass服务，再启动。这次启动就很快了。

然后我们就可以看到这个了。

![](/images/HomeAssistant（1）-helloworld.png)



# hass

hass这个变量名在代码里随处可见。

hass这个变量可以用来访问整个系统。

hass

hass.config

hass.states

hass.bus

hass.services



# 事件

HA是事件驱动的。

HA的事件系统可伸缩性很强。

我们写一个hello_event.py。

```
DOMAIN = 'hello_event'

def setup(hass, config):
	hass.bus.fire('my_event', {
		'answer': 11
	})
```

上面这个是一个发送事件的例子。但是实际上我们更多地是监听事件。

```
DOMAIN = 'hello_event'

def setup(hass, config):
	count = 1
	def handle_event(event):
		nonlocal count
		count += 1
		print('total event get:', count)
		
	hass.bus.listen('my_event', handle_event)
```





加入雅虎天气的看看。

在configuration.yaml里加入：

```
weather:
  - platform: yweather
    woeid: 2151849
```



![](/images/HomeAssistant（1）-雅虎天气.png)





设备分类

一共分为39类。

例如，light（灯）就是一类。



配置为百度的tts。

```
tts:
  - platform: baidu
    app_id: 百度APPID
    api_key: 百度APIKEY
    secret_key: 百度SECRETKEY
    speed: 语速，取值0-9，默认为5中语速
    pitch: 音调，取值0-9，默认为5中语调
    volume: 音量，取值0-15，默认为5中音量
    person: 发音人选择, 0为女声，1为男声，3为情感合成-度逍遥，4为情感合成-度丫丫，默认为0
```

加入新的东西后，启动的安装总是比较慢的。



下面这些增加的内容，都是从https://www.home-assistant.io/components 这里看哪些我当前可以加的。

加入cpu的监控。

我这样写在configuration.yaml里。

```
sensor:
  - platform: yr
  - platform: cpuspeed
```

这个效果是把yr的给覆盖了。

![](/images/HomeAssistant（1）-cpu.png)



我再加上磁盘占用情况的。

```
sensor:
  - platform: yr
  - platform: cpuspeed
  - platform: systemmonitor
    resources:
     - type: disk_use_percent
       arg: /home
     - type: memory_free
```

这次，yr的也都出来了。

![](/images/HomeAssistant（1）-disk.png)

```
2018-06-17 11:44:47 INFO (SyncWorker_2) [homeassistant.util.package] Attempting install of psutil==5.4.5
```

现在为了每次测试重启的速度可以快一点，把一些不需要的东西都注释掉。

现在加入snmp的。

没有正常工作，先跳过。

```
2018-06-17 11:53:07 INFO (SyncWorker_3) [homeassistant.util.package] Attempting install of pysnmp==4.4.4
2018-06-17 11:53:16 WARNING (MainThread) [homeassistant.setup] Setup of config is taking over 10 seconds.
```

发现历史这个还是必须加上。

加入`openhardwaremonitor` ，发现这个是windows下才能用的。去掉。

加入weblink。

```
# weblink
weblink:
  entities:
  - name: Router
    url: http://192.168.0.1
    icon: mdi:router-wireless
  - name: Home Assistant
    url: https://www.home-assistant.io
```

作用就是在你的主页上产生2个超链接而已。

![](/images/HomeAssistant（1）-weblink.png)



加了上面这些模块，对这增加模块的流程也已经心里有数了。

看到说可以替换地图的。

我们看看怎么做。看到说明，还有点麻烦，我当前并不是很需要这个功能。先不做。

https://github.com/cxlwill/ha-inkwavemap



打开shopping_list。

这个是系统自动的模块。

只需要在configuration.yaml里加入：

```
shopping_list:
```

重启服务就好了。





一些HA相关的github库。

小米的，可以放到custom_components目录下的。

https://github.com/lazcad/homeassistant

这个是非常完备的配置文件。

https://github.com/geekofweek/homeassistant

配置文件。

https://github.com/ntalekt/homeassistant







# 设备接入

HA的配置系统非常混乱。

系统架构不清晰也是HA最大的缺点。

我们先看看HA的配置框架。

configuration.yaml是核心配置文件。

这里你可以配置时区、度量单位、开发者模式、主题选择等基础配置。

最重要的是，你在这个文件里完成所有设备的接入。

HA的运行基础是一个个相对独立的组件component。

例如，米家平台就可以看做一个component。

我们先随便接入一个设备作为示例。



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

no add-apt-repository command

https://blog.csdn.net/dearwind153/article/details/53086171

树莓派编译安装python3.6

https://www.jianshu.com/p/df1086337ee4

ModuleNotFoundError: No module named '_sqlite3'

https://github.com/sloria/TextBlob/issues/173

开发入门

https://developers.home-assistant.io/docs/en/dev_101_index.html

启动HomeAssistant

这个网站文档很好。

https://www.hachina.io/docs/1843.html

这个网站也很好。中文的。

https://home-assistant.cc/component/broadlink/