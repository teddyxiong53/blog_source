---
title: busybox之代码目录分析
date: 2017-10-02 11:07:48
tags:
	- busybox

---



# 1. 先看reamde

可以得到如下信息：

1、安装说明是在INSTALL文件里。

2、busybox的简介：

1）busybox是把很多的精简版本的unix基础工具打包到一个小的可执行程序里了。

2）基础工具包有：

bzip2

coreutils：

dhcp：

diffutils：

e2fsprogs：

file

findutils：

gawk：

grep：

inetutils：

less：

modutils：

net-tools：

procps：

sed：

shadow：

sysklogd：

sysvinit：

tar：

util-linux：

vim：

busybox里的实现，去掉了一些复杂的选项的实现。

busybox里的代码充分考虑了资源限制，无论是程序大小还是运行时占用内存都进行了优化。busybox让构建嵌入式系统变得容易。



# 2. 看.config文件

这个文件分为这个几大块。

1、通用配置。

2、编译配置。

3、调试配置。

4、安装配置。

5、库配置。

6、applet配置。

7、各种utils命令选配。



# 3. 看Makefile

先看看make help的输出内容：

```
teddy@teddy-ubuntu:~/work/qemu/busybox/busybox-1.25.1$ make help
Cleaning:
  clean                 - delete temporary files created by build
  distclean             - delete all non-source files (including .config)
  doc-clean             - delete all generated documentation

Build:
  all                   - Executable and documentation
  busybox               - the swiss-army executable
  doc                   - docs/BusyBox.{txt,html,1}
  html                  - create html-based cross-reference

Configuration:
  allnoconfig           - disable all symbols in .config
  allyesconfig          - enable all symbols in .config (see defconfig)
  config                - text based configurator (of last resort)
  defconfig             - set .config to largest generic configuration
  menuconfig            - interactive curses-based configurator
  oldconfig             - resolve any unresolved symbols in .config
  android2_defconfig    - Build for android2
  TEST_noprintf_defconfig - Build for TEST_noprintf
  cygwin_defconfig      - Build for cygwin
  TEST_nommu_defconfig  - Build for TEST_nommu
  android_defconfig     - Build for android
  android_ndk_defconfig - Build for android_ndk
  android_502_defconfig - Build for android_502
  TEST_rh9_defconfig    - Build for TEST_rh9
  freebsd_defconfig     - Build for freebsd


Installation:
  install               - install busybox into CONFIG_PREFIX
  uninstall

Development:
  baseline              - create busybox_old for bloatcheck.
  bloatcheck            - show size difference between old and new versions
  check                 - run the test suite for all applets
  checkhelp             - check for missing help-entries in Config.in
  randconfig            - generate a random configuration
  release               - create a distribution tarball
  sizes                 - show size of all enabled busybox symbols
  objsizes              - show size of each .o object built
  bigdata               - show data objects, biggest first
  stksizes              - show stack users, biggest first

```

