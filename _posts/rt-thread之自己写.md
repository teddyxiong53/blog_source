---
title: rt-thread之自己写
date: 2018-11-30 22:22:13
tags:
	- rt-thread

---



我非常喜欢rt-thread这个系统。

现在通过自己写一遍的方式来加深理解。

就基于qemu-vexpress-a9的来做。我基于的是rt-thread 3.0.2的。

qemu-vexpress-a9这个名字太长了，下面都简称为qemu目录。

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

现在在另外一台电脑上继续写，发现我另外的电脑上的是3.0.4的rt-thread。

从这里下载3.0.2的。选择这个版本纯属偶然。

https://github.com/RT-Thread/rt-thread/tree/ff6b7c4c23b762ada2c6eadf187023910949fa64

现在把building.py里，需要的函数，把需要的分支实现。

碰到不少的scons类，一个个都弄懂先。写测试脚本，一个个实验一下。

现在需要加入menuconfig的。

新建menuconfig.py，在tools目录下。

需要引入一个kconfig-frontends目录，在tools目录下。

menuconfig.py写完了，现在需要在qemu目录下新增Kconfig文件。

Kconfig就是一个各个层级进行包含的关系。

现在需要新建src目录，在下面写一个Kconfig。这个属于kernel的配置项部分。

我当前的目标是，先把menuconfig跑起来，所以把需要的文件，里面尽量少写东西，有一两项保证跑起来不报错就好。

新建libcpu目录，里面新建Kconfig文件。

libcpu下面分了很多子目录，我只管arm/cortex-a这个目录。

libcpu/Kconfig只写这些。

```
config ARCH_ARM
	bool
	

config ARCH_ARM_CORTEX_A
	bool
	select ARCH_ARM
	
	
config ARCH_ARM_CORTEX_A9
	bool 
	select ARCH_ARM_CORTEX_A
```

然后新建components目录。下面新建Kconfig文件。

在qemu目录下新建drivers目录，下面新建Kconfig文件。

现在目录结构是这样：

```
hlxiong@hlxiong-VirtualBox:~/work/myrtt$ tree
.
├── Makefile
└── rt-thread
    ├── bsp
    │   └── qemu-vexpress-a9
    │       ├── drivers
    │       │   └── Kconfig
    │       ├── Kconfig
    │       ├── rtconfig.py
    │       ├── rtconfig.pyc
    │       ├── SConscript
    │       └── SConstruct
    ├── components
    │   └── Kconfig
    ├── Kconfig
    ├── libcpu
    │   ├── arm
    │   │   └── contex-a
    │   └── Kconfig
    ├── src
    │   └── Kconfig
    └── tools
        ├── building.py
        ├── menuconfig.py
        ├── mkdist.py
        └── utils.py
```

执行make config，会报错。

