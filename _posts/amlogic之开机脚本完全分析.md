---
title: amlogic之开机脚本完全分析
date: 2021-06-04 10:56:11
tags:
	- 网络

---

--

当前开机脚本，总有卡住一段时间的问题。

感觉这些脚本内容搞得太多了。相互之间有依赖。而依赖关系还不太清楚。

需要梳理一下。才方便动手优化。

总共是4个脚本：
1、S39wifi。
2、S40network。
3、S41dhcpcd。
4、S41inetd。

```
S39wifi做了什么工作？
    wifi_start &
        这个非阻塞的。
        首先是把hostapd、wpa_supplicant、dnsmasq、dhcpcd这4个进程都杀掉了。
        然后用multi wifi工具加载驱动。
        然后对博通和rtk的进行了区分处理。
        先看rtk的。
            这个默认是启动的ap模式，没有启动sta模式。
            
        这个的后台执行，有带来什么问题？
        
```

```
对应博通
both模式时是这样：
dhd_priv isam_init mode sta-ap
hostapd_conf_pre wlan1   现在应该就是这一步卡住了很久。
按道理，S39wifi没有依赖其他的启动脚本吧。
```

```
S40network做了什么？
就做了一行：/sbin/ifup -a
用这个调试不执行，看到是做了这些。
ifup虽然是C语言写的，但是本质是脚本一样的工作，包装了一些命令。
先把/etc/network/if-pre-up.d 目录下的脚本都执行一遍。
当前实际上只有一个wait_iface的脚本。
然后用ip命令配置lo网卡的。
然后执行/etc/network/if-up.d下的脚本。这个是空的。
# ifup -a -n
run-parts /etc/network/if-pre-up.d   把这个目录下的脚本都执行一遍。
ip addr add 127.0.0.1/8 dev lo
ip link set lo up
run-parts /etc/network/if-up.d
ifup: interface wlan0 already configured
```

几个疑问：

1、run-parts 这个从哪里来？

```
是busybox/debianutils/run_parts.c生成的命令。
debianutils，就4个：
pipe_progress.c
run_parts.c
start_stop_daemon.c
which.c

run-parts的作用：
run-parts is a utility designed to run all the scripts in a directory.
在一个目录下运行所有的脚本。怎么理解这句话？

用法示例：
run-parts -a start /etc/init.d
run-parts -a stop=now /etc/init.d
这就好理解了。

```

2、/etc/network/if-pre-up.d 有哪些脚本

```
从名字看，这个目录下的脚本，是在网卡启动之前执行的。
当前下面就一个脚本，wait_iface。
就是等待网卡出现，又一个超时时间IF_WAIT_DELAY
这个看起来是一个环境变量。
但是没有看到哪里设置了。

interfaces文件里是这样写的。
iface wlan0 inet dhcp
  pre-up /etc/network/nfs_check
  wait-delay 15   这个就是设置了超时。
  hostname $(hostname)
```

wait_iface这个脚本在标准的busybox下就有。

./package/ifupdown-scripts/network/if-pre-up.d/wait_iface

```
├── Config.in
├── ifupdown-scripts.mk
├── network
│   ├── if-down.d
│   ├── if-post-down.d
│   ├── if-pre-up.d
│   │   └── wait_iface
│   └── if-up.d
├── network.service
├── nfs_check
└── S40network
```



现在有一个疑问，开机时，wifi进行sta和ap同时工作的模式。

系统开机会卡住几十秒。就是卡在ifup -a这里。

但是我的疑问是：interfaces文件里，只写了wlan0和loopback的。为什么会卡wlan1的？而且卡的时间特别长，有50秒之久，简直不能忍受。

有网络信息后，就不会卡住了。

在S42wifi这个名字时，不会卡这么久，最多卡15秒这个预设的超时。

为什么会卡这么久，能不能通过参数调节？



看看树莓派3b自带的wifi模块，如何同时开启ap和sta的。

脚本相对复杂。



参考资料

1、run-parts 命令的用法及原理

https://blog.csdn.net/qq_32352565/article/details/70878082

2、RASPBERRY PI 3 - WIFI STATION+AP

https://github.com/peebles/rpi3-wifi-station-ap-stretch