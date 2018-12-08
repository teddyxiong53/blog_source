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

另外加上device定义的。因为我要console。

所以当前在rtdef.h里，大的结构体，先定义rt_device和rt_thread。

然后写rtservice.h。

这个主要是实现rt_list_t和rt_slist_t的操作函数。

写rtthread.h。这个相当于总头文件。

各种函数都在这里声明。

先写几个函数的声明。

另外rthw.h要写一下。



然后还是先按流程写。

回到components.c里，开始写rtthread_startup函数。

首先第一个函数是rt_hw_interrupt_disable。这个函数在qemu/cpu/context_gcc.S里的汇编函数。

这个文件里主要定义中断开关和上下文切换函数。代码不多。

然后回到components.c。

看rt_hw_board_init。

在qemu/drivers/board.c里。

```
rt_hw_board_init
1、调用rt_hw_interrupt_init，这个函数在qemu/cpu/interrupt.c里，新建这个文件。
	首先是vector初始化。是在vector_gcc.S里的。新增这个文件。这个文件就干了这个事情。
	在C文件里引用是这样：extern int system_vectors;
	然后是isr_table清空。这个是rt_irq_desc结构体的，定义在rthw.h里，新增这个结构体定义。
	这个结构体数组大小需要引用到一个中断号，需要引入qemu/drivers/realview.h头文件。
	这个文件就是寄存器地址定义了。直接拷贝过来。
	isr_table的大小是96 。
	然后是gic cpu init和gic dist init。
	需要引入qemu/cpu/gic.c文件。
	然后是一些中断嵌套标志变量的初始化。引入src/irq.c文件。
2、调用system_heap_init。
	堆用的是memheap.c里的。对应的宏是RT_USING_MEMHEAP
	新建src/memheap.c。
	不对，需要RT_USING_MEMHEAP_AS_HEAP这个宏支持。当前没有使能。所以用的是src/mem.c。
	mem.c里开始用到rt_kprintf。所以我开始引入rt_kprintf的相关文件。
	在src/kservice.c里。
```

mem.c这个动态内存分配算法，还是比较好懂的。

rt_kprintf的出现，开始在kservice.c里写大量代码。

这几个函数，都比较复杂，大量的分支和循环嵌套。值得深入研究一番。

```
rt_kprintf
	rt_vsnprintf
		print_number
```

然后开始引入console_device。

所以这里有个先后顺序，前面heap初始化的时候，console device还是NULL的，打印实际上没有用。

所以还是回到mem.c里继续写。

用到了rt_semaphore。所以需要把这个结构体引入进来了。

不过，这里用到的rt_semaphore，是静态的，因为动态的就是依赖mem了。现在mem还没有初始化好呢。

回到rtdef.h里，增加rt_semaphore相关的东西。

开始加入src/ipc.c文件。

然后需要引入object.c。这里面定义了rt_object_init等函数。

现在rt_system_heap_init写完了。目前的目录结构是这样的。

很多文件都是包含2个头文件：

rthw.h

rtthread.h

```
teddy@teddy-ubuntu:~/work/myrtt/rt-thread$ tree
.
├── bsp
│   └── qemu-vexpress-a9
│       ├── cpu
│       │   ├── context_gcc.S
│       │   ├── gic.c
│       │   ├── interrupt.c
│       │   ├── start_gcc.S
│       │   └── vector_gcc.S
│       ├── drivers
│       │   ├── board.c
│       │   ├── Kconfig
│       │   └── realview.h
│       ├── Kconfig
│       ├── rtconfig.h
│       ├── rtconfig.py
│       ├── SConscript
│       └── SConstruct
├── components
│   └── Kconfig
├── include
│   ├── rtdebug.h
│   ├── rtdef.h
│   ├── rthw.h
│   ├── rtm.h
│   ├── rtservice.h
│   └── rtthread.h
├── Kconfig
├── libcpu
│   └── Kconfig
├── src
│   ├── components.c
│   ├── ipc.c
│   ├── irq.c
│   ├── Kconfig
│   ├── kservice.c
│   ├── mem.c
│   └── object.c
```

