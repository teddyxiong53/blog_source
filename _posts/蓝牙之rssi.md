---
title: 蓝牙之rssi
date: 2018-12-20 11:43:35
tags:
	- 蓝牙
---



什么是rssi？

接收信号强度Received Signal Strength Indicator。

rssi = 10 log P。

P表示功率。

```
[例1] 如果发射功率P为1mw，折算为dBm后为0dBm。
[例2] 对于40W的功率，按dBm单位进行折算后的值应为：
10lg（40W/1mw)=10lg（40000）=10lg4+10lg10+10lg1000=46dBm。
```

Rssi和接收功率有关，单位是dBm，一般为负值，反应的是信号的衰减程度，理想状态下（无衰减），Rssi = 0dBm，实际情况是，即使蓝牙设备挨得非常近，Rssi也只有-50dBm的强度，在传输过程中，不可避免要损耗。
一般情况下，经典蓝牙强度 
-50 ~ 0dBm 信号强
-70 ~-50dBm信号中
<-70dBm      信号弱

低功耗蓝牙分四级
-60 ~ 0   4
-70 ~ -60 3
-80 ~ -70 2
-80 1



1、Android 蓝牙强度Rssi

https://blog.csdn.net/jasonwang18/article/details/73131020