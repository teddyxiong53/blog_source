---
title: openwrt（三）UCI
date: 2018-04-11 11:05:30
tags:
	- openwrt

---



# 什么是UCI

UCI是Unified Configuration Interface。统一配置接口。

源代码在这里，不是官方的。https://github.com/jkjuopperi/uci

UCI是用C语言写的小工具。另外用shell包装了一下。

是用来对对openwrt设备进行集中配置的。

**所有配置文件都在/etc/config目录里下。**

这些配置文件可以用uci这个命令行工具来编辑，也可以用shell 、lua、C来修改。

**另外，webui修改的内容也是保存在这里。**

配置应该简单而直接，让程序员的生活更好过些。uci就是为了这个目标而来的。

按照传统的linux里的配置文件，都是分散在各个不同的目录下，例如：

```
/etc/network/interfaces
/etc/exports
/etc/dnsmasq.conf
/etc/samba/smb.conf
```

**不仅目录分散，而且语法各不相同。**

uci就是统一位置，统一语法。

不过，完全统一，也不现实的，**uci做的是把常用部分统一起来。**

uci的做法是：

/etc/samba/smb.conf的配置会被/etc/config/samba的配置覆盖。

如果你想要把不兼容uci的程序，也兼容进来，openwrt提供了一套指导方法。

# 组成

uci

libuci

libuci-lua

安装文件

/sbin/uci

/lib/config/uci.sh：就是uci的shell包装。

/lib/libuci.so

/usr/lib/lua/uci.so



uci虽然是openwrt里的东西，但是你可以在Ubuntu、Raspbian这些系统里用。

# 命令行工具用法

```
root@LEDE:~# uci
Usage: uci [<options>] <command> [<arguments>]

Commands:
        batch
        export     [<config>]
        import     [<config>]
        changes    [<config>]
        commit     [<config>]
        add        <config> <section-type>
        add_list   <config>.<section>.<option>=<string>
        del_list   <config>.<section>.<option>=<string>
        show       [<config>[.<section>[.<option>]]]
        get        <config>.<section>[.<option>]
        set        <config>.<section>[.<option>]=<value>
        delete     <config>[.<section>[[.<option>][=<id>]]]
        rename     <config>.<section>[.<option>]=<name>
        revert     <config>[.<section>[.<option>]]
        reorder    <config>.<section>=<position>

Options:
        -c <path>  set the search path for config files (default: /etc/config)
        -d <str>   set the delimiter for list values in uci show
        -f <file>  use <file> as input instead of stdin
        -m         when importing, merge data into an existing package
        -n         name unnamed sections on export (default)
        -N         don't name unnamed sections
        -p <path>  add a search path for config change files
        -P <path>  add a search path for config change files and use as default
        -q         quiet mode (don't print error messages)
        -s         force strict mode (stop on parser errors, default)
        -S         disable strict mode
        -X         do not use extended syntax on 'show'
```

# 公共原则

**当你用vi或者uci修改了配置之后，相关的服务，需要通过/etc/init.d里的启动脚本进行重启。**

# 配置文件

## basic

```
/etc/config/dhcp
/etc/config/dropbare
/etc/config/firewall
/etc/config/network
/etc/config/system
/etc/config/wireless
```

## ipv6

## 其他

```
babeld
bbstored
ddns
etherwake
freifunk_p2pblock
fstab
hd-idle
httpd
ipset-dns
luci
luci_statistics
mini_snmpd
minidlna
mjpg-streamer
mountd
mroute
multiwan
mwan3
ntpclient
p910nd
pure-ftpd
qos
racoon
samba
snmpd
sqm
sshtunnel
stund
tinc
transmission
uhttpd
upnpd
users
ushare
vblade
vnstat
wifitoggle
wol
wshaper
znc
```

# 语法

这个是一个最简单的例子。

```
package 'example'
config 'example' 'test'
	option 'string' 'some value'
	option 'boolean' '1'
	list 'collection' 'first item'
	list 'collection' 'second item'
```

1、example、test定义了一个section，类型是example，名字是test。

我们看看/etc/config/network里的内容。

```
config interface 'loopback'
        option ifname 'lo'
        option proto 'static'
        option ipaddr '127.0.0.1'
        option netmask '255.0.0.0'

config globals 'globals'
        option ula_prefix 'fda9:2172:1e8c::/48'

config interface 'lan'
        option type 'bridge'
        option ifname 'eth0'
        option proto 'static'
        option ipaddr '192.168.0.100'
        option netmask '255.255.255.0'
        option ip6assign '60'
```

为了方便vi的编辑，还开发了一个vim插件，vim-uci。

# uci数据模型

## 组成元素

1、config。

2、sections。

3、types。

4、options。

5、values。

# 简单例子

我们编辑一个/etc/config/foo文件。内容就是这样。

```
config bar 'first'
        option name 'aaa'
config bar
        option name 'bbb'
config bar 'third'
        option name 'ccc'
```

我们用uci的工具操作一下：

1、读取。

```
root@LEDE:/etc/config# uci show foo
foo.first=bar
foo.first.name='aaa'
foo.@bar[1]=bar
foo.@bar[1].name='bbb'
foo.third=bar
foo.third.name='ccc'
```



# 参考资料

1、

https://wiki.openwrt.org/doc/techref/uci

2、

https://wiki.openwrt.org/doc/uci