---
title: openwrt（一）
date: 2018-04-10 15:29:44
tags:
	- openwrt
typora-root-url: ..\
---



#编译

现在自己来编译openwrt。

从github上下载代码压缩包。make过程中才去下载大量的东西。这个是比较麻烦的一步，因为有很多的编译错误要解决，还有联网下载的东西，在国内的网络环境下，都比较慢，最好带着翻墙工具来做。

我们先看看压缩包的内容：

```
teddy@teddy-ubuntu:~/work/openwrt/tmp/openwrt-master$ tree -L 1
.
├── BSDmakefile
├── config：这个目录下，是几个配置文件。
├── Config.in
├── feeds.conf.default
├── include：全部是mk文件。
├── LICENSE
├── Makefile
├── package：应该用来跟标准的kernel、boot、rootfs进行合并用的特别代码文件。
├── README
├── rules.mk
├── scripts：shell和perl脚本。
├── target：也是一项特别的c文件。
├── toolchain：工具链的补丁。
└── tools：工具的补丁。
```

执行make后，会多出这些目录。

```
1、build_dir。
	这个下面有有3个子目录。都是编译输出的内容。
	host
	target
	toolchain
2、dl目录。
	make过程中下载的内容都在这里。
3、staging_dir。
	跟build_dir类型。
4、tmp。
	这里放一些临时文件。
5..config文件。
	配置文件。
```

编译过程是：

1、make menuconfig。

选择树莓派的方案。

2、make。

这里面会出现很多的错误。一个个解决。

这个编译还有一个比较烦人的问题，就编译不给详细打印。有时候卡住很久。

```
make V=99 -j4
```

V为什么要给99？我也是网上看到 。还有V=s的。但是我V=1，好像没有看到太多打印。

99和s是等价的。在include/verbose.mk里。

```
ifeq ($(OPENWRT_VERBOSE),1)
  OPENWRT_VERBOSE:=w
endif
ifeq ($(OPENWRT_VERBOSE),99)
  OPENWRT_VERBOSE:=s
endif
```



这样编译了10几分钟，编译通过。因为我之前编译过一次，已经下载完成了大部分的文件。

编译完成，需要关注的就是bin目录下的内容。

```
└── targets
    └── brcm2708
        └── bcm2708
            ├── config.seed
            ├── openwrt-brcm2708-bcm2708-device-rpi.manifest
            ├── openwrt-brcm2708-bcm2708-rpi-ext4-sdcard.img.gz  #这个就是我们要关注的。
```

我之前直接下载的镜像文件是这样：

```
lede-17.02.0-rc1-brcm2708-bcm2710-rpi-3-ext4-sdcard-angelina-ace-201760714.img
```



# 烧录到树莓派上

1、我们把bin/targets/bcm2708/bcm2708/open-bcm2708-bcm2708-rpi-ext4-sdcard.img.gz文件解压。

```
teddy@teddy-ubuntu:~/work/openwrt/openwrt-master/bin/targets/brcm2708/bcm2708$ gzip -d openwrt-brcm2708-bcm2708-rpi-ext4-sdcard.img.gz 
```

解压后的大小是284M。

```
-rw-r--r-- 1 teddy teddy 284M 4月  10 16:02 openwrt-brcm2708-bcm2708-rpi-ext4-sdcard.img
```

我之前下载的lede的img文件是1.02G。确实大了很多。

2、我们用Win32DiskImager工具，把解压搭建镜像文件烧录到U盘里。

因为默认配置的cmdline是从 SD卡的分区启动的，所以我们烧录后，要通过pc把boot分区的配置改一下。

把cmdline.txt修改为：

```
dwc_otg.lpm_enable=0 console=serial0,115200 kgdboc=serial0,115200 console=tty1 root=/dev/sda2  rootfstype=ext4 rootwait
```

3、把U盘插到树莓派上，启动，发现启动不了。串口没有看到打印。

我查看我之前写的树莓派从U盘启动的文章。发现还需要在config.txt里加上这些：

```
program_usb_boot_mode=1 #我觉得当前的关键在这里。
enable_uart=1 #这个当前已经有了。
start_x=0 #这个可以没有。加上也没事。
```

如果还不行，我还得替换start.elf和bootcode.bin文件。

确实还是不行，我从我其他的树莓派的机器里，拷贝start.elf和bootcode.bin文件。

