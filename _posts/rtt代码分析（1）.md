---
title: rtt代码分析（1）
date: 2017-10-02 15:39:42
tags:
	- rtt

---



rtt是我对RT-Thread的简称，这样方便称呼。

现在尝试写一个系列，来分析rtt的代码。分析的是1.2.1版本。这个应该是用得比较多的一个版本。

这篇文章，就以stm32f10x的为例，把rtt的代码串起来，先形成一个基本的认识。



# 1.目录分布

简单来看，目录大概情况是这样：

```
bsp：
	stm32f10x
		applications
		drivers
		rtconfig.h：配置。
components：
	各种组件。
src：
	rtt核心代码。
```

我们需要改代码的地方，集中在application和drivers这2个目录。

# 2. rtconfig.h头文件分析

rtconfig.h是系统的配置头文件。

主要内容有：

## 基础部分：

1、配置内核组件名字的最大程度，默认是8字节，够了。

2、配置对齐字节数。默认4个字节。也不改。

3、配置最大优先级。默认32。

4、配置每秒tick数。默认100。

5、配置debug开关。

6、配置溢出检查。

7、配置钩子函数开关。

8、配置定时器线程的优先级为4，堆栈512字节。节拍为100ms。

## ipc部分

1、sem开关。

2、mutex开关。

3、event开关。

4、mailbox开关。

5、messagequeue开关。

## 内存管理

1、内存池开关。

2、heap开关。

3、使用small mem开关。

## 设备驱动

1、使用device开关。

2、device ipc开关。

3、使用串口开关。

4、使用console开关。bufsize 128字节。名字uart1。

5、使用finsh开关。

## 文件系统

1、fat开关。

2、fat的重入开关。

3、文件系统个数。默认为2。

4、fd的最大值，默认是4 。（有点小）

## 协议栈

lwip相关配置。

# 3. 函数入口分析

入口是main函数，在applications/startup.c里。

```
main()
	-- rtthread_startup()
		-- rt_hw_board_init()：在drivers/board.c里。
		-- rt_system_heap_init()：
		-- rt_system_scheduler_init()
		-- rt_system_timer_init()
		-- rt_system_timer_thread_init()
		-- rt_application_init()
		-- rt_thread_idle_init()
		-- rt_system_scheduler_start()
		
```

上面函数里，只有`rt_application_init`是需要用户进行实现的。

这个函数在application.c里实现。

默认的代码是这样的：

```
1、创建一个led线程。启动。作为系统指示。
2、创建一个init线程。启动。
```

init线程里做了这些：

```
1、component初始化。
2、finsh设置串口绑定。
3、挂载SD卡。
4、初始化lcd显示。
```

# 4. 用户应该怎样进行rtt的适配？

总体来说，需要做的事情还是非常明确的。系统的整体代码风格很统一。

需要只需要再芯片目录下的applications和drivers目录下进行编码就可以了。

在已有代码的基础上做这个，是非常简单的。



