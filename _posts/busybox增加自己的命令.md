---
title: busybox增加自己的命令
date: 2016-12-19 22:47:57
tags:
	- busybox
---
往busybox里增加自己的命令，步骤如下。
我用的busybox的版本是1.25.1的。
# 1. 为命令选择一个位置
busybox的命令按照作用放在不同的目录下，我们新增的命令最好也遵循这个规则。因为增加的命令会出现在menuconfig里。现在我们只是做一个简单的验证，新增一个叫mycmd的命令，就放在miscutils目录下面。

# 2. 编写命令文件
将下面的内容保存到busybox/miscutils/mycmd.c里。
```
#include "libbb.h"
int mycmd_main(int argc, char **argv) MAIN_EXTERNALLY_VISIBLE;
int mycmd_main(int argc UNUSED_PARAM, char **argv)
{
	printf("hello, busybox cmd \n");
	return 0;
}
```
# 3. 修改配置脚本
修改下面这些文件内容时，请按照字母排序的方式插入到合理的位置。

## 3.1 修改miscutils/Kbuild.src
插入这一句。
```
lib-$(CONFIG_MYCMD)          += mycmd.o
```
## 3.2 修改miscutils/Config.src
插入这一段。
```
config MYCMD
	bool "mycmd"
	default y
	help
	  mycmd is used to show how to add cmd to busybox.
```
## 3.3 修改include/applets.src.h
插入这一句。
```
IF_MV(APPLET(mycmd, BB_DIR_BIN, BB_SUID_DROP))
```

然后编译运行，就可以看到新增加的命令了。


