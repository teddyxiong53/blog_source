---
title: Linux之dbus
date: 2018-09-10 17:36:31
tags:
	- Linux

---

--

# 替代方案

谷歌搜索dbus alternatives

常用的就是ubus。



dbus能不能移植到嵌入式系统里？如何移植？

如何写一个简单程序来测试dbus工作是否正常？

怎样写一个基本程序来理解dbus的原理？

为什么需要dbus？



dbus是一个为App之间通信的消息总线系统。用于进程间通信。跟共享内存、信号量这些的一个类型的东西。

采用了3层架构。

1、一个库文件libdbus。我们写app，链接这个库，就可以。

2、一个守护进程。所有消息，都通过这个守护进程来转发。

3、跟特定库或者语言的绑定，例如跟Python的绑定，跟glib的绑定，跟qt的绑定。

官方也不建议直接使用dbus，而是使用包装过的。这样用起来会简单些。

```
dbus-daemon --system
```

dbus就是对socket的封装。

DBUS可以完成1对1的IPC, 多对多的IPC, 多对多需要daemon,和android中的service_manger类似,如同router.



看树莓派的情况。

```
root@raspberrypi:/etc/dbus-1# tree
.
├── session.d
└── system.d
    ├── avahi-dbus.conf
    ├── bluetooth.conf
    ├── Mountall.Server.conf
    ├── org.freedesktop.hostname1.conf
    ├── org.freedesktop.locale1.conf
    ├── org.freedesktop.login1.conf
    ├── org.freedesktop.network1.conf
    ├── org.freedesktop.PolicyKit1.conf
    ├── org.freedesktop.RealtimeKit1.conf
    ├── org.freedesktop.resolve1.conf
    ├── org.freedesktop.systemd1.conf
    ├── org.freedesktop.timedate1.conf
    ├── pulseaudio-system.conf
    └── wpa_supplicant.conf

2 directories, 14 files
```

在rk3308的板子上：

```
├── session.conf
├── system.conf
└── system.d
    ├── avahi-dbus.conf
    ├── bluetooth.conf
    ├── dnsmasq.conf
    └── wpa_supplicant.conf
```





buildroot里，可以选配dbus的支持。

在hardware handling下面。



这些conf文件，都是xml格式的。

现在我关注的蓝牙这个部分。

看看蓝牙dbus如何使用的。



多对多的dbus消息都通过dbus后台进程进行中转。相当于一个消息路由。

是一种进程间通信机制，支持一对一和一对多的对等通信。

dbus的主要概念是总线。

连接到总线的消息可以通过总线发送或者接收消息。

消息可以分为4种。

```
1、method call消息。
	触发一个函数调用。
2、method return消息。
	触发函数调用返回的结果。
3、error消息。
	触发的函数调用返回一个异常。
4、signal消息。
	通知，就是触发事件。这个跟上面三个不同。
```

```
/** This value is never a valid message type, see dbus_message_get_type() */
#define DBUS_MESSAGE_TYPE_INVALID       0
/** Message type of a method call message, see dbus_message_get_type() */
#define DBUS_MESSAGE_TYPE_METHOD_CALL   1
/** Message type of a method return message, see dbus_message_get_type() */
#define DBUS_MESSAGE_TYPE_METHOD_RETURN 2
/** Message type of an error reply message, see dbus_message_get_type() */
#define DBUS_MESSAGE_TYPE_ERROR         3
/** Message type of a signal message, see dbus_message_get_type() */
#define DBUS_MESSAGE_TYPE_SIGNAL        4

#define DBUS_NUM_MESSAGE_TYPES          5
```



主要用来进程间**函数调用**和进程间**信号广播**。



dbus的特点：

1、低延迟。

2、低开销。

3、高可用。

**协议是二进制的，避免了序列化的过程。通信效率高。**

**因为主要是用于本机内部通信，所以采用二进制带来的好处大于坏处。**

支持异步操作。

**dbus易于使用，因为它是基于消息，而不是字节流。**



总线有两种，一个是system bus，一个是session bus。

本质上，dbus是一个对等的协议。

每个消息都一个源地址和目的地址。



看dbus代码里的readme的说明。

版本系统，跟Linux内核一个风格，偶数的表示稳定版本，奇数版本表示开发版本。

# dbus为什么复杂

D-Bus（Desktop Bus）作为一种进程间通信机制，确实具有一定的复杂性。以下是一些可能导致 D-Bus 复杂性的原因：

1. 灵活性和功能丰富：D-Bus 的设计目标是为了提供灵活的、可扩展的通信机制，以满足各种不同的通信需求。**它支持广播、请求-响应、异步通信等多种通信模式**，并且提供了丰富的特性和功能，如对象导航、信号传递、方法调用等。这种灵活性和功能丰富性使得 D-Bus 在复杂的通信场景中具有更强大的表达能力，但也增加了一定的学习和使用成本。

