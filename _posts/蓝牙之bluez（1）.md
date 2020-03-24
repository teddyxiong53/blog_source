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



在Ubuntu上，使用的蓝牙协议栈是bluez。在Android上，用的是bluedroid。

使用bluez的时候，需要内核提供一系列的socket接口来操作蓝牙。

内核里的蓝牙框架如下图所示：

![内核蓝牙框架](../images/random_name/20160804195414943)



内核里的蓝牙框架，总体上可以分为2个部分：

1、蓝牙socket。

2、蓝牙驱动。

蓝牙socket是负责给bluez提供socket。并包含L2CAP层功能。

蓝牙驱动层包含：hci层协议，蓝牙硬件接口管理。

这2层的分割线就是：hci_core（图中黄色部分）。

针对bluez移植蓝牙，需要关注的就是2点：

1、蓝牙驱动。

2、bluze工具集里的hicattach这个工具。使用uart接口的蓝牙才需要。usb方式的，会自动枚举。



bluez和bluedroid的不同就是：

在bluez里，hci和L2CAP	都是在内核里。

而在bluedroid里，HCI 和L2CAP，都是内核之上了。



在蓝牙的电源控制方面，Ubuntu及debian系统都没有做很好的处理，从现在的蓝牙图形界面应用看，这两个系统中，默认蓝牙是一直有电的并且开机时就打开，并没有考虑关闭蓝牙的时候把蓝牙断电。



在Ubuntu笔记本上再次走了一般蓝牙连接的流程。碰到的问题跟之前在树莓派上碰到的问题都一样。

也按照一样的方法解决了。



```
teddy@thinkpad:~/work2/aosp$ sudo cat /var/log/syslog | grep -i protocol 
Mar 20 15:05:12 thinkpad kernel: [98813.756185] NET: Registered protocol family 31
Mar 20 15:05:43 thinkpad kernel: [98844.360067] Bluetooth: BNEP filters: protocol multicast
Mar 20 15:41:05 thinkpad bluetoothd[13253]: a2dp-source profile connect failed for B4:0B:44:F4:16:8D: Protocol not available
Mar 20 15:41:33 thinkpad bluetoothd[13253]: a2dp-source profile connect failed for B4:0B:44:F4:16:8D: Protocol not available
```

现在手机连上笔记本，笔记本相当于一个蓝牙音箱。

手机上播放音乐，声音从笔记本这边出来。



在Ubuntu上，直接用wireshark来抓包。



bluez提供的是协议栈。相当于tcpip协议栈。

bluez-utils相当于ping、arp这些工具。



怎么用Ubuntu来连接手机模拟的ble服务呢？

```
timeout -s SIGINT 5s hcitool -i hci0 lescan --passive
```

现在扫描出来有非常多，我随便选择一个：

```
gatttool -i hci0 -b 53:E3:74:F6:6B:8A -I 
```

会进入一个这样的提示符：

```
[53:E3:74:F6:6B:8A][LE]> 
```

但是实际上没有连接上：

```
[53:E3:74:F6:6B:8A][LE]> included
Command Failed: Disconnected
```



找到一份Ubuntu官方的说明。

整体流程是这样：

1、打开bluetoothctl。连接上目标设备。

2、连接成功后，会自动打印出目标设备的可以访问的服务。

```
[CHG] Device 5C:31:3E:71:0C:E7 UUIDs: 0d27ffc0-f0d4-469d-afd3-605a6ebbdb13
[NEW] Service /org/bluez/hci0/dev_5C_31_3E_71_0C_E7/service0010 Vendor specific (Primary)
[NEW] Characteristic /org/bluez/hci0/dev_5C_31_3E_71_0C_E7/service0010/char0011 Vendor specific
[NEW] Characteristic /org/bluez/hci0/dev_5C_31_3E_71_0C_E7/service0010/char0013 Vendor specific
```

但是我当前的问题，找不到Service这种。

3、如果找到。select一下属性。

```
select-attribute /org/bluez/hci0/dev_5C_31_3E_71_0C_E7/service0029/char002a
```

4、执行read操作。

```
[X4-LIFE Xmarty 2.0:/service0029/char002a]# read
Attempting to read /org/bluez/hci0/dev_5C_31_3E_71_0C_E7/service0029/char002a
[CHG] Attribute /org/bluez/hci0/dev_5C_31_3E_71_0C_E7/service0029/char002a Value: 0x49
  49
```

5、也可以打开通知，这样属性变化的时候，自动会通知过来。

```
notify on
```



