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

## 发展历史

systemd 是一个现代化的初始化系统和系统管理器，它在 Linux 系统中扮演着重要的角色。下面是 systemd 的发展历史的主要里程碑：

1. 2010 年：systemd 项目开始：systemd 项目由德国开发者 Lennart Poettering 发起，旨在重新设计和改进 Linux 系统的初始化和管理方式。最初版本的 systemd 于 2010 年首次发布。

2. 2011 年：systemd 在 Fedora 中引入：Fedora Linux 社区采纳了 systemd 作为默认的初始化系统，成为第一个广泛采用 systemd 的 Linux 发行版。systemd 在 Fedora 15 中首次作为默认的初始化系统亮相。

3. 2012 年：systemd 的广泛采用：随着时间的推移，越来越多的 Linux 发行版开始采用 systemd。其中包括 Red Hat Enterprise Linux (RHEL)、CentOS、Debian、Ubuntu 等，使 systemd 成为事实上的标准初始化系统。

4. 2014 年：systemd 成为标准化项目：systemd 成为 Linux 基金会主导的标准化项目，并得到了许多开发者和厂商的支持。这一举措旨在进一步推动 systemd 的发展和统一 Linux 系统管理方式。

5. 2015 年：systemd 发布版本 220：systemd 的版本 220 在 2015 年发布，引入了许多新功能和改进，包括 cgroups 集成、网络管理、命名空间隔离等。

6. 2016 年：systemd 项目扩展：除了初始化系统外，systemd 项目开始涉足其他领域，如容器管理（systemd-nspawn）、日志管理（systemd-journald）和网络管理（systemd-networkd）等。这些组件提供了对整个系统的综合管理能力。

7. 进一步发展：随着时间的推移，systemd 持续演进和发展。每个版本都引入了新的功能、改进和修复。systemd 的目标是提供一个高度集成和功能丰富的系统管理平台，以改善 Linux 系统的启动速度、管理效率和可靠性。

总体而言，systemd 作为一个重要的系统管理框架，通过简化和优化 Linux 系统的初始化和管理过程，为用户和开发者提供了更好的体验和工具。它在 Linux 社区中的广泛采用和持续发展表明了其在现代 Linux 系统中的重要性和影响力。

## 技术

systemd 是基于多种技术和概念构建的，下面列举了一些 systemd 所基于的关键技术和组件：

1. Linux cgroups (Control Groups)：cgroups 是 Linux 内核中的一个功能，用于限制、控制和分离进程组的资源使用。systemd 使用 cgroups 来管理和控制进程的资源分配和限制，包括 CPU、内存、磁盘等。

2. Linux namespaces：命名空间是 Linux 内核提供的一种隔离机制，用于将进程的资源隔离到独立的环境中。systemd 利用命名空间来创建独立的进程隔离环境，确保各个进程组件在彼此之间的隔离运行。

3. D-Bus：D-Bus 是一种消息传递系统，用于进程间通信和组件之间的交互。systemd 使用 D-Bus 实现不同组件之间的通信，如 systemd 命令行工具与 systemd 守护进程之间的通信。

4. udev：udev 是 Linux 内核的一个子系统，用于动态设备管理。systemd 利用 udev 来监测和管理系统中的设备，包括设备的插拔、识别和设备事件的处理。

5. journald：journald 是 systemd 提供的日志管理系统，用于收集、存储和管理系统的日志信息。它使用二进制格式来存储日志，并提供高效的查询和过滤功能。

6. sysvinit 兼容性：为了保持与旧有的 sysvinit 兼容，systemd 提供了 sysvinit 兼容层，允许在 systemd 系统中运行传统的 sysvinit 脚本。

此外，systemd 还利用其他技术和工具来实现诸如网络管理（systemd-networkd）、容器管理（systemd-nspawn）、时间管理（systemd-timesyncd）等功能。

总体而言，systemd 结合了多种先进的 Linux 技术和组件，以提供一个全面且高度集成的初始化系统和系统管理框架。它的设计目标是改善系统的启动速度、资源管理、日志管理等方面的性能和可靠性，并提供更好的系统管理工具和功能。



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

## 怎样兼容sysvinit

