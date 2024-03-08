---
title: openwrt（1）
date: 2020-03-24 09:42:02
tags:
	- openwrt

---

--

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

**下面的变量分为两个大类：**

**1、Package开头的。表示ipk打包相关的。**

**2、Build开头的。编译代码目录编译相关的。**



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



```
WARNING: your configuration is out of sync. Please run make menuconfig, oldconfig or defconfig!
```



# Build/InstallDev

处理一些OpenWrt编译包时可以依赖的文件（如静态库，头文件等），

但是这些在目标设备上用不到。

举例来说，假设你的OpenWrt项目上有一个基本的包，

这个包中的一些头文件在编译其他包时会用到，

但是最终生成的固件镜像烧入目标设备后却用不到这些头文件，

就可以在这个section中定义要将这些头文件拷贝到哪里去（一般是toolchain使用的头文件路径）。

当然如果其他包编译时需要用到这个包的头文件，那么其他包也应该定义为依赖这个包，这样在其他包编译之前会先编译这个包，并执行这些install动作以免其他包编译时找不到头文件。

# Build/InstallDev 表示什么

在OpenWRT的Makefile中，`Build/InstallDev` 是一个构建规则，用于定义软件包的开发文件（development files）安装。这通常包括头文件、库文件以及其他与开发有关的文件，使得其他软件能够与这个软件包进行交互或构建。

在Makefile中，`Build/InstallDev` 的定义类似于下面的形式：

```make
define Build/InstallDev
    $(INSTALL_DIR) $(1)/usr/include
    $(CP) $(PKG_INSTALL_DIR)/usr/include/* $(1)/usr/include/
    $(INSTALL_DIR) $(1)/usr/lib
    $(CP) $(PKG_INSTALL_DIR)/usr/lib/* $(1)/usr/lib/
    # Add more installation commands if needed
endef
```

这个规则指定了如何将开发文件从软件包的构建目录（`$(PKG_INSTALL_DIR)`）复制到目标安装目录。在这个例子中，头文件被复制到 `$(1)/usr/include/`，库文件被复制到 `$(1)/usr/lib/`。`$(1)` 是Makefile系统传递的目标安装目录变量。

在软件包的Makefile中，你可以使用这个规则来定义软件包的开发文件的安装方式。例如：

```make
include $(TOPDIR)/rules.mk

# ...

define Package/my-package
    SECTION:=utils
    CATEGORY:=Utilities
    TITLE:=My Package
    DEPENDS:=+libopenssl
endef

# ...

define Build/InstallDev
    $(INSTALL_DIR) $(1)/usr/include
    $(CP) $(PKG_INSTALL_DIR)/usr/include/* $(1)/usr/include/
    $(INSTALL_DIR) $(1)/usr/lib
    $(CP) $(PKG_INSTALL_DIR)/usr/lib/* $(1)/usr/lib/
endef

# ...

$(eval $(call BuildPackage,my-package))
```

在这个例子中，`Build/InstallDev` 规则被用于定义 `my-package` 软件包的开发文件的安装方式。

## 这个名字可以随意改吗

在OpenWRT的Makefile中，`Build/InstallDev` 是一个约定的规则名，但你可以根据需要自定义规则名。规则名通常是为了方便识别和组织代码，以及与其他软件包的规则进行区分。

当你定义一个新的规则名时，最好保持一致性和可读性，以便其他开发者能够理解你的意图。通常，规则名的格式是 `Build/Install*`，其中 `*` 是一个描述性的标识符，指示这个规则的目的。例如，`Build/InstallDev` 表示安装开发文件。

如果你希望使用一个不同的名字，确保它与其他规则名不冲突，并且最好反映出该规则的用途。然后，在软件包的定义中，你可以使用你自定义的规则名来指定相应的构建和安装步骤。

总的来说，灵活性是存在的，但保持一致性和清晰性有助于提高代码的可读性和可维护性。

## 除了Build/InstallDev，还有哪些预定义的名字？

在OpenWRT的Makefile中，有一些预定义的构建规则名称，它们用于定义软件包的不同构建阶段的操作。以下是一些常见的构建规则名称：

1. **Build/Configure：** 用于配置软件包，通常包括运行 `./configure` 脚本。
   
2. **Build/Compile：** 用于定义软件包的编译过程。

3. **Build/Install：** 定义软件包的安装步骤。

4. **Build/InstallDev：** 用于定义安装软件包的开发文件（头文件、库文件等）的步骤。

5. **Build/Clean：** 定义清理构建目录的步骤。

6. **Build/Prepare：** 用于定义构建准备步骤，通常用于创建构建目录等。

