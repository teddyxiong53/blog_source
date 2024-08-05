---
title: dbus之gdbus
date: 2020-06-16 14:14:49
tags:
	- dbus

---

--

# gdbus和glib-dbus

目前基于d-bus技术的几种编程框架有：glib-dbus，GDbus，QtDbus，dbus-python。这5种编程框架的复杂度有高有低，最简单的应该非QtDbus莫属了，最复杂的过程要属glib-dbus。鉴于我对GDBus的熟悉程度，这里只介绍GDBus的编程过程。

 GDBus和glib-dbus都是由GNU组织开发的。GDBus可以认为是glib-dbus的升级版，其编程过程比起glib-dbus来要简单得多。



参考资料

https://blog.csdn.net/adlindary/article/details/80167840



gdbus — Tool for working with D-Bus objects

```
用法：
  gdbus COMMAND

Commands:
  help         Shows this information
  introspect   Introspect a remote object
  monitor      Monitor a remote object
  call         Invoke a method on a remote object
  emit         Emit a signal
  wait         Wait for a bus name to appear
```



introspect，打印一个remote object的interface和property。

要支持introspection操作，需要remote object实现了org.freedesktop.DBus.Introspectable 这个接口。

举例：

下面的例子表示查看eth0的对象属性。

```
gdbus introspect --system \
        --dest org.freedesktop.NetworkManager \
        --object-path /org/freedesktop/NetworkManager/Devices/0
```

下面表示在图形界面下显示一条桌面通知。

```
gdbus call --session \
             --dest org.freedesktop.Notifications \
             --object-path /org/freedesktop/Notifications \
             --method org.freedesktop.Notifications.Notify \
             my_app_name \
             42 \
             gtk-dialog-info \
             "The Summary" \
             "Here's the body of the notification" \
             [] \
             {} \
             5000
```





# 概念差异

D-Bus 的核心概念在 dbus-glib 和 GDBus 中以非常相似的方式建模。

两者都有表示连接、代理和方法调用的对象。

但也有一些重要的区别：

dbus-glib 使用 libdbus 参考实现，而 GDBus 则没有。

相反，它依赖 GIO 流作为传输层，并有自己的 D-Bus 连接设置和身份验证实现。

==除了使用流作为传输之外，避免使用 libdbus 还可以让 GDBus 避免一些棘手的多线程问题。==

dbus-glib 使用 GObject 类型系统作为方法参数和返回值，包括自行开发的容器专门化机制。 

==GDBus 依赖于 GVariant 类型系统，==该系统专门设计用于匹配 D-Bus 类型。

dbus-glib 仅建模 D-Bus 接口，不提供任何对象类型。 

GDBus 对 D-Bus 接口（通过 GDBusInterface、GDBusProxy 和 GDBusInterfaceSkeleton 类型）和对象（通过 GDBusObject、GDBusObjectSkeleton 和 GDBusObjectProxy 类型）进行建模。

GDBus 包含对 org.freedesktop.DBus.Properties（通过 GDBusProxy 类型）和 org.freedesktop.DBus.ObjectManager D-Bus 接口的本机支持，而 dbus-glib 则不支持。



在 dbus-glib 中导出对象的典型方法包括使用 dbus-binding-tool 从 XML 自省数据生成粘合代码。 

GDBus 提供了一个名为 gdbus-codegen 的类似工具，它也可以生成 Docbook D-Bus 接口文档。



dbus-glib 不提供任何用于拥有和监视总线名称的便捷 API，GDBus 提供了 g_bus_own_name() 和 g_bus_watch_name() 系列便捷函数。



GDBus 提供了 API 来解析、生成和使用 Introspection XML，而 dbus-glib 则没有。

GTestDBus 提供 API 来创建隔离的单元测试



# api对比

dbus-glib，以dbus为核心。函数和类型以dbus为前缀。

GDBus，以glib为核心。函数和列席以GDBus为前缀。

| dbus-glib             | GDBus                                   |
| --------------------- | --------------------------------------- |
| DBusConnection        | GDBusConnection                         |
| DBusProxy             | GDBusProxy                              |
| DBusGObject           | GDBusInterfaceSkeleton   GDBusInterface |
| DBusGMethodInvocation | GDBusGMethodInvocation                  |

其他的函数就不列举了。

以GDBus的为主。

参考资料

1、参考这篇文章写基本的框架就好了。

https://docs.gtk.org/gio/migrating-gdbus.html


# bluez里的gdbus

这个是bluez封装的一个小的dbus库。只有几个文件。

一个头文件。gdbus/gdbus.h。

```
大概400行。
包含：
#include <dbus/dbus.h>
#include <glib.h>
结构体都是GDBusXX格式。
函数都是g_dbus_xx格式。

5个结构体
1个info，4个table。
GDBusArgInfo
GDBusMethodTable
GDBusSignalTable
GDBusPropertyTable
GDBusSecurityTable
这5个结构体，都有一个对应的flag枚举。

```

c文件

