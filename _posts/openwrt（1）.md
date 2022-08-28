---
title: openwrt（1）
date: 2020-03-24 09:42:02
tags:
	- openwrt

---

1

自己编译烧录树莓派3b的。

这个用tar来解压会报错。只有11M左右。

```
bin/targets/brcm2708/bcm2710/openwrt-brcm2708-bcm2710-rpi-3-ext4-factory.img.gz
```

不用解压，直接用rufus进行烧录到sd卡就好了。

默认打开了串口。所以不用调整任何参数。

默认有hdmi输出和支持usb的键盘。所以如果有键盘，可以不用串口。



# 开发调试

## luci的调试

LUCI调试方法
将宿主机的/home/nfs/lua挂载到/usr/lib/lua上，以便于在线调试。
mount -t nfs -o nolock 192.168.200.65:/home/nfs/lua /usr/lib/lua
或  mount -t nfs -o nolock 192.168.200.65:/home/nfs/luci /usr/lib/lua/luci

删除LUCI缓冲
rm -rf /tmp/luci*



## 下载我们的优化后的源码

- GitHub中下载的官方源码，安装软件包时会从国外的网址进行下载，导致编译速度很慢，我们对官方源码进行优化，添加了两个文件（feeds.conf.default、feeds.conf），在其中添加了我们国内的镜像源，这样在编译时速度会快些
- 百度云链接：https://pan.baidu.com/s/1JY8men7tJOxM_HBl1iP7Tg（提取码：9hj7 ）
- CSDN下载链接：https://download.csdn.net/download/qq_41453285/11870828

## 单独编译模块

单独编译模块
下面我们以TcpDump为例：

“make package/tcpdump/clean”清除编译生成的文件，包含安装包及编译过程生成的 临时文件
“make package/tcpdump/prepare”进行编译准备，包含下载软件代码包、并解压缩和 打补丁
“make package/tcpdump/configure”根据设置选项进行配置并生成 Makefile
“make package/tcpdump/compile”根据生成的 Makefile 进行编译
“make package/tcpdump/install”生成安装包
以上编译命令都可以添加“V=s”来查看详细编译过程



“make download”下载所有已选择的软件代码压缩包
“make clean”删除编译目录
“make dirclean”除了删除编译目录之外还删除编译工具目录
“make printdb”输出所有的编译变量定义



现在把lean的openwrt跟openwrt原版的进行比较，看看他改了什么。

config目录：这个就4个配置文件，都改了。看来就是运行更大的空间使用这个方向改的。例如把glibc加进来了。

include目录：这个就是各种mk文件。都是一些补充性的修改。target.mk里，DEFAULT_PACKAGES加了不少。

package目录：一些针对国内优化的修改。

最大的改动就在这里。下面增加了一个lean的目录。下面就是所有新增包的内容。

feed.conf.default：这个是fee的时候，从哪里取数据，原版是从openwrt.org，lean版本是从github。





开发调试，在virtualbox上会比较方便。

编译：

```
./scripts/feeds update -a 
   ./scripts/feeds install -a
   make menuconfig 
```

默认就是x86的的配置。我就要这个。

把配置过了一下，把ext4的勾选上。

编译。现在翻着墙的，编译应该没有什么问题。

| **目 录**       | **含 义**                                                    |
| --------------- | ------------------------------------------------------------ |
| **dl**          | 下载软件代码包临时目录。编译前，将原始的软件代码包下载到该目录 |
| **feeds**       | 扩展软件包目录。将一些不常用的软件包放在其他代码库中，通过feed机制可以自定义下载及配置 |
| **bin**         | 编译完成后的最终成果目录。例如安装映像文件及 ipk 安装包      |
| **build_dir**   | 编译中间文件目录。例如生成的.o 文件                          |
| **staging_dir** | 编译安装目录。文件安装到这里，并由这里的文件生成最终的编译成果 |
| **log**         | 如果打开了针对开发人员 log 选项，则将编译 log 保存在这个目录下，否则该目录并不会创建 |
| **tmp**         | 编译过程的大量临时文件都会在此                               |



