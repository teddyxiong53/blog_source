---
title: uboot之fulinus博文学习
date: 2018-03-02 10:27:22
tags:
	- uboot

---



fulinus是csdn上的一个博客专家，有写了一系列的uboot博文，很系统，我现在就学习总结一下。

第一篇在这里：http://blog.csdn.net/fulinus/article/details/40304719

系列博文是按照日期来排列的，我保持下面的记录日期一致。

基于的板子是tq2440的。

# 第一天

下载uboot源代码。熟悉目录结构。

# 第二天

学习bootloader原理。

https://www.ibm.com/developerworks/cn/linux/l-btloader/

这篇文章讲得很好。

# 第三天

学习裸机程序的编写。

分两种情况：

## 情况一

你的开发板已经有了可用的uboot，因为裸机程序能够运行的前提是系统初始化了。

写一个led程序，用c用汇编都可以，编译得到led.bin文件。

然后把jlink连接到板子上，电脑上打开J-Link Commander，输入下面的命令

```
h
speed 12000
loadbin d:\led.bin 0x33000000
setpc 0x33000000
g
```

## 情况二

你的开发板还没有一个可用的uboot，这样你就不得不自己来进行ddr等的初始化了。

自己写一个Bootstrap.s。

# 第四天

先用汇编写一个蜂鸣器程序beep.s。

然后是改一下，改成汇编调用C语言函数的方式。

现在就需要引入链接脚本文件了。因为链接器不知道该把汇编的内容放在前面还是把C语言的内容放在前面。

这个就需要我们用lds文件来指定。新建beep.lds，内容是这样的：

```
OUTPUT_FORMAT("elf32-littlearm", "elf32-littlearm", "elf32-littlearm" )
OUTPUT_ARCH(arm)
ENTRY(_start)

SECTIONS {
    . = 0x33000000;
    .text : {
        start.o(.text*)
        *(.text*)
        *(.rodata)
    }
    
    .data ALIGN(4): {
        *(.data)
    }
    
    .bss ALIGN(4): {
        *(.bss)
    }
}
```

然后Makefile里的LDFLAGS：

```
LDFLAGS = -nostartfiles -T beep.lds -Ttext 0x33000000
```

# 第五天

C语言写按键的驱动。并且把前面的beep、led都加进了一起。



# 第六天

分析lds文件。

先写了一个section.c的文件。

```
#include <stdio.h>
#include <stdlib.h>

int localmemory0 __attribute__((section("LOCALmem"))) = 0;
int localmemory1 __attribute__((section("LOCALmem"))) = 0;

int globalmemory __attribute__((section("GLOBALmem"))) = 0;

int main()
{
    localmemory0 = 0x123;
    localmemory1 = 0x456;
    globalmemory = localmemory0 + localmemory1;
    return 0;
}

```

编译得到o文件：

```
gcc -o section.o -c section.c
```

内容如下：

```
pi@raspberrypi:~/test/c-test$ objdump -d section.o
section.o:     file format elf32-littlearm
Disassembly of section .text:
00000000 <main>:
   0:   e52db004        push    {fp}            ; (str fp, [sp, #-4]!)
   4:   e28db000        add     fp, sp, #0
   8:   e59f3040        ldr     r3, [pc, #64]   ; 50 <main+0x50>
   c:   e59f2040        ldr     r2, [pc, #64]   ; 54 <main+0x54>
  10:   e5832000        str     r2, [r3]
  14:   e59f303c        ldr     r3, [pc, #60]   ; 58 <main+0x58>
  18:   e59f203c        ldr     r2, [pc, #60]   ; 5c <main+0x5c>
  1c:   e5832000        str     r2, [r3]
  20:   e59f3028        ldr     r3, [pc, #40]   ; 50 <main+0x50>
  24:   e5932000        ldr     r2, [r3]
  28:   e59f3028        ldr     r3, [pc, #40]   ; 58 <main+0x58>
  2c:   e5933000        ldr     r3, [r3]
  30:   e0822003        add     r2, r2, r3
  34:   e59f3024        ldr     r3, [pc, #36]   ; 60 <main+0x60>
  38:   e5832000        str     r2, [r3]
  3c:   e3a03000        mov     r3, #0
  40:   e1a00003        mov     r0, r3
  44:   e24bd000        sub     sp, fp, #0
  48:   e49db004        pop     {fp}            ; (ldr fp, [sp], #4)
  4c:   e12fff1e        bx      lr
  50:   00000000        .word   0x00000000
  54:   00000123        .word   0x00000123
  58:   00000000        .word   0x00000000
  5c:   00000456        .word   0x00000456
  60:   00000000        .word   0x00000000
```

然后写一个section.lds文件。

```
OUTPUT_FORMAT("elf32-littlearm", "elf32-littlearm", "elf32-littlearm")
OUTPUT_ARCH(arm)
ENTRY(_start)

SECTIONS {
    .text: {
        *(.text)
    }
    LOCALmem 0x1f0000 : {
        *(LOCALmem)
    }
    GLOBALmem 0xff0000: {
        *(GLOBALmem)
    }
    
}
```

