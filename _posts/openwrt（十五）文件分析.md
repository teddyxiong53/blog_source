---
title: openwrt（十五）
date: 2018-04-14 08:42:50
tags:
	- openwrt

---



现在看看openwrt里的文件。

# /bin

```
root@LEDE:~# cpu_temp 
temp: 56.382
```

# /etc

这个目录文件很多。

```
59 directories, 1191 files
```

我们先看顶层的文件。

```
root@LEDE:/etc# tree -L 1
.
├── TZ -> /tmp/TZ 里面就是一个CST-8字符串。
├── adblock 广告过滤，下面一个黑名单，一个白名单。
├── adblocklist 下面2个文件，一个adblock，一个adblockip。
├── ahcp ： Ad-Hoc Configuration Protocol
├── avrdude.conf
├── babeld.conf
├── banner ：登陆时的那个图标。
├── banner.failsafe
├── board.d 下面02_network          99-default_network 这2个脚本。
├── board.json 
├── chatscripts
├── china_ssr.txt 下面是一大堆的ip。
├── chinadns_chnroute.txt 
├── chinadns_iplist.txt
├── collectd 空的。
├── collectd.conf -> /var/etc/collectd.conf
├── collectd.conf.bak
├── config
├── config-bak 我自己备份的config目录。
├── crontabs
├── ddns 
├── device_info
├── diag.sh
├── dnsmasq.conf 值得研究一下。
├── dnsmasq.ssr
├── dropbear
├── e2fsck.conf
├── ethers
├── filesystems
├── firewall.user
├── fstab
├── gcom
├── gnutls
├── group
├── hnet-pa.store
├── hosts
├── hotplug-preinit.json
├── hotplug.d
├── hotplug.json
├── init.d
├── inittab
├── iproute2
├── joe
├── l7-protocols
├── lcd4linux.conf
├── localtime -> /tmp/localtime
├── login.defs
├── luci-uploads
├── lvm
├── modules-boot.d
├── modules.d
├── mtab -> /proc/mounts
├── odbc.ini
├── odbcinst.ini
├── openconnect
├── openvpn
├── openwrt_release
├── openwrt_version
├── opkg
├── opkg.conf
├── os-release -> ../usr/lib/os-release
├── passwd
├── passwd-
├── pcap-dnsproxy
├── pip.conf
├── ppp
├── pptpd.conf
├── preinit
├── profile
├── protocols
├── raspbian.sh
├── rc.button
├── rc.common
├── rc.d
├── rc.local
├── reaver
├── redsocks2
├── resolv.conf -> /tmp/resolv.conf
├── samba
├── screenrc
├── services
├── shadow
├── shadow-
├── shadowvpn
├── shells
├── ssl
├── sudoers
├── sudoers.d
├── sysctl.conf
├── sysctl.d
├── sysupgrade.conf
├── uci-defaults
├── urandom.seed
├── usb-mode.json
├── vlmcsd.ini
├── vnstat.conf
├── vpnc
├── vsftpd
├── vsftpd.conf
├── xattr.conf
└── xl2tpd
```

# /lib

```
root@LEDE:/lib# tree -L 1
.
├── brcm2708.sh
├── config
├── firmware 固件bin文件。
├── functions
├── functions.sh
├── ld-musl-armhf.so.1 -> libc.so ：使用的是musl的C库。
├── libblkid-tiny.so
├── libblobmsg_json.so
├── libc.so
├── libfstools.so
├── libgcc_s.so.1
├── libjson_script.so
├── librpc.so
├── libsetlbf.so
├── libubox.so
├── libubus.so
├── libuci.so
├── libvalidate.so
├── modules ：这个下面有260个ko文件。
├── mwan3
├── netifd ：这里有26个脚本。
├── network
├── preinit
├── upgrade
└── wifi
```

# /usr

这个目录下文件最多，有10000个以上。

