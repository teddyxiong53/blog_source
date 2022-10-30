---
title: Linux之systemd分析
date: 2018-12-12 20:43:17
tags:
	- Linux
typora-root-url: ..\
---



现在大部分的linux的init程序都换成了systemd了。

但是这一套我不是很熟悉。我还是熟悉busybox里的那一套init。开机启动的东西是在/etc/init.d里的。

但是现在经常碰到跟systemd相关的东西，所以有必须进行一个系统深入的了解。



service命令是System V的。

systemctl是systemd的。



# 简介

systemd是新一代的linux下的init程序。

开发的目标是：提供更优秀的框架，以表示service之间的依赖关系。并以此实现启动时服务的并行启动。

与传统的init程序相比，systemd采用了这些新的技术：

1、采用socket激活与dbus激活式服务。

2、用cgroups取代pid来追踪进程。这样带来一个好处，就是两次fork之后生成的daemon进程也不会脱离systemd的控制。



触发systemd出现的直接原因是：

传统的sysvinit，启动脚本是顺序执行的，这个对于服务器来说无关紧要，因为服务器不会经常关机开机。

但是随着linux向桌面系统扩展，这个问题就变得非常严重了。

启动各种服务，必须要并行化。但是又要考虑有依赖关系的服务的启动的先后顺序。

正是在这样的历史背景下，systemd应运而生。

```
sysvinit是System V init的缩写。
```

systemd借鉴了macos系统的launchd的不少的理念。

systemd是一个庞大的系统。这也让它受到了不少的诟病，因为unix的原则就是一个工具只做一件事情。systemd做了一个大而全的东西，跟这个原则是冲突的。



![](/images/systemd架构.png)





systemd提供了对应sysvint的兼容性。

系统中已经存在的服务和进程不需要修改。这个降低了sysvinit向systemd迁移的成本。使得systemd替换现在系统成为可能。



# 日志服务



systemd 自带日志服务 journald，该日志服务的设计初衷是克服现有的 syslog 服务的缺点。比如：

- syslog 不安全，消息的内容无法验证。每一个本地进程都可以声称自己是 Apache PID 4711，而 syslog 也就相信并保存到磁盘上。
- 数据没有严格的格式，非常随意。自动化的日志分析器需要分析人类语言字符串来识别消息。一方面此类分析困难低效；此外日志格式的变化会导致分析代码需要更新甚至重写。

systemd journal 用二进制格式保存所有日志信息，用户使用 journalctl 命令来查看日志信息。无需自己编写复杂脆弱的字符串分析处理程序。



**systemd journal 的优点如下**：
  **简单性**：代码少，依赖少，抽象开销最小。
  **零维护**：日志是除错和监控系统的核心功能，因此它自己不能再产生问题。举例说，自动管理磁盘空间，避免由于日志的不断产生而将磁盘空间耗尽。
  **移植性**：日志文件应该在所有类型的 Linux 系统上可用，无论它使用的何种 CPU 或者字节序。
  **性能**：添加和浏览日志非常快。
  **最小资源占用**：日志数据文件需要较小。
  **统一化**：各种不同的日志存储技术应该统一起来，将所有的可记录事件保存在同一个数据存储中。所以日志内容的全局上下文都会被保存并且可供日后查询。例如一条固件记录后通常会跟随一条内核记录，最终还会有一条用户态记录。重要的是当保存到硬盘上时这三者之间的关系不会丢失。syslog 将不同的信息保存到不同的文件中，分析的时候很难确定哪些条目是相关的。
  **扩展性**：日志的适用范围很广，从嵌入式设备到超级计算机集群都可以满足需求。
  **安全性**：日志文件是可以验证的，让无法检测的修改不再可能。





# 基础概念

系统在初始化的过程，需要做很多的事情：

1、启动服务。

2、配置，例如挂载文件系统。

这些事情，都被统一抽象为一个概念：unit。叫配置单元。

服务和配置都统一为配置单元。

unit类型有12种：

1、service。最常用。代表一个后台服务，例如sshd。

2、socket。每个socket有一个对应的unit。进程间通信用。

3、device。硬件设备。

4、mount。文件系统挂载。

5、automount。自动挂载。

6、swap。swap文件。