发现是我的串口弄错了。串口1不是我插入的usb串口。

不知道为什么当前这个usb口识别不了我的串口，我换个usb口就好了。

如果还是不行的话，就用SD卡看看。

换SD卡的还是不行。算了。先不管了。

我先用现成的镜像来启动。

之前可以的镜像，现在怎么也不行了？我把U盘换了个usb口插入就可以了。

# 开机后基本情况

```
BusyBox v1.25.1 () built-in shell (ash)

     _________
    /        /\      _    ___ ___  ___
   /  LE    /  \    | |  | __|   \| __|
  /    DE  /    \   | |__| _|| |) | _|
 /________/  LE  \  |____|___|___/|___|                      lede-project.org
 \        \   DE / -----------------------------------------------------------
  \    LE  \    /   Reboot (17.01.2, r3435-65eec8bd5f)
   \  DE    \  /    Build By:Angelina_ACE
    \________\/    -----------------------------------------------------------

=== WARNING! =====================================
There is no root password defined on this device!
Use the "passwd" command to set up a new password
in order to prevent unauthorized SSH logins.
--------------------------------------------------
root@LEDE:/# 上面这里提示，root用户没有配置密码的。
root@LEDE:/# 
```

磁盘的基本情况是这样：

```
root@LEDE:/# df -h
Filesystem                Size      Used Available Use% Mounted on
/dev/root              1007.9M    323.9M    668.0M  33% /
tmpfs                    60.7M      3.2M     57.4M   5% /tmp
tmpfs                   512.0K         0    512.0K   0% /dev
```

只用了1个G空间。

文件系统情况：

```
root@LEDE:/# mount
/dev/sda2 on / type ext4 (rw,noatime,block_validity,delalloc,barrier,user_xattr)
proc on /proc type proc (rw,nosuid,nodev,noexec,noatime)
sysfs on /sys type sysfs (rw,nosuid,nodev,noexec,noatime)
tmpfs on /tmp type tmpfs (rw,nosuid,nodev,noatime)
tmpfs on /dev type tmpfs (rw,nosuid,relatime,size=512k,mode=755)
devpts on /dev/pts type devpts (rw,nosuid,noexec,relatime,mode=600)
debugfs on /sys/kernel/debug type debugfs (rw,noatime)
```

#openwrt通过路由器联网

其实这里要做的，就是让openwrt成为一个中间节点。拓扑结构是这样的：

```
手机 --> 树莓派openwrt --> 路由器 --> internet
```

所以openwrt要做一个转发。它还要是一个wifi热点。

1、配置树莓派的eth0的ip地址。

```
ifconfig eth0 192.168.0.100 netmask 255.255.255.0
route add default gw 192.168.0.1
```

2、看看能不能ping通我的路由器。

无法ping通。

我拔插了一下网线，有这个打印。

```
root@LEDE:~# [ 1144.653140] smsc95xx 1-1.1:1.0 eth0: link down
[ 1144.658916] br-lan: port 1(eth0) entered disabled state
[ 1146.229631] smsc95xx 1-1.1:1.0 eth0: link up, 100Mbps, full-duplex, lpa 0xCDE1
[ 1146.240215] br-lan: port 1(eth0) entered forwarding state
[ 1146.246800] br-lan: port 1(eth0) entered forwarding state
[ 1148.245794] br-lan: port 1(eth0) entered forwarding state
```

openwrt的配置文件大部分都在/etc/config目录下。这个是自己的一套规则，跟Ubuntu那些不是一套规则。

我在这个目录下，把eth0的网卡地址改为192.168.0.100，我的路由器分配都是在192.168.0.x这个网段。

把系统重启。

看到eth0的ip地址还是没有自动配置，但是这一次，我手动配置后，就可以ping通了。

现在我们的openwrt自己已经可以ping通外网了。

接下来要让我们的手机可以连接到树莓派产生的热点上。

默认的配置/etc/config/wireless是这样的。

```
config wifi-device 'radio0'
        option type 'mac80211'
        option channel '11'
        option hwmode '11g'
        option path 'platform/soc/3f300000.mmc/mmc_host/mmc1/mmc1:0001/mmc1:
0001:1'
        option htmode 'HT20'
        option disabled '1'

config wifi-iface 'default_radio0'
        option device 'radio0'
        option network 'lan'
        option mode 'ap'
        option ssid 'LEDE'
        option encryption 'none'
```

