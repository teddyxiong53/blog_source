---
title: amlogic之buildroot config配置体系分析
date: 2021-11-01 11:11:25
tags:
	- amlogic

---

--

amlogic的buildroot配置，使用了include的机制，进行层级嵌套。

这个默认的buildroot是不支持的。看看是怎么实现的。

怎么展开处理的？

以s400的为例。

最外层的文件就是：configs/axg_s400_sbr_a6432_release_defconfig

内容是：

```
#----------------------------------------------------------#
#include "arch_a6432_6.3.1.config"

#----------------------------------------------------------#
#include "a113_s400_PurelySBR.config"
#include "flash_nand_2k.config"
BR2_TARGET_ROOTFS_INITRAMFS_LIST="board/amlogic/common/initramfs/initramfs-49/ramfslist-32-ubi-release"
```

那就还是要从最外层的配置说起。

source setupenv.sh axg

然后选择需要的板子。

就可以生成一个.config文件。

.confg，就是把各个嵌套的include的配置展开后得到的内容。

setupenv.sh里，是如何进行展开的？

```
make O="$TARGET_OUTPUT_DIR" "$TARGET_BUILD_CONFIG"_defconfig
```

调用到buildroot里的Makefile

```
 defconfig: $(BUILD_DIR)/buildroot-config/conf outputmakefile
         @$(COMMON_CONFIG_ENV) $< --defconfig$(if $(DEFCONFIG),=$(DEFCONFIG)) $(CONFIG_CONFIG_IN)
```

build/buildroot-config



把s400的配置画图在这里

https://naotu.baidu.com/file/e9c807f0649b014b1e669c0c2a24b01b