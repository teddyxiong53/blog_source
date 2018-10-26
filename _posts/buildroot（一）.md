---
title: buildroot（一）
date: 2018-03-25 08:30:56
tags:
	- buildroot

---



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



参考资料

1、HOWTO: Use BuildRoot to create a Linux image for QEMU

http://www.osadl.org/Use-BuildRoot-to-create-a-Linux-image-fo.buildroot-qemu.0.html