---
title: buildroot（一）
date: 2018-03-25 08:30:56
tags:
	- buildroot

---

1

# 资料收集

这个gitbook，台湾人写的，不错。

https://hugh712.gitbooks.io/buildroot/content/

写一个系列文章，把buildroot的编译过程梳理一下。

先看顶层Makefile。

```
1、export当前的版本，2012.05 
2、检查make版本，最低要求是3.81
3、不允许在顶层make -j
4、定义TOPDIR
5、配置文件是Config.in。里面内容结构是跟kconfig一样的。
6、输出目录为output目录。
7、包含.config文件。
8、得到shell的名字。
9、定义工具链。
10、
```

```

hlxiong@hlxiong-VirtualBox:~/work2/buildroot/buildroot$ tree -L 1
.
├── arch
├── board
├── boot
├── build
├── CHANGES
├── Config.in
├── Config.in.legacy
├── configs
├── COPYING
├── DEVELOPERS
├── docs
├── fs
├── linux
├── Makefile
├── Makefile.legacy
├── output
├── package
├── README
├── support
├── system
├── toolchain
└── utils
```

默认下来的包，只有4M。解压后是57M。

主要内容都是要靠编译过程中下载的。

查看make help信息。

```
hlxiong@hlxiong-VirtualBox:~/work2/buildroot/buildroot$ make help
Cleaning:
  clean                  - 删除build生成的所有文件。
  distclean              - 删除了配置文件等。

Build:
  all                    - 等价于make world
  toolchain              - 构建工具链build toolchain
  sdk                    - 构建sdk，build relocatable SDK

Configuration:
  menuconfig             - interactive curses-based configurator
  defconfig              - New config with default answer to all options;
                             BR2_DEFCONFIG, if set on the command line, is used as input
  savedefconfig          - Save current config to BR2_DEFCONFIG (minimal config)

Package-specific:
  <pkg>                  - Build and install <pkg> and all its dependencies
  <pkg>-source           - Only download the source files for <pkg>
  <pkg>-extract          - Extract <pkg> sources
  <pkg>-patch            - Apply patches to <pkg>
  <pkg>-depends          - Build <pkg>'s dependencies
  <pkg>-configure        - Build <pkg> up to the configure step
  <pkg>-build            - Build <pkg> up to the build step
  <pkg>-show-depends     - List packages on which <pkg> depends
  <pkg>-show-rdepends    - List packages which have <pkg> as a dependency
  <pkg>-graph-depends    - Generate a graph of <pkg>'s dependencies
  <pkg>-graph-rdepends   - Generate a graph of <pkg>'s reverse dependencies
  <pkg>-dirclean         - Remove <pkg> build directory
  <pkg>-reconfigure      - Restart the build from the configure step
  <pkg>-rebuild          - Restart the build from the build step

Documentation:
  manual                 - build manual in all formats
  manual-html            - build manual in HTML
  manual-split-html      - build manual in split HTML
  manual-pdf             - build manual in PDF
  manual-text            - build manual in text
  manual-epub            - build manual in ePub
  graph-build            - generate graphs of the build times
  graph-depends          - generate graph of the dependency tree
  graph-size             - generate stats of the filesystem size
  list-defconfigs        - list all defconfigs (pre-configured minimal systems)

Miscellaneous:
  source                 - download all sources needed for offline-build
  external-deps          - list external packages used
  legal-info             - generate info about license compliance
  printvars              - dump all the internal variables

  make V=0|1             - 0 => quiet build (default), 1 => verbose build
  make O=dir             - Locate all output files in "dir", including .config

For further details, see README, generate the Buildroot manual, or consult
it on-line at http://buildroot.org/docs.html
```

我现在要构造buildroot，可以在mylinuxlab里用的。

我的mylinuxlab是32位的。

看configs目录下，直接有qemu相关的配置。

1、拷贝默认配置。

```
hlxiong@hlxiong-VirtualBox:~/work2/buildroot/buildroot$ make qemu_x86_64_defconfig
#
# configuration written to /home/hlxiong/work2/buildroot/buildroot/.config
#
```