现在系统里的网卡情况是：

```
root@LEDE:/etc/config# ifconfig -a
br-lan    Link encap:Ethernet  HWaddr B8:27:EB:00:4E:CA  
          inet addr:192.168.0.100  Bcast:192.168.0.255  Mask:255.255.255.0
          inet6 addr: fe80::ba27:ebff:fe00:4eca/64 Scope:Link
          inet6 addr: fda9:2172:1e8c::1/60 Scope:Global
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:378 errors:0 dropped:0 overruns:0 frame:0
          TX packets:144 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:33407 (32.6 KiB)  TX bytes:12730 (12.4 KiB)

eth0      Link encap:Ethernet  HWaddr B8:27:EB:00:4E:CA  
          inet addr:192.168.0.100  Bcast:192.168.0.255  Mask:255.255.255.0
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:378 errors:0 dropped:0 overruns:0 frame:0
          TX packets:149 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:33407 (32.6 KiB)  TX bytes:14576 (14.2 KiB)

gre0      Link encap:UNSPEC  HWaddr 00-00-00-00-FF-00-00-00-00-00-00-00-00-00-00-00  
          NOARP  MTU:1476  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1 
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

gretap0   Link encap:Ethernet  HWaddr 00:00:00:00:00:00  
          BROADCAST MULTICAST  MTU:1462  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

ip6tnl0   Link encap:UNSPEC  HWaddr 00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00  
          NOARP  MTU:1452  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1 
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

lo        Link encap:Local Loopback  
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:1517 errors:0 dropped:0 overruns:0 frame:0
          TX packets:1517 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1 
          RX bytes:106516 (104.0 KiB)  TX bytes:106516 (104.0 KiB)

sit0      Link encap:IPv6-in-IPv4  
          NOARP  MTU:1480  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1 
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

wlan0     Link encap:Ethernet  HWaddr B8:27:EB:55:1B:9F  
          BROADCAST MULTICAST  MTU:1500  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)
```

挺多的，我们一个个分析一下。

br-lan：

这个跟eth0的网卡地址是一样的，从名字上看，这个是一个网桥，是虚拟的。

这是一个典型路由器的框图。

![openwrt（一）-图1](/images/openwrt（一）-图1.png)

看看Makefile的编译过程。



# openwrt基本情况

官网在这里：https://openwrt.org/

从2018年起，lede项目和openwrt项目都统一为openwrt项目。

项目的基本规则是：https://openwrt.org/rules

```
1、没有核心开发团队，没有特权管理者，所以的提交者是平等的。
2、所有提交者都有投票的权利。
3、项目事务都以投票的方式来决定（妥当吗？）
4、连续3个月无法联系到的提交者，会被剥夺投票权利。
5、任何投票都在网上公开。
6、不会在项目范围内提供邮件地址，保护隐私。
```

合并后的openwrt，基于之前的lede的进行开发。

github的地址是：https://github.com/openwrt/openwrt



# luci界面配置

我们的树莓派ip地址配置为192.168.0.100 。我们在pc的浏览器里访问这个界面。

就到了openwrt的登陆界面了。root，密码就是root密码。

我在浏览器里点击打开wifi。串口打印了这些。

```
[64030.749441] brcmfmac: brcmf_cfg80211_dump_station: BRCMF_C_GET_ASSOCLIST unsupported, err=-512
[64210.946444] IPv6: ADDRCONF(NETDEV_UP): wlan0: link is not ready
[64210.955123] device wlan0 entered promiscuous mode
[64211.089334] IPv6: ADDRCONF(NETDEV_CHANGE): wlan0: link becomes ready
[64211.096971] br-lan: port 2(wlan0) entered forwarding state
[64211.103578] br-lan: port 2(wlan0) entered forwarding state
[64213.096013] br-lan: port 2(wlan0) entered forwarding state
```

然后手机就可以搜索到LEDE的热点，默认没有密码，连接上去。

手机可以通过openwrt来上网。

# 看看系统默认的进程

这里面就有很多点值得研究。

