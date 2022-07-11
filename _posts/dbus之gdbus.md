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



# 参考资料

1、gdbus

https://developer.gnome.org/gio/stable/gdbus.html

2、基于GDBus技术的IPC通信编程详解(1)

这篇讲得很好，一看就懂了。

https://blog.csdn.net/adlindary/article/details/80167840