现在需要把heap_begin和heap_end如何得到的分析一下。

定义在board.h里。

新增qemu/drivers/board.h文件。

```
extern int __bss_end;
#define HEAP_BEGIN ((void *)&__bss_end)

#define HEAP_END (void *)(0x60000000 + 8*1024*1024)
```

然后是调用rt_components_board_init。这个就用到了把对应的初始化函数都链接到镜像的一个命名区域的技巧。

```
__rt_init_rti_board_start
```

所以，我现在要开始写qemu/link.lds文件了。

但是里面也没有看到完整的__rt_init_rti_board_start这个段名。

是拼起来的名字。

有个函数名字叫rti_board_init。

```
./src/components.c:72:static int rti_board_start(void)
```

都是空名字，就是锚点。

我把这些锚点函数都写上。

安排顺序是这样的；

```
 * rti_start         --> 0
 * BOARD_EXPORT      --> 1
 * rti_board_end     --> 1.end
 *
 * DEVICE_EXPORT     --> 2
 * COMPONENT_EXPORT  --> 3
 * FS_EXPORT         --> 4
 * ENV_EXPORT        --> 5
 * APP_EXPORT        --> 6
 *
 * rti_end           --> 6.end
```

我们继续回到rt_hw_board_init函数。

现在需要设置console设备了。是uart0 。

开始要引入src/device.c了。

device.c里又用到thread的东西，所以还是回去先把thread的函数实现。

引入src/thread.c文件。

第一个函数，就是rt_thread_init。

我又发现，可以先不写thread的。我先把基础系统跑起来先，可以没有多任务。

先把用到的thread相关函数暂时不调用。还是调用吧。先留空实现。

2018年12月3日20:52:46

回到rt_hw_board_init。

目前这个函数写完了。

回到rtthread_startup函数。

下一个函数是rt_show_version。我就打印一下版本号。

我觉得可以进行一次编译了。先看看能不能把版本号打印出来。

现在报错。

```
scons: Reading SConscript files ...
AttributeError: 'NoneType' object has no attribute 'extend':
  File "/home/teddy/work/myrtt/rt-thread/bsp/qemu-vexpress-a9/SConstruct", line 26:
    objs = PrepareBuilding(env, RTT_ROOT, has_libcpu=True)
  File "/home/teddy/work/myrtt/rt-thread/tools/building.py", line 167:
    objs.extend(SConscript(Rtt_Root + "/src/SConscript", variant_dir=kernel_vdir+"/src", duplicate=0))
```

因为我很多地方SConscript都没有写呢。

目前只有qemu目录下有一个SConscript，而且还是空的。

写上内容。

把qemu目录下的子目录也都写上。

现在编译出错。一时还查不出问题在哪里。

我看看我之前写的scons_template里的。

```
teddy@teddy-ubuntu:~/work/myrtt$ make build
scons  -C rt-thread/bsp/qemu-vexpress-a9/ --verbose
scons: Entering directory `/home/teddy/work/myrtt/rt-thread/bsp/qemu-vexpress-a9'
scons: Reading SConscript files ...
TypeError: can only concatenate list (not "NoneType") to list:
  File "/home/teddy/work/myrtt/rt-thread/bsp/qemu-vexpress-a9/SConstruct", line 26:
    objs = PrepareBuilding(env, RTT_ROOT, has_libcpu=True)
  File "/home/teddy/work/myrtt/rt-thread/tools/building.py", line 167:
    objs = SConscript("SConscript", variant_dir=bsp_vdir, duplicate=0)
```

为什么会返回None呢？

找到问题了。是我之前，把DefineGroup没有写完。

```
def DefineGroup(name, src, depend, **parameters):
	global Env
	if not GetDepend(depend):
		return []
```

只写了这么点导致的 。

把这个函数写完，已经依赖的MergeGroup写完。现在编译是C语言的错误了。

```
/home/teddy/work/myrtt/rt-thread/include/rtdef.h:216:18: error: field 'thread_timer' has incomplete type
  struct rt_timer thread_timer;
