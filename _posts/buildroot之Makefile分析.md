---
title: buildroot之Makefile分析
date: 2019-05-17 14:31:11
tags:
	- Linux
---



顶层Makefile的大概逻辑是这样：

```
# 这个是清空默认规则
.SUFFIXES:

SHELL = /bin/bash

O = ./output

all:

.PHONY: all

TOPDIR := $(CURDIR)
CONFIG_CONFIG_IN = Config.in
CONFIG = support/kconfig
DATE := $(shell date +%Y%m%d)

# 这个里面定义了空格等基础的对象。
include support/misc/utils.mk

CONFIG_DIR := $(CURDIR)
BASE_DIR := $(CANONICAL_O) # 就是output

这个在output目录下，是空的。
BR2_EXTERNAL_FILE = $(BASE_DIR)/.br-external.mk
-include $(BR2_EXTERNAL_FILE)

指定输出目录。
BUILD_DIR := $(BASE_DIR)/build
BINARIES_DIR := $(BASE_DIR)/images
TARGET_DIR := $(BASE_DIR)/target

HOST_DIR := $(BASE_DIR)/host
GRAPHS_DIR := $(BASE_DIR)/graphs

配置文件。根目录下。
BR2_CONFIG = $(CONFIG_DIR)/.config

然后包含目标对应的defconfig文件。
ifeq ($(filter $(noconfig_targets),$(MAKECMDGOALS)),)
-include $(BR2_CONFIG)
endif

然后是定义host上的工具链。
ifndef HOSTCC
HOSTCC := gcc
HOSTCC := $(shell which $(HOSTCC) || type -p $(HOSTCC) || echo gcc)
endif

包含2个工具文件。
include package/pkg-utils.mk
include package/doc-asciidoc.mk

默认目标来了。
all: world

包含老的Makefile。为了兼容。
include Makefile.legacy

include system/system.mk
include package/Makefile.in


-include $(sort $(wildcard arch/arch.mk.*))
include support/dependencies/dependencies.mk

包含所有的package下面的mk文件。就对应要下载的第三方包。
include $(sort $(wildcard package/*/*.mk))

include boot/common.mk
include linux/linux.mk
include fs/common.mk


.PHONY: dirs

.PHONY: world
world: target-post-image

.PHONY: sdk
sdk: world

.PHONY: source
source: $(foreach p,$(PACKAGES),$(p)-all-source)

menuconfig: $(BUILD_DIR)/buildroot-config/mconf prepare-kconfig
	@$(COMMON_CONFIG_ENV) $< $(CONFIG_CONFIG_IN)
	
.PHONY: help
help:

.PHONY: list-defconfigs
list-defconfigs:
```

看看package下面的文件。

以boa为例进行分析。因为这个简单。

一个目录下的典型文件是：

```
xx.hash
xx.mk
Config.in
```

有些还有patch文件。



Buildroot 是一个工具，它使用交叉编译简化和自动化为嵌入式系统构建完整 Linux 系统的过程。

为了实现这一点，Buildroot 能够为您的目标生成交叉编译工具链、根文件系统、Linux 内核映像和引导加载程序。

 Buildroot 可独立用于这些选项的任意组合（例如，您可以使用现有的交叉编译工具链，并仅使用 Buildroot 构建您的根文件系统）。 

Buildroot 主要对使用嵌入式系统的人有用。

嵌入式系统通常使用的处理器不是每个人都习惯在他的 PC 中使用的常规 x86 处理器。

它们可以是 PowerPC 处理器、MIPS 处理器、ARM 处理器等。

Buildroot 支持多种处理器及其变体；它还带有几个现成可用的板的默认配置。

除此之外，许多第三方项目基于或在 Buildroot 之上开发其 BSP 或 SDK 。



参考资料

1、



