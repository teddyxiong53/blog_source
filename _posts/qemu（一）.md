---
title: qemu（一）
date: 2018-03-23 18:50:35
tags:
	- qemu

---



一直觉得虚拟机很神奇。qemu可以是一个很好的切入点，我也有很多的使用上的问题，希望可以在代码里得到解答。

# 发展历史

QEMU（Quick Emulator）是一款开源的虚拟化软件，最初由Fabrice Bellard于2003年创建。它提供了一个模拟器和虚拟机监视器，能够在不同的硬件架构上运行各种操作系统。以下是QEMU的发展历史的一些重要里程碑：

1. **初始版本（2003年）**：QEMU的初始版本由Fabrice Bellard开发，并于2003年首次发布。最初的版本提供了对x86架构的模拟支持。

2. **加速器模式（2005年）**：为了提高性能，QEMU引入了加速器模式。通过与主机操作系统的内核模块（例如KVM、Xen等）交互，QEMU能够在硬件级别上直接执行客户操作系统的指令，从而加快虚拟化的速度。

3. **系统模拟器（2005年）**：除了虚拟化，QEMU还能作为一个系统模拟器，用于在不同的硬件平台上模拟运行操作系统。这使得开发人员可以在一台计算机上开发和测试针对不同硬件平台的软件。

4. **QEMU开发者会议（2006年至今）**：自2006年起，QEMU开发者定期举办开发者会议，以促进社区交流和合作。这些会议为QEMU的发展提供了重要的平台，并推动了新功能的开发和改进。

5. **硬件加速（2010年）**：QEMU引入了针对特定硬件设备的硬件加速支持，例如GPU和网络设备的硬件加速，进一步提高了虚拟化的性能和兼容性。

6. **QEMU和KVM的整合（2010年至今）**：QEMU与KVM（Kernel-based Virtual Machine）项目的整合使得QEMU能够利用KVM提供的硬件虚拟化扩展，进一步提高了虚拟化性能和功能。

7. **QEMU的多架构支持（2012年至今）**：QEMU逐渐扩展支持多种硬件架构，包括x86、ARM、MIPS、PowerPC等，使得开发人员可以在不同的硬件平台上进行开发和测试。

8. **QEMU的广泛应用（2012年至今）**：随着时间的推移，QEMU已成为虚拟化和模拟领域的重要工具，被广泛应用于各种场景，包括云计算、嵌入式系统开发、操作系统开发和测试等。

总体来说，QEMU经过多年的发展和改进，成为一款强大而

灵活的虚拟化和模拟工具，支持多种硬件架构和操作系统，为开发人员提供了丰富的功能和性能。它在开源社区中得到广泛的关注和使用，并持续进行改进和创新。

# bochs和qemu比较

Bochs和QEMU都是开源的虚拟化软件，但它们在设计和特性上有一些区别。下面是Bochs和QEMU的比较：

1. **模拟器 vs. 虚拟机监视器**：Bochs是一个完全模拟的x86虚拟机，它通过解释执行指令来模拟整个计算机系统。而QEMU既可以作为模拟器，也可以作为虚拟机监视器，在硬件加速的情况下，它能够直接在主机CPU上执行客户机指令。

2. **性能**：由于QEMU能够利用硬件加速和虚拟化技术，它通常比Bochs具有更好的性能。QEMU通过与主机操作系统的内核模块（如KVM）交互，实现硬件级别的虚拟化，可以直接在主机CPU上执行客户机指令，从而加快了虚拟化的速度。

3. **支持的架构**：Bochs主要支持x86架构，可以模拟运行x86操作系统。而QEMU支持多种硬件架构，包括x86、ARM、MIPS、PowerPC等，可以在不同的硬件平台上模拟和运行各种操作系统。

4. **开发和使用**：Bochs的代码相对较老，其开发和维护的活跃程度相对较低。QEMU则是一个活跃的开源项目，拥有庞大的开发社区和活跃的开发者，不断推出新的功能和改进。

5. **应用场景**：由于QEMU具有更好的性能和广泛的硬件架构支持，它在各种场景下得到广泛应用，包括虚拟化、模拟、嵌入式开发等。Bochs则更适合于学术研究、教育和调试等用途。

总体来说，QEMU在性能、硬件架构支持和活跃的开发社区方面更具优势，而Bochs在模拟器的纯粹性和一些特定用途下可能更适合。选择使用哪个软件取决于具体的需求和使用场景。



# 代码分析

