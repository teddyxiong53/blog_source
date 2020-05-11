---
title: Linux之gdbus
date: 2020-05-09 14:59:08
tags:
	- Linux

---

1

bluez里的所谓gdbus，是自己用glib简单封装了一下dbus的接口。

新建一个hello.xml文件，内容如下：

```
<?xml version="1.0" encoding="UTF-8" ?>

<node name="/com/yft/hello">
	<interface name="com.yft.hello.test">
		<method name="setVersion">
			<arg name="version" type="s" direction="in" />
		</method>
		<signal name="testStatus">
			<arg name="status" type="i" />
		</signal>
	</interface>
</node>
```

然后执行下面的命令：

```
gdbus-codegen --generate-c-code=Hello  --c-namespace hello --interface-prefix com.yft.hello. hello.xml
```

就会生成一个Hello.c和一个Hello.h。文件内容非常长。

新建server.c和client.c。

Makefile

```
.PHON: all
LIBS := -I/usr/include/glib-2.0 -I/usr/lib/x86_64-linux-gnu/glib-2.0/include -I/usr/include/gio-unix-2.0 -lpthread -lgio-2.0 -lgobject-2.0 -lgmodule-2.0 -lgthread-2.0 -lrt -lglib-2.0
all:
	gcc server.c Hello.c -o server $(LIBS)
	gcc client.c Hello.c -o client $(LIBS)
```

然后运行需要在图形界面下运行，不然会出错。



参考资料

1、基于GDBUS 的例子

https://blog.csdn.net/snakezy1988/article/details/103522742