```
  PID USER       VSZ STAT COMMAND
    1 root      1344 S    /sbin/procd：看到pid为1了没？这个是openwrt取代init的一个东西。
    2 root         0 SW   [kthreadd]：带中括号的都是内核线程。
    3 root         0 SW   [ksoftirqd/0]
    4 root         0 SW   [kworker/0:0]
    5 root         0 SW<  [kworker/0:0H]
    7 root         0 SW   [rcu_sched]
    8 root         0 SW   [rcu_bh]
    9 root         0 SW   [migration/0]
   10 root         0 SW   [migration/1]
   11 root         0 SW   [ksoftirqd/1]
   13 root         0 SW<  [kworker/1:0H]
   14 root         0 SW   [migration/2]
   15 root         0 SW   [ksoftirqd/2]
   17 root         0 SW<  [kworker/2:0H]
   18 root         0 SW   [migration/3]
   19 root         0 SW   [ksoftirqd/3]
   21 root         0 SW<  [kworker/3:0H]
   22 root         0 SW<  [writeback]
   23 root         0 SW<  [crypto]
   24 root         0 SW<  [bioset]
   25 root         0 SW<  [kblockd]
   26 root         0 SW   [kswapd0]
   28 root         0 SW<  [vmstat]
   29 root         0 SW   [fsnotify_mark]
   34 root         0 SW<  [pencrypt]
中间很多一样的，被我删掉了。
   65 root         0 SW<  [VCHIQ-0]
   66 root         0 SW<  [VCHIQr-0]
   67 root         0 SW<  [VCHIQs-0]
   68 root         0 SW<  [dwc_otg]
   69 root         0 SW   [kworker/3:1]
   70 root         0 SW   [kworker/1:1]
   72 root         0 SW<  [DWC Notificatio]
   73 root         0 SW   [irq/92-mmc1]
   74 root         0 SW<  [ipv6_addrconf]
   76 root         0 SW   [VCHIQka-0]
   77 root         0 SW<  [SMIO]
   78 root         0 SW<  [deferwq]：延迟的工作队列。
   79 root         0 SW   [kworker/1:2]
   80 root         0 SW   [kworker/3:2]
   81 root         0 SW   [scsi_eh_0]
   82 root         0 SW<  [scsi_tmf_0]
   83 root         0 SW   [usb-storage]
   84 root         0 SW<  [bioset]
   86 root         0 SW<  [kworker/2:1H]
   87 root         0 SW<  [kworker/0:1H]
   88 root         0 SW<  [ext4-rsv-conver]
   90 root         0 SW<  [kworker/1:1H]
   94 root         0 SW<  [kworker/3:1H]
  277 root       960 S    /sbin/ubusd：这个值得注意。
  321 root      1040 S    /bin/ash --login：login的调用非常晚啊。
  322 root       668 S    /sbin/askfirst /usr/libexec/login.sh：注意这里。
  472 root         0 SW   [spi0]
  474 root         0 SW<  [cfg80211]
  475 root         0 SW<  [brcmf_wq/mmc1:0]
  476 root         0 SW   [kworker/2:2]
  477 root         0 SW   [brcmf_wdog/mmc1]
  575 root      1040 S    /sbin/logd -S 64
  584 root      1236 S    /sbin/rpcd
  663 root      1444 S    /sbin/netifd
  698 root      1208 S    /usr/sbin/odhcpd
  801 nobody     748 S    /usr/sbin/atd -f
  842 nobody    1496 S    /usr/sbin/dnscrypt-proxy /var/etc/dnscrypt-proxy-ns1
  870 root       808 S    /usr/sbin/dropbear -F -P /var/run/dropbear.1.pid -p
  929 root      1348 S    /usr/sbin/uhttpd -f -h /www -r LEDE -x /cgi-bin -u /
  943 nobody    1408 S    /usr/sbin/mdnsd -debug
  995 root      2572 S    /usr/sbin/smbd -F
  996 root      2632 S    /usr/sbin/nmbd -F
 1007 root      4420 S <  /usr/libexec/softethervpn/vpnbridge execsvc
 1008 root     17508 S <  /usr/libexec/softethervpn/vpnbridge execsvc
 1027 root      4420 S <  /usr/libexec/softethervpn/vpnclient execsvc
 1028 root     14200 S <  /usr/libexec/softethervpn/vpnclient execsvc
 1085 dnsmasq   2204 S    /usr/sbin/dnsmasq -C /var/etc/dnsmasq.conf.cfg02411c
 1088 root      4420 S <  /usr/libexec/softethervpn/vpnserver execsvc
 1089 root     20812 S <  /usr/libexec/softethervpn/vpnserver execsvc
 1101 root       760 S    xl2tpd -D -l -p /var/run/xl2tpd.pid
 1168 root      3704 S    /usr/sbin/collectd -f
 1249 root      1264 S    /usr/sbin/hnetd -d /etc/init.d/dnsmasq -f /tmp/dnsma
 1275 root      1120 S    /usr/bin/redsocks2 -c /var/etc/redsocks2.conf
 7896 root         0 SW   [kworker/u8:0]
11012 root         0 SW   [kworker/2:0]
11013 root      1964 S    /usr/sbin/hostapd -s -P /var/run/wifi-phy0.pid -B /v
11027 root         0 SW   [kworker/0:2]
14740 root         0 SW   [kworker/u8:2]
14744 root      1032 R    ps
26731 root         0 SW   [kworker/u8:3]
29230 root         0 SW   [kworker/u8:1]
30268 root      1036 S    {watchcat.sh} /bin/sh /usr/bin/watchcat.sh period 21
30276 root      1032 S    sleep 1080
30305 root      1032 S    /usr/sbin/ntpd -n -N -l -S /usr/sbin/ntpd-hotplug -p
30392 root       724 S    /usr/sbin/vnstatd -d
```

