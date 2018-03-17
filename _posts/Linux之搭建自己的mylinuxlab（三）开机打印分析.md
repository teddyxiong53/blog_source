---
title: Linux之搭建自己的mylinuxlab（三）开机打印分析
date: 2018-03-16 16:46:37
tags:
	- Linux

---



打印如下，一行一行注释。

```
Booting Linux on physical CPU 0x0 //当前是单核启动。
Linux version 4.14.0 (teddy@teddy-ubuntu) (gcc version 5.4.0 20160609 (Ubuntu/Linaro 5.4.0-6ubuntu1~16.04.9)) #12 SMP Fri Mar 16 16:54:39 CST 2018 //打印编译信息。
CPU: ARMv7 Processor [410fc090] revision 0 (ARMv7), cr=10c5387d //CPU信息。
CPU: PIPT / VIPT nonaliasing data cache, VIPT nonaliasing instruction cache
OF: fdt: Machine model: V2P-CA9//设备树信息。
Memory policy: Data cache writeback//存储的策略，
CPU: All CPU(s) started in SVC mode.
percpu: Embedded 16 pages/cpu @87eac000 s36428 r8192 d20916 u65536
Built 1 zonelists, mobility grouping on.  Total pages: 32512//内存总共的页数。是128M的物理内存。
Kernel command line: console=ttyAMA0//这个是编译进去的，我没有传递cmdline。
log_buf_len individual max cpu contribution: 4096 bytes
log_buf_len total cpu_extra contributions: 12288 bytes
log_buf_len min size: 16384 bytes
log_buf_len: 32768 bytes
early log buf free: 15028(91%)
PID hash table entries: 512 (order: -1, 2048 bytes)//pid的哈希表条目数。
Dentry cache hash table entries: 16384 (order: 4, 65536 bytes)
Inode-cache hash table entries: 8192 (order: 3, 32768 bytes)
Memory: 118728K/131072K available (6144K kernel code, 402K rwdata, 1368K rodata, 1024K init, 169K bss, 12344K reserved, 0K cma-reserved)
Virtual kernel memory layout://虚拟内存布局。
    vector  : 0xffff0000 - 0xffff1000   (   4 kB)
    fixmap  : 0xffc00000 - 0xfff00000   (3072 kB)
    vmalloc : 0x88800000 - 0xff800000   (1904 MB)//vmalloc给了很多啊。
    lowmem  : 0x80000000 - 0x88000000   ( 128 MB)//物理内存全部在这了。
    modules : 0x7f000000 - 0x80000000   (  16 MB)
      .text : 0x80008000 - 0x80700000   (7136 kB)
      .init : 0x80900000 - 0x80a00000   (1024 kB)
      .data : 0x80a00000 - 0x80a649d8   ( 403 kB)
       .bss : 0x80a6bcac - 0x80a96474   ( 170 kB)
SLUB: HWalign=64, Order=0-3, MinObjects=0, CPUs=4, Nodes=1
Hierarchical RCU implementation.
        RCU event tracing is enabled.
        RCU restricting CPUs from NR_CPUS=8 to nr_cpu_ids=4.
RCU: Adjusting geometry for rcu_fanout_leaf=16, nr_cpu_ids=4
NR_IRQS: 16, nr_irqs: 16, preallocated irqs: 16//中断个数是16个。
GIC CPU mask not found - kernel will fail to boot.
GIC CPU mask not found - kernel will fail to boot.
L2C: platform modifies aux control register: 0x02020000 -> 0x02420000//这些都是二级cache吧。
L2C: DT/platform modifies aux control register: 0x02020000 -> 0x02420000
L2C-310 enabling early BRESP for Cortex-A9
L2C-310 full line of zeros enabled for Cortex-A9
L2C-310 dynamic clock gating disabled, standby mode disabled
L2C-310 cache controller enabled, 8 ways, 128 kB
L2C-310: CACHE_ID 0x410000c8, AUX_CTRL 0x46420001
smp_twd: clock not found -2
sched_clock: 32 bits at 24MHz, resolution 41ns, wraps every 89478484971ns
clocksource: arm,sp804: mask: 0xffffffff max_cycles: 0xffffffff, max_idle_ns: 1911260446275 ns
Failed to initialize '/smb@4000000/motherboard/iofpga@7,00000000/timer@12000': -22
Console: colour dummy device 80x30//控制台。
Calibrating local timer... 96.04MHz.
Calibrating delay loop... 709.42 BogoMIPS (lpj=3547136)
pid_max: default: 32768 minimum: 301
Mount-cache hash table entries: 1024 (order: 0, 4096 bytes)
Mountpoint-cache hash table entries: 1024 (order: 0, 4096 bytes)
CPU: Testing write buffer coherency: ok
CPU0: thread -1, cpu 0, socket 0, mpidr 80000000
Setting up static identity map for 0x60100000 - 0x60100060
Hierarchical SRCU implementation.
smp: Bringing up secondary CPUs ...
smp: Brought up 1 node, 1 CPU
SMP: Total of 1 processors activated (709.42 BogoMIPS).
CPU: All CPU(s) started in SVC mode.
devtmpfs: initialized
random: get_random_u32 called from bucket_table_alloc+0xf0/0x240 with crng_init=0
VFP support v0.3: implementor 41 architecture 3 part 30 variant 9 rev 0
clocksource: jiffies: mask: 0xffffffff max_cycles: 0xffffffff, max_idle_ns: 19112604462750000 ns
futex hash table entries: 1024 (order: 4, 65536 bytes)
random: fast init done
NET: Registered protocol family 16 //注册了16号协议，就是netlink。
DMA: preallocated 256 KiB pool for atomic coherent allocations
cpuidle: using governor ladder
hw-breakpoint: debug architecture 0x4 unsupported.
Serial: AMBA PL011 UART driver
OF: amba_device_add() failed (-19) for /memory-controller@100e0000
OF: amba_device_add() failed (-19) for /memory-controller@100e1000
OF: amba_device_add() failed (-19) for /watchdog@100e5000
irq: type mismatch, failed to map hwirq-75 for /interrupt-controller@1e001000!
10009000.uart: ttyAMA0 at MMIO 0x10009000 (irq = 38, base_baud = 0) is a PL011 rev1
console [ttyAMA0] enabled //4个串口。
1000a000.uart: ttyAMA1 at MMIO 0x1000a000 (irq = 39, base_baud = 0) is a PL011 rev1
1000b000.uart: ttyAMA2 at MMIO 0x1000b000 (irq = 40, base_baud = 0) is a PL011 rev1
1000c000.uart: ttyAMA3 at MMIO 0x1000c000 (irq = 41, base_baud = 0) is a PL011 rev1
OF: amba_device_add() failed (-19) for /smb@4000000/motherboard/iofpga@7,00000000/wdt@f000
SCSI subsystem initialized
usbcore: registered new interface driver usbfs//usb相关注册。
usbcore: registered new interface driver hub
usbcore: registered new device driver usb
Advanced Linux Sound Architecture Driver Initialized.
clocksource: Switched to clocksource arm,sp804
NET: Registered protocol family 2//注册协议族2，就是AF_INET。
TCP established hash table entries: 1024 (order: 0, 4096 bytes)
TCP bind hash table entries: 1024 (order: 1, 8192 bytes)
TCP: Hash tables configured (established 1024 bind 1024)
UDP hash table entries: 256 (order: 1, 8192 bytes)
UDP-Lite hash table entries: 256 (order: 1, 8192 bytes)
NET: Registered protocol family 1//协议族1，就是AF_UNIX。
RPC: Registered named UNIX socket transport module.
RPC: Registered udp transport module.
RPC: Registered tcp transport module.
RPC: Registered tcp NFSv4.1 backchannel transport module.
Unpacking initramfs...//解压initramfs。
Freeing initrd memory: 972K
hw perfevents: enabled with armv7_cortex_a9 PMU driver, 1 counters available
workingset: timestamp_bits=30 max_order=15 bucket_order=0
squashfs: version 4.0 (2009/01/31) Phillip Lougher
jffs2: version 2.2. (NAND) © 2001-2006 Red Hat, Inc.
9p: Installing v9fs 9p2000 file system support
io scheduler noop registered (default)
io scheduler mq-deadline registered
io scheduler kyber registered
clcd-pl11x 10020000.clcd: PL111 designer 41 rev2 at 0x10020000
clcd-pl11x 10020000.clcd: /clcd@10020000 hardware, 1024x768@59 display
Console: switching to colour frame buffer device 128x48
clcd-pl11x 1001f000.clcd: PL111 designer 41 rev2 at 0x1001f000
clcd-pl11x 1001f000.clcd: /smb@4000000/motherboard/iofpga@7,00000000/clcd@1f000 hardware, 640x480@59 display
40000000.flash: Found 2 x16 devices at 0x0 in 32-bit bank. Manufacturer ID 0x000000 Chip ID 0x000000
Intel/Sharp Extended Query Table at 0x0031
Using buffer write method
40000000.flash: Found 2 x16 devices at 0x0 in 32-bit bank. Manufacturer ID 0x000000 Chip ID 0x000000
Intel/Sharp Extended Query Table at 0x0031
Using buffer write method
Concatenating MTD devices:
(0): "40000000.flash"
(1): "40000000.flash"
into device "40000000.flash"
libphy: Fixed MDIO Bus: probed
libphy: smsc911x-mdio: probed
smsc911x 4e000000.ethernet eth0: MAC Address: 52:54:00:12:34:56
isp1760 4f000000.usb: bus width: 32, oc: digital
isp1760 4f000000.usb: NXP ISP1760 USB Host Controller
isp1760 4f000000.usb: new USB bus registered, assigned bus number 1
isp1760 4f000000.usb: Scratch test failed.
isp1760 4f000000.usb: can't setup: -19
isp1760 4f000000.usb: USB bus 1 deregistered
usbcore: registered new interface driver usb-storage
rtc-pl031 10017000.rtc: rtc core: registered pl031 as rtc0
IR NEC protocol handler initialized
IR RC5(x/sz) protocol handler initialized
IR RC6 protocol handler initialized
IR JVC protocol handler initialized
IR Sony protocol handler initialized
IR SANYO protocol handler initialized
IR Sharp protocol handler initialized
IR MCE Keyboard/mouse protocol handler initialized
IR XMP protocol handler initialized
mmci-pl18x 10005000.mmci: Got CD GPIO
mmci-pl18x 10005000.mmci: Got WP GPIO
mmci-pl18x 10005000.mmci: mmc0: PL181 manf 41 rev0 at 0x10005000 irq 34,35 (pio)
ledtrig-cpu: registered to indicate activity on CPUs
usbcore: registered new interface driver usbhid
usbhid: USB HID core driver
input: AT Raw Set 2 keyboard as /devices/platform/smb@4000000/smb@4000000:motherboard/smb@4000000:motherboard:iofpga@7,00000000/10006000.kmi/serio0/input/input0
aaci-pl041 10004000.aaci: ARM AC'97 Interface PL041 rev0 at 0x10004000, irq 33
aaci-pl041 10004000.aaci: FIFO 512 entries
oprofile: using arm/armv7-ca9
NET: Registered protocol family 17
9pnet: Installing 9P2000 support
Registering SWP/SWPB emulation handler
rtc-pl031 10017000.rtc: setting system clock to 2018-03-16 11:07:38 UTC (1521198458)
ALSA device list:
  #0: ARM AC'97 Interface PL041 rev0 at 0x10004000, irq 33
xhl -- func:kernel_init_freeable, line:1084 ,rd cmd:/init ,ret:0 
xhl -- func:kernel_init_freeable, line:1089 
Freeing unused kernel memory: 1024K
/dev/pts not exist, now creat it
Generic PHY 4e000000.ethernet-ffffffff:01: attached PHY driver [Generic PHY] (mii_bus:phy_addr=4e000000.ethernet-ffffffff:01, irq=POLL)
smsc911x 4e000000.ethernet eth0: SMSC911x/921x identified at 0x89290000, IRQ: 31

Please press Enter to activate this console. input: ImExPS/2 Generic Explorer Mouse as /devices/platform/smb@4000000/smb@4000000:motherboard/smb@4000000:motherboard:iofpga@7,00000000/10007000.kmi/serio1/input/input2
```





从启动过程，可以看到的一句打印是：

```
Unpacking initramfs...
```

这句话是在linux/init/initramfs.c里的populate_rootfs函数里的。

这个函数是放在init段里被调用到的。