```

需要定义rt_timer。

增加armv7.h，放在bsp/qemu/cpu目录下。

另外，那个has_libcpu的含义是：bsp目录下有cpu目录。这样就可以不用链接libcpu下的东西 了。

irq.c文件里定义rt_interrupt_nest。

需要继续写device的open函数。

需要在bsp/qemu/cpu下增加trap.c。有些汇编里调用到这里面的函数。

是定义各个异常处理函数。

我先都留空。

7个函数，irq和fiq的要实现。

2018年12月3日22:50:03

现在编译出来了。但是运行没有任何反应。

我的串口驱动还没有加上。

另外发现我有些函数写了但是没有调用。

在bsp/qemu/drivers下面新增serial.c和serial.h文件。

uart和Serial的关系：

uart偏硬件，是处理寄存器的。

serial偏软件，是处理各种结构体的。

2018年12月5日21:37:57

继续写。

现在编译报错。

rt_device_write还没有实现。

需要开始引入rt_set_errno。errno这个东西需要好好注意一下。

我先暂时这样实现。

```
void rt_set_errno(rt_err_t error)
{
	__rt_errno = error;
}
```

继续编译，还是报错。需要引入cp15_gcc.S文件。

现在编译过了，运行还是没有任何反应。

因为我的serial.c还没有写完呢。

现在需要引入components/drivers/serial/seiral.c文件了。

目前我的components目录里还没有文件呢。

现在需要先把Kconfig写一下。先加上这一行。

```
source "$RTT_DIR/components/drivers/Kconfig"
```

我当前Kconfig，可以留空文件。

因为我当前写的C代码，都是需要编译的，不依赖配置来进行开关。

然后需要引入rt_completion类型了。

现在实现rt_malloc了。在mem.c里。

鉴于这个项目会有很多的提交，为了方便追溯提交记录，我要把这个项目从c_code目录里挪出去，单独做一个repo。

rt_memset，先实现简单版本的。

2018年12月6日20:37:07

现在碰到同名文件问题。

有2个serial.h头文件。

现在编译qemu目录下的drivers/serial.c的时候，包含的serial.h是components目录下的了。

展开的编译命令是：

```
arm-none-eabi-gcc -o build/drivers/serial.o -c -march=armv7-a -marm -msoft-float -Wall -g -gdwarf-2 -O0 -I. -Icpu -Idrivers -I/home/teddy/work/myrtt/rt-thread/include -I/home/teddy/work/myrtt/rt-thread/components/drivers/include -I/home/teddy/work/myrtt/rt-thread/components/drivers/include drivers/serial.c
```

不是，包含的还是本目录下的，但是有个宏定义找不到。

是需要在rtdevice.h里，包含“drivers/serial.h"。

现在新的问题是，components目录下的serial.c编译的时候，包含不到qemu下面的那个。

导致结构体的定义找不到。

现在在rtdevice.h里，包含的drivers/serial.h，就是components下面这个。

scons怎么把目录加入到-I查找路径的？

现在的问题来源是什么？会不会是我的Python里写的有问题？

我把qemu下面那个改名为bsp_serial.h。这样解决了。

现在运行还是没有任何反应。

用单步调试的方式，加入make debug这个目标。

```
debug:
	sudo $(BOOT_CMD) -gdb tcp::1234 -S
```

一个shell窗口，执行make debug。

另外开一个shell窗口。输入：

```
teddy@teddy-ubuntu:~/work/myrtt$ arm-none-eabi-gdb ./rt-thread/bsp/qemu-vexpress-a9/rtthread.elf 
```

然后在gdb里输入：

```
 target remote :1234
 b _reset
 c  只能用c来执行，remote的方式不支持r。
```



从单步的情况看，在start_gcc.S的bss清理这里就出现了问题了。

```
_reset () at cpu/start_gcc.S:48
48          mov     r0,#0                   /* get a zero                       */
(gdb) 
49          ldr     r1,=__bss_start         /* bss start                        */
(gdb) 
50          ldr     r2,=__bss_end           /* bss end                          */
(gdb) 

