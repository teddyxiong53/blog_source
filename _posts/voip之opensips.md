---
title: voip之opensips
date: 2022-10-27 16:14:33
tags:
	- voip

---

--

opensips是一个voip服务端软件。

代码在这里：

https://github.com/OpenSIPS/opensips

官网：

https://opensips.org/

这个公司在维护。

http://www.opensips-solutions.com/

最近还一直在活跃提交代码。



# 配合linphone梳理voip通信的全链路





Sip服务器搭建全过程(Linphone拨号)

https://blog.csdn.net/qq_38631503/article/details/80005454



# opensips代码分析

OpenSIPS是一个成熟的开源SIP服务器，

除了提供基本的SIP代理及SIP路由功能外，

还提供了一些应用级的功能。

OpenSIPS的结构非常灵活，

**其核心路由功能完全通过脚本来实现，**

可灵活定制各种路由策略，

可灵活应用于语音、视频通信、IM以及Presence等多种应用。

同时OpenSIPS性能上是目前最快的SIP服务器之一，**可用于电信级产品构建。**



opensips自带的脚本文件功能太少，

可参考开源项目kamailio中的kamailio.cfg脚本文件。

kamailio和opensips的前身都是openser,

它们的脚本文件也是大同小异，但kamailio.cfg要更详细些。

我根据kamailio.cfg配置的opensips至今都运行良好。





https://blog.csdn.net/slow_is_beautiful/article/details/5931231



# 参考资料

1、

https://blog.csdn.net/yuanchunsi/article/details/79745619