---
title: Android之adb学习
date: 2018-01-03 10:39:45
tags:
	- Android
	- adb

---



adb是Android Debug Bridge的意思。

# 基本语法

```
adb [-d|-e|-s <serialNumber>] <command>
```

`[-d|-e|-s <serialNumber>]`这部分在当前只连接了一个设备的时候，可以没有。

d选项表示：device。

e选项表示：emulator。模拟器。

s选项表示：序列号。

# 简单使用

先不看

一般我们首先做的是，输入`adb devices`查看当前有哪些设备。这个就可以查看到序列号的。

退出adb命令行怎么做呢？一般命令行退出都是quit、exit、bye这几个单词，挨个试。adb的是exit。



