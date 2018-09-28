---
title: avs（2）
date: 2018-08-24 15:22:35
tags:
	- 音箱

---



AudioPlayer的焦点管理。



DirectiveRouter

指令路由。



里面的缩写解释：

1、ACL。Alexa通信库。完成各种网络通信的。

2、ADSL。Alexa指令排序库。管理每个指令的生命周期。

3、AFML。Activity焦点管理库。焦点是基于频道的。

4、AIP。音频输入处理。

5、ASP。音频信号处理。

6、SDS。共享数据流。

7、WWE。唤醒词引擎。

8、CA。能力代理。

其中唤醒词和ASP的库的方式提供，其余都是源代码方式提供。

这些缩写也对应了AVS系统里的主要模块。数据流转的过程是这样的。

其他缩写：

CBL：Code Based Link。在授权这里用。



代码目录结构：



AuthObserverInterface

授权观察者。



handleAuthorizationFlow

这个是授权状态机处理。



编译过程分析



在Ubuntu上运行avs。

前提：

1、Ubuntu是16.04的。

2、有Mic和音箱。



你需要先在Amazon上注册一个开发者账号。

然后创建一个Alexa设备，编辑security profile。

把product id和client id要复制保存下来，后面有用。



这个是一个较老的sample。提供比较完整。不过现在转成维护的了。

https://github.com/amzn/alexa-avs-raspberry-pi/archive/master.zip



avs的命名空间分析。

https://alexa.github.io/avs-device-sdk/namespaces.html

这里有说明。

```
最外层就是AlexaClientSDK。
命名空间跟目录层次是一样的。

```



# 参考资料

1、android音乐播放器的音频焦点控制

https://blog.csdn.net/weijun421122/article/details/44937259

2、Amazon 智能音箱 AVS Device SDK 架构详解 （智能音箱的通用架构）

https://www.wandianshenme.com/play/avs-device-sdk-architecture-overview/