---
title: openwrt（一）
date: 2018-04-10 15:29:44
tags:
	- openwrt
typora-root-url: ..\
---



#编译

现在自己来编译openwrt。

从github上下载代码压缩包。是基于buildroot的。所以make过程中才去下载大量的东西。这个是比较麻烦的一步，因为有很多的编译错误要解决，还有联网下载的东西，在国内的网络环境下，都比较慢，最好带着翻墙工具来做。

我们先看看压缩包的内容：

```
teddy@teddy-ubuntu:~/work/openwrt/tmp/openwrt-master$ tree -L 1
.
├── BSDmakefile
├── config：这个目录下，是几个配置文件。
├── Config.in
├── feeds.conf.default
├── include：全部是mk文件。
├── LICENSE
├── Makefile
├── package：应该用来跟标准的kernel、boot、rootfs进行合并用的特别代码文件。
├── README
├── rules.mk
├── scripts：shell和perl脚本。
├── target：也是一项特别的c文件。
├── toolchain：工具链的补丁。
└── tools：工具的补丁。
```

执行make后，会多出这些目录。

```
1、build_dir。
	这个下面有有3个子目录。都是编译输出的内容。
	host
	target
	toolchain
2、dl目录。
	make过程中下载的内容都在这里。
3、staging_dir。
	跟build_dir类型。
4、tmp。
	这里放一些临时文件。
5..config文件。
	配置文件。
```

编译过程是：

1、make menuconfig。

选择树莓派的方案。

2、make。

这里面会出现很多的错误。一个个解决。

这个编译还有一个比较烦人的问题，就编译不给详细打印。有时候卡住很久。

```
make V=99 -j4
```

V为什么要给99？我也是网上看到 。还有V=s的。但是我V=1，好像没有看到太多打印。

99和s是等价的。在include/verbose.mk里。

```
ifeq ($(OPENWRT_VERBOSE),1)
  OPENWRT_VERBOSE:=w
endif
ifeq ($(OPENWRT_VERBOSE),99)
  OPENWRT_VERBOSE:=s
endif
```



这样编译了10几分钟，编译通过。因为我之前编译过一次，已经下载完成了大部分的文件。

编译完成，需要关注的就是bin目录下的内容。

```
└── targets
    └── brcm2708
        └── bcm2708
            ├── config.seed
            ├── openwrt-brcm2708-bcm2708-device-rpi.manifest
            ├── openwrt-brcm2708-bcm2708-rpi-ext4-sdcard.img.gz  #这个就是我们要关注的。
```

我之前直接下载的镜像文件是这样：

```
lede-17.02.0-rc1-brcm2708-bcm2710-rpi-3-ext4-sdcard-angelina-ace-201760714.img
```



# 烧录到树莓派上

1、我们把bin/targets/bcm2708/bcm2708/open-bcm2708-bcm2708-rpi-ext4-sdcard.img.gz文件解压。

```
teddy@teddy-ubuntu:~/work/openwrt/openwrt-master/bin/targets/brcm2708/bcm2708$ gzip -d openwrt-brcm2708-bcm2708-rpi-ext4-sdcard.img.gz 
```

解压后的大小是284M。

```
-rw-r--r-- 1 teddy teddy 284M 4月  10 16:02 openwrt-brcm2708-bcm2708-rpi-ext4-sdcard.img
```

我之前下载的lede的img文件是1.02G。确实大了很多。

2、我们用Win32DiskImager工具，把解压搭建镜像文件烧录到U盘里。

因为默认配置的cmdline是从 SD卡的分区启动的，所以我们烧录后，要通过pc把boot分区的配置改一下。

把cmdline.txt修改为：

```
dwc_otg.lpm_enable=0 console=serial0,115200 kgdboc=serial0,115200 console=tty1 root=/dev/sda2  rootfstype=ext4 rootwait
```

3、把U盘插到树莓派上，启动，发现启动不了。串口没有看到打印。

我查看我之前写的树莓派从U盘启动的文章。发现还需要在config.txt里加上这些：

```
program_usb_boot_mode=1 #我觉得当前的关键在这里。
enable_uart=1 #这个当前已经有了。
start_x=0 #这个可以没有。加上也没事。
```

如果还不行，我还得替换start.elf和bootcode.bin文件。

确实还是不行，我从我其他的树莓派的机器里，拷贝start.elf和bootcode.bin文件。

发现是我的串口弄错了。串口1不是我插入的usb串口。

不知道为什么当前这个usb口识别不了我的串口，我换个usb口就好了。

如果还是不行的话，就用SD卡看看。

换SD卡的还是不行。算了。先不管了。

我先用现成的镜像来启动。

之前可以的镜像，现在怎么也不行了？我把U盘换了个usb口插入就可以了。

# 卡机后基本情况

开机打印如下，逐条分析一下。

