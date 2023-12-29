---
title: yocto使用external-prebuilt-toolchain的方法
date: 2023-12-21 16:41:28
tags:
	- yocto
---

--

根据这篇文章来学习总结

https://elinux.org/images/c/c8/ExternalToolchainsInYocto.pdf

常用的第三方二进制工具链有2个：

1、CodeSourcery。

2、Linaro。

我们基本用Linaro。所以就看Linaro的。



TCMODE变量

# 使用Linaro

linaro的layer

```
git://git.linaro.org/openembedded/meta-linaro.git
```

TCMOD设置：

```
TCMODE = “external-linaro”
```

EXTERNAL_TOOLCHAIN变量设置

```
EXTERNAL_TOOLCHAIN = “/path/to/linaro”
```





# 搭建yocto的官方环境

参考这个：

https://docs.yoctoproject.org/brief-yoctoprojectqs/index.html

```
git clone git://git.yoctoproject.org/poky
```

我就切到这个版本：

```
cd poky
git checkout -t remotes/origin/kirkstone
git pull
```

初始化环境：

```
source oe-init-build-env build-min
```

后面跟的参数是build dir。

这样就可以把不同的编译目录分开。

方便在一个目录做多个实验。

我先把工具链

看看source的日志。

```
You had no conf/local.conf file. This configuration file has therefore been
created for you from /mnt/fileroot/hanliang.xiong/work/yocto-study/code/poky/meta-poky/conf/local.conf.sample
```

判断文件不存在，这样直接拷贝过去的：

```
 cp -f "$OECORELOCALCONF" "$BUILDDIR/conf/local.conf"
```

如果"$BUILDDIR/conf/bblayers.conf"也不存在。那么这样用sed把模板改一下：

```
sed -e "s|##OEROOT##|$OEROOT|g" \
        -e "s|##COREBASE##|$OEROOT|g" \
        "$OECORELAYERCONF" > "$BUILDDIR/conf/bblayers.conf"
```

目前我的layer是这样：

```
BBLAYERS ?= " \
  /mnt/fileroot/hanliang.xiong/work/yocto-study/code/poky/meta \
  /mnt/fileroot/hanliang.xiong/work/yocto-study/code/poky/meta-poky \
  /mnt/fileroot/hanliang.xiong/work/yocto-study/code/poky/meta-yocto-bsp \
  "
```

最后会cat打印poky\meta\conf\conf-notes.txt 这个文件里的内容：

```
### Shell environment set up for builds. ###

You can now run 'bitbake <target>'

Common targets are:
    core-image-minimal
    core-image-full-cmdline
    core-image-sato
    core-image-weston
    meta-toolchain
    meta-ide-support

You can also run generated qemu images with a command like 'runqemu qemux86-64'.

Other commonly useful commands are:
 - 'devtool' and 'recipetool' handle common recipe tasks
 - 'bitbake-layers' handles common layer tasks
 - 'oe-pkgdata-util' handles common target package tasks

```

这个有涉及到883个bb文件。

```
Parsing of 883 .bb files
```

编译完之后，直接在tmp/deploy目录下执行runqemu命令：

```
runqemu - INFO - Running bitbake -e ...
runqemu - INFO - Continuing with the following parameters:
KERNEL: [/mnt/fileroot/hanliang.xiong/work/yocto-study/code/poky/build-min/tmp/deploy/images/qemux86-64/bzImage]
MACHINE: [qemux86-64]
FSTYPE: [ext4]
ROOTFS: [/mnt/fileroot/hanliang.xiong/work/yocto-study/code/poky/build-min/tmp/deploy/images/qemux86-64/core-image-minimal-qemux86-64-20231221120621.rootfs.ext4]
CONFFILE: [/mnt/fileroot/hanliang.xiong/work/yocto-study/code/poky/build-min/tmp/deploy/images/qemux86-64/core-image-minimal-qemux86-64-20231221120621.qemuboot.conf]
```

poky\build-min\tmp\deploy\images\qemux86-64\core-image-minimal-qemux86-64.testdata.json

这个json文件里的信息值得读一下。

## 编译qemuarm64的环境

```
source oe-init-build-env build-arm64
```

然后在build-arm64下面，手动修改conf/local.conf文件。

把MACHINE改成qemuarm64的。

