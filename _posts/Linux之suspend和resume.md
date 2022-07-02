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



# 参考资料

1、

https://blog.csdn.net/hshl1214/article/details/6228275

2、

https://unix.stackexchange.com/questions/425661/how-can-tasks-refuse-to-freeze-on-suspend