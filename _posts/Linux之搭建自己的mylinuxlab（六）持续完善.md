---
title: Linux之搭建自己的mylinuxlab（六）持续完善
date: 2018-03-18 21:25:34
tags:
	- Linux

---



# 从initramfs转到SD卡的rootfs

我试了一下给qemu加上-sd，是正常的。

我在qemu里对加载进来的SD卡进行写入也是正常的。所以现在可以用SD卡来带文件系统启动看看。

1、生成一个SD卡镜像文件。先不用多大，给64M就行。

```
dd if=/dev/zero of=./sd.img bs=1M count=64
格式化为ext2的。
sudo mkfs.ext2 ./sd.img
```

2、修改rootfs里的init为这样的脚本内容。

```
#!/bin/sh

bb=/bin/busybox
echo "build root filesystem"


if [ ! -d /sys ];then
  echo "/sys dir not exist, create it..."
  $BUSYBOX mkdir /sys
fi

echo "mount proc and sys"
$bb mount -t proc proc /proc
$bb mount -t sysfs sysfs /sys

echo "mount dev tmpfs"
$bb mount -t tmpfs dev /dev

if [ ! -d /dev/pts ];then
  echo "/dev/pts dir not exist, create it..."
  $BUSYBOX mkdir /dev/pts
fi
$bb mount -t devpts devpts /dev/pts


$bb mdev -s

echo "begin switch root to sd card " >> /dev/kmsg

$bb mkdir /newroot

if [ ! -b "/dev/mmcblk0" ]; then
    echo "can't find /dev/mmcblk0, now use the initramfs" >> /dev/kmsg
    echo "drop to shell" >> /dev/kmsg
    $bb sh 
else
    $bb mount /dev/mmcblk0 /newroot
    if [  $? -eq 0 ]; then
        echo "mount rootfs successfully" >> /dev/kmsg
    else
        echo "mount rootfs failed" >> /dev/kmsg
        $bb sh
    fi
fi 
echo "now begin to change to newroot" >> /dev/kmsg
echo "should clean something firstly" >> /dev/kmsg

$bb umount -f /proc
$bb umount -f /sys
$bb umount -f /dev/pts
$bb umount -f /dev

echo "enter new root " >> /dev/kmsg

exec $bb switch_root -c /dev/console /newroot /init

if [  $? -ne 0 ]; then
    echo "enter new root failed, now drop to shell" >> /dev/kmsg
    $bb mount -t proc proc /proc
    $bb sh
fi

exit 0

```

3、修改Makefile和脚本。

让make rootfs可以生成sd.img的内容。

4、make boot就可以了。

启动后，可以看到已经切换到SD卡的了。

```
/ # df -h
Filesystem                Size      Used Available Use% Mounted on
/dev/mmcblk0             62.0M     11.7M     47.1M  20% /
/ # 
```

# 直接从SD卡的rootfs启动

initramfs其实可以没有的。

增加一个boot-sd的Makefile目标。

```
boot-sd:
	$(ROOT_DIR)/ifconfig_tap0.sh &
	qemu-system-arm -M vexpress-a9 -net nic,model=lan9118 -net tap \
	-smp 1 -kernel $(KERNEL_DIR)/arch/arm/boot/zImage  \
	-nographic  -initrd $(ROOT_DIR)/ramfs.gz -dtb $(KERNEL_DIR)/arch/arm/boot/dts/vexpress-v2p-ca9.dtb \
	-append "console=ttyAMA0 root=/dev/mmcblk0 rootfstype=ext2" -sd $(ROOT_DIR)/sd.img
```

现在把从SD卡的rootfs启动改为默认的，make boot的行为。

而之前的改为make boot-ramfs。



# 关闭initrd和initramfs的内核配置

我本来是想要看SD卡里的系统的挂载过程。

但是，加的打印一直看不到。

我就把内核配置里的initrd和initramfs都关闭。

这些对应的mount代码执行到了。

而且挂载的情况显示也不同了。现在是这样的。

```
/ # mount
/dev/root on / type ext2 (rw,relatime,errors=continue)
proc on /proc type proc (rw,relatime)
sysfs on /sys type sysfs (rw,relatime)
devpts on /dev/pts type devpts (rw,relatime,mode=600,ptmxmode=000)
/ # df -h
Filesystem                Size      Used Available Use% Mounted on
/dev/root                62.0M     11.7M     47.1M  20% /
/ # 
```