链接生成elf文件：

```
ld -o section.elf -T section.lds section.o
```

分析如下：

```
pi@raspberrypi:~/test/c-test$ objdump -S section.elf

section.elf:     file format elf32-littlearm


Disassembly of section .text:

00000000 <main>:
   0:   e52db004        push    {fp}            ; (str fp, [sp, #-4]!)
   4:   e28db000        add     fp, sp, #0
   8:   e59f3040        ldr     r3, [pc, #64]   ; 50 <main+0x50>
   c:   e59f2040        ldr     r2, [pc, #64]   ; 54 <main+0x54>
  10:   e5832000        str     r2, [r3]
  14:   e59f303c        ldr     r3, [pc, #60]   ; 58 <main+0x58>
  18:   e59f203c        ldr     r2, [pc, #60]   ; 5c <main+0x5c>
  1c:   e5832000        str     r2, [r3]
  20:   e59f3028        ldr     r3, [pc, #40]   ; 50 <main+0x50>
  24:   e5932000        ldr     r2, [r3]
  28:   e59f3028        ldr     r3, [pc, #40]   ; 58 <main+0x58>
  2c:   e5933000        ldr     r3, [r3]
  30:   e0822003        add     r2, r2, r3
  34:   e59f3024        ldr     r3, [pc, #36]   ; 60 <main+0x60>
  38:   e5832000        str     r2, [r3]
  3c:   e3a03000        mov     r3, #0
  40:   e1a00003        mov     r0, r3
  44:   e24bd000        sub     sp, fp, #0
  48:   e49db004        pop     {fp}            ; (ldr fp, [sp], #4)
  4c:   e12fff1e        bx      lr
  50:   001f0000        .word   0x001f0000
  54:   00000123        .word   0x00000123
  58:   001f0004        .word   0x001f0004
  5c:   00000456        .word   0x00000456
  60:   00ff0000        .word   0x00ff0000
```

（运行会出现段错误的，不管，不是当前的关键）。



# 第七天

开始看u-boot.lds文件。

```
ENTRY(_start)
SECTIONS
{
 . = 0x00000000;
 . = ALIGN(4);
 .text :
 {
  *(.__image_copy_start)
  *(.vectors)
  CPUDIR/start.o (.text*) 
  *(.text*)
 }
```

`__image_copy_start`是镜像文件拷贝的起始地址，在arch/arm/lib/sections.c里定义如下：

```
char __image_copy_start[0] __attribute__((section(".__image_copy_start")));
char __image_copy_end[0] __attribute__((section(".__image_copy_end")));
```

在common/board_r.c里被使用：

```
int initr_reloc_global_data
{
  #ifdef __ARM__
	monitor_flash_len = _end - __image_copy_start;
}
```

`*(.vectors)`这个段，则是在arch/arm/lib/vectors.S里定义的。

```
.section ".vectors", "x"
```

紧接着vectors段的，就是start.o里的text段了。

文件是arch/arm/cpu/arm920t/start.S。

这个text段的开头就是reset标签。

然后代码里就是关闭中断、进入svc模式等等操作。

#第八天

分析一个cpu_init_crit的函数。我不管这个函数先。

然后是进入到一个_main的函数，在arch/arm/lib/crt0.S里。

#第九天

依次分析arch/arm/lib/crt0.S里面的内容。

最后是一个b	relocate_code。

#第十天

relocate_code函数在arch/arm/lib/relocate.S里。

uboot最重要的一个功能就是relocate重定向。

重定向，简单说，就是把nand flash上的程序搬移到内存里。

重定向涉及到3个地址：link地址、load地址、run地址。

link地址是我们在uboot利配置的。用于指导链接器来生成uboot.bin文件。

load地址是内存里放uboot.bin的位置。

上面这3个地址一般都是同一个值。

uboot在哪里执行，这个信息在编译的时候就已经确定了。

uboot的重定向有2个，老的和新的 。

老的uboot只有一个重定向，这个重定向由移植uboot的工程师，根据板子的具体配置来编写。

新的uboot有2个重定向。第一个重定向跟老的一样，目的就是从nand或nor上把镜像拷贝到ddr里。

第二个重定向，就是relocate_code函数，这个不需要我们修改。它的作用是把uboot从当前的位置拷贝到内存较高的位置上去。因为内核一般是从低的位置放的。

全局变量的重定向，借助了一个GOT（Global Offset Table）的表。

第二个重定向，不做也没什么大的关系。

# 第十一天

没什么。

# 第十二天

没什么。

# 第十三天

开始进行tq2440的uboot移植。

uboot里一直都没有添加对2440的支持。

2440和2410的区别：

```
1、2440主频更高，增加了camera接口、ac97音频接口。
2、nand flash控制器接口有较大的变化。
3、芯片时钟控制寄存器有一些变化。
4、其他的都是相同的。
```

