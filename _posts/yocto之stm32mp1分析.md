---
title: yocto之stm32mp1分析
date: 2023-12-29 13:49:28
tags:
	- yocto
---

--

安装yocto需要的基础工具：

```
sudo apt install -y bc build-essential chrpath cpio diffstat gawk git python texinfo wget gdisk
```

下载代码：

```
pushd ${HOME}/yocto-stm32-labs
git clone -b dunfell-23.0.7 git://git.yoctoproject.org/poky.git
popd
git clone -b dunfell git://git.openembedded.org/meta-openembedded
git clone -b dunfell https://github.com/STMicroelectronics/meta-st-stm32mp.git
```

初始化yocto环境：

```
cd ${HOME}/yocto-stm32-labs
source poky/oe-init-build-env
```

加入stm32mp的layer

```
bitbake-layers add-layer ../meta-openembedded/meta-oe
bitbake-layers add-layer ../meta-openembedded/meta-python
bitbake-layers add-layer ../meta-st-stm32mp
```

修改local.conf里的MACHINE

```
# 修改目標機器
sed -i 's/^MACHINE.*/MACHINE ?= "stm32mp1"/g' conf/local.conf
```



参考资料

1、

https://e61983.github.io/2021-08-11-stm32mp-with-yocto/

https://e61983.github.io/categories/embedded-system/