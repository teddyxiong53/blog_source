---
title: Android之功耗分析及优化
date: 2018-04-08 14:13:13
tags:
	- Android
	- 优化

---



# 底电流调试

底电流是在飞行模式下，手机的基本耗电情况。

一般的底电流参考数据是 ：

```
512M RAM < 1.5mA
1G < 2mA
2G < 2.6mA
```

开启飞行模式，可以基本避免蓝牙、wifi、nfc、网络、fm等的影响。

关闭GPS，排除gps对底电流的影响。

关闭自动旋转屏幕，排除Sensor的影响。

关闭自动亮度调节，排除光线传感器的影响。

关闭其他传感器。

编译内核进行的时候，使用perf_defconfig配置。



尽量把应用都删掉。

手动移除可以移除的外设。

配置不用的gpio。

# 待机电流优化



# 其他优化措施

1、cpu/gpu动态调频。

2、



# 参考资料

1、android 功耗分析方法和优化

https://blog.csdn.net/feitian_666/article/details/51780946