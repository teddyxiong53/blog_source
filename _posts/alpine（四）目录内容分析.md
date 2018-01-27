---
title: alpine（四）目录内容分析
date: 2018-01-26 20:57:57
tags:
	- alpine
	- Linux

---



# bin

大部分是busybox的软链接。有4个不同的。

# boot

放了配置文件、map文件、内核文件。

# etc

1、TZ。里面就放了一个“UTC”字符串。

2、alpine-release。里面就一个“3.7.0”。

3、apk目录。

```
vm-alpine-0:/etc/apk# tree
.
├── arch：里面就是一个“x86”的字符串。
├── cache -> /var/cache/apk
├── keys
│   ├── alpine-devel@lists.alpinelinux.org-4a6a0840.rsa.pub
│   ├── alpine-devel@lists.alpinelinux.org-5243ef4b.rsa.pub
│   └── alpine-devel@lists.alpinelinux.org-5261cecb.rsa.pub
├── protected_paths.d
│   └── ca-certificates.list
├── repositories
└── world：放着已经安装的软件的名字列表。
```

4、chrony目录。里面就一个chrony.conf文件。

```
vm-alpine-0:/etc/chrony# cat chrony.conf 
# default config

server pool.ntp.org 
initstepslew 10 pool.ntp.org
commandkey 10
keyfile /etc/chrony/chrony.keys
driftfile /var/lib/chrony/chrony.drift
```

5、conf.d。这个目录下是各种配置文件。

6、crontabs。下面就一个root文件。

7、fstab。

8、group。

9、hostname。

10、hosts。

11、init.d。

12、inittab。

13、local.d。

14、localtime。

15、mdev.conf。

16、mke2fs.conf。ext2文件系统对应。

17、mkinitfs目录。

18、network目录。

```
vm-alpine-0:/etc/network# tree
.
├── if-down.d
├── if-post-down.d
├── if-post-up.d
├── if-pre-down.d
├── if-pre-up.d
├── if-up.d
│   └── dad
└── interfaces
```

19、os-release。

```
vm-alpine-0:/etc# cat os-release 
NAME="Alpine Linux"
ID=alpine
VERSION_ID=3.7.0
PRETTY_NAME="Alpine Linux v3.7"
HOME_URL="http://alpinelinux.org"
BUG_REPORT_URL="http://bugs.alpinelinux.org"
```

20、passwd。

21、periodic目录。

```
vm-alpine-0:/etc/periodic# tree
.
├── 15min
├── daily
├── hourly
├── monthly
└── weekly
```

22、profile。遍历profile.d里的文件。

23、profile.d。

24、protocols。罗列支持的协议。

25、rc.conf。

26、resolv.conf。

27、runlevels目录。

```
vm-alpine-0:/etc/runlevels# tree
.
├── boot
│   ├── bootmisc -> /etc/init.d/bootmisc
│   ├── hostname -> /etc/init.d/hostname
│   ├── hwclock -> /etc/init.d/hwclock
│   ├── keymaps -> /etc/init.d/keymaps
│   ├── modules -> /etc/init.d/modules
│   ├── networking -> /etc/init.d/networking
│   ├── swap -> /etc/init.d/swap
│   ├── sysctl -> /etc/init.d/sysctl
│   ├── syslog -> /etc/init.d/syslog
│   └── urandom -> /etc/init.d/urandom
├── default
│   ├── acpid -> /etc/init.d/acpid
│   ├── chronyd -> /etc/init.d/chronyd
│   ├── crond -> /etc/init.d/crond
│   ├── lighttpd -> /etc/init.d/lighttpd
│   ├── mariadb -> /etc/init.d/mariadb
│   ├── ntpd -> /etc/init.d/ntpd
│   └── sshd -> /etc/init.d/sshd
├── nonetwork
├── shutdown
│   ├── killprocs -> /etc/init.d/killprocs
│   ├── mount-ro -> /etc/init.d/mount-ro
│   └── savecache -> /etc/init.d/savecache
└── sysinit
    ├── devfs -> /etc/init.d/devfs
    ├── dmesg -> /etc/init.d/dmesg
    ├── hwdrivers -> /etc/init.d/hwdrivers
    └── mdev -> /etc/init.d/mdev
```