bluez的版本之间不兼容。
版本5的和之前的版本就不兼容了。这个导致了很多工具在版本5上没法用了。
文档也很少。
主要的文档就是源代码目录下的txt文档。

使用了标准的dbus接口。你可以使用任何支持dbus接口的语言来进行bluez编程。

但是bluez的dbus，少了很多的东西。

bluez允许你：

1、查找出所有的蓝牙适配器，并单独对它们进行控制。

2、扫描设备，进行connect、pair、bond查找。

3、但是不能访问服务和特征值



如果你看完bluez的doc目录下的txt文档，还不知道怎么动手。

那么你可以看一下test目录下的python写的例子。



bluez更新节奏非常快，差不多每个月都会release版本。

所有有些人就开始寻找其他的库，例如在nodejs里，非常受欢迎的是noble（这个是用于中心节点）和bleno（这个用于外设节点）这2个库。



# bluez test例子

我直接把bluez的代码下的test目录拷贝到Ubuntu笔记本里。

里面有这些文件。

```
├── bluezutils.py
├── bluezutils.pyc
├── dbusdef.py
├── example-advertisement
├── example-gatt-client
├── example-gatt-server
├── ftp-client
├── list-devices
├── map-client
├── monitor-bluetooth
├── opp-client
├── pbap-client
├── sap_client.py
├── service-did.xml
├── service-ftp.xml
├── service-opp.xml
├── service-record.dtd
├── service-spp.xml
├── simple-agent
├── simple-endpoint
├── simple-player
├── test-adapter
├── test-device
├── test-discovery
├── test-gatt-profile
├── test-health
├── test-health-sink
├── test-hfp
├── test-manager
├── test-nap
├── test-network
├── test-profile
└── test-sap-server
```

## test-device

我看test-device这个比较基础。先使用一下。

```
teddy@thinkpad:~/work/bluetooth/test$ ./test-device 
Usage: ./test-device <command>

  list
  create <address>
  remove <address|path>
  connect <address> [profile]
  disconnect <address> [profile]
  class <address>
  name <address>
  alias <address> [alias]
  trusted <address> [yes/no]
  blocked <address> [yes/no]
```

还比较友好。

直接`./test-device list`。列出的这2个，是我Ubuntu蓝牙连接过的设备。

```
18:F0:E4:E9:B6:56 小米手机
B4:0B:44:F4:16:8D Teddy
```

直接连接后面的Teddy这个。

```
./test-device connect B4:0B:44:F4:16:8D
```

可以连接成功。

查看class

```
./test-device class B4:0B:44:F4:16:8D
0x5a020c
```

用了这么几条命令，知道这个test-device的功能了。

现在我们看看代码，是怎么实现这些功能的。

使用的工具包有：

```
import dbus
import dbus.mainloop.glib
import bluezutils
```

代码都是很直白的，最直观的方式实现功能，一点弯都没有转。

逻辑都是bluezutils这个库里实现的。

但是这个bluezutils.py就在当前目录下，这个就是包装了一些dbus操作。

## test-adapter

这个就是对本机的蓝牙进行操作。

```
teddy@thinkpad:~/work/bluetooth/test$ ./test-adapter address
00:1A:7D:DA:71:13
```

```
teddy@thinkpad:~/work/bluetooth/test$ ./test-adapter list
 [ /org/bluez/hci0 ]
    Name = thinkpad
    Powered = 1
    Modalias = usb:v1D6Bp0246d0525
    DiscoverableTimeout = 180
    Alias = thinkpad
    PairableTimeout = 0
    Discoverable = 0
    Address = 00:1A:7D:DA:71:13
    Discovering = 0
    Pairable = 1
    Class = 0x0c010c
    UUIDs = dbus.Array([dbus.String(u'00001112-0000-1000-8000-00805f9b34fb'), 
```

```
teddy@thinkpad:~/work/bluetooth/test$ ./test-adapter name
thinkpad
```

感觉就是bluetoothctl的功能的一部分。



# 代码分析



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

7、这个讲了工具的用法。

https://www.pcsuggest.com/linux-bluetooth-setup-hcitool-bluez/

8、Ubuntu系统(bluez)蓝牙调试

https://blog.csdn.net/zjli321/article/details/52122447

9、Using bluez to access Bluetooth Low Energy devices?

https://unix.stackexchange.com/questions/203504/using-bluez-to-access-bluetooth-low-energy-devices

10、

https://docs.ubuntu.com/core/en/stacks/bluetooth/bluez/docs/reference/gatt-services

11、Bluetooth Low Energy Development on Linux

这篇文章不错。

https://medium.com/@doganyazar/bluetooth-low-energy-development-on-linux-4dc6fc079506