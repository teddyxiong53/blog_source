---
title: amlogic之bootloader不同阶段分析
date: 2021-11-04 11:00:25
tags:
	- amlogic

---

--

在uboot-repo目录下，有这些子目录。

```
bl2
	这个下面只有bin文件，按不同芯片分类放好的。
bl30
	有一个bin目录，也是按芯片放好的。
	下面还有一个src_ao，感觉是freertos的代码。
bl31
	部分芯片有，axg的没有。一些bin文件。
bl31_1.3
	这个里面有axg的。
bl32
	空的。
bl32_3.8
	部分芯片有。
bl33
	这个就是uboot的源代码。
bl40
	bin文件，部分芯片有。
fip
	一些脚本。
soc
	一些bin文件，部分芯片有。
```

怎么编译组装起来的？

手动编译，靠uboot-repo/mk这个脚本来执行。

./mk --config 

查看所有的板子。

这个信息从哪里来的？

mk脚本，实际调用的fip/mk_script.sh脚本。

mk_script.sh脚本的内容

```
source fip/check_compile.sh
source fip/variables.sh
source fip/lib.sh
source fip/build_bl2.sh
source fip/build_bl30.sh
source fip/build_bl31.sh
source fip/build_bl32.sh
source fip/build_bl33.sh
source fip/build_bl40.sh
```

check_compile.sh脚本

```
对外输出一个函数：check_compile
```

用法：

```
#usage:
#
#./check_compile.sh            -check amlogic board configs
#./check_compile.sh cus        -check customer board configs
#./check_compile.sh all        -check both amlogic and customer boards
```

这个目录的情况：

```
bl33/v2015/board/amlogic/axg_s400_v1$ tree
.
├── aml-user-key.sig
├── axg_s400_v1.c
├── eth_setup.c
├── firmware
│   ├── board_init.c
│   ├── power.c
│   ├── ramdump.c
│   ├── ramdump.h
│   ├── scp_task
│   │   ├── dvfs_board.c
│   │   ├── pwm_ctrl.h
│   │   └── pwr_ctrl.c
│   └── timing.c
├── Kconfig
├── lcd.c
└── Makefile
```



编译axg_s400_v1看看。

输出是在build目录下。内容：

```
├── u-boot.bin
├── u-boot.bin.encrypt
├── u-boot.bin.encrypt.efuse
├── u-boot.bin.encrypt.sd.bin
├── u-boot.bin.encrypt.usb.bl2
├── u-boot.bin.encrypt.usb.tpl
├── u-boot.bin.sd.bin
├── u-boot.bin.usb.bl2
└── u-boot.bin.usb.tpl
```

build函数的流程

```
1、clean
	看是不是存在v2015和v2019的目录，存在的话，进去，执行make distclean
	删除build目录。
2、编译uboot的代码
3、	对于这几个，有代码就编译，没有就拷贝bin文件。
	# bl2/bl30/bl31..etc, build or copy from bin.git
	build_blx $@
4、package
	打包。这个是关键，看看怎么做的。
	这个是在不同的芯片目录下。每个芯片的打包都不同。
	init_vari $@
	build_fip $@
	encrypt $@
```



```
Get bl2 from bl2/bin... done
Get bl30 from bl30/bin... done
Get bl31 from bl31_1.3/bin... done
Amlogic img found, use new FIP structure!
Creating "fip/_tmp/fip.bin"
Firmware Image Package ToC:
---------------------------
- SCP Firmware BL3-0: offset=0x4000, size=0xD400
- EL3 Runtime Firmware BL3-1: offset=0x14000, size=0x311B8
- Non-Trusted Firmware BL3-3: offset=0x48000, size=0x145848
---------------------------
Bootloader build done!
```

amlogic bootloader包含BL2，BL30，BL31，BL32，BL33几个部分，打包到u-boot.bin中，

其中BL30 是power相关aop image，BL32 为TEE kernel image。



参考资料

1、bl2开机阶段总结

https://confluence.amlogic.com/pages/viewpage.action?pageId=100805987&preview=%2F100805987%2F107825740%2FBL2%E5%BC%80%E6%9C%BA%E9%98%B6%E6%AE%B5%E6%80%BB%E7%BB%93.pdf

2、

https://confluence.amlogic.com/pages/viewpage.action?pageId=100805987