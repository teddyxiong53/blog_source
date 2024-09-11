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

# 资源收集

官网，这个是最全面和最权威的信息。

https://systemd.io/

systemd 中文版

https://www.bookstack.cn/read/systemd-zh/systemd.md

systemd 使用教程

https://developer.aliyun.com/article/502735

systemd系列文章

https://www.cnblogs.com/f-ck-need-u/p/14209781.html

一本pdf书籍

https://falksangdata.no/wp-content/uploads/2023/03/osdc_Pragmatic-systemd_2023.03.15.pdf



https://people.redhat.com/bbreard/presos/Demystifying_systemd_Summit_2020.pdf

systemd手册的中文翻译

http://www.jinbuguo.com/systemd/systemd.index.html

# arch为什么决定使用systemd

我花了太多时间争论 systemd 的缺陷

（例如：“它不是用 bash 编写的”，“它是由 Lennart Poettering 启动的”，“我不喜欢 systemd 的（可选）磁盘格式”日志”，“它使用 dbus”，“systemd 的 PID1 比 sysvinit 的 PID1 做的更多而且更大”，“我认为可能有其他项目可能正在做类似的事情。我真的不知道，但是我很确定它比 systemd 更好”而且我确定还有更多）。

我坚信 

1) 所有这些感知到的缺陷都不是缺陷，但实际上是好处 

2) 即使我错了，这些东西也不是非常重要。

所以，抛开这些：让我们忽略所有那些无聊的争论，我' 我将概述一些我觉得 systemd 很棒的地方，以及为什么我认为我们都应该对很快能够使用它感到非常兴奋。

排名不分先后：

## 0) 支持热插拔：

systemd 假定所有资源都可能随时出现和消失。

如果您在 systemd 启动后插入外部硬盘驱动器，它将被 fsck'ed 并正确安装。

这与 initscripts 不同，它依赖于在启动 fsck 时枚举并准备好所有磁盘，然后它依赖于在开始安装任何磁盘之前完成所有磁盘的 fsck。

热插拔很重要，不仅因为在系统运行时能够方便地插入/移除硬件，而且因为这就是 linux 内核启动的方式：

当内核意识到它时，每个设备似乎都是“热插拔”的，

因此通过非常快速的启动，我们不能再假设所有设备都准备就绪并在我们需要时等待我们（即使它们是在计算机启动时插入的）。

## 1）我们可以知道系统的状态：

systemd 跟踪所有守护进程，所有启动的进程，谁拥有什么，什么时候发生故障等。

此外，使用（很棒的）日志记录所有 syslog() 条目所有进程对 stdout/stderr 的写入都被 systemd 捕获。

这些存储有足够的元数据，因此您可以很容易地检索说“来自某个服务/二进制/pid 的所有条目”或“内核写入的关于给定设备的所有条目”等。

除了记录此信息，并向您展示，systemd 将允许您（轻松地）指定在各种可能的错误场景中要做什么：

“服务正常关闭/出现错误/在信号上”或“服务没有在指定时间发送其看门狗信号”或“

## 2) 它是模块化的：

现在 rc.sysinit 的所有内容都被拆分成许多独立的服务，

每个服务都有详细的文档并且易于理解。

也就是说，如果您不喜欢 systemd eg 的 fstab 处理方式，那么您可以编写自己的小助手（如果您愿意，可以使用 bash）来替换官方的。

在旧的 initscripts 中执行此操作要困难得多，

因为 

1) rc.sysinit 的哪些部分相互依赖并不那么清楚 

2) 您所做的任何更改都必须在每次更新时合并。

## 3) 它允许 dbus/udev 返回执行它们应该执行的任务：

udev 和 dbus 目前（误）用于按需启动守护进程/长时间运行的服务。

在 dbus 的情况下，这是设计使然，但在 udev 的情况下，它不是。

无论哪种方式，这都不是构建这些守护进程的目的，

因此为了与每个守护进程一个任务的 UNIX 原则保持一致，

我们现在可以让 systemd（它的工作是管理守护进程）接管这一切真是太好了。

也就是说，udev 和 dbus 都可以向 systemd 发出信号以启动某个守护进程，

并且它的行为就像以任何其他方式启动一样（您有日志、状态等）。

这解决的一个问题是某些守护进程中固有的竞争条件

（我认为 bluetoothd 在某些时候是有罪的）

允许两者在启动时尽快启动（比如通过将其放入 DAEMONS），并由 dbus 按需启动。

Systemd 确保这两种情况都可能发生，如果它们确实同时发生，您最终只会像预期的那样拥有一个守护进程实例。

## 4) 我们可以减少守护进程之间显式排序依赖的数量

（这可能需要对相关守护进程进行更改）：

使用套接字激活、自动挂载和 dbus 激活，

我们可以忘记诸如“dbus 必须在我们启动 avahi 之前运行”之类的事情" 

或 "yp-bind 必须在 networkmanager 之后启动"。

systemd 可以在任何守护进程启动之前尽早创建套接字，

然后在它开始启动时将套接字传递给相关的守护进程。

这意味着任何东西都可以连接到任何其他东西，

而不用关心另一个守护进程是否已经完成启动。

内核将在我们等待时简单地缓冲请求，并在可能的时候交付它们。

请注意，这实际上并没有删除任何依赖项（因此如果有循环依赖项，它们仍然会存在），

## 5) 我们免费获得了很多安全/沙盒功能：

您可以简单地向相关单元文件添加一些配置选项，以各种方式将它们与系统隔离。

这在以前当然也是可以的，但是它需要你在每个 rc 脚本中编写大量的样板代码，而且这种东西很容易出错，最好由了解这些东西的人进行审查。

## 6) systemd 服务文件可以（并且希望会！）被编写并分发到上游：

而不是每个发行版都编写自己的 rc 脚本（有他们自己的一组琐碎的错误和误解）可能最了解软件的人（上游）通过最了解 init 系统的人（systemd 开发人员）的一些输入，可以编写应该在任何地方都可以工作的“完美”服务。

我们已经看到了其中的一些，我认为这是非常有益的。

即使对于尚未使用 systemd 的发行版，这也将使他们至少知道该软件是如何初始化的。

## 7) systemd 是一个跨发行版的项目：

每个主要发行版和许多次要发行版都有人为 systemd 做出贡献。

最后我听说甚至有两个 debian 开发人员提交了对 repo 的访问权限，等等。

systemd upstream 非常适应不同的需求和不同的用例（只要它们是基于技术原因呈现的）并且到目前为止我们一直很高兴合作。

我们得到了很多长期在不同初始化系统上工作的人/项目的共同经验，我认为这是一个人可能拥有的最重要的“特性”之一。

## 8) logind 最终将实现 consolekit 应该做的事情：

我们现在可以跟踪用户会话和席位，即时分配资源权限等。这应该是另一条消息的主题，因为它太多了进入。我只想说我很高兴我们终于让这些功能发挥了应有的作用。

## 9) systemd 很快：

或者真的是这样吗？

有些人声称与 initscripts 相比没有区别，很少有人声称它更慢，绝大多数人声称它快得多。

我声称我真的不在乎。

以上几点（这只是我脑海中浮现出的想法，所以无论如何都不是详尽无遗的）

希望能让你相信 systemd 是正确的选择，无论它的速度如何，一旦你尝试了它，你可能会一个惊喜;-)



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

在你提供的这个条件中，`ConditionPathIsDirectory=/sys/class/bluetooth` 表示当`/sys/class/bluetooth`是一个目录时，

该systemd服务单元才会继续启动。如果`/sys/class/bluetooth`不是一个目录或者不存在，那么服务将不会启动。



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

`[Unit]`区块通常是配置文件的第一个区块，用来**定义 Unit 的元数据，以及配置与其他 Unit 的关系。**它的主要字段如下。

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

`[Service]`区块用来 Service 的配置，**只有 Service 类型的 Unit 才有这个区块**。它的主要字段如下。

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

### **target就是由多个unit组成的一个组。就跟文件夹和文件的关系一样。**

启动计算机的时候，需要启动大量的 Unit。如果每一次启动，都要一一写明本次启动需要哪些 Unit，显然非常不方便。

Systemd 的解决方案就是 Target。

简单说，Target 就是一个 Unit 组，包含许多相关的 Unit 。

启动某个 Target 的时候，Systemd 就会启动里面所有的 Unit。

从这个意义上说，Target 这个概念类似于"状态点"，启动某个 Target 就好比启动到某种状态。

传统的`init`启动模式里面，有 RunLevel 的概念，跟 Target 的作用很类似。

**不同的是，RunLevel 是互斥的，不可能多个 RunLevel 同时启动，但是多个 Target 可以同时启动。**

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

## 目录的命名风格

我从代码来看，很多xxctl的命令。

例如：loginctl、bootctl

代码写得还是很干净的。风格不错。

代码里虽然很大，但是架构还是比较清晰。

代码里的sd前缀表示systemd。



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



在 systemd 中，所有的任务都同时并发执行，**总的启动时间被进一步降低为 T1**。可见 systemd 比 upstart 更进一步提高了并行启动能力，极大地加速了系统启动时间。

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

# /etc/systemd/system目录说明

在 `/etc/systemd/system` 目录下，通常存放着 Systemd 系统单位文件的配置。Systemd 是一种初始化系统和系统管理工具，它使用单位文件来定义和配置系统服务、目标、挂载点、定时器等。

以下是 `/etc/systemd/system` 目录中常见的子目录及其作用的说明：

1. `multi-user.target.wants/`：该目录包含了符号链接，链接到要在多用户模式下启动的服务单元。这些符号链接决定了系统启动时默认要启动的服务。

2. `sockets/`：在该目录中，存放了 Systemd socket 单元文件的配置。Socket 单元用于监听网络连接请求，允许其他服务通过套接字与该服务进行通信。

3. `timers/`：该目录用于存放定时器单元文件的配置。定时器单元用于在特定时间或间隔触发系统任务或服务。

4. `targets/`：在该目录中，存放着目标单元文件的配置。目标单元是一组要启动或停止的服务单元的集合，类似于运行级别（runlevel）的概念。

5. `units/`：该目录包含其他类型的单位文件，如服务单元、设备单元、挂载点单元等。这些单位文件定义了具体的系统服务、设备或其他配置。

需要注意的是，`/etc/systemd/system` 目录中的单位文件的优先级高于 `/lib/systemd/system` 目录中的相同文件。因此，如果你希望修改或自定义系统单位的配置，建议在 `/etc/systemd/system` 目录中创建或编辑相应的单位文件。

在修改 Systemd 单位文件之前，请务必熟悉 Systemd 的工作原理和相关配置规则，并备份原始文件以防止意外的更改导致系统问题。



# /usr/lib/systemd目录分析

`/usr/lib/systemd` 目录是用于存放 systemd 系统服务单元文件的目录。在大多数 Linux 发行版中，systemd 是默认的初始化系统和服务管理器，负责启动和管理系统服务。

下面是 `/usr/lib/systemd` 目录中的一些常见子目录和文件：

- `system`: 该子目录包含了系统级别的服务单元文件，用于启动和管理系统的核心服务。这些服务单元文件通常以 `.service` 扩展名结尾，例如 `systemd-logind.service`、`network.service` 等。

- `user`: 该子目录包含了用户级别的服务单元文件，用于启动和管理特定用户的服务。每个用户可以在其用户目录下的 `~/.config/systemd/user/` 目录中创建自己的服务单元文件。

- `system-preset`: 该子目录包含系统级别的预设文件，用于控制哪些系统服务应该在启动时自动启用。这些预设文件的名称以 `.preset` 结尾，例如 `20-default.preset`。这些文件定义了系统服务的默认启动状态。

- `user-preset`: 该子目录包含用户级别的预设文件，用于控制哪些用户服务应该在用户登录时自动启用。这些预设文件的名称以 `.preset` 结尾。

- `system-generators` 和 `user-generators`: 这些子目录包含 systemd 生成器程序，用于根据系统配置和环境生成服务单元文件。生成器程序可以根据需要动态地生成服务单元文件。

除了上述子目录，`/usr/lib/systemd` 目录还可能包含其他与 systemd 相关的文件和目录，用于支持系统的启动和服务管理。

请注意，`/usr/lib/systemd` 目录通常是系统级别的，存放着系统的标准服务单元文件。如果你想为特定用户创建自定义的服务单元文件，可以使用 `~/.config/systemd/user/` 目录。



# systemd代码分析

systemd 是一个庞大而复杂的软件项目，由多个模块和组件组成。其代码托管在 GitHub 上，你可以通过以下链接访问 systemd 的代码仓库：

https://github.com/systemd/systemd

在该仓库中，你可以找到 systemd 的完整源代码，并浏览各个模块的实现细节。

systemd 项目的代码由 C 语言编写，涉及到多个子项目和组件，包括但不限于以下几个主要模块：

- `systemd`: 这是 systemd 项目的核心模块，包含了启动和管理系统服务的功能。它实现了 systemd 初始化进程，提供了 systemd 单元文件的解析、加载和管理功能，以及其他与系统启动和管理相关的功能。

- `systemd-journald`: 这是 systemd 的日志管理模块，负责收集、存储和管理系统日志。它实现了高性能的日志记录和查询功能，并与其他 systemd 组件集成。

- `systemd-networkd` 和 `systemd-resolved`: 这些模块负责系统的网络配置和解析器管理。`systemd-networkd` 提供了网络配置和管理功能，包括网络接口的配置、网络连接的管理等。`systemd-resolved` 则负责 DNS 解析器的管理和域名解析服务。

- `systemd-logind`: 这是 systemd 的用户会话管理模块，负责用户登录和会话管理。它实现了用户登录会话的追踪、用户权限管理、控制台会话的管理等功能。

除了以上列举的模块，systemd 还包括其他模块，如设备管理、定时任务管理、硬件配置等。

要进行深入的 systemd 代码分析，你可以通过克隆 systemd 的代码仓库，使用合适的开发工具（如文本编辑器、调试器等）浏览和分析各个模块的源代码。同时，systemd 官方文档和开发者社区也是获取关于 systemd 架构和实现细节的有用资源。

请注意，由于 systemd 是一个庞大而复杂的项目，代码分析可能需要一定的时间和专业知识。在进行代码分析之前，建议你对 systemd 的基本概念和功能有一定的了解，并准备好相应的开发环境和工具。



# Requires 和wants的区别

简单来说，就是必须和可以的区别。



在 Systemd 中，`Requires=` 和 `Wants=` 都是用于定义单元之间的依赖关系，但它们有一些关键的区别：

1. 强制依赖 vs. 可选依赖：
   - `Requires=`：表示当前单元对目标单元的**强制依赖**。如果目标单元无法启动或启动失败，当前单元将无法启动。这是一种必须满足的依赖关系。
   - `Wants=`：表示当前单元对目标单元的**可选依赖**。如果目标单元无法启动或启动失败，当前单元仍然可以继续启动。这是一种较为宽松的依赖关系。

2. 启动顺序：
   - `Requires=`：当启动当前单元时，Systemd 会自动启动和管理所有被强制依赖的目标单元，并确保它们在当前单元之前启动。
   - `Wants=`：当启动当前单元时，Systemd 会尝试启动和管理所有被可选依赖的目标单元，但它们的启动顺序不是强制的。当前单元可能在一些可选依赖未启动的情况下继续启动。

3. 故障处理：
   - `Requires=`：如果被强制依赖的目标单元启动失败或未启动，当前单元将无法启动，且可能触发错误处理机制。
   - `Wants=`：如果被可选依赖的目标单元启动失败或未启动，当前单元仍然可以继续启动，不会触发错误处理机制。

综上所述，`Requires=` 用于强制依赖关系，要求目标单元必须启动，而 `Wants=` 则用于可选依赖关系，目标单元的启动是可选的。根据具体需求，选择适当的依赖关系类型可以确保系统的正确启动顺序和可靠性。

# systemd启动过程分析



Systemd 是一个用于初始化和管理 Linux 系统的系统和服务的 init 系统。下面是 Systemd 启动过程的一般分析：

1. Boot Loader：系统启动时，Boot Loader（如 GRUB）加载内核镜像和初始化 RAM Disk。Boot Loader 还会加载指定的 init 系统（如 Systemd）作为系统的第一个进程。

2. Systemd 启动：**Systemd 被加载为系统的第一个进程，并负责后续的初始化和服务管理。它使用 `.target` 单元作为启动过程的关键点。**

3. Default Target：Systemd 根据配置文件中指定的默认目标（Default Target）启动。默认目标是一个由各种服务单元组成的目标，定义了系统启动时需要启动的服务和进程。

4. 依赖关系解析和并行启动：Systemd 通过解析各个服务单元之间的依赖关系，确定它们的启动顺序。Systemd 尝试最大限度地并行启动能够并行执行的服务单元，以提高启动速度。

5. 启动服务单元：Systemd 逐个启动每个服务单元，执行各自的启动脚本或程序。服务单元可以是系统服务、用户服务、套接字单元等。

6. 故障处理和错误恢复：Systemd 监控每个服务单元的启动过程，并在需要时进行故障处理和错误恢复。它可以重新启动失败的服务，尝试修复问题，并记录相关的日志信息。

7. 完成启动过程：一旦所有的服务单元都成功启动，Systemd 完成了系统的启动过程。此时，系统进入到指定的默认目标，并进入正常的运行状态。

需要注意的是，Systemd 的启动过程可能会因不同的发行版和配置而有所差异。具体的启动流程和步骤可以在相关的 Systemd 文档中找到。



# 所有service文件分析

```
alsa-restore.service
	负责在系统启动时还原之前保存的 ALSA 音频设置，以确保系统以正确的配置进行音频播放。
	
alsa-state.service
autovt@.service -> getty@.service
bluetooth.service
console-getty.service
container-getty@.service
dbus-org.freedesktop.hostname1.service -> systemd-hostnamed.service
dbus-org.freedesktop.portable1.service -> systemd-portabled.service
dbus-org.freedesktop.timedate1.service -> systemd-timedated.service
dbus.service
debug-shell.service
dhcpcd.service
dropbear.service
e2scrub_all.service
e2scrub_fail@.service
e2scrub_reap.service
e2scrub@.service
emergency.service
getty@.service
initrd-cleanup.service
initrd-parse-etc.service
initrd-switch-root.service
initrd-udevadm-cleanup-db.service
kmod-static-nodes.service
rc-local.service
rescue.service
rsyslog.service
serial-getty@.service
systemd-ask-password-console.service
systemd-ask-password-wall.service
systemd-boot-check-no-failures.service
systemd-exit.service
systemd-fsck-root.service
systemd-fsck@.service
systemd-halt.service
systemd-hostnamed.service
systemd-hwdb-update.service
systemd-initctl.service
systemd-journal-catalog-update.service
systemd-journald.service
systemd-journal-flush.service
systemd-kexec.service
systemd-machine-id-commit.service
systemd-modules-load.service
systemd-networkd.service
systemd-networkd-wait-online.service
systemd-network-generator.service
systemd-nspawn@.service
systemd-portabled.service
systemd-poweroff.service
systemd-pstore.service
systemd-reboot.service
systemd-remount-fs.service
systemd-resolved.service
systemd-suspend.service
systemd-sysctl.service
systemd-timedated.service
systemd-timesyncd.service
systemd-time-wait-sync.service
systemd-tmpfiles-clean.service
systemd-tmpfiles-setup-dev.service
systemd-tmpfiles-setup.service
systemd-udevd.service
systemd-udev-settle.service
systemd-udev-trigger.service
systemd-update-done.service
systemd-update-utmp-runlevel.service
systemd-update-utmp.service
systemd-vconsole-setup.service
systemd-volatile-root.service
system-update-cleanup.service
user-runtime-dir@.service
user@.service
wpa_supplicant-nl80211@.service
wpa_supplicant.service
wpa_supplicant@.service
wpa_supplicant-wired@.service
```

