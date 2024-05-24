---
title: Linux桌面软件打包方式Flatpak
date: 2024-05-24 19:56:17
tags:
	- Linux

---

--



***\*Flatpak\****(前世为xdg-app) 是一种用于构建，分发，安装和运行应用程序的技术。

它主要针对的是Linux桌面，

通过在沙箱中隔离应用程序来提高Linux桌面的安全性，

允许应用程序安装在任何Linux发行版上。

***\*历史：\****

2013: 在[GNOME Developer Experience hackfest, Brussels](https://wiki.gnome.org/DeveloperExperience/Hackfest2013)大会后，萌生在GNOME中使用应用程序容器技术的念头，次年开始开发。

2016年5月: 第一个主版本xdg-app发布。

　　 6月：重命名为flatpak。

　　　 8月：endless OS 3.0, 第一个默认支持Flatpak的发行版。

​      11月：ClearLinux声明采用flatpak。

2017年2月： 最新的flatpak已经可以在Arch, Debian, Fedora, Gentoo, Mageia, openSUSE, Ubuntu等的最新版本上运行。



不依赖于特定发行版的包装格式在Linux生态系中在Flatpak前早已被提出过数次。

2000年代早期，[autopackage](https://zh.wikipedia.org/wiki/Autopackage)开始，

2004年则是klik，

这也提供了Alexander Larsson灵感，

于2007年开发出*glick*项目[[14\]](https://zh.wikipedia.org/wiki/Flatpak#cite_note-14)。

到了2014年，klik便演化成AppImage，

其目标是成为不依赖于特定散布版的[便携式](https://zh.wikipedia.org/wiki/可攜式軟體)上游打包格式。

[Canonical公司](https://zh.wikipedia.org/wiki/Canonical公司)则于2016年发布了[Snappy](https://zh.wikipedia.org/wiki/Snappy_(包管理器))，

其目标也是为了提供广泛的linux生态系一个通用的包装格式[[15\]](https://zh.wikipedia.org/wiki/Flatpak#cite_note-15)，

其支持类似于Flatpak的格式，

同时也支持应用程序商店式的[数字发行](https://zh.wikipedia.org/wiki/数字发行)与更新模式。



Flatpak 使用 [OSTree](https://ostree.readthedocs.io/en/latest/) 以分发和部署数据。它使用的仓库是 OSTree 仓库并且可以用 ostree 的工具来操作。已安装的运行时和应用都已经过 OSTree 检出。



其沙盒是基于[Linux核心](https://zh.wikipedia.org/wiki/Linux核心)以下子系统所提供的功能：

- [cgroups](https://zh.wikipedia.org/wiki/Cgroups)
- Linux namespaces
- [SELinux](https://zh.wikipedia.org/wiki/安全增强式Linux)（目前未使用）
- [kdbus](https://zh.wikipedia.org/wiki/D-Bus#KDBUS)（未来可能会使用，目前使用用户空间过滤）
- 视窗化系统基于[Wayland](https://zh.wikipedia.org/wiki/Wayland)（因为[X Window核心协议](https://zh.wikipedia.org/wiki/X_Window核心協議)已被开发者认为不安全[[13\]](https://zh.wikipedia.org/wiki/Flatpak#cite_note-13)）



# 参考资料

1、维基百科

https://zh.wikipedia.org/wiki/Flatpak