7. **Build/ConfigureDev：** 用于配置软件包的开发文件。

8. **Build/Patch：** 用于定义软件包的打补丁步骤。

这些规则名称对应于不同的构建阶段，它们的作用是为软件包的构建过程提供灵活性和可定制性。你可以在软件包的Makefile中使用这些规则名称，按照需要定义相应的构建步骤。例如：

```make
define Build/Configure
    # 配置步骤
endef

define Build/Compile
    # 编译步骤
endef

define Build/Install
    # 安装步骤
endef

define Build/Clean
    # 清理步骤
endef
```

通过合理使用这些规则名称，你可以有效地定制软件包的构建过程，以满足特定的需求和要求。

## Build/Compile 默认行为在哪里定义的

在OpenWRT的Makefile中，`Build/Compile` 的默认行为是在`include/package.mk`文件中定义的。这个文件包含了OpenWRT构建系统的一些通用规则和配置。

在 `package.mk` 文件中，有以下相关的内容，定义了 `Build/Compile` 的默认行为：

```make
# Default build behavior
# Invoked as $(call Build/Compile/Default)
define Build/Compile/Default
        $(call Build/Compile/Makefile)
        $(call Build/Compile/Default/$(PKG_BUILD_TYPE))
endef

# Default build behavior for "makefile" build type
define Build/Compile/Default/makefile
        $(MAKE) -C $(PKG_BUILD_DIR) \
                $(TARGET_CONFIGURE_OPTS) \
                $(PKG_JOBS) \
                $(if $(PKG_MAKE_PARALLEL), V=s) \
                $(PKG_EXTRA_MAKE_ARGS) \
                all
endef
```

这里，`Build/Compile/Default` 宏定义了默认的构建行为，而 `Build/Compile/Default/makefile` 宏定义了在 "makefile" 构建类型下的默认行为。在这个默认行为中，使用了 `$(MAKE)` 命令来执行构建，调用了构建目录下的Makefile，并传递了相应的配置选项和参数。

当你的软件包的Makefile没有定义自己的 `Build/Compile` 行为时，系统将使用这个默认的构建行为。如果你需要对构建过程进行更具体的定制，可以在软件包的Makefile中重新定义 `Build/Compile` 宏，覆盖默认的行为。

# make编译单个openwrt包的时候，后面跟的字符串是包的路径吗

对于OpenWRT，`Build/Compile` 的默认行为通常由 OpenWRT 的宏、规则以及软件包自身的 Makefile 定义。这个默认行为通常包括了编译整个软件包的步骤。具体的定义会依赖于 OpenWRT 版本以及软件包的类型和结构。

关于 `make` 编译单个 OpenWRT 包时，后面跟的字符串通常是包的名称，而不是路径。这是因为 OpenWRT 使用包的名称来标识和组织软件包。例如，你可以使用以下命令编译单个软件包：

```bash
make package/PACKAGE_NAME/compile
```

其中 `PACKAGE_NAME` 是你想要编译的软件包的名称，而不是包的路径。OpenWRT 的构建系统会自动查找该软件包的 Makefile，执行相关的构建和编译操作。

确保你的软件包名称是正确的，并且在 OpenWRT 源代码目录中可用，以便构建系统正确地定位和处理。

## make package/PACKAGE_NAME/compile 为什么不直接写成make PACKAGE_NAME

在OpenWRT中，`make package/PACKAGE_NAME/compile` 之所以需要这样的语法，是因为OpenWRT采用了一种模块化的软件包管理结构。软件包被组织在`feeds`中，而`package/`前缀告诉构建系统你正在操作的是软件包。

具体来说：

- `package/` 前缀表示你正在处理的是OpenWRT软件包。
- `PACKAGE_NAME` 是实际软件包的名称。

这种结构允许OpenWRT构建系统更灵活地处理软件包，使得构建系统能够自动从`feeds`中选择和集成软件包，而不是手动指定文件路径。通过使用这种模块化的结构，OpenWRT能够轻松地添加、移除或切换软件包，而不会导致构建系统的大幅修改。

总体而言，这种模块化结构提高了OpenWRT的可维护性和可扩展性。虽然 `make package/PACKAGE_NAME/compile` 的语法看起来较长，但它为构建系统提供了足够的信息，以便动态选择和编译所需的软件包。

## 除了package前缀，还有哪些前缀？

在OpenWRT的构建系统中，除了 `package/` 前缀，还有其他几个常用的前缀，用于指定不同的构建目标或操作。以下是一些常见的前缀：

1. **`target/` 前缀：** 用于指定目标系统的构建。例如，`make target/compile` 用于构建目标系统。

