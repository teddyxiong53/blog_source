---
title: fastboot基本命令
date: 2017-06-29 21:01:57
tags:

	- 刷机

---

在设备进入到 fastboot 环境后，根据需求执行下面的命令进行刷机：
  fastboot  flashing  unlock    # 设备解锁，开始刷机
  fastboot  flash  boot  boot.img    # 刷入 boot 分区。如果修改了 kernel 代码，则应该刷入此分区以生效
  fastboot  flash  recovery  recovery.img    # 刷入 recovery 分区
  fastboot  flash  country  country.img    # 刷入 country 分区。这个分区是开发组自己划分的，别的 Android 设备上不一定有
  fastboot  flash  system  system.img    # 刷入 system 分区。如果修改的代码会影响 out/system/ 路径下生成的文件，则应该刷入此分区以生效 
  fastboot  flash  bootloader  bootloader    # 刷入 bootloader
  fastboot  erase  frp    # 擦除 frp 分区，frp 即 Factory Reset Protection，用于防止用户信息在手机丢失后外泄
  fastboot  format  data    # 格式化 data 分区
  fastboot  flashing lock    # 设备上锁，刷机完毕
  fastboot  continue    # 自动重启设备

