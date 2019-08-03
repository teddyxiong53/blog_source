---
title: gnome（1）
date: 2019-07-26 11:49:19
tags:
	- gnome

---



api分类

```
核心库
	核心
		glib
		gio
			提供了对文件系统的访问。
		GObject
	用户界面
	多媒体
		gstreamer
```



为了方便开发，官方提供了一个模板。

https://wiki.gnome.org/AppsTemplate

但是下载不了。

github上有。从这里下载。

https://github.com/ikeydoherty/gnome-app-templates

在我的笔记本上，执行autogen.sh脚本。出错。

```
src/Makefile.am:34: error: HAVE_INTROSPECTION does not appear in AM_CONDITIONAL
```

执行下面的命令，安装这个就可以。

```
sudo apt-get install gobject-introspection
```

编译处理，只有一个动态库。怎么使用呢？



参考资料

1、官网

https://developer.gnome.org/references

2、

https://access.redhat.com/documentation/zh-cn/red_hat_enterprise_linux/7/html/desktop_migration_and_administration_guide/what-is-gnome-classic

3、官方应用

https://wiki.gnome.org/Apps

4、