```
[    0.000000] Booting Linux on physical CPU 0x0
[    0.000000] Linux version 4.4.71 (buildbot@builds-02.infra.lede-project.org) (gcc version 5.4.0 (LEDE GCC 5.4.0 r3103-1b51a49) ) #0 SMP Wed Jun 7 19:24:41 2017
[    0.000000] CPU: ARMv7 Processor [410fd034] revision 4 (ARMv7), cr=10c5383d
[    0.000000] CPU: PIPT / VIPT nonaliasing data cache, VIPT aliasing instruction cache
[    0.000000] Machine model: Raspberry Pi 3 Model B Rev 1.2
[    0.000000] cma: Reserved 16 MiB at 0x06c00000 #这里保留了16M的cma。做什么用了呢？值得研究一下。
[    0.000000] Memory policy: Data cache writealloc
[    0.000000] [bcm2709_smp_init_cpus] enter (9480->f3003010)
[    0.000000] [bcm2709_smp_init_cpus] ncores=4
[    0.000000] PERCPU: Embedded 12 pages/cpu @87eac000 s17984 r8192 d22976 u49152
[    0.000000] Built 1 zonelists in Zone order, mobility grouping on.  Total pages: 32512
[    0.000000] Kernel command line: 8250.nr_uarts=1 bcm2708_fb.fbwidth=656 bcm2708_fb.fbheight=416 bcm2708_fb.fbswap=1 dma.dmachans=0x7f35 bcm2709.boardrev=0xa22082 bcm2709.serial=0x5e004eca bcm2709.uart_clock=48000000 smsc95xx.macaddr=B8:27:EB:00:4E:CA vc_mem.mem_base=0xec00000 vc_mem.mem_size=0x10000000  dwc_otg.lpm_enable=0 console=ttyS0,115200 kgdboc=ttyS0,115200 console=tty1 root=/dev/sda2 rootfstype=ext4 rootwait
[    0.000000] PID hash table entries: 512 (order: -1, 2048 bytes)
[    0.000000] Dentry cache hash table entries: 16384 (order: 4, 65536 bytes)
[    0.000000] Inode-cache hash table entries: 8192 (order: 3, 32768 bytes)
[    0.000000] Memory: 107696K/131072K available (4087K kernel code, 134K rwdata, 684K rodata, 224K init, 373K bss, 6992K reserved, 16384K cma-reserved)
[    0.000000] Virtual kernel memory layout:
[    0.000000]     vector  : 0xffff0000 - 0xffff1000   (   4 kB)
[    0.000000]     fixmap  : 0xffc00000 - 0xfff00000   (3072 kB)
[    0.000000]     vmalloc : 0x88800000 - 0xff800000   (1904 MB)
[    0.000000]     lowmem  : 0x80000000 - 0x88000000   ( 128 MB)
[    0.000000]     modules : 0x7f000000 - 0x80000000   (  16 MB)
[    0.000000]       .text : 0x80008000 - 0x804b102c   (4773 kB)
[    0.000000]       .init : 0x804b2000 - 0x804ea000   ( 224 kB)
[    0.000000]       .data : 0x804ea000 - 0x8050bb48   ( 135 kB)
[    0.000000]        .bss : 0x8050bb48 - 0x805691b8   ( 374 kB)
[    0.000000] SLUB: HWalign=64, Order=0-3, MinObjects=0, CPUs=4, Nodes=1
[    0.000000] Hierarchical RCU implementation.
[    0.000000] NR_IRQS:16 nr_irqs:16 16 //总共16个中断。
[    0.000000] Architected cp15 timer(s) running at 19.20MHz (phys).
[    0.000000] clocksource: arch_sys_counter: mask: 0xffffffffffffff max_cycles: 0x46d987e47, max_idle_ns: 440795202767 ns
[    0.000006] sched_clock: 56 bits at 19MHz, resolution 52ns, wraps every 4398046511078ns
[    0.000020] Switching to timer-based delay loop, resolution 52ns
[    0.000169] Console: colour dummy device 80x30
[    0.000817] console [tty1] enabled
[    0.000854] Calibrating delay loop (skipped), value calculated using timer frequency.. 38.40 BogoMIPS (lpj=192000)
[    0.000906] pid_max: default: 32768 minimum: 301
[    0.001021] Mount-cache hash table entries: 1024 (order: 0, 4096 bytes)
[    0.001053] Mountpoint-cache hash table entries: 1024 (order: 0, 4096 bytes)
[    0.001616] CPU: Testing write buffer coherency: ok
[    0.001938] CPU0: update cpu_capacity 1024
[    0.001967] CPU0: thread -1, cpu 0, socket 0, mpidr 80000000
[    0.001994] [bcm2709_smp_prepare_cpus] enter
[    0.002043] Setting up static identity map for 0x8240 - 0x8298
[    0.003050] [bcm2709_boot_secondary] cpu:1 failed to start (9480)
[    0.003245] [bcm2709_secondary_init] enter cpu:1
[    0.003272] CPU1: update cpu_capacity 1024
[    0.003278] CPU1: thread -1, cpu 1, socket 0, mpidr 80000001
[    0.003566] [bcm2709_boot_secondary] cpu:2 failed to start (9480)
[    0.003755] [bcm2709_secondary_init] enter cpu:2
[    0.003774] CPU2: update cpu_capacity 1024
[    0.003780] CPU2: thread -1, cpu 2, socket 0, mpidr 80000002
[    0.004058] [bcm2709_boot_secondary] cpu:3 failed to start (9480)
[    0.004244] [bcm2709_secondary_init] enter cpu:3
[    0.004263] CPU3: update cpu_capacity 1024
[    0.004269] CPU3: thread -1, cpu 3, socket 0, mpidr 80000003
[    0.004320] Brought up 4 CPUs //4个CPU都已经启动了。
[    0.004410] SMP: Total of 4 processors activated (153.60 BogoMIPS).
[    0.004436] CPU: All CPU(s) started in HYP mode.
[    0.004460] CPU: Virtualization extensions available.
[    0.013421] VFP support v0.3: implementor 41 architecture 3 part 40 variant 3 rev 4
[    0.013682] clocksource: jiffies: mask: 0xffffffff max_cycles: 0xffffffff, max_idle_ns: 19112604462750000 ns
[    0.013738] futex hash table entries: 1024 (order: 4, 65536 bytes)
[    0.014374] pinctrl core: initialized pinctrl subsystem
[    0.014938] NET: Registered protocol family 16
[    0.019958] DMA: preallocated 4096 KiB pool for atomic coherent allocations
[    0.049940] cpuidle: using governor ladder
[    0.079958] cpuidle: using governor menu
[    0.085955] bcm2709: Mini UART enabled
[    0.086040] Serial: AMBA PL011 UART driver
[    0.086182] uart-pl011 3f201000.uart: could not find pctldev for node /soc/gpio@7e200000/uart0_pins, deferring probe
[    0.086357] bcm2835-mbox 3f00b880.mailbox: mailbox enabled
[    0.131001] bcm2835-dma 3f007000.dma: DMA legacy API manager at f3007000, dmachans=0x1
[    0.131224] SCSI subsystem initialized
[    0.131311] usbcore: registered new interface driver usbfs
[    0.131360] usbcore: registered new interface driver hub
[    0.131403] usbcore: registered new device driver usb
[    0.139982] raspberrypi-firmware soc:firmware: Attached to firmware from 2018-03-07 19:08
[    0.165787] clocksource: Switched to clocksource arch_sys_counter
[    0.169601] NET: Registered protocol family 2
[    0.169950] TCP established hash table entries: 1024 (order: 0, 4096 bytes)
[    0.169975] TCP bind hash table entries: 1024 (order: 1, 8192 bytes)
[    0.170024] TCP: Hash tables configured (established 1024 bind 1024)
[    0.170067] UDP hash table entries: 256 (order: 1, 8192 bytes)
[    0.170091] UDP-Lite hash table entries: 256 (order: 1, 8192 bytes)
[    0.170185] NET: Registered protocol family 1
[    0.170980] Crashlog allocated RAM at address 0x3f00000
[    0.175455] io scheduler noop registered
[    0.175472] io scheduler deadline registered
[    0.175497] io scheduler cfq registered (default)
[    0.176774] BCM2708FB: allocated DMA memory c7010000
[    0.176797] BCM2708FB: allocated DMA channel 0 @ f3007000
[    0.181616] Console: switching to colour frame buffer device 82x26
[    0.184733] Serial: 8250/16550 driver, 1 ports, IRQ sharing enabled
[    0.186168] console [ttyS0] disabled
[    0.187192] 3f215040.uart: ttyS0 at MMIO 0x3f215040 (irq = 59, base_baud = 50000000) is a 16550
[    0.789569] console [ttyS0] enabled
[    0.794411] vc-cma: Videocore CMA driver
[    0.799375] vc-cma: vc_cma_base      = 0x00000000
[    0.805106] vc-cma: vc_cma_size      = 0x00000000 (0 MiB)
[    0.811517] vc-cma: vc_cma_initial   = 0x00000000 (0 MiB)
[    0.817956] vc-mem: phys_addr:0x00000000 mem_base=0x0ec00000 mem_size:0x10000000(256 MiB)
[    0.833650] brd: module loaded
[    0.841137] loop: module loaded
[    0.845631] vchiq: vchiq_init_state: slot_zero = 0x87080000, is_master = 0
[    0.854607] usbcore: registered new interface driver smsc95xx
[    0.861382] dwc_otg: version 3.00a 10-AUG-2012 (platform bus)
[    1.068285] Core Release: 2.80a
[    1.072411] Setting default values for core params
[    1.078245] Finished setting default values for core params
[    1.285040] Using Buffer DMA mode
[    1.289357] Periodic Transfer Interrupt Enhancement - disabled
[    1.296254] Multiprocessor Interrupt Enhancement - disabled
[    1.302874] OTG VER PARAM: 0, OTG VER FLAG: 0
[    1.308238] Dedicated Tx FIFOs mode
[    1.312830] WARN::dwc_otg_hcd_init:1047: FIQ DMA bounce buffers: virt = 0x87004000 dma = 0xc7004000 len=9024
[    1.324754] FIQ FSM acceleration enabled for :
[    1.324754] Non-periodic Split Transactions
[    1.324754] Periodic Split Transactions
[    1.324754] High-Speed Isochronous Endpoints
[    1.324754] Interrupt/Control Split Transaction hack enabled
[    1.352412] WARN::hcd_init_fiq:415: FIQ on core 1 at 0x802a3910
[    1.359407] WARN::hcd_init_fiq:416: FIQ ASM at 0x8000ee60 length 36
[    1.366771] WARN::hcd_init_fiq:441: MPHI regs_base at 0x8887a000
[    1.373873] dwc_otg 3f980000.usb: DWC OTG Controller
[    1.379892] dwc_otg 3f980000.usb: new USB bus registered, assigned bus number 1
[    1.388306] dwc_otg 3f980000.usb: irq 62, io mem 0x00000000
[    1.394942] Init: Port Power? op_state=1
[    1.399872] Init: Power Port (0)
[    1.404162] usb usb1: New USB device found, idVendor=1d6b, idProduct=0002
[    1.412025] usb usb1: New USB device strings: Mfr=3, Product=2, SerialNumber=1
[    1.420323] usb usb1: Product: DWC OTG Controller
[    1.426043] usb usb1: Manufacturer: Linux 4.4.71 dwc_otg_hcd
[    1.432730] usb usb1: SerialNumber: 3f980000.usb
[    1.438675] hub 1-0:1.0: USB hub found
[    1.443398] hub 1-0:1.0: 1 port detected
[    1.448610] usbcore: registered new interface driver uas
[    1.454918] usbcore: registered new interface driver usb-storage
[    1.461948] mousedev: PS/2 mouse device common for all mice
[    1.468859] bcm2835-wdt 3f100000.watchdog: Broadcom BCM2835 watchdog timer
[    1.476814] sdhci: Secure Digital Host Controller Interface driver
[    1.484011] sdhci: Copyright(c) Pierre Ossman
[    1.489472] sdhost: log_buf @ 87007000 (c7007000)
[    1.555791] mmc0: sdhost-bcm2835 loaded - DMA enabled (>1)
[    1.564300] mmc-bcm2835 3f300000.mmc: mmc_debug:0 mmc_debug2:0
[    1.571160] mmc-bcm2835 3f300000.mmc: DMA channel allocated
[    1.615826] sdhci-pltfm: SDHCI platform and OF driver helper
[    1.623316] NET: Registered protocol family 10
[    1.629187] NET: Registered protocol family 17
[    1.634611] bridge: automatic filtering via arp/ip/ip6tables has been deprecated. Update your scripts to load br_netfilter if you need this.
[    1.649261] 8021q: 802.1Q VLAN Support v1.8
[    1.654651] Registering SWP/SWPB emulation handler
[    1.660714] vc-sm: Videocore shared memory driver
[    1.666424] [vc_sm_connected_init]: start
[    1.671537] Indeed it is in host mode hprt0 = 00021501
[    1.685921] [vc_sm_connected_init]: end - returning 0
[    1.693073] 3f201000.uart: ttyAMA0 at MMIO 0x3f201000 (irq = 87, base_baud = 0) is a PL011 rev2
[    1.704104] of_cfs_init
[    1.707587] of_cfs_init: OK
[    1.711754] Waiting for root device /dev/sda2... //这里开始等U盘。
[    1.842389] mmc1: queuing unknown CIS tuple 0x80 (2 bytes)
[    1.850750] mmc1: queuing unknown CIS tuple 0x80 (3 bytes)
[    1.855795] usb 1-1: new high-speed USB device number 2 using dwc_otg
[    1.855862] Indeed it is in host mode hprt0 = 00001101
[    1.872654] mmc1: queuing unknown CIS tuple 0x80 (3 bytes)
[    1.882460] mmc1: queuing unknown CIS tuple 0x80 (7 bytes)
[    1.994042] mmc1: new high speed SDIO card at address 0001
[    2.055915] usb 1-1: New USB device found, idVendor=0424, idProduct=9514
[    2.063661] usb 1-1: New USB device strings: Mfr=0, Product=0, SerialNumber=0
[    2.072129] hub 1-1:1.0: USB hub found
[    2.076864] hub 1-1:1.0: 5 ports detected
[    2.355792] usb 1-1.1: new high-speed USB device number 3 using dwc_otg
[    2.475902] usb 1-1.1: New USB device found, idVendor=0424, idProduct=ec00
[    2.483798] usb 1-1.1: New USB device strings: Mfr=0, Product=0, SerialNumber=0
[    2.494438] smsc95xx v1.0.4
[    2.557361] smsc95xx 1-1.1:1.0 eth0: register 'smsc95xx' at usb-3f980000.usb-1.1, smsc95xx USB 2.0 Ethernet, b8:27:eb:00:4e:ca
[    3.025790] usb 1-1.2: new high-speed USB device number 4 using dwc_otg
[    3.142730] usb 1-1.2: New USB device found, idVendor=058f, idProduct=6387
[    3.150732] usb 1-1.2: New USB device strings: Mfr=1, Product=2, SerialNumber=3
[    3.159177] usb 1-1.2: Product: Mass Storage
[    3.164506] usb 1-1.2: Manufacturer: Generic
[    3.169855] usb 1-1.2: SerialNumber: C1FE869E
[    3.175607] usb-storage 1-1.2:1.0: USB Mass Storage device detected
[    3.183135] scsi host0: usb-storage 1-1.2:1.0
[    4.187512] scsi 0:0:0:0: Direct-Access     Generic  Flash Disk       8.07 PQ: 0 ANSI: 4
[    4.198854] sd 0:0:0:0: [sda] 31129600 512-byte logical blocks: (15.9 GB/14.8 GiB)
[    4.209350] sd 0:0:0:0: [sda] Write Protect is off
[    4.215937] sd 0:0:0:0: [sda] Write cache: disabled, read cache: enabled, doesn't support DPO or FUA
[    4.231582]  sda: sda1 sda2
[    4.237619] sd 0:0:0:0: [sda] Attached SCSI removable disk
[    4.250280] EXT4-fs (sda2): mounted filesystem without journal. Opts: (null)
[    4.258623] VFS: Mounted root (ext4 filesystem) readonly on device 8:2.
[    4.266642] Freeing unused kernel memory: 224K (804b2000 - 804ea000)
[    4.356536] init: Console is alive
[    4.361163] init: - watchdog -
[    4.946395] kmodloader: loading kernel modules from /etc/modules-boot.d/*
[    4.978504] pps_core: LinuxPPS API ver. 1 registered
[    4.984639] pps_core: Software ver. 5.3.6 - Copyright 2005-2007 Rodolfo Giometti <giometti@linux.it>
[    5.003177] softdog: Software Watchdog Timer: 0.08 initialized. soft_noboot=0 soft_margin=60 sec soft_panic=0 (nowayout=0)
[    5.022877] kmodloader: done loading kernel modules from /etc/modules-boot.d/*
[    5.039551] init: - preinit -
[    5.176871] smsc95xx 1-1.1:1.0 eth0: hardware isn't capable of remote wakeup
[    5.185445] IPv6: ADDRCONF(NETDEV_UP): eth0: link is not ready
[    6.691439] IPv6: ADDRCONF(NETDEV_CHANGE): eth0: link becomes ready
[    6.699515] smsc95xx 1-1.1:1.0 eth0: link up, 100Mbps, full-duplex, lpa 0xCDE1
[    7.578879] random: nonblocking pool is initialized
[    8.244166] mount_root: mounting /dev/root
[    9.682134] EXT4-fs (sda2): re-mounted. Opts: (null)
[    9.688577] mount_root: loading kmods from internal overlay
[    9.710017] kmodloader: loading kernel modules from //etc/modules-boot.d/*
[    9.719116] kmodloader: done loading kernel modules from //etc/modules-boot.d/*
[   10.458186] block: attempting to load /etc/config/fstab
[   10.466749] block: extroot: not configured
[   10.473230] urandom-seed: Seeding with /etc/urandom.seed
[   10.500461] smsc95xx 1-1.1:1.0 eth0: hardware isn't capable of remote wakeup
[   10.511326] procd: - early -
[   10.515494] procd: - watchdog -
[   11.124188] procd: - ubus -
[   11.279868] procd: - init -
Please press Enter to activate this console.
[   11.517955] kmodloader: loading kernel modules from /etc/modules.d/*
[   11.531905] bcm2835-rng 3f104000.rng: hwrng registered
[   11.547766] NET: Registered protocol family 8
[   11.553303] NET: Registered protocol family 20
[   11.562333] device-mapper: ioctl: 4.34.0-ioctl (2015-10-28) initialised: dm-devel@redhat.com
[   11.586996] tun: Universal TUN/TAP device driver, 1.6
[   11.593139] tun: (C) 1999-2004 Max Krasnyansky <maxk@qualcomm.com>
[   11.609827] l2tp_core: L2TP core driver, V2.0
[   11.615747] l2tp_netlink: L2TP netlink interface
[   11.623294] sit: IPv6 over IPv4 tunneling driver
[   11.632856] nat46: module (version 8ff2ae59ec9840a7b8b45f976c51cae80abe0226) loaded.
[   11.647242] gre: GRE over IPv4 demultiplexor driver
[   11.653943] ip_gre: GRE over IPv4 tunneling driver
[   11.664682] PPP generic driver version 2.4.2
[   11.674408] ip6_tables: (C) 2000-2006 Netfilter Core Team
[   11.684141] Netfilter messages via NETLINK v0.30.
[   11.691131] ip_set: protocol 6
[   11.728607] lp: driver loaded but no devices found
[   11.736505] ppdev: user-space parallel port driver
[   11.747651] i2c /dev entries driver
[   11.770741] bcm2708_i2c 3f205000.i2c: BSC0 Controller at 0x3f205000 (irq 83) (baudrate 100000)
[   11.782071] bcm2708_i2c 3f804000.i2c: BSC1 Controller at 0x3f804000 (irq 83) (baudrate 100000)
[   11.798193] usbcore: registered new interface driver i2c-tiny-usb
[   11.817448] Linux video capture interface: v2.00
[   11.828938] hidraw: raw HID events driver (C) Jiri Kosina
[   11.863322] fuse init (API version 7.23)
[   11.932036] Loading modules backported from Linux version wt-2017-01-31-0-ge882dff19e7f
[   11.942462] Backport generated by backports.git backports-20160324-13-g24da7d3c
[   11.952635] ip_tables: (C) 2000-2006 Netfilter Core Team
[   11.973436] nf_conntrack version 0.5.0 (1942 buckets, 7768 max)
[   11.981590] ctnetlink v0.93: registering with nfnetlink.
[   12.107842] PPP MPPE Compression module registered
[   12.114286] NET: Registered protocol family 24
[   12.120366] PPTP driver version 0.8.5
[   12.126565] usbcore: registered new interface driver Philips webcam
[   12.135662] usbcore: registered new interface driver r8712u
[   12.146814] usbcore: registered new interface driver ums-alauda
[   12.154254] usbcore: registered new interface driver ums-cypress
[   12.161744] usbcore: registered new interface driver ums-datafab
[   12.169117] usbcore: registered new interface driver ums-freecom
[   12.176480] usbcore: registered new interface driver ums-isd200
[   12.183656] usbcore: registered new interface driver ums-jumpshot
[   12.190966] usbcore: registered new interface driver ums-karma
[   12.198076] usbcore: registered new interface driver ums-sddr09
[   12.205156] usbcore: registered new interface driver ums-sddr55
[   12.212211] usbcore: registered new interface driver ums-usbat
[   12.219898] usbcore: registered new interface driver usbhid
[   12.226236] usbhid: USB HID core driver
[   12.232811] usbcore: registered new interface driver uvcvideo
[   12.239288] USB Video Class driver (1.1.1)
[   12.246630] Driver for 1-wire Dallas network protocol.
[   12.260774] xt_time: kernel timezone is -0000
[   12.277395] usbcore: registered new interface driver DS9490R
[   12.285552] l2tp_ppp: PPPoL2TP kernel driver, V2.0
[   12.321431] usbcore: registered new interface driver rt73usb
[   12.328737] usbcore: registered new interface driver rtl8187
[   12.340367] 1-Wire driver for the DS2760 battery monitor chip - (c) 2004-2005, Szabolcs Gyurko
[   12.491766] brcmfmac: brcmf_c_preinit_dcmds: Firmware version = wl0: Aug 29 2016 20:48:16 version 7.45.41.26 (r640327) FWID 01-4527cfab
[   12.513262] brcmfmac: brcmf_cfg80211_reg_notifier: not a ISO3166 code (0x30 0x30)
[   12.536543] usbcore: registered new interface driver brcmfmac
[   12.544999] usbcore: registered new interface driver rt2500usb
[   12.556044] usbcore: registered new interface driver rt2800usb
[   12.567905] usbcore: registered new interface driver rtl8192cu
[   12.578521] usbcore: registered new interface driver ath9k_htc
[   12.585583] kmodloader: done loading kernel modules from /etc/modules.d/*
[   16.356987] smsc95xx 1-1.1:1.0 eth0: hardware isn't capable of remote wakeup
[   16.366923] device eth0 entered promiscuous mode
[   16.373701] br-lan: port 1(eth0) entered forwarding state
[   16.380241] br-lan: port 1(eth0) entered forwarding state
[   17.957975] smsc95xx 1-1.1:1.0 eth0: link up, 100Mbps, full-duplex, lpa 0xCDE1
[   18.375813] br-lan: port 1(eth0) entered forwarding state


BusyBox v1.25.1 () built-in shell (ash)

     _________
    /        /\      _    ___ ___  ___
   /  LE    /  \    | |  | __|   \| __|
  /    DE  /    \   | |__| _|| |) | _|
 /________/  LE  \  |____|___|___/|___|                      lede-project.org
 \        \   DE / -----------------------------------------------------------
  \    LE  \    /   Reboot (17.01.2, r3435-65eec8bd5f)
   \  DE    \  /    Build By:Angelina_ACE
    \________\/    -----------------------------------------------------------

=== WARNING! =====================================
There is no root password defined on this device!
Use the "passwd" command to set up a new password
in order to prevent unauthorized SSH logins.
--------------------------------------------------
root@LEDE:/# 上面这里提示，root用户没有配置密码的。
root@LEDE:/# 
```