# /etc/systemd下的配置文件

在 `/etc/systemd` 目录下，存放了一些与 systemd 系统管理器相关的配置文件。这些配置文件用于定义和控制系统的各种服务、单元和其他功能。

以下是 `/etc/systemd` 目录中常见的一些配置文件：

- `/etc/systemd/system.conf`：这个文件包含了全局的 systemd 配置选项，可以对 systemd 的行为进行全局性的设置和调整。

- `/etc/systemd/logind.conf`：这个文件用于配置 systemd-logind 服务的行为，其中包含了与用户登录和会话管理相关的配置选项。

- `/etc/systemd/journald.conf`：这个文件用于配置 systemd-journald 服务的行为，其中包含了与系统日志记录和日志存储相关的配置选项。

- `/etc/systemd/network/`：这个目录存放了网络配置相关的文件，用于定义网络接口、网络连接和网络设置。

- `/etc/systemd/system/`：这个目录存放了用户自定义的 systemd 单元文件，可以在其中创建和管理自己的服务、套接字、挂载点等。

除了以上列出的文件和目录，`/etc/systemd` 还可以包含其他一些配置文件，这取决于系统的具体设置和安装的软件包。在这个目录中，你可以找到许多与 systemd 相关的配置文件，用于对系统行为进行个性化配置和调整。

需要注意的是，对这些配置文件的修改可能需要管理员权限，并且修改后可能需要重新加载 systemd 服务或重启系统才能生效。在对这些配置文件进行修改时，建议先备份原始文件，并谨慎进行修改，以免对系统的稳定性和功能产生不良影响。

# 用python写一个systemd服务

https://github.com/torfsen/python-systemd-tutorial



# systemctl --user daemon-reload

`systemctl --user daemon-reload` 是用于重新加载用户级别的 systemd 守护进程配置的命令。

在 Linux 系统上，systemd 是一个系统和服务管理器，它负责启动、停止和管理系统中的各种服务和进程。systemd 提供了用于管理系统级别服务的 `systemctl` 命令和用于管理用户级别服务的 `systemctl --user` 命令。

`daemon-reload` 是 `systemctl` 命令的一个选项，用于重新加载 systemd 的配置文件。当您对 systemd 的配置文件进行更改后，例如在 `/etc/systemd/system/` 目录中添加、修改或删除了服务配置文件，需要使用 `daemon-reload` 命令来通知 systemd 重新加载配置。这样 systemd 就能够读取并生效新的配置，以便正确管理相应的服务。

而 `systemctl --user daemon-reload` 命令则是针对用户级别的 systemd 配置。用户级别的 systemd 配置文件通常位于 `~/.config/systemd/user/` 目录下。使用 `systemctl --user daemon-reload` 命令会重新加载用户级别的 systemd 配置文件，使更改生效。

需要注意的是，`daemon-reload` 命令只是重新加载配置文件，并不会启动、停止或重新启动服务。要启动、停止或重新启动服务，需要使用 `systemctl` 命令的其他选项和参数。

总之，`systemctl --user daemon-reload` 命令用于重新加载用户级别的 systemd 配置文件，以使配置更改生效。

# systemd 同时采用 socket 式与 D-Bus

这个意味着什么呢？

## 基于socket做了什么功能？基于dbus做了什么功能？举例说明

基于 socket 的功能：
1. Socket 激活：Systemd 允许服务在需要时通过 socket 激活，即当有请求通过套接字连接到系统时，systemd 自动启动相应的服务并处理请求。这种机制可以实现按需启动服务，减少资源消耗。
   举例：一个 Web 服务器服务可以使用 socket 激活，当有客户端连接到指定端口时，systemd 会自动启动该服务并处理客户端请求。

2. 套接字传递：Systemd 支持套接字传递，允许服务在启动时接收传递过来的套接字连接。这样可以实现平滑的服务重启和无缝的套接字迁移。
   举例：一个负载均衡器服务在启动时可以接收传递过来的套接字连接，从而实现在服务重启期间不中断客户端连接的无缝切换。

基于 D-Bus 的功能：
1. 系统管理接口：Systemd 提供了 D-Bus 接口，可以通过该接口查询和控制系统的状态、管理单元的依赖关系、启动和停止服务等。用户可以通过 D-Bus API 与 systemd 进行交互，进行系统管理操作。
   举例：用户可以使用 D-Bus 接口查询系统中正在运行的服务、查看服务的状态、启动和停止指定的服务等。

2. 事件通知机制：Systemd 使用 D-Bus 来发送和接收系统事件的通知，可以实现服务状态变化、系统启动完成等事件的订阅和接收。
   举例：一个监控服务可以通过订阅 systemd 发送的事件通知来获取系统的状态变化，例如服务的启动、停止或失败状态，并根据事件采取相应的操作。

总结：
基于 socket，Systemd 提供了套接字激活和传递功能，使服务可以按需启动和接收套接字连接。
基于 D-Bus，Systemd 提供了系统管理接口和事件通知机制，使用户可以通过 D-Bus 接口与 systemd 进行交互，并获取系统状态和处理系统事件。



# systemd按需启动守护进程

在 systemd 中，可以通过配置服务的启动条件来实现按需启动守护进程。下面是一些常用的方法：

1. 使用 `Wants` 和 `After` 条件：可以在服务单元文件中使用 `Wants` 和 `After` 条件来定义守护进程的依赖关系。例如，假设你有一个服务 A 和一个守护进程 B，你希望 B 在 A 启动后启动。你可以在 B 的服务单元文件中添加以下配置：
   ```
   [Unit]
   Wants=A.service
   After=A.service
   ```

2. 使用 `Requires` 和 `After` 条件：类似于 `Wants` 和 `After` 条件，`Requires` 和 `After` 条件也可以用来定义依赖关系。不同之处在于，如果被依赖的服务启动失败，使用 `Requires` 条件会导致依赖的服务也无法启动。你可以根据需求选择适合的条件。

3. 使用 `BindsTo` 条件：`BindsTo` 条件用于指定一个服务与另一个服务绑定，并且当绑定的服务终止时，本服务也会被终止。这可以用于在需要特定守护进程运行时启动服务，并在守护进程终止时自动停止服务。

4. 使用 `Condition` 条件：`Condition` 条件允许你根据特定的条件来控制服务的启动。你可以在服务单元文件中使用诸如 `ConditionPathExists`、`ConditionPathIsDirectory`、`ConditionFileNotEmpty` 等条件，根据文件或目录的存在与否、非空状态等来确定服务是否启动。

这些条件可以结合使用，以满足更复杂的需求。通过配置适当的启动条件，你可以确保守护进程在需要时按需启动，并与其他服务之间建立正确的依赖关系。请注意，具体的配置方法可能因系统和服务的不同而有所差异，建议查阅 systemd 的文档和相关资源以获取更详细的信息。



# systemd快照和系统恢复说明

systemd提供了快照和系统恢复的功能，可以方便地创建和管理系统的快照，并在需要时将系统还原到先前的状态。下面是关于systemd快照和系统恢复的说明：

1. 快照（Snapshot）：快照是系统当前状态的镜像，包括所有运行的进程、挂载的文件系统、系统设置等。通过创建快照，可以在系统运行期间保存系统状态的副本，以便在需要时进行恢复。

2. 创建快照：使用`systemctl`命令和`snapshot`操作，可以创建系统的快照。例如，要创建一个名为`mysnapshot`的快照，可以运行以下命令：
   ```
   sudo systemctl snapshot mysnapshot
   ```

3. 查看快照列表：使用`systemctl`命令和`list-snapshots`操作，可以列出所有可用的系统快照。例如，要查看系统中所有的快照，可以运行以下命令：
   ```
   sudo systemctl list-snapshots
   ```

4. 恢复系统：通过恢复快照，可以将系统还原到先前的状态。使用`systemctl`命令和`rollback`操作，可以恢复系统到指定的快照。例如，要将系统恢复到名为`mysnapshot`的快照，可以运行以下命令：
   ```
   sudo systemctl rollback mysnapshot
   ```

   在恢复过程中，系统将会停止当前运行的服务和进程，并还原到快照中保存的状态。

5. 清除快照：使用`systemctl`命令和`delete`操作，可以清除指定的系统快照。例如，要删除名为`mysnapshot`的快照，可以运行以下命令：
   ```
   sudo systemctl delete mysnapshot
   ```

   清除快照将永久删除快照的相关信息和状态，并释放占用的系统资源。

请注意，使用快照和系统恢复功能需要root权限。确保在操作之前充分了解相关风险，并谨慎使用。在进行系统恢复之前，建议先备份重要的数据和配置文件。详细的系统恢复流程和相关操作可以参考systemd的文档和官方资源。

# SysV 和 LSB 初始脚本比较

SysV（System V）和LSB（Linux Standard Base）是两种用于启动和管理系统服务的脚本标准。下面是SysV和LSB初始脚本的比较：

1. 标准：SysV脚本是最早的Unix系统初始化脚本标准，而LSB是为Linux系统定义的标准。

2. 兼容性：LSB脚本基于SysV脚本，并添加了一些额外的功能和标准化的命名约定，以提高脚本的可移植性和兼容性。

3. 文件位置：SysV脚本通常存储在`/etc/init.d`目录下，而LSB脚本通常存储在`/etc/init.d`目录下，同时使用符号链接将其链接到`/etc/rc.d`目录中的特定运行级别。

4. 注释：LSB脚本要求包含一组特定的注释行，用于指定脚本的信息、依赖关系和功能。这些注释行使得脚本更易于阅读和管理。

5. 命令行参数：LSB脚本定义了一组通用的命令行参数，用于控制服务的启动、停止、重启和状态查询等操作。这些参数在不同的系统上具有一致的行为。

6. 依赖关系：LSB脚本使用特定的依赖关系声明语法，用于指定服务的启动顺序和依赖关系。这样可以确保在启动或停止服务时正确处理依赖关系。

7. 运行级别：SysV脚本使用运行级别（runlevel）来确定何时启动或停止服务。而LSB脚本使用init系统的控制命令（如`start`、`stop`、`restart`）来控制服务的状态。

8. 规范化：LSB脚本的目标是提供一套规范化的脚本格式和功能，使得不同发行版的Linux系统能够共享和交换脚本。

总体而言，LSB脚本是对SysV脚本的一种扩展和改进，旨在提供更一致、可移植和易管理的系统服务脚本。LSB脚本具有更多的标准化要求和功能，以提高脚本的可靠性和互操作性。然而，在某些较旧的系统上，仍然可以使用SysV脚本。具体使用哪种脚本取决于所使用的Linux发行版和个人偏好。

# systemd怎样运行容器和虚拟机

systemd是一个功能强大的初始化系统和服务管理器，它可以用于运行容器和虚拟机。下面是关于如何使用systemd运行容器和虚拟机的一般步骤：

1. 容器：systemd通过其内置的`systemd-nspawn`工具来管理和运行容器。`systemd-nspawn`提供了一种在一个隔离的容器环境中启动和管理进程的方式。

   - 创建容器：使用`machinectl`命令创建一个新的容器，例如：`machinectl --quiet --uidmap=auto --setenv=SYSTEMD_NSPAWN_PRIVATE_NETWORK=1 --collect systemd-nspawn -D /path/to/container-rootfs`。
   - 进入容器：使用`machinectl`命令进入已创建的容器，例如：`machinectl shell <container-name>`。
   - 管理容器：在容器中使用`systemctl`命令来管理容器内的服务和进程，例如：`systemctl start <service-name>`。
   - 停止容器：使用`machinectl`命令停止容器，例如：`machinectl poweroff <container-name>`。

2. 虚拟机：systemd可以与虚拟化技术（如KVM、QEMU等）结合使用来管理和运行虚拟机。

   - 创建虚拟机：使用虚拟化工具（如`virt-install`）创建一个新的虚拟机，指定其磁盘镜像、内存、CPU等配置。
   - 启动虚拟机：使用虚拟化工具启动虚拟机，例如：`virsh start <vm-name>`。
   - 管理虚拟机：在虚拟机中，systemd将作为初始化系统运行，可以使用`systemctl`命令来管理虚拟机内的服务和进程，例如：`systemctl start <service-name>`。
   - 关闭虚拟机：使用虚拟化工具关闭虚拟机，例如：`virsh shutdown <vm-name>`。

需要注意的是，具体的操作步骤可能会因使用的发行版、虚拟化技术和配置而有所不同。建议参考相关文档和手册以获得更详细和针对特定环境的指导。

# systemd怎样进行日志管理

systemd提供了强大的日志管理功能，它使用`journald`作为系统日志收集和存储的后端。下面是一些systemd日志管理的常用功能和操作：

1. 查看日志：
   - 使用`journalctl`命令可以查看系统日志，例如：`journalctl`。
   - 可以根据不同的条件过滤和检索日志，例如：`journalctl -u <unit-name>`查看特定单元（服务）的日志。

2. 进行日志分析：
   - `journalctl`支持多种选项和过滤条件，可以根据时间范围、优先级、单元名称等进行过滤和排序。
   - 可以使用`journalctl`的`-f`选项实时跟踪日志输出。

3. 设定日志存储限制：
   - 通过systemd的日志存储限制，可以控制日志文件的大小和保留时间。可以在`/etc/systemd/journald.conf`文件中配置相关选项。

4. 定义日志转发：
   - `journald`支持将日志转发到远程系统或日志聚合服务器。可以在`/etc/systemd/journald.conf`文件中配置相关选项。

5. 生成日志摘要：
   - `journalctl`提供了`--output`选项，可以选择不同的输出格式，如`short`、`json`、`export`等。

6. 日志压缩和旋转：
   - `journald`可以自动压缩和旋转日志文件，以节省磁盘空间。相关配置可以在`/etc/systemd/journald.conf`文件中进行设置。

7. 日志持久化：
   - systemd的日志是持久化的，默认情况下日志将保存到磁盘上的`/var/log/journal`目录中。

这些只是systemd日志管理的一些常见功能和操作，systemd还提供了更多高级的日志分析和管理功能。建议查阅systemd和journald的官方文档以获取更详细的信息和指南。



# systemd初始化流程

systemd 是一种现代的初始化系统，负责在 Linux 系统启动过程中进行进程管理、服务管理和资源管理等任务。下面是 systemd 的简要初始化流程：

1. Bootloader 载入内核：系统启动时，Bootloader（如GRUB）负责加载内核映像到内存中，并将控制权交给内核。

2. 内核初始化：内核在启动过程中进行各种初始化操作，包括硬件检测、内存管理、设备驱动加载等。

3. systemd 启动：在内核初始化完成后，systemd 作为第一个用户空间进程启动。systemd 是一个 PID 为 1 的进程，负责初始化系统环境。

4. systemd 初始化阶段：
   - systemd 读取并解析配置文件，包括 `/etc/systemd/system.conf` 和 `/etc/systemd/system/*.conf` 等，以确定系统的默认行为和配置选项。
   - systemd 建立基础的系统环境，包括挂载文件系统、设置主机名、启动 udev 服务等。

5. 启动基本系统服务：**systemd 会按照依赖关系和启动顺序启动各个系统服务，以提供基本的功能支持。这些服务可能包括网络管理、日志记录、时间同步等。**

6. 触发默认目标（default target）：systemd 会根据配置文件中指定的默认目标，启动该目标所关联的一组服务。**默认目标通常是 graphical.target（图形界面）或 multi-user.target（多用户命令行界面）。**

7. 用户会话管理：systemd 会启动用户会话管理服务，负责管理用户登录和会话的生命周期。这包括启动用户登录管理器、创建用户会话、启动用户服务等。

总体而言，systemd 的初始化流程涉及解析配置文件、建立系统环境、启动系统服务和用户会话管理等关键步骤。通过这些步骤，systemd 管理着整个系统的启动和运行过程，提供了更加高效和灵活的初始化和管理功能。

## systemd 读取并解析配置文件的过程展开说一下

systemd 在启动过程中会读取和解析多个配置文件，以确定系统的默认行为和配置选项。下面展开说明 systemd 读取和解析配置文件的过程：

1. 系统配置文件：
   - `/etc/systemd/system.conf`：这个配置文件包含了全局的 systemd 配置选项。systemd 在启动时会读取并解析这个文件，以确定系统范围的默认行为。例如，可以在这个文件中配置日志记录方式、最大并发任务数、进程优先级等系统级设置。
   - `/etc/systemd/logind.conf`：这个配置文件包含了 systemd-logind 服务的配置选项，用于管理用户登录和会话。例如，可以在这个文件中配置休眠和唤醒行为、闲置会话超时等与用户会话相关的设置。

2. 单元配置文件：
   - `/etc/systemd/system/` 目录下的配置文件：这个目录包含了系统级别的单元配置文件，如服务单元（.service）、套接字单元（.socket）、设备单元（.device）等。这些配置文件用于定义系统服务和资源的行为。systemd 会递归地读取该目录下的所有配置文件，**并根据需要启动相应的单元。**

3. 用户配置文件：
   - `~/.config/systemd/user/` 目录下的配置文件：这个目录包含了用户级别的单元配置文件。每个用户可以在自己的家目录下创建这个目录，并在其中定义自己的 systemd 单元。这些配置文件用于管理用户级别的服务和资源。

4. 启动目标（target）配置文件：
   - `/etc/systemd/system/default.target`：这个配置文件指定了系统默认的启动目标。启动目标是一组相关联的单元，定义了在特定场景下应启动的服务。默认情况下，它可能指向 `graphical.target`（图形界面）或 `multi-user.target`（多用户命令行界面）。

在启动过程中，systemd 会按照上述顺序读取和解析配置文件。它会检查配置文件的语法和格式，并根据配置选项确定系统的默认行为。读取的配置信息将用于启动系统服务、管理资源、确定启动目标和用户会话等方面。

需要注意的是，systemd 的配置文件语法采用了INI文件格式，使用键值对的方式表示配置选项。每个配置文件中可以包含多个配置节（section），用于组织不同类型的配置。通过配置文件的灵活组织和配置选项的设置，可以对系统的行为进行精细调整和定制。

## /etc/systemd/system.conf 配置项有哪些

`/etc/systemd/system.conf` 是 systemd 的全局配置文件，用于设置系统范围的默认行为和配置选项。以下是一些常见的配置项：

1. `[Manager]` 配置节：
   - `LogLevel=`：设置 systemd 日志的详细级别。
   - `LogTarget=`：设置 systemd 日志的输出目标，可以是 `console`、`journal` 或文件路径。
   - `DefaultTimeoutStartSec=`：设置服务启动的默认超时时间。
   - `DefaultTimeoutStopSec=`：设置服务停止的默认超时时间。
   - `DefaultRestartSec=`：设置服务重启的默认延迟时间。
   - `DefaultLimitCORE=`：设置进程的默认核心转储限制。

2. `[Unit]` 配置节：
   - `DefaultDependencies=`：设置单元之间的默认依赖关系。
   - `DefaultRestartSec=`：设置单元重启的默认延迟时间。
   - `DefaultTimeoutStartSec=`：设置单元启动的默认超时时间。
   - `DefaultTimeoutStopSec=`：设置单元停止的默认超时时间。

3. `[Install]` 配置节：
   - `WantedBy=`：设置单元的默认安装位置。

4. `[Service]` 配置节：
   - `Type=`：设置服务的类型，可以是 `simple`、`forking`、`oneshot`、`dbus` 等。
   - `ExecStart=`：设置服务启动时要执行的命令或脚本。
   - `ExecStop=`：设置服务停止时要执行的命令或脚本。
   - `WorkingDirectory=`：设置服务的工作目录。
   - `Environment=`：设置服务的环境变量。
   - `Restart=`：设置服务重启的条件和策略。

以上仅列举了一些常见的配置项，实际上 `/etc/systemd/system.conf` 文件中还包含了更多的配置选项，可以根据需要进行定制和调整。在配置文件中，每个配置项的注释都提供了详细的说明，可以参考注释以了解每个配置项的作用和用法。