28、services。罗列了启动的服务。

29、shadow。

30、shells。里面罗列shell。就bash和ash两个。

31、sysctl.conf。

32、sysctl.d目录。

33、terminfo目录。

```
vm-alpine-0:/etc/terminfo# tree
.
├── a
│   └── ansi
├── d
│   └── dumb
├── l
│   └── linux
├── r
│   └── rxvt
├── s
│   ├── screen
│   └── sun
├── v
│   ├── vt100
│   ├── vt102
│   ├── vt200
│   ├── vt220
│   └── vt52
└── x
    ├── xterm
    ├── xterm-color
    └── xterm-xfree86

```

# lib

下面大概5000个文件。

1、apk目录。没什么东西。就一些信息。

2、firmware目录。东西较多。应该是linux标准的东西。1500个文件。

3、几个so文件。ld-musl-i386.so等。

4、mdev目录。下面5个脚本。

5、modules目录。一堆的ko文件。大概3400个。

6、rc。下面70个脚本。

# proc

目录就不管。看文件。

1、buddyinfo。

```
vm-alpine-0:/proc# cat buddyinfo 
Node 0, zone      DMA      0      1      1      0      2      1      1      0      1      1      3 
Node 0, zone   Normal     11   1338    248     39    123     46     11      5      2      2     56 
Node 0, zone  HighMem      0      1      2      3      2      0      0      0      0      0      0 
```

2、cgroups。

```
vm-alpine-0:/proc# cat cgroups 
#subsys_name    hierarchy       num_cgroups     enabled
cpu     2       1       1
cpuacct 3       1       1
blkio   4       1       1
devices 5       1       1
freezer 6       1       1
net_cls 7       1       1
net_prio        8       1       1
pids    9       1       1
```

3、cmdline。

```
vm-alpine-0:/proc# cat cmdline 
BOOT_IMAGE=vmlinuz-hardened root=UUID=e58ee021-1eba-48b5-826e-8d9c5ac49673 modules=sd-mod,usb-storage,ext4 nomodeset pax_nouderef quiet rootfstype=ext4 initrd=initramfs-hardened
```

4、console。

```
tty0                 -WU (EC p  )    4:1
```

5、cpuinfo。

```
processor       : 0
vendor_id       : GenuineIntel
cpu family      : 6
model           : 94
model name      : Intel(R) Core(TM) i5-6500 CPU @ 3.20GHz
stepping        : 3
microcode       : 0x7c
cpu MHz         : 3191.661
cache size      : 6144 KB
physical id     : 0
siblings        : 1
core id         : 0
cpu cores       : 1
apicid          : 0
initial apicid  : 0
fdiv_bug        : no
f00f_bug        : no
coma_bug        : no
fpu             : yes
fpu_exception   : yes
cpuid level     : 22
wp              : yes
flags           : fpu vme de tsc msr pae mce cx8 apic mtrr pge mca cmov pat pse36 clflush dts mmx fxsr sse sse2 ss nx pdpe1gb rdtscp lm constant_tsc arch_perfmon pebs bts xtopology tsc_reliable nonstop_tsc aperfmperf eagerfpu pni pclmulqdq ssse3 fma cx16 pcid sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand hypervisor lahf_lm abm 3dnowprefetch fsgsbase tsc_adjust bmi1 hle avx2 smep bmi2 invpcid rtm rdseed adx smap xsaveopt dtherm ida arat pln pts hwp hwp_notify hwp_act_window hwp_epp
bugs            :
bogomips        : 6386.16
clflush size    : 64
cache_alignment : 64
address sizes   : 42 bits physical, 48 bits virtual
power management:
```

# usr

1、lib目录。

我看到有libgcc_s.so文件。



