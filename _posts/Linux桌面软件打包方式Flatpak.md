---
title: Linux桌面软件打包方式Flatpak
date: 2024-05-24 19:56:17
tags:
	- Linux

---

--

# 简介

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

# flatpak打包的基本方法

Flatpak的基本打包方法如下：

1. **准备工作**：在开始之前，确保你的系统已经安装了Flatpak以及Flatpak Builder工具。你可以在官方网站或者你的发行版仓库中找到相应的安装方法。

2. **创建应用目录**：创建一个新的目录来存放你的应用程序的文件。在这个目录中，你需要创建一个`manifest.json`文件来描述你的应用程序和它的依赖关系。

3. **编写manifest.json文件**：`manifest.json`文件是Flatpak应用的核心配置文件，它包含了应用的名称、版本、运行时依赖、打包命令等信息。你需要根据你的应用程序填写相应的字段，确保所有的依赖关系都被正确声明。

4. **构建应用程序**：使用Flatpak Builder工具来构建你的应用程序。在命令行中执行`flatpak-builder`命令，并指定你的应用目录以及输出目录。Flatpak Builder将会自动下载并构建你的应用程序，生成一个`.flatpak`文件。

5. **安装应用程序**：使用Flatpak命令来安装你的应用程序。在命令行中执行`flatpak install`命令，并指定你的`.flatpak`文件路径。Flatpak将会把你的应用程序安装到系统中，并自动解决所有的依赖关系。

6. **运行应用程序**：安装完成后，你可以在应用菜单中找到你的应用程序，并启动它运行。Flatpak会自动在沙盒环境中运行你的应用程序，保证它的安全性和稳定性。

这是一个基本的Flatpak打包方法的概述。具体的步骤和命令可能会根据你的应用程序的需求和Flatpak版本的不同而有所变化，你可以参考Flatpak的官方文档或者其他教程来获取更详细的信息。

# 原理

flatpak的原理，它是把应用的依赖项都打包进去了吗？可以做到想macos上app文件那样的效果吗？

Flatpak的原理是通过将应用程序和其运行时依赖项一起打包，以创建一个独立的、沙盒化的运行环境。它并不是将所有的依赖项都打包进去，而是提供了一个可重复使用的运行时环境，称为运行时。应用程序和运行时环境是分开打包的，这样可以减小应用程序的大小，并且在运行时可以共享运行时环境，减少资源浪费。

Flatpak可以做到类似macOS上.app文件的效果，即提供了一种独立的、自包含的应用程序格式。用户可以直接从Flatpak仓库安装应用程序，而不需要手动安装依赖项或者担心依赖冲突的问题。同时，Flatpak应用程序在沙盒环境中运行，与系统其它部分相互隔离，提供了更好的安全性和稳定性。

总的来说，Flatpak采用沙盒化的运行环境，将应用程序和依赖项一起打包，并提供类似macOS上.app文件的独立运行效果，以实现更加便捷、安全和稳定的应用程序分发和运行。

# 参考资料

1、维基百科

https://zh.wikipedia.org/wiki/Flatpak