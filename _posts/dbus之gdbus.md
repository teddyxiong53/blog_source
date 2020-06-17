---
title: dbus之gdbus
date: 2020-06-16 14:14:49
tags:
	- dbus

---

1

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



参考资料

1、gdbus

https://developer.gnome.org/gio/stable/gdbus.html