同时让downloads目录指向公共的下载目录。避免重复下载。

```
ln -s ../downloads ./
```

编译：

```
bitbake core-image-minimal
```

生成的local.conf文件，是可以手动修改的。

例如我现在要编译qemuarm64的，就需要在local.conf里修改：

```
MACHINE ?= "qemuarm64"
```

然后bitbake core-image-minimal

work目录下生成了这些目录：

```
all-poky-linux  cortexa57-poky-linux  qemuarm64-poky-linux  x86_64-linux
```

# 使用meta-linaro做external toolchain编译qemuarm64

把对应的meta下载下来：

```
git clone https://github.com/lmp-mirrors/meta-linaro
```

跟poky在同一个目录层级。

需要在

```
TCMODE = “external-linaro”
EXTERNAL_TOOLCHAIN = “/path/to/linaro”
```

但是这些工具链文件怎么下载存放呢？



我开始将现有的 Linux 系统移植到最新的 yocto 基础上。

这硬件基于 TI am 335x。

我想使用外部 linaro 工具链。由于我使用现有的 3.2linux 内核以及旧的 u-boot，我创建了自己的机器和发行版配置。

我成功地构建并运行了目标，到目前为止一切顺利。

为了合并我添加的外部工具链



```
> TCMODE = "external-linaro"
>
> EXTERNAL_TOOLCHAIN =
> "/<homedir>/gcc-linaro-5.1-2015.08-x86_64_arm-linux-gnueabihf"
```

meta-linaro/meta-linaro-toolchain

这里有个例子：

https://wiki.koansoftware.com/index.php/Setup_an_external_toolchain_with_Yocto

```
TCLIBC = "external-linaro-toolchain"
TCMODE = "external-linaro"
EXTERNAL_TOOLCHAIN = "/home/koan/altera-linux/linaro/gcc-linaro-arm-linux-gnueabihf-4.7-2012.11-20121123_linux"
```

我先就这样配置，然后直接编译看看。

```
source oe-init-build-env build-arm64-ext-tc
```

修改local.conf的内容：

```
TCLIBC = "external-linaro-toolchain"
TCMODE = "external-linaro"
EXTERNAL_TOOLCHAIN = "/mnt/fileroot/hanliang.xiong/work/a113x2/code5/toolchain/gcc/linux-x86/aarch64/gcc-linaro-7.3.1-2018.05-x86_64_aarch64-linux-gnu/"

```

直接编译，报错了：

```
/mnt/fileroot/hanliang.xiong/work/yocto-study/code/poky/meta/conf/distro/defaultsetup.conf:6: Could not include required file conf/distro/include/tcmode-external-linaro.inc
```

那么看起来就要把对应的layer添加到bblayers里去。

这样添加一下：

```
bitbake-layers add-layer ../../meta-linaro/meta-linaro
```

报错了：

```
ERROR: Layer 'linaro' depends on layer 'networking-layer', but this layer is not enabled in your configuration
ERROR: Parse failure with the specified layer added, exiting.
```

看起来是依赖了networking-layer，

那应该是对应这个。

https://layers.openembedded.org/layerindex/branch/master/layer/meta-networking/

该层旨在成为网络相关的中心点包和配置。

它应该直接在上面有用oe-core 并补充了元开放嵌入式。主要应该是有用的给以下团体：

\- 任何构建小型网络设备的人（例如家庭路由器/桥/开关）。

\- 任何想要向其设备添加网络服务的人（例如任何可能受益于小型 ftp/tftp 服务器的事物）

来自于meta-openembedded这个层。

所以要下载这个。

下载除了poky之外的层就慢慢增加了。那就需要参考yoe的做法。

yoe是怎么生成bblayers.conf的。

它是提前手动写好的。

然后发现我当前的meta-linaro的分支是daisy。这个是比较老的。

所以我所有的仓库，都切换到kirkstone的分支，避免出现奇怪的问题。

```
git checkout -t remotes/origin/kirkstone
```

再手动下载openembedded仓库。

```
git clone https://github.com/openembedded/meta-openembedded
```

手动把bblayers.conf改成这样：