1、procd。

```
从pid可以看出，这个就是init进程。procd是process daemon的缩写。进程管理用的。
它肯定是改进了普通的init进程。
它做了什么特别的事情？
它会跟踪通过init脚本启动的进程。
procd取代了这些东西：
1、hotplug。procd把热插拔的活也干了。
2、busybox的klogd和syslogd。把日志的活也干了。
3、busybox的watchdog。把看门狗的活也干了。
为什么需要procd？
为了让系统更加健壮。
```

我觉得需要看一下，内核改了一些什么。

openwrt的改动应该是在编译的过程中合入的，所以需要看看编译过程。



# 配置软件源

一般linux系统的软件源，国外的下载都太慢。

openwrt也是一样，需要修改为国内的源。

对应的配置文件是/etc/opkg/distfeeds.conf文件。先把之前的备份一份。

我从官网找到这个，电脑访问这个网站感觉还挺快的。

```
src/gz reboot_core https://downloads.openwrt.org/releases/17.01.4/targets/brcm2708/bcm2710/packages/
src/gz reboot_base https://downloads.openwrt.org/releases/17.01.4/packages/arm_cortex-a53_neon-vfpv4/base
src/gz reboot_luci https://downloads.openwrt.org/releases/17.01.4/packages/arm_cortex-a53_neon-vfpv4/luci
src/gz reboot_packages https://downloads.openwrt.org/releases/17.01.4/packages/arm_cortex-a53_neon-vfpv4/packages
src/gz reboot_routing https://downloads.openwrt.org/releases/17.01.4/packages/arm_cortex-a53_neon-vfpv4/routing
src/gz reboot_telephony https://downloads.openwrt.org/releases/17.01.4/packages/arm_cortex-a53_neon-vfpv4/telephony
```

但是写到文件，opkg update提示下载失败。

我在openwrt上访问百度也不行，我的手机现在是连接在openwrt上，手机都可以上网。

为什么openwrt本身反而不能上网呢？

可以ping通`114.114.114.114`。说明网络是通的。只是openwrt的dns有问题。

浏览器进入到管理界面。

网络，接口，修改，把dns改成114.114.114.114。点击保存应用。

然后再执行opkg update就好了。



# 用winscp连接

一开始是不行的。因为没有安装启动对应的服务。

```
opkg update
opkg install vsftpd openssh-sftp-server
```

这样就可以了。



# 参考资料

1、编译OpenWrt烧录树莓派3B

http://tobefun.cn/2017/07/18/编译OpenWrt烧录树莓派3B/

2、

https://wiki.openwrt.org/doc/networking/network.interfaces

3、br-lan、eth0、eth1及lo

https://blog.csdn.net/u013485792/article/details/50943069

4、交换机手册(Switch Documentation)

https://wiki.openwrt.org/zh-cn/doc/uci/network/switch

5、What is procd?

https://wiki.openwrt.org/doc/techref/procd

6、Openwrt上开启sftp,使用SecureCRT,WinSCp等传输文件

https://www.cnblogs.com/Motorola/p/7469962.html