```
client.c
	GDBusClient
		这个是最重要的结构体。代表了一个本机的dbus通信。
		g_dbus_client_new
	GDBusProxy
mainloop.c
object.c
polkit.c
watch.c
```



gdbus.h里主要函数

```
建立连接
g_dbus_setup_bus
	返回conn
新建client
g_dbus_client_new
	参数是conn。service：org.bluez。path：/org/bluez
	
```

然后是做什么呢？

跟client相关的函数：

```
ref
unref
set_connect_watch
	这个一般可以做，回调就是打印一下。没有什么必须做的。
set_disconnect_watch
	跟connect的回调类似。
set_ready_watch
set_signal_watch
set_proxy_handlers
	这个是这样用：
	(client, proxy_added, proxy_removed, property_changed, NULL)
	最后一个参数是userdata。
	这些回调也不是必须的。
	以bluetooth-player.c里的为例子看看。
	也只是做了打印。说明连接断开情况。
	
```

g_dbus_setup_bus

这个里面调用了setup_dbus_with_main_loop

靠g_io_add_watch添加了事件注册。

还有一类重要的东西，就是proxy。

函数调用，都是通过proxy来做的。

例如bluetooth-player.c里。播放操作：

```
g_dbus_proxy_method_call(proxy, "Play", NULL, play_reply,
							NULL, NULL)
```

最重要的也就是这个method_call函数了。



一个简单例子。

```
#include "gdbus.h"
static DBusConnection *dbus_conn;

static GMainLoop *main_loop;

void mainloop_init(void)
{
	main_loop = g_main_loop_new(NULL, FALSE);
}

static void connect_handler(DBusConnection *connection, void *user_data)
{
	printf("connect\n");
}

static void disconnect_handler(DBusConnection *connection, void *user_data)
{
    printf("disconnect\n");
}
int main()
{
    mainloop_init();
    GDBusClient *client;
    dbus_conn = g_dbus_setup_bus(DBUS_BUS_SYSTEM, NULL, NULL);
    client = g_dbus_client_new(dbus_conn, "org.freedesktop.DBus", "/org/freedesktop/DBus");
    g_dbus_client_set_connect_watch(client, connect_handler, NULL);
    g_dbus_client_set_disconnect_watch(client, disconnect_handler, NULL);

    g_main_loop_run(main_loop);

}
```

代码放在https://github.com/teddyxiong53/mygdbus

# 重新学习gdbus

在搭建嵌入式Linux应用软件系统框架时，

常常会将其划分为好几个模块，

每个模块之间的通信方式多数时候都会用到d-bus技术。

目前基于d-bus技术的几种编程框架有：

glib-dbus，GDbus，QtDbus，dbus-python。

这5种编程框架的复杂度有高有低，

最简单的应该非QtDbus莫属了，

最复杂的过程要属glib-dbus。

鉴于我对GDBus的熟悉程度，这里只介绍GDBus的编程过程。



GDBus和glib-dbus都是由GNU组织开发的。

GDBus可以认为是glib-dbus的升级版，

其编程过程比起glib-dbus来要简单得多。

网上有很多讨论glib-dbus编程的，

但就是鲜有讲解GDBus编程过程的，

于是便有了写下这篇文章的初衷。

在展开讲解GDBus编程过程之前，

希望各位看官具备下面列举的一些背景知识，以便更好的理解GDBus编程过程。

不过也可以先跳过这些背景知识，在后面的讲解中如果有不理解的，可以再回过头来看。


一套复杂的应用软件系统肯定会被划分成许多子模块，

每个子模块只负责一个或几个有关的功能。

在Linux下，我们可以将各个子模块实现为一个个进程。

一套完整的系统，就需要各个进程相互配合通信，以交换数据和信息，完成应用系统要求的功能。

比如，以时下流行的车载导航娱乐系统以及车载TBOX终端应用系统为例。

车载导航娱乐系统：

我们可以将其划分为这些模块——USB多媒体、蓝牙电话、蓝牙音乐、收音机、导航、手机互联、倒车后视等。

这些模块都将以进程的方式实现。

这些进程间就需要通信，以达到一个有机有序稳定的车载导航娱乐系统。



车载TBOX终端应用系统：

我们可以将其划分成这些模块——车辆数据采集模块、车辆数据处理模块、车辆数据存储模块、与TSP后台服务器通信模块，

可能还附加与车内移动设备的通信模块。

这些模块也都以进程的方式实现，他们之间的通信，我们都将采用GDBus技术。

这么多进程需要通信，可能有一对一，可能有一对多，多对多的通信方式。

为简单起见，我们假设某个系统中就只有两个进程需要通信——我们称之为Server和Client。

基于GDBus的进程间通信，

最最重要的就是要定义好Server和Client之间的通信接口。

**在GDBus编程框架下，我们使用xml文件来描述接口。**

按照惯常的思路，就是一种数据，一个接口，N多种数据，就要N多个接口，这样的思路简单、便于理解。