```
BBLAYERS ?= " \
  /mnt/fileroot/hanliang.xiong/work/yocto-study/code/poky/meta \
  /mnt/fileroot/hanliang.xiong/work/yocto-study/code/poky/meta-poky \
  /mnt/fileroot/hanliang.xiong/work/yocto-study/code/poky/meta-yocto-bsp \
  /mnt/fileroot/hanliang.xiong/work/yocto-study/code/meta-linaro/meta-linaro \
  /mnt/fileroot/hanliang.xiong/work/yocto-study/code/meta-openembedded/meta-networking \
  /mnt/fileroot/hanliang.xiong/work/yocto-study/code/meta-openembedded/meta-filesystems \
  /mnt/fileroot/hanliang.xiong/work/yocto-study/code/meta-openembedded/meta-initramfs \
  /mnt/fileroot/hanliang.xiong/work/yocto-study/code/meta-openembedded/meta-multimedia \
  /mnt/fileroot/hanliang.xiong/work/yocto-study/code/meta-openembedded/meta-oe \
  /mnt/fileroot/hanliang.xiong/work/yocto-study/code/meta-openembedded/meta-perl \
  /mnt/fileroot/hanliang.xiong/work/yocto-study/code/meta-openembedded/meta-python \
  "
```

然后再把external那3个变量加到local.conf里来看看。

还是不对：

```
poky/meta/conf/distro/defaultsetup.conf:6: Could not include required file conf/distro/include/tcmode-external-linaro.inc
```

搜索不到tcmode-external-linaro.inc这个文件。

以tcmode开头的inc文件，也只有tcmode-default.inc这个默认的。

切换到daisy分支，至少是有这个文件的：

```
./meta-linaro-toolchain/conf/distro/include/tcmode-external-linaro.inc
```

daisy是1.6的版本，很老了。

zeus是3.0的版本，也有。

为什么kirkstone没有呢？

master也是没有的。

这个就很坑爹了。

那感觉linaro的方式不行了。

那试一下external-arm-toolchain的看看。



如果 TCMODE 设置为“默认”以外的值，则您有责任确保工具链与默认工具链兼容。

使用这些组件的旧版本或新版本可能会导致构建问题。

请参阅您的 Yocto 项目版本的发行信息，以查找工具链必须兼容的特定组件。



试一下这个

https://github.com/MentorEmbedded/meta-sourcery/

这个最近几个月还在更新。所以还可用。

但是sourcery的工具链好像不怎么提供了。

那就直接找arm工具链了。

下载这个：

```
git clone https://git.yoctoproject.org/meta-arm
```

切换到kirkstone分支。

编译，报错：

```
Could not include required file conf/distro/include/tclibc-external-arm-toolchain.inc
```

*TCLIBC* 用默认的。

现在可以进行编译。

从日志看：

```
gcc-source-arm-11.2-arm-11.2-r2022.02 do_fetch 
```

那是有进行下载这个工具链。

这个版本是meta-arm里的。

那这个下载的，跟我指定的，是什么关系呢？用哪个呢？

编译出来了。看看一些日志文件。

```
poky\build-arm64-ext-tc\tmp\work-shared\gcc-arm-11.2-r2022.02\temp\log.do_fetch
```



```
DEBUG: Fetching https://developer.arm.com/-/media/Files/downloads/gnu/11.2-2022.02/srcrel/gcc-arm-src-snapshot-11.2-2022.02.tar.xz using command '/usr/bin/env wget -t 2 -T 30 --passive-ftp -P /mnt/fileroot/hanliang.xiong/work/yocto-study/code/poky/build-arm64-ext-tc/downloads 'https://developer.arm.com/-/media/Files/downloads/gnu/11.2-2022.02/srcrel/gcc-arm-src-snapshot-11.2-2022.02.tar.xz''

```



# 思考

现在的思路就是先把单纯的环境研究透彻。

然后测试自己在poky的基础上添加layer。

现在可以看看我们是怎么加的layer。

我们的source脚本做了哪些不同的事情。

我们是靠sed来修改local.conf里的内容的。

我们在自己的meta-xx下面，有自己的local.conf.sample和bblayers.conf.sample模板。

所以这个layer是手动指定的？



我看yoe的rpi的编译结果里，怎么没有看到local.conf和bblayers.conf文件呢？

conf\projects\rpi4-64\layers.conf

这个是预定义的文件。

看看yoe的逻辑又是怎样的。

