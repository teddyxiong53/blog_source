---
title: 蓝牙之bluez
date: 2018-05-31 21:51:28
tags:
	- 蓝牙

---

--

# 简介

BlueZ是一个开源的Linux蓝牙协议栈，为Linux系统提供了蓝牙功能的支持。

它由一个用户空间的库和一组系统工具组成，

能够实现蓝牙设备的发现、配对、连接等功能。

BlueZ由一个团队进行开发和维护，是Linux系统中最常用的蓝牙协议栈之一。

BlueZ的主要特点包括：

- **开源和免费**：BlueZ是开源的，任何人都可以查看、修改和分发它的源代码。它采用GPL许可证发布，完全免费使用。
- **功能丰富**：BlueZ提供了广泛的蓝牙功能支持，包括基本的设备发现、配对、连接，以及高级的音频传输、文件传输、串口传输等功能。
- **模块化设计**：BlueZ采用模块化的设计，提供了一系列的蓝牙协议和服务，可以根据需要进行选择和定制，从而适应不同的应用场景。
- **兼容性强**：BlueZ支持最新的蓝牙标准，能够与各种类型的蓝牙设备进行通信，包括手机、平板电脑、笔记本电脑、智能音箱、智能手表等。
- **活跃的社区支持**：BlueZ拥有一个活跃的开源社区，提供了丰富的文档、示例代码和技术支持，方便开发者学习和使用。

总的来说，BlueZ是Linux系统中最流行的蓝牙协议栈之一，被广泛应用于各种类型的Linux设备上，包括个人电脑、嵌入式系统、物联网设备等。

# 发展历史

BlueZ的发展历史可以追溯到2001年，以下是其主要里程碑和发展历程：

- **2001年**：BlueZ项目由Maksim Krasnyansky发起，最初是为了在Linux系统上支持蓝牙技术而创建的。
  
- **2002年**：BlueZ首次被合并到Linux内核中，成为Linux系统的一部分。这一举动使得Linux系统能够原生支持蓝牙设备。

- **2004年**：BlueZ发布了第一个稳定版本（版本3.x），并迅速成为Linux系统中使用最广泛的蓝牙协议栈。

- **2007年**：BlueZ项目开始转向版本4.x，这一版本带来了许多改进和新功能，包括更好的蓝牙音频支持、蓝牙低功耗（Bluetooth Low Energy，BLE）支持等。

- **2011年**：BlueZ 5.x版本发布，这一版本对BlueZ进行了彻底的重构和重新设计，采用了D-Bus作为通信机制，提供了更好的性能和可扩展性。

- **2013年**：BlueZ项目被Linux基金会接管，成为Linux基金会的一个重要项目，这一举措进一步增强了BlueZ的开发和支持力度。

- **2020年**：BlueZ项目继续发展，发布了最新版本BlueZ 5.54，该版本增加了对新蓝牙标准的支持，并改进了性能和稳定性。

在过去的二十多年里，BlueZ经历了多次重大版本更新和改进，不断适应蓝牙技术的发展和Linux系统的需求，成为了Linux系统中不可或缺的一部分，为各种类型的Linux设备提供了强大的蓝牙功能支持。

# 对比说明android的 bluedroid协议栈和bluez协议栈

好的，我们来对比一下Android的Bluedroid协议栈和BlueZ协议栈：

| 特性           | Bluedroid                             | BlueZ                                |
| -------------- | ------------------------------------- | ------------------------------------ |
| 使用平台       | Android                               | Linux（包括嵌入式Linux）             |
| 开发者         | Broadcom（后来被谷歌维护）            | Linux社区                            |
| 语言           | C                                     | C                                    |
| 主要用途       | 为Android设备提供蓝牙功能             | 为各种Linux设备提供蓝牙功能          |
| 蓝牙版本支持   | 支持最新的蓝牙规范                    | 支持最新的蓝牙规范                   |
| 体系架构       | 集成到Android框架中，专为移动设备优化 | 模块化设计，适用于广泛的设备         |
| 可扩展性       | 专为Android设计，扩展性有限           | 高度模块化，易于扩展和定制           |
| 文档和社区支持 | 文档较少，主要依赖于Android开发者社区 | 丰富的文档和活跃的开源社区支持       |
| 调试工具       | Android Studio、ADB等                 | 蓝牙调试工具（如bluetoothctl）       |
| 性能优化       | 针对移动设备进行优化                  | 更通用的优化，可在不同类型设备上运行 |
| 安全性         | 集成到Android安全体系中，定期更新     | 依赖Linux内核和开源社区的安全更新    |

### 主要区别：

1. **平台专用性**：Bluedroid专为Android设备设计，而BlueZ是为所有Linux设备设计的，包括嵌入式系统。
2. **社区和支持**：BlueZ有一个活跃的开源社区和丰富的文档支持，而Bluedroid的文档相对较少，主要依赖Android社区。
3. **架构和可扩展性**：BlueZ采用模块化设计，易于扩展和定制；Bluedroid则集成在Android框架中，更适合移动设备，但扩展性较差。