当前我都是在命令行下面使用qemu的。其实可以试一下图形化界面的情况。

我就试一下在windows的使用。看看有什么不一样的地方。

下载地址在这里。

http://qemu.weilnetz.de/w64/2018/

安装程序98M。不大。下载是2.12版本的。

安装后，还是只能命令行运行。然后是有问题。

```
D:\Program Files\qemu>qemu-system-i386
Unexpected error in aio_context_set_poll_params() at /home/stefan/src/qemu/repo.or.cz/qemu/ar7/util/aio-win32.c:413:
qemu-system-i386: AioContext polling is not implemented on Windows
```

解决的办法有，就是降低qemu的版本。



下载qemu代码。解压后，大概260M。文件24000个左右。是挺多的，跟linux源代码的规模差不多了。

可以在各种平台上编译，我就在linux上编译。

```
ERROR: glib-2.22 gthread-2.0 is required to compile QEMU
```



后面我在搭建mini2440的qemu环境时，下载了2440定制版的qemu。代码不多，编译很顺利。

我就以这个版本来进行学习。



qemu没有顶层设计文档，只能通过代码来阅读。

qemu的和核心是一个叫TCG的东西，TCG是Tiny Code Generator。是用来动态地把指令翻译成目标的指令。

例如把x86的翻译成arm的指令。



我们先看看顶层的Makefile。

我们可以先生成文档。

```
teddy@teddy-ubuntu:~/work/mini2440-lab/qemu$ make html
  GEN   qemu-doc.html
  GEN   qemu-tech.html
```

qemu-doc.html就是使用文档。

qem-tech.html里没什么东西。



make生成的可执行文件有4个：

```
1、arm-softmmu/qemu-system-arm。这个是主要文件。
2、qemu-img：用来生成镜像文件的。
3、qemu-io   
4、qemu-nbd  ：网络块设备。
```

简单起见，我可以从qemu-img这个工具开始看。

这个文件很简单。就一个c文件qemu-img.c。

qemu-system-arm的入口文件是vl.c。

最顶层的数据结构是QEMUMachine。代表了一个qemu虚拟机的抽象。

```
typedef struct QEMUMachine {
    const char *name;
    const char *desc;
    QEMUMachineInitFunc *init;//重点是这个。
    int use_scsi;
    int max_cpus;
    struct QEMUMachine *next;
} QEMUMachine;
```

结构体倒是不大。

我们可以看一下versatilepb这个machine的情况。

```
QEMUMachine versatilepb_machine = {
    .name = "versatilepb",
    .desc = "ARM Versatile/PB (ARM926EJ-S)",
    .init = vpb_init,
    .use_scsi = 1,
};
```

最最主要的抽象应该就是这个。

```
#define CPUState struct CPUARMState
```

我们看看CPUARMState这个结构体的内容，非常多。但是我们还是一条条看。

```
1、u32 regs[16] //代表当前模式的16个寄存器。
2、u32 uncached_cpsr。 //
3、u32 spsr
4、u32 banked_spsr[6] //有几个特殊模式有自己的备份。
5、u32 banked_r13[6]
6、u32 banked_r14[6]
7、u32 usr_regs[5] //r8到r12的
8、u32 fiq_regs[5]
9、u32 CF/VF/NF/ZF/GE
10、u32 thumb。0是arm模式，1是thumb模式。
11、u32 condexec_bits
12、struct { //cp15寄存器结构体
  u32 c0_cpuid;
  u32 c0_cachetype;
  u32 c0_ccsid[16];
  ...
  u32 c3;
  ...
  u32 c15_i_max;
} cp15;
13、struct {//v7m这种特殊架构。
  u32 other_sp;
  ...
  void *nvic
} v7m;
14、struct {
  ARMReadFunc *cp_read;
  ARMWriteFunc *cp_write;
  void *opaque;
} cp[15]; //协处理器被外设io使用的。
15、u32 teecr, teehbr; //thumb-2 EE state
16、u32 features //cpu features
17、int (*get_irq_vector)(struct CPUARMState *);
18、void *irq_opaque //opaque跟transparent是反义词，表示不透明。
19、struct { // vfp 协处理器。
  f64 regs[32];
  ...
} vfp;
20、u32 mmon_addr //不知道是什么。
21、struct {//iwmmxt 协处理器。
  ...
} iwmmxt; 
22、CPU_COMMON。这个是一个宏。包含了所有CPU通用的部分，是一大堆内容，我这里不展开了。
23、struct arm_boot_info *boot_info。
	int ram_size
	char *kernel_filename, *kernel_cmdline, *initrd_filename, 
	u32 loade_start, smp_loader_start
	int nb_cpus, board_id
	int (*atag_board)(struct arm_boot_info *info, void *p)
```



