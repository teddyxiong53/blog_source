---
title: rt-thread之自己写
date: 2018-11-30 22:22:13
tags:
	- rt-thread

---



我非常喜欢rt-thread这个系统。

现在通过自己写一遍的方式来加深理解。

就基于qemu-vexpress-a9的来做。我基于的是rt-thread 3.0.2的。

只考虑gcc工具链。

一方面也是熟悉一下scons的这一套编译工具。

在我的github的c_code目录下，新建一个myrtt目录。就上传到这里。

```
teddy@teddy-ubuntu:~/work/myrtt$ tree
.
├── Makefile
└── rt-thread
```

我还是保持我比较习惯的这种结果。通过最外面的Makefile来进行编译。

新建目录。

```
teddy@teddy-ubuntu:~/work/myrtt$ tree
.
├── Makefile
└── rt-thread
    └── bsp
        └── qemu-vexpress-a9
```

在qemu-vexpress-a9目录下，新建SConstruct和SConscript文件。

SConstruct相当于Makefile。

这个里面用到了rtconfig.py的东西，所以我们先新建rtconfig.py文件。

这个文件里就是配置cpu类型，工具链，CFLAGS这些。

可以先写完。

然后继续写SConstruct。这里定义RTT_ROOT，然后引用到tools目录下的东西。

新建tools目录。这个下面就要开始写不少的py文件了。

tools目录下新建building.py。

这个文件内容较多。大概800行。

building.py又引入了utils.py和mkdist.py这2个文件。

所以还要先写这2个。

在mkdist.py里写了几个函数，感觉写不下去，先不深入，还是回到building.py，看看用到了哪些函数，再针对性来写。

building.py暴露的主要接口是：

```
PrepareBuilding：被qemu-vexpress-a9下的SConstruct调用。
```

SConstruct最重要的两行就是：

```
objs = PrepareBuilding(env, RTT_ROOT, has_libcpu=True)
DoBuilding(TARGET, objs)
```