7、target。多个unit构成一个组。

8、timer。定时器。

9、snapshot。systemd快照。可以切换到指定的快照。

10、path。文件或者路径。

11、scope。不是由systemd启动的外部进程。

12、slice。进程组。



# 依赖关系

依赖关系带来了复杂性，依赖关系，其实就是耦合性。

systemd已经尽力在降低各个服务之间的依赖性，但是无法完全消除。

systemd为了处理好依赖关系，提供了一些机制。









# 文件目录

2个目录：

1、/etc/systemd/system。这个有软链接指向了/lib/systemd/system

2、/lib/systemd/system

我们从etc目录下的，选择几个简单的，做一个分析。

1、dbus-org.bluez.service 

2、syslog.service

```
teddy@teddy-ThinkPad-SL410:/etc/systemd/system$ cat dbus-org.bluez.service 
[Unit]
Description=Bluetooth service
Documentation=man:bluetoothd(8)
ConditionPathIsDirectory=/sys/class/bluetooth

[Service]
Type=dbus
BusName=org.bluez
ExecStart=/usr/lib/bluetooth/bluetoothd -C
NotifyAccess=main
#WatchdogSec=10
#Restart=on-failure
CapabilityBoundingSet=CAP_NET_ADMIN CAP_NET_BIND_SERVICE
LimitNPROC=1

[Install]
WantedBy=bluetooth.target
Alias=dbus-org.bluez.service
```

```
teddy@teddy-ThinkPad-SL410:/etc/systemd/system$ cat syslog.service 
[Unit]
Description=System Logging Service
Requires=syslog.socket
Documentation=man:rsyslogd(8)
Documentation=http://www.rsyslog.com/doc/

[Service]
Type=notify
ExecStart=/usr/sbin/rsyslogd -n
StandardOutput=null
Restart=on-failure

[Install]
WantedBy=multi-user.target
Alias=syslog.service
```

WantedBy具体含义是什么？





## unit配置文件的写法

每一个 Unit 都有一个配置文件，告诉 Systemd 怎么启动这个 Unit 。

Systemd 默认从目录`/etc/systemd/system/`读取配置文件。但是，里面存放的大部分文件都是符号链接，指向目录`/usr/lib/systemd/system/`，真正的配置文件存放在那个目录。

usr目录下那里放的所有的文件。而etc下面的，则是需要开机执行的文件。

systemctl enable命令，就是把需要使能的文件，在etc下面新建一个软链接过去。

```
$ sudo systemctl enable clamd@scan.service
# 等同于
$ sudo ln -s '/usr/lib/systemd/system/clamd@scan.service' '/etc/systemd/system/multi-user.target.wants/clamd@scan.service'
```

而disable相当于删掉这个软链接。

文件的后缀名就是unit的类型。所有是有12种。

默认的后缀名是service。所以sshd等价于sshd.service。

systemctl list-unit-files

这个命令会列出所有的unit文件，并说明对应的状态。

状态有4种

- enabled：已建立启动链接
- disabled：没建立启动链接
- static：该配置文件没有`[Install]`部分（无法执行），只能作为其他配置文件的依赖
- masked：该配置文件被禁止建立启动链接

一旦修改配置文件，就要让 SystemD 重新加载配置文件，然后重新启动，否则修改不会生效。

> ```bash
> $ sudo systemctl daemon-reload
> $ sudo systemctl restart httpd.service
> ```