2、开始编译，把过程打印保存下来，好好研究一下。

下载是很慢的。我挂上代理来下载。

我加上代理，可以ping通Google了。但是下载还是失败。

```
hlxiong@hlxiong-VirtualBox:~/work2/buildroot/buildroot$ export https_proxy=http://localhost:8123
hlxiong@hlxiong-VirtualBox:~/work2/buildroot/buildroot$ export http_proxy=http://localhost:8123
hlxiong@hlxiong-VirtualBox:~/work2/buildroot/buildroot$ 
hlxiong@hlxiong-VirtualBox:~/work2/buildroot/buildroot$ 
hlxiong@hlxiong-VirtualBox:~/work2/buildroot/buildroot$ ping www.google.com
PING www.google.com (14.215.177.38) 56(84) bytes of data.
64 bytes from 14.215.177.38: icmp_seq=1 ttl=55 time=8.15 ms
64 bytes from 14.215.177.38: icmp_seq=2 ttl=55 time=9.91 ms
^C
--- www.google.com ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 8.153/9.036/9.919/0.883 ms
hlxiong@hlxiong-VirtualBox:~/work2/buildroot/buildroot$ make
>>> host-lzip 1.19 Downloading
--2018-10-26 11:09:53--  http://download.savannah.gnu.org/releases/lzip/lzip-1.19.tar.gz
正在解析主机 localhost (localhost)... 127.0.0.1
正在连接 localhost (localhost)|127.0.0.1|:8123... 已连接。
```

我选择在Linux上使用ssr客户端的方式来做。这样可以了。

下载还是比较耗时的。我一边看看配置文件。

接近4000行。我用的是qemu_x86_64_defconfig的。

配置文件组成

```
1、gcc版本要求。
2、target选项。
	64位。
	MMU
	MMX
3、build选项。
4、命令。
	wget的选项。
	svn
	git等。
5、下载地址。
6、工具链。
	使用了ulibc。
7、Linux header。
8、uclibc选项。
9、binutils选项。
10、gcc选项。
11、系统配置。
	初始化系统。用busybox的。
12、kernel配置。
13、接下来就是各种包配置了。

```

先暂时不细究这些配置。

在make xxx_defconfig之后，目录产生的变化：

1、产生了output目录。这里把buildroot-config这个工具编译了，生成在这里。

2、顶层目录有一个.config文件生成。



采取的编译方法是把压缩包都解压到output/build目录下进行的编译。

看board/qemu/x86_64目录的reame.txt。这个是运行命令。

```
qemu-system-x86_64 -M pc -kernel output/images/bzImage -drive file=output/images/rootfs.ext2,if=virtio,format=raw -append "root=/dev/vda" -net nic,model=virtio -net user
```



从我的ssr的日志看，期间连接了这些地址进行了下载。

```
connecting download.savannah.gnu.org:80 from 127.0.0.1:35712
connecting download-mirror.savannah.gnu.org:80 from 127.0.0.1:35716
connecting ftpmirror.gnu.org:80 from 127.0.0.1:35722
connecting mirror.team-cymru.com:80 from 127.0.0.1:35726
connecting ftpmirror.gnu.org:80 from 127.0.0.1:35732
connecting gnu.askapache.com:80 from 127.0.0.1:35736
connecting mirror.team-cymru.com:80 from 127.0.0.1:35742
connecting www.mpfr.org:80 from 127.0.0.1:35748
connecting www.mpfr.org:443 from 127.0.0.1:35754
connecting ftpmirror.gnu.org:80 from 127.0.0.1:35760
connecting mirror.us-midwest-1.nexcess.net:80 from 127.0.0.1:35764
connecting mirror.keystealth.org:80 from 127.0.0.1:35770
connecting cdn.kernel.org:443 from 127.0.0.1:35776
connecting downloads.uclibc-ng.org:80 from 127.0.0.1:35782
connecting downloads.uclibc-ng.org:443 from 127.0.0.1:35788
connecting www.busybox.net:80 from 127.0.0.1:35794
connecting busybox.net:443 from 127.0.0.1:35800
connecting github.com:443 from 127.0.0.1:35806
connecting github-production-release-asset-2e65be.s3.amazonaws.com:443 from 127.0.0.1:35812
connecting www.zlib.net:80 from 127.0.0.1:35818
connecting cdn.kernel.org:443 from 127.0.0.1:35824
connecting cdn.kernel.org:443 from 127.0.0.1:35830
connecting releases.nixos.org:80 from 127.0.0.1:35836
connecting sources.buildroot.net:80 from 127.0.0.1:35842
connecting cdn.kernel.org:443 from 127.0.0.1:35848
connecting download.savannah.gnu.org:80 from 127.0.0.1:35854
connecting nongnu.askapache.com:80 from 127.0.0.1:35858
connecting download-mirror.savannah.gnu.org:80 from 127.0.0.1:35864
connecting snapshot.debian.org:80 from 127.0.0.1:35870
```



