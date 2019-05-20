---
title: buildroot之树莓派系统编译
date: 2019-05-17 13:27:11
tags:
	- Linux
---



配置：

```
make raspberrypi3_defconfig
```

编译：

```
make ARCH=arm -j16
```

在output目录下，得到sdcard.img文件。

把这个文件用工具烧录到SD卡里。

就可以用这个卡来启动了。

很顺利，直接就运行起来了。

默认是root用户。没有密码。

现在分析一下系统里的内容。

用户

```
# cat /etc/passwd 
root:x:0:0:root:/root:/bin/sh
daemon:x:1:1:daemon:/usr/sbin:/bin/false
bin:x:2:2:bin:/bin:/bin/false
sys:x:3:3:sys:/dev:/bin/false
sync:x:4:100:sync:/bin:/bin/sync
mail:x:8:8:mail:/var/spool/mail:/bin/false
www-data:x:33:33:www-data:/var/www:/bin/false
operator:x:37:37:Operator:/var:/bin/false
nobody:x:65534:65534:nobody:/home:/bin/false
```

磁盘

```
# df -h
Filesystem                Size      Used Available Use% Mounted on
/dev/root               112.2M     56.1M     47.7M  54% /
devtmpfs                447.3M         0    447.3M   0% /dev
tmpfs                   451.8M         0    451.8M   0% /dev/shm
tmpfs                   451.8M     24.0K    451.7M   0% /tmp
tmpfs                   451.8M     16.0K    451.8M   0% /run
```

默认编译的是32位的。

bin目录下的工具

```
# ls
ash            dumpkmap       linux64        nice           sh
busybox        echo           ln             pidof          sleep
cat            egrep          login          ping           stty
chattr         false          ls             pipe_progress  su
chgrp          fdflush        lsattr         printenv       sync
chmod          fgrep          mkdir          ps             tar
chown          getopt         mknod          pwd            touch
cp             grep           mktemp         rm             true
cpio           gunzip         more           rmdir          umount
date           gzip           mount          run-parts      uname
dd             hostname       mountpoint     sed            usleep
df             kill           mt             setarch        vi
dmesg          link           mv             setpriv        watch
dnsdomainname  linux32        netstat        setserial      zcat
```

group有这些：

```
# cat group 
root:x:0:
daemon:x:1:
bin:x:2:
sys:x:3:
adm:x:4:
tty:x:5:
disk:x:6:
lp:x:7:
mail:x:8:
kmem:x:9:
wheel:x:10:root
cdrom:x:11:
dialout:x:18:
floppy:x:19:
video:x:28:
audio:x:29:
tape:x:32:
www-data:x:33:
operator:x:37:
utmp:x:43:
plugdev:x:46:
staff:x:50:
lock:x:54:
netdev:x:82:
users:x:100:
nogroup:x:65534:
```

/etc/profile文件

```
# cat profile
export PATH=/bin:/sbin:/usr/bin:/usr/sbin

if [ "$PS1" ]; then    
        if [ "`id -u`" -eq 0 ]; then
                export PS1='# '
        else
                export PS1='$ '  设置提示符。
        fi
fi

export PAGER='/bin/more' 默认的分页器。
export EDITOR='/bin/vi' 默认的编辑器。

# Source configuration files from /etc/profile.d 执行其他文件。当前就一个umask.sh文件。
for i in /etc/profile.d/*.sh ; do
        if [ -r "$i" ]; then
                . $i
        fi
done
unset i
```

启动命令

```
8250.nr_uarts=1 bcm2708_fb.fbwidth=720 bcm2708_fb.fbheight=480 bcm2708_fb.fbswap=1 vc_mem.mem_base=0x3ec00000 vc_mem.mem_size=0x40000000  root=/dev/mmcblk0p2 rootwait console=tty1 console=ttyAMA0,115200
```

把node、git、make都选配上。还有binutils。opkg。

编译看看。

都是安装在/usr/bin目录下。

