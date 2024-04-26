---
title: Linux桌面（1）
date: 2024-04-25 10:02:17
tags:
	- Linux

---

--

# 基本概念

Linux桌面先要搞清楚几个基本概念。

http://www.smth.org/posts/dm_de_wm/

## DM

操作系统的图形环境只是方便用户使用，不应该太过重量级喧宾夺主，所以DM(Display Manager)用LightDM，只是管理用户登录嘛，要那么复杂干嘛？

### lightdm

https://wiki.archlinux.org/title/LightDM

https://github.com/canonical/lightdm

## DE

缺省桌面环境(DE)选的是Xfce4，因为它是轻量的，但又不是特别轻量的。桌面环境只是个支撑，目的是方便运行其他程序，为什么要用重磅的KDE或Gnome呢？Xfce桌面只占用少量内存就无比强大，稳定、简单优雅、可配置性强、模块化。

## WM

但是我以前常用的并不是Xfce4，而是i3wm。但登录后i3wm是一片空白，如果不知道快捷键甚至不知道如何操作。既然是一个发行版，不能让没用过i3wm的不知从何入手。

但瓦片式WM的方便性确实让人着迷，虽然Xfwm4也可以用快捷键把应用窗口左右/上下二分，或者四分，但还是不够爽，无法同时看到5个以上的窗口。所以决定把Xfce4和瓦片式WM结合起来，用bspwm代替Xfwm4，这就形成了上面有菜单条状态条、主界面是bspwm瓦片式的情况，不知道快捷键的人可以从菜单执行程序，又能得到瓦片式WM的便捷性。

之所以用bspwm而不是i3wm，是使用中觉得bspwm和Xfce4的结合更好、更方便。

### Ulauncher

GUI操作环境一个最重要的作用就是方便用户找到需要的程序执行，

Xfce4+bspwm 可以从程序菜单树找到程序执行，也可以设定快捷键直接执行。

但macOS的Spotlight是一个非常方便的入口，只要知道要执行的程序的名字，甚至部分，也可以方便地找到执行。

所以用上Ulauncher，连快捷键定义也跟macOS一样，Super+空格。

当然，经常跟i3wm配合使用的dmenu、Rofi等，不过我最喜欢Ulauncher。