可以保存的日志的阅读方法，可以通过`>>>`搜索来查看。

```
>>>   Finalizing target directory
```



但是运行，碰到了问题。

就是无法运行。需要图形界面支持。

所以，还是编译一个arm的。

```
make qemu_arm_vexpress_defconfig
```

看会下载一个不同版本的Linux。

直接编译，会出错。需要make clean一下。

不然工具链会不对。

编译完了，也挺快的。

运行指令：

```
qemu-system-arm -M vexpress-a9 -smp 1 -m 256 -kernel output/images/zImage -dtb output/images/vexpress-v2p-ca9.dtb -drive file=output/images/rootfs.ext2,if=sd,format=raw -append "console=ttyAMA0,115200 root=/dev/mmcblk0"  -net nic,model=lan9118 -net user -nographic
```

根据readme.txt内容修改：增加-nographic，去掉-serial stdio。

如果是在图形界面下运行，可以按原样来做

```
qemu-system-arm -M vexpress-a9 -smp 1 -m 256 -kernel output/images/zImage -dtb output/images/vexpress-v2p-ca9.dtb -drive file=output/images/rootfs.ext2,if=sd,format=raw -append "console=ttyAMA0,115200 root=/dev/mmcblk0"  -net nic,model=lan9118 -net user -serial stdio
```



运行：用户是root，密码是空。

```
deleting routers
adding dns 10.0.2.3
OK

Welcome to Buildroot
buildroot login: 
Welcome to Buildroot
buildroot login: root
# 
# 
# 
# ls
# df -h
Filesystem                Size      Used Available Use% Mounted on
/dev/root                58.1M      2.6M     52.5M   5% /
devtmpfs                122.5M         0    122.5M   0% /dev
tmpfs                   123.0M         0    123.0M   0% /dev/shm
tmpfs                   123.0M     24.0K    123.0M   0% /tmp
tmpfs                   123.0M     20.0K    123.0M   0% /run
```

如果要定制自己的配置文件，就make menuconfig，然后保存到configs目录下。

看看配置项怎样传递给kernel的。

怎样传递给busybox的。

靠的是package目录下的busybox/busybox.config这个文件来做的。



文件系统情况。

```
# df -h
Filesystem                Size      Used Available Use% Mounted on
/dev/root                58.1M      2.6M     52.5M   5% /
devtmpfs                122.5M         0    122.5M   0% /dev
tmpfs                   123.0M         0    123.0M   0% /dev/shm
tmpfs                   123.0M     24.0K    123.0M   0% /tmp
tmpfs                   123.0M     20.0K    123.0M   0% /run
```

文件系统介质的大小哪里改呢？

menuconfig里有配置的地方。我改为512M的。

勾选上make和git这2个组件。然后make。

把我下载的东西，都上传到百度云盘保存下来，这样我在其他地方搭建buildroot环境的时候，就不需要重新下载这些包了。

这些package都是开源代码学习的好材料。

这个环境开源作为各种脚本的测试环境。

现在把重要的包都下载好。

音频视频类

1、alsa-utils。

2、ffmpeg。

压缩类

1、zip

2、bzip。