```
# node -v
v8.11.4
# npm -v
5.6.0
```

我需要把文件系统做大一点。

放大到2G吧。

现在需要把无线的打开。

安装timezone的。

安装native语言支持。

shell改成bash的。（这个在改成systemv之后才可以选择）。

初始化系统换成systemv的。

把nginx打开。

nfs也打开。

gdb也安装上，gcc也要安装。

要把树莓派打造成一个小型服务器。而且是自己编译出来的。

能不能跑docker？估计够呛。

包管理目前是用opkg。看到可以选择rpm的。



现在编译后，发现有几个问题：

1、镜像太大了。所以我改成300M的先。

2、wlan0网卡没有出来。网上看了下，是需要打开mdev。

在board/raspberrypi目录下，新建interfaces文件。

内容如下：

```
iface lo inet loopback

auto eth0
iface eth0 inet dhcp
    pre-up /etc/network/nfs_check
    wait-delay 15

auto wlan0
iface wlan0 inet dhcp
    pre-up wpa_supplicant -B -Dnl80211 -iwlan0 -c/etc/wpa_supplicant.conf
    post-down killall -q wpa_supplicant
    wait-delay 15

iface default inet dhcp
```

新建wpa_supplicant.conf文件。填入你的wifi信息。

在post-build.sh里加入：

```
cp package/busybox/S10mdev ${TARGET_DIR}/etc/init.d/S10mdev
chmod 755 ${TARGET_DIR}/etc/init.d/S10mdev
cp package/busybox/mdev.conf ${TARGET_DIR}/etc/mdev.conf

cp board/raspberrypi3/interfaces ${TARGET_DIR}/etc/network/interfaces
cp board/raspberrypi3/wpa_supplicant.conf ${TARGET_DIR}/etc/wpa_supplicant.conf
```



我测试时，很容易就出现了文件系统损坏。

暂时不做了。







搭建web服务器。

nodejs工作。







现在默认是busybox的初始化系统。

另外还有systemv、systemd可以选择。



打开uboot支持，比较麻烦。





看看配置文件。

是会下载专门的内核。

```
BR2_LINUX_KERNEL_CUSTOM_REPO_URL="https://github.com/raspberrypi/linux.git"
BR2_LINUX_KERNEL_CUSTOM_REPO_VERSION="33ee56d5927ceff630fbc87e3f5caa409b6ae114"
BR2_LINUX_KERNEL_DEFCONFIG="bcm2709"
```

指定dtb。

```
BR2_LINUX_KERNEL_DTS_SUPPORT=y
BR2_LINUX_KERNEL_INTREE_DTS_NAME="bcm2710-rpi-3-b bcm2710-rpi-cm3"
```

一些特殊的脚本。

```
BR2_ROOTFS_POST_BUILD_SCRIPT="board/raspberrypi3/post-build.sh"
BR2_ROOTFS_POST_IMAGE_SCRIPT="board/raspberrypi3/post-image.sh"
BR2_ROOTFS_POST_SCRIPT_ARGS="--add-pi3-miniuart-bt-overlay"
```

我make menuconfig看一下，发现默认用的是uclibc，我改成glibc的。

默认也没有使用uboot。

board目录下的配置，都是同一个目录。

```
raspberrypi
raspberrypi0 -> raspberrypi
raspberrypi2 -> raspberrypi
raspberrypi3 -> raspberrypi
raspberrypi3-64 -> raspberrypi
```





参考资料

1、Buildroot构建树莓派轻量级的Linux根文件系统

https://blog.csdn.net/apiculate/article/details/79257789

2、buildroot wifi image for raspberry pi 3 does not work

https://raspberrypi.stackexchange.com/questions/69184/buildroot-wifi-image-for-raspberry-pi-3-does-not-work

3、Enabling WiFi and converting the Raspberry Pi into a WiFi AP

https://blog.crysys.hu/2018/06/enabling-wifi-and-converting-the-raspberry-pi-into-a-wifi-ap/