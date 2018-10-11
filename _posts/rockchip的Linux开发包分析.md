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