磁盘的基本情况是这样：

```
root@LEDE:/# df -h
Filesystem                Size      Used Available Use% Mounted on
/dev/root              1007.9M    323.9M    668.0M  33% /
tmpfs                    60.7M      3.2M     57.4M   5% /tmp
tmpfs                   512.0K         0    512.0K   0% /dev
```

只用了1个G空间。

文件系统情况：

```
root@LEDE:/# mount
/dev/sda2 on / type ext4 (rw,noatime,block_validity,delalloc,barrier,user_xattr)
proc on /proc type proc (rw,nosuid,nodev,noexec,noatime)
sysfs on /sys type sysfs (rw,nosuid,nodev,noexec,noatime)
tmpfs on /tmp type tmpfs (rw,nosuid,nodev,noatime)
tmpfs on /dev type tmpfs (rw,nosuid,relatime,size=512k,mode=755)
devpts on /dev/pts type devpts (rw,nosuid,noexec,relatime,mode=600)
debugfs on /sys/kernel/debug type debugfs (rw,noatime)
```

#openwrt通过路由器联网

其实这里要做的，就是让openwrt成为一个中间节点。拓扑结构是这样的：

```
手机 --> 树莓派openwrt --> 路由器 --> internet
```

所以openwrt要做一个转发。它还要是一个wifi热点。

