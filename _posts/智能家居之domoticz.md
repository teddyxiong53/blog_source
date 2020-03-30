---
title: 智能家居之domoticz
date: 2019-11-11 17:39:49
tags:
	- 智能家居

---

1

代码在这里：

https://github.com/domoticz/domoticz

domoticz是一个智能家居系统，用来监视和配置各种设备，包括灯、开关、传感器等。

通知可以发送到你的手机上。

支持多平台。

这个是用c++写的。所以非常轻量。

简单的逻辑可以用图形化编程做。

复杂的用lua脚本来写。



现在在B站看到“未脱发的程序员”这个up主使用domoticz搭建智能家居系统。就又产生了兴趣。

http://install.domoticz.cn/ 保存这个脚本到本地。稍微修改一下，因为这个实际上是针对debian系统的，里面有检查版本，我是在Ubuntu1604上安装。所以需要把检测条件屏蔽一下，另外还有libcurl4的改成libcurl3的。

这样就可以顺利安装。还有需要sudo权限来执行。

选择安装在~/domoticz目录。

```
HTTP:        172.16.2.168:8080  
HTPS:        172.16.2.168:8043  
```

后面发现https的改动没有生效。

在安装目录下，手动修改domoticz.sh文件，把443修改为8043，因为我的机器上安装了nginx和apache，避免端口冲突。

然后执行domoticz.sh脚本，就可以运行了。





参考资料

1、玩玩智能家居1：Domoticz

https://xujiwei.com/blog/2017/03/homeautomation-domoticz/

2、Domoticz 中添加彩云天气

https://www.cnblogs.com/HintLee/p/9557182.html

3、home assistant 和domoticz的优劣区别？

https://www.zhihu.com/question/265966977

4、系列文章

https://xujiwei.com/blog/tags/domoticz/