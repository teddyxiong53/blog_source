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