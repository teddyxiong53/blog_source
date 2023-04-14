---
title: uboot之bootm和go的区别
date: 2018-03-16 12:49:40
tags:
	- uboot

---



go和bootm的区别就是：

1、go只是修改了pc的值。go用来引导没有使用mkimage制作过的内核。

2、bootm除了修改pc值，还传递了R0/R1/R2的值过去。

bootm的m表示memory。

# bootm用法

用法：

```
bootm [addr [arg ...]]
```

arg参数对于启动linux kernel时有用。

arg可以表示initrd的地址，

如果使用了设备树，那么还有第三个参数，参数表示dtb文件的地址。

如果没有initrd，那么第二个参数给一个`-`。

例如：

```
bootm 0x108000 - 0x2000000
```

bootm包含了几个步骤，可以用子命令来单独执行对应的步骤。

步骤包括：

1、loados。把os的image读取到ddr。

2、ramdisk。这个是relocate initrd。设置uboot env：initrd_start/initrd_end。

3、fdt。relocate 设备树。

4、cmdline。os的cmdline设置。

5、bdt。board info处理。

6、prep。prepare一些操作，在go之前。

7、go，启动os。



我们当前启动是这样的：

```
bootm ${loadaddr}
```

所以是只给了一个kernel的地址参数。ramdisk和设备树的地址都没有给。

那是从哪里获取到的？



kernel的内容是这样读取出来的

```
imgread kernel ${boot_part} ${loadaddr}
```

imgread相比于普通的flash读取，有什么特别之处？

cmd\amlogic\imgread.c

```
is_andr_9_image
	有这样一个函数，那就是处理android9的镜像的。android9的镜像有什么特别的？
	
```

imgread有这些子命令：

```
static cmd_tbl_t cmd_imgread_sub[] = {
    U_BOOT_CMD_MKENT(kernel, 4, 0, do_image_read_kernel, "", ""),
    U_BOOT_CMD_MKENT(dtb,    4, 0, do_image_read_dtb, "", ""),
    U_BOOT_CMD_MKENT(res,    3, 0, do_image_read_res, "", ""),
    U_BOOT_CMD_MKENT(pic,    4, 0, do_image_read_pic, "", ""),
};
```

我关注kernel和dtb这2个命令即可。

关键是这个hdr_addr。

```
hdr_addr = (boot_img_hdr_t *)loadaddr;
```

就是kernel的镜像的最前面的内容。

```
kernel_size     =(hdr_addr->kernel_size + (hdr_addr->page_size-1)+hdr_addr->page_size)&(~(hdr_addr->page_size -1));
            ramdisk_size    =(hdr_addr->ramdisk_size + (hdr_addr->page_size-1))&(~(hdr_addr->page_size -1));
			dtbsz           = hdr_addr->second_size;
```

是不是对应的boot.img？

头部的内容是不是mkbootimg命令写进去的？

那就要分析一下mkboot.img的逻辑了。

是的。逻辑很简单。

```
config AML_IMG_READ
	depends on AML_STORAGE
	bool "image read"
	default y
	help
	  based on AML_STORAGE
	  read image without specify size
```



这个是为了处理安全的upgrade而设计的。

https://jira.amlogic.com/browse/SWPL-31296

```
forUpgrade_1stBootIndex=0
forUpgrade_bootloaderCopies=3
forUpgrade_bootloaderIndex=0
forUpgrade_flashType=BOOT_EMMC
forUpgrade_robustOta=true
forUpgrade_secureBoot=false
forUpgrade_socType=3c
```



```
a5_av400# mmc info
Device: emmc
Manufacturer ID: 15
OEM: 100
Name: 4FTE4 
Bus Speed: 192000000
Mode : HS200 (200MHz)
Rd Block Len: 512
MMC version 5.1
High Capacity: Yes
Capacity: 3.6 GiB
Bus Width: 8-bit
Erase Group Size: 512 KiB
HC WP Group Size: 8 MiB
User Capacity: 3.6 GiB WRREL
Boot Capacity: 4 MiB ENH
RPMB Capacity: 512 KiB ENH
```



get_os_type



bootm这个命令用于启动一个操作系统映像。

它会从映像文件的头部取得一些信息，

这些信息包括：

映像文件的基于的cpu架构、

其操作系统类型、

映像的类型、

压缩方式、

映像文件在内存中的加载地址、

映像文件运行的入口地址、

映像文件名等。

紧接着bootm将映像加载到指定的地址，

如果需要的话，还会解压映像并传递必要有参数给内核，最后跳到入口地址进入内核。

需要打开的宏

```cpp
CONFIG_BOOTM_LINUX=y
CONFIG_CMD_BOOTM=y
```



# upgrade_step的逻辑



假设kernel的链接地址是0x2000 8000 。

# reboot_mode有哪些

从这个寄存器读取内容

