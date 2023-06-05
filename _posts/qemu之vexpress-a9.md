---
title: qemu之vexpress-a9
date: 2018-03-22 22:04:54
tags:
	- qemu

---



有必要对这个machine进行一个梳理了。

今天我尝试在qemu启动时，加上-device，来添加一些外设来测试驱动。

但是最终没有成功。



网上找的别人的例子。qemu的参数可以写到这么多，这么复杂。

```
qemu-system-x86_64 
-drive file=images/HLK-Client1-W10x64-1703.qcow2,serial=110011 
-netdev tap,id=hostnet0,script=./hck_ctrl_bridge_ifup_0011.sh,downscript=no,ifname=cc1_0011 -device e1000,netdev=hostnet0,mac=56:cc:cc:01:cc:cc,bus=pci.0,id=cc1_0011 
-netdev tap,id=hostnet2,vhost=on,script=./hck_test_bridge_ifup_0011.sh,downscript=no,ifname=t1c1_0011,queues=1 
-device virtio-net-pci,netdev=hostnet2,mac=56:cc:cc:01:01:cc,bus=pci.0,id=t1c1_0011 -uuid CDEF127c-8795-4e67-95da-8dd0a8891001 
-machine pc 
-nodefaults 
-nodefconfig 
-m 3G 
-smp 2,cores=2 
-enable-kvm 
-cpu qemu64,+x2apic,+fsgsbase,model=13 
-usbdevice tablet 
-boot order=cd,menu=on 
-rtc-td-hack 
-global kvm-pit.lost_tick_policy=discard 
-rtc base=localtime,clock=host,driftfix=slew 
-global PIIX4_PM.disable_s3=0 -global PIIX4_PM.disable_s4=0 
-name HCK-Client1_0011_bark_/home/lior/ivshmem 
-vga cirrus 
-vnc :32 
-monitor telnet::10032,server,nowait 
-monitor vc 
-chardev socket,path=/tmp/ivshmem_socket,id=ivshmemid 
-device ivshmem-doorbell,chardev=ivshmemid
```



根据这篇文章，https://wiki.linaro.org/PeterMaydell/QemuVersatileExpress

vexpress-a9的硬件情况：

```
Implemented components:
Quad-core A9MP
Up to 1GB RAM
SD/MMC card
CLCD graphics, keyboard and mouse
Serial ports
Timers and RTC
LAN9118 ethernet
-------------------------------------------------------
Missing components:
No USB (no model of the ISP1761 USB chip)
No modelling of the Flash memory
Components like the PL341 dynamic memory controller, PL354 static memory controller, PL310 L2 cache controller are not implemented (not even as dummy registers). This causes no problems for Linux booting but will probably be needed if we want to run u-boot or the VE boot ROM or other low level setup code
No Trustzone support (either in QEMU's A9 core model or in the Trustzone address space controller etc on the board)
We provide a PL110 CLCD controller, not a PL111
No Compact Flash
No audio (no PL041 model)
We don't implement remapping low memory; it is always RAM
No support for running the VE boot ROM -- you must provide the kernel and initrd directly to qemu

Note: there is no PCI, and therefore no way to expose an IDE or SCSI controller to the guest; the only available block device is the SD card. This is a limitation of the hardware, not a missing feature in qemu.
```

似乎支持的硬件非常少。

# chatgpt问到的

ARM Versatile Express（也称为 ARMv7-A Versatile Express）是一个开发和评估平台，旨在支持基于 ARMv7-A 架构的嵌入式系统软件开发。它是由 ARM 公司提供的硬件平台，用于在开发过程中进行软件验证、调试和性能评估。

Versatile Express 主要包含以下组件：

1. 主板（Motherboard）：提供了处理器插槽、内存插槽、外设接口等基本硬件组件。可以选择不同的主板模型，以适应不同的需求。

2. 处理器（Processor）：通常使用 ARM Cortex-A 系列处理器，如 Cortex-A9、Cortex-A15 等。这些处理器具有较高的性能和较低的功耗，适合嵌入式系统开发。

3. 外设模块（Peripheral Modules）：包括网络接口、串口、USB 接口、显示控制器、SD 卡接口等，用于连接外部设备和扩展模块。

4. 调试接口（Debug Interface）：支持通过 JTAG 或者其他调试接口进行软件调试和性能分析。

ARM Versatile Express 平台的优势在于它提供了一个完整的硬件环境，可以用于开发和测试各种嵌入式系统软件，包括操作系统内核、驱动程序、应用程序等。它广泛应用于嵌入式系统开发、物联网设备、嵌入式 Linux 等领域。

需要注意的是，ARM Versatile Express 平台是一个开发和评估平台，而不是用于生产的最终产品。它的主要目的是帮助开发人员快速验证和调试软件，以便在实际产品中部署。在将软件移植到其他 ARMv7-A 架构的硬件平台时，可能需要针对特定的目标硬件进行适配和优化。

# 硬件配置信息