BBLAYERS里的变量的先后顺序没有任何意义。

可以从上到下，也可以从下到上，总体保持一个规律就好。没有规律应该也没有关系。



meta-toolchain

这个怎么理解？



添加一个layer

```
bitbake-layers add-layer ../meta-altera
```



```
bitbake-layers create-layer meta-mylayer
```



一个bsp的典型目录：

```
meta-bsp_root_name/
meta-bsp_root_name/bsp_license_file
meta-bsp_root_name/README
meta-bsp_root_name/README.sources
meta-bsp_root_name/binary/bootable_images
meta-bsp_root_name/conf/layer.conf
meta-bsp_root_name/conf/machine/*.conf
meta-bsp_root_name/recipes-bsp/*
meta-bsp_root_name/recipes-core/*
meta-bsp_root_name/recipes-graphics/*
meta-bsp_root_name/recipes-kernel/linux/linux-yocto_kernel_rev.bbappend
```



==机器文件将 BSP 中其他位置包含的所有信息绑定在一起，形成构建系统可以理解的格式。==

每个 BSP 层==至少需要一个机器文件。==

如果BSP支持多机，则可以存在多机配置文件。

这些文件名对应于用户设置 MACHINE 变量的值。

这些文件定义了诸如要使用的内核包（虚拟/内核的 PREFERRED_PROVIDER）、要包含在不同类型映像中的硬件驱动程序、所需的任何特殊软件组件、任何引导加载程序信息以及任何特殊映像格式要求等内容。



该配置文件还可以包括硬件“tuning”文件，

该文件通常用于定义包架构并指定优化标志，

这些优化标志经过精心选择，以便在给定处理器上提供最佳性能。

调整文件位于源目录内的meta/conf/machine/include 目录中。

例如，许多tune-*文件（例如tune-arm1136jf-s.inc、tune-1586-nlp.inc等）驻留在poky/meta/conf/machine/include目录中。



# qemuarm和qemuarm64比较

| 不同点           | arm                       | arm64                     |
| ---------------- | ------------------------- | ------------------------- |
| 包含的文件       | armv7a/tune-cortexa15.inc | armv8a/tune-cortexa57.inc |
| KERNEL_IMAGETYPE | zImage                    | Image                     |
| UBOOT_MACHINE    | qemu_arm_defconfig        | qemu_arm64_defconfig      |
| QB_SYSTEM_NAME   | qemu-system-arm           | qemu-system-aarch64       |
| QB_MACHINE       | -machine virt,highmem=off | -machine virt             |
| QB_CPU           |                           |                           |
|                  |                           |                           |

## qemu.inc的内容

| 变量                                            | 值                                   |
| ----------------------------------------------- | ------------------------------------ |
| PREFERRED_PROVIDER_virtual/egl和其他libgles1到4 | 都是mesa                             |
| MACHINE_FEATURES                                | alsa bluetooth usbgadget screen vfat |
| MACHINEOVERRIDES                                | qemuall                              |
| IMAGE_FSTYPES                                   | tar.bz2 ext4                         |
| IMAGE_CLASSES                                   | qemuboot                             |

## tune-cortexa15.inc

| 变量          | 值                |
| ------------- | ----------------- |
| DEFAULTTUNE   | cortexa15thf-neon |
| TUNE_FEATURES |                   |
|               |                   |
|               |                   |
|               |                   |
|               |                   |
|               |                   |



| 变量          | 值                           |
| ------------- | ---------------------------- |
| DEFAULTTUNE   | cortexa15thf-neon            |
| TUNE_FEATURES | aarch64 armv8a crc cortexa57 |



tune是可选的微调。可以都不要的。



# poky\meta\conf\machine\include\arm\README说明

ARM 架构的定义分布在多个文件中。

主要的变量定义由核心的 `arch-arm.inc` 文件处理。

`TUNE_ARCH` 被设置为 "arm" 或 "armeb"，==取决于给定 `tune` 中是否存在 "bigendian" 特性的值。==

一小部分特定于 ARM 的变量已被定义，

以允许自动定义 `TUNE_PKGARCH`。

优化的调整不能改变 `TUNE_PKGARCH` 的定义。

`TUNE_PKGARCH:tune-<tune>` 将被忽略。

