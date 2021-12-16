---
title: amlogic之分区配置
date: 2021-12-09 16:45:25
tags:
	- amlogic

---

--

客户由于生产、升级等需求，

需要厂商在系统中为其添加相应的分区，

供其存放特定的应用及工厂数据，

 在做差分升级时也可只升级某特定分区来更新对应的应用数据，

同时也要求厂商删除不必要的分区、调整其他 分区的大小、修改分区间的间隔大小，以便腾出更多的空间给其他分区利用。

（这个文档主要针对Android的，不继续看了，自己分析代码）

搜索aml_upgrade_package.conf使用的地方。

在buildroot的Makefile里，

```
include $(sort $(wildcard package/*/*.mk))

include boot/common.mk
include linux/linux.mk
include fs/common.mk
```



BR2_ROOTFS_POST_IMAGE_SCRIPT这个变量一般是空的。

要看这个。

```
./fs/ext2/ext2.mk:56:UPGRADE_DIR := $(patsubst "%",%,$(BR2_ROOTFS_UPGRADE_DIR))
```



```
ifeq ($(BR2_TARGET_USBTOOL_AMLOGIC),y)
ifeq ($(filter y,$(BR2_TARGET_UBOOT_AMLOGIC_2015) $(BR2_TARGET_UBOOT_AMLOGIC_REPO)),y)
ifneq ($(UPGRADE_DIR_OVERLAY),)
define ROOTFS-USB-IMAGE-PACK
        cp -rfL $(UPGRADE_DIR)/* $(BINARIES_DIR)
        cp -rfL $(UPGRADE_DIR_OVERLAY)/* $(BINARIES_DIR)
        BINARIES_DIR=$(BINARIES_DIR) \
        TOOL_DIR=$(HOST_DIR)/bin \
        $(HOST_DIR)/bin/aml_upgrade_pkg_gen.sh \
        $(BR2_TARGET_UBOOT_PLATFORM) $(BR2_TARGET_UBOOT_ENCRYPTION) $(BR2_PACKAGE_SWUPDATE_AB_SUPPORT)
endef
else
```

靠aml_upgrade_pkg_gen.sh 这个脚本。

./buildroot/package/amlogic/aml_img_packer_new/src/aml_upgrade_pkg_gen.sh



amlogic在配置文件的include机制展开是靠这里。

```
%_defconfig: $(BUILD_DIR)/buildroot-config/conf $(1)/configs/%_defconfig outputmakefile
		$(TOPDIR)/build/defconfig_hook.py -m $(1)/configs/$$@ $(BASE_DIR)/.amlogic-config
		$$(COMMON_CONFIG_ENV) BR2_DEFCONFIG=$(1)/configs/$$@ \
			$$< --defconfig=$(BASE_DIR)/.amlogic-config $$(CONFIG_CONFIG_IN);
```



参考资料

1、