```
reboot_mode_val = ((readl(AO_SEC_SD_CFG15) >> 12) & 0x7f);
```

取值可能：

```
/*
Reboot reason AND corresponding env setting:
0:  Cold boot                 cold_boot
1:  Normal boot               normal
2:  Factory reset             factory_reset
3:  Upgrade system            update
4:  Fastboot                  fastboot
5:  Suspend                   suspend_off
6:  Hibernate                 hibernate
7:  Fastboot Bootloader       bootloader
8:  Shutdown reboot           shutdown_reboot
9:  RPMBP reboot              rpmbp
10: quiescent reboot          quiescent reboot
11 : rescueparty               rollback in AB mode
12:  Kernel panic             kernel_panic
13:  Watchdog reboot          watchdog_reboot
14: quiescent recovery reboot   quiescent recovery
15: reserved
*/
```



读取值后，会进行下面这样的一些设置

```
env_set("reboot_mode","cold_boot");
```

# 升级按键

```
	"upgrade_key="\
	"if gpio input GPIOD_2; then "\
		"echo detect upgrade key; run update;"\
	"fi;"\
```

# uboot if

common\cli_hush.c

```
static struct reserved_combo reserved_list[] = {
	{ "if",    RES_IF,    FLAG_THEN | FLAG_START },
	{ "then",  RES_THEN,  FLAG_ELIF | FLAG_ELSE | FLAG_FI },
	{ "elif",  RES_ELIF,  FLAG_THEN },
	{ "else",  RES_ELSE,  FLAG_FI   },
	{ "fi",    RES_FI,    FLAG_END  },
	{ "for",   RES_FOR,   FLAG_IN   | FLAG_START },
	{ "while", RES_WHILE, FLAG_DO   | FLAG_START },
	{ "until", RES_UNTIL, FLAG_DO   | FLAG_START },
	{ "in",    RES_IN,    FLAG_DO   },
	{ "do",    RES_DO,    FLAG_DONE },
	{ "done",  RES_DONE,  FLAG_END  }
};
```

if else这些相当于是保留关键字。

process_command_subs

handle_dollar

parse_stream

内置的命令

```
static struct built_in_command bltins[] = {
	{"bg", "Resume a job in the background", builtin_fg_bg},
	{"break", "Exit for, while or until loop", builtin_not_written},
	{"cd", "Change working directory", builtin_cd},
	{"continue", "Continue for, while or until loop", builtin_not_written},
	{"env", "Print all environment variables", builtin_env},
	{"eval", "Construct and run shell command", builtin_eval},
	{"exec", "Exec command, replacing this shell with the exec'd process",
		builtin_exec},
	{"exit", "Exit from shell()", builtin_exit},
	{"export", "Set environment variable", builtin_export},
	{"fg", "Bring job into the foreground", builtin_fg_bg},
	{"jobs", "Lists the active jobs", builtin_jobs},
	{"pwd", "Print current directory", builtin_pwd},
	{"read", "Input environment variable", builtin_read},
	{"return", "Return from a function", builtin_not_written},
	{"set", "Set/unset shell local variables", builtin_set},
	{"shift", "Shift positional parameters", builtin_shift},
	{"trap", "Trap signals", builtin_not_written},
	{"ulimit","Controls resource limits", builtin_not_written},
	{"umask","Sets file creation mask", builtin_umask},
	{"unset", "Unset environment variable", builtin_unset},
	{".", "Source-in and run commands in a file", builtin_source},
	{"help", "List shell built-in commands", builtin_help},
	{NULL, NULL, NULL}
};
```



参考资料

1、

https://stackoverflow.com/questions/5646749/how-to-make-if-and-comparison-statement-in-uboot

2、

https://lore.kernel.org/u-boot/20220331232716.241283-7-francis.laniel@amarulasolutions.com/T/

# mkbootimg逻辑

代码在这里：

output\a4_ba400_spk_a6432_release\build\android-tools-4.2.2+git20130218\core\mkbootimg\mkbootimg.c

结构体是这样：

```
#define BOOT_MAGIC "ANDROID!"
#define BOOT_MAGIC_SIZE 8
#define BOOT_NAME_SIZE 16
#define BOOT_ARGS_SIZE 512
struct boot_img_hdr
{
    unsigned char magic[BOOT_MAGIC_SIZE];

    unsigned kernel_size;  /* size in bytes */
    unsigned kernel_addr;  /* physical load addr */

    unsigned ramdisk_size; /* size in bytes */
    unsigned ramdisk_addr; /* physical load addr */

    unsigned second_size;  /* size in bytes */
    unsigned second_addr;  /* physical load addr */

    unsigned tags_addr;    /* physical addr for kernel tags */
    unsigned page_size;    /* flash page size we assume */
    unsigned unused[2];    /* future expansion: should be 0 */

    unsigned char name[BOOT_NAME_SIZE]; /* asciiz product name */
    
    unsigned char cmdline[BOOT_ARGS_SIZE];

    unsigned id[8]; /* timestamp / checksum / sha1 / etc */
};
```

