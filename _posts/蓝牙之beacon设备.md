---
title: 蓝牙之beacon设备
date: 2019-03-29 14:35:32
tags:
	- 蓝牙

---



beacon这个单词的字面含义是浮标。蓝牙beacon的中文翻译是蓝牙信标。



beacon设备一般是放在室内的固定位置。被设置成广播模式。

上电后就进行广播。不能和任何ble主机通信。

需要手机app支持。

近场感知。



一个应用场景是这样：

一个顾客安装了商场的app，商家在数码专柜的角度部署了一个蓝牙beacon。

当顾客靠近这个地方时，app在后台检查到举例beacon不到5米。

这时候，app弹窗提示相关产品的信息。

这个其实在博物馆里更加适合这个应用。



beacon可以做什么？

1、室内导航。

2、移动支付。景点门票支付。

3、店内导购。

4、人流分析。

公交站可以发送车辆信息。



我们可以理解为省去了用户扫描二维码的这个过程。

 

beacon这个技术，还是苹果率先使用的。苹果是iBeacon。

然后谷歌在2015年推出了Eddystone。



ibeacon发送的是uuid，而且只能发送uuid。

uuid的确定是它总是和app绑定的。

每一种信标都需要一个专门的app才能发挥作用。

EddyStone为了解决这个问题，使用了URL。

URL可以理解为信标的二维码版本。





参考资料

1、

https://zhuanlan.zhihu.com/p/39059144

2、Beacon设备定位是怎么实现的？

https://zhuanlan.zhihu.com/p/47466321

3、Beacon技术：室内交互的新浪潮

https://www.leiphone.com/news/201406/d-ibeacon.html

4、Eddystone 和 iBeacon 到底有什么区别？

https://www.zhihu.com/question/32708729