调试类

1、strace。

2、uclibc-ng-test

开发工具：

1、git

2、make

文件系统

1、nfs。

2、mmc-utils

脚本类

1、micropython

2、lua。

3、php

网络类

1、boa。一个webserver。

2、dhcpcd。

3、dropbear。

4、hostapd。

5、iperf3.

6、iputils。

7、lighttpd。

8、openssh。

9、rsync。

10、tinyhttpd。

11、uhttpd。

12、wpa_supplicant

13、

shell类

1、file命令。

2、sudo命令。

系统工具类

1、cpuload。

差不多就这些了。编译一把。

虽然挂了代理，但是有些东西下载还是慢。从其他地方下载，放到dl目录下就好了。



可以尝试一下其他的init system。看看区别何在。

现在启动时打印。

```
eth0: soliciting a DHCP lease
eth0: offered 10.0.2.15 from 10.0.2.2
eth0: leased 10.0.2.15 for 86400 seconds
eth0: adding route to 10.0.2.0/24
eth0: adding default route via 10.0.2.2
forked to background, child pid 810
Starting dropbear sshd: OK
Starting lighttpd: OK
ssh-keygen: generating new host keys: RSA DSA ECDSA ED25519 
Starting sshd: OK
Starting NFS statd: OK
Starting NFS services: exportfs: can't open /run/nfs/xtab for reading
FAIL
Starting NFS daemon: rpc.nfsd: Unable to access /proc/fs/nfsd errno 2 (No such file or directory).
Please try, as root, 'mount -t nfsd nfsd /proc/fs/nfsd' and then restart rpc.nfsd to correct the problem
FAIL
Starting NFS mountd: OK
Starting tinyhttpd: done
bind: Address already in use
```



make savedefconfig这个是很有用的。

```
make savedefconfig
cp defconfig configs/<boardname>_defconfig
```

Once you have a known working configuration, run `make savedefconfig`. This will generate a minimal `defconfig` file at the root of the Buildroot source tree. Move this file into the `configs/` directory, and rename it `<boardname>_defconfig`. 

The recommended place to store this defconfig is `configs/<boardname>_defconfig`. If you follow this recommendation, the configuration will be listed in `make help` and can be set again by running `make <boardname>_defconfig`. 



从实际操作来看。



```
qemu-system-i386 -M pc -kernel output/images/bzImage -drive file=output/images/rootfs.ext2,if=virtio,format=raw -append "root=/dev/vda" -net nic,model=virtio -net user -nographic
```

```

qemu-system-arm -M vexpress-a9 -smp 1 -m 256 -kernel output/images/zImage -dtb output/images/vexpress-v2p-ca9.dtb -drive file=output/images/rootfs.ext2,if=sd,format=raw -append "console=ttyAMA0,115200 root=/dev/mmcblk0"  -net nic,model=lan9118 -net user -nographic

```



# make file

这个是编译file这个工具。

从编译过程的打印看，会先编译host的，然后编译板端的。

而且会先打补丁。



# 依赖关系

在我们新增自己的package的时候，往往可能依赖了某些其他的包。需要先把其他的包编译完了才能编译我们的包。

所以需要添加依赖。

```
在在mk文件里。添加这个。
XX_DEPENDANCIES += yy
```

在Config.in里，depends on并不会产生这种编译依赖。



# 深入

还是看顶层Makefile。

help信息里。

## graph-build

```

	这个是通过读取output/build/build-time.log来生成图表，可以直观看出编译花费的时间细节。
	执行出错
	You need python-matplotlib and python-numpy to generate build graphs
	但是我用apt-get来安装这2个软件，提示是已经安装的。
	是靠这个脚本的。support/scripts/graph-build-time
	import matplotlib as mpl
	import numpy
	这2句产生了import错误。
	
```

直接打开python。进入交互，import matplotlib，报错如下：

```
ImportError: No module named functools_lru_cache
```

把python版本切换到3.6，就可以了。

输出目录是：

output/graphs/build.hist-name.pdf 

没有太多可看的。

## graph-depends