1、配置树莓派的eth0的ip地址。

```
ifconfig eth0 192.168.0.100 netmask 255.255.255.0
route add default gw 192.168.0.1
```

2、看看能不能ping通我的路由器。

无法ping通。

我拔插了一下网线，有这个打印。

```
root@LEDE:~# [ 1144.653140] smsc95xx 1-1.1:1.0 eth0: link down
[ 1144.658916] br-lan: port 1(eth0) entered disabled state
[ 1146.229631] smsc95xx 1-1.1:1.0 eth0: link up, 100Mbps, full-duplex, lpa 0xCDE1
[ 1146.240215] br-lan: port 1(eth0) entered forwarding state
[ 1146.246800] br-lan: port 1(eth0) entered forwarding state
[ 1148.245794] br-lan: port 1(eth0) entered forwarding state
```

openwrt的配置文件大部分都在/etc/config目录下。这个是自己的一套规则，跟Ubuntu那些不是一套规则。

我在这个目录下，把eth0的网卡地址改为192.168.0.100，我的路由器分配都是在192.168.0.x这个网段。

把系统重启。

看到eth0的ip地址还是没有自动配置，但是这一次，我手动配置后，就可以ping通了。

现在我们的openwrt自己已经可以ping通外网了。

接下来要让我们的手机可以连接到树莓派产生的热点上。