OpenWrt固件中，几乎所有东西都是**软件包（package）**，

可以编译为以“.ipk”结尾的安装包，

这样就可以很方便地安装、升级和卸载了。

注意，**扩展软件包不是在主分支中维护的，**

但是可以使用**软件包编译扩展机制（feeds）来进行扩展安装**。

这些包能够扩展基本系统的功能，只需要将它们链接进入主干。

之后，这些软件包将会显示在编译配置菜单中

./sripts/feeds install -a时，feeds目录就产生了，安装的软件就存放在这个目录下了



因此，当**开始执行一 个UCI兼容的守护进程初始化脚本**时，

你应该意识到**程序的原始配置文件被覆盖**了。

例如，在DNS代理服务器 dnsmasq进程启动的情况下，

文件/var/etc/dnsmasq.conf 是从 UCI 配置文件/etc/config/dhcp生成并覆盖的，

是运行/etc/init.d/dnsmasq脚本进行配置文件转换的

配置文件的存储：

因为应用程序的配置文件是启动时通过UCI转换生成的，

因此它不需要存储在非易失性存储器中，

通常存储在内存中而不是在闪存中，

而var目录为其内容在正常运行时不断变化的目录，因此将var目录创建为/tmp目录的一个链接



如果只是直接启动可执行文件，没有通过 init.d 调用，将不会将一个 UCI 配置文件更新到特定程序相应的配置文件位置，在/etc/config/的 修改将不会对现有进程有任何影响



- 当使用UCI工具写入配置文件时，配置文件都是整个重写并且不需要确认命令。这意味着在文件中任何**多余的注释行和空行均会被删除**
- 如果你有 UCI 类型的配置文件，**想保存自己的注释和空行**，那就**不应该使用UCI命令**行工具来编辑文件



- OpenWrt 还有一些配置并不是通过UCI配置来实现的，这部分是大多数 Linux 系统都有的配置，并且用户很少修改，因此并不提供接口给用户修改



OpenWrt 有一个非常好的构建系统，

这样我们就可以非常方便地管理数千个软件包和几十个硬件平台。

我们也可以非常方便地移植已有的软件到OpenWrt系统中。

在前面我们介绍的OpenWrt源码中，你会发现各个软件包目录下一般会有**两个文件夹和一个Makefile 文件**

![img](../images/random_name/20191014171411975.png)

- **补丁（patches）目录：**是可选的，典型包含缺陷修改或者用于优化可执行程序大小的补丁文件
- **files目录：**也是可选的，它一般用于保存默认配置文件和初始化启动脚本
- **src目录：**如果为OpenWrt本身项目所包含的软件模块，因为代码将完全受到自己控制，这时将不会patches 目录存在，而是会有一个 src 目录，代码直接放在src目录下（在下一篇文章中我们自己定义的软件包就有这个目录）
- Makefile：提供下载、编译、安装以及生成 OPKG 安装包的功能，这个文件是必须有的



从Makefile的内容可以看出，此Makefile与普通的Makefile不同，OpenWrt没有遵守传统的Makefile格式风格，而是将Makefile写成面向对 象格式，这样就简化了多平台移植过程



## 软件包构建步骤