systemd 提供了与 sysvinit 的兼容层，以确保在 systemd 系统中可以运行传统的 sysvinit 脚本。这种兼容性层的存在使得许多基于 sysvinit 的脚本和服务可以在 systemd 系统中无需修改而继续运行。以下是 systemd 如何兼容 sysvinit 的主要方式：

1. SysV init 脚本支持：systemd 支持运行 sysvinit 风格的初始化脚本。当系统启动时，systemd 可以解析并运行位于 `/etc/init.d/` 目录下的 sysvinit 脚本。

2. 启动级别兼容性：sysvinit 使用运行级别（runlevel）来定义系统在不同阶段的运行状态。systemd 提供了与 sysvinit 运行级别相对应的目标（target），以便在系统启动时执行相应的任务和服务。系统管理员可以使用 `systemctl` 命令切换到不同的目标，实现与 sysvinit 的启动级别兼容性。

3. SysV init 环境变量兼容性：sysvinit 使用一些特定的环境变量来定义服务的行为和配置。systemd 提供了与 sysvinit 环境变量相对应的兼容性，以确保 sysvinit 脚本在 systemd 环境下能够正确读取和使用这些环境变量。

需要注意的是，尽管 systemd 具有与 sysvinit 的兼容性层，但并不是所有的 sysvinit 脚本和功能都能完全适用于 systemd 系统。某些高级特性和功能可能需要进行适当的修改或迁移以与 systemd 兼容。

此外，systemd 提供了更先进和强大的服务管理功能，包括并行启动、依赖关系管理、故障恢复等，以取代传统的 sysvinit 脚本方式。因此，在新的 systemd 系统中，建议使用 systemd 的原生服务单元（service unit）来管理和配置服务，以充分发挥 systemd 的优势和功能。

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



systemd 自带了一个名为 journald 的日志服务，它是 systemd 日志管理系统的一部分。journald 提供了一种现代化的方法来收集、存储和管理系统日志。

以下是 journald 的一些特点和功能：

1. 二进制日志格式：journald 使用二进制格式来存储日志，而不是传统的文本文件。这种格式可以提供更高的性能和更紧凑的存储，同时支持更丰富的元数据。

2. 结构化日志数据：journald 允许将日志数据结构化为字段，每个字段包含特定的信息。这使得日志数据更易于分析、搜索和过滤，并支持高级的日志查询语言。

3. 日志数据的持久化：journald 将日志数据持久化存储在磁盘上，以便在系统重启后仍然可用。这有助于日志的长期保存和审计。

4. 压缩和轮转：journald 可以自动对日志进行压缩和轮转，以限制日志文件的大小并管理磁盘空间的使用。

5. 日志转发：journald 支持将日志转发到远程日志服务器，以实现集中化的日志收集和分析。

6. 日志优先级和元数据：journald 具有对日志条目的优先级进行分类的能力，并支持添加额外的元数据（如时间戳、进程ID、用户ID等）以便更详细地描述日志。

7. 安全性：journald 支持对日志进行访问控制，以确保只有授权用户或进程能够读取敏感的日志数据。

通过 journald，systemd 提供了一个集成的日志管理系统，使得日志记录、存储和分析更加方便和高效。同时，它还与其他 systemd 组件紧密集成，例如 systemd 单元的状态和事件与日志数据关联，从而提供更全面的系统监控和故障排查能力。

# 基础概念

系统在初始化的过程，需要做很多的事情：

1、启动服务。

2、配置，例如挂载文件系统。

## unit

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



systemd 单元（unit）可以分为几个不同的分类，每个分类代表不同的系统组件或服务类型。以下是 systemd 单元的常见分类：

1. 服务单元（Service Units）：.service
   服务单元代表系统中的一个服务或守护进程。它定义了如何启动、停止、重启和管理一个特定的服务。服务单元通常对应于在系统中运行的后台进程，如网络服务、数据库服务、Web 服务器等。

2. 目标单元（Target Units）：.target
   目标单元是一组相关的服务单元的集合。它们用于定义系统启动时的目标，表示系统应该达到的特定状态。目标单元通常用于表示不同的运行级别或系统模式，如图形模式、多用户模式、救援模式等。

3. 设备单元（Device Units）：.device
   设备单元表示系统中的硬件设备。它们用于管理设备的初始化、配置和使用。设备单元可以用于挂载磁盘、管理网络接口、控制输入设备等。