头部的magic字符串是`ANDROID!`这8个字母。

然后依次放的是：

```
kernel的地址和长度
ramdisk的地址和长度
second的地址和长度
tags（kernel的）的地址
flash page的大小。
boot分区的名字，最多16个字符
cmdline，最多512字节。
8个字节的id，可以是校验码。
```

boot_header占据一个flash page的大小。

当前我们的--second传递的是dtb的内容。

为什么要这样把dtb打包进去呢？

我们的dtb不是单独的分区吗？

这个怎么理解？

我们这里传递的cmdline是这样：

```
BR2_TARGET_UBOOT_AMLOGIC_BOOTARGS="root=/dev/system rootfstype=squashfs init=/sbin/init"
```

这里打包的，跟uboot环境变量里的关系是什么？

mkbootimg的逻辑还是很简单直观的。

就是把几个文件拼接到一起，然后加上一个header信息。



参考资料

1、

https://blog.csdn.net/zangdongming/article/details/37969079

# 用未压缩内核Image

1、让运行地址，不等于链接地址。

```
tftp 0x21000000 Image; go 0x21000000
```

不能运行。



# 用压缩内核zImage

1、让运行地址，不等于链接地址。

```
tftp 0x21000000 Image; go 0x21000000
```

可以解压成功。因为解压代码是地址无关的。

解压后的内核不能运行。

2、让运行地址，等于链接地址。

```
tftp 0x20008000 Image; go 0x20008000
```



对于不是用gzip压缩的内核，bootm命令会先判断bootm xxx这个xxx地址跟mkimage的-a参数指定的地址一样。

如果一样，就原封不动放在那里。

如果不一样，就会从xxx这个地址提取64字节 头部。把去掉头部的内部，复制到-a指定的地址上运行。