| ***\*Build 步骤\**** | ***\*是否必需\**** | ***\*含 义\****                                              |
| -------------------- | ------------------ | ------------------------------------------------------------ |
| **Build/Prepare**    | 可选               | 一组用于解包及打补丁的命令，也可以不使用                     |
| **Build/Configure**  | 可选               | 如果源代码不需要configure来生成Makefile或者是通用的configure脚本， 就不需要这部分。否则就需要你自己的命令脚本或者使用"$(call Build/Configure/Default, FOO=bar)"增加额外的参数传递给 configure 脚本 |
| **Build/Compile**    | 可选               | 编译源代码，在大多数情况下应该不用定义而使用默认值。如果你想传递给 make 特定的参数，可以使用“$(call Build/Compile/Default, FOO=bar)” |
| **Build/Install**    | 可选               | 安装编译后的文件，默认是调用 make install，如果需要传递指定的参 数，使用$(call Build/Install/Default,install install-foo)。注意你需要传递所 有的参数，要增加在“install”参数后面，不要忘了“install”参数 |
| **Build/InstallDev** | 可选               | 例如静态库和头文件等，但是不需要在目标设备上使用             |





docker，它非常适合快速部署各种应用。

比如nextcloud网盘，transmission，hoemassistant，博客等

虽然说路由器就应该踏踏实实做个路由，但是不排除有人路由器性能确实过剩了。所以跑个docker是有必要的。

进入到dockerman管理界面，选择拉取这个。这个是一个图形化的docker管理界面。

```
portainer/portainer
```

## 在virtualbox里运行

当前编译出来的，x86版本，默认就生成了vmdk文件。

openwrt-snapshot-r2952-bcbce88-x86-64-generic-ext4-combined.vmdk

新建虚拟几件，选择其他Linux，64位。

然后设置硬盘为vmdk文件。

选择2个网卡。网卡1为host only的。网卡2为nat的。

然后开机。

查看网络配置：

```
uci show network
```

可以看到lan的ip是192.168.1.1。

我们修改一下：

```
uci set network.lan.ipaddr='192.168.56.2'
uci commit
reboot
```

重启后，默认root用户没有密码。

我们先修改密码：

```
passwd
```

改好密码后，然后电脑这边用ssh客户端进行连接。

连接正常。

然后再进行下面的设置。

```
uci batch <<EOF
set network.mng=interface
set network.mng.type='bridge'
set network.mng.proto='static'
set network.mng.netmask='255.255.255.0'
set network.mng.ifname='eth0'
set network.mng.ipaddr='192.168.56.2'
delete network.lan
delete network.wan6
set network.wan=interface
set network.wan.ifname='eth1'
set network.wan.proto='dhcp'
EOF
```

然后保存，重启。

```
uci commit && reboot
```

但是上面的改动会导致dropbear这个ssh服务端无法启动。因为删掉了lan设备。

luci还是可以访问的。

我在网络-接口里把lan添加回来。效果是这样：

```
config interface 'lan'
        option proto 'static'
        option ifname 'eth0'
        option ipaddr '192.168.56.2'
        option netmask '255.255.255.0'
        option gateway '192.168.56.1'
        option broadcast '192.168.56.255'
        option dns '192.168.56.1'
```

现在可以ssh连接了。

# feeds

Feeds是OpenWRT环境所需要的软件包套件，比较重要的feeds有：

‘pacakges’：一些额外的基础路由器特性软件

‘LuCI’：OpenWRT默认的GUI

‘Xwrt’：另一种可选的GUI界面

下载之前可以通过查看更改feeds.conf.default这个文件来查看和选择相应的软件包。

这个文件包含了feeds的列表，每一行由三个部分组成，feeds的方法，feeds的名字和feeds的源。

下面是一个feeds.conf.default的例子：



下面是feeds支持的方法类型：

src-bzr通过使用bzr从数据源的pxiaath/URL下载数据

src-cpy通过从数据源path拷贝数据

src-darcs通过使用darcs从数据源path/URL下载数据

src-hg通过使用hg从数据源path/URL下载数据

src-link创建一个数据源path的symlink

src-svn通过使用svn从数据源path/URL下载数据



其实还有一种就是可以添加本地源，如这种写法：

```text
src-link custom /home/openwrt/Desktop/odin/custom
```



# 扩大分区容量

32G的SD卡没有使用所有空间。

我之前是把后面的分区挂载在/root下面。

这样系统的空间还是没有扩大。使用上总感觉空间会不够。

