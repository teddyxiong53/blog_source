---
title: Linux发行版之alpine
date: 2018-01-26 10:37:51
tags:
	- Linux发行版

---



前段时间学习docker的时候，接触到alpine这个Linux发行版，特点是小。小才适合研究。

我看docker那边的alpine基础镜像只有5M左右。而Ubuntu的是180M。

alpine的字母意思是高山。

官网上给的宣传字样是：Small、Simple、Secure。



# alpine特点

https://www.alpinelinux.org/downloads/

这里选择x86的standard版本。3.7版本的。只有83M。官网的下载速度也不错。

## Small

1、基于musl libc和busybox。

## Simple

1、提供了自己的包管理器。apk。

2、OpenRC init系统。这个是一个对应systemd的程序。

## Secure

1、集成了Pax/GRSecurity特性的内核。

2、所有用户可执行文件编译为PIE模式，这个前瞻性的特性可以有效避免0day漏洞（不太懂）。



# 安装过程

1、新建一个虚拟机，就选择Ubuntu类型的。命名为vm_alpine_0，我加上数字编号，就是我可能会建立多个这个类型的虚拟机。

2、把iso插入到虚拟机，然后开机。

3、开机后，没有图形界面的。登录，用户名是root，没有密码。

4、看上面的提示说，输入`setup-alpine`进行安装。

5、然后选择键盘类型，输入`us`。然后是选择键盘变种，还是输入：`us`。

6、然后让你输入hostname，输入：`vm-alpine-0`。这里不让输入下划线的。

7、然后配置eth0，按默认的来。

8、然后让你改root密码，太简单也不让过。

9、选择时区，默认UTC，不改了。

10、是否选择proxy，默认是none。默认。你输入回车后，会给出一个列表，默认选择了f，是自动选择速度最快的镜像站点。是配置包管理器下载的站点。

然后会自动逐个测试下载速度。

我看快的在0.6s，有的连接不上，有的6s。

较快的是http://dl-cdn.alpinelinux.org/alpine

最后选择了一个日本的站点。我还是选择dl-cdn这个，实际下载速度比日本那个快很多。

11、自动更新仓库的index。这一步有点慢。要2分钟左右。

12、提示选择ssh server，默认是openssh，用默认。

13、提示选择ntp client。默认是chrony。我选择busybox的，避免下载。

14、然后选择硬盘相关配置。默认apk缓存目录：/var/cache/apk

但是做完这些，没有看到启动后有内容。

到wiki上查了一下：https://wiki.alpinelinux.org/wiki/Installation

alpine有三种模式：

1、无盘模式。

2、data模式。

3、sys模式。

sys模式是一个传统的硬盘安装模式。

15、重启，按照上面的一路继续，第14步，输入sda，而不是选择默认的none。

但是我又碰到了错误。

```
alpine unsatisfiable contraints  sfdisk missing 
另外还提示了syslinux
```

从这个意思上看，是这2个软件包缺失。我直接

```
apk add sfdisk
```

没有成功。

我做了这些操作：

```
# 1. setup-dns ，默认敲了几下。ping www.sina.com是可以通的。网络没有问题。
# 2. apk 仓库重新建立了一下，应该是setup-什么，忘了。看tab提示就知道了。
# 3. setup-alpine重新来一遍，现在到第15步就可以正常往下走了。
看到把sda格式化了3个分区，sda1是是给了/mnt/boot，sda3用来安装系统了。
这一步要花费几分钟。
```

16、然后提示安装完成，让你reboot。



# ssh连接

之前的安装过程中选择了openssh，但是现在连接不上。卸载掉。

```
apk del openssh
```

整个过程打印很清晰。

搜索一下有哪些ssh软件可以安装。

```
apk search ssh
```

找到dropbear。安装。

```
apk add dropbear
```



https://distrowatch.com/table.php?distribution=alpine&pkglist=true&version=3.3.0

这里有alpine的软件包的列表。

http://mirrors.gigenet.com/alpinelinux/v3.5/main/x86/

这个也是。

dropbear试了也是不行。还是回到openssh。仔细看看怎么配置才好。

现在可以了。配置正常的sshd_config文件如下。

之前的问题：

1、public key的问题。

2、root用户登录的问题。

我现在的解决方法，不要public 可以，允许root用户远程登录。

改动点（主要看下面没有被注释掉的行，因为默认都是注释的，注释内容就是默认值）：

1、

```
PermitRootLogin yes
StrictModes no
```

2、

```
PubkeyAuthentication no
```

3、

```
PasswordAuthentication yes
PermitEmptyPasswords yes
```



