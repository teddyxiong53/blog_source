---
title: 蓝牙之bluetoothctl代码分析
date: 2018-11-28 13:34:28
tags:
	- 蓝牙

---



bluetooothctl的入口代码是在bluez/client/main.c里。

我们先看list这个命令是如何实现的。

```
static const struct bt_shell_menu main_menu = {
	.name = "main",
	.entries = {
	{ "list",         NULL,       cmd_list, "List available controllers" },
```

依赖了glib和