2. 安全性和权限管理：D-Bus 强调安全性，通过提供细粒度的权限管理和访问控制机制来保护通信的安全性。这包括对对象、接口和方法的访问权限、消息的验证和策略等。虽然这种安全性是必要的，但同时也增加了使用 D-Bus 的复杂性，需要了解和配置正确的权限规则。

3. 性能和效率考虑：D-Bus 作为一种高级通信机制，需要提供一定程度的性能和效率。为了实现高效的通信，D-Bus 使用了多线程、异步操作和消息传递机制等技术。这些技术的使用增加了一些复杂性，需要正确地处理线程同步、消息处理和错误处理等问题。

4. 跨平台支持：D-Bus 是一个跨平台的通信机制，可以在多种操作系统和编程语言中使用。为了实现这种跨平台支持，D-Bus 需要提供相应的库和工具，使得在不同平台上使用 D-Bus 变得更加复杂。此外，不同平台对于 D-Bus 的实现和配置也可能存在一些差异，需要进行适配和调试。

尽管 D-Bus 有一定的复杂性，但它也带来了一些重要的好处，如强大的通信能力、安全性和跨平台支持。对于需要在不同应用程序之间进行可靠、安全和灵活通信的场景，D-Bus 提供了一种成熟的解决方案。虽然使用 D-Bus 可能需要一些学习和调试的成本，但一旦掌握并正确使用，它可以极大地简化进程间通信的开发和管理。

# 有没有对dbus进行包装易于使用的接口？

是的，有一些第三方库对 D-Bus 进行了包装，提供更易于使用的接口，简化了在 C 语言中使用 D-Bus 的过程。以下是一些常用的 D-Bus 包装库：

1. GDBus（GLib D-Bus Binding）：GDBus 是 GLib 提供的 D-Bus 包装库，它为 C 语言提供了更高级的接口，简化了与 D-Bus 的交互。GDBus 提供了一组易于使用的函数和数据结构，支持发送和接收 D-Bus 消息、注册和暴露对象、调用方法、监听信号等操作。GDBus 是 GNOME 桌面环境的默认 D-Bus 实现，广泛用于 GNOME 应用的开发。

2. sd-bus（Systemd D-Bus Library）：sd-bus 是 Systemd 提供的 D-Bus 包装库，它为 C 语言提供了简单而高效的接口，支持与 D-Bus 通信的各种操作。sd-bus 的设计目标是提供一个轻量级、无依赖的 D-Bus 实现，与 Systemd 紧密集成。它提供了简洁的 API，包括消息的发送和接收、接口的注册和调用、信号的监听等功能。

3. Dbuskit：Dbuskit 是一个开源的 D-Bus 包装库，提供了简单的 C 语言接口，旨在简化使用 D-Bus 的复杂性。它提供了一组易于使用的函数和数据结构，支持连接 D-Bus、发送和接收消息、调用方法、监听信号等操作。Dbuskit 是一个轻量级的库，适用于嵌入式系统和资源有限的环境。

这些包装库提供了更高级的接口，抽象了底层的细节，使得在 C 语言中使用 D-Bus 更加方便和直观。根据具体的需求和项目的要求，选择适合的包装库可以提高开发效率并简化代码的编写。

# 自动生成dbus相关函数的工具

在 Linux 平台上，有一些工具可以帮助自动生成 D-Bus 相关的代码。以下是两个常用的工具：

1. gdbus-codegen：gdbus-codegen 是 GLib 提供的一个工具，用于生成基于 GLib 的 D-Bus 代理和接口的代码。它可以从 D-Bus 接口描述文件 (XML 格式) 自动生成相关的代码，包括接口、代理和信号处理函数等。您可以使用该工具生成用于连接到 D-Bus 服务的客户端代码。

2. dbus-codegen：dbus-codegen 是 D-Bus 提供的官方工具，用于生成基于 libdbus 的 D-Bus 客户端和服务端代码。它可以从 D-Bus 接口描述文件 (XML 格式) 自动生成相关的代码，包括接口、方法、信号和属性等。您可以使用该工具生成用于实现 D-Bus 服务或连接到 D-Bus 服务的客户端代码。

这些工具都需要提供一个 D-Bus 接口描述文件作为输入，并生成相应的代码文件。您可以在生成的代码中使用自动生成的函数来进行 D-Bus 通信和调用。

请注意，生成的代码可能需要根据您的具体需求进行进一步的修改和定制。另外，这些工具通常与特定的开发框架或库相关联，例如 GLib 或 libdbus，因此您需要确保在使用这些工具之前正确设置和配置相关的开发环境。

建议查阅相关工具的官方文档以获取更详细的使用说明和示例。

# 概念理解

运行一个dbus-daemon，就创建一个bus。