```



但是我按下ctrl +C，会看到这个。

```
^C
Program received signal SIGINT, Interrupt.
rt_strncmp (cs=0xfffffff4 "", ct=0x60003511 "art", count=8)
    at /home/teddy/work/myrtt/rt-thread/src/kservice.c:165
165     {
(gdb) 
```

我把断点下在rtthread_startup函数上，可以执行到。

现在看看heap的初始化。

```
(gdb) p begin_addr 
$1 = (void *) 0x60003cd0
(gdb) p end_addr 
$2 = (void *) 0x60800000
```

现在可以看到是卡死在rt_device_find函数里了。

我知道了。我配置的是uart，而实际应该是uart0。所以找不到设备。

```
Breakpoint 1, rt_strncmp (cs=0xfffffff4 "", ct=0x60003510 "uart", count=8)
    at /home/teddy/work/myrtt/rt-thread/src/kservice.c:166
166             register signed char __res = 0;
```

继续运行，还是卡死。

现在看到是没有调用到INIT_BOARD_EXPORT(rt_hw_uart_init);这个函数。

因为我把这里关闭了导致的。

```
void rt_components_board_init()
{
#if 1
	const init_fn_t *fn_ptr;
	for(fn_ptr=&__rt_init_rti_board_start; fn_ptr<&__rt_init_rti_board_end; fn_ptr++) {
		(*fn_ptr)();
	}
#endif
}
```

我打开，发现还是找不到设备。

单步调试，发现错得离谱。

```
(gdb) p *information 
$3 = {type = RT_Object_Class_Thread, object_list = {next = 0x0, prev = 0x0},
  object_size = 0}
```

怎么会是RT_Object_Class_Thread这个呢？

发现问题了，是我之前偷懒，没有写完这个导致的。

```
static struct rt_object_information rt_object_container[RT_Object_Class_Unknown] = {
	{
		RT_Object_Class_Thread, 
		_OBJ_CONTAINER_LIST_INIT(RT_Object_Class_Thread),
		sizeof(struct rt_thread)			
	},
	{
		RT_Object_Class_Semaphore, 
		_OBJ_CONTAINER_LIST_INIT(RT_Object_Class_Semaphore),
		sizeof(struct rt_semaphore)			
	},
};
```

这么一来，就索性把需要的结构体都定义了。

再运行，现在可以运行到当前的最后一行了。

```
rtthread_startup () at /home/teddy/work/myrtt/rt-thread/src/components.c:37
37              }
(gdb) 
```

但是打印没有出来。

进一步调试，发现这里是NULL的。

```
if(_console_device == RT_NULL) {
```

问题还是在rt_device_find的时候，没有找到。

找到问题了，是我这里第三个参数没有加进来。name

```
rt_object_init(&(dev->parent), RT_Object_Class_Device, name);
	dev->flag = flags;
```

但是改了，还是不能打印出来。

是有个地方我条件写错了。

```
		rx_fifo = (struct rt_serial_rx_fifo *)rt_malloc(sizeof(struct rt_serial_rx_fifo) + serial->config.bufsz);
		if(!rx_fifo) {//这里我开始忘了加！了。
			return -RT_ENOMEM;
		}
```

改了这里，现在打印可以出来了。

2018年12月6日22:38:39

今天终于有实质进展了。找到了好的调试手段，而且打印也出来了。



# 12月7日

接下来，把线程部分的写完。

目前还只是一个空文件src/thread.c。

thread里用到了timer。timer则比较独立且简单。可以先写。

新建src/timer.c。

新建src/scheduler.c。

我先只写静态的线程创建。

新增bsp/qemu/cpu/stack.c。里面就一个函数rt_hw_stack_init。

新增了目录，下面都要增加一个SConscript，不然不会被编译进来的。

现在运行会卡到这里。

```
0x60003f80 in _serial_int_tx (serial=0x60004a50, data=0x60153ef5 "", 
    length=1609260551)
    at /home/teddy/work/myrtt/rt-thread/components/drivers/serial/serial.c:118
118                             rt_completion_wait(&(tx->completion), RT_WAITING_FOREVER);
```

所以我现在要把completion里的函数都实现先。

增加src/clock.c文件。

现在系统的tick系统还没有呢。

所以说当前调度就是根本不可能。

加上tick中断这些。



# 12月8日

继续写，定时中断的加上，现在还是卡在rt_completion_wait。

看来这个条件是不满足了，所以一直在等。

好像问题是在于，当前没有使能发送中断。

发送一般是用查询的方式。

所以改一下。

现在还是有问题。为什么这个size这么大呢？

```
Breakpoint 1, rt_serial_write (dev=0x600052f8, pos=0, buffer=0x60005b58, 
    size=1610633976)
```

是我rt_kprintf调用的时候，忘了传递length参数了。

现在打印没有乱码了。但是线程main函数没有调用到。

idle线程还没有，调度器也没有start呢。都加上。

增加idle.c文件。在src目录下。

现在完全是跑飞了。

单步看看。

现在的问题应该是在线程和调度器这2个文件里。

通过单步发现，目前我只有一个idle线程，一开始调度，为什么就调用了rt_thread_exit呢？

导致idle线程都不见了。

```
(gdb) p highest_ready_priority
$6 = -1
```

这个是非法的了。导致现在没有线程可以调度。

我怀疑是entry跟exit错位了，为什么会导致这种错位呢？

就是我在rt_hw_stack_init，多写了一次--stk导致的。

改了。现在可以了。

2018年12月8日15:05:12

现在主线程也可以跑起来了。



接下来，把ipc的写一些。先把sem和mutex的写完。

内存分配的需要先完善一下，现在free都还没有实现。

默认的内存管理模块是从lwip那里弄过来的。

看当前rt-thread的ipc，基本都是用FIFO的方式进行队列处理的。这种也简单。我就只实现这个。

需要加上delay函数。

现在把main函数这样修改。

```
int main(void)
{
	int i = 0;
	while(1) {
		rt_kprintf("main thread, count:%d \n", i++);
		rt_thread_delay(100);
	}
	
}
```

并不能循环打印。

只打印了一次。

现在的问题就是，线程sleep之后，就切不回来了。

看看定时中断调度那里是否在起作用？

发现一个问题，就是我没有把这句加上，导致没有调用。

```
INIT_BOARD_EXPORT(rt_hw_timer_init);
```

但是加上还是一样的问题。

是我还忘了把硬件定时器的中断使能。现在打开。可以了。

现在测试一下sem的。

然后测试一下malloc和free的。

没有问题再往下走。不然后面问题可能会越来越难查。

我当前的接口都是尽量在用静态的，动态的那些还没有去实现。

还有打印函数。

目前看是正常的。

我的下一个目标是把finsh加进去。

所以从这个角度出发，看看需要什么，就加什么。

先加目录。

components/finsh目录。里面新建SConscript文件。

msh的我先不实现。

先这么写。

```
Import('rtconfig')

from building import *

cwd = GetCurrentDir()
src = Split("""
shell.c
symbol.c
cmd.c
"""
)

fsh_src = Split('''
finsh_compiler.c
finsh_error.c
'''
)

CPPPATH = [cwd]

LINKFLAGS = ''

src = src + fsh_src

group = DefineGroup('finsh', src, depend=[''], CPPPATH=CPPPATH, LINKFLAGS=LINKFLAGS)

Return('group')
```

先把这5个c文件新建，都给空的。

看看从哪个开始写。

从shell.c开始写，这个是入口文件。

发现不能只写finsh。因为默认进的就是msh。而且msh是更加符合使用习惯的那个。

反而是可以只实现msh。

我就先只实现msh。

有个这样的宏。FINSH_USING_MSH_ONLY

说明只实现msh是可行的。

只需要这6个文件就可以了。

```
src = Split("""
shell.c
symbol.c
cmd.c
"""
)

msh_src = Split('''
msh.c
msh_cmd.c
msh_file.c
'''
)
```

而且我不打开FINSH_USING_SYMTAB这个。所以就可以让程序变得更加好理解。

先不管历史命令的。

原则就是用最少的代码实现shell功能。

现在发现shell的初始化函数没有被调用到。

现在需要把初始化的过程打印一下。

把RT_DEBUG_INIT这个宏的相关代码加进来。

才注意到components.c里有2个初始化函数。

一个是rt_components_board_init。这个调用比较早。

一个是rt_components_init。这个是在main线程的main函数之前调用的。



发现现在输入没有反应，是因为我的serial.c中断里没有处理indicate函数。

加上，还是输入没有反应。

看看参数值。

```
(gdb) p rx_fifo->put_index
$2 = 0
(gdb) p rx_fifo->get_index
$3 = 24576
(gdb) p serial->config.bufsz
```

get_index的不对劲。

我单步可以看到确实正确收到输入的字符。

例如我输入a再回车，确实收到2个字符，一个97，一个13 。

但是处理不低。get_index和put_index都不对。

是我这里写错了。

```
rx_fifo = (struct rt_serial_rx_fifo *)serial->serial_tx;//写成了tx的了。
```

现在输入回车有反应了。

2018年12月8日18:32:37

现在继续完善shell。

2018年12月8日19:08:15

现在可以进行msh命令解析执行了。

shell的我暂时有个基本功能了。暂时不再输入了。

现在要换个点了。

我觉得文件系统的可以。先看看，可能还是需要先实现其他才能做这个。

其实我是希望可以尽快把MicroPython的弄起来。

现在其实也可以暂停一下，看看链接的map文件。

当前链接的C库是标准的。

```
/usr/lib/gcc/arm-none-eabi/4.9.3/../../../arm-none-eabi/lib/armv7-ar/thumb/libc.a(lib_a-memset.o)
                              build/cpu/interrupt.o (memset)
/usr/lib/gcc/arm-none-eabi/4.9.3/../../../arm-none-eabi/lib/armv7-ar/thumb/libc.a(lib_a-strncmp.o)
                              build/kernel/components/finsh/msh.o (strncmp)
```

还是把dfs实现。

先只实现ramfs的。

建立目录结构如下：

```
teddy@teddy-ubuntu:~/work/myrtt/rt-thread/components/dfs$ tree
.
├── filesystems
│   ├── ramfs
│   │   ├── dfs_ramfs.c
│   │   ├── dfs_ramfs.h
│   │   └── SConscript
│   └── SConscript
├── include
├── Kconfig
├── SConscript
└── src
```

SConscript都写上。

新建dfs/src/dfs.c。这个是入口文件。

这个会用到mutex。我前面实现命令行，都还是只用到sem就够了。

所以现在需要先实现mutex。

mutex有修改线程优先级的行为，所以这一块的内容也要加进来。

从struct stat发现一个我之前没有注意的东西。

在rtdef.h里包含了rtlibc.h这个头文件。

我一直没有创建这个头文件。这个头文件挺重要的。

是在顶层include下的。然后这下面还有一个libc目录。是一起的。

我现在就把这加进来。



现在看看怎么把文件系统挂载进来，这个才是入口位置。从这个地方开始写，不然有点不知道从哪里继续。

看看mount函数哪里有调用。



在applications目录下新建一个mnt.c。里面就写一个mnt_init函数，放在初始化section自动调用。

需要实现函数dfs_mount。

```
int mnt_init()
{
	//rt_thread_delay();
	if(dfs_mount("ram0", "/", "ram", 0, 0) == 0) {
		rt_kprintf("ramfs mount ok\n");
	}
	return 0;
}

INIT_ENV_EXPORT(mnt_init);
```



现在要到dfs_ramfs.c里去写了。

ramfs要用到memheap.c。这个可以跟mem.c共存的。只要你不使能这个宏。RT_USING_MEMHEAP_AS_HEAP

不知道这个的算法跟mem.c的有什么区别。