之前的/dev/root都是显示/dev/mmcblk0 。

不过实际上也就是一个软链接而已。

```
~ # ls /dev/root -l
lrwxrwxrwx    1 root     0                7 Mar 18 15:47 /dev/root -> mmcblk0
```



# telnet登陆问题

我要调试一个程序，会阻塞当前的shell窗口。所以就要打开telnetd，另外telnet连接上去。

但是现在是这样的，我当前确实没有配置用户验证。

所以telnet这里验证就过不去。

```
teddy@teddy-ubuntu:~/work/mylinuxlab/kernel/linux-stable$ telnet 192.168.0.2
Trying 192.168.0.2...
Connected to 192.168.0.2.
Escape character is '^]'.

(none) login: root
Password: 

Login incorrect
```

所以现在的问题就是：

busybox如何添加用户。

我在《busybox之要求输入密码登陆》里已经分析过这个问题了。

我现在先加上root用户。不要密码的。

就是在/etc目录下新建一个passwd文件。

加上这一行。

```
root::0:0:root:/root:/bin/sh
```

然后就可以用telnet以root身份免密码登陆了。

# 增加deb包相关内容

busybox支持deb包的安装，但是不支持制作。

需要增加一些目录，不然

# 在etc目录加上profile文件

当前默认的环境变量是这样的。

```
/ # set
HISTFILE='/.ash_history'
HOME='/'
HOSTNAME='(none)'
IFS=' 
'
OPTIND='1'
PATH='/sbin:/usr/sbin:/bin:/usr/bin'
PPID='1'
PS1='\w \$ '
PS2='> '
PS4='+ '
PWD='/'
SHELL='/bin/sh'
SHLVL='1'
TERM='vt102'
USER='root'
```

这些都是在哪里设置的呢？

一部分是在init.c里，用putenv设置进去的。

```
	putenv((char *) "HOME=/");
	putenv((char *) bb_PATH_root_path);
	putenv((char *) "SHELL=/bin/sh");
	putenv((char *) "USER=root"); /* needed? why? */
```

PATH则是在login里设置的。

```
login_main
	sanitize_env_if_suid
		putenv((char*)bb_PATH_root_path);
		const char bb_PATH_root_path[] ALIGN1 =
	"PATH=/sbin:/usr/sbin:/bin:/usr/bin" BB_ADDITIONAL_PATH;
```

那么现在问题来了，login是谁调用的？

我们只显式调用了-/bin/sh。

我看到getty有调用到login。

但是没有看到我哪里调用了getty。

加上打印看看调用顺序是怎样的。

从打印看，只调用了init_main。getty和login的都没有调用到。

实际的调用情况是：

init_main里的inittab指定了“-/bin/sh”。然后就调用到ash_main了。

ash_main里会read_profile("/etc/profile"); read_profile("$HOME/.profile");

当前的情况是跳过了login这个阶段的。

如果要加上，就改一下inittab。把-sh改成getty。就会有让你登陆的过程了。



# 加入多用户

加入2个带密码的用户。teddy和xhliang。

```
/etc # cat passwd-
root::0:0:root:/:/bin/sh
teddy:Vqj1rLdE/APjI:1000:1000:Linux User,,,:/home/teddy:/bin/sh
xhliang:x:1001:1001:Linux User,,,:/home/xhliang:/bin/sh
/etc # cat passwd
root::0:0:root:/:/bin/sh
teddy:Vqj1rLdE/APjI:1000:1000:Linux User,,,:/home/teddy:/bin/sh
xhliang:cHT9gEtiS2R4o:1001:1001:Linux User,,,:/home/xhliang:/bin/sh
```

添加后的情况是这样的。

把这2个文件保存下来。以后做出来的文件夹默认就带这个。

# 加入syslogd的配置

1、新建/etc/syslogd.conf文件。内容如下：

```
mail.* /var/log/maillog
cron.* /var/log/cron
news.=crit /var/log/news/news.crit
user.* /var/log/userlog
```

2、在rcS脚本里加上动态创建/var目录的语句。算了，还是静态创建吧。

3、脚本里默认启动syslogd。

# 运行thttpd