`/etc/systemd/system.conf` 是 `systemd` 的全局配置文件，控制系统服务和单元的行为。以下是一些常见的配置项及其描述：

| 配置项                   | 描述                                       |
| ------------------------ | ------------------------------------------ |
| `DefaultTimeoutStartSec` | 启动服务的默认超时时间（秒）。             |
| `DefaultTimeoutStopSec`  | 停止服务的默认超时时间（秒）。             |
| `DefaultRestart`         | 默认重启策略（如 `no`、`on-failure` 等）。 |
| `DefaultLimitNOFILE`     | 默认打开的文件描述符限制。                 |
| `DefaultLimitNPROC`      | 默认进程数限制。                           |
| `DefaultEnvironment`     | 为服务设置的环境变量。                     |
| `DefaultTasksMax`        | 默认最大任务数限制。                       |
| `DefaultLimitAS`         | 默认地址空间限制。                         |
| `DefaultLimitRSS`        | 默认常驻集大小限制。                       |
| `DefaultLimitFSIZE`      | 默认文件大小限制。                         |

### 示例

以下是一个 `/etc/systemd/system.conf` 文件的示例：

```ini
[Manager]
DefaultTimeoutStartSec=90s
DefaultTimeoutStopSec=30s
DefaultRestart=on-failure
DefaultLimitNOFILE=1024
DefaultTasksMax=512
```

### 说明

- **[Manager]**：指定这些配置项适用于 `systemd` 管理器。
- 大多数配置项可以在单个服务的单元文件中重写。

如果您需要更详细的信息或示例，请随时询问！

# systemd init的main函数入口在哪个文件里

在systemd的源代码中，systemd的初始化入口函数位于文件`src/core/main.c`中。在该文件中，有一个名为`main()`的函数，这是整个systemd的入口函数。在该函数中，会进行一系列的初始化操作，包括加载配置文件、启动各个系统服务、设置信号处理等。从该入口函数开始，systemd会根据配置和依赖关系来启动和管理系统中的各个组件和服务。

# systemd的代码目录分布分析

systemd的代码目录结构如下：

- `src`: 这是systemd的主要源代码目录，包含了核心的系统服务和功能模块。
  - `basic`: 包含一些基本的系统服务和功能模块，如时间同步、控制台设置等。
  - `boot`: 包含启动相关的代码，包括启动过程的处理和初始化。
  - `core`: 包含systemd的核心功能模块，如单位管理、进程管理、日志管理等。
  - `journal`: 包含systemd的日志管理模块，用于记录和管理系统日志。
  - `login`: 包含登录和用户会话管理相关的代码。
  - `network`: 包含网络管理相关的代码，如网络接口管理、DHCP等。
  - `resolved`: 包含DNS解析相关的代码，用于提供本地DNS解析服务。
  - `shared`: 包含一些共享的工具函数和数据结构。
  - `sysvcompat`: 提供对SysV兼容性的支持，用于处理SysV风格的初始化脚本。
  - `system`: 包含systemd本身的初始化和管理代码。
  - `timedate`: 包含时间和日期管理相关的代码。
  - `udev`: 包含udev设备管理相关的代码。
- `units`: 这是systemd的单位文件目录，包含了各种单位文件，如服务单位文件、套接字单位文件、定时器单位文件等。
- `test`: 包含了systemd的测试代码，用于测试系统服务和功能模块的正确性。
- `man`: 包含systemd的文档和手册页。
- `po`: 包含国际化相关的翻译文件。
- `tools`: 包含一些辅助工具和脚本。

这只是systemd代码目录的主要部分，还有一些其他的子目录和文件用于支持不同的功能和组件。整体而言，systemd的代码目录结构设计清晰，模块化程度高，每个目录都承担着特定的功能和责任，使得代码组织和维护更加方便。

# slice切片的用途

`systemd[1]: Created slice Slice /system/modprobe.` 是 systemd 启动时的一条日志信息，表示创建了一个名为 "Slice /system/modprobe" 的切片（slice）。

在 systemd 中，切片是一种用于组织和管理系统资源的单元。

**切片可以将一组相关的进程、服务或其他资源分组在一起，并提供资源管理和控制。**

切片的创建可以根据需要进行，以便更好地管理系统的资源分配和调度。

这条日志消息表明 systemd 在启动过程中创建了一个名为 "Slice /system/modprobe" 的切片。

根据名称可以推测，该切片可能用于管理与模块加载相关的进程或资源。具体的切片功能和用途可能会根据系统的配置和需求而有所不同。

切片是 systemd 的一个重要概念，它可以帮助管理员更好地组织和管理系统资源，实现资源隔离、优先级控制和任务调度等功能。通过切片，systemd 可以更加灵活和高效地管理系统的进程和服务。

# systemd启动流程分析

## systemd启动过程

systemd启动时会默认启动default.target配置，

并且**递归的处理它的依赖关系，**

一般这个配置为graphical.target 或者 multi-user.target。

第一种会启动图形界面，第二种会启动多用户字符模式。

下图是关键服务配置的启动依赖：

![systemd](/_posts/images/random_name/20200819122112468.png)



下面将简单介绍启动中的4个关键步骤：

### 第一步

systemd 执行默认target 配置，

配置文件/etc/systemd/system/default.target，

它一般是一个软链接，

指向multi-user.target或者graphical.target。

可以通过如下命令查询和修改default.target:

```
systemctl get-default #查询
systemctl set-default multi-user.target #设置
```

### 第二步

==systemd 执行启动所依赖的目标basic.target和sysinit.target初始化系统==

通过查看cat /etc/systemd/system/default.target查看依赖：

```
  8 [Unit]
  9 Description=Multi-User System
 10 Documentation=man:systemd.special(7)
 11 Requires=basic.target
 12 Conflicts=rescue.service rescue.target
 13 After=basic.target rescue.service rescue.target
 14 AllowIsolate=yes
```


After指定的target需要在default.target之前运行。

### 第三步

systemd 启动multi-user.target 下的本机与服务器服务，

由于default.target指向multi-user.target，

那么这一步就启动对应的target服务。

它的服务存在于 /etc/systemd/system/multi-user.target.wants 目录中：

```
lrwxrwxrwx. 1 root root 37 Aug  8  2018 acpid.service -> /usr/lib/systemd/system/acpid.service
lrwxrwxrwx. 1 root root 35 Aug  8  2018 atd.service -> /usr/lib/systemd/system/atd.service
lrwxrwxrwx. 1 root root 38 Aug  8  2018 auditd.service -> /usr/lib/systemd/system/auditd.service
lrwxrwxrwx. 1 root root 37 Aug  8  2018 crond.service -> /usr/lib/systemd/system/crond.service
lrwxrwxrwx. 1 root root 37 Aug  8  2018 kdump.service -> /usr/lib/systemd/system/kdump.service
lrwxrwxrwx. 1 root root 46 Aug  8  2018 libstoragemgmt.service -> /usr/lib/systemd/system/libstoragemgmt.service
lrwxrwxrwx  1 root root 36 Aug 13  2018 ntpd.service -> /usr/lib/systemd/system/ntpd.service
lrwxrwxrwx. 1 root root 39 Aug  8  2018 postfix.service -> /usr/lib/systemd/system/postfix.service
lrwxrwxrwx. 1 root root 40 Aug  8  2018 remote-fs.target -> /usr/lib/systemd/system/remote-fs.target
lrwxrwxrwx. 1 root root 46 Aug  8  2018 rhel-configure.service -> /usr/lib/systemd/system/rhel-configure.service
lrwxrwxrwx. 1 root root 39 Aug  8  2018 rpcbind.service -> /usr/lib/systemd/system/rpcbind.service
lrwxrwxrwx. 1 root root 39 Aug  8  2018 rsyslog.service -> /usr/lib/systemd/system/rsyslog.service
lrwxrwxrwx. 1 root root 36 Aug  8  2018 sshd.service -> /usr/lib/systemd/system/sshd.service
lrwxrwxrwx. 1 root root 37 Aug  8  2018 tuned.service -> /usr/lib/systemd/system/tuned.service
lrwxrwxrwx. 1 root root 35 Aug  8  2018 vdo.service -> /usr/lib/systemd/system/vdo.service

```

但是我的buildroot qemu vexpress的只有2个文件：

```
# ls -lh
total 0      
lrwxrwxrwx    1 root     root          40 May 30 10:15 remote-fs.target -> /usr/lib/systemd/system/remote-fs.target
lrwxrwxrwx    1 root     root          48 May 30 10:15 systemd-networkd.service -> /usr/lib/systemd/system/systemd-networkd.service
# 
```

### 第四步

==systemd 执行multi-user.target 下的/etc/rc.d/rc.local。==

systemd是可以兼容systemv init中的rc.local配置的，

通过rc-local.service来实现兼容的，

systemd在启动的很早就会判断/etc/rc.local是否存在并且是可执行的，

**如果满足条件，**

**那么systemd会调用/usr/lib/systemd/system-generators/下面的小程序来把rc-local.service服务加入到default.target中来。**

这样在后面的执行时就会触发rc.local的运行：

```
[Unit]
Description=/etc/rc.d/rc.local Compatibility
ConditionFileIsExecutable=/etc/rc.d/rc.local
After=network.target

[Service]
Type=simple
ExecStart=/etc/rc.d/rc.local start
TimeoutStartSec=0
TimeoutStopSec=1
RemainAfterExit=yes
```



After指定的target需要在default.target之前运行。

## 参考资料

1、

https://blog.csdn.net/rikeyone/article/details/108097837



# /etc/systemd/system/default.target 不存在

如果 `/etc/systemd/system/default.target` 文件不存在，那么系统将使用默认的目标作为启动的目标。

在大多数 Linux 发行版中，这个默认目标通常是 `multi-user.target` 或 `graphical.target`。

`default.target` 是一个符号链接（symlink），它指向系统中要作为默认启动目标的目标单元文件。它的实际路径可能会因不同的发行版和配置而有所不同，但通常在 `/etc/systemd/system/default.target` 中。

**如果该文件不存在，**

**系统将使用预设的默认目标，**

**这通常在 `/lib/systemd/system` 目录中定义。**

例如，在许多系统中，`/lib/systemd/system/default.target` 是一个符号链接，指向 `/lib/systemd/system/multi-user.target` 或 `/lib/systemd/system/graphical.target`。

```
# ls default.target -lh
lrwxrwxrwx    1 root     root          17 May 30 10:01 default.target -> multi-user.target
```



要确定系统的默认目标是哪个，可以使用以下命令：

```shell
systemctl get-default
```

该命令将输出当前系统的默认目标。你还可以使用以下命令来查看可用的目标单元列表：

```shell
systemctl list-units --type=target
```

这将列出系统中定义的所有目标单元，包括默认目标和其他可用的目标单元。



# basic.target

`basic.target` 是 Systemd 中的一个基本目标单元，它是其他目标单元的父目标。它定义了系统启动的基本要求和基础设施。

当 Systemd 启动时，它会首先尝试达到 `basic.target`，以确保系统的基本要求得到满足。`basic.target` 的完成意味着系统已经完成了一些基本的初始化步骤，并准备好启动其他目标单元。

`basic.target` 主要包含以下方面的功能：

1. 文件系统挂载：确保必需的文件系统已被挂载，包括根文件系统和其他重要的文件系统。

2. 资源管理：初始化系统资源管理器，并确保系统资源（如内存、CPU 等）的基本配置和管理。

3. 日志系统：启动系统日志服务，以便记录系统启动过程和运行时的日志信息。

4. 时间同步：启动时间同步服务，确保系统时间与外部时间源保持同步。

5. 虚拟文件系统：挂载虚拟文件系统（如`/proc`、`/sys` 等）以提供系统状态和信息。

通过达到 `basic.target`，Systemd 确保系统的基础环境已经准备就绪，可以继续启动其他目标单元，完成系统的初始化和启动过程。

你可以使用以下命令来检查系统中是否存在 `basic.target` 目标单元：

```shell
systemctl status basic.target
```

该命令将显示 `basic.target` 目标单元的状态信息，包括它的依赖关系和已加载的单元列表。



```
● basic.target - Basic System
     Loaded: loaded (/usr/lib/systemd/system/basic.target; static)
     Active: active since Wed 2023-05-31 02:12:26 UTC; 22min ago
      Until: Wed 2023-05-31 02:12:26 UTC; 22min ago
       Docs: man:systemd.special(7)

May 31 02:12:26 buildroot systemd[1]: Reached target Basic System.
```

# 查看default.target的依赖关系

systemctl list-dependencies default.target > 1.txt

```
default.target
● ├─dbus.service
● ├─systemd-ask-password-wall.path
● ├─systemd-networkd.service
● ├─basic.target
● │ ├─-.mount
● │ ├─tmp.mount
● │ ├─paths.target
● │ ├─slices.target
● │ │ ├─-.slice
● │ │ └─system.slice
● │ ├─sockets.target
● │ │ ├─dbus.socket
○ │ │ ├─systemd-journald-audit.socket
● │ │ ├─systemd-journald-dev-log.socket
● │ │ ├─systemd-journald.socket
● │ │ ├─systemd-networkd.socket
● │ │ ├─systemd-udevd-control.socket
● │ │ └─systemd-udevd-kernel.socket
● │ ├─sysinit.target
○ │ │ ├─dev-hugepages.mount
○ │ │ ├─dev-mqueue.mount
○ │ │ ├─kmod-static-nodes.service
○ │ │ ├─sys-fs-fuse-connections.mount
○ │ │ ├─sys-kernel-config.mount
○ │ │ ├─sys-kernel-debug.mount
● │ │ ├─sys-kernel-tracing.mount
● │ │ ├─systemd-ask-password-console.path
● │ │ ├─systemd-journal-flush.service
● │ │ ├─systemd-journald.service
○ │ │ ├─systemd-machine-id-commit.service
○ │ │ ├─systemd-modules-load.service
● │ │ ├─systemd-network-generator.service
○ │ │ ├─systemd-pstore.service
● │ │ ├─systemd-resolved.service
● │ │ ├─systemd-sysctl.service
● │ │ ├─systemd-timesyncd.service
● │ │ ├─systemd-tmpfiles-setup-dev.service
● │ │ ├─systemd-tmpfiles-setup.service
● │ │ ├─systemd-udev-trigger.service
● │ │ ├─systemd-udevd.service
○ │ │ ├─systemd-update-done.service
● │ │ ├─local-fs.target
● │ │ │ ├─-.mount
● │ │ │ ├─systemd-fsck-root.service
● │ │ │ ├─systemd-remount-fs.service
● │ │ │ └─tmp.mount
● │ │ └─swap.target
● │ └─timers.target
● │   └─systemd-tmpfiles-clean.timer
● ├─getty.target
● │ └─serial-getty@ttyAMA0.service
● └─remote-fs.target
```

## dbus.service什么时候启动

`dbus.service` 是由 systemd 管理的 D-Bus 服务的单元。它负责启动 D-Bus 守护进程，以便其他应用程序可以通过 D-Bus 进行进程间通信。

在大多数 Linux 发行版中，`dbus.service` 通常在系统引导过程中由 systemd 启动。具体来说，它是作为系统的默认目标（target）之一的 `multi-user.target` 的一个依赖项。当系统切换到 `multi-user.target` 时，systemd 会启动 `dbus.service`，以确保 D-Bus 守护进程正常运行。

需要注意的是，具体的启动顺序和依赖关系可能因不同的发行版和系统配置而有所不同。但通常情况下，`dbus.service` 在系统启动时会尽早启动，以确保其他依赖于 D-Bus 的服务和应用程序能够正常工作。



```
# cd multi-user.target.wants/
# ls
dbus.service                    systemd-ask-password-wall.path
getty.target
```

## systemd-ask-password-wall.path

`systemd-ask-password-wall.path` 是一个 systemd 的路径单元，用于触发密码请求的墙面（wall）通知。

在 systemd 中，密码请求通常用于需要用户输入密码或密钥才能继续进行的操作，例如解密加密的磁盘或文件系统、网络身份验证等。`systemd-ask-password-wall.path` 用于监视特定文件或目录的创建，并在文件或目录创建时触发密码请求的墙面通知。

具体来说，当 `systemd-ask-password-wall.path` 监测到指定的文件或目录被创建时，它会自动触发 `systemd-ask-password-wall.service` 服务单元。这个服务单元会在系统的控制台或图形界面上显示一个密码请求的墙面通知，要求用户输入密码或密钥。一旦用户提供了正确的密码或密钥，后续的操作将继续进行。

使用 `systemd-ask-password-wall.path` 和 `systemd-ask-password-wall.service` 可以实现在需要用户输入密码的场景下，以墙面通知的方式向用户请求密码，并在密码输入正确后继续操作。这对于自动化脚本或系统初始化过程中需要交互的操作非常有用。



# systemd的path unit的作用是什么

在 systemd 中，Path Unit（路径单元）用于监视文件或目录的状态变化，并在特定事件发生时触发相关的 systemd 服务单元。Path Unit 是 systemd 提供的一种事件驱动机制，**用于根据文件系统的变化来触发相应的操作。**

Path Unit 的作用是监视指定的文件或目录，当文件或目录的状态发生变化时，比如创建、修改、删除等操作，Path Unit 将相应地触发关联的服务单元。这样可以实现根据文件系统的变化来自动启动、停止或重新加载服务，从而实现一些自动化的操作。

例如，可以使用 Path Unit 监视一个目录，当目录中有新文件创建时，触发相应的服务单元来处理这些文件。或者可以使用 Path Unit 监视一个特定的文件，当文件内容发生变化时，触发服务单元执行相应的操作。

Path Unit 在 systemd 中常用于实现监控、自动化和事件驱动的场景。它提供了一种灵活的机制，可以根据文件或目录的状态变化来触发服务的启动、停止或其他操作，帮助管理和控制系统的行为。

# blockdev@.target 名字里的@什么意思

在 systemd 中，名字中带有 @ 符号的单元是一种特殊类型的单元，称为实例化单元（instantiated unit）。

实例化单元允许在一个单元定义的基础上创建多个具体的实例。@ 符号后面的部分被视为实例名称，并用于区分不同的实例。

对于 blockdev@.target，@ 符号表示实例化的参数。该单元可以用于创建多个 blockdev 实例，每个实例具有不同的名称。这种实例化机制使得可以根据实际需求来创建和管理不同的 blockdev 实例。

例如，可以创建多个具有不同名称的 blockdev 实例，如 blockdev@dev1.target、blockdev@dev2.target 等等。每个实例可以有自己的配置和依赖关系，以满足特定的需求。

实例化单元在 systemd 中广泛用于动态创建和管理多个相似的单元，提供了更灵活和可扩展的配置选项。

# systemctl list-dependencies输出内容的实心圆点和空心圆点的区别

在 `systemctl list-dependencies` 命令的输出中，实心圆点和空心圆点用于表示单元之间的依赖关系。

- 实心圆点（●）表示硬性依赖关系。如果一个单元的依赖关系是实心圆点，那么它是必需的依赖关系，意味着该单元必须在其依赖的单元启动之后才能启动。

- 空心圆点（○）表示软性依赖关系。如果一个单元的依赖关系是空心圆点，那么它是可选的依赖关系，意味着该单元可以在其依赖的单元启动之前或之后启动。

通过这种方式，您可以在依赖关系图中清楚地看到哪些依赖是必需的，哪些是可选的。这有助于理解和分析单元之间的启动顺序和依赖关系。

# emergency.target

`emergency.target` 是 systemd 中的一个特殊目标单元（target unit），用于系统的紧急模式（emergency mode）。当系统遇到严重问题无法正常启动时，可以进入紧急模式以进行故障排查和修复。

在 `emergency.target` 中，系统只会启动最基本的服务和进程，以提供一个最小化的运行环境。它不会启动多用户模式下的服务，而是专注于提供最小限度的功能来进行故障排查和修复。