4. 挂载单元（Mount Units）：.mount
   挂载单元用于管理文件系统的挂载和卸载。它定义了如何挂载和卸载特定的文件系统，包括本地文件系统、网络文件系统等。

5. 定时器单元（Timer Units）：.timer
   定时器单元用于执行预定的任务或触发事件。它可以设置定期运行的任务、延时触发的任务或周期性触发的任务。定时器单元通常用于计划定期备份、定时任务、日志轮转等。

6. 路径单元（Path Units）：.path
   路径单元监控文件或路径的状态变化，并在满足条件时触发相关操作。它可以用于监控特定文件或目录的创建、删除、修改等事件，并触发相应的操作。

除了以上列举的单元类型，systemd 还支持其他一些单元类型，如作用域单元（Scope Units）、片段单元（Slice Units）等。每个单元类型都有特定的目的和功能，用于管理不同的系统组件和服务。可以根据需要选择合适的单元类型来定义和管理系统中的各个组件。

## chatgpt回复的基本概念

systemd 是一个初始化系统和系统管理器，具有一些基本概念，下面是 systemd 的一些基本概念和术语：

1. Service Units（服务单元）：服务单元是 systemd 中用于定义和管理服务的配置单元。每个服务都有一个对应的服务单元文件，其中包含服务的配置和行为。服务单元文件通常以 `.service` 扩展名结尾，并存放在 `/etc/systemd/system/` 或 `/usr/lib/systemd/system/` 目录中。

2. Target Units（目标单元）：目标单元是 systemd 中用于组织和控制一组相关服务的单元。目标单元类似于 sysvinit 中的运行级别（runlevel），用于定义系统在不同阶段的运行状态。每个目标单元都有一个对应的目标单元文件，通常以 `.target` 扩展名结尾。

3. Unit Files（单元文件）：单元文件是 systemd 中用于配置各种单元的文本文件。除了服务单元和目标单元外，还有其他类型的单元文件，如设备单元、挂载单元、定时器单元等。单元文件采用 INI 风格的格式，定义了单元的属性和行为。

4. systemctl 命令：systemctl 是 systemd 的命令行工具，用于管理和控制 systemd 单元。通过 systemctl 命令，可以启动、停止、重启、启用、禁用和查询系统中的各种单元。

5. Journal（日志）：Journal 是 systemd 内置的日志管理系统，用于收集、存储和管理系统日志。Journal 使用二进制格式存储日志，并提供高级的日志查询和过滤功能。

6. Dependencies（依赖关系）：systemd 通过依赖关系来管理单元之间的启动顺序和关联。每个单元可以定义它所依赖的其他单元，以确保它们在正确的顺序下启动或停止。

7. Targets and Dependencies Graph（目标和依赖关系图）：systemd 通过目标和依赖关系图来表示单元之间的关系。目标单元形成一个层级结构，每个目标单元可以依赖于其他目标单元或服务单元，形成依赖关系图。

这些是 systemd 的一些基本概念和术语，它们共同构成了 systemd 的核心框架和功能。通过这些概念，systemd 提供了一种现代化和灵活的方式来管理和控制 Linux 系统的启动、服务、日志和其他关键组件。



# 依赖关系

依赖关系带来了复杂性，依赖关系，其实就是耦合性。

systemd已经尽力在降低各个服务之间的依赖性，但是无法完全消除。

systemd为了处理好依赖关系，提供了一些机制。

systemd 使用依赖关系来管理和控制单元（units）之间的启动顺序和关联。它使用依赖关系图（Dependency Graph）来表示单元之间的关系，并确保它们按照正确的顺序启动或停止。下面是 systemd 处理依赖关系的一些基本原则和机制：

1. 依赖类型：systemd 支持不同类型的依赖关系，包括 Requires、Wants、Requisite、Conflicts、Before、After 等。这些依赖类型定义了不同单元之间的关系和约束条件。

- Requires：表示一个单元依赖于另一个单元，并且需要在它启动之前启动。如果依赖的单元启动失败，系统将阻止启动依赖它的单元。
- Wants：类似于 Requires，但是如果依赖的单元启动失败，不会阻止启动依赖它的单元。
- Requisite：表示一个单元依赖于另一个单元，并且需要在它启动之前启动。与 Requires 类似，但是如果依赖的单元未启用，则会导致启动失败。
- Conflicts：表示一个单元与另一个单元冲突，它们不能同时运行。
- Before：表示一个单元需要在另一个单元之前启动。
- After：表示一个单元需要在另一个单元之后启动。

