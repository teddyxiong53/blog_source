---
title: rockchip的Linux开发包分析
date: 2018-10-11 13:57:51
tags:
	- Linux

---



RK3308的开发包是基于buildroot来做的。 

从使用上来看，编译比较简单，分两步：

1、设置环境。

```
./envsetup.sh 
```

根据提示，选择要编译的版本。例如我们选择32位的release版本。rockchip_rk3308_32_release

2、编译。

```
./build.sh
```

这个脚本可以带一个参数，参数是要编译的模块的名字。

envsetup.sh的结果是，

```
make -C /home/hlxiong/work/rk3308/buildroot O=/home/hlxiong/work/rk3308/buildroot/output/rockchip_rk3308_32_release 
```

我们看看这个Makefile里怎么写的。

这个Makefile是被自动生成的，里面的修改没用。

被buildroot/support/scripts/mkmakefile生成。

我们找到rockchip_rk3308_32_release_defconfig这个配置文件。

在这里./buildroot/configs/rockchip_rk3308_32_release_defconfig。

配置项大概80条。

我们再看build.sh脚本。

如果没有参数，就是build all和save all。

```
if [ ! -n "$1" ];then
	echo "build all and save all as default"
	BUILD_TARGET=allsave
else
	BUILD_TARGET="$1"
	NEW_BOARD_CONFIG=$TOP_DIR/device/rockchip/$RK_TARGET_PRODUCT/$1
fi
```

增量编译做得很好。

配置项在device/rockchip/.BoardConfig.mk里。



文档也写得比较齐全。

buildroot下的编译。

```
source buildroot/build/envsetup.sh
```

build.sh

```
该脚本会自动配置环境变量， 编译 U-Boot， 编译 Kernel， 编译 Buildroot， 编译 Recovery
继而生成固件。
```



rockchip默认的发布包没有详细的芯片手册。

网上找到一个RK3328的TRM手册。是详细的芯片手册。大概650页。

一共分为27章。

目录如下：

```
1、系统概览
	1.1 地址映射
		支持从内部bootrom启动，支持remap。remap被SGRF_SOC_CON2[0]控制。
		如果设置为1，那么bootrom映射到0xff08 0000，内部sram被映射到0xffff 0000
		从0到0xff00 0000，都是ddr的区域。寄存器都是在0xff00 0000这里往上的16M空间内。
	1.2 系统启动
		支持sd卡、emmc、nand、nor这些介质启动。
	1.3 中断
		提供了一个gic，有128个SPI（共享外设中断）。有3个PPI（私有外设中断）。
		中断是高电平触发，不是可编程的。
		中断号从32开始，到144结束。
	1.4 dma硬件请求连接
		提供了一个dma控制器。也是高电平触发，不可编程。
		
2、时钟和复位单元。Clock & Reset Unit，简称CRU
	寄存器非常多。用到了0x39c。
3、通用寄存器文件。General Register File。GRF
	grf分为4种：
        1、普通的。
        2、ddr grf
        3、usb2phy grf
        4、usb3phy grf
	功能包括：
		1、io复用。
		2、控制gpio的状态，在power-down模式下。
		3、gpio上拉下拉控制。
		4、系统控制。
		5、系统状态。
		
4、Context-A53
	4核心的A53 。256K的L2 Cache。
	
5、内置sram。
	36K大小。
6、pmu。
7、gic。
8、DMA Controller。
9、温度传感器ADC（TSADC）
10、SARADC
11、系统调试。
12、efuse
13、看门狗
14、timer
15、Transport Stream Processing(TSP)
16、pwm
17、uart
18、gpio
19、i2c
20、spi
21、spdif 
22、gmac 以太网
23、pdm
24、Smart Card Reader（SCR）
25、i2s和pcm
26、gpu
27、视频DAC
```