默认的配置/etc/config/wireless是这样的。

```
config wifi-device 'radio0'
        option type 'mac80211'
        option channel '11'
        option hwmode '11g'
        option path 'platform/soc/3f300000.mmc/mmc_host/mmc1/mmc1:0001/mmc1:
0001:1'
        option htmode 'HT20'
        option disabled '1'

config wifi-iface 'default_radio0'
        option device 'radio0'
        option network 'lan'
        option mode 'ap'
        option ssid 'LEDE'
        option encryption 'none'
```

现在系统里的网卡情况是：

```
root@LEDE:/etc/config# ifconfig -a
br-lan    Link encap:Ethernet  HWaddr B8:27:EB:00:4E:CA  
          inet addr:192.168.0.100  Bcast:192.168.0.255  Mask:255.255.255.0
          inet6 addr: fe80::ba27:ebff:fe00:4eca/64 Scope:Link
          inet6 addr: fda9:2172:1e8c::1/60 Scope:Global
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:378 errors:0 dropped:0 overruns:0 frame:0
          TX packets:144 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:33407 (32.6 KiB)  TX bytes:12730 (12.4 KiB)

eth0      Link encap:Ethernet  HWaddr B8:27:EB:00:4E:CA  
          inet addr:192.168.0.100  Bcast:192.168.0.255  Mask:255.255.255.0
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:378 errors:0 dropped:0 overruns:0 frame:0
          TX packets:149 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:33407 (32.6 KiB)  TX bytes:14576 (14.2 KiB)

gre0      Link encap:UNSPEC  HWaddr 00-00-00-00-FF-00-00-00-00-00-00-00-00-00-00-00  
          NOARP  MTU:1476  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1 
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

gretap0   Link encap:Ethernet  HWaddr 00:00:00:00:00:00  
          BROADCAST MULTICAST  MTU:1462  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

ip6tnl0   Link encap:UNSPEC  HWaddr 00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00  
          NOARP  MTU:1452  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1 
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

lo        Link encap:Local Loopback  
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:1517 errors:0 dropped:0 overruns:0 frame:0
          TX packets:1517 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1 
          RX bytes:106516 (104.0 KiB)  TX bytes:106516 (104.0 KiB)

sit0      Link encap:IPv6-in-IPv4  
          NOARP  MTU:1480  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1 
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

wlan0     Link encap:Ethernet  HWaddr B8:27:EB:55:1B:9F  
          BROADCAST MULTICAST  MTU:1500  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)
```