```xml
<?xml version="1.0" encoding="UTF-8" ?>  
<node name="/com/company/project/s">
  <interface name="com.company.project.s">
    <method name="SetSomeData">          <!-- method 方法：定义了server提供给client调用的接口名SetSomeData -->
        <arg type="i" name="datatype" direction="in" /> <!-- 定义了接口SetSomeData的参数1：datatype；direction表示值传递方向：“in”表示参数值的传递方向是client到server -->
	<arg type="i" name="data" direction="in" /> <!-- 同上，定义了接口函数SetSomeData的另一个参数，type表示参数类型：“i“表示为gint类型-->
    </method>
    <method name="GetSomeData"> <!-- 定义了server的另一个接口函数GetSomeData -->
        <arg type="i" name="datatype" direction="in" /> <!--  接口函数GetSomeData 的参数1，类型为gint，名字为datatype，值传递方向为 client到 server -->
        <arg type="i" name="retdata" direction="out" /> <!-- 参数2，类型为gint，名字为retdata，值传递方向为 server到client -->
    </method> 
    <signal name="SendMessage"> <!-- 此接口为 server 端使用，不提供给client。server使用此接口，主动向client端发送数据，signal定义的接口是异步的 -->
	<arg type="i" name="signal_id"> <!-- signal接口函数SendMessage 的参数-->
    </signal>
  </interface>
</node>
```

上面的xml文件，共描述了三个接口：

SetSomData、GetSomeData、SendMessage。其注释都已详细附上。

**但是，这样的接口描述方式存在一个非常不便的地方——每种数据一个接口，如果进程间需要交换的数据类型很多的时候，就需要定义非常多的接口，这样xml文件就会变得庞大；**

而且如果进程间交换的某些数据量很大时，这样的接口描述就无能为力了。

因此，有必要找到一种通用的，又能交换大量数据的接口描述方式。



基于上述目的，我们进一步抽象进程间的通信过程时发现——进程间通信不外乎就是下面这几种情况：

1、进程A从进程B中获取数据

2、进程A传递数据给进程B

3、进程B主动传递数据给进程A



![img](../images/playopenwrt_pic/20180503111716599)



显然，这里的进程B就是Server端，进程A就是Client端。

Server端提供给Client端调用的接口应该有：GET、SET；同时Server端还应具备主动向客户端发数据的能力SEND。

因此，基于上述抽象，我们的GDBus接口描述文档应该如下，保存为interface-S.xml文件：

```XML
<?xml version="1.0" encoding="UTF-8" ?>
<node name="/com/company/project/s">
  <interface name="com.company.project.demo.s">
    <method name="Client_request"> <!-- 提供给客户端使用的接口 -->
                <arg type="a*" name="input_array" direction="in" /> <!-- Client 传递给Server 的数据。被抽象为一个通用数组 a* -->
                <arg type="a*" name="output_array" direction="out" /> <!-- client端从server端get 的数据,通过这个参数传递到client端.也是一个抽象的数组 a*-->
                <arg type="i" name="result" direction="out" /> <!-- 接口的返回值，一个整型数 -->
    </method>
    <signal name="Server_message"> <!-- 服务端主动发送数据到客户端 -->
                <arg type="a{ii}" name="message_array" /> <!-- 由key 和 value 组成的 dictionary。仅仅是示例。可以是其他类型 -->
    </signal>
  </interface>
</node>
```

至此，我们已经抽象出所有的通信接口。

接下来，我们要做的工作就是，将这份通用的接口文件转换为C代码文件，以便加入到我们的工程中。



在终端执行如下命令：

gdbus-codegen --generate-c-code=libgdbusdemo_s interface-S.xml

或者写一个shell脚本，将上面的过程写进去，这样就不用每次敲代码，只需执行下脚本，即可产生我们需要的C源文件：libgdbusdemo_s.c libgdbusdemo_s.h。



至此，我们就可以将这两个文件加入到我们的工程中，一起和我们的其他源文件参与编译了。

但是，这还不是最合理的设计，我们的设计应该遵循模块化设计思想，

所以，我们可以将这两个文件单独做成一个静态库。

在编译我们的工程项目时，链接这个库即可。



基于软件设计的原则——低耦合高内聚、可扩展性等，我们大致可画出server端和client端的通信框图如下：

![img](../images/playopenwrt_pic/20180502174044257)



1、gdbus-interface模块：是对前面的接口库提供的单元接口函数的进一步封装。server端和client的封装的函数是有差异的。后续的讲解会提到如何封装。

2、gdbus-server：对gdbus-interface的进一步封装，使其提供给server的其他模块的接口更加简单、方便。

3、gdbus-proxy：也是对gdbus-interface的进一步封装，使其提供给client其他模块的接口更加简单、方便。

先讲Server端的编程过程。

## server端

基于GDBus的server端，可以抽象成两大模块：

数据接收/发送的gdbus-interface模块、

解析/封装通信数据的gdbus-server模块。



gdbus-interface模块向server中的其他模块暴露的接口有：

initialize，deinitialize，run，sendmessage。

具体代码如下（gdbusiface.h）：