当一个app连接到这个bus的时候，就创建了一个connection。

每个app里，有多个object。站在dbus的角度，通信的不是app，而是object。

一个object里，有多个不同的interface。我们可以把interface理解为对象的成员变量。这些变量有getter和setter方法。

interface其实是通信方式的集合。

signal通信方式，不需要对方回复。

**method call通信方式，需要对方回复。回复的是method return。**



signal方式比较简单，我们就以signal为例，来看看整个通信过程。

```
conn = dbus_bus_get(DBUS_BUS_SESSION, &err);//连接到bus上。
ret = dbus_bus_request_name(conn, "test.method.server", DBUS_NAME_FLAG_REPALCE_EXISTING, &err);//把自己的进程名字注册到bus上。
```

加入一个进程，想要接收interface名字为test.signal.Type的信号。

则这样：

```
dbus_bus_add_watch(conn, "type='signal',interface='test.signal.Type'", &err);
```

然后就等待消息的到来：

```
dbus_connection_read_write(conn, 0);//0表示一直等待，没有超时。
//执行到这里，说明消息已经来了，取出消息。
msg = dbus_connection_pop_message(conn);
```



发送的进程里这样做：

```
dbus_uint32_t serial = 0;//消息id
DBusMessage *msg;
msg = dbus_message_new_signal("/test/signal/Object", "test.signal.Type", "Test");
//添加参数给signal
dbus_message_iter_init_append(msg, &args);
dbus_message_iter_append_basic(&args, DBUS_TYPE_STRING, &sigval);
//发送
dbus_connection_send(conn, msg, &serial);
```



DBusMessage是dbus的核心数据结构。

里面存储了2个主要信息，一个是为通信机制服务的各种name，一个是通信数据本身。



## 各种name

### dbus name

最重要的name就是dbus name。

这个是每个app用来标记自己的。

可以理解为ip地址。

bus name有两种，

1、unique connection name。`:10`这种以冒号开头的，可读性不太好。

2、well-known name。这种就可读性好一些。

默认只给分配冒号开头的bus name。

如果要well-known name。就使用dbus_bus_request_name来申请。

### interface name

这个是为了上层架构而设计的。例如qt dbus。

在C api这一层，你几乎可以不管它。

它的命名规则个dbus name几乎一样，只是不是用`-`。

### object path

跟interface一样，是为上层架构设计的。

在C api这一层，几乎可以不管他。

### member name





**dbus规范里标准化了一些接口。**

**这些接口对我们调用其他服务提供的dbus api很有帮助。**

我们看其中比较重要的两个。

```
org.freedesktop.DBus.Introspectable
```

看bluez里的gatt-service.c代码：

```
add_interface(data, DBUS_INTERFACE_INTROSPECTABLE, introspect_methods,
						NULL, NULL, data, NULL);
```

会这样调用。那么应该就可以查看这个的信息吧。

对应的命令怎么写呢？

下面这样可以得到回复。

```
dbus-send --system --type=method_call --print-reply --dest=org.bluez /org/bluez/Device1/hci0/dev_54_A4_93_A0_00_08 org.freedesktop.DBus.Introspectable.Introspect                                          
```

--dest=org.bluez，表示是发送给bluetoothd这个app。

object path，是从bluez/doc/device-api.txt里分析得到的。

```
Service		org.bluez
Interface	org.bluez.Device1
Object path	[variable prefix]/{hci0,hci1,...}/dev_XX_XX_XX_XX_XX_XX
```

当前这样返回的，是一个没有什么有效内容的xml文件。

内容是这里填入的：

```
data->introspect = g_strdup(DBUS_INTROSPECT_1_0_XML_DOCTYPE_DECL_NODE "<node></node>");
```





# 建立服务的流程

dbus_bus_get：获取一个dbus连接。

dbus_bus_reques_name：为这个连接起名。这个名字就是后续进行远程调用的时候的服务名

dbus_connection_read_write：进入监听循环。（一般不用这种方式，用mainloop的方式来做）

然后在循环里，我们从bus上取出消息。dbus_connection_pop_message

然后对比消息中的方法接口名和方法名：dbus_message_is_method_call

如果对比一致，那么就跳转到响应的处理函数里去。并从消息里取出远程调用的参数。

并且建立起回传结果的通路，reply_to_method_call。

# 发送信号的流程

dbus_message_new_signal

把信号相关的参数放进去。dbus_message_iter_init_append。

dbus_message_iter_append_basic。

然后启动发送：

dbus_connection_send

dbus_connection_flush



# 进行一次远程调用的流程

申请一个远程调用通道：dbus_message_new_method_call

需要填写的参数有： 本次调用的接口名。本地调用的方法名。

实际上是申请了一个内存，把内容往里面填。

然后启动发送调用并释放发送相关的消息。