挺多的，我们一个个分析一下。

br-lan：

这个跟eth0的网卡地址是一样的，从名字上看，这个是一个网桥，是虚拟的。

这是一个典型路由器的框图。

![openwrt（一）-图1](/images/openwrt（一）-图1.png)

看看Makefile的编译过程。



# openwrt基本情况

官网在这里：https://openwrt.org/

从2018年起，lede项目和openwrt项目都统一为openwrt项目。

项目的基本规则是：https://openwrt.org/rules

```
1、没有核心开发团队，没有特权管理者，所以的提交者是平等的。
2、所有提交者都有投票的权利。
3、项目事务都以投票的方式来决定（妥当吗？）
4、连续3个月无法联系到的提交者，会被剥夺投票权利。
5、任何投票都在网上公开。
6、不会在项目范围内提供邮件地址，保护隐私。
```

合并后的openwrt，基于之前的lede的进行开发。

github的地址是：https://github.com/openwrt/openwrt



# luci界面配置

我们的树莓派ip地址配置为192.168.0.100 。我们在pc的浏览器里访问这个界面。

就到了openwrt的登陆界面了。root，密码就是root密码。

我在浏览器里点击打开wifi。串口打印了这些。

```
[64030.749441] brcmfmac: brcmf_cfg80211_dump_station: BRCMF_C_GET_ASSOCLIST unsupported, err=-512
[64210.946444] IPv6: ADDRCONF(NETDEV_UP): wlan0: link is not ready
[64210.955123] device wlan0 entered promiscuous mode
[64211.089334] IPv6: ADDRCONF(NETDEV_CHANGE): wlan0: link becomes ready
[64211.096971] br-lan: port 2(wlan0) entered forwarding state
[64211.103578] br-lan: port 2(wlan0) entered forwarding state
[64213.096013] br-lan: port 2(wlan0) entered forwarding state
```

