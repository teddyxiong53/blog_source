---
title: 蓝牙之ble测试环境搭建
date: 2021-02-27 13:59:30
tags:
- 蓝牙
---

--

笔记本电脑：运行Ubuntu16.04，一个usb蓝牙适配器。

华为手机：安装nrf connect软件。

nrf点击菜单 - configure gatt server。选择sample configuration。这样手机就启动了一个简单的gatt server。

这个server的服务有：

```
heart rate服务
	uuid是：0x180d
一个禁用的服务
	uuid是128为的。随便写的。
test service
	uuid也是128位的。随便写的。
user data	
	uuid是0x181c。
```

点击test service这一个服务的编辑按钮。可以看到可以编辑的不多，就名字和uuid可以修改。

选择add service。添加一个link loss服务（就是服务下拉列表的第二项，具体指什么还不清楚）。

这个的uuid是0x1803，是一个标准服务。

gatt server准备好了。

现在 看看电脑这边如何操作测试。

首先是扫描，然后连接。

```
hcitool lescan
```



# nrf connect

nrf connect是一个帮助你扫描，发现，调试ble设备的app。

这个工具是开源的。

当前版本是4.10.0

分为这么几个部分：

scanner

在app界面上是一个tab页。

这个页面列出的是可以扫描到附近的在进行广播的ble设备。

你可以对设备进行过滤，可以选项可以是名字或者蓝牙地址。你可以是你收藏的设备。

还可以通过rssi信号强度来进行过滤。

还可以通过广播数据进行过滤。

在设备上点击，可以查看设备的广播里的详细信息。

可以点击connect按钮对选择的设备进行ble连接。

还可以查看rssi信号图。

bonded

这个标签页列出的是所有绑定的设备，它们当前没有在进行广播，或者已经跟其他设备连接了。

advertiser

这个标签页允许你定制广播包（如果你的设备支持peripheral role的话）

通过开关打开或者关闭广播。

gatt server

这个在菜单里。你可以把手机配置为一个gatt server。配置可以通过xml文件进行导出和导入。

connected



我的手机蓝牙地址：

```
0C:83:9A:5D:7D:6E
```





发现电脑这边用hcitool lescan，扫描打印一直不停。

而且还扫描不到我手机的广播。

可以扫描到这个

```
71:38:F7:4D:3A:15 HONOR V30 PRO
```

用gatttool交互连接这个设备。

```
gatttool -b 71:38:F7:4D:3A:15 -I
```

可以连上

```
root@thinkpad:~# gatttool -b 71:38:F7:4D:3A:15 -I
[71:38:F7:4D:3A:15][LE]> help
help                                           Show this help
exit                                           Exit interactive mode
quit                                           Exit interactive mode
connect         [address [address type]]       Connect to a remote device
disconnect                                     Disconnect from a remote device
primary         [UUID]                         Primary Service Discovery
included        [start hnd [end hnd]]          Find Included Services
characteristics [start hnd [end hnd [UUID]]]   Characteristics Discovery
char-desc       [start hnd] [end hnd]          Characteristics Descriptor Discovery
char-read-hnd   <handle>                       Characteristics Value/Descriptor Read by handle
char-read-uuid  <UUID> [start hnd] [end hnd]   Characteristics Value/Descriptor Read by UUID
char-write-req  <handle> <new value>           Characteristic Value Write (Write Request)
char-write-cmd  <handle> <new value>           Characteristic Value Write (No response)
sec-level       [low | medium | high]          Set security level. Default: low
mtu             <value>                        Exchange MTU for GATT/ATT
```

这个不算是连上。



疑问：

ble连接需要一直保持吗？



参考资料

1、[BlueZ] 2、使用bluetoothctl搜索、连接、配对、读写、使能notify蓝牙低功耗设备

https://www.cnblogs.com/zjutlitao/p/9589661.html