```
#       $OpenBSD: sshd_config,v 1.101 2017/03/14 07:19:07 djm Exp $

# This is the sshd server system-wide configuration file.  See
# sshd_config(5) for more information.

# This sshd was compiled with PATH=/bin:/usr/bin:/sbin:/usr/sbin

# The strategy used for options in the default sshd_config shipped with
# OpenSSH is to specify options with their default value where
# possible, but leave them commented.  Uncommented options override the
# default value.

#Port 22
#AddressFamily any
#ListenAddress 0.0.0.0
#ListenAddress ::

#HostKey /etc/ssh/ssh_host_rsa_key
#HostKey /etc/ssh/ssh_host_dsa_key
#HostKey /etc/ssh/ssh_host_ecdsa_key
#HostKey /etc/ssh/ssh_host_ed25519_key

# Ciphers and keying
#RekeyLimit default none

# Logging
#SyslogFacility AUTH
#LogLevel INFO

# Authentication:

#LoginGraceTime 2m
PermitRootLogin yes
StrictModes no
#MaxAuthTries 6
#MaxSessions 10

PubkeyAuthentication no

# The default is to check both .ssh/authorized_keys and .ssh/authorized_keys2
# but this is overridden so installations will only check .ssh/authorized_keys
#AuthorizedKeysFile     .ssh/authorized_keys

#AuthorizedPrincipalsFile none

#AuthorizedKeysCommand none
#AuthorizedKeysCommandUser nobody

# For this to work you will also need host keys in /etc/ssh/ssh_known_hosts
#HostbasedAuthentication no
# Change to yes if you don't trust ~/.ssh/known_hosts for
# HostbasedAuthentication
#IgnoreUserKnownHosts no
# Don't read the user's ~/.rhosts and ~/.shosts files
#IgnoreRhosts yes

# To disable tunneled clear text passwords, change to no here!
PasswordAuthentication yes
PermitEmptyPasswords yes

# Change to no to disable s/key passwords
#ChallengeResponseAuthentication yes

# Kerberos options
#KerberosAuthentication no
#KerberosOrLocalPasswd yes
#KerberosTicketCleanup yes
#KerberosGetAFSToken no

# GSSAPI options
#GSSAPIAuthentication no
#GSSAPICleanupCredentials yes

# Set this to 'yes' to enable PAM authentication, account processing,
# and session processing. If this is enabled, PAM authentication will
# be allowed through the ChallengeResponseAuthentication and
# PasswordAuthentication.  Depending on your PAM configuration,
# PAM authentication via ChallengeResponseAuthentication may bypass
# the setting of "PermitRootLogin without-password".
# If you just want the PAM account and session checks to run without
# PAM authentication, then enable this but set PasswordAuthentication
# and ChallengeResponseAuthentication to 'no'.
#UsePAM no

#AllowAgentForwarding yes
#AllowTcpForwarding yes
#GatewayPorts no
#X11Forwarding no
#X11DisplayOffset 10
#X11UseLocalhost yes
#PermitTTY yes
#PrintMotd yes
#PrintLastLog yes
#TCPKeepAlive yes
#UseLogin no
#PermitUserEnvironment no
#Compression delayed
#ClientAliveInterval 0
#ClientAliveCountMax 3
#UseDNS no
#PidFile /run/sshd.pid
#MaxStartups 10:30:100
#PermitTunnel no
#ChrootDirectory none
#VersionAddendum none

# no default banner path
#Banner none

# override default of no subsystems
Subsystem       sftp    /usr/lib/ssh/sftp-server

# the following are HPN related configuration options
# tcp receive buffer polling. disable in non autotuning kernels
#TcpRcvBufPoll yes
 
# disable hpn performance boosts
#HPNDisabled no

# buffer size for hpn to non-hpn connections
#HPNBufferSize 2048


# Example of overriding settings on a per-user basis
#Match User anoncvs
#       X11Forwarding no
#       AllowTcpForwarding no
#       PermitTTY no
#       ForceCommand cvs server
```



# 系统情况查看

1、占用空间343M。比我想象的大。

2、硬盘sda的分区情况：

```
Device  Boot StartCHS    EndCHS        StartLBA     EndLBA    Sectors  Size Id Type
/dev/sda1 *  0,32,33     12,223,19         2048     206847     204800  100M 83 Linux
Partition 1 does not end on cylinder boundary
/dev/sda2    12,223,20   269,94,17       206848    4327423    4120576 2012M 82 Linux swap
Partition 2 does not end on cylinder boundary
/dev/sda3    269,94,18   562,212,34     4327424   41943039   37615616 17.9G 83 Linux
Partition 3 does not end on cylinder boundary
```

可见，sda2做了swap分区。



# 版本情况

我安装的是2017年底发布的3.7.0版本。

看看这个版本的情况。

## 新特性

1、支持EFI。

2、支持grub bootloader。

## 重要更新

1、gcc6.4 

2、llvm5.0

##最近的开发活动

1、开发是基于git来做的。



# 参与进去

1、注册了账号。https://bugs.alpinelinux.org/projects/alpine/issues



分析一下项目的情况。

看看这个提交记录。

https://git.alpinelinux.org/cgit/abuild/commit/?id=e970c74b0e3117c2172cbda45985c9e592c72fcc

看commit这个标签下的内容。

```

author	Natanael Copa <ncopa@alpinelinux.org>	2018-01-02 14:22:42 +0100
committer	Natanael Copa <ncopa@alpinelinux.org>	2018-01-02 14:22:42 +0100
commit	e970c74b0e3117c2172cbda45985c9e592c72fcc (patch)
tree	1d70a0ceca911d997ad2df98be309111ea6e834b
parent	d007f7967c7e4d253dcb4eb6204022f2996e4bc3 (diff)
download	abuild-e970c74b0e3117c2172cbda45985c9e592c72fcc.tar.bz2
```

1、`+0100`表示跟UTC加了1个小时，这个时间是东一区的时间。

2、Natanael Copa这个不知是否这个项目的主导者。

网上看到一段话：

```
1月底,Docker公司创始人Solomon曾经说道,Alpine Linux的创始人Natanael Copa已经加入Docker,他正在将Docker的官方镜像包从Ubuntu切换到Alpine。
```

abuild是构建工具。用来编译alpine linux的包的。

翻了一下log，大概有1050次的提交记录。

第一次提交是2008年10月18日。

第一次提交是3个文件：

```
Makefile
abuild
abuild.conf
```

现在最新的版本是abuild-3.1.0.tar.bz2 。大概30个文件，都是脚本。



alpine的子项目有：

1、build tools。

2、documentation。

3、infrastructure。

4、package keeper。

5、setup script

6、AWall

# 仓库加速

国内也是可以进行加速的。用阿里云的。

```
https://mirrors.aliyun.com/alpine/v3.7/main/
https://mirrors.aliyun.com/alpine/v3.7/community/
```