**bootm** 用于将内核镜像加载到[内存](https://so.csdn.net/so/search?q=内存&spm=1001.2101.3001.7020)的指定地址处，

如果有需要还要解压镜像，

然后根据操作系统和体系结构的不同给内核传递不同的启动参数，最后启动内核。



# Image和zImage区别

内核编译（make）之后会生成两个文件，

一个Image，一个zImage，

其中Image为内核映像文件，而zImage为内核的一种映像压缩文件，

Image大约为4M，而zImage不到2M。

那么uImage又是什么的？

它是uboot专用的映像文件，

**它是在zImage之前加上一个长度为64字节的“头”，**

说明这个内核的版本、加载位置、生成时间、大小等信息；

其0x40之后与zImage没区别。

如何生成uImage文件？

首先在uboot的/tools目录下寻找mkimage文件，

把其copy到系统/usr/local/bin目录下，这样就完成制作工具。

然后在内核目录下运行make uImage，

如果成功，便可以在arch/arm/boot/目录下发现uImage文件，其大小比zImage多64个字节。

其实就是一个自动跟手动的区别,有了uImage头部的描述,u-boot就知道对应Image的信息,如果没有头部则需要自己手动去搞那些参数。



zImage是ARM Linux常用的一种压缩映像文件，

uImage是U-boot专用的映像文件，

它是在zImage之前加上一个长度为0x40的“头”，

说明这个映像文件的类型、加载位置、生成时间、大小等信息。

换句话说，如果直接从uImage的0x40位置开始执行，zImage和uImage没有任何区别。

另外，Linux2.4内核不支持uImage，Linux2.6内核加入了很多对嵌入式系统的支持，但是uImage的生成也需要设置，这个以后我会介绍。

一般情况下都在生成vmlinux后，再对内核进行压缩成为zImage，压缩的目录是

kernel/arch/arm/boot。

但是我们没有压缩。

看看我们的编译命令是啥？

```
BR2_LINUX_KERNEL_ANDROID_FORMAT=y
BR2_LINUX_KERNEL_IMAGE=y
```

没有定义

```
BR2_LINUX_KERNEL_UIMAGE
BR2_LINUX_KERNEL_ZIMAGE
```

是这个分支

```
ifeq ($(BR2_LINUX_KERNEL_IMAGE_NOGZIP),y)
  LINUX_IMAGE_NAME = Image
else
  LINUX_IMAGE_NAME = Image.gz
endif
```

```
LINUX_TARGET_NAME = $(LINUX_IMAGE_NAME)
```

那么相当于是make Image.gz

有这样的一个target。在arch\arm64\boot\Makefile

```
$(obj)/Image.gz: $(obj)/Image FORCE
	$(call if_changed,gzip)
```

有这些target可以生成

```
targets := Image Image.bz2 Image.gz Image.lz4 Image.lzma Image.lzo
```

BR2_LINUX_KERNEL_APPENDED_DTB 这个选项没有使能。

所以dtb文件没有append在Image文件的后面。

我们也没有使能这个：

```
# BR2_LINUX_KERNEL_GKI is not set
```

BR2_LINUX_KERNEL_BOOTIMAGE_OFFSET 

这个配置项有什么作用？

BR2_LINUX_KERNEL_APPENDED_DTB 我们当前的方案，也不适合打开这个选项。

那就把dtb单独放分区吧。分区大小可以给小一点。

关于rootfs.cpio的部分，

```
ifeq ($(BR2_TARGET_ROOTFS_CPIO_GZIP),y)
	ROOTFS_CPIO = rootfs.cpio.gz
```

```
linux-rebuild-with-initramfs: $(BINARIES_DIR)/$(ROOTFS_CPIO)
```

# bootm涉及的数据结构

在 bootm 中常用的数据结构有 **image_info_t** 和 **bootm_headers_t**，

```

/* 镜像信息 */
typedef struct image_info {
	ulong       start, end;             /* start/end of blob */
	ulong       image_start, image_len; /* start of image within blob, len of image */
	ulong       load;                   /* load addr for the image */
	uint8_t     comp, type, os;         /* compression, type of image, os type */
} image_info_t;


```

```
/* bootm 头 */
typedef struct bootm_headers {
	image_header_t  *legacy_hdr_os;		/* 指向镜像头的指针 */
	image_header_t  legacy_hdr_os_copy;	/* 镜像头的备份 */
	ulong           legacy_hdr_valid;   /* 镜像头存在标记 */
 
	image_info_t    os;                 /* 系统镜像信息 */
	ulong           ep;		            /* 系统入口地址 */
	ulong           rd_start, rd_end;   /* 虚拟磁盘起始地址 */
	ulong           ft_len;             /* 平坦设备树的长度 */
	ulong           initrd_start;
	ulong           initrd_end;
	ulong           cmdline_start;
	ulong           cmdline_end;
	bd_t            *kbd;
	int             verify;             /* getenv("verify")[0] != 'n' */
 
#define BOOTM_STATE_START       (0x00000001)
#define BOOTM_STATE_LOADOS      (0x00000002)
#define BOOTM_STATE_RAMDISK     (0x00000004)
#define BOOTM_STATE_FDT         (0x00000008)
#define BOOTM_STATE_OS_CMDLINE  (0x00000010)
#define BOOTM_STATE_OS_BD_T     (0x00000020)
#define BOOTM_STATE_OS_PREP     (0x00000040)
#define BOOTM_STATE_OS_GO       (0x00000080)
	int             state;              /* 状态标记 */
 
	struct lmb	lmb;		            /* 逻辑内存块 */
} bootm_headers_t;
```

# bootm函数分析

bootm 的主函数为 do_bootm，代码如下

```

```

我们的uboot代码里，有2个bootm.c文件。

common/bootm.c

cmd/bootm.c

那么我们具体用的哪一个？

还有一个bootm_os.c文件。

```
obj-$(CONFIG_CMD_BOOTM) += bootm.o bootm_os.o
```

配置就这个：

```
CONFIG_CMD_BOOTM=y
```

所以这2个bootm.c都编译了。

cmd/bootm.c这个里面才定义了命令。cmd/bootm.c调用了common/bootm.c里的函数。是这样的关系。

# uImage的格式：Legacy-uImage和FIT-uImage

uImage有两种格式。

- Legacy-uImage
  对于Legacy-uImage，我们需要另外加载ramdisk和fdt到RAM上面。
  执行的命令如下

```
假设Legacy-uImage的加载地址是0x20008000，ramdisk的加载地址是0x21000000，fdt的加载地址是0x22000000

(1) 只加载kernel的情况下
bootm 0x20008000

(2) 加载kernel和ramdisk
bootm 0x20008000 0x21000000

(3) 加载kernel和fdt
bootm 0x20008000 - 0x22000000

(4) 加载kernel、ramdisk、fdt
bootm 0x20008000 0x21000000 0x22000000
```

- FIT-uImage
  对于FIT-uImage，kernel镜像、ramdisk镜像和fdt都已经打包到FIT-uImage的镜像中了。
  执行的命令如下

```text
假设FIT-uImage的加载地址是0x30000000，启动kernel的命令如下：
bootm 0x30000000
```

# imgread kernel

这个命令读取boot.img时，做了什么？



# 参考资料

1、uboot 命令分析(一) — bootm

https://blog.csdn.net/g_salamander/article/details/8463854

2、[uboot] uboot启动kernel篇（二）——bootm跳转到kernel的流程

这个系列不错

https://blog.csdn.net/ooonebook/article/details/53495021

3、Image和zImage区别

https://blog.csdn.net/u014379540/article/details/51900906