2. **`package/` 前缀：** 用于指定软件包的构建和操作。例如，`make package/PACKAGE_NAME/compile` 用于构建特定的软件包。

3. **`feeds/` 前缀：** 用于指定软件包源的操作。例如，`make feeds/update` 用于更新软件包源。

4. **`tmp/` 前缀：** 用于指定临时构建目录的操作。例如，`make tmp/clean` 用于清理临时构建目录。

5. **`kernel/` 前缀：** 用于指定内核相关的操作。例如，`make kernel/compile` 用于编译内核。

这些前缀提供了一种清晰的结构，使得用户能够针对不同的构建目标执行相应的操作。例如，`make package/PACKAGE_NAME/compile` 中的 `package/` 前缀明确表示这是与软件包构建相关的操作。这种结构有助于模块化构建系统，提高可维护性和可扩展性。

## 后缀除了compile，还有哪些？

在OpenWRT的构建系统中，除了 `compile` 后缀，还有其他一些常用的后缀，用于指定不同的构建和操作目标。以下是一些常见的后缀：

1. **`install` 后缀：** 用于指定安装相关的目标。例如，`make package/PACKAGE_NAME/install` 用于安装软件包。

2. **`clean` 后缀：** 用于指定清理构建相关文件的目标。例如，`make package/PACKAGE_NAME/clean` 用于清理软件包的构建目录。

3. **`menuconfig` 后缀：** 用于指定配置系统的目标。例如，`make menuconfig` 用于打开命令行菜单配置工具。

4. **`config` 后缀：** 用于指定配置软件包的目标。例如，`make package/PACKAGE_NAME/config` 用于配置特定的软件包。

5. **`update` 后缀：** 用于指定更新软件包源的目标。例如，`make feeds/update` 用于更新软件包源。

这些后缀提供了一种清晰的方式，使用户能够执行特定的构建和操作目标。通过使用这些后缀，OpenWRT的构建系统能够提供更灵活的构建和配置选项，同时保持清晰的命令结构。

## `make target/compile` 具体做了什么

`make target/compile` 是OpenWRT构建系统中的一个目标，用于编译整个目标系统。具体而言，这个目标会执行以下主要步骤：

1. **配置目标系统：** 执行与目标系统配置相关的操作。这包括根据设备和体系结构选择合适的配置选项。

2. **下载和安装依赖项：** 检查目标系统所需的依赖项，并下载、编译、安装这些依赖项。这可能包括交叉编译工具链、内核源代码等。

3. **构建目标系统：** 使用所选的配置选项和编译工具链，构建整个目标系统的所有组件，包括内核、基础系统工具和库等。

4. **安装目标系统：** 将构建好的目标系统安装到指定的输出目录，以供后续的固件生成或烧录。

执行 `make target/compile` 会触发OpenWRT构建系统对目标系统的全面构建过程。在这个过程中，会根据你的配置选择交叉编译工具链、构建和编译内核，以及生成目标系统的所有必要文件。这个目标通常是构建整个OpenWRT固件所需的第一步。

# openwrt的package/feeds目录下面有什么内容

`package/feeds` 目录是OpenWRT软件包管理中的一个重要目录，

它包含了软件包源（feeds）的定义和配置。

软件包源是包含软件包定义的目录，

可以是官方的OpenWRT软件包源，

也可以是用户自定义的第三方软件包源。

每个软件包源都包含一系列软件包的 Makefile 文件以及相关的元信息。

在 `package/feeds` 目录下，一般会看到一些默认的软件包源子目录，如：

1. **`packages` 目录：** 这是OpenWRT官方软件包源的默认目录，包含了许多常见的软件包，例如网络工具、应用程序、驱动等。

2. **`luci` 目录：** 包含LuCI（OpenWRT Web界面）相关的软件包。LuCI是一个用于配置和管理OpenWRT路由器的Web界面。

3. **其他自定义软件包源：** 用户可以在 `package/feeds` 目录下添加自己的软件包源，以扩展或定制OpenWRT的软件包集合。

每个子目录都包含了一个或多个软件包的 Makefile 文件，这些文件定义了如何构建和安装相应的软件包。软件包源的配置和定义可以在 `package/feeds.conf` 文件中找到，这个文件描述了使用哪些软件包源以及它们的配置信息。

总体而言，`package/feeds` 目录是OpenWRT软件包管理的核心之一，提供了组织和管理软件包的框架。

## 在feeds目录外面的package有什么不一样

