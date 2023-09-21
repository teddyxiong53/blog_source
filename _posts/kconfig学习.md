---
title: kconfig学习
date: 2018-12-01 15:43:13
tags:
	- kconfig

---

--

# 简介

Kconfig 是一种配置系统，广泛用于开源项目和嵌入式系统中，用于管理项目的配置选项。它最初由Linux内核社区开发，现在已经被广泛用于许多开源项目，以便用户可以轻松地自定义项目的功能和行为。以下是有关Kconfig的详细介绍：

1. **配置选项**：Kconfig 允许开发者定义一组配置选项，这些选项用于控制项目的各种功能和行为。这些选项可以包括开关、整数值、字符串等，可以根据需要进行自定义。

2. **菜单结构**：Kconfig 使用菜单结构来组织配置选项。这意味着配置选项可以按照一定的层次结构进行组织，以提供更好的可读性和导航性。通常，配置选项按照相关性和用途进行分组，并以子菜单的形式进行展示。

3. **依赖关系**：Kconfig 允许配置选项之间建立依赖关系。这意味着某些选项可能需要另一些选项已启用，或者某些选项可能会排除其他选项。这有助于确保配置选项的合理性和一致性。

4. **自动生成配置文件**：Kconfig 工具可以根据用户的选择自动生成配置文件。这个配置文件通常是一个文本文件，包含了用户选择的配置选项的值，以及相关的宏定义，可以在项目的源代码中使用。

5. **命令行工具**：Kconfig 配置系统通常与命令行工具一起使用。用户可以使用命令行界面来选择配置选项，并生成配置文件。这使得自动化构建和配置过程变得更加容易。

6. **多平台支持**：Kconfig 不仅限于Linux内核，它可以用于各种嵌入式系统和开源项目。许多开源项目（如BusyBox、U-Boot等）都采用了Kconfig作为其配置系统。

7. **可扩展性**：Kconfig 具有一定的可扩展性，开发者可以根据项目的需求编写自定义的配置选项和菜单，以适应特定项目的需要。

总之，Kconfig 是一种配置系统，用于管理项目的配置选项。它提供了一种组织、自定义和自动生成配置的方法，使项目开发和维护更加容易和可控。无论是在Linux内核中还是在其他开源项目和嵌入式系统中，Kconfig都是一个有用的工具，可以帮助开发者配置和定制其软件。

# 结构

```
config
	配置项
menuconfig
	带菜单的配置项。
choice/endchoice
	单选项。
comment
	注释。
	这个menuconfig里显示一行，很明显的。
	一般用来做分隔符的。
menu/endmenu
	菜单。
if/endif
	条件判断。
source
	引用其他文件。
```

# config

一个config有5个属性。

1、类型。有5种。bool、int、string、tristate、hex。后面可以跟一个字符串来做提示。

2、输入提示input prompt。

3、依赖关系。

4、默认值。

5、帮助信息。



## 关于prompt

```
bool "networking support"
```

等价于

```
bool 
prompt "networking support"
```

## 关于依赖

```
bool "foo" if BAR
default y if BAR
```

等价于

```
depends on BAR
bool "foo"
default y
depends on BAR
```



# buildroot的配置文件

顶层的Config.in。

```
首先是source arch/Config.in
	根据条件包含：
	source "arch/Config.in.arm"
```

一个choice，下面有多个config。

例如选择芯片类型的。是这样的格式。显示上，是一个箭头，进去后，X标记的为选中项。

```
choice 
	prompt "Target Architecture"
	default BR2_i386
	help 
		select the arch
config BR2_arm
	bool "ARM little endian"
	help
		"arm "
		
endchoice
```

elf格式的这个

```
choice
	prompt "target binary format"
	default BR2_BINFMT_ELF if BR2_USE_MMU
	
config BR2_BINFMT_ELF
	bool "ELF"
	depends on BR2_USE_MMU
	select BR2_BINFMT_SUPPORTS_SHARED
	
config BR2_BINFMT_FLAT
	bool "FLAT"
	depends on !BR2_USE_MMU
	help
		"xx"
endchoice
```



mconf prepare-kconfig

这个做了什么？



```
menuconfig: $(BUILD_DIR)/buildroot-config/mconf prepare-kconfig
	@$(COMMON_CONFIG_ENV) $< $(CONFIG_CONFIG_IN)
```



# 源代码分析



# 错误分析

endmenu in different file than menu? 

报这个错误，需要在endmenu后面还有一个空行才行。



# select

```
config A
    depends on B
    select C
```

它的含义是：CONFIG_A配置与否，取决于CONFIG_B是否配置。一旦CONFIG_A配置了，CONFIG_C也自动配置了。

# 完整的示例

以下是一个完整的Kconfig示例，展示了配置语法的各个方面，包括开关、整数、字符串、依赖关系和菜单结构。这个示例定义了一个虚拟的系统配置，其中包括系统版本、CPU类型、内存大小和一些功能开关。

```config
# 顶级菜单
menu "系统配置"

# 系统版本配置
config SYSTEM_VERSION
    string "系统版本号"
    default "1.0.0"
    help
      这是系统的版本号。

# CPU类型配置
config CPU_TYPE
    string "CPU类型"
    default "ARM Cortex-M4"
    help
      选择系统使用的CPU类型。

# 内存大小配置
config MEMORY_SIZE
    int "系统内存大小（KB）"
    default 1024
    range 256 4096
    help
      设置系统的内存大小，单位为KB。

# 功能开关
config FEATURE_A
    bool "启用功能A"
    default n
    help
      启用此选项以启用功能A。

config FEATURE_B
    bool "启用功能B"
    default n
    depends on FEATURE_A
    help
      启用此选项以启用功能B。依赖于功能A。

config FEATURE_C
    bool "启用功能C"
    default y
    help
      启用此选项以启用功能C。

endmenu
```

在这个示例中，我们定义了一个名为“系统配置”的顶级菜单，下面包含了一些配置选项。这些选项包括字符串、整数和开关类型的选项。其中一些选项具有默认值，一些具有范围限制，而另一些具有依赖关系。

这个示例中的配置语法包括以下要点：

- `config`：用于定义一个配置选项。
- `string`：用于定义字符串类型的选项。
- `int`：用于定义整数类型的选项。
- `bool`：用于定义开关类型的选项。
- `default`：指定默认值。
- `range`：指定整数选项的范围。
- `depends on`：定义选项之间的依赖关系。
- `help`：提供有关选项的描述。

您可以根据自己的项目需求和配置选项来扩展这个示例，以满足特定的配置管理需求。在实际项目中，Kconfig文件通常包括更多的配置选项和更复杂的结构，以便更灵活地控制项目的行为。

# 参考资料

1、kconfig语法整理

https://www.jianshu.com/p/aba588d380c2

2、Kconfig中的“depends on”和“select”

https://nanxiao.me/linux-kernel-note-59-kconfig-depends-on-select/