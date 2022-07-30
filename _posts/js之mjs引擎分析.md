---
title: js之mjs引擎分析
date: 2022-07-30 18:16:07
tags:
	- js

---

--

首先看编译，这个基于docker的编译方式，就比较新颖，值得学习一下。

还有把所有的文件都组装成一个单c文件的方式，也让代码在其他的地方进行集成变得非常方便。

这都是值得学习的好的做法。

先看docker编译的方式

```
RD ?= docker run -v $(CURDIR):$(CURDIR) --user=$(shell id -u):$(shell id -g) -w $(CURDIR)
DOCKER_GCC ?= $(RD) mgos/gcc
DOCKER_CLANG ?= $(RD) mgos/clang
```

使用-v的方式，应该是做到了直接使用docker的工具链编译当前目录的东西。

这种方式非常的好。保证工具链不会污染当前的机器，而且非常简单。

编译的地方，这样调用

```
$(PROG): $(TOP_MJS_SOURCES) $(TOP_COMMON_SOURCES) $(TOP_HEADERS) $(BUILD_DIR)
	$(DOCKER_CLANG) clang $(CFLAGS) $(TOP_MJS_SOURCES) $(TOP_COMMON_SOURCES) -o $(PROG)
```



参考资料

1、

