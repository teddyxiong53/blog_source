---
title: 树莓派3上安装Android things
date: 2017-07-12 00:06:09
tags:

	- 树莓派
	- Android Things

---

# 1. 下载镜像

地址上：https://developer.android.com/things/preview/download.html。选择树莓派3的下载。

# 2. 烧录镜像

跟树莓派上安装其他的系统一样。使用win32 disk imager，将镜像文件烧录到SD卡里。然后把SD卡插入到树莓派上就好了。

# 3. 启动

因为我当前买的hdmi线还没有到，我连接串口看输出。启动过程的打印如下。我们分析一下。

1、采用了uboot来引导。

2、输出是指向了lcd。

3、Linux内核版本是4.4。

4、在7.8秒附近时，启动了一些谷歌的服务。



```


U-Boot 2017.01-g2ce116e560 (Jun 14 2017 - 03:23:10 +0000)

DRAM:  944 MiB
RPI 3 Model B (0xa22082)
MMC:   bcm2835_sdhci: 0
reading uboot.env
In:    serial
Out:   lcd
Err:   lcd
Net:   Net Initialization Skipped
No ethernet found.
ANDROID: Booting slot: a
ANDROID: reboot reason: "(none)"
Booting kernel at 0x1000000 with fdt at 2fffbc00...


## Booting Android Image at 0x01000000 ...
Kernel load addr 0x01000800 size 6963 KiB
RAM disk load addr 0x11000000 size 3580 KiB
## Flattened Device Tree blob at 2fffbc00
   Booting using the fdt blob at 0x2fffbc00
   XIP Kernel Image ... OK
   Loading Ramdisk to 3a7b7000, end 3ab35f82 ... OK
   Loading Device Tree to 2dff8000, end 2dfff38f ... OK

Starting kernel ...

[    0.000000] Booting Linux on physical CPU 0x0
[    0.000000] Initializing cgroup subsys cpuset
[    0.000000] Initializing cgroup subsys cpu
[    0.000000] Initializing cgroup subsys cpuacct
[    0.000000] Linux version 4.4.19-v7+ (android-build@wphn5.hot.corp.google.com) (gcc version 4.9 20150123 (prerelease) (GCC) ) #1 SMP PREEMPT Wed Jun 14 03:33:55 UTC 2017
[    0.000000] CPU: ARMv7 Processor [410fd034] revision 4 (ARMv7), cr=10c5383d
[    0.000000] CPU: PIPT / VIPT nonaliasing data cache, VIPT aliasing instruction cache
[    0.000000] Machine model: Raspberry Pi 3 Model B Rev 1.2
[    0.000000] Truncating RAM at 0x00000000-0x3b000000 to -0x30000000
[    0.000000] Consider using a HIGHMEM enabled kernel.
[    0.000000] INITRD: 0x3a7b7000+0x0037ef82 is not a memory region - disabling initrd
[    0.000000] cma: Reserved 8 MiB at 0x2f800000
[    0.000000] Memory policy: Data cache writealloc
[    0.000000] [bcm2709_smp_init_cpus] enter (1015a0->f3003010)
[    0.000000] [bcm2709_smp_init_cpus] ncores=4
[    0.000000] PERCPU: Embedded 11 pages/cpu @ef0f5000 s23232 r0 d21824 u45056
[    0.000000] Built 1 zonelists in Zone order, mobility grouping on.  Total pages: 194880
[    0.000000] Kernel command line: 8250.nr_uarts=1 dma.dmachans=0x7f35 bcm2708_fb.fbwidth=656 bcm2708_fb.fbheight=416 bcm2709.boardrev=0xa22082 bcm2709.serial=0x5e004eca smsc95xx.macaddr=B8:27:EB:00:4E:CA bcm2708_fb.fbdepth=16 bcm2708_fb.fbswap=1 bcm2709.uart_clock=48000000 vc_mem.mem_base=0x3dc00000 vc_mem.mem_size=0x3f000000  dwc_otg.lpm_enable=0 console=ttyS0,115200 ro rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait earlyprintk init=/init androidboot.hardware=rpi3 androidboot.selinux=permissive androidboot.serialno=000000005e004eca androidboot.slot_suffix=_a root="/dev/mmcblk0p6" skip_initramfs 
[    0.000000] PID hash table entries: 4096 (order: 2, 16384 bytes)
[    0.000000] Dentry cache hash table entries: 131072 (order: 7, 524288 bytes)
[    0.000000] Inode-cache hash table entries: 65536 (order: 6, 262144 bytes)
[    0.000000] Memory: 752232K/786432K available (12012K kernel code, 702K rwdata, 2796K rodata, 1024K init, 880K bss, 26008K reserved, 8192K cma-reserved)
[    0.000000] Virtual kernel memory layout:
[    0.000000]     vector  : 0xffff0000 - 0xffff1000   (   4 kB)
[    0.000000]     fixmap  : 0xffc00000 - 0xfff00000   (3072 kB)
[    0.000000]     vmalloc : 0xf0800000 - 0xff800000   ( 240 MB)
[    0.000000]     lowmem  : 0xc0000000 - 0xf0000000   ( 768 MB)
[    0.000000]       .text : 0xc0008000 - 0xc0f7636c   (15801 kB)
[    0.000000]       .init : 0xc1000000 - 0xc1100000   (1024 kB)
[    0.000000]       .data : 0xc1100000 - 0xc11af8f4   ( 703 kB)
[    0.000000]        .bss : 0xc11b2000 - 0xc128e30c   ( 881 kB)
[    0.000000] SLUB: HWalign=64, Order=0-3, MinObjects=0, CPUs=4, Nodes=1
[    0.000000] Preemptible hierarchical RCU implementation.
[    0.000000]  Build-time adjustment of leaf fanout to 32.
[    0.000000] NR_IRQS:16 nr_irqs:16 16
[    0.000000] Architected cp15 timer(s) running at 19.20MHz (phys).
[    0.000000] clocksource: arch_sys_counter: mask: 0xffffffffffffff max_cycles: 0x46d987e47, max_idle_ns: 440795202767 ns
[    0.000009] sched_clock: 56 bits at 19MHz, resolution 52ns, wraps every 4398046511078ns
[    0.000029] Switching to timer-based delay loop, resolution 52ns
[    0.000199] Calibrating delay loop (skipped), value calculated using timer frequency.. 38.40 BogoMIPS (lpj=192000)
[    0.000227] pid_max: default: 32768 minimum: 301
[    0.000339] Security Framework initialized
[    0.000358] SELinux:  Initializing.
[    0.000665] Mount-cache hash table entries: 2048 (order: 1, 8192 bytes)
[    0.000685] Mountpoint-cache hash table entries: 2048 (order: 1, 8192 bytes)
[    0.001825] Disabling cpuset control group subsystem
[    0.001864] Initializing cgroup subsys io
[    0.001897] Initializing cgroup subsys memory
[    0.001946] Initializing cgroup subsys devices
[    0.001971] Initializing cgroup subsys freezer
[    0.001997] Initializing cgroup subsys debug
[    0.002065] CPU: Testing write buffer coherency: ok
[    0.002139] ftrace: allocating 32332 entries in 95 pages
[    0.088087] CPU0: update cpu_capacity 1024
[    0.088127] CPU0: thread -1, cpu 0, socket 0, mpidr 80000000
[    0.088143] [bcm2709_smp_prepare_cpus] enter
[    0.088262] Setting up static identity map for 0x100000 - 0x100034
[    0.167512] [bcm2709_boot_secondary] cpu:1 started (0) 18
[    0.167703] [bcm2709_secondary_init] enter cpu:1
[    0.167742] CPU1: update cpu_capacity 1024
[    0.167750] CPU1: thread -1, cpu 1, socket 0, mpidr 80000001
[    0.197559] [bcm2709_boot_secondary] cpu:2 started (0) 16
[    0.197704] [bcm2709_secondary_init] enter cpu:2
[    0.197727] CPU2: update cpu_capacity 1024
[    0.197734] CPU2: thread -1, cpu 2, socket 0, mpidr 80000002
[    0.227620] [bcm2709_boot_secondary] cpu:3 started (0) 15
[    0.227753] [bcm2709_secondary_init] enter cpu:3
[    0.227775] CPU3: update cpu_capacity 1024
[    0.227783] CPU3: thread -1, cpu 3, socket 0, mpidr 80000003
[    0.227858] Brought up 4 CPUs
[    0.227885] SMP: Total of 4 processors activated (153.60 BogoMIPS).
[    0.227896] CPU: All CPU(s) started in HYP mode.
[    0.227906] CPU: Virtualization extensions available.
[    0.228947] devtmpfs: initialized
[    0.245912] VFP support v0.3: implementor 41 architecture 3 part 40 variant 3 rev 4
[    0.246325] clocksource: jiffies: mask: 0xffffffff max_cycles: 0xffffffff, max_idle_ns: 19112604462750000 ns
[    0.247092] pinctrl core: initialized pinctrl subsystem
[    0.247777] NET: Registered protocol family 16
[    0.253950] DMA: preallocated 4096 KiB pool for atomic coherent allocations
[    0.265024] bcm2709: Mini UART enabled
[    0.265072] hw-breakpoint: found 5 (+1 reserved) breakpoint and 4 watchpoint registers.
[    0.265085] hw-breakpoint: maximum watchpoint size is 8 bytes.
[    0.265255] Serial: AMBA PL011 UART driver
[    0.265437] uart-pl011 3f201000.uart: could not find pctldev for node /soc/gpio@7e200000/uart0_pins, deferring probe
[    0.265641] bcm2835-mbox 3f00b880.mailbox: mailbox enabled
[    0.371273] bcm2835-dma 3f007000.dma: DMA legacy API manager at f3007000, dmachans=0x1
[    0.372029] SCSI subsystem initialized
[    0.372412] usbcore: registered new interface driver usbfs
[    0.372495] usbcore: registered new interface driver hub
[    0.372620] usbcore: registered new device driver usb
[    0.372839] media: Linux media interface: v0.10
[    0.372929] Linux video capture interface: v2.00
[    0.377951] raspberrypi-firmware soc:firmware: Attached to firmware from 2016-09-14 20:00
[    0.388127] Advanced Linux Sound Architecture Driver Initialized.
[    0.389216] Bluetooth: Core ver 2.21
[    0.389270] NET: Registered protocol family 31
[    0.389282] Bluetooth: HCI device and connection manager initialized
[    0.389306] Bluetooth: HCI socket layer initialized
[    0.389326] Bluetooth: L2CAP socket layer initialized
[    0.389383] Bluetooth: SCO socket layer initialized
[    0.391954] clocksource: Switched to clocksource arch_sys_counter
[    0.486952] FS-Cache: Loaded
[    0.487281] CacheFiles: Loaded
[    0.489263] NET: Registered protocol family 2
[    0.490100] TCP established hash table entries: 8192 (order: 3, 32768 bytes)
[    0.490218] TCP bind hash table entries: 8192 (order: 4, 65536 bytes)
[    0.490410] TCP: Hash tables configured (established 8192 bind 8192)
[    0.490512] UDP hash table entries: 512 (order: 2, 16384 bytes)
[    0.490562] UDP-Lite hash table entries: 512 (order: 2, 16384 bytes)
[    0.490847] NET: Registered protocol family 1
[    0.491298] RPC: Registered named UNIX socket transport module.
[    0.491311] RPC: Registered udp transport module.
[    0.491323] RPC: Registered tcp transport module.
[    0.491334] RPC: Registered tcp NFSv4.1 backchannel transport module.
[    0.493338] hw perfevents: enabled with armv7_cortex_a7 PMU driver, 7 counters available
[    0.495082] futex hash table entries: 1024 (order: 4, 65536 bytes)
[    0.495207] audit: initializing netlink subsys (disabled)
[    0.495264] audit: type=2000 audit(0.449:1): initialized
[    0.512626] VFS: Disk quotas dquot_6.6.0
[    0.513000] VFS: Dquot-cache hash table entries: 1024 (order 0, 4096 bytes)
[    0.515916] FS-Cache: Netfs 'nfs' registered for caching
[    0.517040] NFS: Registering the id_resolver key type
[    0.517099] Key type id_resolver registered
[    0.517111] Key type id_legacy registered
[    0.517460] fuse init (API version 7.23)
[    0.525439] Block layer SCSI generic (bsg) driver version 0.4 loaded (major 252)
[    0.525606] io scheduler noop registered
[    0.525629] io scheduler deadline registered (default)
[    0.525691] io scheduler cfq registered
[    0.527694] clk: couldn't get clock 0 for /soc/pwm@7e20c000
[    0.529281] BCM2708FB: allocated DMA memory efc00000
[    0.529313] BCM2708FB: allocated DMA channel 0 @ f3007000
[    0.532083] Serial: 8250/16550 driver, 1 ports, IRQ sharing disabled
[    0.533269] console [ttyS0] disabled
[    0.533334] 3f215040.uart: ttyS0 at MMIO 0x3f215040 (irq = 59, base_baud = 31250000) is a 16550
[    1.354221] console [ttyS0] enabled
[    2.297539] bcm2835-rng 3f104000.rng: hwrng registered
[    2.302903] vc-cma: Videocore CMA driver
[    2.306882] vc-cma: vc_cma_base      = 0x00000000
[    2.311655] vc-cma: vc_cma_size      = 0x00000000 (0 MiB)
[    2.317156] vc-cma: vc_cma_initial   = 0x00000000 (0 MiB)
[    2.322947] vc-mem: phys_addr:0x00000000 mem_base=0x3dc00000 mem_size:0x3f000000(1008 MiB)
[    2.332314] gpiomem-bcm2835 3f200000.gpiomem: Initialised: Registers at 0x3f200000
[    2.358777] brd: module loaded
[    2.372812] loop: module loaded
[    2.377247] vchiq: vchiq_init_state: slot_zero = 0xefc80000, is_master = 0
[    2.385807] Loading iSCSI transport class v2.0-870.
[    2.393926] tun: Universal TUN/TAP device driver, 1.6
[    2.399054] tun: (C) 1999-2004 Max Krasnyansky <maxk@qualcomm.com>
[    2.405635] PPP generic driver version 2.4.2
[    2.410223] PPP BSD Compression module registered
[    2.415029] PPP Deflate Compression module registered
[    2.420175] PPP MPPE Compression module registered
[    2.425068] NET: Registered protocol family 24
[    2.429870] usbcore: registered new interface driver brcmfmac
[    2.435871] usbcore: registered new interface driver asix
[    2.441435] usbcore: registered new interface driver ax88179_178a
[    2.447722] usbcore: registered new interface driver cdc_ether
[    2.453746] usbcore: registered new interface driver smsc95xx
[    2.459656] usbcore: registered new interface driver net1080
[    2.465493] usbcore: registered new interface driver cdc_subset
[    2.471570] usbcore: registered new interface driver zaurus
[    2.477347] usbcore: registered new interface driver cdc_ncm
[    2.483122] ehci_hcd: USB 2.0 'Enhanced' Host Controller (EHCI) Driver
[    2.489756] dwc_otg: version 3.00a 10-AUG-2012 (platform bus)
[    2.705942] Core Release: 2.80a
[    2.709134] Setting default values for core params
[    2.714042] Finished setting default values for core params
[    2.920084] Using Buffer DMA mode
[    2.923467] Periodic Transfer Interrupt Enhancement - disabled
[    2.929384] Multiprocessor Interrupt Enhancement - disabled
[    2.935056] OTG VER PARAM: 0, OTG VER FLAG: 0
[    2.939479] Dedicated Tx FIFOs mode
[    2.943387] WARN::dwc_otg_hcd_init:1047: FIQ DMA bounce buffers: virt = 0xefc14000 dma = 0xefc14000 len=9024
[    2.953403] FIQ FSM acceleration enabled for :
[    2.953403] Non-periodic Split Transactions
[    2.953403] Periodic Split Transactions
[    2.953403] High-Speed Isochronous Endpoints
[    2.953403] Interrupt/Control Split Transaction hack enabled
[    2.976163] WARN::hcd_init_fiq:413: FIQ on core 1 at 0xc05f50c4
[    2.982176] WARN::hcd_init_fiq:414: FIQ ASM at 0xc05f5434 length 36
[    2.988543] WARN::hcd_init_fiq:439: MPHI regs_base at 0xf0924000
[    2.994701] dwc_otg 3f980000.usb: DWC OTG Controller
[    2.999768] dwc_otg 3f980000.usb: new USB bus registered, assigned bus number 1
[    3.007236] dwc_otg 3f980000.usb: irq 62, io mem 0x00000000
[    3.012951] Init: Port Power? op_state=1
[    3.016931] Init: Power Port (0)
[    3.020476] usb usb1: New USB device found, idVendor=1d6b, idProduct=0002
[    3.027394] usb usb1: New USB device strings: Mfr=3, Product=2, SerialNumber=1
[    3.034748] usb usb1: Product: DWC OTG Controller
[    3.039523] usb usb1: Manufacturer: Linux 4.4.19-v7+ dwc_otg_hcd
[    3.045636] usb usb1: SerialNumber: 3f980000.usb
[    3.051244] hub 1-0:1.0: USB hub found
[    3.055116] hub 1-0:1.0: 1 port detected
[    3.060151] usbcore: registered new interface driver cdc_acm
[    3.065924] cdc_acm: USB Abstract Control Model driver for USB modems and ISDN adapters
[    3.074196] usbcore: registered new interface driver usb-storage
[    3.080439] usbcore: registered new interface driver usbserial
[    3.086447] usbcore: registered new interface driver usbserial_generic
[    3.093154] usbserial: USB Serial support registered for generic
[    3.099313] usbcore: registered new interface driver ftdi_sio
[    3.105224] usbserial: USB Serial support registered for FTDI USB Serial Device
[    3.113304] mousedev: PS/2 mouse device common for all mice
[    3.119048] usbcore: registered new interface driver xpad
[    3.124630] usbcore: registered new interface driver usb_acecad
[    3.130715] usbcore: registered new interface driver aiptek
[    3.136472] usbcore: registered new interface driver gtco
[    3.142047] usbcore: registered new interface driver hanwang
[    3.147865] usbcore: registered new interface driver kbtab
[    3.154456] i2c /dev entries driver
[    3.158724] bcm2708_i2c 3f804000.i2c: BSC1 Controller at 0x3f804000 (irq 83) (baudrate 100000)
[    3.169577] IR NEC protocol handler initialized
[    3.174207] IR RC5(x/sz) protocol handler initialized
[    3.179341] IR RC6 protocol handler initialized
[    3.183965] IR JVC protocol handler initialized
[    3.188568] IR Sony protocol handler initialized
[    3.193280] IR SANYO protocol handler initialized
[    3.198058] IR Sharp protocol handler initialized
[    3.202858] IR MCE Keyboard/mouse protocol handler initialized
[    3.208782] IR XMP protocol handler initialized
[    3.231075] gspca_main: v2.14.0 registered
[    3.236483] device-mapper: uevent: version 1.0.3
[    3.241767] device-mapper: ioctl: 4.34.0-ioctl (2015-10-28) initialised: dm-devel@redhat.com
[    3.252079] Indeed it is in host mode hprt0 = 00021501
[    3.260538] Bluetooth: HCI UART driver ver 2.3
[    3.265076] Bluetooth: HCI UART protocol H4 registered
[    3.270292] Bluetooth: HCI UART protocol Three-wire (H5) registered
[    3.282093] Bluetooth: HCI UART protocol BCM registered
[    3.287584] bcm2835-cpufreq: min=600000 max=1200000
[    3.292914] sdhci: Secure Digital Host Controller Interface driver
[    3.299185] sdhci: Copyright(c) Pierre Ossman
[    3.304037] sdhost: log_buf @ efc13000 (efc13000)
[    3.381993] mmc0: sdhost-bcm2835 loaded - DMA enabled (>1)
[    3.389920] mmc-bcm2835 3f300000.mmc: mmc_debug:0 mmc_debug2:0
[    3.395873] mmc-bcm2835 3f300000.mmc: DMA channel allocated
[    3.439598] mmc0: host does not support reading read-only switch, assuming write-enable
[    3.442101] sdhci-pltfm: SDHCI platform and OF driver helper
[    3.442613] hidraw: raw HID events driver (C) Jiri Kosina
[    3.447405] usbcore: registered new interface driver usbhid
[    3.447409] usbhid: USB HID core driver
[    3.447827] ashmem: initialized
[    3.450837] usbcore: registered new interface driver snd-usb-audio
[    3.451878] u32 classifier
[    3.451882]     Actions configured
[    3.451903] Netfilter messages via NETLINK v0.30.
[    3.452071] nf_conntrack version 0.5.0 (11881 buckets, 47524 max)
[    3.453100] ctnetlink v0.93: registering with nfnetlink.
[    3.454130] xt_time: kernel timezone is -0000
[    3.454735] ip_tables: (C) 2000-2006 Netfilter Core Team
[    3.455077] arp_tables: (C) 2002 David S. Miller
[    3.455195] Initializing XFRM netlink socket
[    3.456873] NET: Registered protocol family 10
[    3.458410] mip6: Mobile IPv6
[    3.458449] ip6_tables: (C) 2000-2006 Netfilter Core Team
[    3.458711] sit: IPv6 over IPv4 tunneling driver
[    3.459763] NET: Registered protocol family 17
[    3.459799] NET: Registered protocol family 15
[    3.459939] Key type dns_resolver registered
[    3.461442] Registering SWP/SWPB emulation handler
[    3.462024] usb 1-1: new high-speed USB device number 2 using dwc_otg
[    3.462530] registered taskstats version 1
[    3.462726] vc-sm: Videocore shared memory driver
[    3.462737] [vc_sm_connected_init]: start
[    3.465215] [vc_sm_connected_init]: end - returning 0
[    3.466705] 3f201000.uart: ttyAMA0 at MMIO 0x3f201000 (irq = 87, base_baud = 0) is a PL011 rev2
[    3.467655] otg_wakelock_init: No USB transceiver found
[    3.467670] of_cfs_init
[    3.467713] of_cfs_init: OK
[    3.468756] Indeed it is in host mode hprt0 = 00001101
[    3.476802] ALSA device list:
[    3.476808]   #0: bcm2835 ALSA
[    3.611551] Waiting for root device /dev/mmcblk0p6...
[    3.613084] mmc0: Problem switching card into high-speed mode!
[    3.613265] mmc0: new SDHC card at address 0001
[    3.624168] mmcblk0: mmc0:0001 SD16G 14.6 GiB
[    3.644090] GPT:Primary header thinks Alt. header is not at the end of the disk.
[    3.651603] GPT:8912895 != 30547967
[    3.655199] GPT:Alternate GPT header not at the end of the disk.
[    3.661297] GPT:8912895 != 30547967
[    3.662311] usb 1-1: New USB device found, idVendor=0424, idProduct=9514
[    3.662322] usb 1-1: New USB device strings: Mfr=0, Product=0, SerialNumber=0
[    3.663280] hub 1-1:1.0: USB hub found
[    3.663393] hub 1-1:1.0: 5 ports detected
[    3.686801] GPT: Use GNU Parted to correct GPT errors.
[    3.692143]  mmcblk0: p1 p2 p3 p4 p5 p6 p7 p8 p9 p10 p11 p12 p13 p14 p15
[    3.720932] mmc1: queuing unknown CIS tuple 0x80 (2 bytes)
[    3.728142] mmc1: queuing unknown CIS tuple 0x80 (3 bytes)
[    3.735364] mmc1: queuing unknown CIS tuple 0x80 (3 bytes)
[    3.743796] mmc1: queuing unknown CIS tuple 0x80 (7 bytes)
[    3.752140] EXT4-fs (mmcblk0p6): mounted filesystem with ordered data mode. Opts: (null)
[    3.760399] VFS: Mounted root (ext4 filesystem) readonly on device 179:6.
[    3.768835] devtmpfs: mounted
[    3.773875] Freeing unused kernel memory: 1024K (c1000000 - c1100000)
[    3.843799] mmc1: new high speed SDIO card at address 0001
[    3.855822] init: init first stage started!
[    3.942006] usb 1-1.1: new high-speed USB device number 3 using dwc_otg
[    3.951766] brcmfmac: brcmf_c_preinit_dcmds: Firmware version = wl0: Dec 15 2015 18:10:45 version 7.45.41.23 (r606571) FWID 01-cc4eda9c
[    3.983779] audit: type=1403 audit(3.939:2): policy loaded auid=4294967295 ses=4294967295
[    3.986666] brcmfmac: brcmf_cfg80211_reg_notifier: not a ISO3166 code
[    3.999763] init: (Initializing SELinux non-enforcing took 0.14s.)
[    4.020581] init: init second stage started!
[    4.038780] init: Running restorecon...
[    4.062349] usb 1-1.1: New USB device found, idVendor=0424, idProduct=ec00
[    4.069341] usb 1-1.1: New USB device strings: Mfr=0, Product=0, SerialNumber=0
[    4.077352] audit: type=1400 audit(4.029:3): avc:  denied  { write } for  pid=23 comm="kdevtmpfs" name="001" dev="devtmpfs" ino=1083 scontext=u:r:kernel:s0 tcontext=u:object_r:device:s0 tclass=dir permissive=1
[    4.096331] audit: type=1400 audit(4.049:4): avc:  denied  { mknod } for  pid=23 comm="kdevtmpfs" capability=27  scontext=u:r:kernel:s0 tcontext=u:r:kernel:s0 tclass=capability permissive=1
[    4.103509] init: waitpid failed: No child processes
[    4.105521] init: (Loading properties from /default.prop took 0.00s.)
[    4.115405] init: (Parsing /init.environ.rc took 0.00s.)
[    4.125165] init: (Parsing /init.usb.rc took 0.01s.)
[    4.126394] init: (Parsing /init.rpi3.rc took 0.00s.)
[    4.130286] init: (Parsing /init.usb.configfs.rc took 0.00s.)
[    4.131502] init: (Parsing /init.zygote32.rc took 0.00s.)
[    4.131537] init: (Parsing /init.rc took 0.03s.)
[    4.133755] init: Starting service 'ueventd'...
[    4.134606] init: Waiting for /dev/.coldboot_done...
[    4.138828] ueventd: ueventd started!
[    4.170144] audit: type=1400 audit(4.119:5): avc:  denied  { add_name } for  pid=23 comm="kdevtmpfs" name="003" scontext=u:r:kernel:s0 tcontext=u:object_r:device:s0 tclass=dir permissive=1
[    4.187304] audit: type=1400 audit(4.139:6): avc:  denied  { create } for  pid=23 comm="kdevtmpfs" name="003" scontext=u:r:kernel:s0 tcontext=u:object_r:device:s0 tclass=chr_file permissive=1
[    4.204733] audit: type=1400 audit(4.159:7): avc:  denied  { setattr } for  pid=23 comm="kdevtmpfs" name="003" dev="devtmpfs" ino=1706 scontext=u:r:kernel:s0 tcontext=u:object_r:device:s0 tclass=chr_file permissive=1
[    4.226942] smsc95xx v1.0.4
[    4.296606] smsc95xx 1-1.1:1.0 eth0: register 'smsc95xx' at usb-3f980000.usb-1.1, smsc95xx USB 2.0 Ethernet, b8:27:eb:00:4e:ca
[    4.388329] audit: type=1400 audit(4.339:8): avc:  denied  { relabelfrom } for  pid=116 comm="ueventd" name="003" dev="tmpfs" ino=8232 scontext=u:r:ueventd:s0 tcontext=u:object_r:usb_device:s0 tclass=chr_file permissive=1
[    4.408416] audit: type=1400 audit(4.359:9): avc:  denied  { relabelto } for  pid=116 comm="ueventd" name="003" dev="tmpfs" ino=8232 scontext=u:r:ueventd:s0 tcontext=u:object_r:usb_device:s0 tclass=chr_file permissive=1
[    4.449135] ueventd: Coldboot took 0.29s.
[    4.458157] init: Waiting for /dev/.coldboot_done took 0.32s.
[    4.478606] audit: type=1400 audit(4.429:10): avc:  denied  { create } for  pid=1 comm="init" name="sdcard" scontext=u:r:init:s0 tcontext=u:object_r:tmpfs:s0 tclass=lnk_file permissive=1
[    4.497973] init: write_file: Unable to open '/proc/sys/kernel/sched_compat_yield': No such file or directory
[    4.510833] init: write_file: Unable to write to '/dev/cpuctl/cpu.shares': Invalid argument
[    4.525646] init: write_file: Unable to open '/proc/sys/abi/swp': No such file or directory
[    4.545072] EXT4-fs (mmcblk0p15): Ignoring removed nomblk_io_submit option
[    5.075466] EXT4-fs (mmcblk0p15): recovery complete
[    5.082418] EXT4-fs (mmcblk0p15): mounted filesystem with ordered data mode. Opts: errors=remount-ro,nomblk_io_submit
[    5.093395] fs_mgr: check_fs(): mount(/dev/block/platform/soc/3f202000.sdhost/by-name/userdata,/data,ext4)=0: Success
[    5.141108] fs_mgr: check_fs(): unmount(/data) succeeded
[    5.150202] fs_mgr: Running /system/bin/e2fsck on /dev/block/platform/soc/3f202000.sdhost/by-name/userdata
[    5.210327] random: e2fsck: uninitialized urandom read (40 bytes read, 83 bits of entropy available)
[    6.210232] e2fsck: e2fsck 1.42.9 (28-Dec-2013)
[    6.210232] 
[    6.216439] e2fsck: Pass 1: Checking inodes, blocks, and sizes
[    6.216439] 
[    6.223904] e2fsck: Pass 2: Checking directory structure
[    6.223904] 
[    6.230809] e2fsck: Pass 3: Checking directory connectivity
[    6.230809] 
[    6.238000] e2fsck: Pass 4: Checking reference counts
[    6.238000] 
[    6.244666] e2fsck: Pass 5: Checking group summary information
[    6.244666] 
[    6.252193] e2fsck: /dev/block/platform/soc/3f202000.sdhost/by-name/userdata: 1249/168000 files (6.0% non-contiguous), 37238/670934 blocks
[    6.252193] 
[    6.268360] EXT4-fs (mmcblk0p15): Ignoring removed nomblk_io_submit option
[    6.282617] EXT4-fs (mmcblk0p15): mounted filesystem with ordered data mode. Opts: nomblk_io_submit,errors=panic
[    6.293096] fs_mgr: __mount(source=/dev/block/platform/soc/3f202000.sdhost/by-name/userdata,target=/data,type=ext4)=0
[    6.323399] EXT4-fs (mmcblk0p11): mounted filesystem with ordered data mode. Opts: (null)
[    6.331795] fs_mgr: __mount(source=/dev/block/platform/soc/3f202000.sdhost/by-name/oem_a,target=/oem,type=ext4)=0
[    6.362033] EXT4-fs (mmcblk0p13): mounted filesystem with ordered data mode. Opts: (null)
[    6.370423] fs_mgr: __mount(source=/dev/block/platform/soc/3f202000.sdhost/by-name/gapps_a,target=/gapps,type=ext4)=0
[    6.386614] init: (Parsing /system/etc/init/atrace.rc took 0.00s.)
[    6.394154] init: (Parsing /system/etc/init/audioserver.rc took 0.00s.)
[    6.402022] init: (Parsing /system/etc/init/bootanim.rc took 0.00s.)
[    6.409946] init: (Parsing /system/etc/init/bootstat.rc took 0.00s.)
[    6.417850] init: (Parsing /system/etc/init/cameraserver.rc took 0.00s.)
[    6.426121] init: (Parsing /system/etc/init/crash_reporter.rc took 0.00s.)
[    6.434232] init: (Parsing /system/etc/init/debuggerd.rc took 0.00s.)
[    6.442107] init: (Parsing /system/etc/init/drmserver.rc took 0.00s.)
[    6.450132] init: (Parsing /system/etc/init/dumpstate.rc took 0.00s.)
[    6.457794] init: (Parsing /system/etc/init/gatekeeperd.rc took 0.00s.)
[    6.465710] init: (Parsing /system/etc/init/init-debug.rc took 0.00s.)
[    6.473639] init: (Parsing /system/etc/init/inputdriverserv.rc took 0.00s.)
[    6.482004] init: (Parsing /system/etc/init/installd.rc took 0.00s.)
[    6.489586] init: (Parsing /system/etc/init/keystore.rc took 0.00s.)
[    6.497205] init: (Parsing /system/etc/init/lmkd.rc took 0.00s.)
[    6.504718] init: (Parsing /system/etc/init/logcatd.rc took 0.00s.)
[    6.512459] init: (Parsing /system/etc/init/logd.rc took 0.00s.)
[    6.519675] init: (Parsing /system/etc/init/mdnsd.rc took 0.00s.)
[    6.527017] init: (Parsing /system/etc/init/mediacodec.rc took 0.00s.)
[    6.534963] init: (Parsing /system/etc/init/mediadrmserver.rc took 0.00s.)
[    6.543262] init: (Parsing /system/etc/init/mediaextractor.rc took 0.00s.)
[    6.551371] init: (Parsing /system/etc/init/mediaserver.rc took 0.00s.)
[    6.559226] init: (Parsing /system/etc/init/metrics_collector.rc took 0.00s.)
[    6.567873] init: (Parsing /system/etc/init/metricsd.rc took 0.00s.)
[    6.575643] init: (Parsing /system/etc/init/mtpd.rc took 0.00s.)
[    6.582890] init: (Parsing /system/etc/init/netd.rc took 0.00s.)
[    6.590109] init: (Parsing /system/etc/init/perfprofd.rc took 0.00s.)
[    6.598010] init: (Parsing /system/etc/init/peripheralman.rc took 0.00s.)
[    6.606255] init: (Parsing /system/etc/init/racoon.rc took 0.00s.)
[    6.613677] init: (Parsing /system/etc/init/recovery-persist.rc took 0.00s.)
[    6.621908] init: (Parsing /system/etc/init/recovery-refresh.rc took 0.00s.)
[    6.630468] init: (Parsing /system/etc/init/servicemanager.rc took 0.00s.)
[    6.638777] init: (Parsing /system/etc/init/surfaceflinger.rc took 0.00s.)
[    6.646974] init: (Parsing /system/etc/init/uncrypt.rc took 0.00s.)
[    6.654501] init: (Parsing /system/etc/init/update_engine.rc took 0.00s.)
[    6.662699] init: (Parsing /system/etc/init/vdc.rc took 0.00s.)
[    6.670016] init: (Parsing /system/etc/init/vold.rc took 0.00s.)
[    6.681634] init: Starting service 'logd'...
[    6.687354] EXT4-fs (mmcblk0p6): re-mounted. Opts: (null)
[    6.699500] init: Starting service 'exec 1 (/system/bin/recovery-refresh)'...
[    6.708212] random: logd: uninitialized urandom read (40 bytes read, 88 bits of entropy available)
[    6.712359] random: recovery-refres: uninitialized urandom read (40 bytes read, 88 bits of entropy available)
[    6.741859] init: Service 'exec 1 (/system/bin/recovery-refresh)' (pid 128) exited with status 254
[    6.756271] init: (Loading properties from /system/build.prop took 0.00s.)
[    6.763653] init: (Loading properties from /vendor/build.prop took 0.00s.)
[    6.770792] init: (Loading properties from /factory/factory.prop took 0.00s.)
[    6.778493] init: /recovery not specified in fstab
[    6.788070] init: Starting service 'debuggerd'...
[    6.793979] init: do_start: Service debuggerd64 not found
[    6.803675] init: Starting service 'vold'...
[    6.809301] random: debuggerd: uninitialized urandom read (40 bytes read, 88 bits of entropy available)
[    6.816596] init: Not bootcharting.
[    6.823973] random: vold: uninitialized urandom read (40 bytes read, 89 bits of entropy available)
[    6.854642] logd.auditd: start
[    6.857802] logd.klogd: 6815828955
[    7.113166] random: vdc: uninitialized urandom read (40 bytes read, 90 bits of entropy available)
[    7.620199] init: Starting service 'exec 2 (/system/bin/tzdatacheck)'...
[    7.633226] random: tzdatacheck: uninitialized urandom read (40 bytes read, 91 bits of entropy available)
[    7.669806] init: Service 'exec 2 (/system/bin/tzdatacheck)' (pid 143) exited with status 0
[    7.695035] init: Starting service 'exec 3 (/system/bin/recovery-persist)'...
[    7.707929] random: recovery-persis: uninitialized urandom read (40 bytes read, 91 bits of entropy available)
[    7.740473] init: Service 'exec 3 (/system/bin/recovery-persist)' (pid 144) exited with status 0
[    7.749671] init: (Loading properties from /data/local.prop took 0.00s.)
[    7.759463] random: init: uninitialized urandom read (40 bytes read, 91 bits of entropy available)
[    7.827689] init: Starting service 'logd-reinit'...
[    7.834863] init: write_file: Unable to open '/proc/sys/vm/min_free_order_shift': No such file or directory
[    7.835653] random: logd: uninitialized urandom read (40 bytes read, 91 bits of entropy available)
[    7.857853] init: Starting service 'healthd'...
[    7.864007] init: Starting service 'lmkd'...
[    7.866687] logd.daemon: reinit
[    7.873339] init: Starting service 'servicemanager'...
[    7.880474] init: Starting service 'surfaceflinger'...
[    7.887028] init: couldn't write 150 to /sys/fs/cgroup/stune/foreground/tasks: No such file or directory
[    7.887185] init: Service 'logd-reinit' (pid 146) exited with status 0
[    7.889144] init: write_file: Unable to open '/sys/kernel/debug/tracing/tracing_on': No such file or directory
[    7.890089] init: Starting service 'console'...
[    7.890956] init: Starting service 'adbd'...
[    7.892611] init: cannot find '/system/bin/update_verifier' (No such file or directory), disabling 'exec 4 (/system/bin/update_verifier)'
[    7.892703] init: cannot find '/system/bin/install-recovery.sh' (No such file or directory), disabling 'flash_recovery'
[    7.893305] init: Starting service 'zygote'...
[    7.895023] init: Starting service 'audioserver'...
[    7.896870] init: Starting service 'cameraserver'...
[    7.898524] init: Starting service 'drm'...
[    7.900585] init: Starting service 'installd'...
[    7.902310] init: Starting service 'keystore'...
[    7.904309] init: Starting service 'mediacodec'...
[    7.906186] init: Starting service 'mediadrm'...
[    7.907798] init: Starting service 'mediaextractor'...
[    7.909443] init: Starting service 'media'...
[    7.911029] init: Starting service 'netd'...
[    7.913047] init: Starting service 'peripheralman'...
[    7.914944] init: Starting service 'crash_reporter'...
[    7.916629] init: Starting service 'crash_sender'...
[    7.918669] init: Starting service 'gatekeeperd'...
[    7.920570] init: Starting service 'inputdriverserv'...
[    7.922677] init: Starting service 'metricscollector'...
[    7.924560] init: Starting service 'metricsd'...
[    7.969471] init: Starting service 'perfprofd'...
[    7.971092] init: Starting service 'update_engine'...
[    7.988910] init: write_file: Unable to open '/sys/class/android_usb/android0/enable': No such file or directory
[    7.988995] init: write_file: Unable to open '/sys/class/android_usb/android0/idVendor': No such file or directory
[    7.989065] init: write_file: Unable to open '/sys/class/android_usb/android0/idProduct': No such file or directory
[    7.989147] init: write_file: Unable to open '/sys/class/android_usb/android0/functions': No such file or directory
[    7.989214] init: write_file: Unable to open '/sys/class/android_usb/android0/enable': No such file or directory
[    7.989940] init: write_file: Unable to open '/sys/class/android_usb/android0/enable': No such file or directory
[    7.990008] init: write_file: Unable to open '/sys/class/android_usb/android0/idVendor': No such file or directory
[    7.990077] init: write_file: Unable to open '/sys/class/android_usb/android0/idProduct': No such file or directory
[    7.990149] init: write_file: Unable to open '/sys/class/android_usb/android0/functions': No such file or directory
[    7.990215] init: write_file: Unable to open '/sys/class/android_usb/android0/enable': No such file or directory
[    8.326168] healthd: No battery devices found
rpi3:/ $ [    8.582687] init: avc:  denied  { set } for property=ctl.mdnsd pid=152 uid=2000 gid=2000 scontext=u:r:adbd:s0 tcontext=u:object_r:ctl_mdnsd_prop:s0 tclass=property_service permissive=1
[    8.601788] init: Starting service 'mdnsd'...
[    9.252437] init: Service 'crash_reporter' (pid 165) exited with status 0
[    9.776477] type=1400 audit(9.729:11): avc: denied { read } for pid=155 comm="cameraserver" name="/" dev="tmpfs" ino=7171 scontext=u:r:cameraserver:s0 tcontext=u:object_r:device:s0 tclass=dir permissive=1
[    9.839277] type=1400 audit(9.729:12): avc: denied { open } for pid=155 comm="cameraserver" path="/dev" dev="tmpfs" ino=7171 scontext=u:r:cameraserver:s0 tcontext=u:object_r:device:s0 tclass=dir permissive=1
[    9.985247] init: Starting service 'bootanim'...
[   11.844349] type=1400 audit(11.799:13): avc: denied { execmem } for pid=271 comm="BootAnimation" scontext=u:r:bootanim:s0 tcontext=u:r:bootanim:s0 tclass=process permissive=1
[   11.863321] type=1400 audit(11.799:14): avc: denied { execute } for pid=271 comm="BootAnimation" path="/dev/ashmem" dev="tmpfs" ino=8223 scontext=u:r:bootanim:s0 tcontext=u:object_r:ashmem_device:s0 tclass=chr_file permissive=1
[   13.116410] type=1400 audit(13.059:15): avc: denied { dac_override } for pid=164 comm="peripheralman" capability=1 scontext=u:r:peripheralman:s0 tcontext=u:r:peripheralman:s0 tclass=capability permissive=1
[   15.097072] type=1400 audit(15.049:16): avc: denied { sys_module } for pid=163 comm="netd" capability=16 scontext=u:r:netd:s0 tcontext=u:r:netd:s0 tclass=capability permissive=1
[   21.045858] capability: warning: `main' uses 32-bit capabilities (legacy support in use)

rpi3:/ $ 
rpi3:/ $ [   25.893261] random: nonblocking pool is initialized
[   30.081167] healthd: battery l=100 v=0 t=42.4 h=2 st=2 chg=a
[   33.214939] smsc95xx 1-1.1:1.0 eth0: hardware isn't capable of remote wakeup
[   33.222788] IPv6: ADDRCONF(NETDEV_UP): eth0: link is not ready
```



# 4. adb连接

我的树莓派用网线跟电脑连接到同一个局域网。树莓派的ip地址是192.168.0.107 。

在window的cmd界面里。输入下面的命令：

```
adb connect 192.168.0.107:5555
```

再查看：

```
C:\Users\Administrator>adb devices
List of devices attached
192.168.0.107:5555      device
```

看看板端能否ping通网络。

```
adb shell ping www.sina.com
```

是正常的。

# 5. 系统的一些基本情况

1、内置了toybox，是类似busybox的一个东西。



# 5. 用Android studio开发一个helloworld



