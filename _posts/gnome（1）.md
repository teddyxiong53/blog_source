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



编译gedit的代码。

https://github.com/GNOME/gedit

必须用git clone的方式来做。下载压缩包不行，因为还依赖了其他的工程。

gnome的音乐应用，是用python写的。这个会是gnome上的主流吗？可能会，至少说明目前用C语言来开发，确实比较费力。而python比较省力。gnome目前还是缺失应用，而不是应用的效率。所以当务之急是先产生足够多的应用。

https://github.com/GNOME/gnome-music

计算器应用，是用vala语言写的。

vala是gnome社区开发的编程语言。



# gnome music

从github下载代码，

```
mkdir _build
meson.py _build
```

然后需要安装这个。

```
sudo apt-get install  libgirepository1.0-dev
```

但是还是出错，提示gtk版本太低了。

写在我升级一下gtk版本。

```
sudo add-apt-repository ppa:gnome3-team/gnome3-staging
sudo add-apt-repository ppa:gnome3-team/gnome3
sudo apt update
sudo apt dist-upgrade
```

这个需要下载400M左右的东西。

还是不行，版本要求太严格了。

不继续编译了。



参考资料

1、官网

https://developer.gnome.org/references

2、

https://access.redhat.com/documentation/zh-cn/red_hat_enterprise_linux/7/html/desktop_migration_and_administration_guide/what-is-gnome-classic

3、官方应用

https://wiki.gnome.org/Apps

4、升级Ubuntu16.04的gtk版本

https://www.omgubuntu.co.uk/2016/05/install-gnome-3-20-ubuntu-16-04-lts