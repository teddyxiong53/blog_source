---
title: arm之wfi指令
date: 2023-02-13 11:19:17
tags:
	- arm

---



WFI指令的主要目的就是使core进入standby模式，直到中断或者类似中断的事件发送，才退出，core继续工作。



HINT 指令可以合法地被视为 NOP指令，但它们可以具有特定于实现的效果，常见的HINT指令有：

NOP // No operation，无操作， 不保证CPU会花时间去执行
YIELD // 提示当前线程正在执行可以换出的任务
WFE // Wait for Event，进入low power状态，直到等待的事件发生
WFI // Wait for interrupt，进入low power状态，直到等待的中断或与中断类似的操作发生
SEV // Send Event，发送事件，与WFE对应
SEVL // Send Event Local，发送本地事件，与WFE对应





# 参考资料

1、

https://blog.csdn.net/luolaihua2018/article/details/126773265

2、

http://www.wowotech.net/armv8a_arch/wfe_wfi.html