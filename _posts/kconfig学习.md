---
title: kconfig学习
date: 2018-12-01 15:43:13
tags:
	- kconfig

---

1

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
bool "foo" is BAR
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



参考资料

1、kconfig语法整理

https://www.jianshu.com/p/aba588d380c2

2、Kconfig中的“depends on”和“select”

https://nanxiao.me/linux-kernel-note-59-kconfig-depends-on-select/