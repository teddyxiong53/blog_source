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

# 2. 

