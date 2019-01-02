---
title: mac之搭建hackintosh
date: 2018-11-01 19:45:01
tags:
	- mac

---



想体验一下mac系统，但是不打算买苹果，太贵。

打算自己配置一台黑苹果。

我也不打算很折腾，找到一套可行的便宜方案就行了。

tonymacx86是一个很权威的网站。



有个华擎的小机器，可以装mac，价格还挺便宜的。

可以研究一下。

deskmini310 这个，看看多少钱。

1000块。京东价格。

https://item.jd.com/8790405.html#crumb-wrap

是Intel的310芯片组。

这个里面有什么？

```
支持1151脚的cpu，intel第8代的core系列都可以。
最大支持32G内存。
```



需要自己配的东西：

```
1、cpu。cpu i3 8100散。6100也可以。
2、内存。选便宜的。8G。
3、硬盘。小的便宜的。
4、散热器。
5、无线。
```

6100和8100的对比。6100功耗低一些。便宜一些。

http://detail.zol.com.cn/pk/1136272_1179798.shtml



i3 8100参数

```
65W
6核心。
3.6GHz
14nm制程。
coffee lake
```



cpu这里，680元。盒装的是900元。

https://item.taobao.com/item.htm?spm=a230r.1.14.11.92eb71e2o7hW45&id=562919631849&ns=1&abbucket=11



网友的一个配置。

```
Deskmini + i3-6100 + 8G DDR4 + 120G SSD + 散热器 + 垃圾 WIFI-300M
1000 + 650 + 400 + 300 + 100 + 50 = 2500

CPU 、内存和 SSD 如果用二手的，还能再少 300 。然而何必呢？
```



这里有好的资料。

https://github.com/mygoare/Hackintosh



这里有卖整套方案的。

https://tieba.baidu.com/p/5815700473?red_tag=2771802704

tonymac上的方案。

https://www.tonymacx86.com/threads/asrock-deskmini-310-com-issue.254724/



这份pdf。是deskmini 110的黑苹果教程。我可以把这篇翻译一下。

https://www.tonymacx86.com/attachments/asrock-110m-deskmini-hackintosh-guide-pdf.249990/



deskmini  110和 310区别

```
我看110的价格还贵些。
```



占美工控机。可以了解一下。



deskmini只支持ddr4 。

频率2133或者2400 。

官方店：

https://detail.tmall.com/item.htm?id=566365521873

不过这个店没有卖出什么。不知道是为什么。

京东上卖得多一些。

价格是899元。

H110的主板，价格在430元左右。



这篇文章讲了110和310的区别。

http://www.dnpz.net/diannaoyingjian/diannaoyingjianpingce/2957.html

110属于上一代的芯片组，用来搭配Intel六代和七代CPU，而310可以搭配八代CPU。

110的制程是22nm，310的是14nm。制程影响的是功耗。

310集成了无线网卡mac模块。

其余没有什么大的区别。

```
八代i3推荐用H310主板，八代i5用B360主板，八代i7用Z370主板。
```



就参考这个来做了。

https://www.chenweikang.top/?p=613

配置这样：

```
deskmini 310
	这个哪里买？
	京东1000元。
	淘宝也是这个价格。
CPU用i3 8100
	京东要899 。贵了。
	不过带风扇。
	不带风扇要多少？
	散片是681元。风扇要多少？
内存：
	8G 2400，威刚的，355。
	淘宝的。
硬盘
	金百达。120G。118元。京东。
```

这里有装机视频。

https://www.bilibili.com/video/av36146274/

我现在比较担心的就是，不同地方的买的东西，怎么确认哪个的问题？

能不能把黑苹果搞起来？

冷处理几天吧。多考虑一下。





# 参考资料

1、现阶段最便宜的完美黑苹果配置？

https://www.zhihu.com/question/35340215

2、UniBeast: Install OS X El Capitan on Any Supported Intel-based PC

https://link.zhihu.com/?target=http%3A//www.tonymacx86.com/el-capitan-desktop-guides/172672-unibeast-install-os-x-el-capitan-any-supported-intel-based-pc.html

3、小白的第一次装机——华擎deskmini310准系统&尝试黑苹果

https://post.smzdm.com/p/725822/

4、Broadcom BCM94352z/DW1560驱动新姿势[新方法]

https://blog.daliansky.net/Broadcom-BCM94352z-DW1560-drive-new-posture.html

5、当ASRock 华擎 Deskmini 110 STX 遇到Intel 英特尔 i3 8100

https://post.smzdm.com/p/655515/

6、

https://zhuanlan.zhihu.com/p/34724030

7、DESKMINI 走心评测之CPU导向篇：110/310如何选？谁是性价比之王

https://www.chiphell.com/thread-1918559-1-1.html

8、

https://github.com/damnnfo/DeskMini-110-COM

9、 黑苹果主机 — ASRock 华擎 DeskMini 110/COM 平台组机

这个比较详细，时间是2017年底。

https://post.smzdm.com/p/584100/

10、家用 Linux server，有啥推荐没有呢？

http://cn.v2ex.com/t/469383?p=1