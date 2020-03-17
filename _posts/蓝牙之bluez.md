---
title: 蓝牙之bluez
date: 2018-05-31 21:51:28
tags:
	- 蓝牙

---

1

不用那么，现在buildroot里可以直接选择使用bluez，不存在什么需要自己移植的问题了。



bluetooothctl的入口代码是在bluez/client/main.c里。



bluez和bsa是2个蓝牙协议栈。

bluez5_utils-5.50/lib/.libs/libbluetooth.so

bluez5_utils就是bluez

得到的有库，也有工具。



bluez有这些工具。

```
bccmd
bluemoon
	这个是进行配置，例如重启蓝牙。复位这些。
bluetoothctl
	这个很强大。主要操作工具。
btattach
	这个也是修改配置。
btmon
	
ciptool
	这个是cmtp相关操作。
hciattach
	
hciconfig ：类似于ifconfig的操作。
hcidump
	这个也比较重要。调试时把数据打出来看。
hcitool
	这个也很强大。是主要的调试工具。
hcitop
	这个类似top的行为，显示当前的动态数据。
hex2hcd
	
l2ping
	这个就是ping操作。
l2test
	这个也很有用。
mpris-proxy
rctest
rfcomm
sdptool
```



# 参考资料

1、这篇不用看了。

https://blog.csdn.net/gatieme/article/details/48751743

2、蓝牙配置相关的文章

https://blog.csdn.net/morixinguan/article/details/79197455

3、蓝牙协议栈

https://en.wikipedia.org/wiki/Bluetooth_stack

4、用BlueZ A2DP Profile播放音乐

https://blog.csdn.net/bluebeach/article/details/5891035

5、详细的arm移植过程

https://www.cnblogs.com/dong1/p/8271385.html

6、linux bluez bluetooth工具命令使用

https://blog.csdn.net/songyulong8888/article/details/81489210