```
#ifndef GDBUS_INTERFACE_H
#define GDBUS_INTERFACE_H


#include "libgdbusdemo_s.h"


#ifdef __cplusplus
extern "C"{
#endif

typedef void (*callback_client_request)(GVariant* input_message, GVariant** output_message);

gboolean InitGdbusServer(const gchar* bus_name,const gchar* object_path, callback_client_request callback_funtion);

void run();

gboolean DeinitGdbusServer();

gboolean SendMessage(GVariant* server_message);

#ifdef __cplusplus
}
#endif
```

对应的实现。

```
#include "gdbusiface.h"

static void bus_acquired_cb(
    GDBusConnection *connection,
    const gchar *bus_name,
    gpointer usre_data
);
static void name_acquired_cb(
    GDBusConnection *connection,
    const gchar *bus_name,
    gpointer usre_data
);
static void name_lost_cb(
    GDBusConnection *connection,
    const gchar *bus_name,
    gpointer usre_data
);
static gboolean handle_client_request(
    ComCompanyProjectDemoS *object,
    GDBusMethodInvocation *invocation,
    GVarint *arg_input_array
);

static GMainLoop *g_mainloop = NULL;
static guint g_gdbus_own_name;
static ComCompanyProjectDemoS *g_proxy;
static ComCompanyProjectDemoS *g_skeleton;

static callback_client_request g_callback_function;
const gchar *g_object_path;

gboolean InitGdbusServer(const gchar *bus_name,
    const gchar *object_path,
    callback_client_request callback_function
)
{
    gboolean ret = TRUE;
    GError *pConnError = NULL;
    GError *pProxyError = NULL;
    GDBusConnection *pConnection = NULL;
    g_mainloop = g_main_loop_new(NULL, FALSE);
    g_gdbus_own_name = g_dbus_own_name(G_BUS_TYPE_SESSION,
        bus_name,
        G_BUS_NAME_OWNER_FLAGS_NONE,
        &bus_acquired_cb,
        &name_acquired_cb,
        &name_lost_cb,
        NULL,
        NULL
        );
    g_object_path = object_path;
    g_callback_function = callback_function;
    return ret;
}

gboolean DeinitGdbusServer()
{
    gboolean ret = FALSE;
    if(g_main_loop != NULL) {
        g_main_loop_quit(g_mainloop);
        g_main_loop_unref(g_mainloop);
        g_bus_unown_name(g_gdbus_own_name);
        ret = TRUE;
        g_mainloop = NULL;
        usleep(10*1000);
        if(g_proxy) {
            g_object_unref(g_proxy);
        }
        g_proxy = NULL;
    }
    return ret;
}

void run()
{
    g_main_loop_run(g_mainloop);
}

static void bus_acquired_cb(
    GDBusConnection *connection,
    const gchar *bus_name,
    gpointer usre_data
)
{
    GError *pError = NULL;
    g_skeleton = com_company_project_demo_s_skeleton_new();
    g_signal_connect(g_skeleton, "handle-client-request", G_CALLBACK(handle_client_request), NULL);
    g_dbus_interface_skeleton_export(G_DBUS_INTERFACE_SKELETON(g_skeleton),
        connection,
        g_object_path,
        &pError
    );
    if(pError != NULL) {
        g_error_free(pError);
        g_main_loop_quit(g_mainloop);
    }
}
static void name_acquired_cb(
    GDBusConnection *connection,
    const gchar *bus_name,
    gpointer usre_data
)
{
    printf("name accquried\n");
}

static void name_lost_cb(
    GDBusConnection *connection,
    const gchar *bus_name,
    gpointer usre_data
)
{
    DeinitGdbusServer();
}

static gboolean handle_client_request(
    ComCompanyProjectDemoS *object,
    GDBusMethodInvocation *invocation,
    GVarint *arg_input_array
)
{
    if(g_callback_function) {
        GVariant *output_msg = NULL;
        g_callback_function(arg_input_array, &output_msg);
        if(output_msg) {
            com_company_project_demo_s_complete_client_request(
                object, invocation, output_msg, 1
            );
        }
    }
    return TRUE;
}

gboolean SendMessage(GVariant *server_message)
{
    if(g_skeleton != NULL) {
        com_company_project_demo_s_emit_server_message(g_skeleton, server_message);
        g_variant_unref(server_message);
        return TRUE;
    }
    return FALSE;
}

```

# 完全通用的协议接口文档

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<node name="/com/company/project/dbus/s">
  <interface name="com.company.project.dbus.s">
    <method name="SetValue">
                <arg type="i" name="type" direction="in" /> 		<!-- op type -->
                <arg type="s" name="input_array" direction="in" />	<!-- input value array-->
                <arg type="i" name="result" direction="out" />
    </method>
    <method name="GetValue">
                <arg type="i" name="type" direction="in" />             <!-- input op type -->
				<arg type="s" name="input_array" direction="in" />	<!-- input value array-->
                <arg type="s" name="output_array" direction="out" />   <!-- output value array -->
                <arg type="i" name="result" direction="out" />
    </method>
    <signal name="Message">
                <arg type="s" name="message_array" /> 		<!-- message array-->
    </signal>
  </interface>