然后手机就可以搜索到LEDE的热点，默认没有密码，连接上去。

手机可以通过openwrt来上网。

# 看看系统默认的进程

这里面就有很多点值得研究。

```
  PID USER       VSZ STAT COMMAND
    1 root      1344 S    /sbin/procd：看到pid为1了没？这个是openwrt取代init的一个东西。
    2 root         0 SW   [kthreadd]：带中括号的都是内核线程。
    3 root         0 SW   [ksoftirqd/0]
    4 root         0 SW   [kworker/0:0]
    5 root         0 SW<  [kworker/0:0H]
    7 root         0 SW   [rcu_sched]
    8 root         0 SW   [rcu_bh]
    9 root         0 SW   [migration/0]
   10 root         0 SW   [migration/1]
   11 root         0 SW   [ksoftirqd/1]
   13 root         0 SW<  [kworker/1:0H]
   14 root         0 SW   [migration/2]
   15 root         0 SW   [ksoftirqd/2]
   17 root         0 SW<  [kworker/2:0H]
   18 root         0 SW   [migration/3]
   19 root         0 SW   [ksoftirqd/3]
   21 root         0 SW<  [kworker/3:0H]
   22 root         0 SW<  [writeback]
   23 root         0 SW<  [crypto]
   24 root         0 SW<  [bioset]
   25 root         0 SW<  [kblockd]
   26 root         0 SW   [kswapd0]
   28 root         0 SW<  [vmstat]
   29 root         0 SW   [fsnotify_mark]
   34 root         0 SW<  [pencrypt]
中间很多一样的，被我删掉了。
   65 root         0 SW<  [VCHIQ-0]
   66 root         0 SW<  [VCHIQr-0]
   67 root         0 SW<  [VCHIQs-0]
   68 root         0 SW<  [dwc_otg]
   69 root         0 SW   [kworker/3:1]
   70 root         0 SW   [kworker/1:1]
   72 root         0 SW<  [DWC Notificatio]
   73 root         0 SW   [irq/92-mmc1]
   74 root         0 SW<  [ipv6_addrconf]
   76 root         0 SW   [VCHIQka-0]
   77 root         0 SW<  [SMIO]
   78 root         0 SW<  [deferwq]：延迟的工作队列。
   79 root         0 SW   [kworker/1:2]
   80 root         0 SW   [kworker/3:2]
   81 root         0 SW   [scsi_eh_0]
   82 root         0 SW<  [scsi_tmf_0]
   83 root         0 SW   [usb-storage]
   84 root         0 SW<  [bioset]
   86 root         0 SW<  [kworker/2:1H]
   87 root         0 SW<  [kworker/0:1H]
   88 root         0 SW<  [ext4-rsv-conver]
   90 root         0 SW<  [kworker/1:1H]
   94 root         0 SW<  [kworker/3:1H]
  277 root       960 S    /sbin/ubusd：这个值得注意。
  321 root      1040 S    /bin/ash --login：login的调用非常晚啊。
  322 root       668 S    /sbin/askfirst /usr/libexec/login.sh：注意这里。
  472 root         0 SW   [spi0]
  474 root         0 SW<  [cfg80211]
  475 root         0 SW<  [brcmf_wq/mmc1:0]
  476 root         0 SW   [kworker/2:2]
  477 root         0 SW   [brcmf_wdog/mmc1]
  575 root      1040 S    /sbin/logd -S 64
  584 root      1236 S    /sbin/rpcd
  663 root      1444 S    /sbin/netifd
  698 root      1208 S    /usr/sbin/odhcpd
  801 nobody     748 S    /usr/sbin/atd -f
  842 nobody    1496 S    /usr/sbin/dnscrypt-proxy /var/etc/dnscrypt-proxy-ns1
  870 root       808 S    /usr/sbin/dropbear -F -P /var/run/dropbear.1.pid -p
  929 root      1348 S    /usr/sbin/uhttpd -f -h /www -r LEDE -x /cgi-bin -u /
  943 nobody    1408 S    /usr/sbin/mdnsd -debug
  995 root      2572 S    /usr/sbin/smbd -F
  996 root      2632 S    /usr/sbin/nmbd -F
 1007 root      4420 S <  /usr/libexec/softethervpn/vpnbridge execsvc
 1008 root     17508 S <  /usr/libexec/softethervpn/vpnbridge execsvc
 1027 root      4420 S <  /usr/libexec/softethervpn/vpnclient execsvc
 1028 root     14200 S <  /usr/libexec/softethervpn/vpnclient execsvc
 1085 dnsmasq   2204 S    /usr/sbin/dnsmasq -C /var/etc/dnsmasq.conf.cfg02411c
 1088 root      4420 S <  /usr/libexec/softethervpn/vpnserver execsvc
 1089 root     20812 S <  /usr/libexec/softethervpn/vpnserver execsvc
 1101 root       760 S    xl2tpd -D -l -p /var/run/xl2tpd.pid
 1168 root      3704 S    /usr/sbin/collectd -f
 1249 root      1264 S    /usr/sbin/hnetd -d /etc/init.d/dnsmasq -f /tmp/dnsma
 1275 root      1120 S    /usr/bin/redsocks2 -c /var/etc/redsocks2.conf
 7896 root         0 SW   [kworker/u8:0]
11012 root         0 SW   [kworker/2:0]
11013 root      1964 S    /usr/sbin/hostapd -s -P /var/run/wifi-phy0.pid -B /v
11027 root         0 SW   [kworker/0:2]
14740 root         0 SW   [kworker/u8:2]
14744 root      1032 R    ps
26731 root         0 SW   [kworker/u8:3]
29230 root         0 SW   [kworker/u8:1]
30268 root      1036 S    {watchcat.sh} /bin/sh /usr/bin/watchcat.sh period 21
30276 root      1032 S    sleep 1080
30305 root      1032 S    /usr/sbin/ntpd -n -N -l -S /usr/sbin/ntpd-hotplug -p
30392 root       724 S    /usr/sbin/vnstatd -d
```