进入紧急模式的方式可以是在启动时指定 `emergency` 参数，或者通过系统管理员手动切换到该目标。在紧急模式下，系统可能会提供一些基本的命令行工具和服务，以便进行故障诊断、文件系统修复、备份操作等。

需要注意的是，`emergency.target` 是一个静态目标单元，它没有任何依赖关系，也不会触发其他目标单元的启动。它专注于提供一个最小化的运行环境，以便进行系统修复和故障排查。

# systemctl status内容分析

```
# cat 1.txt 
● buildroot
    State: running
    Units: 149 loaded (incl. loaded aliases)
     Jobs: 0 queued
   Failed: 0 units
    Since: Wed 2023-05-31 02:12:06 UTC; 1h 20min ago
  systemd: 252
   CGroup: /
           ├─init.scope
           │ └─1 /sbin/init
           └─system.slice
             ├─dbus.service
             │ └─106 /usr/bin/dbus-daemon --system --address=systemd: --nofork --nopidfile --systemd-activation --syslog-only
             ├─system-serial\x2dgetty.slice
             │ └─serial-getty@ttyAMA0.service
             │   ├─107 -sh
             │   └─194 systemctl status
             ├─systemd-journald.service
             │ └─70 /usr/lib/systemd/systemd-journald
             ├─systemd-networkd.service
             │ └─86 /usr/lib/systemd/systemd-networkd
             ├─systemd-resolved.service
             │ └─87 /usr/lib/systemd/systemd-resolved
             ├─systemd-timesyncd.service
             │ └─88 /usr/lib/systemd/systemd-timesyncd
             └─systemd-udevd.service
               └─udev
                 └─81 /usr/lib/systemd/systemd-udevd
```

# 单独system命令的输出分析

即使是buildroot的qemu的输出，也太多了。

等价于systemctl list-units

```

```

systemctl --failed

查看失败的。我当前的



# 查看所有的unit file

systemctl list-unit-files

```
UNIT FILE                              STATE           PRESET
-.mount                                generated       -
dev-hugepages.mount                    static          -
dev-mqueue.mount                       static          -
sys-fs-fuse-connections.mount          static          -
sys-kernel-config.mount                static          -
sys-kernel-debug.mount                 static          -
sys-kernel-tracing.mount               static          -
tmp.mount                              static          -
systemd-ask-password-console.path      static          -
systemd-ask-password-wall.path         static          -
autovt@.service                        alias           -
console-getty.service                  disabled        disabled
container-getty@.service               static          -
dbus-org.freedesktop.hostname1.service alias           -
dbus-org.freedesktop.network1.service  alias           -
dbus-org.freedesktop.resolve1.service  alias           -
dbus-org.freedesktop.timedate1.service alias           -
dbus-org.freedesktop.timesync1.service alias           -
dbus.service                           static          -
debug-shell.service                    disabled        disabled
emergency.service                      static          -
getty@.service                         disabled        enabled
kmod-static-nodes.service              static          -
modprobe@.service                      static          -
rescue.service                         static          -
serial-getty@.service                  enabled         enabled
system-update-cleanup.service          static          -
systemd-ask-password-console.service   static          -
systemd-ask-password-wall.service      static          -
systemd-boot-check-no-failures.service disabled        disabled
systemd-exit.service                   static          -
systemd-fsck-root.service              enabled-runtime enabled
systemd-fsck@.service                  static          -
systemd-halt.service                   static          -
systemd-hostnamed.service              static          -
systemd-journal-flush.service          static          -
systemd-journald.service               static          -
systemd-journald@.service              static          -
systemd-kexec.service                  static          -
systemd-machine-id-commit.service      static          -
systemd-modules-load.service           static          -
systemd-network-generator.service      enabled         enabled
systemd-networkd-wait-online.service   enabled         disabled
systemd-networkd-wait-online@.service  disabled        enabled
systemd-networkd.service               enabled         enabled
systemd-nspawn@.service                disabled        enabled
systemd-poweroff.service               static          -
systemd-pstore.service                 enabled         enabled
systemd-reboot.service                 static          -
systemd-remount-fs.service             enabled-runtime enabled
systemd-resolved.service               enabled         enabled
systemd-suspend.service                static          -
systemd-sysctl.service                 static          -
systemd-time-wait-sync.service         disabled        disabled
systemd-timedated.service              static          -
systemd-timesyncd.service              enabled         enabled
systemd-tmpfiles-clean.service         static          -
systemd-tmpfiles-setup-dev.service     static          -
systemd-tmpfiles-setup.service         static          -
systemd-udev-settle.service            static          -
systemd-udev-trigger.service           static          -
systemd-udevd.service                  static          -
systemd-update-done.service            static          -
systemd-vconsole-setup.service         static          -
user-runtime-dir@.service              static          -
user@.service                          static          -
user.slice                             static          -
dbus.socket                            static          -
syslog.socket                          static          -
systemd-journald-audit.socket          static          -
systemd-journald-dev-log.socket        static          -
systemd-journald-varlink@.socket       static          -
systemd-journald.socket                static          -
systemd-journald@.socket               static          -
systemd-networkd.socket                enabled         enabled
systemd-udevd-control.socket           static          -
systemd-udevd-kernel.socket            static          -
basic.target                           static          -
blockdev@.target                       static          -
bluetooth.target                       static          -
boot-complete.target                   static          -
ctrl-alt-del.target                    alias           -
default.target                         alias           -
emergency.target                       static          -
exit.target                            disabled        disabled
factory-reset.target                   static          -
final.target                           static          -
first-boot-complete.target             static          -
getty-pre.target                       static          -
getty.target                           static          -
graphical.target                       static          -
halt.target                            disabled        disabled
kexec.target                           disabled        disabled
local-fs-pre.target                    static          -
local-fs.target                        static          -
multi-user.target                      static          -
network-online.target                  static          -
network-pre.target                     static          -
network.target                         static          -
nss-lookup.target                      static          -
nss-user-lookup.target                 static          -
paths.target                           static          -
poweroff.target                        disabled        disabled
printer.target                         static          -
reboot.target                          enabled         enabled
remote-fs-pre.target                   static          -
remote-fs.target                       enabled         enabled
rescue.target                          static          -
rpcbind.target                         static          -
shutdown.target                        static          -
sigpwr.target                          static          -
sleep.target                           static          -
slices.target                          static          -
smartcard.target                       static          -
sockets.target                         static          -
sound.target                           static          -
suspend.target                         static          -
swap.target                            static          -
sysinit.target                         static          -
system-update-pre.target               static          -
system-update.target                   static          -
time-set.target                        static          -
time-sync.target                       static          -
timers.target                          static          -
umount.target                          static          -
usb-gadget.target                      static          -
systemd-tmpfiles-clean.timer           static          -

127 unit files listed.
```

# 编写unit文件

