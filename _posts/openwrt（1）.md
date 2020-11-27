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