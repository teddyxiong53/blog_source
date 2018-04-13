---
title: openwrt（十一）ubus
date: 2018-04-13 14:42:23
tags:
	- openwrt

---



ubus是openwrt里守护进程和应用之间通信的桥梁，类似于桌面系统里的dbus。

设计理念也跟dbus的一样。区别在于简化了。u代表的就是micro的意思，微型。

目标也是提供系统级的ipc和rpc。

都是基于socket来实现的。

ubus具有很好的可移植性。



核心部分是ubusd。

还有一个库libusbd。



# 命令行的ubus工具

ubus

```
root@LEDE:/# ubus list
dhcp
hnet
hostapd.wlan0
log
network
network.device
network.interface
network.interface.lan
network.interface.loopback
network.wireless
service
session
system
uci
```

查看某一项的详细信息。

```
root@LEDE:/# ubus -v list dhcp
'dhcp' @d628a667
        "ipv4leases":{}
        "ipv6leases":{}
```

# ubus的实现框架

ubus实现的基础是unix socket，就是本地socket。

unix socket工作的框架：

1、建立一个socket server端，绑定到一个socket文件。监听client的连接。

2、建立一个或者多个client端，连接到server。

3、client和server直接互相发送消息。

ubus的server端就是ubusd。

client端的实现，可以用shell、lua、C这3种语言来写。

# ubus的应用场景和局限性

ubus可以用于2个进程之间的通信，数据用类似json的格式进行组织。

常用的场景是：

1、进程A注册一系列的服务。进程B去调用这些服务。

2、订阅通知。

由于ubus实现方式的限制，ubus有这些局限性：

1、数据量不能太大，也不能太频繁。一次超过60KB，就不能正常工作了。

2、对多线程支持不好。如果多个线程中去请求同一个服务，就有不可预知的结果。

3、不要递归调用。



# 在Ubuntu上安装ubus

##安装libubus。

1、下载。

```
git clone git://git.openwrt.org/project/libubox.git
```

2、编译。

```
teddy@teddy-ubuntu:~/work/ubus/libubox$ mkdir build
teddy@teddy-ubuntu:~/work/ubus/libubox$ cd build/
teddy@teddy-ubuntu:~/work/ubus/libubox/build$ cmake ../
```

提示没有安装lua。安装。

```
sudo apt-get install lua5.2
```

提示没有json。安装。

```
libjson-c-dev
```

make还是出错。提示lua的头文件没有。再安装下面的。

```
 sudo apt-get install liblua5.1-0-dev 
```

安装还是不行，我修改ubus/CMakeLists.txt文件。这里指定lua的目录。

```
ADD_DEFINITIONS(-Os -Wall -Werror --std=gnu99 -g3 -Wmissing-declarations -I/usr/include/lua5.1)
```

再编译就好了。

3、sudo make install

这就安装好了。但是现在安装的还只是libubus

## 安装ubus工具

1、下载。

```
git clone git://nbd.name/luci2/ubus.git
```

2、编译。

这个很顺利了。cmake、make、make install。没有碰到问题。

3、启动服务。

```
teddy@teddy-ubuntu:~/work/ubus/ubus/build$ ubus listen &
[1] 36546
teddy@teddy-ubuntu:~/work/ubus/ubus/build$ ubus: error while loading shared libraries: libubox.so: cannot open shared object file: No such file or directory

[1]+  Exit 127                ubus listen
```

说找不到libubox.so。但是在/usr/local/lib目录下，有这个文件。

那就要更新链接库的目录。

执行一下：

```
sudo ldconfig
```

就好了。

查看服务：

```
teddy@teddy-ubuntu:~/work/ubus/ubus/build$ ubus listen &
[1] 36565
teddy@teddy-ubuntu:~/work/ubus/ubus/build$ sudo systemctl start ubus.service
teddy@teddy-ubuntu:~/work/ubus/ubus/build$ sudo systemctl status ubus.service
● ubus.service - OpenWrt micro bus
   Loaded: loaded (/usr/lib/systemd/system/ubus.service; static; vendor preset: ena
   Active: active (running) since 五 2018-04-13 15:49:51 CST; 1min 0s ago
 Main PID: 36566 (ubusd)
    Tasks: 1
   Memory: 88.0K
      CPU: 864us
   CGroup: /system.slice/ubus.service
           └─36566 /usr/local/sbin/ubusd

4月 13 15:49:51 teddy-ubuntu systemd[1]: Started OpenWrt micro bus.
4月 13 15:50:43 teddy-ubuntu systemd[1]: Started OpenWrt micro bus.
teddy@teddy-ubuntu:~/work/ubus/ubus/build$ 
```

是正常的了。

让普通用户可以读写这个文件。

```
sudo chmod 777 /var/run/ubus.sock
```



## 写代码测试

目录情况是这样。

```
teddy@teddy-ubuntu:~/work/test/ubus$ ls
client  client.c  Makefile  server  server.c
```