有静态服务xxx.service: 
( 没有Install项的service都是[static](https://so.csdn.net/so/search?q=static&spm=1001.2101.3001.7020)的, 所以你不可能enable/disable他了, 所以他的状态永远是static的了, 也就是说他的运行只能通过其他的服务单元触发 )

```
systemctl --reverse list-dependencies dbus.service
```



配置文件的语法有点像ini文件。

区块

`[Unit]`区块通常是配置文件的第一个区块，用来定义 Unit 的元数据，以及配置与其他 Unit 的关系。它的主要字段如下。

```
Description：描述。
Documentation：文档的地址。
Requires：依赖的其他unit，如果依赖没有运行，则本unit会启动失败。
Wants：与当前unit配合的其他unit。即使没有运行，也不会失败。
BindsTo：如果绑定的unit退出了，那么自己也会退出。
Before：本unit要在指定的unit前面启动。
After：
Conflicts：本unit跟指定的unit冲突。

```

`[Install]`通常是配置文件的最后一个区块，用来定义如何启动，以及是否开机启动。它的主要字段如下。

```
WantedBy：
	它的值是一个或者多个target。
	当本unit被激活的时候，软链接符号会被放入到target-name.wants后缀的子目录中。
RequiredBy：
	当本unit被激活的时候，软链接符号会被放入到target-name.required后缀的子目录中。
Alias
	本unit起的别名。例如bluetooth，可以起bt的别名。
Also：
	激活本unit的时候，同时把指定的unit也激活。
	
```

`[Service]`区块用来 Service 的配置，只有 Service 类型的 Unit 才有这个区块。它的主要字段如下。

```
Type
	有多种取值：
	simple。默认值。执行ExecStart指定的命令启动进程。
	forking。以fork的方式启动。
	oneshot。systemd等当前进程执行完再继续往下走。
	dbus。通过dbus启动服务。
	notify。当前服务启动完成后，通知给到systemd，这时候systemd才继续执行。
	idle。只有在systemd空闲的时候（其他的任务执行完成后）才执行。
ExecStart
ExecStartPre
ExecStartPost
ExecReload
ExecStop
ExecStopPost
RestartSec：重启服务的间隔。
Restart：
	服务停止时的重启策略。always、on-success、on-failure、on-abnormal、on-abort、on-watchdog。
TimeoutSec
	systemd停止当前进程之前要等的时间。
Environment：
	启动当前服务的环境变量。
	
```

## target

target就是由多个unit组成的一个组。就跟文件夹和文件的关系一样。

启动计算机的时候，需要启动大量的 Unit。如果每一次启动，都要一一写明本次启动需要哪些 Unit，显然非常不方便。Systemd 的解决方案就是 Target。

简单说，Target 就是一个 Unit 组，包含许多相关的 Unit 。启动某个 Target 的时候，Systemd 就会启动里面所有的 Unit。从这个意义上说，Target 这个概念类似于"状态点"，启动某个 Target 就好比启动到某种状态。

传统的`init`启动模式里面，有 RunLevel 的概念，跟 Target 的作用很类似。不同的是，RunLevel 是互斥的，不可能多个 RunLevel 同时启动，但是多个 Target 可以同时启动。

查看系统里所有的target。

```
systemctl list-unit-files --type=target
```

查看默认的target。

```
systemctl get-default
multi-user.target
```

Target 与 传统 RunLevel 的对应关系如下。

> ```bash
> Traditional runlevel      New target name     Symbolically linked to...
> 
> Runlevel 0           |    runlevel0.target -> poweroff.target
> Runlevel 1           |    runlevel1.target -> rescue.target
> Runlevel 2           |    runlevel2.target -> multi-user.target
> Runlevel 3           |    runlevel3.target -> multi-user.target
> Runlevel 4           |    runlevel4.target -> multi-user.target
> Runlevel 5           |    runlevel5.target -> graphical.target
> Runlevel 6           |    runlevel6.target -> reboot.target
> ```



它与`init`进程的主要差别如下。

> **（1）默认的 RunLevel**（在`/etc/inittab`文件设置）现在被默认的 Target 取代，位置是`/etc/systemd/system/default.target`，通常符号链接到`graphical.target`（图形界面）或者`multi-user.target`（多用户命令行）。
>
> **（2）启动脚本的位置**，以前是`/etc/init.d`目录，符号链接到不同的 RunLevel 目录 （比如`/etc/rc3.d`、`/etc/rc5.d`等），现在则存放在`/lib/systemd/system`和`/etc/systemd/system`目录。
>
> **（3）配置文件的位置**，以前`init`进程的配置文件是`/etc/inittab`，各种服务的配置文件存放在`/etc/sysconfig`目录。现在的配置文件主要存放在`/lib/systemd`目录，在`/etc/systemd`目录里面的修改可以覆盖原始设置。

multi-user.target的内容：

```
[Unit]
Description=Multi-User System
Documentation=man:systemd.special(7)
Requires=basic.target
Conflicts=rescue.service rescue.target
After=basic.target rescue.service rescue.target
AllowIsolate=yes
```

而basic.target的内容：

```
Requires=sysinit.target
Wants=sockets.target timers.target paths.target slices.target
```



# 命令使用

## systemctl

```
systemctl list-units
systemctl list-sockets
systemctl list-timers

systemctl start/stop/reload/restart/status xx
systemctl enable/disable xx 

systemctl list-dependencies sshd.service
```



```
sh-5.0# hostnamectl
   Static hostname: mesona5-av400
         Icon name: computer
        Machine ID: 615c3b12ea8a4b6eb528c0e481cad107
           Boot ID: c413def3ac1049c9b8e7349111df10ec
  Operating System: Poky (Yocto Project Reference Distro) 3.1.11 (dunfell)
            Kernel: Linux 5.4.180-amlogic
      Architecture: arm64
```



```
sh-5.0# localectl
   System Locale: LANG=C
       VC Keymap: n/a
      X11 Layout: n/a
```

```
sh-5.0# timedatectl
               Local time: Thu 2022-07-07 06:44:51 UTC
           Universal time: Thu 2022-07-07 06:44:51 UTC
                 RTC time: Thu 2022-07-07 06:44:51
                Time zone: UTC (UTC, +0000)
System clock synchronized: yes
              NTP service: active
          RTC in local TZ: no
```

### 查看开机启动项

```
systemctl list-unit-files | grep enable
```

## systemd-analyze

systemd-analyze 是 Linux 自带的分析系统启动性能的工具。

有这些子命令：

```
Commands:
  time                     Print time spent in the kernel
  blame                    Print list of running units ordered by time to init
  critical-chain [UNIT...] Print a tree of the time critical chain of units
  plot                     Output SVG graphic showing service initialization
  dot [UNIT...]            Output dependency graph in man:dot(1) format
  log-level [LEVEL]        Get/set logging threshold for manager
  log-target [TARGET]      Get/set logging target for manager
  dump                     Output state serialization of service manager
  syscall-filter [NAME...] Print list of syscalls in seccomp filter
  verify FILE...           Check unit files for correctness
  calendar SPEC...         Validate repetitive calendar time events
  service-watchdogs [BOOL] Get/set service watchdog state
```



```
$ systemd-analyze time
Startup finished in 7.899s (kernel) + 12min 17.518s (userspace) = 12min 25.417s
graphical.target reached after 39.359s in userspace
```



# 问题解决

## systemctl start audioservice会先start再stop

从日志中看

```
-- Logs begin at Fri 2022-07-08 02:41:57 UTC, end at Fri 2022-07-08 02:47:43 UTC. --
Jul 08 02:41:58 mesona5-av400 systemd[1]: Started Start the audioservice.
Jul 08 02:41:58 mesona5-av400 audioservice_ctl.sh[840]: Starting audioservice: OK
Jul 08 02:41:58 mesona5-av400 audioservice_ctl.sh[886]: Stopping audioservice:
Jul 08 02:41:58 mesona5-av400 audioservice_ctl.sh[938]: Stopping homeapp: No such process
Jul 08 02:41:58 mesona5-av400 audioservice_ctl.sh[886]: OK
```

自动调用了stop。这不合理啊。

分析原因：

查阅了很多资料，都没有找到具体明确的解释。systemctl中service在start （ExecStop）后马上调用了ExecStop的内容，我猜测原因是systemctl status test.device，处于inactive，systemctl在service处于inactive状态时会自动调用ExecStop

所以解决办法就是增加

 RemainAfterExit=yes

这样，service在运行后就会处于active状态，就不会调用stop了。

参考资料

https://blog.csdn.net/Peter_JJH/article/details/108446380

# ExecStart可以阻塞吗

导致此问题的原因是：hello.service类型选择有问题, 不应该选forking类型；类型改为Type=simple（或删除Type=forking这句），问题便得到解决。

这样：

```
python3 -m http.server  --directory /home/teddy/.config/clash/clash-dashboard/dist 3000
```



https://www.csdn.net/tags/MtTaMg1sNTczNjk0LWJsb2cO0O0O.html

# sysvinit回顾

sysvinit 就是 System V 风格的 init 系统，

顾名思义，它源于 System V 系列的 UNIX。

最初的 linux 发行版几乎都是采用 sysvinit 作为 init 系统。

sysvinit 用术语 runlevel 来定义 "预订的运行模式"。

比如 

runlevel 3 是命令行模式，

runlevel 5 是图形界面模式，

runlevel 0 是关机，

runlevel 6 是重启。

sysvinit 会按照下面的顺序按部就班的初始化系统：

sysvinit 会按照下面的顺序按部就班的初始化系统：

- 激活 udev 和 selinux
- 设置定义在 /etc/sysctl.conf 中的内核参数
- 设置系统时钟
- 加载 keymaps
- 启用交换分区
- 设置主机名(hostname)
- 根分区检查和 remount
- 激活 RAID 和 LVM 设备
- 开启磁盘配额
- 检查并挂载所有文件系统
- 清除过期的 locks 和 PID 文件
- 最后找到指定 runlevel 下的脚本并执行，其实就是启动服务。



除了负责初始化系统，sysvinit 还要负责关闭系统，

主要是在系统关闭是为了保证数据的一致性，

需要小心地按照顺序进行任务的结束和清理工作。

另外，sysvinit 还提供了很多管理和控制系统的命令，比如 halt、init、mesg、shutdown、reboot 等等。

sysvinit 的优点是概念简单。

特别是服务(service)的配置，只需要把启动/停止服务的脚本链接接到合适的目录就可以了。

sysvinit 的另一个重要优点是确定的执行顺序，

脚本严格按照顺序执行(sysvinit 靠脚本来初始化系统)，一个执行完毕再执行下一个，这非常有益于错误排查。



同时，完全顺序执行任务也是 sysvinit 最致命的缺陷。

如果 linux 系统只用于服务器系统，

那么漫长的启动过程可能并不是什么问题，毕竟我们是不会经常重启服务器的。

但是现在 linux 被越来越多的用在了桌面系统中，漫长的启动过程对桌面用户来说是不能接受的。

除了启动慢，sysvinit 还有一些其它的缺陷，

比如不能很好的处理即插即用的设备，对网络共享磁盘的挂载也存在一定的问题，

于是 init 系统开始了它的进化之旅。

# upstart

由于 sysvinit 系统的种种弊端，[Ubuntu](https://www.linuxidc.com/topicnews.aspx?tid=2) 的开发人员决定重新设计和开发一个全新的 init 系统，即 upstart 。upstart 是第一个被广泛应用的新一代 init 系统。

upstart 基于事件机制，

比如 U 盘插入 USB 接口后，udev 得到内核通知，发现该设备，这就是一个新的事件。

upstart 在感知到该事件之后触发相应的等待任务，比如处理 /etc/fstab 中存在的挂载点。

采用这种事件驱动的模式，upstart 完美地解决了即插即用设备带来的新问题。

采用事件驱动机制也带来了一些其它有益的变化，比如加快了系统启动时间。

sysvinit 运行时是同步阻塞的。一个脚本运行的时候，后续脚本必须等待。

这意味着所有的初始化步骤都是串行执行的，而实际上很多服务彼此并不相关，完全可以并行启动，从而减小系统的启动时间。



upstart 的特点

upstart 解决了之前提到的 sysvinit 的缺点。采用事件驱动模型的 upstart 可以：

- 更快地启动系统
- 当新硬件被发现时动态启动服务
- 硬件被拔除时动态停止服务

这些特点使得 upstart 可以**很好地应用在桌面或者便携式系统**中，处理这些系统中的动态硬件插拔特性。

# systemd

systemd 是 linux 系统中最新的初始化系统(init)，它主要的设计目标是克服 sysvinit 固有的缺点，提高系统的启动速度。

systemd 和 ubuntu 的 upstart 是竞争对手，

但是时至今日 ubuntu 也采用了 systemd，所以 systemd 在竞争中胜出，大有一统天下的趋势。

其实，systemd 的很多概念都**来源于苹果 Mac OS 操作系统上的 launchd**。

systemd 的优点是功能强大，使用方便，

缺点是体系庞大，非常复杂，

下图展示了 systemd 的架构(此图来自互联网)：



systemd 能够在与 upstart 的竞争中胜出自然有很多过人之处，接下来让我们介绍一些 systemd 的主要优点。

**兼容性**

systemd 提供了和 sysvinit 兼容的特性。系统中已经存在的服务和进程无需修改。这降低了系统向 systemd 迁移的成本，使得 systemd 替换现有初始化系统成为可能。

**启动速度**

systemd 提供了比 upstart **更激进的并行启动能力**，采用了 socket / D-Bus activation 等技术启动服务。一个显而易见的结果就是：更快的启动速度。为了减少系统启动时间，systemd 的目标是：

- 尽可能启动更少的进程
- 尽可能将更多进程并行启动

同样地，upstart 也试图实现这两个目标。下图展示了 upstart 相对于 sysvinit 在并发启动这个方面的改进(此图来自互联网)：



upstart 增加了系统启动的并行性，从而提高了系统启动速度。但是在 upstart 中，有依赖关系的服务还是必须先后启动。比如任务 A,B,(C,D)因为存在依赖关系，所以在这个局部，还是串行执行。

systemd 能够更进一步提高并发性，即便对于那些 upstart 认为存在相互依赖而必须串行的服务，比如 Avahi 和 D-Bus 也可以并发启动。从而实现如下图所示的并发启动过程(此图来自互联网)：



在 systemd 中，所有的任务都同时并发执行，总的启动时间被进一步降低为 T1。可见 systemd 比 upstart 更进一步提高了并行启动能力，极大地加速了系统启动时间。

# system V

**UNIX System V**是[Unix](https://zh.wikipedia.org/wiki/Unix)[操作系统](https://zh.wikipedia.org/wiki/操作系统)众多版本中的一支。

它最初由[AT&T](https://zh.wikipedia.org/wiki/AT%26T)开发，在1983年第一次发布，因此也被称为**AT&T System V**。

一共发行了4个System V的主要版本：版本1、2、3和4。

System V Release 4，或者称为SVR4，是最成功的版本，

成为一些UNIX共同特性的源头，

例如“SysV [初始化](https://zh.wikipedia.org/wiki/初始化)脚本”（`/etc/init.d`），用来控制系统启动和关闭，

*System V Interface Definition*（SVID）是一个System V如何工作的标准定义。

AT&T出售运行System V的专有硬件，

但许多（或许是大多数）客户在其上运行一个转售的版本，这个版本基于AT&T的[实现说明](https://zh.wikipedia.org/w/index.php?title=实现说明&action=edit&redlink=1)。

流行的SysV派生版本包括Dell SVR4和Bull SVR4。

当今广泛使用的System V版本是[SCO](https://zh.wikipedia.org/wiki/SCO) [OpenServer](https://zh.wikipedia.org/wiki/OpenServer)，基于System V Release 3，以及[SUN](https://zh.wikipedia.org/wiki/昇陽電腦) [Solaris](https://zh.wikipedia.org/wiki/Solaris)和SCO [UnixWare](https://zh.wikipedia.org/w/index.php?title=UnixWare&action=edit&redlink=1)，都基于System V Release 4。



System V是AT&T的第一个商业UNIX版本（[UNIX System III](https://zh.wikipedia.org/wiki/UNIX_System_III)）的加强。

传统上，System V被看作是两种UNIX“风味”之一（另一个是[BSD](https://zh.wikipedia.org/wiki/BSD)）。

然而，随着一些并不基于这两者代码的类UNIX实现的出现，

例如[Linux](https://zh.wikipedia.org/wiki/Linux)和[QNX](https://zh.wikipedia.org/wiki/QNX)，这一归纳不再准确，但不论如何，像[POSIX](https://zh.wikipedia.org/wiki/POSIX)这样的标准化努力一直在试图减少各种实现之间的不同。



# 参考资料

1、systemd

https://baike.baidu.com/item/systemd/18473007

2、systemd (简体中文)

https://wiki.archlinux.org/index.php/Systemd_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)

3、关于 systemd 的初步理解

https://www.linuxidc.com/Linux/2018-03/151291.htm

4、

http://www.jinbuguo.com/systemd/systemd.unit.html

5、

https://www.ruanyifeng.com/blog/2016/03/systemd-tutorial-commands.html