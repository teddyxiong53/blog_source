---
title: Makefile经验
date: 2017-02-22 23:16:30
tags:
	- Makefile
---
# 1. 创建文件夹或者删除文件夹的函数
```
CreateDir = $(shell [ -d $1 ] || mkdir -p $1 || echo "$1 exists")
RemoveDir = $(shell [ -d $1 ] && rm -rf $1 || echo "rm $1 failed ")

dummy := $(call CreateDir, $(DIR1_NAME))
dummy += $(call CreateDir, $(DIR2_NAME))
```

# 2. 编译加快速度 

make的时候带-j选项，例如`make -j128`。-j后面的数字，取多少，取决于你的电脑的cpu核心数量。如果不知道可以这样`make -j$(nproc)`。或者指定多一些，也没有关系。