两者各有优势，选择哪个协议栈取决于具体的应用场景和需求。如果是开发Android应用或设备，Bluedroid更为合适；如果是开发通用的Linux蓝牙解决方案，BlueZ则是更好的选择。

# 简单使用

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

# bluez里对glib的使用

在BlueZ中，GLib是一个常用的工具库，用于简化C语言编程过程，提供了许多常用的数据结构、函数和宏。

BlueZ使用GLib来实现一些常见的功能，比如事件循环、异步操作等。

以下是BlueZ中对GLib的主要使用方式：

1. **事件循环（Event Loop）**：BlueZ使用GLib提供的事件循环机制来处理蓝牙相关的事件。通过调用GLib提供的函数，BlueZ可以注册事件源并监听事件的到来，然后在事件发生时执行相应的回调函数。

2. **异步操作**：在处理一些耗时的操作时，BlueZ可能会使用GLib提供的异步操作机制。通过GLib提供的异步函数和回调机制，BlueZ可以在后台执行耗时操作，同时不阻塞主线程。

3. **数据结构**：BlueZ可能会使用GLib提供的一些数据结构，比如链表、哈希表等，来方便地管理数据。

4. **内存管理**：BlueZ也可能会使用GLib提供的内存管理函数，比如内存分配、释放等，来管理动态分配的内存。

总的来说，GLib在BlueZ中的使用主要是为了简化编程过程，提高代码的可读性和可维护性，同时提供了一些常用的功能和工具，使开发者能够更方便地开发和维护蓝牙相关的代码。

# /etc/bluetooth/main.conf说明

`/etc/bluetooth/main.conf`是BlueZ蓝牙协议栈的主要配置文件，用于配置系统范围内的蓝牙设置和选项。以下是该文件的一般说明：

1. **[General]**：这个部分包含了一般性的蓝牙设置，如蓝牙适配器的名称、类别、可见性等。一些常见的选项包括：

   - `Name`：设定蓝牙适配器的名称。
   - `Class`：设置蓝牙适配器的设备类别。
   - `DiscoverableTimeout`：设置蓝牙设备在可见性模式下的超时时间。
   - `Discoverable`：设置蓝牙设备是否可见。

2. **[Policy]**：这个部分定义了一些与蓝牙设备连接和配对相关的策略。一些常见的选项包括：

   - `AutoEnable`：设置是否自动启用蓝牙适配器。
   - `PairableTimeout`：设置蓝牙设备在可配对模式下的超时时间。
   - `PairedDevices`：列出了已配对的蓝牙设备。

3. **[GATT]**：这个部分包含了与通用属性框架（GATT）相关的选项。GATT是蓝牙4.0及以上版本中使用的协议，用于描述蓝牙设备之间的通信和数据交换。

4. **[Policy]、[GATT]等其他部分**：除了上述列出的几个常见部分外，`main.conf`文件还可以包含其他自定义部分，用于配置其他特定的功能和选项。

总的来说，`/etc/bluetooth/main.conf`文件是用于配置系统范围内的蓝牙设置和选项的主要文件，通过修改该文件可以调整蓝牙适配器的名称、类别、可见性，以及连接和配对策略等。

## 例子

以下是一个`/etc/bluetooth/main.conf`文件的简单示例：

```plaintext
[General]
# 设置蓝牙适配器的名称
Name = MyBluetoothDevice

# 设置蓝牙适配器的设备类别
Class = 0x1F00

# 设置蓝牙设备在可见性模式下的超时时间（秒）
DiscoverableTimeout = 0

# 设置蓝牙设备是否可见
Discoverable = yes

[Policy]
# 设置是否自动启用蓝牙适配器
AutoEnable = true

# 设置蓝牙设备在可配对模式下的超时时间（秒）
PairableTimeout = 0

# 列出已配对的蓝牙设备
# PairedDevices = 00:11:22:33:44:55
```

在这个示例中：

- 蓝牙适配器的名称被设置为"MyBluetoothDevice"。
- 蓝牙适配器的设备类别被设置为0x1F00。
- 蓝牙设备的可见性被设置为永久可见。
- 蓝牙设备在可见性模式下的超时时间被设置为0，表示永久可见。
- 蓝牙适配器将会在系统启动时自动启用。
- 蓝牙设备在可配对模式下的超时时间被设置为0，表示永久可配对。
- 列出了一个已配对的蓝牙设备的示例。

这只是一个简单的示例，`/etc/bluetooth/main.conf`文件中可以包含更多的选项和配置。

## 解析函数

```
static void parse_config(GKeyFile *config)
{
	if (!config)
		return;

	check_config(config);

	DBG("parsing %s", main_conf_file_path);

	/* Parse Groups */
	parse_general(config);
	parse_br_config(config);
	parse_le_config(config);
	parse_gatt(config);
	parse_csis(config);
	parse_avdtp(config);
	parse_advmon(config);
}
```