所以最好还是把空间都给根分区。

但是当前的数据不能丢。

这个是ext格式的镜像的扩展方式。我当前的不是这个，我是squashfs的。

https://www.icxbk.com/article/detail/1331.html

这个讲的是overlay扩容。

https://www.vediotalk.com/archives/13889

其实很简单，只需要在网页上，挂载点那里修改，按照上面问题修改。然后重启就可以了。

最后的效果：

```
/dev/mmcblk0p3           28.4G    350.1M     26.6G   1% /overlay
overlayfs:/overlay       28.4G    350.1M     26.6G   1% /
```



# 官方版本的发布节奏

OpenWrt 19.07 稳定版。它是之前的 18.06 稳定版的继任者。

OpenWrt 19.07 系列：让所有已支持设备更新到Linux4.14内核

增加对基于[ath79](https://openwrt.org/docs/techref/targets/ath79)框架设备系统的支持。

当前稳定的 OpenWrt 版本是 19.07，2020年9月10日发布的 **v19.07.4** 是此系列的最新版本。

这个版本的镜像

https://downloads.openwrt.org/releases/19.07.4/targets/

树莓派3b

https://downloads.openwrt.org/releases/19.07.4/targets/brcm2708/bcm2710/

这个官方文档首页

https://openwrt.org/start?id=zh/start



**闪存小于4M或内存小于32M的设备在可用性、扩展性及操作的稳定性上将有所局限。** 在您选择购买设备或因设备被受支持决定在设备上刷入OpenWrt时，请务必关注这点。

当前支持的设备类型有1700多种。

https://openwrt.org/start?id=zh/toh/views/toh_fwdownload

这个表里可以看到所有。

有的老旧设备，能用的版本就比较老。

# 新增一个package



https://blog.csdn.net/jf_xu/article/details/53486177

增加一个内核驱动。

https://blog.csdn.net/qq_41453285/article/details/102760270



“Build/Prepare”定义了如何准备编译本软件包，



这篇非常详细了。

https://blog.csdn.net/iampisfan/article/details/78128688

一些主要的变量：

```
BUILD_DIR
build_dir/target-arm_cortex-a9+vfpv3_musl-1.1.16_eabi

STAGING_DIR
staging_dir/target-arm_cortex-a9+vfpv3_musl-1.1.16_eabi

BIN_DIR
bin/mvebu

BUILD_LOG_DIR
logs

STAGING_DIR_HOST
staging_dir/host

TOOLCHAIN_DIR
staging_dir/toolchain-arm_cortex-a9+vfpv3_gcc-5.3.0_musl-1.1.16_eabi

BUILD_DIR_HOST
build_dir/host

BUILD_DIR_TOOLCHAIN
build_dir/toolchain-arm_cortex-a9+vfpv3_gcc-5.3.0_musl-1.1.16_eabi

PACKAGE_DIR
bin/mvebu/packages

TARGET_ROOTFS_DIR
build_dir/target-arm_cortex-a9+vfpv3_musl-1.1.16_eabi

TARGET_DIR
build_dir/target-arm_cortex-a9+vfpv3_musl-1.1.16_eabi/root-mvebu

STAGING_DIR_ROOT
staging_dir/target-arm_cortex-a9+vfpv3_musl-1.1.16_eabi/root-mvebu
```



```
$(INCLUDE_DIR)/subdir.mk定义了两个非常重要的函数：subdir和stampfile，
subdir会生成一些规则，
例如package/Makefile调用了(eval $(call subdir,$(curdir)))，则会递归到各个子目录下，生成package/$(bd)/$(target)和package/$(lastdir)/$(target)，$(target)取值为clean download prepare compile install update refresh prereq dist distcheck configure。
以iperf为例，subdir会为其生成下面规则：
```



```
Makefile中首先定义了一些变量，包括：
- PKG_NAME
package的名字，用于显示在menuconfig和生成ipkg，例中该值等于iperf
- PKG_VERSION
package的版本号，例中该值等于2.0.5
- PKG_RELEASE
package的Makefile的版本，例中该值等于1
- PKG_SOURCE
package的sourcecode包的名称，例中该值等于iperf-2.0.5.tar.gz
- PKG_SOURCE_URL
package sourcecode包的下载链接，可以添加多个链接，以分号隔开，例中该值等于@SF/iperf，其中@SF表示从sourceforge
- PKG_MD5SUM
tar包的MD5校验码，由于核对tar包下载是否正确
- PKG_CAT
tar包的解压方式，包括zcat, bzcat, unzip等
- PKG_BUILD_DIR
tar包解压以及编译的路径，如果Makefile中不指定，则默认为$(BUILD_DIR)/$(PKG_NAME)$(PKG_VERSION)，例子中将PKG_BUILD_DIR指定成了$(BUILD)/iperf-single/iperf-2.0.5

PKG_*这些变量主要描述了package的从什么连接下载，下载什么版本的tar包，以及如何解压tar包。
```

**Build/Prepare (可选):**
定义一些列解压缩tar包，打patch，拷贝sourcecode到build dir等操作的命令

**Build/Compile (可选):**
定义编译的命令



## package里的相关变量

把这些`/`理解成`-`，看起来就就好理解多了。不然就看出目录层次。

```
make package/rokid/property/compile
就相当于
make package-rokid-property-compile
```

另外一个不爽的点是有大写字母，目前没有发现什么规律。

下面的变量分为两个大类：

1、Package开头的。表示ipk打包相关的。

2、Build开头的。编译代码目录编译相关的。



```
define Package/property
	SECTION:=libs
	CATEGORY:=custom
	TITLE:=property
	DEPENDS:=+libstdcpp
endef
```

```
# 表示这个package对所有架构都适用。
PKGARCH:=all
```

```
# 本package需要安装的config文件。一行一个文件。
define Package/base-files/conffiles
/etc/config/network
endef
```

```
# 描述
define Package/property/description
	property
endef
```

```
# 一般是下面这样，把代码拷贝到build目录。
define Build/Prepare
	$(CP) $(PKG_SOURCE_DIR)/* $(PKG_BUILD_DIR)
	$(call Build/Prepare/Default,)
endef
```

```
# configure 定义
define Build/Configure/Default
(cd $(PKG_BUILD_DIR); \
        CFLAGS="$(TARGET_CFLAGS) $(EXTRA_CFLAGS)" \
        CXXFLAGS="$(TARGET_CFLAGS) $(EXTRA_CFLAGS)" \
        LDFLAGS="$(TARGET_LDFLAGS) $(EXTRA_LDFLAGS)" \
        cmake $(CMAKE_SOURCE_DIR) 
endef
```

```
# compile编译
define Build/Compile/Default

endef
Build/Compile = $(Build/Compile/Default)

define Build/RunMake
        CFLAGS="$(TARGET_CPPFLAGS) $(TARGET_CFLAGS)" \
        $(MAKE) $(PKG_JOBS) -C $(PKG_BUILD_DIR)/$(1) \
                $(TARGET_CONFIGURE_OPTS) \
                $(DRIVER_MAKEOPTS) \
                LIBS="$(TARGET_LDFLAGS)" \
                LIBS_c="$(TARGET_LDFLAGS_C)" \
                BCHECK= \
                $(2)
endef

define Build/Compile/hostapd
        $(call Build/RunMake,hostapd, \
                hostapd hostapd_cli \
        )
endef
```

```
# Build/Install
# 这个默认是执行make install
“$(call Build/Install/Default,install install-foo)”

```

```
# Build/InstallDev
# 这个是安装到staging目录
```

```
# Build/Clean

```



```
Package/install

A set of commands to copy files into the ipkg which is represented by the $(1) directory. 
```

```
Package/preinst
Package/postinst
Package/prerm
Package/postrm

```



这个Makefile比较全面，值得分析一下。

openwrt/package/network/services/hostapd/Makefile

在menuconfig里可以看到4个hostapd。

```
< > hostapd................................. IEEE 802.1x Authenticator (full)
-*- hostapd-common............... hostapd/wpa_supplicant common support files
< > hostapd-common-old                                                       
< > hostapd-mini.................... IEEE 802.1x Authenticator (WPA-PSK only)
```

是因为在一个Makefile里定义了多个Package。

```
define Package/hostapd-common-old
  TITLE:=hostapd/wpa_supplicant common support files (legacy drivers)
  SECTION:=net
  CATEGORY:=Network
endef
```

构建了多个package。

```
$(eval $(call BuildPackage,hostapd))
$(eval $(call BuildPackage,hostapd-mini))
$(eval $(call BuildPackage,wpad))
$(eval $(call BuildPackage,wpad-mesh))
$(eval $(call BuildPackage,wpad-mini))
$(eval $(call BuildPackage,wpa-supplicant))
$(eval $(call BuildPackage,wpa-supplicant-mesh))
$(eval $(call BuildPackage,wpa-supplicant-mini))
$(eval $(call BuildPackage,wpa-supplicant-p2p))
$(eval $(call BuildPackage,wpa-cli))
$(eval $(call BuildPackage,hostapd-utils))
$(eval $(call BuildPackage,hostapd-common))
$(eval $(call BuildPackage,hostapd-common-old))
$(eval $(call BuildPackage,eapol-test))
```

## 依赖类型

```
+xx
	依赖于xx，当自己被select的时候，xx也会被select。
xx
	只有在xx被选中的时候，自己才能被看到。
@XX
	依赖于CONFIG_XX配置项。
+XX:yy 
	如果CONFIG_XX配置项打开，那么依赖yy。

```

## 单独编译

```
四，单独编译

1，包清理编译方式：

清理包：make package/xxx/clean V=s -j1
准备包：make package/xxx/prepare V=s -j1
编译包：make package/xxx/compile V=s -j1
安装包：make package/xxx/install V=s -j1



2，单独清理编译kernel，kernel在target内
make target/linux/clean V=s -j1
make target/linux/prepare V=s -j1
make target/linux/compile V=s -j1
make target/linux/install V=s -j1



3，单独清理编译uboot
make package/boot/uboot-meson/clean V=s -j1
make package/boot/uboot-meson/prepare V=s -j1
make package/boot/uboot-meson/compile V=s -j1
make package/boot/uboot-meson/install V=s -j1
```



# Build/InstallDev

处理一些OpenWrt编译包时可以依赖的文件（如静态库，头文件等），

但是这些在目标设备上用不到。

举例来说，假设你的OpenWrt项目上有一个基本的包，

这个包中的一些头文件在编译其他包时会用到，

但是最终生成的固件镜像烧入目标设备后却用不到这些头文件，

就可以在这个section中定义要将这些头文件拷贝到哪里去（一般是toolchain使用的头文件路径）。

当然如果其他包编译时需要用到这个包的头文件，那么其他包也应该定义为依赖这个包，这样在其他包编译之前会先编译这个包，并执行这些install动作以免其他包编译时找不到头文件。



# rules.mk

大部分重要变量，都是在这里定义的。



# rc.common用法

由于openwrt使用自己的初始script系统，所有的initscript必须使用/etc/rc.common作为wrapper安装

如/etc/init.d/httpd：

```

#!/bin/sh/etc/rc.common
# Copyright (C)2006 OpenWrt.org
START=50
start() {
    [ -d /www ] && httpd -p 80 -h /www-r OpenWrt
}
stop() {
    killall httpd
}

```

从上可以看出 ，script本身并不解析命令行参数，而是由/etc/rc.common来完成。

Start和stop是最基本的功能，几乎所有init script都要提供。Start是在运行/etc/init.d/httpd start时来调用，可以是系统启动时，或用户手动运行此脚本时。

通过/etc/init.d/<name> enable/disable

可以启用或禁止模块的初始化脚本，

他是通过创建或删除/etc/rc.d中的符号连接来完成，

**而这些符号连接是/etc/init.d/rcS在启动阶段处理。**

脚本运行的顺序是在初始脚本中通过变量START来定义，改变后需要再次运行/etc/init.d/<name>enable。



# USE_PROCD

在openwrt系统内init进程被procd取代，

procd作为父进程可以监控子进程的状态。

一旦子进程退出后即可在某一个时刻尝试进行重启进程。

在op系统内使用procd监控的有uhttpd,netifd等。

在/etc/init.d/文件夹内带有USE_PROCD=1标志，

下面就介绍如何让procd启动某一个应用程序 

我的应用程序名是binloader, 直接上脚本代码

```
#!/bin/sh /etc/rc.common
# Copyright (C) 2008 OpenWrt.org    

START=98
#执行的顺序，按照字符串顺序排序并不是数字排序

USE_PROCD=1
#使用procd启动

BINLOADER_BIN="/usr/bin/binloader"

start_service() {
	procd_open_instance
	#创建一个实例， 在procd看来一个应用程序可以多个实例
	#ubus call service list 可以查看实例
	procd_set_param respawn
	#定义respawn参数，告知procd当binloader程序退出后尝试进行重启
	procd_set_param command "$BINLOADER_BIN"
	# binloader执行的命令是"/usr/bin/binloader"， 若后面有参数可以直接在后面加上

	procd_close_instance
	#关闭实例
}
#start_service 函数必须要重新定义

stop_service() {
	rm -f /var/run/binloader.pid
}
#stop_service重新定义，退出服务器后需要做的操作

restart() {
	stop
	start
}
```

必须指出来的是，被procd执行的程序不能是daemon后台程序，因为后台程序的主进程退出后在procd看来就是程序退出了，然后会进入respawn流程，之后重复启动和退出。

最后失效了



procd 的进程管理功能主要包含 3 个部分。

- reload_config，检查配置文件是否发生变化，如果有变化则通知 procd 进程。

- procd，守护进程，接收使用者的请求，增加或删除所管理的进程，并监控进程的状态，如果发现进程退出，则再次启动进程。

- procd.sh，提供函数封装procd提供系统总线方法，调用者可以非常便利的使用procd 提供的方法。

  

参考资料

  1、

  https://blog.csdn.net/liangdsing/article/details/53906445/2。

  2、10-Openwrt procd守护进程

  https://www.jianshu.com/p/acd2ccb5ea8d

# openwrt启动流程

总结一下OpenWrt的启动流程：

1.CFE->2.linux->3./etc/preinit->4./sbin/init ->5./etc/inittab ->6./etc/init.d/rcS->7./etc/rc.d/S* ->8.

CFE是一个bootloader。



参考资料

1、

https://developer.aliyun.com/article/375992





# 参考资料

1、openwrt luci开发方便调试的方法

https://blog.csdn.net/qq_19004627/article/details/86699217

2、OpenWrt开发

这个是系列文章，挺好的。

https://blog.csdn.net/qq_41453285/category_9376523.html

3、在Virtualbox虚拟机中运行OpenWrt

https://openwrt.org/zh/docs/guide-user/virtualization/virtualbox-vm

4、OPENWRT启动流程分析（史上最全）

https://blog.csdn.net/fengfeng0328/article/details/83352459

5、openwrt下 docker使用

https://koolshare.cn/thread-180474-1-1.html

6、OpenWRT的Feeds分析学习

https://www.cnblogs.com/rohens-hbg/articles/4969222.html

7、OpenWRT实践5：Feeds安装本地源

https://zhuanlan.zhihu.com/p/114424172

8、

http://iceway.github.io/2017/03/24/openwrt-study-notes-04-packages-upper-section.html