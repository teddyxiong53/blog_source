---
title: Makefile之技巧
date: 2018-04-12 21:10:51
tags:
	- Makefile

---



# 定义一个空格的方法

```
empty:=
space:= $(empty) $(empty)
```

```
merge=$(subst $(space),,$(1))
```



# 防止重复包含一个mk文件

```
ifneq ($(this_filname),1)
this_filename=1
...
endif
```