对于内存的抽象是RAMBlock结构体。

```
1、u8 *host
2、u32 offset
3、u32 length
4、*next
```

创建寄存器是这样的：

```
    sysbus_create_simple("pl011", 0x101f1000, pic[12]);
    sysbus_create_simple("pl011", 0x101f2000, pic[13]);
    sysbus_create_simple("pl011", 0x101f3000, pic[14]);
    sysbus_create_simple("pl011", 0x10009000, sic[6]);
```

我们现在还是回到mini2440的上面来。

对这个板子也有一个结构体来进行描述。

struct mini2440_board_s

```
1、struct s3c_state_s。这个也是一个很大的结构体，是对S3C2440这个soc的抽象。下面单独展开看。
2、u32 ram
3、struct ee24c80_s *eeprom //一块at24c08的eeprom。
4、char *kernel
5、SDState *mmc。
6、pflash_t *nor
7、 int bl_level。
8、int boot_mode。
```

现在看看struct s3c_state_s

```
1、CPUState *env。对于arm核心的抽象。
2、struct s3c_freq_s clock 
3、u32 cpu_id
4、qemu_irq *irq
5、qemu_irq *drq
6、struct s3c_pic_state_s *pic //这些都是对于内部寄存器的抽象。每一个都值得展开看看。
7、struct s3c_dma_state_s *dma
   *gpio
   *lcd
   *timers
   *uart[3]
   *mmci
   *adc
   *i2c
   *i2s
   *rtc
   *spi
   *udc
   *wdt
   *nand
8. u32 mc_base; //mmc controller
9. u32 mc_regs[13]
10. u32 clkpwr_base
11. u32 clkpwr_regs[6+1]
```

把s3c_gpio_state_s 看看。

```
1. u32 cpu_id
2. u32 base
3. qemu_irq *pic
4. qemu_irq *in
5. struct {
  int n;
  u32 con;
  u32 dat;
  u32 up;
  qemu_irq handler[32];
} bank[S3C_IO_BANKS];//8
6. u32 inform[2]
7. u32 pwrstat
8. u32 misccr
9. u32 dclkcon
10. u32 extint[3]
11. u32 eintflt[2]
12. u32 eintmask
13. u32 eintpend
```

对应的文件是qemu/hw/s3c24xx_gpio.c。

继续回到main函数，看看对于参数的解析。

我们先看看help信息的展示。

help信息都在qemu/arm-softmmu/qemu-options.h里。

我们一条条看。

```
-h ：这个显示帮助信息。
-version ：显示版本。
------------基础内容-------------------
-M xxx。你可以-M ?来查看支持的机器。
-cpu xxx。你可以-cpu ?来查看支持的CPU。
-smp x。指定几个CPU核心。
-numa 后面跟一堆的内容，这个是指定多块不连续的内存芯片。一般不用。
-fda xxx 指定软盘镜像文件。
-hda xxx 指定硬盘镜像文件。
-cdrom xxx 指定光盘镜像文件。
-drive 后面是一堆的参数。不看了。
-mtdblock xxx 指定flash
-sd xxx 指定SD卡镜像文件
-pflash xxx指定并口flash
-m xxx 指定内存大小。
-k xxx 指定键盘布局。
-usb xxx 指定usb驱动
-usbdevice xxx 指定usb设备。
-name xxx 指定机器的名字。
-nographic 默认是会启动一个图形界面的。这样就不会启动。
-curses 启动一个curses界面。
-------------网络相关---------------

------------boot相关---------------
-kernel xxx 指定内核。
-append xxx。带cmdline
-initrd xxx。使用initrd镜像。

---------调试选项--------------------
-serial xxx。重定向串口
-parallel xxx。重定向并口。
-monitor xxx。重定向monitor
-gdb xxx
-show-cursor

```

我当前比较关注usb的，看看usb设备的如何加载进去。

现在我在qemu启动命令里加上：

```
-usb -usbdevice disk::./usb.img
```

-usb是打开usb功能。

现在在linux里可以看到usb信息，但是没有设备节点出来。是不是需要把usb对应的驱动加载进来？

我拷贝进来，加载看看。

```
/ko # insmod usb-storage.ko 
usb_storage: Unknown symbol scsi_report_device_reset (err 0)
```

是scsi没有被编译进来。

