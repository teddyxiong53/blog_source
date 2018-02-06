---
title: rt-thread（十一）bsp目录分析
date: 2018-02-05 22:51:25
tags:
	- rt-thread

---



以qmeu-vexpress-a9为例。分析bsp目录的构成。

```
.
├── applications：用户自己开发东西，就放这个目录。
├── build：所有编译的文件都输出到这个目录。
├── cpu：放cpu相关的文件，有几个汇编。
├── drivers：放板子相关驱动代码。
├── Kconfig
├── link.lds：链接脚本。
├── packages：你配置的package，会下载源代码到这个目录。
├── qemu.bat
├── qemu-dbg.bat
├── qemu-nographic.sh
├── qemu.sh
├── README.md
├── rtconfig.h：配置文件。
├── rtconfig.py：可以在这里改工具链等配置。
├── rtthread.bin：这个可以烧录到板端运行。
├── rtthread.elf：可执行文件。用这个运行。
├── rtthread.map
├── SConscript
└── SConstruct
```

看看cpu目录下的内容：

```
.
├── armv7.h：定义了usr、irq等模式的宏。几十行代码。
├── context_gcc.S：开关中断、切换任务。100行汇编。
├── cp15_gcc.S：协处理器相关。
├── cp15.h：几个函数声明。
├── cpu.c：就一个shutdown函数。
├── gic.c：中断。
├── gic.h：函数声明。
├── interrupt.c
├── interrupt.h
├── mmu.c：
├── pmu.c
├── pmu.h
├── SConscript
├── stack.c：定义了任务栈初始化一个函数。
├── start_gcc.S：入口。
├── trap.c：出错处理。
└── vector_gcc.S：中断向量。
```

