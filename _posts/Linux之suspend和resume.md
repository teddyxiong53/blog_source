---
title: Linux之suspend和resume
date: 2022-04-11 14:30:11
tags:
	- Linux

---

--

```
在作之前，先检查一下你的内核能支持哪些方式：

# cat /sys/power/state

standby disk
```



# One or more tasks refusing to freeze

```
# [  180.291820@1]  Restarting tasks ... done.
[  180.294131@1]  gxbb_pm: late_resume: call handlers
[  180.294479@1]  gxbb_pm: late_resume: bt_lateresume
[  180.295068@1]  gxbb_pm: late_resume: loopback_platform_late_resume
[  180.295836@1]  gxbb_pm: late_resume: pdm_platform_late_resume
[  180.296552@1]  gxbb_pm: late_resume: tdm_platform_late_resume
[  180.297264@1]  gxbb_pm: late_resume: tdm_platform_late_resume
[  180.298053@1]  gxbb_pm: late_resume: tdm_platform_late_resume
[  180.298690@1]  gxbb_pm: late_resume: done
[  180.299190@1]  audio_ddr_mngr: ddr_pm_event, pm_event:4
[  180.299841@1]  Abort: One or more tasks refusing to freeze  重点是这里。
[  180.300658@1]  PM: suspend exit
```

# 支持的sleep状态

Linux Kernel支持四种`Sleep State`：

- `Suspend-to-Idle`
  纯软件，轻量级的Suspend操作，它会`freeze user space`，`suspend the timekeeping`，`put all I/O devices into low-power states`。
  处于S2Idle状态下时，设备中断就可以将其唤醒。
- `Standby`
  除了实现`Suspend-to-Idle`时的操作外，还会将`nonboot CPUs`置于`offline`状态，以及`suspend all low-level system functions`。由于系统核心逻辑单元保持上电状态，操作的状态不会丢失，也会很容易恢复到之前的状态。
  处于`Standby`状态时，可能需要依赖平台来设置唤醒源。
- `Suspend-to-RAM`
  `STR/S2RAM`时，除了`Memory`需要进行自刷新来保持数据外，其他的所有设备都需要进入到低功耗状态。除了实现`Standby`中的操作外，还有一些平台相关的操作要进行。比如，在STR的最后一步，将控制权交给`Firmware`，然后下电，等着唤醒时再重新Resume回来。由于存在掉电行为，因此Resume的时候需要重新进行配置。
  处于`STR`状态时，需要依赖平台设置唤醒源。
  **本文主要分析的流程就是`STR`。**
- `Hibernation`
  `Suspend-to-Disk, STD`，简而言之，这个操作会将运行时的context保存在Disk这种非易失的存储器中，然后进行掉电操作。当按下电源键进行唤醒时，Firmware/Uboot会将保存的context进行恢复。

上述四个状态，功耗节省效果依次增强，同时唤醒回来的时间开销也相应加大。



代码路径：
`kernel/power/main.c`
`kernel/power/suspend.c`



入口函数是pm_suspend

kernel\power\suspend.c

```
pm_suspend
	enter_state
		valid_state
		suspend_prepare
			pm_prepare_console
				pm_vt_switch
				vt_move_to_console
				vt_kmsg_redirect
				这个是当前的console切换到虚拟console，并重定向kmsg。
			__pm_notifier_call_chain
				通知相关的设备做一些准备工作。
			suspend_freeze_processes
				freeze进程。
				freeze_processes
				freeze_kernel_threads
		suspend_devices_and_enter
			这个是主要的处理。
			suspend_console
			dpm_suspend_start
				device pm处理开始。
```





# 对于休眠(suspend)的简单介绍

在Linux中,休眠主要分三个主要的步骤:
1) 冻结用户态进程和内核态任务
  2) 调用注册的设备的suspend的回调函数, ==顺序是按照注册顺序==
  3) 休眠核心设备和使CPU进入休眠态, 冻结进程是内核把进程列表中所有的进程的状态都设置为停止,并且保存下所有进程的上下文. ==当这些进程被解冻的时候,他们是不知道自己被冻结过的,只是简单的继续执行。==
  如何让Linux进入休眠呢?用户可以通过读写sys文件/sys /power/state 是实现控制系统进入休眠. 比如
  \# echo mem > /sys/power/state
  命令系统进入休眠. 也可以使用

  \# cat /sys/power/state
  来得到内核支持哪几种休眠方式.



https://blog.csdn.net/MyArrow/article/details/8136109



# kernel suspend的原理是什么

内核的挂起（suspend）是一种操作系统的电源管理功能，用于将计算机系统切换到低功耗状态以节省电能。挂起的具体实现可能因不同的硬件和内核版本而有所不同，但其基本原理通常包括以下步骤：

1. **准备挂起：** 当用户或系统触发挂起操作时，内核首先会通知各个子系统，以便它们准备好挂起前的状态。

2. **保存状态：** 内核会保存当前系统的状态，包括各个设备的状态、CPU寄存器的内容、内存中的数据等。这通常涉及到将系统的运行状态保存到内存中。

3. **设备关闭：** 内核会通知各个设备进入低功耗状态或关闭状态，以尽量减少功耗。这可能包括磁盘驱动器、网络接口、图形卡等设备的关闭或降低功耗。

4. **停止CPU：** 为了降低功耗，内核可能会将CPU置于某种低功耗状态，以便在挂起时消耗尽可能少的电能。这可以通过调整时钟频率、进入某种休眠状态（如深度睡眠）来实现。

5. **唤醒处理：** 当系统需要被唤醒时（例如，用户按下电源按钮或定时器触发），内核会恢复之前保存的状态，并通知各个设备和子系统重新初始化。

需要注意的是，不同的架构和硬件平台可能有不同的挂起实现方式。例如，针对移动设备的挂起可能会更加复杂，因为它需要处理移动设备的特殊硬件和网络连接。

在 Linux 内核中，挂起和唤醒的具体实现与架构相关，并且可以通过 ACPI（高级配置与电源接口）等标准进行电源管理。 ACPI 提供了一个标准的接口，允许操作系统与硬件平台进行通信，以实现挂起和唤醒等电源管理功能。



# 参考资料

1、

https://blog.csdn.net/hshl1214/article/details/6228275

2、

https://unix.stackexchange.com/questions/425661/how-can-tasks-refuse-to-freeze-on-suspend

3、内核文档

https://docs.kernel.org/admin-guide/pm/suspend-flows.html

4、【原创】Linux Suspend流程分析 

这篇文章的绘图方法非常有启发性。

就是脑图的方式，但是把在相同文件里的函数用同一种颜色框起来。

看起来非常清晰。适合我分析代码的时候模仿。

作者是用visio画图的。

https://www.cnblogs.com/LoyenWang/p/11372679.html