1、添加开发板目录。

```
mkdir -p board/samsung/tq2440
```

2、选择smdk2410的作为tq2440的模板。把里面的文件都拷贝到tq2440下面来。

修改文件名。

```
mv smdk2410.c tq2440.c
```

3、在include/configs/目录下增加一个tq2440.h的文件。先把smdk2410.h的内容拷贝到里面。

4、修改arch/arm/kconfig文件，增加tq2440的条目。就拷贝2410的改就行。

5、现在先编译一下。会有错误。

# 第十四天

继续。

1、修改tq2440.h内容。

屏蔽暂时不需要的功能，网卡、usb、一些cmd。

加上跳过底层初始化函数。

```
#define CONFIG_SKIP_LOWLEVEL_INIT  （这个实际上有问题）后面会解决这个。
```

编译成功，得到u-boot.bin文件。

2、然后在板子上跑起来，死机了。

提示Flash failed。

在tq2440.h里加上：

```
#define DEBUG
```

这样再编译运行，死机信息就更加详细。

发现是是因为没有找到匹配的flash型号导致的。

加上tq2440的EN29LV160AB的这款。这个是norflash。

然后继续看。还需要进行一些微调，要看flash的手册。

# 第十五天

uboot代码被重定位到了0x33FC0000的位置好，后面的4160K做了heap，

0X33FC0000才是uboot代码开始的位置，我们可以修改tq2440.h里的CONFIG_SYS_TEXT_BASE的值为0x33FC0000，这样uboot就不需要重定向了。

# 第十六天

第十五天的改法有问题。

需要做下面的事情：

```
1、#define CONFIG_SYS_TEXT_BASE 0 ，这个改回为0
2、CONFIG_SKIP_LOWLEVEL_INIT 这个宏不要定义。我们应该进行底层初始化。
```

现在烧录就是可以运行的了。

# 第十七天

是把网卡驱动的打开。

# 第十八天

测试网络相关功能。

# 第十九天

开始调2440的nand驱动。

因为从2410到2440，nand控制器有较大的调整，用来支持大块nand。

1、拷贝文件。

```
cp drivers/mtd/nand/s3c2410_nand.c drivers/mtd/nand/s3c2440_nand.c 
```

2、把里面所有的2410替换为2440 。

3、修改一些寄存器。

4、修改Makefile，编译。

# 第二十天

昨天的运行，发现不能探测到nand，是因为这里：

```
board_nand_init
	nand->select_chip = NULL  
```

这个指针应该给一个函数的。

写这个：

```
static void s3c2440_nand_select(struct mtd_info *mtd, int chipnr)  
{  
    struct s3c2440_nand *nand = s3c2440_get_base_nand();  
  
  
    switch(chipnr){  
        case -1: /* 取消选中 */  
            nand->nfcont |= (1<<1);  
            break;  
        case 0: /* 选中 */  
            nand->nfcont &= ~(1 << 1);  
            break;  
        default:  
            BUG();  
    }  
    return;  
}  
```

赋值给select_chip指针。运行，可以探测到了。

然后测试nand，功能正常。



# 第二十一天

当前nand 读写是正常了。但是标记坏块功能会出错。

需要查阅资料进行修改。

# 第二十二天

解决了标记坏块功能的问题。

# 第二十三天

今天是把环境变量保存到nand里去。

在tq2440.h里修改：

```
#define CONFIG_ENV_IS_IN_NAND

```

# 第二十四天

分析从nand启动。我们需要做的是，在u-boot前4K代码里加入操作nand的代码。然后重定向。

# 第二十五天

1、新建一个目录。在u-boot代码根目录。

```
mkdir nand-boot
```

里面放3个文件：

```
Makefile  nand-boot.h nand-boot.S
```

把里面的内容写好。

编译得到nand-boot.bin文件。

把nand-boot.bin烧写到nand中。把板子选择为从nand启动。



# 第二十六天

要实现从nand启动，就要把uboot镜像拷贝到ddr里的某个位置上去。再从ddr里运行。



# 第二十七天

实现nand启动，最好的方法就是用u-boot提供的SPL方式。就是借助另外一个小的u-boot-spl.bin，来把u-boot.bin拷贝到ddr里去运行。

我们先试一下老的方法。

改了一堆的东西，没有成功。

# 第二十八天

继续修改，还是没有成功。

# 第二十九天

决定还是使用SPL的方式。

打开配置。编译生成u-boot-spl.bin文件。

还是需要改一些东西才能编译通过的。

# 第三十天

解决环境变量覆盖了uboot镜像的问题。

# 第三十一天

开始启动内核。

出现了卡在starting kernel的问题。

网上说这个问题的可能原因有：

1、uboot和kernel主频不匹配。

2、机器码不匹配。

3、bootargs参数不对。

4、内核中没有添加串口驱动。

解决这个问题。