dbus_connection_send_with_reply。

**会阻塞等待调用执行完成。**

当这个句柄回传消息之后，我们从消息结构中分离出参数。

用dbus提供的函数提取参数的类型和参数 -- dbus_message_iter_init(); dbus_message_iter_next(); dbus_message_iter_get_arg_type(); dbus_message_iter_get_basic()。也就达成了我们进行本次远程调用的目的了。

# 信号接收流程

dbus_bus_add_match()。我们进入等待循环后，只需要对信号名，信号接口名进行判断就可以分别处理各种信号了。在各个处理分支上。我们可以分离出消息中的参数。对参数类型进行判断和其他的处理。



# 工具

dbus默认提供了一些工具。

dbus-monitor和dbus-send。可以用来测试。



系统里的dbus工具有：

````
dbus-binding-tool
	这个是生成glib代码文件的工具。
dbus-daemon
	--session等价于：--config-file=/usr/share/dbus-1/session.conf
	
dbus-monitor
	这个只有5个选项。比较简单。
	--system：监控系统bus的消息。
	--session：监控用户session bus的消息。默认是这个。
	--profile：不指定，就是classic模式。这个是精简模式。
	--monitor：监控输出模式。默认就是这个。
dbus-send
	发送dbus消息。
dbus-uuidgen
	生成一个uuid。
dbus-cleanup-sockets
	
dbus-launch
dbus-run-session
dbus-update-activation-environment
````

## dbus-send

在bluez的代码里搜索dbus_message_new_method_call。就可以看到注册了哪些东西，可以让我们进行调用的。



```
dbus-send --system --print-reply --dest=org.bluez /org/bluez/audio org.bluez.audio.Manager.CreateDevice string:'11:11:11:11:11:11'
其中:

--system
将命令发向系统总线，也可使用--session
--print-reply
打印返回结果
--dest=org.bluez
服务名。用户可以用查询命令获得当前系统的所有服务名
/org/bluez/audio
对象名。由服务定义
org.bluez.audio.Manager.CreateDevice
object.interface.Method
string:'11:11:11:11:11'
参数。 类型:值 int32:123
```



命令要有2个必须的参数：

```
<destination object path> <message name>
```

path比较好理解，就是`/`这样的路径一样的东西。

message name

这个是怎么写的呢？



遍历dbus上所有的对象。

```
dbus-send --session --type=method_call --print-reply --dest=org.freedesktop.DBus / org.freedesktop.DBus.ListNames
```

向某个对象发送消息

```
dbus-send --session --type=method_call --print-reply --dest=org.gnome.ScreenSaver  / org.freedesktop.DBus.Introspectable.Introspect
```



buildroot下编译的板端程序，这些dbus的东西，基本都有。

bluez的dbus，有哪些东西可以被dbus-send来查看和设置呢？

可以尝试查看uuid。



下面这个命令是可以有效果的。是打开discovery。注意这条命令的使用方式。这个对bluez是通用的写法。

```
dbus-send --system --type=method_call --dest=org.bluez /org/bluez/hci0 org.freedesktop.DBus.Properties.Set string:org.bluez.Adapter1 string:Discoverable variant:boolean:true
```

下面这个不行。

```
dbus-send --system --type=method_call --dest=org.bluez --print-reply /org/bluez/hci0 org.bluez.Adapter1.GetName
```



查看板端dbus的所有管理的object。

```
dbus-send --system --print-reply --type=method_call --dest='org.bluez' '/' org.freedesktop.DBus.ObjectManager.GetManagedObjects
```

```
dbus-send --system --print-reply --type=method_call --dest='org.bluez' '/org/bluez/hci0/dev_54_A4_93_A0_00_08' org.freedesktop.DBus.ObjectManager.GetManagedObjects

```



这个文档就是讲用dbus来操作bluez的。

https://www.landley.net/kdocs/ols/2006/ols2006v1-pages-421-426.pdf



https://www.linumiz.com/bluetooth-list-available-controllers-using-dbus/



## dbus-launch

```
/ # dbus-launch
DBUS_SESSION_BUS_ADDRESS=unix:abstract=/tmp/dbus-UE021yKXGo,guid=caec9b667660f597a32dd7395ee97b4c
DBUS_SESSION_BUS_PID=10467
```

这个命令的作用是什么？