# bluez的dbus服务说明

BlueZ通过DBus（Desktop Bus）提供了一组服务，

这些服务允许其他应用程序与蓝牙协议栈进行通信，

从而实现对蓝牙功能的控制和管理。

DBus是Linux和Unix系统中用于进程间通信的一种机制，

它允许不同的进程之间通过消息传递来进行通信。

以下是BlueZ通过DBus提供的一些常见服务和功能：

1. **org.bluez.ServiceManager**：这是BlueZ提供的主要服务之一，用于管理和控制蓝牙服务。它提供了一组接口，允许应用程序注册、注销和查询蓝牙服务。通过该服务，应用程序可以获取有关已连接设备、发现设备、配对设备等信息。

2. **org.bluez.Adapter1**：这个服务用于管理和控制蓝牙适配器。它提供了一组接口，允许应用程序设置适配器的可见性、扫描设备、连接设备等操作。通过该服务，应用程序可以与蓝牙适配器进行交互，实现对蓝牙功能的控制。

3. **org.bluez.Device1**：这个服务用于管理和控制蓝牙设备。它提供了一组接口，允许应用程序对已配对设备进行操作，如连接、断开连接、读取设备属性等。通过该服务，应用程序可以与蓝牙设备进行通信，实现对设备的控制和管理。

4. **org.bluez.GattCharacteristic1**：这个服务用于管理和控制GATT（Generic Attribute Profile）特征。GATT是蓝牙4.0及以上版本中使用的协议，用于描述蓝牙设备之间的通信和数据交换。通过该服务，应用程序可以读取和写入GATT特征的值，实现对蓝牙设备的数据交换。

总的来说，BlueZ通过DBus提供了一组服务，允许应用程序与蓝牙协议栈进行通信，从而实现对蓝牙功能的控制和管理。通过这些服务，应用程序可以实现蓝牙设备的发现、配对、连接，以及数据交换等功能。

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

## list-devices

# test目录的python测试脚本分析

这些脚本都是通过跟dbus通信来实现功能的，所以不需要对bluez进行python binding。



# 代码分析

## bluez/lib/hci.h

这个头文件里定义了很多的重要结构体。

```
struct hci_dev_info 
```

hcitool dev，这个命令执行的是查询本地的hci设备信息。

最后是调用了系统调用。

```
ioctl(s, HCIGETDEVINFO, (void *) &di)
```

HCIGETDEVINFO 这个宏在kernel/include/net/blutooth/hci_sock.h里定义：

```
#define HCIGETDEVINFO	_IOR('H', 211, int)
```

这个hci_sock.h里，也有hci_dev_info结构体定义，跟应用层的一样。

打开一个蓝牙socket。是这样：

```
sk = socket(AF_BLUETOOTH, SOCK_RAW | SOCK_CLOEXEC, BTPROTO_HCI);
```

HCI_MAX_DEV这个最大是16个。

## bluetoothd

这个代码入口在bluez/src/main.c。

调试方法：

```
/usr/libexec/bluetooth/bluetoothd -d -n
```

-n表示前台运行，-d表示debug模式。

```
connect_dbus
	连接到bus，设置本app的name为org.bluez。
adapter_init
btd_device_init
btd_agent_init
btd_profile_init
	这些都是注册dbus的interface。
plugin_init
	Loading builtin plugins
        Loading gap plugin
        Loading a2dp plugin
        Loading avrcp plugin
        Loading hostname plugin
        Loading builtin plugins
        not load battery plugin
	Loading plugins /usr/lib/bluetooth/plugins
rfkill_init();
	fd = open("/dev/rfkill", O_RDWR);
然后就进入mainloop。
```



```
#define BTPROTO_L2CAP	0
#define BTPROTO_HCI	1
#define BTPROTO_SCO	2
#define BTPROTO_RFCOMM	3
#define BTPROTO_BNEP	4
#define BTPROTO_CMTP	5
#define BTPROTO_HIDP	6
#define BTPROTO_AVDTP	7

#define SOL_HCI		0
#define SOL_L2CAP	6
#define SOL_SCO		17
#define SOL_RFCOMM	18

```



# bluez的dbus使用

还是以gatt-service.c作为分析。

```
create_services_one
	register_service(IAS_UUID)
```

register_service函数分析

```

```

一个service，对应了dbus里一个interface。

不只是service，其实其他的对象，也都是对应一个dbus的service。

```
#define GATT_MGR_IFACE			"org.bluez.GattManager1"
#define GATT_SERVICE_IFACE		"org.bluez.GattService1"
#define GATT_CHR_IFACE			"org.bluez.GattCharacteristic1"
#define GATT_DESCRIPTOR_IFACE		"org.bluez.GattDescriptor1"
```

我似乎可以这样理解：

gatt-service.c这个app，里面就一个dbus object，所有跟dbus打交道的东西，都是这个object的interface（相当于成员变量）。



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