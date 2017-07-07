---
title: macos使用入门
date: 2017-07-06 21:37:28
tags:

	- macos

---

尽管不是苹果粉，但是还是无法抗拒macos漂亮的界面，于是在虚拟机里安装了一个。因为我的电脑配置很不错，虚拟机也是放在ssd里，所以启动和运行效果都不错。

现在就尝试把macos当成工作的机器，来配置一下基本的使用环境，也做一个基本的了解。



# 1. 按键和windows的不同点

碰到的第一个问题就是，pc键盘如何在mac上使用。

在没有经过设置的情况下，pc键盘在mac上使用是非常不顺手的。

在macos的体系里，有3个按键：command键、option键、control键。

我们需要做的就是把option和command键的设置反一下，这个就符合我们日常的使用习惯了。control维持不变。command键的位置是微软键。option键的位置是alt键。

设置的位置是：系统偏好设置，键盘，修饰键。



# 2. mac如何切换输入法

设置的位置是：系统偏好设置，键盘，输入源，点击加号，添加简体拼音就好了。

这样设置后，你可以在屏幕的右上角有鼠标来切换输入法，但是这样无疑是不方便的。

键盘切换输入法快捷键：系统偏好设置，键盘，快捷键，输入源，把选择框勾上，可以看到提示有冲突，可以看到是跟Spotlight冲突了。我暂时不了解spotlight，所以把spotlight的都关闭先。

所以现在默认的切换就是：alt+空格可以切换输入法。



# 3. 安装基本软件

打开App Store，打开方式是点击左上角的苹果图标，然后选择App Store。

安装就很简单了。



# 4. 搭建开发环境

先安装homebrew，这个相当于Ubuntu下的apt-get。

将这句代码粘贴到macos下的终端里，`ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`。根据提示进行操作即可。

很不幸，这个都安装失败，看来必须先翻墙了。

下载一个免费的shadowsocks客户端先。