`TUNE_PKGARCH` 的格式是由 `TUNE_PKGARCH` 默认值强制定义的。

格式必须是这样的形式：

`<armversion>[t][e][hf][b][-vfp][-neon]`

`TUNE_PKGARCH` 被定义为：
`${ARMPKGARCH}${ARMPKGSFX_THUMB}${ARMPKGSFX_DSP}${ARMPKGSFX_EABI}${ARMPKGSFX_ENDIAN}${ARMPKGSFX_FPU}`

- `ARMPKGARCH`：这是由每个 `tuning` 指定的核心包架构组件。这是一个 tuning 的主要标识符。通常的值有：arm、armv4、armv5、armv6、armv7a 等。

- `ARMPKGSFX_THUMB`：这是 Thumb 特定的后缀。目前在 `feature-arm-thumb.inc` 文件中定义。

- `ARMPKGSFX_DSP`：这是 DSP 特定的后缀。目前当在 armv5 上启用了 dsp 特性时，它被设置为 'e'。

- `ARMPKGSFX_EABI`：这是 EABI 特定的后缀。目前有两个定义的 ABI，标准的 EABI 和 Hard Float（VFP）EABI。当启用了 `callconvention-hard` 时，指定为 "hf"，否则为空白。

- `ARMPKGSFX_ENDIAN`：这是 endian 特定的后缀。它在 `arch-arm.inc` 文件中定义。

- `ARMPKGSFX_FPU`：这是 FPU 特定的后缀。后缀表示特定的 FPU 优化。'vfp' 和 'neon' 都有定义。

这些解释描述了 Yocto 中 ARM 架构的一些关键变量和后缀的含义，用于指定不同调整中的不同特性和优化选项。



# -mcpu和-march的关系是什么

```
export CC="aarch64-poky-linux-gcc  -mcpu=cortex-a57 -march=armv8-a+crc -mbranch-protection=standard -fstack-protector-strong  -O2 -D_FORTIFY_SOURCE=2 -Wformat -Wformat-security -Werror=format-security --sysroot=/mnt/fileroot/hanliang.xiong/work/yocto-study/code/poky/build-arm64/tmp/work/qemuarm64-poky-linux/core-image-minimal/1.0-r0/recipe-sysroot"
```

`-mcpu` 和 `-march` 是 GCC 编译器中用于指定目标 CPU 架构和所需优化级别的选项。

- **`-mcpu`**：这个选项用于指定要生成代码的目标处理器。它会优化生成的代码以适应指定的 CPU。在给定架构的情况下，`-mcpu` 允许你更精确地选择要生成代码的目标处理器型号。例如，`-mcpu=cortex-a57` 将使用适合 Cortex-A57 处理器的优化级别。

- **`-march`**：这个选项用于指定生成代码的目标体系结构。它设置生成的代码遵循的架构标准。在指定的体系结构中，可以使用 `-march=armv8-a` 来指定生成 ARMv8-A 架构的代码，`+crc` 表示生成代码要包含 CRC 指令支持。

在许多情况下，`-march` 和 `-mcpu` 可以一起使用，`-march` 指定了生成的代码要遵循的架构标准，而 `-mcpu` 则更具体地指定了目标处理器型号。通常情况下，指定 `-march` 会隐含地设置好了 `-mcpu`。但在一些情况下，如果需要更具体的优化或指定不同的处理器型号，可以使用 `-mcpu` 来进一步定义目标处理器。

# poky\meta-poky\conf\distro\poky-tiny.conf

```
DISTRO = "poky-tiny"
DISTROOVERRIDES = "poky:poky-tiny"
TCLIBC = "musl"
```

这个用的是musl c库。

# poky\meta-skeleton\recipes-kernel\linux\linux-yocto-custom.bb

自己是自定义kernel的编译。





https://stackoverflow.com/questions/62517431/how-to-use-external-toolchain-with-yocto

# meta-linaro分析



```
BBFILE_COLLECTIONS=" core yocto yoctobsp"
```



# meta-linaro\meta-linaro-toolchain\conf\distro\include\tcmode-external-linaro.inc

```
ELT_TARGET_SYS_arm ?= "arm-linux-gnueabihf"
ELT_TARGET_SYS_aarch64 ?= "aarch64-linux-gnu"
```