2. 依赖关系图：systemd 使用依赖关系图来表示单元之间的关系。依赖关系图是一个有向无环图（DAG），其中单元表示节点，依赖关系表示边。这个图形描述了各个单元之间的启动顺序和关联关系。

3. 依赖解析：systemd 在启动过程中进行依赖解析，根据单元的依赖关系图确定启动顺序。它会检查单元的依赖关系，并确保依赖的单元在合适的时候启动，以满足依赖关系。

4. 依赖满足和失败处理：当一个单元启动时，systemd 会检查它的依赖关系，确保所有依赖的单元都已经启动。如果某个依赖的单元启动失败，systemd 可以根据依赖类型的不同采取不同的行动，如阻止启动依赖它的单元或继续启动。

通过这些机制，systemd 可以精确控制和管理单元之间的启动顺序，确保依赖关系得到满足，并提供灵活的服务管理和控制能力。管理员可以使用 systemctl 命令查看和调

整单元之间的依赖关系，以满足特定的系统需求。







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



systemd 在 Linux 系统中涉及多个目录，用于存储配置文件、单元文件和其他相关文件。以下是 systemd 的一些重要目录：

1. /etc/systemd/system/：这个目录是系统管理员定义和配置 systemd 单元的主要位置。在这个目录中，可以创建和编辑服务单元、目标单元、挂载单元等各种类型的单元文件。

2. /usr/lib/systemd/system/：这个目录包含由发行版提供的系统安装的默认单元文件。这些单元文件通常是只读的，如果需要修改或覆盖这些单元文件，应将其拷贝到 /etc/systemd/system/ 目录下进行编辑。

3. /run/systemd/system/：这个目录存储运行时创建的临时单元文件。这些单元文件通常由系统或用户动态创建，用于临时调整 systemd 的行为或配置。

4. /etc/systemd/system.conf：这个文件是 systemd 的主要配置文件，包含全局的 systemd 配置选项。可以在这里配置系统的全局行为、日志设置、默认目标等。

5. /etc/systemd/systemd-logind.conf：这个文件是 systemd-logind 服务的配置文件，用于配置用户会话和登录管理相关的设置，如休眠、电源按钮行为、用户空闲超时等。

6. /etc/systemd/journald.conf：这个文件是 journald 日志服务的配置文件，用于配置系统日志的存储、转发、压缩、日志级别等设置。

7. /var/log/journal/：这个目录是 journald 日志服务的默认日志存储位置。系统的日志会以二进制格式存储在这个目录下，并按时间进行归档和轮转。

这些是 systemd 在 Linux 系统中涉及的一些重要目录。它们用于存储配置文件、单元文件和运行时数据，对于配置和管理 systemd 的行为和服务非常重要。

## unit配置文件的写法

## chatgpt回复

systemd 中的单元配置文件使用 INI（Initialization）风格的语法。每个单元（unit）对应一个单独的配置文件，具体写法如下所示：

1. 服务单元配置文件（.service）的写法：
```
[Unit]
Description=My Service
After=network.target

[Service]
ExecStart=/path/to/my/service
Restart=always

[Install]
WantedBy=default.target
```

2. 目标单元配置文件（.target）的写法：
```
[Unit]
Description=My Target
Requires=network.target

[Install]
WantedBy=default.target
```

3. 设备单元配置文件（.device）的写法：
```
[Unit]
Description=My Device
Before=network.target

[Device]
Driver=my-driver

[Install]
WantedBy=default.target
```

4. 挂载单元配置文件（.mount）的写法：
```
[Unit]
Description=My Mount
Requires=network.target

[Mount]
What=/dev/sdb1
Where=/mnt/my-mount
Options=defaults

[Install]
WantedBy=default.target
```

5. 定时器单元配置文件（.timer）的写法：
```
[Unit]
Description=My Timer

[Timer]
OnBootSec=5min
OnUnitActiveSec=1h
Unit=my-service.service

[Install]
WantedBy=timers.target
```

这只是单元配置文件的一些示例，具体的写法和可用的配置选项取决于不同类型的单元。每个配置文件都包含不同的段（Section），如 [Unit]、[Service]、[Install] 等，每个段下面包含相应的配置选项。可以根据需求添加、修改或删除相应的配置选项。

