---
title: uboot之arm-trusted-firmware
date: 2022-11-29 11:07:32
tags:
	- uboot

---

--

arm-trusted-firmware缩写为ATF。下面都以ATF来称呼。

什么是ATF？

代码在这里：

https://github.com/ARM-software/arm-trusted-firmware.git

ATF冷启动实现分为5个步骤：

- BL1 - AP Trusted ROM，一般为BootRom。
- BL2 - Trusted Boot Firmware，一般为Trusted Bootloader。
- BL31 - EL3 Runtime Firmware，一般为SML，管理SMC执行处理和中断，运行在secure monitor中。
- BL32 - Secure-EL1 Payload，一般为TEE OS Image。
- BL33 - Non-Trusted Firmware，一般为uboot、linux kernel。



# 参考资料

1、ARM Trusted Firmware分析——启动、PSCI、OP-TEE接口

https://blog.csdn.net/kunkliu/article/details/124026280