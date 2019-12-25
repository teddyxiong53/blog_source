---
title: dlna（1）
date: 2018-06-21 15:19:08
tags:
	- dlna

---



dlna是数字生活网络联盟的缩写。

目的是建立电脑、电器、移动设备之间的互联互通。

5个功能组件。



DLNA 宣布组织在2017年1月15日正式解散，未来不会再更新DLNA标准。



 https://github.com/mrjimenez/pupnp



音箱有dlna功能，手机跟音箱在同一个局域网。

手机打开QQ音乐播放器，点击左下角的Q图标，就可以选择连接到音箱。



电脑和手机的互通

电脑上，win7的。Windows media Player里的媒体流里设置。

手机上安装MirageDLNA软件。

这样手机和电脑就能互相看到对方了，可以播放对方的文件。



Ubuntu下搭建dlna环境

安装：

```
sudo apt-get install minidlna
```

配置文件是/etc/minidlna.conf

minidlna是一个dlna服务。

默认的配置情况：

```
# 媒体目录
media_dir=/var/lib/minidlna
```



使用vlc播放器来播放dlna

点击：视图，播放列表。

弹出的界面，往下拉，可以看到通用即插即播upnp的。



# 参考资料

1、

https://www.jb51.net/diannaojichu/144125.html