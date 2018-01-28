---
title: Linux之proc目录下1目录分析
date: 2018-01-28 09:07:44
tags:
	- Linux

---



/proc目录下有很多有用的信息状态信息，而/proc/xx（xx代表pid号）下面放着各个进程的相关信息。1是init进程的pid。我们就以这个为例，看看下面都有些什么东西。

总共20个目录，191个文件。

```
vm-alpine-0:/proc/1# tree
.
├── autogroup：linux2.6.38开始引入，用来改善桌面交互的性能。对应的配置在/proc/sys/kernel/sched_autogroup_enable文件里，我这个是使能的，里面就是一个“1”。作用是对进程自动分组。例如，一边放电影，一边make -j10编译，没有这个特性，放电影就会卡。
├── auxv：我看网上有解释说这个是elf相关信息，但是我当前看到的都是空的。先不管。
├── cgroup
├── cmdline：内容是/sbin/init
├── comm：进程的命令名。内容是init。
├── coredump_filter：一般都是0x23，指定生成core文件的规则。
├── cwd -> / ：软链接到根目录。
├── environ环境变量，内容是：SHLVL=1HOME=/modules=sd-mod,usb-storage,ext4TERM=linuxBOOT_IMAGE=vmlinuz-hardenedPATH=/usr/bin:/bin:/usr/sbin:/sbininitrd=initramfs-hardenedPWD=/
├── exe -> /bin/busybox ：正在进程中运行的程序的内容。
├── fd
│   ├── 0 -> /dev/console (deleted)
│   ├── 1 -> /dev/console (deleted)
│   └── 2 -> /dev/console (deleted)
├── fdinfo
│   ├── 0
│   ├── 1
│   └── 2
├── gid_map：跟namespaces有关系。
├── io：看具体进程的io统计情况。
├── ipaddr：内容是0.0.0.0
├── latency：这个已经没有什么用了。里面内容；Latency Top version : v0.1
├── limits：这个跟ulimit设置的那些值一样。
├── maps：这个很重要，就是进程的内存布局情况了。
├── mem：看不了。
├── mountinfo
├── mounts
├── mountstats：这3个内容差不多。都是挂载情况。
├── net：这部分基本是统计信息。
│   ├── anycast6：广播。空的。
│   ├── arp：arp表。
│   ├── connector：
│   ├── dev：统计信息。
│   ├── dev_mcast：多播统计。
│   ├── dev_snmp6
│   │   ├── eth0：
│   │   └── lo
│   ├── fib_trie：
│   ├── fib_triestat
│   ├── icmp
│   ├── icmp6
│   ├── if_inet6
│   ├── igmp
│   ├── igmp6
│   ├── ip6_flowlabel
│   ├── ip6_mr_cache
│   ├── ip6_mr_vif
│   ├── ip_mr_cache
│   ├── ip_mr_vif
│   ├── ipv6_route
│   ├── mcfilter
│   ├── mcfilter6
│   ├── netfilter
│   │   └── nf_log
│   ├── netlink
│   ├── netstat
│   ├── packet
│   ├── protocols
│   ├── psched
│   ├── ptype
│   ├── raw
│   ├── raw6
│   ├── route
│   ├── rt6_stats
│   ├── rt_acct
│   ├── rt_cache
│   ├── snmp
│   ├── snmp6
│   ├── sockstat
│   ├── sockstat6
│   ├── softnet_stat
│   ├── stat
│   │   ├── arp_cache
│   │   ├── ndisc_cache
│   │   └── rt_cache
│   ├── tcp
│   ├── tcp6
│   ├── udp
│   ├── udp6
│   ├── udplite
│   ├── udplite6
│   ├── unix
│   ├── wireless
│   └── xfrm_stat
├── ns
│   ├── cgroup -> cgroup:[4026531835]
│   ├── ipc -> ipc:[4026531839]
│   ├── mnt -> mnt:[4026531840]
│   ├── net -> net:[4026531957]
│   ├── pid -> pid:[4026531836]
│   ├── user -> user:[4026531837]
│   └── uts -> uts:[4026531838]
├── oom_adj
├── oom_score
├── oom_score_adj
├── personality
├── projid_map
├── root -> /
├── sched
├── schedstat
├── setgroups
├── stack
├── stat
├── statm
├── status
├── task ：这个又绕回去了。跟外面的内容一样的。
│   └── 1
│       ├── auxv
│       ├── cgroup
│       ├── cmdline
│       ├── comm
│       ├── cwd -> /
│       ├── environ
│       ├── exe -> /bin/busybox
│       ├── fd
│       │   ├── 0 -> /dev/console (deleted)
│       │   ├── 1 -> /dev/console (deleted)
│       │   └── 2 -> /dev/console (deleted)
│       ├── fdinfo
│       │   ├── 0
│       │   ├── 1
│       │   └── 2
│       ├── gid_map
│       ├── io
│       ├── latency
│       ├── limits
│       ├── maps
│       ├── mem
│       ├── mountinfo
│       ├── mounts
│       ├── net
│       │   ├── anycast6
│       │   ├── arp
│       │   ├── connector
│       │   ├── dev
│       │   ├── dev_mcast
│       │   ├── dev_snmp6
│       │   │   ├── eth0
│       │   │   └── lo
│       │   ├── fib_trie
│       │   ├── fib_triestat
│       │   ├── icmp
│       │   ├── icmp6
│       │   ├── if_inet6
│       │   ├── igmp
│       │   ├── igmp6
│       │   ├── ip6_flowlabel
│       │   ├── ip6_mr_cache
│       │   ├── ip6_mr_vif
│       │   ├── ip_mr_cache
│       │   ├── ip_mr_vif
│       │   ├── ipv6_route
│       │   ├── mcfilter
│       │   ├── mcfilter6
│       │   ├── netfilter
│       │   │   └── nf_log
│       │   ├── netlink
│       │   ├── netstat
│       │   ├── packet
│       │   ├── protocols
│       │   ├── psched
│       │   ├── ptype
│       │   ├── raw
│       │   ├── raw6
│       │   ├── route
│       │   ├── rt6_stats
│       │   ├── rt_acct
│       │   ├── rt_cache
│       │   ├── snmp
│       │   ├── snmp6
│       │   ├── sockstat
│       │   ├── sockstat6
│       │   ├── softnet_stat
│       │   ├── stat
│       │   │   ├── arp_cache
│       │   │   ├── ndisc_cache
│       │   │   └── rt_cache
│       │   ├── tcp
│       │   ├── tcp6
│       │   ├── udp
│       │   ├── udp6
│       │   ├── udplite
│       │   ├── udplite6
│       │   ├── unix
│       │   ├── wireless
│       │   └── xfrm_stat
│       ├── ns
│       │   ├── cgroup -> cgroup:[4026531835]
│       │   ├── ipc -> ipc:[4026531839]
│       │   ├── mnt -> mnt:[4026531840]
│       │   ├── net -> net:[4026531957]
│       │   ├── pid -> pid:[4026531836]
│       │   ├── user -> user:[4026531837]
│       │   └── uts -> uts:[4026531838]
│       ├── oom_adj
│       ├── oom_score
│       ├── oom_score_adj
│       ├── personality
│       ├── projid_map
│       ├── root -> /
│       ├── sched
│       ├── schedstat
│       ├── setgroups
│       ├── stack
│       ├── stat
│       ├── statm
│       ├── status
│       ├── uid_map
│       └── wchan
├── timerslack_ns
├── uid_map
└── wchan
```