也是模块，编译了，我没有拷贝过。

是 ./drivers/scsi/scsi_mod.ko 这个模块。

```
/ko # insmod scsi_mod.ko 
SCSI subsystem initialized
/ko # lsmod
scsi_mod 102805 0 - Live 0xbf000000
/ko # insmod usb-storage.ko 
usb-storage 1-3:1.0: USB Mass Storage device detected
scsi host0: usb-storage 1-3:1.0
usbcore: registered new interface driver usb-storage
/ko # scsi 0:0:0:0: Direct-Access     QEMU     QEMU HARDDISK    0.10 PQ: 0 ANSI: 3

/ko # 
/ko # lsmod
usb_storage 40410 0 - Live 0xbf028000
scsi_mod 102805 1 usb_storage, Live 0xbf000000
```

这样插入就不会报错了。

但是还是看不到节点。

改一下qemu的选项。

```
-drive if=none,id=usbstick,file=./usb.img -usb -device usb-ehci,id=ehci -device usb-storage,bus=ehci.0,drive=usbstick
```

但是这个在我的qemu上是不识别的。

```
/home/teddy/work/mini2440-lab/qemu/arm-softmmu/qemu-system-arm: invalid option -- '-device'
Makefile:71: recipe for target 'boot' failed
make: *** [boot] Error 1
```

算了还是回退到：

```
-usb -usbdevice disk::./usb.img
```

暂时不管usb的了。

后面我单独看usb的内容的时候，发现是应该这样加载：

```
insmod scsi_mod.ko
insmod sd_mod.ko #之前少了这个。
insmod usb-storage.ko
```

现在打印是这样的：

```
/ko # scsi 0:0:0:0: Direct-Access     QEMU     QEMU HARDDISK    0.10 PQ: 0 ANSI: 3
sd 0:0:0:0: [sda] 131072 512-byte logical blocks: (67.1 MB/64.0 MiB)
sd 0:0:0:0: [sda] Write Protect is off
sd 0:0:0:0: [sda] Write cache: enabled, read cache: enabled, doesn't support DPO or FUA
lsd 0:0:0:0: [sda] Attached SCSI disk
```

但是/dev下面还是没有看到节点。

看分区信息里，有了。

```
/proc/bus # cat /proc/partitions 
major minor  #blocks  name

   1        0      65536 ram0
   1        1      65536 ram1
   1        2      65536 ram2
   1        3      65536 ram3
   1        4      65536 ram4
   1        5      65536 ram5
   1        6      65536 ram6
   1        7      65536 ram7
   1        8      65536 ram8
   1        9      65536 ram9
   1       10      65536 ram10
   1       11      65536 ram11
   1       12      65536 ram12
   1       13      65536 ram13
   1       14      65536 ram14
   1       15      65536 ram15
  31        0        256 mtdblock0
  31        1        128 mtdblock1
  31        2       5120 mtdblock2
  31        3      60032 mtdblock3
   8        0      65536 sda
```

这个时候，我只要输入mdev -s进行一次扫描就好了。

这样就自动在/dev目录下生成了sda的节点了。

```
/proc/bus # ls /dev/s
sda   snd/
```

这里是个改进点，我要把我的mini2440-lab改进一下，让热插拔的时候自动扫描才好。

这个具体到mini2440-lab的相关文章里去描述。



主循环我不管。

我还是关注硬件的抽象这一部分。

我看看i2c的和at24c08的模拟。

at24的抽象。

```
struct _eeprom24c0x_t {
  u8 kind;
  u8 tick;
  u8 address;
  u8 command;
  u8 ack;
  u8 scl;
  u8 sda;
  u8 data;
  u8 contents[1024];//这里就是模拟数据区域的。
};
```











# 参考资料

1、Libvirt Qemu KVM 教程大全

https://wenku.baidu.com/view/999f2c6b52ea551810a687e3.html

2、Qemu使用手册

https://wenku.baidu.com/view/c8ccb5ce9ec3d5bbfd0a74d4.html?sxts=1522901304319

3、官方文档

https://wiki.qemu.org/Documentation

4、编程领域中的 "transparent" 和 "opaque"

https://blog.csdn.net/dashuniuniu/article/details/51702772

5、Qemu 简述。相关博文都值得阅读。

https://www.cnblogs.com/bakari/p/7858029.html

6、

https://github.com/qemu/qemu/blob/master/docs/usb-storage.txt

7、

https://github.com/qemu/qemu/blob/master/docs/usb2.txt