`systemd` [单元文件](https://www.freedesktop.org/software/systemd/man/systemd.unit.html)的语法来源于 XDG 桌面项配置文件`.desktop`文件，最初的源头则是Microsoft Windows的`.ini`文件。

单元文件可以从多个地方加载，`systemctl show —property=UnitPath` 可以按优先级从低到高显示加载目录：

- `/usr/lib/systemd/system/` ：软件包安装的单元
- `/etc/systemd/system/` ：系统管理员安装的单元
  **注意:**
- 当 `systemd` 运行在[用户模式](https://wiki.archlinux.org/index.php/Systemd/User#How_it_works)下时，使用的加载路径是完全不同的。
- systemd 单元名仅能包含 ASCII 字符，下划线和点号和有特殊意义的字符('@', '-')。其它字符需要用 C-style "\x2d" 替换。参阅 [systemd.unit(5)](https://jlk.fjfi.cvut.cz/arch/manpages/man/systemd.unit.5) 和 [systemd-escape(1)](https://jlk.fjfi.cvut.cz/arch/manpages/man/systemd-escape.1) 。

## 处理依赖关系

使用 systemd 时，可通过正确编写单元配置文件来解决其依赖关系。

典型的情况是，单元 `A` 要求单元 `B` 在 `A` 启动之前运行。

在此情况下，向单元 `A` 配置文件中的 `[Unit]` 段添加 `Requires=B` 和 `After=B` 即可。若此依赖关系是可选的，可添加 `Wants=B` 和 `After=B` 。

请注意 `Wants=` 和 `Requires=` 并不意味着 `After=` ，即如果 `After=` 选项没有制定，这两个单元将被并行启动。

**依赖关系通常被用在服务（service）而不是[目标（target）](https://www.bookstack.cn/read/systemd-zh/spilt.2.systemd.md#目标（target）)上。**

例如， `network.target` 一般会被某个配置网络接口的服务引入，所以，将自定义的单元排在该服务之后即可，因为 `network.target` 已经启动。

# 临时文件

`/usr/lib/tmpfiles.d/` 和 `/etc/tmpfiles.d/` 中的文件描述了 systemd-tmpfiles 如何创建、清理、删除临时文件和目录，这些文件和目录通常存放在 `/run` 和 `/tmp` 中。配置文件名称为 `/etc/tmpfiles.d/<program>.conf`。此处的配置能覆盖 `/usr/lib/tmpfiles.d/` 目录中的同名配置。



```
# cd /usr/lib/tmpfiles.d/
# ls
README                         systemd-network.conf
dbus.conf                      systemd-pstore.conf
etc.conf                       systemd-resolve.conf
home.conf                      systemd-tmp.conf
journal-nocow.conf             systemd.conf
legacy.conf                    tmp.conf
provision.conf                 var.conf
static-nodes-permissions.conf  x11.conf
```

# timers

这个是用来替代cron的作用的。

# 挂载

因为 systemd 也负责按 `/etc/fstab` 挂载目录。在系统启动和重新加载系统管理器时，[systemd-fstab-generator(8)](https://jlk.fjfi.cvut.cz/arch/manpages/man/systemd-fstab-generator.8) 会将 `/etc/fstab` 中的配置转化为 systemd 单元。

*systemd* 扩展了 [fstab](https://wiki.archlinux.org/index.php/Fstab) 的传统功能，提供了额外的挂载选项。例如可以确保一个挂载仅在网络已经连接时进行，或者仅当另外一个分区已挂载时再挂载。这些选项通常以 `x-systemd.` 开头，[systemd.mount(5)](https://jlk.fjfi.cvut.cz/arch/manpages/man/systemd.mount.5#FSTAB) 中包含了完整说明。

*automounting* 也是一个例子，可以在使用时，而不是启动时挂载分区，详情请参考 [fstab#Automount with systemd](https://wiki.archlinux.org/index.php/Fstab#Automount_with_systemd)。

## GPT 分区自动挂载

在 [GPT](https://wiki.archlinux.org/index.php/GPT) 分区磁盘系统上，[systemd-gpt-auto-generator(8)](https://jlk.fjfi.cvut.cz/arch/manpages/man/systemd-gpt-auto-generator.8) 会按照 [可探测分区规范](https://www.freedesktop.org/wiki/Specifications/DiscoverablePartitionsSpec/) 进行挂载。可以在 `fstab` 中忽略。

要禁用自动挂载，请修改分区的 [类型 GUID](https://en.wikipedia.org/wiki/GUID_Partition_Table#Partition_type_GUIDs) 或设置分区属性 63 位 "不自动挂载"，详情参考 [gdisk#Prevent GPT partition automounting](https://wiki.archlinux.org/index.php/Gdisk#Prevent_GPT_partition_automounting)。

# 服务器systemd操作实例



参考资料

1、

https://www.cnblogs.com/qinlulu/p/14671370.html

# systemd限制进程的资源消耗

创建一个 .service 文件，在该文件中指定需要限制资源的服务的配置信息。例如：

```bash
[Unit]
Description=My Service

[Service]
ExecStart=/usr/bin/my-service
CPUQuota=50%
MemoryLimit=256M
```

在上述示例中，CPUQuota 限制了该服务最多只能使用系统 CPU 的 50%，而 MemoryLimit 限制了该服务最多只能使用 256 MB 的内存。





https://zhuanlan.zhihu.com/p/609898948

# initrd阶段的systemd





![img](/_posts/images/random_name/1594211722595.png)

https://www.junmajinlong.com/linux/systemd/systemd_bootup/



# 源代码解读

## **systemd 的主要功能**

1. systemd 采用**并行**的启动方式，并提供按需启动的方式：systemd 在设计之初最关注两件事情：**更少的开始，更多的并行。**更少的开始，意味着在开机启动阶段，systemd 仅启动系统启动时必要的一些服务，更多其他的服务推迟启动，直到真正需要它的时候，例如优麒麟的蓝牙 bluetooth 与截图相关的服务，开机的时候系统不会用到它；优麒麟的 U 盘启动器相关的服务，可以等到接入 U 盘的时候再启动；如果系统未连接到网络，那那些需要用到网络的相关服务也可以无需启动，直到网络连通后的第一次连接再启动即可。更多的并行，意味着服务的启动不需要像 sysvinit 一样序列化启动，而是同时运行所有需要的服务，以便系统 cpu 资源利用的最大化，因此总的启动时间最小化，后面会介绍 systemd 是如何实现所有服务并行启动。
2. 采用 cgroup 跟踪管理进程的生命周期：cgroup 为控制组，是一个层级结构，类似与文件管理系统的结构。当一个进程创建了子进程，子进程会继承父进程的 cgroup，就好比子进程创建在父进程的目录下，当子进程又创建一个子进程时，这个子进程会继承上一个子进程的 cgroup，也就相当与继承了父进程的 cgroup，好比这个子进程创建在上一个子进程的目录下，也就在父进程的目录下，通过这一机制就可以把父进程与所有的子进程关联起来并进行跟踪，当停止父进程时，可以通过查询 cgroup 找到所有关联的子进程，从而确保干净的停止所有相关服务。
3. 启动挂载与自动挂载：在系统启动过程中，systemd 在初始化时会自身进行一些挂载，如/sys 目录与/run 目录的挂载，这些都是系统启动时至关重要的文件系统。systemd 还能实现动态挂载点的自动挂载，例如不需要经常使用的光盘、U 盘的挂载，只在这些设备接入时，systemd 启动相应的服务并对其进行临时的挂载以便访问其中的内容，当这些设备拔出时，这些挂载点将被取消以便节约资源。
4. 事务的依赖关系管理：系统有很多的服务存在依赖关系，例如麒麟软件商店需要等待网络服务的启动，lightdm 与 systemd 交互需要等待 D-Bus 的启动，大多数服务也需要等待 syslog 的完全启动与初始化。systemd 采用 Unit（配置单元）管理这些服务的依赖关系，维护一个事务的一致性，并保证所有的相关服务不会出现相互依赖而产生死锁的情况，后面会对 Unit 进行详细介绍。
5. 日志：systemd 自带 journalctl 命令来查看系统保存的所有日志信息，并且可以支持通过一些参数来对日志进行过滤，方便用户进行日志分析。
6. 其他：systemd 经过几代的更新，实现的功能已经十分的多了，甚至**有人觉得 systemd 管得太多了，导致一些服务都没有了存在的必要。**例如 systemd 添加了许多 systemctl 的命令，可以实现系统电源的管理；systemd 还添加了看门狗机制，其他守护进程需要定期 ping systemd 进程，否则会视为失败而重启它等等。详情可以去阅读设计师的博客 [http://0pointer.de/blog/projects。](https://link.zhihu.com/?target=https%3A//www.oschina.net/action/GoToLink%3Furl%3Dhttp%3A%2F%2F0pointer.de%2Fblog%2Fprojects%E3%80%82)



## systemd 如何实现服务的并行

systemd 的设计理念就是**希望让所有的服务并行的启动，以最大化利用硬件资源，提高启动的时间**。

但是我们知道服务之间存在依赖关系，

客户端需要等待服务端的启动才可以建立连接，

例如前面提到的，在优麒麟操作系统中，所有的服务都需要等待 syslog 服务的启动，那 systemd 是如何摆脱这同步和序列化过程的呢？

systemd 的设计师认为，

对于传统的守护进程，他们真正实际等待另一个守护进程提供的是套接字的准备，

需要的是一个文件系统的 socket 套接字描述符，

这是它们唯一等待的，因此是否可以设法让这些套接字描述符可以更早的创建用于连接，从而不用等待整个守护进程完整的启动？

答案是可以的。

在 C 语言中，一个进程启动另一个进程时，一般是执行系统调用 exec()，

<u>systemd 在调用 exec()来启动服务之前，</u>

<u>先创建与该服务关联的监听套接字并激活，</u>

然后在 exec()启动服务期间把套接字传递给它，

==因此在服务还在启动的时候，套接字就已经处于可用的状态。==

通过这一方式，systemd 可以*在第一步中为所有的服务创建套接字，*

然后第二步一次运行所有的服务，

如果一个服务需要依赖于另一个服务，

由于套接字已经准备好，服务之间可以直接进行连接并继续执行启动，

如果遇到了需要同步的请求，不得不等待阻塞的情况，那阻塞的也将只会是一个服务，并且只是一个服务的一个请求，不会影响其他服务的启动，由此实现服务之间不需要再进行序列化的启动。

Linux 内核提供了套接字缓冲区功能，帮助 systemd 实现了最大的并行化，

还是拿 syslog 服务来说，

优麒麟操作系统上大多数服务在启动初期都会先进行日志相关的初始化配置，

如果同时启动 syslog 服务与各种 syslog 的客户端服务，

由于 syslog 相关套接字在 systemd 执行 exec()启动 syslog 之前已经创建并准备好，

客户端可以直接连接到 syslog 的套接字上，

如果遇到 syslog 启动比较慢，客户端向 syslog 发送请求消息，syslog 还无法处理的情况，

通过内核 socket 缓冲区的机制，请求的消息将会传到 syslog 套接字的缓冲区之中，

只要缓冲区未满，客户端就不需要等待并继续往下执行；

一旦 syslog 服务完全启动，它就会使所有消息出列并处理他们；

当出现另一种情况，缓冲区已满，或者需要同步消息请求的情况，虽然这个时候客户端不得不阻塞等待，但是也只有一个客户端的一个请求被阻塞，并且直到服务端赶上并处理为止。

因此 systemd 先进行套接字的激活，然后开始服务的创建，使得所有的服务可以并行启动，依赖的管理也变得多余，至少可以说是次要的，

==因为从服务的角度看，==

==只要套接字是激活的，==

==另一个服务有没有启动都没有区别，==

这样一种方式也使得程序更加地健壮，因为不论服务可用或不可用，甚至是崩溃，套接字都处于可用的状态，不会让客户端注意到丢失连接。



## **systemd 执行单元--Unit 介绍**

Unit 是 systemd 管理服务与资源的基本单元，

可以简单理解为 systemd 启动后每次需要执行的服务，每次需要处理的资源，

==都被抽象为一个配置单元 Unit，保存在一个 Unit 文件里面。==

例如，当用户登录到优麒麟操作系统时，

systemd 会执行 systemd-login.service 这个 Unit 文件来启动 login 服务，

持续跟踪用户的会话、进程、空闲状态，**为用户分配一个 slice 单元；**

当用户执行睡眠操作时，

systemd 会执行 systemd-suspend.service 文件的 Unit，来启动 systemd-sleep 服务执行系统睡眠操作。

Unit 文件可以根据其后缀名分为12种不同的类型，

systemd 内部给这12种类型的 Unit 定义了不同的全局模板，

因此 systemd 的执行流程为：

首先找到对应的 Unit 文件，然后根据 Unit 文件的类型匹配对应的全局模板，再然后根据这个模板解析 Unit 文件，最后执行 Unit 文件里的操作。

接下来简单介绍一下12种 Unit 文件类型：

(1)service：这是最明显的单元类型，代表一个后台守护进程，可以启动、停止、重新启动、重新加载守护进程，是最常用的一类 Unit 文件。

(2)socket：这个单元在文件系统或互联网上封装了一个套接字。目前 systemd 支持流、数据报和顺序包类型的 AF_INET、AF_INET6、AF_UNIX 套接字。还支持经典的 FIFO 作为传输。每个套接字单元都有一个匹配的服务单元，相应的服务在第一个连接进入套接字时就会启动，例如：nscd.socket 在传入连接上启动 nscd.service。

(3)device：这个单元封装了 Linux 设备树中的一个设备。如果设备通过 udev 规则为此标记，它将在 systemd 中作为设备单元公开。使用 udev 设置的属性可用作配置源来设置设备单元的依赖关系。

(4)mount：这个单元封装了文件系统层次结构中的一个挂载点。systemd 监控所有挂载点，也可用于挂载或卸载挂载点。**systemd 会将/etc/fstab 中的条目都转换为挂载点，并在开机时处理。**

(5)automount：这个单元类型在文件系统层次结构中封装了一个自动挂载点。每个自动挂载单元都有一个匹配的挂载单元，当该自动挂载点被访问时，systemd 就会执行挂载点中定义的挂载行为。

(6)target：这种单元类型用于单元的逻辑分组：**它本身并不做任何事情，它只是引用其他单元，从而可以一起控制。**比如：想让系统进入图形化模式，需要运行许多服务和配置命令，这些操作都由一个个的配置单元表示，将所有这些配置单元组合为一个目标(target)，就表示需要将这些配置单元全部执行一遍以便进入目标所代表的系统运行状态。

(7)snapshot：类似于 target 单元，snapshot 本身实际上不做任何事情，它们的唯一目的是引用其他单元。快照可用于保存或回滚 init 系统的所有服务和单元的状态。比如允许用户临时进入特定状态，例如“紧急外壳”，终止当前服务，并提供一种简单的方法返回之前的状态。

(8)swap：和挂载配置单元类似，交换配置单元用来管理交换分区。用户可以使用交换配置单元来定义系统中的交换分区，可以让这些交换分区在启动时被激活。

(9)timer：定时器配置单元用来定时触发用户定义的服务操作，是一种基于定时器的服务激活，**这类配置单元取代了 atd、crond 等传统的定时服务。**

(10)path：这类配置单元用来监控指定目录或者文件的变化，根据变化触发其他配置单元服务的运行。

(11)scope：这个单元主要表示从 systemd 外部创建的进程。

(12)slice：此单元主要用于封装管理一组进程资源占用的控制组的 slice 单元，也就是主要用于 cgroup，它通过在 cgroup 中创建一个节点实现资源的控制，一般包含 scope 与 service 单元。

## 启动过程

通过前面的描述，我们可以把 systemd 分为两个阶段：

虚拟根文件系统阶段与实根文件系统阶段。

内核通过解压 initrd 文件得到虚拟根文件系统，

然后执行虚拟根文件系统下的 init 程序来启动 systemd，

systemd 作为内核的子进程在虚拟根文件系统下开始运行。

虚拟根文件下的 systemd 首先对目前的系统进行一些检查，

例如判断系统的运行状态是 user 态还是 system 态，

系统是正常的启动状态还是异常出错后的重启状态等等，

然后进行一些系统的初始化配置，

包括：

环境变量的配置、日志的相关配置等，

接着对一些关键的文件系统进行挂载，

主要包括 /proc、/sys、/dev、/var 这些基本的文件系统目录，

到这一步后，systemd 就开始为切换实根文件目录做准备，

保存一些已经配置的项目，并进行一些环境的适配之后，

==systemd 执行 setsid()系统调用脱离内核控制，==

==成为一个完全独立的父进程，==

**至此 systemd 的虚拟根文件系统阶段结束，systemd 进入到实根文件系统阶段。**

在实根文件系统阶段，

systemd 首先进行一些切换后的环境适配，

然后开启日志终端的功能，

并把系统启动时临时保存在内核中的日志提取出来，

整理后存放到相应的日志文件中，

下一步，systemd 开始进行一些系统能力的获取与系统相关的初始化与配置，

例如：

CPU 亲和力的获取、主机名的配置、系统 ID 的配置，

cgroup 控制器的挂载、回环网络的配置等，

完成以上的这些所有初始化工作后，

systemd 作为 PID 为 1 的守护进程，

开始了各个系统服务的创建与管理工作，

根据相应 Unit 配置单元文件执行相应的系统服务，

通过各个服务逐步完成系统的启动工作。

systemd 执行 Unit 的顺序大致可以分为

 sysinit.target->basic.target->default.target，

其中 sysinit.target 与 basic.target 

主要用来启动一些系统初始化相关的一些服务与执行一些开机启动早期的一些任务，

default.target 则指向不同的“运行级别”target 文件，

**如果是进入命令行模式则指向 multi-user.target 文件，**

如果是进入图形界面模式则指向 graphical.target 文件。

至此，systemd 开机启动阶段的工作完成。



在完成了 systemd 初始化阶段以后，

系统根据配置的运行级别，进入不同的登录界面，

下面主要从图形登录界面进行介绍。

在优麒麟操作系统中，

systemd 之后的启动流程主要如下：

systemd->lightdm->Xorg->lightdm-greeter->ukui-greeter->ukui-session，

在优麒麟的终端通过 pstree 命令可以看到如下两个进程树：



lightdm 是一个全新的、轻量的 Linux 桌面的桌面显示管理器，

它首先会拉起 Xorg，

Xorg 是一个显示的后台，负责屏幕的绘制，

然后 lightdm 还会拉起 lightdm-greeter，

lightdm-greeter 是 lightdm 的子进程，它会拉起 ukui-greeter 进程，

**ukui-greeter 是登录界面进程，**

因此 ukui-greeter 起来以后，

系统进入到登录界面，

当输入登录的用户名与密码，用户名与密码效验通过以后，

**lightdm 建立个人的 ukui-session 桌面窗口管理器进程，**

至此，终端登录阶段结束，系统完成启动。



## 参考资料

1、

https://zhuanlan.zhihu.com/p/419372683

2、

https://zhuanlan.zhihu.com/p/426438095

# systemd preset-all 

总的来说，这个就是根据preset文件配置，决定我们最后的镜像的文件系统里，哪些service需要enable，哪些需要被disable，好建立对应的软链接。



systemctl preset-all 会读取哪些配置文件

它会读取以下位置的配置文件来确定服务的启用状态：

1. 预设目录 (`/usr/lib/systemd/system-preset/`): 这个目录包含了 systemd 服务预设文件，其命名以 `.preset` 结尾。`systemctl preset-all` 会读取该目录下的预设文件，并根据其中的配置来设置服务的启用状态。
2. 安装位置的预设目录 (`/etc/systemd/system-preset/`): 这个目录用于系统管理员自定义的 systemd 服务预设文件。类似于上述的预设目录，`systemctl preset-all` 会读取该目录下的预设文件，并根据其中的配置来设置服务的启用状态。



buildroot编译的target目录下有这些：

```
./usr/lib/systemd/system-preset/80-buildroot.preset  空的。
./usr/lib/systemd/system-preset/81-buildroot-tty.preset 这个使能了console tty的。这个是mk里根据配置生成的。我去掉它。
./usr/lib/systemd/system-preset/90-systemd.preset   这个文件是systemd源代码目录下的。
./usr/lib/systemd/system-preset/50-wpa_supplicant.preset 来自于./buildroot/package/wpa_supplicant/50-wpa_supplicant.preset
./usr/lib/systemd/user-preset/90-systemd.preset 这个文件是systemd源代码目录下的。
```

90-systemd.preset

主要是这个里面有不少的内容：

```
enable remote-fs.target
enable remote-cryptsetup.target
enable machines.target

enable getty@.service
enable systemd-timesyncd.service
enable systemd-networkd.service
enable systemd-resolved.service

disable console-getty.service
disable debug-shell.service

disable halt.target
disable kexec.target
disable poweroff.target
enable reboot.target
disable rescue.target
disable exit.target

disable syslog.socket

disable systemd-journal-gatewayd.*
disable systemd-journal-remote.*
disable systemd-journal-upload.*

# Passive targets: always off by default, since they should only be pulled in
# by dependent units.

disable cryptsetup-pre.target
disable getty-pre.target
disable local-fs-pre.target
disable network.target
disable network-pre.target
disable nss-lookup.target
disable nss-user-lookup.target
disable remote-fs-pre.target
disable rpcbind.target
disable time-set.target
disable time-sync.target
```



`81-buildroot-tty.preset` 是一个 systemd 配置文件，用于配置 tty 的优先级顺序。

在 systemd 中，**`preset` 文件用于定义服务或单元的启用或禁用顺序**。`81-buildroot-tty.preset` 文件特定于 Buildroot 系统，并与终端设备（tty）相关。

该文件的目的是定义 Buildroot 系统中哪些 tty 设备应该启用或禁用。根据文件的名称，可以推断出该文件将影响 tty 设备的启用顺序，具体来说是第 81 个位置。

通常，`81-buildroot-tty.preset` 文件位于 systemd 配置目录下的 `/etc/systemd/system-preset/` 目录中。

**该文件中的每一行定义了一个 tty 设备及其对应的启用或禁用操作**。例如：

```
disable ttyAMA0
enable ttyS0
```

上述示例表示 `ttyAMA0` 设备将被禁用，而 `ttyS0` 设备将被启用。这决定了在系统启动时哪些 tty 设备将被启用或禁用。

**请注意，`81-buildroot-tty.preset` 文件是根据特定的 Buildroot 配置生成的，并且可以根据具体的 Buildroot 系统进行修改和自定义。文件中的内容可能因 Buildroot 版本和配置的不同而有所变化。**

## buildroot修改systemd的preset

要修改 Buildroot 中使用的 systemd 的 preset（启用/禁用）配置，可以按照以下步骤进行操作：

1. 进入 Buildroot 的根目录。

2. 打开 `board/<board_name>/overlay/etc/systemd/system-preset/` 目录。这个目录用于存放 systemd preset 文件的自定义配置。

3. 在 `systemd-preset` 目录下创建一个新的 `.preset` 文件，例如 `my-preset.preset`。请确保文件名后缀为 `.preset`。

4. 在 `.preset` 文件中添加 systemd 服务的配置。每个服务一行，使用 `enable` 或 `disable` 指令指定是否启用该服务。例如：

   ```
   enable dbus.service
   disable my-service.service
   ```

   这将启用 `dbus.service` 服务并禁用 `my-service.service` 服务。

5. 保存并关闭 `.preset` 文件。

6. 在 Buildroot 根目录执行 `make` 命令重新编译 Buildroot。

7. 在重新生成的根文件系统中，修改的 systemd preset 配置将生效。

通过以上步骤，你可以自定义 Buildroot 中使用的 systemd 的 preset 配置，以启用或禁用特定的 systemd 服务。

需要注意的是，确保 `.preset` 文件位于正确的路径下，并且文件名后缀为 `.preset`。另外，如果使用了多个 Buildroot 板级配置，则需要在相应的板级配置目录下创建 `.preset` 文件。

希望以上信息对你有所帮助！如果还有其他问题，请随时提问。

## machines.target

`machines.target` 是一个系统目标（target），用于表示系统中的物理和虚拟机器。

**它本身不包含具体的服务单元，**而是作为一个**占位符目标，**用于组织和控制与机器相关的服务单元。

由于 `machines.target` 是一个占位符目标，其具体内容取决于系统的配置和需求。

在一个典型的系统中，`machines.target` 可能包含以下类型的服务单元：

1. 与虚拟机管理相关的服务单元：这些单元可能是负责启动和管理虚拟机的服务，如 libvirt、QEMU、KVM 等。
2. 与容器管理相关的服务单元：这些单元可能是负责启动和管理容器的服务，如 Docker、Kubernetes 等。
3. 与云平台相关的服务单元：这些单元可能是与云平台集成的服务，如 OpenStack、AWS EC2 等。
4. 与物理机管理相关的服务单元：这些单元可能是与物理机硬件管理和监控相关的服务，如硬件监控、传感器驱动程序等。

具体来说，`machines.target` 的内容取决于系统中安装和配置的相关软件和服务。

它的作用是提供一个目标，用于组织和控制这些与机器相关的服务单元的启动顺序和依赖关系。

需要注意的是，以上仅是可能的示例，实际的 `machines.target` 内容可能因系统配置和需求而有所不同。

您可以通过查看系统中的服务单元文件和目标依赖关系来了解特定系统中 `machines.target` 的内容。



http://www.jinbuguo.com/systemd/systemd.preset.html

# systemd跟android初始化系统对比

以下是 Android 初始化系统与 systemd 的一些对比：

1. **目标：** Android 初始化系统旨在启动 Android 操作系统，并管理各个服务和应用程序的启动。而 systemd 是一个通用的初始化系统和服务管理器，用于管理 Linux 系统中的进程、服务和系统资源。

2. **配置方式：** Android 初始化系统使用 `init.rc` 和 `/init.<device>.rc` 配置文件进行初始化配置。这些配置文件使用自定义的语法和命令进行定义。而 systemd 使用单元文件（unit files）进行配置，使用更通用的语法，可以定义服务、挂载点、套接字等。

3. **启动顺序：** Android 初始化系统按照配置文件中定义的顺序启动服务和进程。而 systemd 使用依赖关系图（dependency graph）来确定启动顺序，可以并行启动具有相互依赖关系的单元。

4. **功能丰富性：** systemd 提供了丰富的功能和特性，例如启动和停止控制、进程监控、日志记录、定时任务、套接字激活等。它还提供了更灵活的服务管理和系统配置选项。相比之下，Android 初始化系统的功能相对较为简单，主要关注 Android 系统的初始化和服务启动。

5. **日志记录：** systemd 提供了强大的日志记录和日志查询功能，使用 systemd Journal 进行集中的日志管理。而 Android 初始化系统通常使用 Android 的日志系统，如 logcat，以记录和显示系统日志。

需要注意的是，Android 初始化系统和 systemd 是针对不同的操作系统和用途而设计的。Android 初始化系统专注于 Android 操作系统的启动和服务管理，而 systemd 则是一个更通用的初始化系统和服务管理器，用于管理 Linux 系统中的各个组件。两者在设计和实现上有很大的差异，因此在功能、配置和使用方式上也存在一些区别。

# 免去login

我是在buildroot下面使用systemd。

当前串口上提示要登录。

我想要关闭这个登录要求。

要在 systemd 中通过串口实现免去登录（无需用户名和密码直接登录），可以按照以下步骤进行配置：

1. 打开 `getty` 服务配置文件：使用文本编辑器打开 `getty` 服务的配置文件，路径为 `/etc/systemd/system/getty.target.wants/serial-getty@ttyS0.service`。请根据实际的串口设备名称进行调整，例如 `/etc/systemd/system/getty.target.wants/serial-getty@ttyUSB0.service`。

2. 修改 `getty` 服务配置：找到 `ExecStart` 行，注释掉该行以禁用登录程序，并添加一行 `ExecStart=-/sbin/agetty --autologin <username> --noclear %I $TERM`。将 `<username>` 替换为要自动登录的用户名。

   修改前：
   ```
   ExecStart=-/sbin/agetty -o '-p -- \\u' --keep-baud 115200,38400,9600 %I $TERM
   ```

   修改后：
   ```
   #ExecStart=-/sbin/agetty -o '-p -- \\u' --keep-baud 115200,38400,9600 %I $TERM
   ExecStart=-/sbin/agetty --autologin <username> --noclear %I $TERM
   ```

3. 保存配置文件并重启 systemd：保存修改后的配置文件，并重新启动 systemd 服务。

   ```
   sudo systemctl daemon-reload
   sudo systemctl restart serial-getty@ttyS0.service
   ```

在完成以上步骤后，系统将通过串口自动登录指定的用户名，无需提供用户名和密码。

请注意，这样的自动登录可能会带来安全风险，因为任何人都可以直接访问系统而无需用户名和密码。因此，在实际使用中，请谨慎考虑自动登录的使用，并确保只在受控环境中使用。

# buildroot里的systemd

## SYSTEMD_INSTALL_SERVICE_TTY





# systemd-getty-generator工作逻辑

systemd-getty-generator 是 systemd 中的一个生成器（generator），它负责动态生成和管理 getty 服务单元。

在启动过程中，systemd-getty-generator **根据系统中的终端设备以及相关的配置信息**，自动生成相应的 getty 服务单元。

以下是 systemd-getty-generator 的工作逻辑：

1. 设备扫描：systemd-getty-generator 首先扫描系统中的终端设备。**它检测已连接的串行端口（如 ttyS0）和虚拟控制台设备（如 tty1）等**。这些设备通常存储在 `/dev` 目录下。

2. 配置检查：对于每个检测到的终端设备，systemd-getty-generator 会检查 `/etc/systemd/system/getty.target.wants/` 目录下是否存在与设备对应的 getty 服务单元配置文件。这些配置文件的命名规则通常为 `getty@ttyX.service`，其中 `ttyX` 是设备名称。

3. 生成服务单元：**如果对应的配置文件不存在**，systemd-getty-generator **将根据默认模板生成一个 getty 服务单元**。该服务单元描述了如何启动和管理 getty 程序，**以及与特定终端设备的关联**。**默认模板通常包含 getty 程序的路径、命令行参数、启动条件等信息。**

4. 链接服务单元：生成的 getty 服务单元会链接到 `/etc/systemd/system/getty.target.wants/` 目录下，**使其成为 getty.target 的一个依赖项**。这样，在启动或切换到对应的终端设备时，**systemd 将自动启动关联的 getty 服务。**

5. 重新加载配置：如果有新的终端设备被检测到或配置发生了变化，systemd-getty-generator 会通知 systemd 重新加载配置，以确保更新后的 getty 服务单元生效。

总体而言，systemd-getty-generator 的作用是自动管理终端设备的 getty 服务单元，根据设备的检测情况和配置信息，生成并链接相应的服务单元，以提供终端登录功能。它简化了终端管理的配置过程，使终端设备的启动和管理更加自动化和可靠。



# getty.target.wants 目录的作用

`getty.target.wants` 目录是 systemd 中用于存放 getty 服务单元启动链接的目录。它的作用是确定在特定终端设备上启动哪些 getty 服务。

systemd 使用目标（target）作为单位来组织和管理服务单元。getty.target 是 systemd 中用于管理 getty 服务的目标单元，表示在控制台或终端设备上提供登录会话。

`getty.target.wants` 目录是一个符号链接目录，位于 `/etc/systemd/system` 目录下。它存放了一系列符号链接，每个链接对应一个终端设备的 getty 服务单元。这些符号链接的名称通常为 `getty@ttyX.service`，其中 `ttyX` 是具体的终端设备名。

通过将 getty 服务单元的符号链接放置在 `getty.target.wants` 目录中，systemd 在启动过程中会自动加载和启动这些服务单元。这样，当系统切换到对应的终端设备时，systemd 会自动启动关联的 getty 服务，以提供终端登录功能。

通过将符号链接放置在 `getty.target.wants` 目录中，可以方便地配置和管理需要在特定终端设备上启动的 getty 服务。当需要添加、删除或禁用某个终端设备的 getty 服务时，只需创建、删除或禁用相应的符号链接即可，而无需直接修改原始的 getty 服务单元文件。

总而言之，`getty.target.wants` 目录的作用是存放 getty 服务单元的启动链接，以确定在特定终端设备上启动哪些 getty 服务。它提供了方便的方式来配置和管理 getty 服务，使系统能够在需要时自动启动适当的 getty 服务以提供登录功能。



# buildroot-console.conf文件的作用

因为我看到这个文件的内容是：

```
[Install]
DefaultInstance=
```

这个的作用是什么？

在 `buildroot-console.conf` 文件中，`[Install]` 部分用于指定默认的实例（Instance）。在 systemd 中，服务单元可以有多个实例，通过实例可以在不同的环境或配置下运行相同的服务。

在 `[Install]` 部分中，`DefaultInstance=` 用于设置默认的实例。它指定了在没有明确指定实例时，应该使用的默认实例名称。

例如，如果 `DefaultInstance=tty1`，那么当没有指定具体的实例名称时，systemd 将使用 `tty1` 作为默认实例。

这个默认实例通常与终端设备的名称相关。

在启动过程中，systemd 会根据终端设备的名称和配置信息来确定要使用的实例。

请注意，`DefaultInstance=` 只适用于特定的服务单元（例如 getty 服务单元），

并且需要在对应的服务单元配置文件中进行设置。

在 `buildroot-console.conf` 文件中，`DefaultInstance=` 用于配置默认实例。

具体的配置取决于您的需求和系统配置。



```
# cat /usr/lib/systemd/system/serial-getty@.service.d/buildroot-console.conf
[Install]
DefaultInstance=ttyAMA0
```

# initrd.target

```
[Unit]
Description=Initrd Default Target
Documentation=man:systemd.special(7)
OnFailure=emergency.target
OnFailureJobMode=replace-irreversibly
ConditionPathExists=/etc/initrd-release
Requires=basic.target
Wants=initrd-root-fs.target initrd-root-device.target initrd-fs.target initrd-parse-etc.service
After=initrd-root-fs.target initrd-root-device.target initrd-fs.target basic.target rescue.service rescue.target
AllowIsolate=yes
```

# man 7 systemd.special

这部分描述的是特殊的systemd unit。

包括了：

```
basic.target, bluetooth.target, cryptsetup-pre.target, cryptsetup.target, ctrl-alt-del.target, default.target, emergency.target,
       exit.target, final.target, getty.target, getty-pre.target, graphical.target, halt.target, hibernate.target, hybrid-sleep.target,
       suspend-then-hibernate.target, initrd-fs.target, initrd-root-device.target, initrd-root-fs.target, kbrequest.target, kexec.target,
       local-fs-pre.target, local-fs.target, machines.target multi-user.target, network-online.target, network-pre.target, network.target,
       nss-lookup.target, nss-user-lookup.target, paths.target, poweroff.target, printer.target, reboot.target, remote-cryptsetup.target,
       remote-fs-pre.target, remote-fs.target, rescue.target, rpcbind.target, runlevel2.target, runlevel3.target, runlevel4.target,
       runlevel5.target, shutdown.target, sigpwr.target, sleep.target, slices.target, smartcard.target, sockets.target, sound.target,
       suspend.target, swap.target, sysinit.target, system-update.target, time-sync.target, timers.target, umount.target, -.slice,
       system.slice, user.slice, machine.slice, -.mount, dbus.service, dbus.socket, display-manager.service, init.scope, syslog.socket,
       system-update-cleanup.service
```

## basic.target

`basic.target` 是 systemd 的一个基本目标单元，它定义了在系统启动过程中必须启动的基本服务和任务。这些基本服务和任务是实现系统的最小功能所需的，通常包括底层的初始化、加载核心模块、挂载文件系统等。

## system/basic.target 和user/basic.target关系

`system/basic.target` 和 `user/basic.target` 是 systemd 中的两个基本目标单元，分别用于系统级别和用户级别的服务管理。

1. `system/basic.target`：它是 systemd 在系统级别的基本目标单元。它定义了系统启动过程中必须启动的基本服务和任务，用于实现系统的最小功能。这包括底层的初始化、加载核心模块、挂载文件系统等。在系统引导过程中，systemd 首先启动 `system/basic.target`，然后按照定义的依赖关系加载和执行其中的服务和任务。

2. `user/basic.target`：它是 systemd 在用户级别的基本目标单元。它定义了**用户登录后**必须启动的基本服务和任务。这些服务和任务通常与用户会话相关，如启动用户的窗口管理器、启动用户级别的服务等。当用户登录后，systemd 启动 `user/basic.target`，并根据定义的依赖关系加载和执行其中的服务和任务。

`system/basic.target` 和 `user/basic.target` 是独立的目标单元，分别管理系统级别和用户级别的服务。它们的内容和执行过程相互独立，不会相互影响。

需要注意的是，`user/basic.target` 只在启用了用户级别的 systemd 实例（user instance）时才有效。用户级别的 systemd 实例是在用户登录时启动的，用于管理用户级别的服务和进程。如果未启用用户级别的 systemd 实例，则 `user/basic.target` 不会被使用。

总结来说，`system/basic.target` 是 systemd 在系统级别的基本目标单元，用于定义系统启动过程中必须启动的基本服务和任务。`user/basic.target` 是 systemd 在用户级别的基本目标单元，用于定义用户登录后必须启动的基本服务和任务。它们独立管理系统级别和用户级别的服务，不会相互影响。

user/basic.target依赖这几个。

```
Wants=sockets.target timers.target paths.target
```

system/basic.target依赖这几个：

```
Wants=sockets.target timers.target paths.target slices.target
After=sysinit.target sockets.target paths.target slices.target tmp.mount
RequiresMountsFor=/var /var/tmp
Wants=tmp.mount
```

## sysinit.target 

`sysinit.target` 是 systemd 启动过程中的一个目标单元，它定义了系统初始化阶段必须启动的服务和任务。

这些服务和任务的目的是在系统引导过程中进行系统初始化操作，如加载驱动程序、设置系统时钟、初始化网络等。

完成 `sysinit.target` 单元的启动后，systemd 将继续启动其他目标单元，如 `basic.target`、`multi-user.target` 等，以实现系统的完整启动。

```
Wants=local-fs.target swap.target
After=local-fs.target swap.target emergency.service emergency.target
```

## tmp.mount

`tmp.mount` 是 systemd 的一个挂载单元（mount unit），它用于挂载临时文件系统（tmpfs）到 `/tmp` 目录。

在 Linux 系统中，`/tmp` 目录通常用于存储临时文件，如临时缓存、临时下载文件等。为了提高性能和安全性，许多系统会将 `/tmp` 目录挂载为临时文件系统，使用内存来存储临时文件，而不是直接写入硬盘。

`tmp.mount` 单元定义了如何挂载临时文件系统到 `/tmp` 目录。它包含了挂载的参数、依赖关系和执行顺序等信息。当系统启动时，systemd 会自动加载和启动 `tmp.mount` 单元，根据定义的配置将临时文件系统挂载到 `/tmp` 目录。

通过使用临时文件系统，可以提高文件的读写速度，减少对硬盘的访问，同时也可以增加安全性，因为在系统重启后，临时文件系统中的文件将被清空，不会留下潜在的敏感信息。

需要注意的是，`tmp.mount` 单元的具体配置可以根据发行版和系统配置而有所不同。在一些系统中，可能会使用其他名称的挂载单元来挂载临时文件系统。

总结来说，`tmp.mount` 是 systemd 的一个挂载单元，用于将临时文件系统挂载到 `/tmp` 目录。它提供了挂载的参数和配置，通过使用临时文件系统，可以提高性能和安全性。具体配置可能因发行版和系统配置的不同而有所变化。

```
ConditionPathIsSymbolicLink=!/tmp
DefaultDependencies=no
Conflicts=umount.target
Before=local-fs.target umount.target
After=swap.target

[Mount]
What=tmpfs
Where=/tmp
Type=tmpfs
Options=mode=1777,strictatime,nosuid,nodev
```

当设置 `DefaultDependencies=no` 时，表示该单元不应具有默认的依赖关系。换句话说，该单元将不会自动继承与其类型相关的默认依赖关系。这样可以让你更灵活地定义自己的依赖关系。

### unit文件里[Mount]的配置

在 systemd 单元文件中，`[Mount]` 部分用于配置文件系统挂载相关的选项。下面是一些常见的 `[Mount]` 配置选项：

- `What=`：指定要挂载的文件系统的设备或路径。可以是设备节点（如 `/dev/sdb1`）、UUID（如 `UUID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`）或路径（如 `/mnt/data`）。

- `Where=`：指定挂载点的路径，即将文件系统挂载到的目录。

- `Type=`：指定文件系统的类型，例如 `ext4`、`ntfs`、`vfat` 等。

- `Options=`：指定挂载的选项，例如读写权限 (`rw`)、只读权限 (`ro`)、访问权限 (`noexec`)、禁止同步写入 (`async`) 等。

- `ReadOnly=`：指定文件系统是否以只读模式挂载。可以设置为 `yes` 或 `no`。

- `ExecOptions=`：指定可执行文件的挂载选项，例如允许执行 (`exec`)、禁止执行 (`noexec`)。

- `User=`：指定允许哪些用户挂载文件系统。可以设置为用户名或用户组名。

- `Group=`：指定挂载文件系统时所属的用户组。

- `SloppyOptions=`：指定是否允许挂载选项的容错性。设置为 `yes` 可以忽略无效的选项而不引发错误。

- `TimeoutSec=`：指定挂载操作的超时时间，以秒为单位。

- `RequiredFor=`, `Requires=`, `WantedBy=`, `Conflicts=`, `Before=`, `After=` 等：用于定义与其他单元的依赖关系、顺序关系和冲突关系。

上述仅是 `[Mount]` 部分常用的配置选项，实际的配置取决于具体的需求和场景。可以根据实际情况在单元文件中配置适当的选项，以定义文件系统挂载的行为和属性。

## local-fs.target

```
DefaultDependencies=no
Conflicts=shutdown.target
After=local-fs-pre.target
OnFailure=emergency.target
OnFailureJobMode=replace-irreversibly
```

`local-fs.target` 是 systemd 的一个目标单元，它是启动过程中文件系统相关单元的依赖目标。

在 systemd 启动过程中，`local-fs.target` 用于**控制文件系统的挂载和准备**。当系统启动时，包括根文件系统和其他本地文件系统（如 `/home`、`/var` 等）的挂载单元会依赖于 `local-fs.target`。

只有当 `local-fs.target` 完成之后，相关的文件系统挂载单元才会开始执行。

`local-fs.target` 的主要作用是确保在启动过程中的适当时机进行文件系统的挂载。**它提供了一个同步点**，以便在文件系统挂载之前进行必要的准备工作，如检查磁盘一致性、进行文件系统修复等。

此外，`local-fs.target` 也可以用作其他单元的依赖目标。通过将其他单元（如服务单元）的依赖关系指向 `local-fs.target`，可以确保在启动或激活这些单元之前，文件系统已经完成挂载和准备。

总之，`local-fs.target` 在 systemd 中扮演着协调文件系统挂载和准备的重要角色，确保在系统启动过程中的适当时机进行相关操作，并管理文件系统与其他单元之间的依赖关系。



OnFailure=emergency.target

当一个单元的执行失败，并且它配置了 `OnFailure=emergency.target`，系统会自动触发进入 `emergency.target`。这意味着当该单元失败时，系统将转入紧急模式，提供一个最小功能的环境来处理系统问题。



依赖的：

```
local-fs.target
● ├─-.mount
● ├─boot-efi.mount
● ├─home.mount
● ├─systemd-fsck-root.service
● └─systemd-remount-fs.service
```



### -.mount

`-.mount` 是 systemd 中的一个特殊挂载单元（mount unit），**用于表示根文件系统的挂载点。**

在 systemd 中，`-.mount` 是根文件系统的挂载点单元，它在系统引导过程中负责挂载根文件系统。这个挂载单元的名称是固定的，表示根文件系统的挂载点。

==`-.mount` 单元没有实际的配置文件，它是由 systemd 自动生成的。==它负责在系统引导时自动挂载根文件系统，并处理相关的依赖关系和挂载顺序。

挂载根文件系统是系统引导过程中的一个关键步骤，它是启动 Linux 操作系统所必需的。`-.mount` 单元确保在引导过程中正确地挂载根文件系统，并使其他依赖于根文件系统的单元能够正常启动。

需要注意的是，`-.mount` 单元是由 systemd 管理的，通常不需要手动操作或干预。在正常情况下，系统会自动处理根文件系统的挂载过程，并确保引导顺利进行。

## swap.target

对于嵌入式来说，这个是空的。

## system.slice

`system.slice` 是 systemd 中的一个切片（slice）单元，用于管理系统级别的进程组。

在 systemd 中，**切片是一种组织和管理进程的机制，它将相关的进程组织在一起并提供资源限制和控制。**

`system.slice` 切片是系统级别的切片，用于管理与系统相关的进程。

`system.slice` 切片包含了许多子切片和单元，

用于组织和管理不同类型的系统进程。

**它是 systemd 的一个默认切片，用于将系统级别的进程分类和隔离。**

通过将进程放置在适当的切片中，systemd 可以根据需要对进程进行资源管理、优先级控制和监控。

`system.slice` 切片为系统进程提供了一个统一的管理点，使系统管理员能够更好地了解和控制系统中运行的进程。

需要注意的是，`system.slice` 切片是**由 systemd 自动创建和管理的，通常不需要手动干预。**

它是 systemd 中进程管理的一部分，用于提供系统级别的进程控制和资源管理功能。

```
system.slice
● └─-.slice
```

### system.slice 构成

`system.slice` 是 systemd 中的一个切片（slice）单元，用于管理系统级别的进程组。它由一系列子切片和单元组成，用于组织和管理不同类型的系统进程。

以下是 `system.slice` 可能包含的一些子切片和单元：

1. `system.slice` 的子切片：`-.slice`、`user.slice`、`machine.slice` 等。这些子切片用于进一步组织和管理不同类型的进程。

2. 服务单元：`systemd.service` 类型的单元，表示系统级别的服务进程。例如，`systemd-logind.service`、`network.service` 等。

3. 套接字单元：`systemd.socket` 类型的单元，用于管理系统级别的套接字。例如，`systemd-journald.socket`、`dbus.socket` 等。

4. 设备单元：`systemd.device` 类型的单元，用于管理系统级别的设备。例如，`dev-hugepages.mount`、`dev-mqueue.mount` 等。

5. 虚拟文件系统单元：`systemd.automount` 类型的单元，用于自动挂载虚拟文件系统。例如，`proc-sys-fs-binfmt_misc.automount`。

6. 其他类型的单元：还可以包含其他类型的单元，如路径单元、定时器单元等，用于系统级别的进程管理和控制。

这些子切片和单元在 `system.slice` 中组织起来，构成了系统级别的进程组。它们共同协作，使系统管理员能够更好地管理和控制系统中运行的进程，并提供资源隔离和优先级控制的功能。

需要注意的是，`system.slice` 的具体构成可能会因不同的系统配置和运行环境而有所差异。具体的构成可以通过运行 `systemctl list-dependencies system.slice` 命令来查看系统上的实际情况。



buildroot下面的配置文件是system/user.slice。

```
Before=slices.target
```

slices.target的内容是：

```
Wants=-.slice system.slice
```

### -.slice

`-.slice` 是 systemd 中的一个特殊切片（slice），它是根切片（root slice）或称为根容器。它是整个 systemd 切片层次结构的顶级切片，用于组织和管理系统中的所有其他切片和单元。

根切片（`-.slice`）是一个虚拟切片，它没有对应的定义文件。它的作用是为其他切片和单元提供一个父容器。所有其他切片和单元都直接或间接地属于根切片。

在 systemd 的切片层次结构中，各个切片按层次关系组织在一起。根切片是最顶层的切片，下面是一些可能的子切片：

- `system.slice`: 系统级别的切片，用于管理系统级别的进程组。
- `user.slice`: 用户级别的切片，用于管理用户级别的进程组。
- `machine.slice`: 机器级别的切片，用于管理容器或虚拟机级别的进程组。

通过将各个切片组织在一起，systemd 可以对进程进行层次化管理和控制，提供资源隔离、优先级控制和监控的功能。

需要注意的是，`-.slice` 是一个系统级别的切片，对应的根容器。它是 systemd 切片层次结构中的顶级切片，没有对应的定义文件。它在 systemd 初始化过程中自动创建，无需手动干预。

## sockets.target

桌面系统：

```
sockets.target
● ├─acpid.socket
● ├─apport-forward.socket
● ├─avahi-daemon.socket
● ├─cups.socket
● ├─dbus.socket
● ├─dm-event.socket
● ├─docker.socket
● ├─rpcbind.socket
● ├─snapd.socket
● ├─systemd-initctl.socket
● ├─systemd-journald-audit.socket
● ├─systemd-journald-dev-log.socket
● ├─systemd-journald.socket
● ├─systemd-udevd-control.socket
● ├─systemd-udevd-kernel.socket
● └─uuidd.socket
```

buildroot：

```
sockets.target
● ├─dbus.socket
● ├─dm-event.socket
○ ├─systemd-journald-audit.socket
● ├─systemd-journald-dev-log.socket
● ├─systemd-journald.socket
● ├─systemd-networkd.socket
● ├─systemd-udevd-control.socket
● └─systemd-udevd-kernel.socket
```

### dbus.socket

这个也是有一个具体的文件的。

```
[Socket]
ListenStream=/var/run/dbus/system_bus_socket
```

查看依赖：

```
dbus.socket
● ├─-.mount
● ├─system.slice
● └─sysinit.target
●   ├─blk-availability.service
○   ├─dev-hugepages.mount
○   ├─dev-mqueue.mount
○   ├─kmod-static-nodes.service
●   ├─lvm2-monitor.service
○   ├─sys-fs-fuse-connections.mount
○   ├─sys-kernel-config.mount
○   ├─sys-kernel-debug.mount
●   ├─sys-kernel-tracing.mount
●   ├─systemd-ask-password-console.path
●   ├─systemd-journal-flush.service
●   ├─systemd-journald.service
○   ├─systemd-machine-id-commit.service
○   ├─systemd-modules-load.service
●   ├─systemd-network-generator.service
○   ├─systemd-pstore.service
●   ├─systemd-resolved.service
●   ├─systemd-sysctl.service
●   ├─systemd-timesyncd.service
●   ├─systemd-tmpfiles-setup-dev.service
●   ├─systemd-tmpfiles-setup.service
●   ├─systemd-udev-trigger.service
●   ├─systemd-udevd.service
●   ├─systemd-update-done.service
●   ├─local-fs.target
●   │ ├─-.mount
○   │ ├─systemd-fsck-root.service
●   │ ├─systemd-remount-fs.service
●   │ └─tmp.mount
●   └─swap.target
```

但是看对应的dbus.socket文件里，只有这样：

```
[Socket]
ListenStream=/var/run/dbus/system_bus_socket
```

## paths.target

在systemd中，`paths.target`是一种特殊的目标（target），用于指定文件路径相关的操作。它是systemd单元（unit）的一种类型，可以在系统引导过程中或在运行时对特定文件路径进行操作。

`paths.target`用于监视和触发文件路径的状态变化。当指定的路径存在或满足特定条件时，systemd将触发与该目标关联的其他单元。例如，您可以定义一个服务单元（service unit），当指定的路径出现变化时，启动该服务。

以下是一个`paths.target`单元的示例配置文件（位于`/etc/systemd/system/`目录下）：

```plaintext
[Unit]
Description=Monitor a file path
Documentation=man:path.unit(5)

[Path]
PathExists=/path/to/file
Unit=my-service.service

[Install]
WantedBy=multi-user.target
```

在这个示例中，当`/path/to/file`存在时，`my-service.service`将被启动。通过`[Install]`部分，您还可以定义该单元的启动级别（WantedBy）。

要使用`paths.target`，您需要将相关的配置文件放置在适当的systemd目录中（通常是`/etc/systemd/system/`）。然后使用`systemctl`命令启用和管理该单元。



# slice文件和target文件的关系

在 systemd 中，slice 文件和 target 文件都用于组织和管理系统中的单元。它们之间有一些相似之处，但也存在一些区别。

Slice 文件是用于组织和管理进程切片的单元。

一个 slice 文件定义了一组相关进程的组合，它们可以共享资源、限制资源使用和优先级，并以层次结构的方式进行组织。

slice 文件使用 `.slice` 后缀命名，如 `system.slice`、`user.slice` 等。

它们通常存储在 `/usr/lib/systemd/system/`、`/lib/systemd/system/` 或 `/etc/systemd/system/` 等路径下。

Target 文件用于定义一组需要同时启动或停止的单元。

**它们是一种特殊类型的 slice 文件，用于表示特定的系统状态或运行级别。**

target 文件使用 `.target` 后缀命名，如 `multi-user.target`、`graphical.target` 等。它们通常存储在 `/usr/lib/systemd/system/`、`/lib/systemd/system/` 或 `/etc/systemd/system/` 等路径下。

Slice 文件和 target 文件之间的关系是：

1. Slice 文件可以作为 target 文件的依赖。这意味着当一个 target 文件被启动或停止时，它所依赖的 slice 文件也会被相应地启动或停止。

2. **Target 文件可以包含多个 slice 文件作为其成员**。这意味着一个 target 文件可以同时启动或停止它所包含的多个 slice 文件中的进程。

3. Slice 文件和 target 文件都可以包含其他单元，如服务单元、套接字单元等，以便进行更细粒度的管理和控制。

总的来说，slice 文件用于组织和管理进程切片，而 target 文件用于定义系统状态或运行级别，并包含要同时启动或停止的单元。它们在 systemd 中扮演不同的角色，但可以相互关联和协作，以实现对系统资源和进程的有效管理。

## slices.target

```
[Unit]
Description=Slices
Documentation=man:systemd.special(7)
Wants=-.slice system.slice
After=-.slice system.slice
```



# systemd的默认依赖规则

systemd有一组默认的依赖规则，用于确定单元之间的启动顺序。这些默认规则可确保系统的核心组件按正确的顺序启动，并处理它们之间的依赖关系。以下是systemd的一些默认依赖规则：

1. `default.target`：默认目标是systemd启动过程中的初始目标，通常是multi-user.target。其他单元通常会依赖于该目标，以确保在启动时正确加载。

2. `basic.target`：基本目标是systemd启动过程中的第一个实际目标，它仅包含系统所需的最基本功能。其他更高级别的目标都依赖于它。

3. `sysinit.target`：系统初始化目标包含在系统引导期间启动的早期系统服务。其他单元在引导过程中可能依赖于这些服务。

4. `multi-user.target`：多用户目标是在引导过程中启动的大多数常规系统服务和用户会话。它是大多数服务器和桌面系统的默认目标。

5. `graphical.target`：图形目标是针对桌面环境的目标，通常依赖于multi-user.target。它包含启动图形界面和相关的服务。

这只是一小部分systemd的默认依赖规则，实际上还有更多目标和单元之间的依赖关系。依赖规则可以通过单元文件中的`Requires`、`Wants`、`After`等指令来自定义和修改。每个单元都可以在其配置文件中显式指定所依赖的其他单元、启动顺序以及其他属性。



# systemd-path

在桌面系统上看到的是这样：

```
temporary: /tmp
temporary-large: /var/tmp
system-binaries: /usr/bin
system-include: /usr/include
system-library-private: /usr/lib
system-library-arch: /usr/lib/x86_64-linux-gnu
system-shared: /usr/share
system-configuration-factory: /usr/share/factory/etc
system-state-factory: /usr/share/factory/var
system-configuration: /etc
system-runtime: /run
system-runtime-logs: /run/log
system-state-private: /var/lib
system-state-logs: /var/log
system-state-cache: /var/cache
system-state-spool: /var/spool
user-binaries: /home/amlogic/.local/bin
user-library-private: /home/amlogic/.local/lib
user-library-arch: /home/amlogic/.local/lib/x86_64-linux-gnu
user-shared: /home/amlogic/.local/share
user-configuration: /home/amlogic/.config
user-runtime: /run/user/1000
user-state-cache: /home/amlogic/.cache
user: /home/amlogic
user-documents: /home/amlogic/Documents
user-music: /home/amlogic/Music
user-pictures: /home/amlogic/Pictures
user-videos: /home/amlogic/Videos
user-download: /home/amlogic/Downloads
user-public: /home/amlogic/Public
user-templates: /home/amlogic/Templates
user-desktop: /home/amlogic/Desktop
search-binaries: /home/amlogic/.local/bin:/home/amlogic/.cargo/bin:/home/amlogic/tools/go/bin:/home/amlogic/.nvm/versions/node/v14.17.0/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/home/amlogic/tools/bitbake/bin:/home/amlogic/platform-tools
search-library-private: /home/amlogic/.local/lib:/usr/local/lib:/usr/lib:/lib
search-library-arch: /home/amlogic/.local/lib/x86_64-linux-gnu:/usr/lib/x86_64-linux-gnu:/lib/x86_64-linux-gnu
search-shared: /home/amlogic/.local/share:/usr/local/share:/usr/share:/var/lib/snapd/desktop
search-configuration-factory: /usr/local/share/factory/etc:/usr/share/factory/etc
search-state-factory: /usr/local/share/factory/var:/usr/share/factory/var
search-configuration: /home/amlogic/.config:/etc
```

# getty.target

qemu上

```
getty.target
● └─serial-getty@ttyAMA0.service
```

桌面系统：

```
getty.target
● ├─getty-static.service
● └─getty@tty1.service
```



在 systemd 中，有两个模板单元负责在文本控制台上显示登录提示：

1. `getty@.service`负责[虚拟终端](https://en.wikipedia.org/wiki/Virtual_console)(VT) 登录提示，即显示在`/dev/tty1`和类似设备中的 VGA 屏幕上的提示。
2. `serial-getty@.service`负责所有其他终端，包括`/dev/ttyS0`等串行端口。`它与getty@.service`在几个方面有所不同：除其他外，`$TERM`环境变量设置为 `vt102`（希望这是大多数串行终端的良好默认值）而不是`linux`（这仅是 VT 的正确选择），并且清除 VT 回滚缓冲区（并且仅适用于 VT）的特殊逻辑被跳过。



让我们仔细看看`getty@.service`是如何启动的，

即虚拟终端（即非串行 TTY）上的登录提示是如何工作的。

传统上，Linux 机器上的 init 系统被配置为在启动时产生固定数量的登录提示。

`在大多数情况下，在前六个 VT tty1`到`tty6`上产生了六个 getty 程序实例 。

在 systemd 世界中，我们使它更加动态：

**为了使事情更有效，登录提示现在仅按需启动。**

当您切换到 VT 时，getty 服务被实例化为 `getty@tty2.service`、`getty@tty5.service`等等。

由于我们不必再无条件地启动 getty 进程，这使我们可以节省一些资源，并使启动速度更快一些。

这种行为对用户来说基本上是透明的：

如果用户激活 VT，getty 会立即启动，因此用户几乎不会注意到它并非一直在运行。

如果他随后登录并键入`ps，`他会注意到 getty 实例仅针对他目前切换到的 VT 运行。

默认情况下，这种自动生成仅针对最高为 VT6 的 VT（以便接近 Linux 系统的传统默认配置）[1]。请注意，只有在没有其他子系统占有 VT 时才会尝试自动生成 getty。更具体地说，如果用户通过 GNOME 频繁使用[快速用户切换](https://en.wikipedia.org/wiki/Fast_user_switching)，他也会在前六个 VT 上获得他的 X 会话，因为为每个会话分配了最低的可用 VT。

两个 VT 由自动生成逻辑专门处理：首先 `tty1`得到特殊处理：如果我们启动到图形模式，显示管理器将占有这个 VT。如果我们启动到多用户（文本）模式，则会在其上启动一个 getty——无条件地，没有任何按需逻辑[2]。

其次，`tty6`是专门为自动生成的 getty 保留的，对 X [3]等其他子系统不可用。这样做是为了确保始终有办法获得文本登录，即使由于快速用户切换 X 拥有超过 5 个 VT。



串行终端（以及所有其他类型的非 VT 终端）上登录提示的处理与 VT 不同。

默认情况下，systemd 将在主内核[4]控制台上实例化一个`serial-getty@.service`，如果它不是虚拟终端的话。

`内核控制台是内核输出自己的日志消息的地方，通常通过诸如console=ttyS0 `[5]之类的参数在引导加载程序的内核命令行上进行配置。

这个逻辑确保当用户要求内核将其输出重定向到某个串行终端时，他也会在引导完成时自动获得登录提示[6]。systemd 还将在第一个特殊的 VM 控制台（即`/dev/hvc0`， `````/dev/xvc0`，`/dev/hvsi0`），如果系统在提供这些设备的 VM 中运行。 此逻辑在名为[systemd-getty-generator 的](http://www.freedesktop.org/software/systemd/man/systemd-getty-generator.html)[生成器](http://www.freedesktop.org/wiki/Software/systemd/Generators)中实现 ，该生成器在启动时早期运行，并根据执行环境引入必要的服务。

在许多情况下，这种自动逻辑应该已经足以让您在需要时获得登录提示，而无需对 systemd 进行任何特定配置。然而，有时需要手动配置串行 getty，例如，如果需要多个串行登录提示或内核控制台应重定向到与登录提示不同的终端。为了促进这一点，为每个你希望它在[7]上运行的串行端口实例化一次`serial-getty@.service`就足够了 ：

# 禁止agetty启动

如果在你的嵌入式系统中没有`/etc/systemd/logind.conf`文件，那么你可以尝试使用`/etc/systemd/system/`目录下的单元文件来禁用`agetty`服务。以下是一种方法：

1. 在`/etc/systemd/system/`目录中创建一个新的单元文件，例如`disable-getty.service`：
   ```
   sudo nano /etc/systemd/system/disable-getty.service
   ```

2. 在打开的文件中输入以下内容：
   ```
   [Unit]
   Description=Disable agetty service
   
   [Service]
   ExecStart=/bin/true
   RemainAfterExit=yes
   Type=oneshot
   
   [Install]
   WantedBy=multi-user.target
   ```

   这个单元文件将执行一个虚拟的命令 `/bin/true`，并将其设置为一次性服务。

3. 保存文件并关闭编辑器。

4. 重新加载systemd配置：
   ```
   sudo systemctl daemon-reload
   ```

5. 停用和禁用`agetty`服务：
   ```
   sudo systemctl stop getty@tty1.service
   sudo systemctl disable getty@tty1.service
   ```

   这将停止和禁用`agetty`服务在tty1上的运行。如果你想禁用其他终端上的`agetty`服务，可以相应地更改`tty1`为其他终端编号（例如`tty2`、`tty3`等）。

6. 重新启动systemd：
   ```
   sudo systemctl restart systemd
   ```

现在，`agetty`服务将被禁用并不会在对应的终端上运行。请记住，在禁用`agetty`服务后，你将无法通过终端登录进行交互式会话。这适用于一些特定的嵌入式系统场景，例如使用串口或网络远程访问进行系统管理。

请注意，以上步骤仅提供了一种禁用`agetty`服务的方法，具体的系统配置可能因嵌入式系统的不同而有所差异。确保在你的系统中使用适当的路径和命令。此外，禁用`agetty`服务可能会影响系统的其他功能和服务，因此在进行相关更改之前，请确保你了解其影响并备份重要数据。

# user-.slice.d

`user-.slice.d` 是systemd中的一个目录，用于配置和定制用户切片（user slice）。

在systemd中，用户切片是为每个用户会话创建的一个单独的切片单元，用于管理与该用户相关的进程和资源。用户切片提供了一种隔离和限制用户会话中的进程资源的机制，以确保用户会话的稳定和安全。

`user-.slice.d` 目录用于存放针对用户切片的配置和定制文件。在该目录下可以放置各种配置文件，以覆盖或修改默认的用户切片设置。这些配置文件可以包含切片属性、资源限制、进程控制参数等。

通过在 `user-.slice.d` 目录中放置配置文件，可以对特定用户切片应用自定义的设置，例如设置特定的资源限制、绑定特定的CPU、限制内存使用等。这样可以根据实际需求对用户切片进行个性化的调整。

需要注意的是，`user-.slice.d` 目录中的配置文件会覆盖默认的用户切片设置。因此，在修改或添加配置文件时，请确保了解其对用户切片行为的影响，并进行适当的测试和验证。

buildroot里的10-defaults.conf里来是这样：

```
[Unit]
Description=User Slice of UID %j
Documentation=man:user@.service(5)
After=systemd-user-sessions.service
StopWhenUnneeded=yes

[Slice]
TasksMax=33%
```

# systemd-sysv-generator

output\build\systemd-252.4\src\sysv-generator\sysv-generator.c

一旦 `systemd-sysv-generator` 完成检测和转换，它将创建对应的 systemd 服务单元文件，并放置在 `/run/systemd/generator/` 或 `/etc/systemd/system/` 目录中，具体取决于操作系统的配置。

## systemd-sysv-generator是在编译时执行还是运行时执行

`systemd-sysv-generator` 是在运行时执行的，而不是在编译时执行。

当 systemd 初始化系统时，它会启动 `systemd-sysv-generator` 进程，并由其负责检测和转换 SysV init 脚本为 systemd 单元。

这个过程是动态的，发生在系统启动期间。

`systemd-sysv-generator` 会扫描特定的目录，查找符合规则的 SysV init 脚本，并根据脚本的内容生成相应的 systemd 服务单元。

生成的 systemd 单元文件可以在 `/run/systemd/generator/` 或 `/etc/systemd/system/` 目录中找到，具体取决于系统的配置。

需要注意的是，`systemd-sysv-generator` 是作为 systemd 的一部分进行安装和配置的，因此它在 systemd 安装后会自动运行，无需手动操作。它会在每次系统启动时执行，以确保将 SysV init 脚本转换为 systemd 单元并进行正确的集成。



这个配置是通过 systemd 的相关配置文件进行指定的。在大多数 Linux 发行版中，systemd 的配置文件通常位于 `/etc/systemd/` 目录下。

具体来说，生成的 systemd 单元文件的存放位置由以下两个配置项控制：

1. `systemd-sysv-generator` 默认的生成目录可以通过修改 `/etc/systemd/system.conf` 配置文件中的 `RuntimeDirectory` 选项来调整。例如，你可以将其设置为 `/run/systemd/generator/`：
   
   ```
   RuntimeDirectory=generator
   ```
   这样生成的 systemd 单元文件将存放在 `/run/systemd/generator/` 目录中。
   
2. 如果你希望将生成的 systemd 单元文件保存到永久存储位置，可以通过修改 `/etc/systemd/system.conf` 配置文件中的 `UnitPath` 选项来指定。例如，你可以将其设置为 `/etc/systemd/system/`：
   ```
   UnitPath=/etc/systemd/system/
   ```
   这样生成的 systemd 单元文件将存放在 `/etc/systemd/system/` 目录中。

请注意，修改 systemd 的配置文件需要管理员权限。在修改后，你需要重新加载 systemd 的配置或重新启动系统，以使配置生效。

需要注意的是，具体的配置文件路径和配置项名称可能因 Linux 发行版的不同而略有差异。在某些情况下，你可能需要参考特定发行版的文档或查阅 systemd 的手册来获取准确的配置信息。



1. **RuntimeDirectory**: 指定运行时目录的路径，例如 `/run/systemd`。用于存放运行时生成的文件。
2. **UnitPath**: 指定单元文件的搜索路径，例如 `/etc/systemd/system`。这是用于存放静态单元文件的位置。



## 执行

```
systemctl enable --now systemd-sysv-generator
```

我在板端执行，报错：

```
Failed to enable unit: Unit file systemd-sysv-generator.service does not exist.
```



# modprobe.d/      modules-load.d/ 这2个目录是什么关系

`modprobe.d/` 和 `modules-load.d/` 是两个目录，用于配置内核模块的加载行为和规则，它们在 Linux 系统中具有不同的作用和关系。

1. `modprobe.d/` 目录：
   - 位于 `/etc/modprobe.d/` 路径下。
   - 用于配置 `modprobe` 命令的行为和规则。
   - `modprobe` 命令用于动态加载和卸载内核模块。
   - 在 `modprobe.d/` 目录中，你可以创建以 `.conf` 结尾的文件，其中每个文件包含一条 `modprobe` 命令的配置选项和参数。
   - 这些配置选项可以指定要加载的内核模块、加载时的参数和选项等。

2. `modules-load.d/` 目录：
   - 位于 `/etc/modules-load.d/` 路径下。
   - 用于配置 Systemd 的 `systemd-modules-load.service` 服务。
   - `systemd-modules-load.service` 服务负责在系统启动过程中加载所需的内核模块。
   - 在 `modules-load.d/` 目录中，你可以创建以 `.conf` 结尾的文件，其中每个文件列出要在启动时加载的内核模块。
   - 每行一个内核模块名称。

虽然这两个目录都用于配置内核模块的加载，但它们分别针对不同的工具和服务。

==`modprobe.d/` 目录是为了配置 `modprobe` 命令的行为，而 `modules-load.d/` 目录是为了配置 Systemd 的内核模块加载服务。==



在大多数情况下，建议使用 `modules-load.d/` 目录来配置系统的内核模块加载规则，因为它是与 Systemd 集成的标准方式。

如果你需要配置 `modprobe` 命令的行为，可以使用 `modprobe.d/` 目录。



# systemd是否支持syslog

是的，systemd 支持与 syslog（系统日志）的集成。systemd 提供了 `journald`，它是 systemd 的日志管理器，可以用作传统的 syslog 守护进程的替代方案。`journald` 提供了一种集中管理和存储系统日志的方法，并提供了一些高级功能。

**当系统使用 systemd 作为 init 系统时，系统日志会直接由 `journald` 处理，而不是传统的 syslog 守护进程。**`journald` 将日志消息存储在二进制格式的日志文件中，并提供了基于日志来源、优先级、时间戳等条件进行过滤和查询的功能。

**但是，systemd 仍然可以与传统的 syslog 守护进程集成，以便将日志消息发送到 syslog。**可以通过配置 systemd 的 `rsyslog` 或 `syslog-ng` 插件来实现此集成。这样做可以使 systemd 日志和传统 syslog 日志同时存在，并满足特定的日志需求。

要了解更多关于 systemd 的日志管理和与 syslog 的集成方式，请参考 systemd 官方文档以及相关的 syslog 集成配置文档。

需要注意的是，具体的配置和集成方法可能因操作系统和 systemd 版本而有所差异，建议查阅相关文档并根据实际情况进行配置。

希望以上信息对你有所帮助！如果还有其他问题，请随时提问。

# systemd调试服务



# systemd ExecStart是一个复杂脚本的模板

是的，`ExecStart` 属性可以包含一个复杂脚本的模板，以实现更灵活的命令执行。

在 systemd 服务文件中，`ExecStart` 属性可以包含一个完整的脚本命令行，而不仅仅是单个命令。你可以使用变量、条件语句、循环等来构建更复杂的命令。

以下是一个示例，展示了如何在 `ExecStart` 属性中使用模板：

```plaintext
[Service]
ExecStart=/bin/bash -c '
    var1="value1"
    var2="value2"
    if [ "$var1" = "value1" ]; then
        echo "Variable var1 is set to value1"
    fi
    for i in {1..5}; do
        echo "Iteration $i"
        sleep 1
    done
'
```

在上述示例中，`ExecStart` 属性包含了一个 `/bin/bash -c` 命令，后跟一个用单引号包裹的复杂脚本。脚本内部定义了变量 `var1` 和 `var2`，并使用了条件语句和循环进行逻辑控制。

你可以根据需要修改示例脚本，并将其嵌入到你的 systemd 服务文件的 `ExecStart` 属性中。

请注意，在使用复杂脚本模板时，确保脚本的语法正确，且能够在指定的执行环境中运行。你可以使用 `systemctl --verify` 命令验证服务文件的语法和语义错误。

希望这可以满足你的需求！如有任何其他问题，请随时提问。

# 自己进行进程的检查重启判断

如果你希望在 `ExecStart` 后面的脚本后台执行时，能够捕获异常并进行重新启动判断，可以通过以下几种方法来实现：

1. 使用 `ExecStartPost` 属性：在 systemd 服务文件中，可以使用 `ExecStartPost` 属性来指定在主 `ExecStart` 命令执行完成后执行的命令。你可以在 `ExecStartPost` 命令中编写脚本来检查服务的退出状态码，并根据需要执行重新启动操作。例如：

```plaintext
[Service]
ExecStart=/path/to/your-command &
ExecStartPost=/path/to/restart-check-script
```

在上述示例中，`ExecStart` 命令使用 `&` 将其放入后台执行，而 `ExecStartPost` 命令则用于执行重新启动检查脚本。

2. 使用自定义的启动脚本：将复杂的脚本放入一个单独的启动脚本中，并在该脚本中处理异常和重新启动逻辑。然后，在 systemd 服务文件中使用该脚本作为 `ExecStart` 的命令。例如：

```plaintext
[Service]
ExecStart=/path/to/start-script
```

在自定义的启动脚本中，你可以使用适当的语法和命令来后台执行你的脚本，并进行异常检测和重新启动判断。

无论哪种方法，都可以在后台执行的脚本或脚本模板中捕获异常，并根据自定义的逻辑进行重新启动操作。请根据你的具体需求选择适当的方法，并确保脚本的正确性和可靠性。

希望这对你有所帮助！如果还有其他问题，请随时提问。

## 调整某个service的reboot检查间隔

```
Restart=always
RestartSec=60s
```

## 默认的时间间隔是多少

在 systemd 中，`RestartSec` 属性的默认值是 100 毫秒（0.1 秒）。这意味着如果没有显式设置 `RestartSec` 属性，系统将默认等待 0.1 秒后重新启动服务。

## RemainAfterExit=yes

在 systemd 服务文件中，`RemainAfterExit` 是一个用于定义服务的状态的属性。当将 `RemainAfterExit` 设置为 `yes` 时，**它表示即使在服务主进程退出后，该服务仍然被视为处于活动状态。**

通常情况下，当一个服务的主进程退出时，systemd 会将该服务的状态标记为停止。但是，如果在服务文件中设置了 `RemainAfterExit=yes`，则 systemd 将保持该服务的状态为活动状态，不受主进程的退出影响。

**这个属性通常用于一些特殊类型的服务，比如后台进程或守护进程，它们的状态在主进程退出后仍然被认为是活动的。**

以下是一个示例 systemd 服务文件中使用 `RemainAfterExit=yes` 的部分：

```plaintext
[Service]
ExecStart=/path/to/your-command
RemainAfterExit=yes
```

通过设置 `RemainAfterExit` 为 `yes`，即可指示 systemd 在主进程退出后仍将该服务视为活动状态。

希望这能解答你的问题！如果还有其他疑问，请随时提问。

## systemd-tmpfiles-setup.service

`systemd-tmpfiles-setup.service` 是一个由 systemd 提供的服务单元，用于在启动过程中创建和管理临时文件和目录。

在 Linux 系统中，临时文件和目录对于临时性的数据存储和处理非常重要。`systemd-tmpfiles-setup.service` 服务负责根据预定义的规则，在系统启动时自动创建和清理临时文件和目录。

该服务会读取位于 `/usr/lib/tmpfiles.d/` 和 `/etc/tmpfiles.d/` 目录中的配置文件，这些配置文件定义了需要在每次启动时创建、修改或删除的临时文件和目录。

通过配置这些规则，可以确保临时文件和目录的正确权限、所有权和清理策略。这有助于保持系统的整洁性和安全性，并避免临时文件和目录积累导致的磁盘空间问题。

`systemd-tmpfiles-setup.service` 通常是在系统启动过程中自动运行的，它的目的是在早期阶段设置临时文件和目录，以便后续的服务和进程可以使用它们。

要查看 `systemd-tmpfiles-setup.service` 的状态，可以使用以下命令：

```
systemctl status systemd-tmpfiles-setup.service
```



```
# ls /usr/lib/tmpfiles.d/
dbus.conf                      static-nodes-permissions.conf
etc.conf                       systemd-tmp.conf
home.conf                      systemd.conf
journal-nocow.conf             tmp.conf
legacy.conf                    var.conf
portables.conf                 x11.conf
```

service里就是执行了这个命令：

```
/usr/bin/systemd-tmpfiles --create --remove --boot --exclude-prefix=/dev
```

## systemctl list-unit-files输出内容解析

`systemctl list-unit-files` 命令用于列出 systemd 中所有单元文件的状态和信息。其输出内容包含以下几个字段：

1. UNIT FILE：单元文件的名称。它包括单元文件的类型和名称，例如服务（service）、套接字（socket）、挂载（mount）等。

2. STATE：单元文件的当前状态。常见的状态包括 enabled（已启用）、disabled（已禁用）、static（静态）、masked（已屏蔽）等。

   - enabled：表示单元文件已启用，并会在系统启动时自动加载和运行。
   - disabled：表示单元文件已禁用，不会在系统启动时自动加载和运行。
   - static：表示单元文件是静态的，无法启动或停止。
   - masked：表示单元文件已屏蔽，无法启动。

3. DROP-IN：任何与单元文件关联的 drop-in 配置文件的数量。

   drop-in 配置文件是用于修改或扩展现有单元文件配置的附加配置文件。它们通常位于 `/etc/systemd/system/单元文件名称.d/` 目录中。

4. UNIT LOAD：单元文件的加载状态。常见的加载状态包括 loaded（已加载）、not-found（未找到）等。

   - loaded：表示单元文件已加载并可用。
   - not-found：表示未找到单元文件。

5. ACTIVE：单元文件的当前活动状态。常见的活动状态包括 active（活动）、inactive（非活动）、activating（正在激活）、deactivating（正在停用）等。

   - active：表示单元文件当前处于活动状态。
   - inactive：表示单元文件当前处于非活动状态。
   - activating：表示单元文件正在激活中。
   - deactivating：表示单元文件正在停用中。

6. SUB：单元文件的当前子状态。子状态是活动状态的更具体的描述。

7. DESCRIPTION：单元文件的描述信息。

通过分析 `systemctl list-unit-files` 命令的输出内容，你可以了解到系统中所有单元文件的状态、加载情况和活动状态。这对于管理和调试 systemd 单元文件非常有用。

希望这回答了你的问题！如果还有其他疑问，请随时提问。

## systemd 的状态是generated说明什么

在 systemd 中，"generated" 状态表示服务单元是由系统自动生成的。

当一个服务单元的状态显示为 "generated" 时，这意味着该服务单元的配置文件（.service 文件）不是直接手动创建的，而是通过其他机制（例如模板、生成器等）根据系统的特定条件自动生成的。

这种自动生成的机制可以根据系统配置和需要动态地创建、管理和调整服务单元。生成的服务单元通常是基于系统环境、硬件设备、用户配置等因素进行自适应。

例如，当使用 systemd 的模板化服务单元（template unit）时，根据需要动态地生成多个实例。这些实例根据模板中的参数进行自定义，以满足不同的需求。

当服务单元的状态显示为 "generated" 时，说明该服务单元的配置是由 systemd 自动处理的，而不是手动创建或编辑的。这样的机制使得 systemd 更加灵活和适应性强，能够根据系统的变化和需求进行动态调整和管理。

# system-generators

```
/usr/lib/systemd/system-generators # ls
systemd-debug-generator          systemd-rc-local-generator
systemd-fstab-generator          systemd-run-generator
systemd-getty-generator          systemd-system-update-generator
systemd-gpt-auto-generator       systemd-sysv-generator
```

## systemd-debug-generator 

`systemd-debug-generator` 是 systemd 的一个生成器脚本，用于生成用于调试目的的单位文件。它位于 `/usr/lib/systemd/system-generators/` 目录下。

该生成器脚本会检查系统是否启用了调试模式，如果是，则生成一系列用于调试的单位文件，以便在系统调试期间使用。

这些调试单位文件通常包括 `systemd-debug-shell.service`、`systemd-debug-generator.service`、`systemd-debug-generator.socket` 等，用于提供调试 shell、收集调试信息等功能。

**当 systemd 启动时，如果系统启用了调试模式，`systemd-debug-generator` 将自动运行并生成相应的调试单位文件。**

需要注意的是，`systemd-debug-generator` 是 systemd 内置的生成器脚本，通常无需进行手动配置或修改。它主要用于 systemd 开发和调试环境中，以便提供调试功能。

希望这个解答对你有帮助！如果你有其他问题，请随时提问。



## /run/systemd/generator.late目录

```
/run/systemd/generator.late # ls
S02lightDaemon.service       S80mdns.service
S02overlayfs.service         S82airplay2.service
S39wifi.service              S83dsd.service
S40network.service           S89usbgadget.service
S41dhcpcd.service            avs_mdns.service
S43sysname.service           avs_moniter.service
S43webserver.service         bluealsa_profilecfg.service
S44bluetooth.service         get_sysname.service
S48avs.service               ntpdate.service
S49optee.service             rc.modules.service
S71_load_dspa.service
```

怎么控制这个generate的行为呢？

# systemd禁止运行时生成/etc/init.d对应的service文件

如果你希望禁止 systemd 在运行时自动生成 `/etc/init.d` 目录下对应的 service 文件，可以通过修改 systemd 的配置文件来实现。

打开 `/etc/systemd/system.conf` 文件，找到并修改以下行：

```
RuntimeWatchdogSec=0
```

将上述行的值修改为 `0`，表示禁用运行时监控 watchdog。

保存文件后，重新加载 systemd 配置：

```
systemctl daemon-reload
```

这样修改后，systemd 将不再运行时生成 `/etc/init.d` 目录下的 service 文件。

请注意，这是一个系统范围的修改，将影响所有服务。如果你只想针对特定的服务禁用自动生成，请参考 systemd unit 文件的相关选项，例如 `Generator`、`ConditionPathExists` 等。

在进行任何系统配置修改之前，请确保备份重要文件，并在测试环境中进行验证。

# cgroups如何进行使用？

使用 `systemd` 中的 cgroups 进行资源管理和限制，可以按照以下步骤进行：

### 1. **查看当前 cgroups 状态**

可以使用以下命令查看当前系统中的 cgroups 状态：

```bash
# 查看 cgroup 层次结构
systemd-cgls
```

### 2. **创建和管理服务单元**

在创建或修改服务单元文件时，可以添加资源限制配置。以下是一个示例单元文件 `/etc/systemd/system/myservice.service`：

```ini
[Unit]
Description=My Custom Service

[Service]
ExecStart=/usr/bin/myapp
CPUQuota=50%          # 限制 CPU 使用率为 50%
MemoryLimit=100M     # 限制内存使用为 100MB

[Install]
WantedBy=multi-user.target
```

### 3. **重新加载和启动服务**

在修改单元文件后，需要重新加载 `systemd` 配置并启动服务：

```bash
# 重新加载 systemd 配置
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start myservice
```

### 4. **监控资源使用**

可以使用 `systemctl` 命令查看服务状态：

```bash
sudo systemctl status myservice
```

### 5. **使用 `cgset` 和 `cgget` 管理 cgroups**

如果需要更细粒度地控制 cgroups，可以使用 `cgroup-tools` 中的 `cgset` 和 `cgget`：

```bash
# 设置 cgroup 的资源限制
sudo cgset -r memory.limit_in_bytes=100M mygroup

# 获取 cgroup 的资源使用情况
sudo cgget -r memory.usage_in_bytes mygroup
```

### 6. **使用 `systemd` 直接管理 cgroups**

也可以通过 `systemd` 直接管理特定的 cgroups：

```bash
# 创建一个新的 cgroup
sudo systemctl set-property myservice.service MemoryLimit=200M
```

### 7. **停止或重启服务**

要停止或重启服务，可以使用以下命令：

```bash
# 停止服务
sudo systemctl stop myservice

# 重启服务
sudo systemctl restart myservice
```

### 总结

通过以上步骤，您可以有效地使用 `systemd` 中的 cgroups 来管理和限制系统资源，以提高系统的稳定性和性能。如有其他问题，请随时询问！

# systemd的namespace包括哪些内容

`systemd` 中的命名空间（namespace）用于提供资源隔离和管理，主要包括以下几种类型：

### 1. **Mount Namespace**
   - 隔离文件系统挂载点，允许不同进程有不同的视图。

### 2. **PID Namespace**
   - 隔离进程 ID，允许在不同的命名空间中重用相同的进程 ID。

### 3. **Network Namespace**
   - 隔离网络接口、IP 地址、路由表等，允许进程在不同的网络环境中运行。

### 4. **User Namespace**
   - 隔离用户和组 ID，允许进程以不同的用户权限运行而不影响系统全局设置。

### 5. **IPC Namespace**
   - 隔离进程间通信（IPC）资源，如共享内存和信号量，确保不同命名空间的进程不能相互访问 IPC 资源。

### 6. **Cgroup Namespace**
   - 隔离 cgroups，允许不同命名空间中的进程独立地管理资源限制。

### 使用示例

在 `systemd` 单元文件中，可以通过以下指令来配置命名空间：

```ini
[Service]
PrivateTmp=true               # 使用独立的临时文件系统
ProtectSystem=full            # 保护系统目录
ProtectHome=yes               # 保护用户主目录
NoNewPrivileges=true           # 防止新进程获得额外权限
```

### 总结

通过使用命名空间，`systemd` 能够为服务提供更好的资源隔离和安全性，增强系统的可靠性和安全性。如果您有其他问题或需要更多细节，请告知！

# 具体有什么命令可以使用

在 `systemd` 中，可以使用以下命令来管理和操作命名空间及相关功能：

### 1. **systemctl**
用于管理 `systemd` 服务和单元。

```bash
# 启动服务
sudo systemctl start <service-name>

# 停止服务
sudo systemctl stop <service-name>

# 查看服务状态
sudo systemctl status <service-name>

# 重新加载服务配置
sudo systemctl daemon-reload
```

### 2. **systemd-run**
用于创建新的服务或单元，并指定命名空间。

```bash
# 在新的网络命名空间中启动命令
sudo systemd-run --scope --property=PrivateNetwork=yes /path/to/command
```

### 3. **systemd-nspawn**
用于创建轻量级容器，支持多种命名空间。

```bash
# 启动一个新的 nspawn 容器
sudo systemd-nspawn -D /path/to/container
```

### 4. **ip**
用于管理网络命名空间。

```bash
# 创建网络命名空间
ip netns add <namespace-name>

# 进入网络命名空间
ip netns exec <namespace-name> /bin/bash
```

### 5. **unshare**
用于创建新命名空间并运行命令。

```bash
# 创建一个新的 PID 命名空间并运行命令
sudo unshare --fork --pid /bin/bash
```

### 6. **lsns**
用于列出当前系统中的所有命名空间。

```bash
# 列出所有命名空间
lsns
```

### 7. **nsenter**
用于进入另一个进程的命名空间。

```bash
# 进入指定 PID 的命名空间
sudo nsenter --target <pid> --mount --uts --ipc --net --pid
```

### 示例

创建和使用命名空间的简单示例：

```bash
# 创建一个新的网络命名空间
ip netns add mynamespace

# 在新的命名空间中执行命令
ip netns exec mynamespace ip addr
```

这些命令可以帮助您管理和操作 `systemd` 中的命名空间及其相关功能。如有其他问题，请随时询问！

# systemd会有哪些后台进程在运行？分别起什么作用？

在 `systemd` 中，多个后台进程（服务）可能会同时运行，每个进程都有特定的作用。以下是一些常见的 `systemd` 后台进程及其功能：

### 1. **systemd**
   - **作用**：`systemd` 本身是系统和服务管理器，负责启动和管理其他服务，处理系统引导和关闭。

### 2. **systemd-journald**
   - **作用**：管理系统日志，收集和存储日志信息，提供日志查询功能。

### 3. **systemd-logind**
   - **作用**：管理用户登录会话，包括用户登录、注销、会话管理等。

### 4. **systemd-networkd**
   - **作用**：管理网络配置和连接，支持静态和动态 IP 配置。

### 5. **systemd-resolved**
   - **作用**：提供 DNS 解析服务，处理名称解析请求。

### 6. **systemd-timesyncd**
   - **作用**：提供时间同步功能，确保系统时间与网络时间服务器同步。

### 7. **systemd-udevd**
   - **作用**：处理设备事件，动态管理设备节点，执行设备相关的规则。

### 8. **systemd-tmpfiles**
   - **作用**：管理临时文件和目录的创建、清理和删除。

### 9. **systemd-cgls**
   - **作用**：用于查看和管理控制组（cgroups），显示当前 cgroup 层次结构。

### 10. **systemd-userdbd**
   - **作用**：管理用户和组数据库，提供用户信息查询。

### 11. **systemd-oomd**
   - **作用**：监控内存使用并在必要时杀死进程，以防止系统耗尽内存。

### 总结

这些后台进程共同工作，以确保系统的稳定性、可管理性和安全性。`systemd` 通过这些组件来提供强大的服务管理和资源控制功能。如果您需要了解某个特定进程的更多细节，欢迎询问！

# systemd的log怎么打印和查看

在 `systemd` 中，日志的打印和查看主要通过 `journalctl` 工具和 `systemd-journald` 服务来实现。以下是如何打印和查看日志的步骤：

### 1. **打印日志**

#### 使用 `journalctl`

- **查看所有日志**：
  ```bash
  journalctl
  ```

- **查看最新日志**（实时更新）：
  ```bash
  journalctl -f
  ```

- **查看特定服务的日志**：
  ```bash
  journalctl -u <service-name>
  ```

- **查看自某个时间点以来的日志**：
  ```bash
  journalctl --since "2024-09-01 12:00:00"
  ```

- **查看特定优先级的日志**：
  ```bash
  journalctl -p warning   # 查看警告及更高优先级的日志
  ```

- **查看特定用户的日志**：
  ```bash
  journalctl _UID=<user-id>
  ```

### 2. **格式化输出**

- **以 JSON 格式输出**：
  ```bash
  journalctl -o json
  ```

- **以短格式输出**：
  ```bash
  journalctl -o short
  ```

### 3. **持久化日志**

默认情况下，`systemd-journald` 将日志存储在内存中。要使日志持久化，您需要创建一个目录 `/var/log/journal`：

```bash
sudo mkdir /var/log/journal
sudo systemd-tmpfiles --create --prefix /var/log/journal
```

### 4. **查看系统日志**

- **查看系统日志**（包括内核消息）：
  ```bash
  journalctl -k
  ```

### 5. **清理日志**

- **清理过期的日志**：
  ```bash
  journalctl --vacuum-time=2weeks   # 删除2周前的日志
  ```

### 总结

通过这些命令，您可以方便地打印和查看 `systemd` 的日志，帮助您进行系统故障排查和监控。如果有其他问题，请随时询问！

# 那些以*ctl为后缀的命令呢？例如timedatectl这些

以下是以 `*ctl` 为后缀的常用 `systemd` 命令的列表：

| 命令              | 描述                                                  |
| ----------------- | ----------------------------------------------------- |
| `systemctl`       | 管理系统服务和单元                                    |
| `journalctl`      | 查看和管理系统日志                                    |
| `timedatectl`     | 管理系统时间和日期                                    |
| `hostnamectl`     | 管理系统主机名                                        |
| `localectl`       | 管理本地化设置（语言和键盘布局）                      |
| `loginctl`        | 管理用户会话和登录信息                                |
| `udevadm control` | 管理设备管理器（udev）的行为                          |
| `resolvectl`      | 管理 DNS 解析（在某些系统中命名为 `systemd-resolve`） |
| `machinectl`      | 管理本地和远程容器                                    |
| `networkctl`      | 管理网络连接和状态                                    |
| `coredumpctl`     | 查看和管理核心转储文件                                |
| `busctl`          | 与 D-Bus 消息总线进行交互                             |
| `systemd-analyze` | 分析启动性能和服务依赖                                |

这些命令提供了对系统各种功能的控制和管理。如果您需要更详细的说明或具体用法，请随时询问！

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