注意：配置文件的名称应与单元的名称相匹配，并以对应的扩展名结尾（例如，.service、.target 等）。配置文件通常存储在 `/etc/systemd/system/` 或 `/usr/lib/systemd/system/` 目录中。对于用户定义的单元，建议将配置文件放在 `/etc/systemd/system/` 目录中，而不是修改 `/usr/lib/systemd/system/` 目录中的默认配置文件。

以上是单元配置文件的基本写法，您可以根据具体的需求和单元类型进行相应的配置。

## 网上梳理

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

## chatgpt回复

systemd 提供了一系列命令用于管理和操作系统服务和单元。以下是一些常用的 systemd 命令：

1. systemctl：用于管理系统服务和单元。
   - 启动服务：`systemctl start <unit>`。
   - 停止服务：`systemctl stop <unit>`。
   - 重启服务：`systemctl restart <unit>`。
   - 查看服务状态：`systemctl status <unit>`。
   - 启用服务开机自启：`systemctl enable <unit>`。
   - 禁用服务开机自启：`systemctl disable <unit>`。
   - 查看服务日志：`systemctl --no-pager --full status <unit>`。

2. journalctl：用于管理和查看系统日志。
   - 查看所有日志：`journalctl`。
   - 查看特定单元的日志：`journalctl -u <unit>`。
   - 根据时间范围过滤日志：`journalctl --since "2023-01-01" --until "2023-01-02"`。
   - 实时查看日志：`journalctl -f`。

3. systemctl list-units：列出当前加载的所有单元。
   - 列出所有激活的服务：`systemctl list-units --type=service`。
   - 列出所有激活的目标：`systemctl list-units --type=target`。
   - 列出所有激活的设备：`systemctl list-units --type=device`。

4. systemctl list-dependencies：显示指定单元及其依赖关系。

5. systemctl show：显示指定单元的详细信息。

6. systemctl is-active：检查指定单元是否处于活动状态。

7. systemctl is-enabled：检查指定单元是否设置为开机自启。

这些命令提供了对 systemd 的基本管理和操作功能，您可以使用它们来启动、停止、重启服务，查看状态和日志，管理开机自启设置等。此外，systemd 还有其他一些命令和选项，可以根据具体需求查阅 systemd 的官方文档或使用 `man` 命令来获取更多详细信息。

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

## 发展历史

SysVinit是一种传统的Unix系统初始化系统，它具有很长的发展历史。以下是SysVinit的主要发展历史：

1. 早期的Unix系统：在早期的Unix系统中，启动和管理系统服务是通过启动脚本（init scripts）和`init`程序来完成的。这些脚本位于特定的目录中，由系统启动时的`init`进程依次执行，以启动和停止系统服务。

2. SysVinit的引入：SysVinit最早是由System V Unix操作系统引入的，它引入了一种标准的启动脚本格式和管理机制。SysVinit使用`/etc/init.d`目录中的启动脚本，并通过运行级别（runlevel）来管理系统的不同状态。每个运行级别都有特定的启动脚本集合，以在系统启动或切换运行级别时启动或停止相应的服务。

3. SysVinit的传统运行级别：SysVinit定义了一组传统的运行级别，如0（关机）、1（单用户模式）、2-5（多用户模式）等。每个运行级别都有预定义的系统服务启动和停止的方式。

4. SysVinit脚本的编写：编写SysVinit脚本需要遵循一定的规范和格式。脚本通常包含启动、停止和重启服务的动作，以及处理依赖关系和顺序执行的逻辑。

5. SysVinit的问题：尽管SysVinit在过去的许多年里是主流的初始化系统，但它也存在一些问题。其中之一是启动过程较慢，因为需要顺序执行多个启动脚本。此外，SysVinit对于并行启动和处理复杂的依赖关系相对较弱。

6. 现代替代方案的出现：随着计算机系统的发展和进步，出现了一些现代化的初始化系统，如Upstart和systemd。这些系统通过并行启动、事件驱动和更灵活的配置等特性来改进系统的启动性能和管理能力。

尽管SysVinit仍然在一些系统中得到使用，但在许多现代Linux发行版中，已经逐渐被更先进的初始化系统取代，以提供更强大、更高效的系统初始化和服务管理功能。



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