</node>
```

对上面的xml稍作解释

客户端调用服务端的method时，传递的参数可归纳为只有2个：

type-操作类型；input_array-参数。

接口定义文档要做到通用，这个参数就必须为string类型。

为什么string类型可以做到通用呢？

原因就是——我们可以将所有类型的数据使用json转换成字串类型，这一点灵感来自网络通信。

有了json的加持，我们采用dbus通信就非常方便了，开发人员在调试、改变接口时，

不再需要重新生成协议源码文件，只需要修改代码即可；

另外，使用dbus-monitor工具时，也能使用字串调试。

相比QDBus中的QVariant类型、Glib中的GVariant类型，调试方便得很了。



# call和complete

好像是client这边调用call函数，server这边调用complete函数。

server这边分配的内存，在client这边进行了释放？

可以这样吗？

还没有找到明确说法。

# chatpgt重新梳理

## g_bus_own_name 分析

`g_bus_own_name` 是 GLib 库中的一个函数，用于在 D-Bus 总线上注册和拥有一个特定的名字。下面是对 `g_bus_own_name` 函数的分析：

函数签名：
```c
guint g_bus_own_name(GDBusConnection *connection,
                    const gchar *name,
                    GDBusProxyFlags flags,
                    GBusAcquiredCallback bus_acquired_handler,
                    GBusNameAcquiredCallback name_acquired_handler,
                    GBusNameLostCallback name_lost_handler,
                    gpointer user_data,
                    GDestroyNotify user_data_free_func);
```

参数说明：
- `connection`：要注册名字的 D-Bus 连接。
- `name`：要注册的名字。
- `flags`：DBus 代理的标志，指定代理的行为。
- `bus_acquired_handler`：当成功获取总线拥有权时调用的回调函数。
- `name_acquired_handler`：当成功获取指定名字的拥有权时调用的回调函数。
- `name_lost_handler`：当失去指定名字的拥有权时调用的回调函数。
- `user_data`：传递给回调函数的用户数据。
- `user_data_free_func`：用于释放用户数据的回调函数。

功能说明：
`g_bus_own_name` 函数用于在 D-Bus 总线上注册一个名字并拥有它。当成功获取名字的拥有权后，会调用 `bus_acquired_handler` 回调函数。如果指定的名字已经被其他进程拥有，函数将等待直到该名字被释放，并在成功获取拥有权后调用 `name_acquired_handler` 回调函数。如果在尝试获取名字拥有权的过程中出现错误或超时，会调用 `name_lost_handler` 回调函数。通过这些回调函数，开发人员可以处理和响应名字拥有权的变化。

该函数适用于基于 D-Bus 的应用程序开发，允许应用程序在 D-Bus 总线上注册和管理自己的名字，以便与其他应用程序进行通信和交互。

## glib dbus介绍

GLib D-Bus 是一个基于 GLib 库的 D-Bus 消息传递系统的实现。GLib D-Bus 提供了在应用程序中使用 D-Bus 进行进程间通信的功能。

以下是 GLib D-Bus 的一些重要特性和组件：

1. D-Bus 连接管理：GLib D-Bus 提供了 `GDBusConnection` 对象，用于建立和管理与 D-Bus 服务器的连接。可以使用 `g_bus_get` 或 `g_bus_get_sync` 函数来获取 D-Bus 连接。

2. D-Bus 代理和接口：GLib D-Bus 允许创建 D-Bus 代理和接口来进行进程间通信。通过 `GDBusProxy` 和 `GDBusInterface` 对象，可以定义和实现 D-Bus 的方法、信号和属性。

3. D-Bus 消息传递：GLib D-Bus 提供了 `GDBusMessage` 对象，用于创建、发送和接收 D-Bus 消息。可以使用 `g_dbus_connection_send_message` 函数发送消息，并使用 `g_dbus_connection_send_message_with_reply` 函数发送带回复的消息。

4. D-Bus 信号处理：GLib D-Bus 提供了 `GDBusSignalFlags` 和 `GDBusSignalCallback`，用于注册和处理 D-Bus 信号。可以使用 `g_signal_connect` 或 `g_signal_connect_data` 函数来连接信号回调函数。

5. D-Bus 事件循环：GLib D-Bus 提供了 `GDBusObjectManager` 和 `GDBusObjectProxy`，用于在事件循环中管理和监视 D-Bus 对象。可以使用 `g_dbus_object_manager_server_start` 函数启动对象管理器，并使用 `g_dbus_object_proxy_new` 函数创建对象代理。

通过使用 GLib D-Bus，开发人员可以方便地使用 D-Bus 进行进程间通信，并利用 GLib 提供的功能来简化和抽象底层的 D-Bus 操作。GLib D-Bus 提供了一种方便、跨平台的方式来开发支持 D-Bus 的应用程序，使开发人员能够更容易地与其他应用程序进行交互和通信。

## gdbus xml定义说明

在使用 GLib 的 GDBus 库进行 D-Bus 编程时，可以使用 XML 文件来定义 D-Bus 接口、对象和信号的结构。这种 XML 文件称为 GDBus XML 定义文件。

GDBus XML 定义文件使用一种特定的格式来描述 D-Bus 接口和相关内容。以下是 GDBus XML 定义文件的一些常见元素和其说明：

1. `<node>` 元素：表示 D-Bus 对象的根节点，包含一个或多个接口。
2. `<interface>` 元素：定义 D-Bus 接口，包含方法、信号和属性的描述。
3. `<method>` 元素：定义 D-Bus 接口的方法，包含方法名称、输入参数和输出参数的描述。
4. `<signal>` 元素：定义 D-Bus 接口的信号，包含信号名称和参数的描述。
5. `<property>` 元素：定义 D-Bus 接口的属性，包含属性名称、类型和访问权限的描述。
6. `<annotation>` 元素：用于添加元数据或注释到 D-Bus 接口、方法、信号或属性中。

通过使用 GDBus XML 定义文件，可以在代码中通过 `g_dbus_node_info_new_for_xml()` 函数加载 XML 文件并生成相应的 `GDBusNodeInfo` 结构，其中包含了从 XML 文件中解析出来的 D-Bus 接口、对象和信号的信息。

使用 GDBus XML 定义文件可以更方便地定义和管理 D-Bus 接口和相关内容，使得 D-Bus 编程更加简单和灵活。

以下是一个示例的 GDBus XML 定义文件的结构：

```xml
<node>
  <interface name="org.example.MyInterface">
    <method name="DoSomething">
      <arg type="s" direction="in" name="input" />
      <arg type="s" direction="out" name="output" />
    </method>
    <signal name="StateChanged">
      <arg type="b" name="new_state" />
    </signal>
    <property name="SomeProperty" type="i" access="readwrite" />
  </interface>