1、procd。

```
从pid可以看出，这个就是init进程。procd是process daemon的缩写。进程管理用的。
它肯定是改进了普通的init进程。
它做了什么特别的事情？
它会跟踪通过init脚本启动的进程。
procd取代了这些东西：
1、hotplug。procd把热插拔的活也干了。
2、busybox的klogd和syslogd。把日志的活也干了。
3、busybox的watchdog。把看门狗的活也干了。
为什么需要procd？
为了让系统更加健壮。
```

我觉得需要看一下，内核改了一些什么。

openwrt的改动应该是在编译的过程中合入的，所以需要看看编译过程。



# 配置软件源

一般linux系统的软件源，国外的下载都太慢。

openwrt也是一样，需要修改为国内的源。

对应的配置文件是/etc/opkg/distfeeds.conf文件。先把之前的备份一份。

我从官网找到这个，电脑访问这个网站感觉还挺快的。

```
src/gz reboot_core https://downloads.openwrt.org/releases/17.01.4/targets/brcm2708/bcm2710/packages/
src/gz reboot_base https://downloads.openwrt.org/releases/17.01.4/packages/arm_cortex-a53_neon-vfpv4/base
src/gz reboot_luci https://downloads.openwrt.org/releases/17.01.4/packages/arm_cortex-a53_neon-vfpv4/luci
src/gz reboot_packages https://downloads.openwrt.org/releases/17.01.4/packages/arm_cortex-a53_neon-vfpv4/packages
src/gz reboot_routing https://downloads.openwrt.org/releases/17.01.4/packages/arm_cortex-a53_neon-vfpv4/routing
src/gz reboot_telephony https://downloads.openwrt.org/releases/17.01.4/packages/arm_cortex-a53_neon-vfpv4/telephony
```

但是写到文件，opkg update提示下载失败。

我在openwrt上访问百度也不行，我的手机现在是连接在openwrt上，手机都可以上网。

为什么openwrt本身反而不能上网呢？

可以ping通`114.114.114.114`。说明网络是通的。只是openwrt的dns有问题。

浏览器进入到管理界面。

网络，接口，修改，把dns改成114.114.114.114。点击保存应用。

然后再执行opkg update就好了。



# 用winscp连接

一开始是不行的。因为没有安装启动对应的服务。

```
opkg update
opkg install vsftpd openssh-sftp-server
```

这样就可以了。



# 参考资料

1、编译OpenWrt烧录树莓派3B

http://tobefun.cn/2017/07/18/编译OpenWrt烧录树莓派3B/

2、

https://wiki.openwrt.org/doc/networking/network.interfaces

3、br-lan、eth0、eth1及lo

https://blog.csdn.net/u013485792/article/details/50943069

4、交换机手册(Switch Documentation)

https://wiki.openwrt.org/zh-cn/doc/uci/network/switch

5、What is procd?

https://wiki.openwrt.org/doc/techref/procd

6、Openwrt上开启sftp,使用SecureCRT,WinSCp等传输文件

https://www.cnblogs.com/Motorola/p/7469962.html