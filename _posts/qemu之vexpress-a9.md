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