</node>
```

上述示例定义了一个名为 `org.example.MyInterface` 的 D-Bus 接口，其中包含了一个名为 `DoSomething` 的方法、一个名为 `StateChanged` 的信号，以及一个名为 `SomeProperty` 的属性。

使用 GDBus XML 定义文件可以更方便地定义 D-Bus 接口的结构，使得 D-Bus 编程更加清晰和可维护。

## gdbus call_*_sync函数

`gdbus_call_*_sync()` 函数是 GLib 提供的用于进行同步调用 D-Bus 方法的函数系列。这些函数用于向指定的 D-Bus 对象发送方法调用请求，并等待对方返回结果。

这些函数的命名规则是 `gdbus_call_*_sync()`，其中 `*` 可以是不同的后缀，表示不同的数据类型和参数组合。常见的后缀包括：

- `_sync`：表示同步调用，即发送请求后会等待对方返回结果，直到结果返回或超时。
- `_finish`：用于获取异步调用的结果，需要与相应的异步函数配对使用。

下面是一些常用的 `gdbus_call_*_sync()` 函数示例：

- `gdbus_call_sync()`：用于发送无输入参数、无返回值的方法调用请求。
- `gdbus_call_with_unix_fd_list_sync()`：用于发送包含 Unix 文件描述符的方法调用请求。
- `gdbus_call_with_unix_fd_list_finish()`：用于获取包含 Unix 文件描述符的方法调用的结果。

这些函数的使用方式是提供 D-Bus 连接、目标对象路径、方法名以及其他必要的参数，然后调用相应的函数进行同步调用。函数会阻塞当前线程，直到接收到对方返回的结果或超时。

需要注意的是，`gdbus_call_*_sync()` 函数是同步调用，会阻塞当前线程。如果需要异步调用，可以使用对应的异步函数，并通过回调函数处理结果。

# gpt帮忙生成一个通用的框架

prompt：

```
请扮演一个Linux gdbus方面的专家。
我现在需要使用gdbus配合gdbus-codegen工具来生成一个通用的进程通信代码框架。
这个框架包含server.c和client.c 这两部分。
二者之间的通信在gdbus之上，通信内容格式是json格式。
json使用cjson来实现。
请提供完整的代码实现：
包括xml文件、server.c、client.c。已经对应的测试文件。
并提供一个Makefile，以便我可以直接编译进行测试。
```

输出内容：

好的，我可以帮你完成这个任务。以下是所需的代码实现、XML 文件、Makefile 和测试文件。

首先，我们需要创建一个 XML 文件来描述我们的 D-Bus 接口。我们将命名为 "com.example.SampleInterface"，其中包含两个方法：`SendMessage` 和 `ReceiveMessage`。这里是 `com.example.SampleInterface.xml` 的内容：

```xml
<!DOCTYPE node PUBLIC "-//freedesktop//DTD D-BUS Object Introspection 1.0//EN"
                      "http://www.freedesktop.org/standards/dbus/1.0/introspect.dtd">
