---
title: Android之nearby功能
date: 2021-01-22 14:43:11
tags:
	- Android

---

--

官网：

https://developers.google.com/nearby

nearby平台可以让你发现附近的设备并跟它建立连接。

使用的技术可以是：蓝牙、wifi、ip、audio。

nearby连接 api

nearby消息api

fast pair



我现在关注fast pair。

GFPS服务：Google Fast Pair Service。

使用ble来发现附近的蓝牙设备。这样功耗就非常低。

在设备靠近的时候，进行弹窗提示。

主要应用就是耳机的自动连接。

1、当设备处于配对模式是，手机显示一个通知initial pairing通知。

2、initial Pairing配对完成后，把设备关联到用户的谷歌账号。

3、当耳机开机后，靠近另外一台手机的是，显示一个subsequent pairing 通知，用户不需要手动让耳机再进入到配对模式。

4、给设备命名。

5、当设备固件有更新的时候，显示一个信息。



需要蓝牙4.2以后的。

字节序的大端的。



这个功能可以理解为一个蓝牙profile。

定义了2个角色：

seeker和provider。

seeker就是手机。

provider就是耳机。

provider就是在广播它的出现和就绪状态。

seeker使用GAP central role。

provider使用GAP 外设role。



为了加快设备发现，provider应该广播一个消息，消息的内容是对GFPS的支持。

seeker则是周期性地扫描。



provider的注册

耳机厂家应该在谷歌网站上进行注册。

谷歌会给产品分配一个model ID和一个防止嗅探的私钥。

在注册的时候提供的信息，会在弹窗时进行显示。



provider还应该用一个比较低的发送功率进行广播。

避免出现广播爆炸。

但是，发射功率还要足够大，让1米外的任何手机都可以收到。

为了得到这个合适的发射功率。

seeker必须知道provider的发送功率是多少。

功率用dBm来做单位衡量。

最后的测量方式是，把一个安卓手机放到1米外，然后加41dBm（？？这个怎么理解？）

那么41dBm就是在1米的平均功率衰减。



这个测量值，应该通过下面的2种方法之一来发送出来：

1、在广播里发出来。

2、在谷歌网站注册网站的时候填写。



# 广播：在discoverable时

广播间隔

间隔不要大于100ms。这样可以让发现设备更快。

广播的数据

model id是一个24bit的数据，就是3个字节。

# 广播：在非discoverable时

也就是在非配对模式的时候，

耳机设备应该广播fast pair的账号数据。

这样附近的手机，就可以找出属于同一个账号的耳机。

不需要手动让耳机进行配对模式。这个是一个用户痛点。

这个的广播间隔最大是250ms。

广播的数据，

```
字节0：flags。当前为0x00，保留。
后面的就是账号信息数据。
包括：
字节0：高4位，Account key filter的长度。低4位：类型（0000：显示ui，0010：隐藏ui）
然后就是account key filter。长度可变。1到15个字节。
然后又是一个字节，长度+类型的。长度为1，类型0001，表示salt。
然后是一个字节的salt。
```

account key filter。

账号key过滤器。是指什么？

简单可以认为是用户各个账号的hash值吧。



gatt的uuid是0xfe2c。

特征值有4个：

```
model id： 只读。uuid是1233
key-based Pairing：写和通知。uuid是1234
passkey： 写和通知。uuid是1235
account key：只写。uuid是1236
```

标准的特征值：

```
固件版本，只读，uuid是2a26
```

mtu，如果可以，用83字节，默认是23字节。







参考资料

1、