在OpenWRT中，`feeds` 目录之外的 `package` 目录包含了一些与 OpenWRT 主线（feeds/packages）不同的软件包。这些软件包通常是由社区维护的，而不是OpenWRT官方团队维护的。以下是 `package` 目录与 `feeds` 目录之外的主要区别：

1. **来源与维护：**
   - `feeds` 目录中的软件包通常由OpenWRT官方团队维护，包含了官方支持的软件包。
   - `package` 目录之外的软件包通常是由社区成员或第三方维护的，它们可能是一些官方未收录的软件包或是社区维护的变种。

2. **软件包的组织：**
   - `feeds` 目录下的软件包是按照一定的分类和结构组织的，例如 `feeds/packages/net/` 子目录下包含了网络相关的软件包。
   - `package` 目录之外的软件包组织方式可能因维护者而异，可能是按照不同的分类或结构组织，也可能直接放在 `package` 目录下。

3. **更新频率：**
   - `feeds` 目录中的软件包通常会定期从源仓库同步，保持更新。
   - `package` 目录之外的软件包更新频率可能较低，取决于维护者的更新策略。

综上所述，`package` 目录之外的软件包通常是一些社区维护的或者不符合官方团队标准的软件包。用户在选择使用这些软件包时，需要注意它们的维护状况、更新频率以及与OpenWRT主线的兼容性。

## PACKAGE_librokid-bt:librokid-bt这个名字怎么理解

在OpenWRT的Makefile中，`DEPENDS` 变量用于指定软件包的构建依赖关系。在你提供的示例中，`PACKAGE_librokid-bt:librokid-bt` 是一个构建依赖项的指定，它的格式为：

```plaintext
PACKAGE_NAME:TARGET_NAME
```

这里的 `PACKAGE_librokid-bt` 是一个软件包的名称，而 `librokid-bt` 是该软件包在构建过程中的目标名称或库名称。

解释一下这个依赖项的含义：

- `PACKAGE_librokid-bt` 是一个软件包的名称，表示这是一个名为 `librokid-bt` 的软件包。
  
- `librokid-bt` 是该软件包在构建过程中的目标名称或库名称。这通常表示在构建过程中，该软件包会生成一个名为 `librokid-bt` 的库文件。

整个依赖项的含义是，当前软件包在构建过程中依赖于 `librokid-bt` 软件包，并且在链接时会链接到 `librokid-bt` 库。这通常表示软件包依赖于其他软件包提供的库或功能。

在实际构建过程中，构建系统会自动解析这些依赖关系，并确保在构建当前软件包时，需要的依赖项也会被正确构建和链接。

# Build/InstallDev 和Package/activation/install的关系

`Build/InstallDev` 和 `Package/activation/install` 是两个不同的构建规则，用于不同的目的。让我解释它们之间的关系：

1. **`Build/InstallDev`：** 这是一个构建规则，通常用于定义软件包的开发文件（development files）的安装。开发文件包括头文件、库文件等，它们允许其他软件包在构建时使用当前软件包的功能。这个规则通常在软件包的 Makefile 中定义，用于安装开发文件到目标安装目录。

    例如：
    ```make
    define Build/InstallDev
        $(INSTALL_DIR) $(1)/usr/include
        $(CP) $(PKG_INSTALL_DIR)/usr/include/* $(1)/usr/include/
        $(INSTALL_DIR) $(1)/usr/lib
        $(CP) $(PKG_INSTALL_DIR)/usr/lib/* $(1)/usr/lib/
    endef
    ```

2. **`Package/activation/install`：** 这是一个软件包的安装规则，用于定义软件包的运行时文件（runtime files）的安装。运行时文件包括执行文件、配置文件等，它们用于实际运行软件包。这个规则通常在软件包的 Makefile 中定义，用于安装运行时文件到目标安装目录。

    例如：
    ```make
    define Package/activation/install
        $(INSTALL_DIR) $(1)/usr/bin
        $(INSTALL_BIN) $(PKG_INSTALL_DIR)/usr/bin/* $(1)/usr/bin/
        $(INSTALL_DIR) $(1)/etc
        $(CP) $(PKG_INSTALL_DIR)/etc/* $(1)/etc/
    endef
    ```

关系：
- 在构建软件包时，`Build/InstallDev` 用于安装开发文件，以便其他软件包可以使用当前软件包的头文件和库文件进行编译。
  
- 在软件包的安装阶段，`Package/activation/install` 用于安装运行时文件，将可执行文件和配置文件等安装到目标系统中，以便软件包可以在运行时使用。

这两个规则在构建和安装过程中分别负责不同类型的文件。 `Build/InstallDev` 主要用于开发环境，而 `Package/activation/install` 主要用于目标系统上的运行环境。

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