<node>
  <interface name="com.example.SampleInterface">
    <method name="SendMessage">
      <arg type="s" direction="in"/>
      <arg type="s" direction="out"/>
    </method>
    <method name="ReceiveMessage">
      <arg type="s" direction="out"/>
    </method>
  </interface>
</node>
```

接下来，我们使用 `gdbus-codegen` 工具根据 XML 文件生成 C 代码。运行以下命令：

```bash
gdbus-codegen --c-generate-source --generate-docbook --interface-prefix com.example. --output server-generated --c-namespace Example com.example.SampleInterface.xml
```

这将生成名为 `server-generated.h` 和 `server-generated.c` 的文件。

然后，我们需要编写服务器端的代码。创建一个名为 `server.c` 的文件，并将以下内容复制到其中：

```c
#include <glib.h>
#include <gio/gio.h>
#include <stdio.h>
#include <stdlib.h>
#include "server-generated.h"
#include <cjson/cJSON.h>

static gchar* process_message(const gchar* json_message) {
    // 在这里处理 JSON 消息并返回结果
    cJSON* root = cJSON_Parse(json_message);
    cJSON* message = cJSON_GetObjectItem(root, "message");

    if (message) {
        printf("Received message: %s\n", message->valuestring);

        // 构造回复消息
        cJSON* response = cJSON_CreateObject();
        cJSON_AddStringToObject(response, "reply", "Message received successfully!");
        char* json_response = cJSON_PrintUnformatted(response);

        cJSON_Delete(response);
        cJSON_Delete(root);

        return json_response;
    }

    cJSON_Delete(root);
    return NULL;
}

static void on_bus_acquired(GDBusConnection *connection, const gchar *name, gpointer user_data) {
    GError *error = NULL;

    // 在 D-Bus 上注册一个对象和接口
    g_dbus_interface_skeleton_export(G_DBUS_INTERFACE_SKELETON(user_data), connection,
                                     "/com/example/SampleObject", &error);
    if (error != NULL) {
        g_printerr("Failed to export D-Bus interface: %s\n", error->message);
        g_error_free(error);
    } else {
        g_print("D-Bus interface exported successfully\n");
    }
}

int main() {
    GMainLoop *loop;
    GError *error = NULL;

    // 初始化 GIO 和 D-Bus
    g_type_init();
    loop = g_main_loop_new(NULL, FALSE);

    // 创建一个 D-Bus 的 GMainBusType
    GDBusConnection *connection = g_bus_get_sync(G_BUS_TYPE_SESSION, NULL, &error);
    if (error != NULL) {
        g_printerr("Failed to connect to D-Bus: %s\n", error->message);
        g_error_free(error

);
        exit(1);
    }

    // 创建一个对象和接口
    ExampleSampleInterfaceSkeleton *skeleton = example_sample_interface_skeleton_new();
    g_signal_connect(skeleton, "handle-send-message", G_CALLBACK(process_message), NULL);

    // 请求一个 D-Bus 名称
    guint owner_id = g_bus_own_name(G_BUS_TYPE_SESSION, "com.example.SampleService",
                                    G_BUS_NAME_OWNER_FLAGS_NONE, NULL,
                                    on_bus_acquired, NULL, skeleton, NULL);

    g_print("Server is running...\n");
    g_main_loop_run(loop);

    // 清理资源
    g_bus_unown_name(owner_id);
    g_object_unref(skeleton);
    g_object_unref(connection);
    g_main_loop_unref(loop);

    return 0;
}
```

接下来，我们编写客户端的代码。创建一个名为 `client.c` 的文件，并将以下内容复制到其中：

```c
#include <glib.h>
#include <gio/gio.h>
#include <stdio.h>
#include <stdlib.h>
#include "server-generated.h"
#include <cjson/cJSON.h>

int main() {
    GMainLoop *loop;
    GError *error = NULL;

    // 初始化 GIO 和 D-Bus
    g_type_init();
    loop = g_main_loop_new(NULL, FALSE);

    // 创建一个 D-Bus 的 GMainBusType
    GDBusConnection *connection = g_bus_get_sync(G_BUS_TYPE_SESSION, NULL, &error);
    if (error != NULL) {
        g_printerr("Failed to connect to D-Bus: %s\n", error->message);
        g_error_free(error);
        exit(1);
    }

    // 获取远程对象
    GDBusProxy *proxy = g_dbus_proxy_new_sync(connection, G_DBUS_PROXY_FLAGS_NONE, NULL,
                                              "com.example.SampleService", "/com/example/SampleObject",
                                              "com.example.SampleInterface", NULL, &error);
    if (error != NULL) {
        g_printerr("Failed to create D-Bus proxy: %s\n", error->message);
        g_error_free(error);
        exit(1);
    }

    // 构造 JSON 消息
    cJSON* root = cJSON_CreateObject();
    cJSON_AddStringToObject(root, "message", "Hello from client!");
    char* json_message = cJSON_PrintUnformatted(root);

    // 调用 D-Bus 方法
    GVariant *result = g_dbus_proxy_call_sync(proxy, "SendMessage", g_variant_new("(s)", json_message),
                                              G_DBUS_CALL_FLAGS_NONE, -1, NULL, &error);
    if (error != NULL) {
        g_printerr("Failed to call D-Bus method: %s\n", error->message);
        g_error_free(error);
        exit(1);
    }

    // 解析返回结果
    const gchar* reply;
    g_variant_get(result, "(s)", &reply);

    // 在这里处理返回结果
    cJSON* response = cJSON_Parse(reply);
    cJSON* reply_message = cJSON_GetObjectItem(response, "reply");
    if (reply_message) {
        printf("Received reply: %s\n", reply_message->valuestring);
    }

    // 清理资源
    cJSON_Delete(response);
    g_variant_unref(result);
    g_free(json_message);
    g_object_unref(proxy);
    g_object_unref(connection);
    g_main_loop_unref(loop);

    return 0;
}
```

现在，我们需要创建一个 Makefile，以便可以方便地编译和运行我们的代码。创建一个名为 `Makefile

