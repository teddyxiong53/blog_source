---
title: Linux之dnsmasq
date: 2018-04-14 09:11:36
tags:
	- Linux

---



查看openwrt的dnsmasq的位置。

```
root@LEDE:/etc# which dnsmasq
/usr/sbin/dnsmasq
```

查看进程信息。

```
24287 dnsmasq   3328 S    /usr/sbin/dnsmasq -C /var/etc/dnsmasq.conf.cfg02411c -k -x /var/run/dnsmasq/dnsmasq.cfg02411c.pid
```

所以对应的配置文件是/var/etc/dnsmasq.conf.cfg02411c 。看看内容。

```
root@LEDE:/etc# cat /var/etc/dnsmasq.conf.cfg02411c 
# auto-generated config file from /etc/config/dhcp 这个文件是config自动生成的。
conf-file=/etc/dnsmasq.conf 这里有主要信息。
dhcp-authoritative 
domain-needed
localise-queries
read-ethers
expand-hosts
domain=lan
server=/lan/
dhcp-leasefile=/tmp/dhcp.leases  租约文件。当前是空的。
resolv-file=/tmp/resolv.conf.auto 
stop-dns-rebind
rebind-localhost-ok
dhcp-broadcast=tag:needs-broadcast
addn-hosts=/tmp/hosts hosts文件。
conf-dir=/tmp/dnsmasq.d 
user=dnsmasq 用户和组。
group=dnsmasq
```

我们看看/etc/config/dhcp如何配置的。

```
root@LEDE:/etc# cat /etc/config/dhcp

config dnsmasq
        option domainneeded '1'
        option filterwin2k '0'
        option localise_queries '1'
        option rebind_protection '1'
        option rebind_localhost '1'
        option local '/lan/'
        option domain 'lan'
        option expandhosts '1'
        option nonegcache '0'
        option authoritative '1'
        option readethers '1'
        option leasefile '/tmp/dhcp.leases'
        option resolvfile '/tmp/resolv.conf.auto'
        option localservice '0'
        option boguspriv '0'

config dhcp 'lan'
        option interface 'lan'
        option start '100'
        option limit '150'
        option leasetime '12h'
        option dhcpv6 'server'
        option ra 'server'
        option ra_management '1'

config dhcp 'wan'
        option interface 'wan'
        option ignore '1'

config odhcpd 'odhcpd'
        option leasefile '/tmp/hosts/odhcpd'
        option leasetrigger '/usr/sbin/odhcpd-update'
        option maindhcp '1'
```

当前/etc/dnsmasq.conf文件里是空的，只有一些注释。

```
# You may add multiple srv-host lines.
# The fields are <name>,<target>,<port>,<priority>,<weight>
```

这个我们后面再具体举例说明。

查看openwrt当前有的组。

```
root@LEDE:/etc# cat /etc/passwd
root:x:0:0:root:/root:/bin/bash
daemon:*:1:1:daemon:/var:/bin/false
ftp:*:55:55:ftp:/home/ftp:/bin/false
network:*:101:101:network:/var:/bin/false
nobody:*:65534:65534:nobody:/var:/bin/false
dnsmasq:x:453:453:dnsmasq:/var/run/dnsmasq:/bin/false
transmission:x:224:224:transmission:/var/run/transmission:/bin/false
```

好，现在基本上有一个感性认识了。我们开始从理论上来认识dnsmasq。

# dnsmasq是什么？

是一个小巧的dns和dhcp配置工具。适用于小型网络。

dns功能是必选的，dhcp功能是可选的。

它服务于只在本地使用的域名，这些域名不会在全球的dns服务器里出现。

如果你想要快速搭建一个dns服务或者dhcp服务，dnsmasq是一个很好的选择。

查看我的版本。

```
root@LEDE:/etc# dnsmasq -v
Dnsmasq version 2.77  Copyright (c) 2000-2016 Simon Kelley
Compile time options: IPv6 GNU-getopt no-DBus no-i18n no-IDN DHCP DHCPv6 no-Lua TFTP conntrack ipset auth DNSSEC no-ID loop-detect inotify

This software comes with ABSOLUTELY NO WARRANTY.
Dnsmasq is free software, and you are welcome to redistribute it
under the terms of the GNU General Public License, version 2 or 3.
```

# 配置

我们修改/etc/dnsmasq.conf文件。

```
resolve-file=/etc/resolv.conf
strict-order
listen-address=192.168.0.100
address=/teddyxiong53.com/192.168.0.100
server=114.114.114.114
bogus-nxdomain=114.114.114.114
```

resolve-file：定义dnsmasq从哪里获取上游dns服务器的地址。

strict-order：表示严格按照resolve-file里的内容一行一行解析。

listen-address：定义dnsmasq监听的地址，默认是监控本机的所有网卡。那这个我可以不配置。

address：启用泛域名解析，就定义私有的域名。

server：这些就是真的全球dns的解析了。相当于中转了一下。



# 参考资料

1、DNSmasq介绍

https://www.cnblogs.com/demonxian3/p/7472300.html