D-Bus daemon是D-Bus的非常重要的一个服务，类似于IP网络中的[路由器](https://so.csdn.net/so/search?q=路由器&spm=1001.2101.3001.7020)。

跟这个后台服务有关的应用程序包括：

dbus-daemon: 

D-Bus的后台进程，作为D-Bus的消息中转枢纽，可分成system和[session](https://so.csdn.net/so/search?q=session&spm=1001.2101.3001.7020)两种。

dbus-launch: 

启动一个dbus-daemon，后面有不同的参数。

一般而言，dbus-daemon启动后需要将其地址告诉给所有需要使用该bus的applications。



当系统启动时，需要使用dbus-launch来启动dbus-daemon，一般而言，

一般采用下面的命令启动dbus daemon以及dbus application

(1) eval `dbus-launch --auto-syntax`

(2) ./yourapp

第一行代码，采用eval来执行两次，第一次执行dbus-lauch --auto-syntax，除了启动dbus daemon之外，还输出了下面的内容：

DBUS_SESSION_BUS_ADDRESS='unix:path=/tmp/dbus-6Z62FMmwf3,guid=5dbd92e4865a3f56880d2120000000d6';
export DBUS_SESSION_BUS_ADDRESS;
DBUS_SESSION_BUS_PID=998;

第二次执行时就将环境变量DBUS_SESSION_BUS_ADDRESS暴露出去了。所有的dbus application在注册DBUS服务时，必须知道这个DBUS_SESSION_BUS_ADDRESS的数据。

在第二行执行自己的dbus application的时候，根据DBUS_SESSION_BUS_ADDRESS环境变量，能够找到session bus进行注册和通讯。



```
sh-5.0# /usr/bin/dbus-launch | /bin/sed '/^#.*\|^$/d'
DBUS_SESSION_BUS_ADDRESS=unix:abstract=/tmp/dbus-BdRxIZh1da,guid=18bed0c46c25ded3f95dda5f62da449a
DBUS_SESSION_BUS_PID=1451
```



这里我们会有两个app: app1(client)，app2(server), 然后，再启动一个“dbus-daemon （session）”

我们期望，app1 和 app2 之间的通信，可以使用 刚才启动的 “dbus-daemon”



### 启动一个dbus-daemon (session)

方式1： 使用dbus-launch 创建一个dbus-daemon:

```ini
#yum install -y dbus-x11-1:1.6.12-13.1.alios7.x86_64

#dbus-launch
DBUS_SESSION_BUS_ADDRESS=unix:abstract=/tmp/dbus-7Q7Spuq5IH,guid=079edc76e4c5c6433d3507855c5260ce
DBUS_SESSION_BUS_PID=121376
```

方式2： 手动启动

```typescript
#DBUS_VERBOSE=1 dbus-daemon --session --print-address
unix:abstract=/tmp/dbus-jXwkggHTo2,guid=dc666ee7ba7ddf788efd8c485c526564
```

两个方式的目的，**不仅仅是启动dbus-daemon, 更重要的是，获得address.**



注意，这里会反馈一个地址， `unix:abstract=/tmp/dbus-7Q7Spuq5IH,guid=079edc76e4c5c6433d3507855c5260ce` ， 所以，你需要保证 你的环境变量 `DBUS_SESSION_BUS_ADDRESS`的值就是这个地址。

其实dbus-daemon是有地址的，而且有一个环境变量来表示它`--DBUS_SESSION_BUS_ADDRESS`，可以用命令env查看到。我们的程序，也就就是依靠这个环境变量来确认使用哪一个dbus-daemon的。



参考资料

1、

https://blog.csdn.net/whatday/article/details/114474167

2、Getting start with dbus in systemd (02)

https://www.cnblogs.com/muahao/p/10341178.html

## d-feet

这个是Ubuntu下的一个图形界面。可以查看系统里的dbus的情况。



## dbus-binding-tool

 C language GLib bindings generation utility.

一个生成glib绑定代码的工具。

dbus-binding-tool is used to expose a GObject via D-Bus.

As input, dbus-binding-tool uses a D-Bus Introspection XML file.  

As output, the client-side or server-side bindings is generated.  This output is a header file which eases the use of a remote D-Bus object. 

输入一个xml文件，生成C文件和头文件。

## gdbus-codegen

gdbus-codegen --interface-prefix=aml.linux.dbus --generate-c-code=audioservice_gdbus aml.linux.dbus.xml





参考资料

1、

有需要的时候，参考这个来改就好了。

https://www.freedesktop.org/software/gstreamer-sdk/data/docs/latest/gio/ch30s05.html

# glib-dbus和GDBus的区别

GDBus和glib-dbus都是由GNU组织开发的。GDBus可以认为是glib-dbus的升级版，其编程过程比起glib-dbus来要简单得多。

# python例子

```
#!/usr/bin/python

import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
import time
import gobject

MSG_OBJ_PATH = "/com/example/msg"
MSG_INTERFACE_URI = "com.example.msg"

TIMEFORMAT = "%H:%M:%S"

class Msg(dbus.service.Object):
    def __init__(self,bus,object_path):
        dbus.service.Object.__init__(self,bus,object_path)

    @dbus.service.method(dbus_interface=MSG_INTERFACE_URI,
                         in_signature='', out_signature='s')
    def say_hello(self):
        return "hello, exported method"

    @dbus.service.signal(dbus_interface=MSG_INTERFACE_URI,
                         signature='as')
    def msg_signal(self,msg_list):
        print "exported signal: ",msg_list

    def construct_msg(self):
        timeStamp = time.strftime(TIMEFORMAT)
        self.msg_signal(["1111",timeStamp,"This is the content","1 2 3"])
        return True

if __name__ == "__main__":
    DBusGMainLoop(set_as_default=True)
    bus = dbus.SessionBus()
    aMsg = Msg(bus,MSG_OBJ_PATH)

    gobject.timeout_add(1000,aMsg.construct_msg)
    loop = gobject.MainLoop()
    loop.run()

```



# 官网文档

## 介绍

**dbus是一个低开销、易于使用的ipc通信机制。**

低开销是因为它是二进制协议，它设计就是为了本机内部的通信。设计时避免round trip。允许异步操作。跟X Protocol有点像。

dbus易于使用，因为它使用了消息的机制，而不是字节流的机制。

帮我们处理了很多复杂的ipc事务。

另外，有很多wrapper库，可以让使用者易于集成。

有message protocol和message bus这2个概念。

system bus，在嵌入式里适合用。

session bus，这个主要是为gnome和KDE这样的桌面环境用的。

dbus并不打算成为一个通用的ipc框架，所以它去掉了很多不必要的功能。

同时，dbus也提供了一些其他ipc一般没有的特色功能。

例如，bus names、安全策略。

这些特性，也是触发dbus进行开发的主要动力。



dbus协议的稳定性

dbus协议在2006年就已经frozen了。只需要兼容性地扩展。

## 类型系统

dbus有一个类型系统。

可以把不同类型的值，进行序列化。**序列化的结果，叫做wire format。**

序列化，叫编码。

反序列化，叫反编组。

### 基本类型

```
u8 ： y
bool： b
s16 ： n
u16： q
s32： i
u32： u
s64：x
u64：t
double：d
unix_fd：h。实际是int32类型。h表示handle的意思。
```

字符串也是基本类型。

下面3个都是字符串。但是用不同的类型来表示。

```
string: s
object path: o
signature: g
```

### object path

object path是一个name，用来表示一个对象实例。

一个app里的对象实例，构成了一个树状结构。

object path，一般是用域名倒着写作为开头，相当于一个namespace。

还包含一个interface version number。

**这样就可以实现多个service。以及同一个service的多个版本。**

例如，xx.com公司在为一个播放器开发一个dbus api。则对应的object path设计为这样：

```
/com/xx/MusicPlayer1
```

### 容器类型

有4种容器类型。

struct、array、variant、dict_entry。

struct的类型码是`r`。但是在类型签名里，`r`并不出现。

而是用小括号来表示。

例如，一个包含2个int类型的结构体的类型签名是这样：

```
(ii)
```

结构体也可以嵌套。

```
(i(ii))
```

这个相当于：

```
struct {
	int a;
	struct {
		int b;
		int c;
	} x;
};
```

空的struct不允许。

array类型，用字母`a`表示。

int类型的array：`ai`

array里还可以放结构体。`a(ii)`。表示array里放了结构体，结构体的成员是2个int数据。

array还可以嵌套。`aai`。表示array，里面元素是int类型的array。

**variant的限制比较多。用字母v表示。后面只能有一个类型。**

而且长度不能超过64字节。

dict_entry跟array有点像。但是用大括号括起来。限制也比较多。



## message protocol

消息格式

有一个header和一个body。

消息最长可以到128MB。

消息的类型签名是：

```
yyyyuua(yv)
```

表示的含义：

```
字节1：大小端标志。l表示小端，B表示大端。
字节2：消息类型。就4种。
字节3：flags。有3种情况。
字节4：发送的app的major version。

u32成员1：body的长度。
u32成员2：消息的id。
array成员：元素是结构体，这个需要重点看一下。
```



# 操作蓝牙

```
/ # dbus-send --system --print-reply --type=method_call --dest=org.bluez /org/bl
uez/hci0 org.freedesktop.DBus.Properties.Get string:org.bluez.Adapter1 string:Ad
dress
method return time=1592534678.200347 sender=:1.2 -> destination=:1.15 serial=24 reply_serial=2
   variant       string "54:A4:93:A0:00:08"
```

把dbus-send，都可以按照上面的格式来写。

上面这一条获取本机蓝牙适配器地址的。

--dest=org.bluez 这个固定不变，表示我要给bluez的daemon进程发消息。

/org/bluez/hci0  这个要看bluez/doc下面的文档描述。这个就是object path。可以理解为找到要操作的对象。

![1592534821851](../images/random_name/1592534821851.png)

然后就是操作对象的接口。

org.freedesktop.DBus.Properties.Get

这个就是bluez实现的一个dbus标准接口。

![1592535098065](../images/random_name/1592535098065.png)

下面2个是org.freedesktop.DBus.Properties.Get接口的参数。

string:org.bluez.Adapter1 

string:Address



还可以用GetAll方法一次性获取。

```
dbus-send --system --print-reply --type=method_call --dest=org.bluez /org/bl
uez/hci0 org.freedesktop.DBus.Properties.GetAll string:org.bluez.Adapter1
```



```
dbus-send --system --dest=org.bluez --print-reply / org.freedesktop.DBus.ObjectManager.GetManagedObjects
```

用在这个获取所有的对象的情况。总结如下：

```
/org/bluez
	这个object path下面，
	有3个interface
		org.freedesktop.DBus.Introspectable
		org.bluez.AgentManager1
		org.bluez.ProfileManager1
/org/bluez/hci0
	org.freedesktop.DBus.Introspectable
	org.bluez.Adapter1
		有这些property
		Address
		AddressType
		Name
		Alias
		Class
		Powered
		Discoverable
		DiscoverableTimeout
		Pairable
		PairableTimeout
		Discovering
		UUIDs
		Modalias
	org.freedesktop.DBus.Properties
	org.bluez.GattManager1
	org.bluez.LEAdvertisingManager1
		ActiveInstances
		SupportedInstances
		SupportedIncludes
	org.bluez.Media1
/org/bluez/hci0/dev_00_6A_8E_16_C7_48
	org.freedesktop.DBus.Introspectable
	org.bluez.Device1
		有很多的property，跟上面Adapter的类似。
	org.freedesktop.DBus.Properties
```

# DBUS_SESSION_BUS_ADDRESS

当使用bus daemon时，libdbus会从环境变量中（DBUS_SESSION_BUS_ADDRESS）自动认识“会话daemon”的地址。

如果是系统daemon，它会检查指定的socket路径获得地址，也可以使用环境变量（DBUS_SESSION_BUS_ADDRESS）进行设定。

当dbus中不使用daemon时，需要定义哪一个应用是server，哪一个应用是client，同时要指明server的地址，这不是很通常的做法。

# 不同的拓扑结构

基于DBus的应用程序可以是使用DBus Daemon的总线型结构，

每个DBus的请求通过DBus Daemon转发；

或者是点对点的星型结构，

Client与Server之间是直接的Peer2Peer的连接。

这俩种结构各有优缺点：

总线型的结构比较清晰，Server需要维护的连接较少，实际上只有一个与DBus Daemon相连的连接，广播消息可以很容易的发送到各个Client；

**P2P形式的DBus通信中间因为少了DBus Daemon的中转，因此性能更好，大约提升30%。**



提供一个用于代码生成的XML文件

这份XML数据在GDBus中称为introspection data，用来描述提供服务的GObject的接口名与参数。用于gdbus-codegen可以使用这份XML文件生成在Client与Server侧使用的代码。

对于总线型DBus应用和P2P型DBus应用，这份代码是通用的。

生成的代码需要分别链接到俩个进程中：带有Skeleton字样的代码，运行在Server侧；带有Proxy字样的代码，运行在Client侧。



# buildroot dbus启动流程

amlogic的soundbar应用为例。

在开机启动过程中，依次是：

* /etc/init.d/rcS脚本的开头处，比任何S开头的脚本都优先的位置。

```
for i in `/usr/bin/dbus-launch | /bin/sed '/^#.*\|^$/d'`; do
export $i
done
mkdir -p /tmp/dbus
echo DBUS_SESSION_BUS_ADDRESS=$DBUS_SESSION_BUS_ADDRESS > /tmp/dbus/dbus-addr
echo DBUS_SESSION_BUS_PID=$DBUS_SESSION_BUS_PID > /tmp/dbus/dbus-pid
```

* S30dbus脚本start函数

```
    dbus-uuidgen --ensure
    dbus-daemon --system
```

dbus-uuidgen在这里是什么作用？

`dbus-uuidgen --ensure`在var/lib/dbus/machine-id 里生成一串sha值字符串。如果已经有值，则不会进行覆盖。

这个值的作用又是什么呢？可能是跨机器通信作为机器的id用的。对我来说，没有什么作用。

* audioservice进程启动

audioservice和homepapp应该是点对点的dbus通信。



用git blame查看。`/tmp/dbus/dbus-addr`对应的行是谁添加的。

```
108e491586a package/initscripts/init.d/rcS                        (Yeping Miao              2018-10-29 11:01:56 +0800 22) mkdir -p /tmp/dbus
108e491586a package/initscripts/init.d/rcS                        (Yeping Miao              2018-10-29 11:01:56 +0800 23) echo DBUS_SESSION_BUS_ADDRESS=$DBUS_SESSION_BUS_ADDRESS > /tmp/dbus/dbus-addr
108e491586a package/initscripts/init.d/rcS                        (Yeping Miao              2018-10-29 11:01:56 +0800 24) echo DBUS_SESSION_BUS_PID=$DBUS_SESSION_BUS_PID > /tmp/dbus/dbus-pid
```

108e491586a 找到这个提交。

写入文件，是因为环境变量有些地方传递不到。所以通过文件来传递。

对我来说没啥用。先不管，有问题时再解决。



https://dbus.freedesktop.org/doc/dbus-uuidgen.1.html

# systemd启动dbus

```
sh-5.0# systemctl status dbus
* dbus.service - D-Bus System Message Bus
     Loaded: loaded (/lib/systemd/system/dbus.service; static; vendor preset: disabled)
     Active: active (running) since Fri 2022-07-22 03:42:17 UTC; 3h 33min ago
TriggeredBy: * dbus.socket
       Docs: man:dbus-daemon(1)
   Main PID: 866 (dbus-daemon)
     Memory: 1.8M
     CGroup: /system.slice/dbus.service
             `-866 /usr/bin/dbus-daemon --system --address=systemd: --nofork ...

Jul 22 03:42:17 mesona5-av400 systemd[1]: Started D-Bus System Message Bus.
```

service文件的内容是：

```
[Unit]
Description=D-Bus System Message Bus
Documentation=man:dbus-daemon(1)
Requires=dbus.socket

[Service]
ExecStart=/usr/bin/dbus-daemon --system --address=systemd: --nofork --nopidfile --systemd-activation --syslog-only
ExecReload=/usr/bin/dbus-send --print-reply --system --type=method_call --dest=org.freedesktop.DBus / org.freedesktop.DBus.ReloadConfig
OOMScoreAdjust=-900
```



# dbus-daemon

dbus-deamon是一个D-Bus消息总线daemon,跑在后台，

它支持两个应用进程间一对一的通信，

dbus-deamon也是用上面的库实现的



系统启动之后，有两个dbus daemon的实例，　

一个称为system, 一个称为session(如果是多个用户，那么会每个用户启动一个)，

这个实例配置不同，权限也不同

system 实例使用的配置文件＝/etc/dbus-1/system.conf

session实例使用的配置文件=/etc/dbus-1/session.conf



一般来说system实例，被init script启动，所以具有root权根．大部分功能用于广播系统事件，比如插拨设备．

session　daemon用于不同桌面的进程通信或不同进程间的通信．



SIGHUP 信号导致dbus-daemon重新去加载配置，如果你改变配置之后，就需要发信号给dbus-daemon,让其去重新加载配置．





参考资料

https://blog.csdn.net/u012385733/article/details/80881343

# 参考资料

1、DBus 入门与应用 －－ DBus 的 C 编程接口

https://www.cnblogs.com/liyiwen/archive/2012/12/02/2798876.html

2、官方文档

https://dbus.freedesktop.org/doc/api/html/annotated.html

3、和菜鸟一起学linux之DBUS基础学习记录

https://blog.csdn.net/eastmoon502136/article/details/10044993

4、dbus通信与接口介绍

https://www.cnblogs.com/klb561/p/9135642.html

5、

https://www.cnblogs.com/chenxf0619/p/4829253.html

6、

https://dbus.freedesktop.org/doc/dbus-tutorial.html

7、dbus-send以及dbus-monitor工具的使用方法示例

https://www.xuebuyuan.com/3188840.html

8、dbus-glib示例说明

https://wenku.baidu.com/view/9a352d1152d380eb62946d67.html?sxts=1564551835283

9、dbus基础知识

https://wenku.baidu.com/view/0804b93283c4bb4cf7ecd1a9.html?from=search

10、DBus API的使用

https://my.oschina.net/u/994235/blog/113238

11、DBUS及常用接口介绍

https://blog.csdn.net/mr_wangning/article/details/60324291

12、D-Bus Documentation

https://dbus.freedesktop.org/doc/api/html/index.html

13、DBUS基础知识

https://www.cnblogs.com/wzh206/archive/2010/05/13/1734901.html

14、dbus-glib 和 GDBus 的区别

https://www.cnblogs.com/LubinLew/p/dbus-glib_and_GDBus.html

15、基于GDBus技术的IPC通信编程详解(1)

https://blog.csdn.net/adlindary/article/details/80167840

16、

https://blog.csdn.net/guoke312/article/details/81352944

17、

这文章挺好。

https://www.cnblogs.com/klb561/p/9058282.html

18、

这个有完整例子，讲解详细。

http://just4coding.com/2018/07/31/dbus/

19、

这个dbus系列文章不错。

https://blog.csdn.net/u012385733/category_7764546.html

20、

这个教程写得比较规范。可以看看。

https://thebigdoc.readthedocs.io/en/latest/dbus/dbus.html