Makefile：

```
.PHONY: all clean
CFLAGS := -lubus -lubox -lblobmsg_json -levent
all:
	gcc server.c -o server $(CFLAGS) 
	gcc client.c -o client $(CFLAGS) 
clean:
	rm -f  *.o server client
```

server.c

```
#include <event2/event.h>
#include <libubus.h>
#include <libubox/blobmsg_json.h>


static struct ubus_event_handler listener;


static void receive_event(struct ubus_contex *ctx, struct ubus_event_handler *ev,
     const char * type, struct blob_attr *msg)
{
    char *str;
    str = blobmsg_format_json(msg, true);
    printf("%s: %s\n",type, str);
    free(str);
}

static void signal_cb(evutil_socket_t fd, short event, void *arg)
{
    struct event_base *evloop  = arg;
    event_base_loopbreak(evloop);
}

void cb(evutil_socket_t fd, short what, void *arg)
{
    struct ubus_contex *ctx = arg;
    ubus_handle_event(ctx);
}

int main(int argc, char **argv)
{
    char *ubus_socket = "/var/run/ubus.sock";
    struct ubus_context *ctx = ubus_connect(ubus_socket);
    if(!ctx) {
        printf("failed to connect to ubus");
        return -1;
    }
    listener.cb = receive_event;
    int ret = ubus_register_event_handler(ctx, &listener, "foo");
    if(ret) {
        printf("register event failed\n");
        return ret;

    }
    struct event_base *evloop = event_base_new();

    struct event *signal_int = evsignal_new(evloop, SIGINT, signal_cb, evloop);
    event_add(signal_int, NULL);

    struct event *e = event_new(evloop, ctx->sock.fd, EV_READ|EV_PERSIST, cb, ctx);
    event_add(e, NULL);

    event_base_dispatch(evloop);

    event_free(signal_int);
    event_free(e);
    event_base_free(evloop);

    ubus_free(ctx);

    return 0;
}
```

client.c

```
#include <libubus.h>
#include <libubox/blobmsg_json.h>

static struct blob_buf b;

int main(int argc, char **arg)
{
    const char *ubus_socket = "/var/run/ubus.sock";
    struct ubus_context *ctx  = ubus_connect(ubus_socket);
    if(!ctx) {
        printf("connect to ubus failed\n");
        return -1;
    }
    blob_buf_init(&b, 0);
    bool ret = blobmsg_add_json_from_string(&b, "{\"a\":\"b\"}");
    if(!ret) {
        printf("add msg failed\n");
        return -1;
    }
    ubus_send_event(ctx, "foo", b.head);
    blob_buf_free(&b);
    ubus_free(ctx);
    return 0;
}
```

测试：

1、在一个shell运行

```
./server
```

2、再开一个shell，运行。

```
./client
```

3、然后可以在server那边看到：

```
teddy@teddy-ubuntu:~/work/test/ubus$ ./server
foo: {"a":"b"}
```



# 命令行工具深入

```
root@LEDE:/# ubus -v list dhcp
'dhcp' @d628a667
        "ipv4leases":{}
        "ipv6leases":{}
root@LEDE:/# ubus call dhcp ipv4leases
{
        "device": {
                "br-lan": {
                        "leases": [
                                {
                                        "mac": "940e6b67ec5a",
                                        "hostname": "HUAWEI_Mate_10-a13ea6ed29",
                                        "flags": [
                                                "bound"
                                        ],
                                        "ip": "192.168.0.103",
                                        "valid": 28240
                                },
                                {
                                        "mac": "b40b44edfc0d",
                                        "hostname": "Smartisan-U3-Pro",
                                        "flags": [
                                                "bound"
                                        ],
                                        "ip": "192.168.0.244",
                                        "valid": 29887
                                }
                        ]
                }
        }
}
```

ubus list看到的东西，就是一个个的namespace。

call是调用namespace里的 函数 。

shell脚本的例子。

```
#!/bin/sh

. /usr/share/libubox/jshn.sh

dev="$(uci get network.lan.ifname)"
echo $dev

json_load "$(devstatus $dev)"
json_get_var var1 speed
json_get_var var2 link

echo "speed: $var1"
echo "link: $var2"
```

测试：

```
root@LEDE:~/work/test/shell# ./test.sh 
eth0
speed: 100F
link: 
```



# 参考资料

1、ubus (OpenWrt micro bus architecture)

https://wiki.openwrt.org/zh-cn/doc/techref/ubus

2、Openwrt netifd ubus解析（三）

https://blog.csdn.net/bingyu9875/article/details/62422933

3、[openwrt] 使用ubus实现进程通信

https://blog.csdn.net/jasonchen_gbd/article/details/45627967

4、[openwrt] ubus实现进程间通信举例

https://blog.csdn.net/jasonchen_gbd/article/details/46055885

5、ubus-demo

https://github.com/mehlis/ubus-demo