```
hlxiong@hlxiong-VirtualBox:~/work/myrtt$ make config
scons --menuconfig -C rt-thread/bsp/qemu-vexpress-a9/
scons: Entering directory `/home/hlxiong/work/myrtt/rt-thread/bsp/qemu-vexpress-a9'
scons: Reading SConscript files ...
  File "/home/hlxiong/work/myrtt/rt-thread/tools/building.py", line 46

    env.Append(CPPPATH=[str(Dir('#').abspath])

                                            ^

SyntaxError: invalid syntax

Makefile:31: recipe for target 'config' failed
make: *** [config] Error 2
```

当前我还没有把kconfig-frontends拷贝过来。

这个目录下的东西，直接拷贝过来。

再执行，还是一样的错误。是我这里少了个括号。

现在python里的错误都改了。

现在执行make config，报这个错误。

```
'config:1:warning: ignoring unsupported character '
'config:1:warning: ignoring unsupported character '
Kconfig:3:warning: ignoring unsupported character '$'
'config:3:warning: ignoring unsupported character '
'config:4:warning: ignoring unsupported character '
Kconfig:3:warning: environment variable BSP_ROOT undefined
'config:5:warning: ignoring unsupported character '
'config:6:warning: ignoring unsupported character '
```

看来rtt默认的，也是会报这些警告。这些没有关系。至少是不影响实际功能的。

我把qemu下的Kconfig删到只剩这些。这样可以出现menuconfig的窗口的。

```
mainmenu "rt-thread project menuconfig"

config $BSP_DIR
    string
    option env="BSP_ROOT"
    default "."

```

说明了一个问题，就是Kconfig里不能用tab键，要用空格。

不是，有那么多的warning，是因为dos格式的换行符导致的，都换成Unix风格的，就好了。

把所有Kconfig文件里的tab转成空格。

```
find . -name 'Kconfig' ! -type d -exec bash -c 'expand -t 4 "$0" > /tmp/e && mv /tmp/e "$0"' {} \;
```

最后的错误是这个。

```
../../Kconfig:3: can't open file "RTT_DIR/components/Kconfig"
```

这个是因为少了个美元符导致的

改了。

现在错误是这个：

```
Kconfig:19: can't open file "/home/hlxiong/.myrtt_env/packages/Kconfig"
```

把还是不用自己的myrtt_env了。还是用.env这个默认的。

endmenu in different file than menu? 

报这个错误，需要在endmenu后面还有一个空行才行。

现在可以出完整配置界面了。但是退出时会报错。

```
configuration written to .config

*** End of the configuration.
*** Execute 'make' to start the build or try 'make help'.

AttributeError: 'str' object has no attribute 'lstript':
  File "/home/hlxiong/work/myrtt/rt-thread/bsp/qemu-vexpress-a9/SConstruct", line 26:
    objs = PrepareBuilding(env, RTT_ROOT, has_libcpu=True)
  File "/home/hlxiong/work/myrtt/rt-thread/tools/building.py", line 131:
    menuconfig(Rtt_Root)
  File "/home/hlxiong/work/myrtt/rt-thread/tools/menuconfig.py", line 124:
    mk_rtconfig(fn)
  File "/home/hlxiong/work/myrtt/rt-thread/tools/menuconfig.py", line 17:
    line = line.lstript(' ').replace('\n', '').replace('\r', '')
Makefile:31: recipe for target 'config' failed
make: *** [config] Error 2
```

这个是在根据.config内容生成rtconfig.h时出错了。

还是有些手误导致的，改了就 好了。都是在menuconfig.py里的。

有两处。

现在menuconfig没有问题了。

上传一个版本。

接下来把menuconfig需要的都加上。

drivers目录下的，我只留下uart0和uart1的。

现在主要是把src下面的配置弄好。这个是内核的相关配置。

2018年12月1日16:57:54

现在Kconfig基本部分都写完了。开始动手写C代码部分。

入口文件在哪里？

qemu目录下，也有一个cpu目录，看文件名字跟libcpu下的一样，用的是哪个？

从gic.c来看，用的是qemu/cpu目录下的文件的。那么libcpu下的就是没有用的了。

入口文件是qemu/cpu/gcc_start.S。

这个汇编就暂时不写了，直接拷贝过来。

引用到C语言入口函数rtthread_startup。

在./rt-thread/src/components.c文件里。

所以新建components.c文件。

这个c文件用到了这2个头文件。

```
#include <rthw.h>
#include <rtthread.h>
```

开始加入这2个头文件。

在根目录下新建include目录。

rtthread.h是一个总的头文件。

里面包括了这些头文件。

```
#include <rtconfig.h>
#include <rtdebug.h>
#include <rtdef.h>
#include <rtservice.h>
#include <rtm.h>
```

所以我们先加入这些头文件。

rtconfig.h是自动生成了。ok。

rtdebug.h。

这个在include目录下，我们先留空。

RT_USING_NEWLIB这个宏是打开的。

但是在哪里定义的呢？



rt_list_t是rtt系统里，一个特别的数据类型。

rt_xx_t这种格式的数据类型，一般都是指针的，而rt_list_t，不是指针，是结构体。

先只实现线程这部分的。