这个生成包的依赖关系图。倒是值得看看。

## graph-size

这个可以看rootfs里各个部分的大小。

## legal-info

## printvars

这个会打印出所有的var的名字和值（Makefile里的）。

非常多。

## list-defconfigs

这个是一个目标。

有一个同名的宏定义。

```
define list-defconfigs
	
endef
```

就是把configs目录下的所有defconfig罗列了一下。

## show-targets

这个是列出实际的target。

我当前的vexpress的例子。是这样。demo_app是我自己加的一个package。

```
alsa-lib
alsa-utils
atest
busybox
demo_app
glibc
host-e2fsprogs
host-fakeroot
host-lzip
host-makedevs
host-patchelf
host-util-linux
ifupdown-scripts
initscripts
libeXosip2
libev
libogg
libosip2
linphone
linux
linux-headers
ncurses
skeleton
skeleton-init-common
skeleton-init-sysv
speex
toolchain
toolchain-buildroot
rootfs-ext2
```

## dirs

这个是创建所有需要的目录。

## prepare

```
prepare: $(BUILD_DIR)/buildroot-config/auto.conf
```

只是依赖auto.conf这个文件。

这个文件依赖：

```
$(BUILD_DIR)/buildroot-config/auto.conf: $(BR2_CONFIG)
	$(MAKE1) $(EXTRAMAKEARGS) HOSTCC="$(HOSTCC_NOCCACHE)" HOSTCXX="$(HOSTCXX_NOCCACHE)" silentoldconfig
```

```
$(BR2_CONFIG)
	这个就是.config文件。
	
```

## sdk

```
.PHONY: world
world: target-post-image

.PHONY: sdk
sdk: world
```

make sdk依赖于make world。

在world的基础上，做了

```
1、调用support/scripts/fix-rpath host 
2、调用support/scripts/fix-rpath staging
3、安装一个脚本。
	$(INSTALL) -m 755 $(TOPDIR)/support/misc/relocate-sdk.sh $(HOST_DIR)/relocate-sdk.sh
	
```

target-post-image

这个目标做了什么。

```
依赖与$(TARGETS_ROOTFS) target-finalize。
是Executing post-image script

```

BR2_ROOTFS_POST_IMAGE_SCRIPT

这个变量里，包含了哪些脚本？

## show-build-order

显示编译的顺序。

## prepare-kconfig

```
menuconfig: $(BUILD_DIR)/buildroot-config/mconf prepare-kconfig
```

mconf这个是二进制文件。

```
prepare-kconfig: outputmakefile $(BUILD_DIR)/.br2-external.in
```

outputmakefile 这个是空的目标，等于啥也不做。

br2-external.in这个是这样，靠br-external脚本来生成。

```
$(BUILD_DIR)/.br2-external.in: $(BUILD_DIR)
	$(Q)support/scripts/br2-external -k -o "$(@)" $(BR2_EXTERNAL)
```

br-external脚本是怎样工作的？不管先。

## savedefconfig

这个做了什么。

就是保存了配置到configs目录下。



## world

```
world只是依赖了target-post-image
target-post-image是个伪目标。
依赖了$(TARGETS_ROOTFS) target-finalize。
进行的操作是执行post image脚本。vexpress这个设备没有post image脚本需要处理。

重点是这个：
target-finalize: $(PACKAGES)

```



```
PACKAGES += $(DEPENDENCIES_HOST_PREREQ)
```



参考资料

1、HOWTO: Use BuildRoot to create a Linux image for QEMU

http://www.osadl.org/Use-BuildRoot-to-create-a-Linux-image-fo.buildroot-qemu.0.html

2、My 6 tips for working with Buildroot

https://www.viatech.com/en/2015/06/buildroot/

3、

https://www.cnblogs.com/tfanalysis/p/3643308.html

4、buildroot架构

https://hugh712.gitbooks.io/buildroot/content/default-path.html

5、buildroot里增加自己的包。

http://www.mamicode.com/info-detail-2460329.html

6、buildroot重新编译package

https://blog.csdn.net/qq_31811537/article/details/81069993