` 的文件，并将以下内容复制到其中：

```Makefile
CC = gcc
CFLAGS = -Wall `pkg-config --cflags glib-2.0 gio-2.0`
LDFLAGS = `pkg-config --libs glib-2.0 gio-2.0`
CJSON_DIR = /path/to/cjson # 替换为 cjson 的安装路径

all: server client

server: server.c server-generated.c
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS) -I$(CJSON_DIR)/include -L$(CJSON_DIR)/lib -lcjson

client: client.c
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS) -I$(CJSON_DIR)/include -L$(CJSON_DIR)/lib -lcjson

clean:
	rm -f server client

.PHONY: clean
```

请将 `CJSON_DIR` 替换为 `cjson` 库的实际安装路径。

最后，我们需要创建一个测试文件，用于测试我们的代码。创建一个名为 `test.sh` 的文件，并将以下内容复制到其中：

```bash
#!/bin/bash

# 编译
make

# 启动服务器
./server &

# 等待服务器启动
sleep 1

# 启动客户端
./client

# 清理
killall server
make clean
```

现在，您可以运行 `test.sh` 脚本进行测试：

```bash
chmod +x test.sh
./test.sh
```

这样就完成了使用 gdbus 和 cjson 进行进程通信的通用代码框架的实现。希望对您有所帮助！

# g_bus_get_sync 和g_dbus_connection_close_sync

g_bus_get_sync 和g_dbus_connection_close_sync，是出自同一套库吗？为什么一个以g_bus为前缀，一个以g_dbus为前缀，风格不统一

`g_bus_get_sync` 和 `g_dbus_connection_close_sync` 确实出自同一套库：GLib 的 GIO 模块。然而，这两个函数的前缀不同 (`g_bus` 和 `g_dbus`) 是因为它们属于不同的命名空间或功能集合。

### 命名空间解释

1. **g_bus_get_sync**:
   - 前缀 `g_bus` 表示它是与 D-Bus 相关的“总线”操作的函数。这些函数通常用于获取与 D-Bus 系统总线或会话总线的连接。
   - 这个命名空间中的其他函数还包括 `g_bus_watch_name`, `g_bus_own_name`, 等等，这些都涉及总线级别的操作。

2. **g_dbus_connection_close_sync**:
   - 前缀 `g_dbus_connection` 表示它是与 D-Bus 连接操作相关的函数。这些函数通常用于处理具体的 D-Bus 连接实例，比如打开或关闭连接、发送消息、接收消息等。
   - `g_dbus_connection` 命名空间中的其他函数还包括 `g_dbus_connection_new`, `g_dbus_connection_send_message`, 等等。

### 命名空间区分的原因

GLib 和 GIO 库中采用这种命名约定是为了区分不同类别的功能和操作：

- **g_bus** 前缀的函数主要是与 D-Bus 总线的整体管理和监控相关。
- **g_dbus_connection** 前缀的函数是具体处理 D-Bus 连接的操作。

这种命名空间区分有助于开发者理解和查找相关功能，同时避免函数命名冲突。尽管两者都涉及 D-Bus 操作，但它们作用的层次和场景不同，因此使用了不同的前缀来明确各自的用途。

# g_dbus_connection_call和g_dbus_connection_call_finish 

- `g_dbus_connection_call` 是一个异步方法调用，可以通过设置回调函数来处理异步操作的完成。返回值是一个 `GDBusProxy` 对象，表示方法调用的代理对象。
- `g_dbus_connection_call_finish` 是 GLib 中与 `g_dbus_connection_call` 函数配套使用的函数，用于获取异步 D-Bus 方法调用的结果。`GAsyncResult` 类型的异步操作结果。用完结果后，要在回调函数里释放结果的指针。



# 参考资料

1、gdbus

https://developer.gnome.org/gio/stable/gdbus.html

2、基于GDBus技术的IPC通信编程详解(1)

这篇讲得很好，一看就懂了。

https://blog.csdn.net/adlindary/article/details/80167840