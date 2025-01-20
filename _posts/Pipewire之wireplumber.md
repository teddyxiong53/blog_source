---
title: Pipewire之wireplumber
date: 2024-05-24 18:58:17
tags:
	- 音频

---

--

# 资源收集

官网文档

https://pipewire.pages.freedesktop.org/wireplumber/

重构wireplumber的配置文件系统：从lua到json

https://www.collabora.com/news-and-blog/blog/2022/10/27/from-lua-to-json-refactoring-wireplumber-configuration-system/

# 简介

PipeWire 的主要目的是充当应用程序和设备之间的中间层。

为此，它为应用程序提供了一种创建媒体流的通用方法，

然后可以将其定向到任何设备或其他应用程序进行播放或捕获。

此功能将 PipeWire 定义为流交换框架。

然而，除了提供创建媒体流的机制外，流交换还需要一种机制来定义谁在与谁交换数据。

换句话说，它需要一种机制来决定哪个应用程序将连接到哪个设备，如何以及何时连接。



在传统设置中，

应用程序可以直接访问设备。

这意味着他们需要自己选择他们想要打开的设备，

并根据他们的媒体要求进行设置（即选择音频采样率、格式、视频分辨率等）。

虽然系统配置可以具有“系统默认”设备（例如在ALSA中），

但在某些设置中并非如此，

这给应用程序开发人员提供了一种配置设备选择的方法。

此外，此类设置不允许设备的透明切换（例如，在播放音乐时将音频播放从笔记本电脑扬声器切换到蓝牙耳机），除非应用程序实现这样做所需的复杂操作。

在某些情况下，另一个问题是设备完全由单个应用程序控制，不允许需要共享设备的更复杂的用例。

最后但并非最不重要的一点是，

访问设备直接增加了应用程序媒体管道的复杂性，以便处理多种设备格式或处理行为异常/非标准设备。



PulseAudio 显著改善了音频应用的这种情况。

在 PulseAudio 中，音频设备在内部打开和配置，音频应用程序可以创建任何所需格式的流，并请求从“默认”设备播放或捕获。

应用程序开发人员不再需要提供配置要使用的设备的方法，尽管如果他们愿意，他们仍然可以这样做。

PulseAudio 在内部维护此“默认”设备首选项，

并自动创建必要的内部链接，

以便在从应用程序传入新流时使工作正常。

可以在运行时更改此默认设备首选项，

并且可以透明地将应用程序流重新存储到另一个设备，从而消除所有复杂性。

然而，这里的问题是，虽然这种逻辑对大多数桌面应用程序来说非常有用，但它不能很好地扩展到其他用例。此外，PulseAudio 不处理视频流......



另一方面是 JACK，它也处理一个特定的用例：专业音频。

JACK 同样允许应用程序只创建流而忘记设备。

但与 PulseAudio 不同的是，它在内部没有实现任何连接逻辑。

这留给一个外部组件：会话管理器。

会话管理器监视应用程序连接或断开连接，

并使用自己的逻辑将它们链接到设备或对等应用程序。

这可能涉及“默认”设备目标，

但它通常遵循一组更复杂的用户可配置规则，

允许灵活地为专业音频应用设置音频处理阶段。

然而，这里的问题是，JACK不能很好地处理典型的桌面用例，并且对于非专业人士来说很复杂。



这让我们回到了 PipeWire......PipeWire将所有这些设计的一部分结合在一起，提供了一个灵活的媒体服务器，可用于实现音频和视频的桌面、嵌入式、专业和非专业用例。

为了获得最大利益，PipeWire 还由会话管理器提供支持，类似于 JACK 中的会话管理器，但具有更多可用功能。



PipeWire 上游有一个非常有限的示例会话管理器。

它是构建新示例的一个很好的示例，

并且具有一些用于基本桌面用例和测试的功能，但它仅此而已。

WirePlumber 作为此示例的替代品，还提供了一个用于构建自定义会话管理器的框架。



WirePlumber 作为会话管理器的主要目标显然是监视来自应用程序的流，并确保它们根据其实现的用例规则链接到适当的设备或对等应用程序。

但是，与 JACK 会话管理器不同，PipeWire 会话管理器具有更多职责。



PipeWire 本身在启动时实际上不会打开任何设备。

它提供了可以执行此操作的组件，

但默认情况下不会在守护程序中加载这些组件。

会话管理器的主要任务是为其感兴趣的设备加载这些组件，并适当地配置设备。



作为会话管理器的一部分是合理的，

因为要探测哪些设备以及如何配置它们的决定特定于用例。

汽车的音频硬件需要与台式机的声卡不同的配置。



WirePlumber 提供了一个处理监控设备的模块，该模块适用于实现spa_device接口的所有 PipeWire 设备监控组件。

这包括 ALSA、V4L2 和 bluez5 显示器。

此外，它还提供了一个模块来加载特殊的“JACK”设备，

该模块允许 PipeWire 作为 JACK 音频服务器的客户端运行。



PipeWire 非常重视安全性，并默认假设所有应用程序都是不可信的。

在内部，它提供了一个类似于UNIX文件系统上的权限系统，

允许在客户端可以通过其IPC协议访问的所有对象上设置读取，写入和执行（rwx）位。

没有访问对象所需权限的客户端无法对其执行任何恶意操作。



因此，会话管理器的另一项任务是对客户端进行身份验证并授予它们适当的权限。

WirePlumber 为此提供了一个模块，

尽管在撰写本文时，该模块是虚拟的，并且没有进行适当的权限管理;

它只是授予所有客户端对所有对象的完全访问权限。

不过，有计划为 AGL 和桌面正确实现这一点，敬请期待。



PipeWire 在内部使用称为“节点”的组件图来表示媒体流，

这些组件相互链接。

这些是上图中的紫色和绿色框。

节点抽象处理逻辑，

并提供一种将数据传入和传出 PipeWire 的方法，将处理委托给客户端或设备。



在管理此图时，通常需要将多个节点作为单个实体一起管理，以提供更复杂的功能。

例如，在音频设备上运行的音频 DSP 滤波器将由直接链接到该音频设备节点的节点表示。

然后，希望其音频通过该筛选器的应用程序应将其节点与筛选器节点（而不是设备节点）链接。

这增加了任何组件的复杂性，无论哪个组件决定在哪里链接什么，因为它现在需要对这个过滤器的操作有特定的了解。

此外，这不适用于 pavucontrol 或 GNOME 的声音设置等配置 UI，

这些 UI 是围绕应用程序直接连接到设备的概念构建的，两者之间没有任何内容。



另一个问题是，在现代系统中，流通常与用例相关联。

这在桌面系统上并不明显，

但想想你的手机。

传递音乐的音频流与传递通知或警报声音的音频流是分开的，

它们带有单独的音量控制和策略，

包括它们是否可听见、是否被强调（所有其他流都静音或躲避到较低的音量）等......

类似的属性也适用于视频流，

例如，用于在屏幕上实时预览的相机源与用于视频录制的源和用于静止图像（照片）捕获的源具有不同的编码和分辨率。



虽然这听起来可能并不复杂，但在嵌入式系统中，将流与用例相关联可能非常复杂。

例如，在纯软件中，音频用例的实现只是对应用程序流进行分类，并根据策略配置调整其音量控制或链接状态。

然而，在嵌入式中，所有这些都是在专用的硬件 DSP 上实现的，

该 DSP 通过不同的路径接收所有流，

并在硬件中应用所有混音、音量变化、效果和策略。

因此，控制此硬件的操作变得特定于设备，

这意味着 CPU 端的会话管理器需要为策略配置提供一个抽象层，以便在不同的设备上类似地工作。



所有这些问题都可以在 WirePlumber 中通过实现某些称为端点的对象来解决。

端点，就像节点一样，也相互链接，形成一个图。

它们中的每一个都代表一个用户可以想象的位置，

媒体可以在其中路由到/路由到/传出（例如一对扬声器或蓝牙耳机的麦克风），并提供一组端点流，

这些端点流表示可以到达该位置的逻辑路径，通常与用例相关联。



此端点图（在文档中也称为“会话管理图”）的目的是提供一种从更高层次的角度查看节点图的方法，该视角涉及用户可以理解的用例和目标。

这样可以更轻松地编写策略和其他配置，使用户能够了解特定于设备的详细信息，并专注于此配置将提供的实际用户体验。



最后但并非最不重要的一点是，WirePlumber 提供了一个模块，该模块根据用户可配置的策略规则在端点之间创建链接。

这是它作为会话管理器的主要目标。

不幸的是，当前的策略配置方式并不像我们希望的那样灵活，

尽管它是编写策略管理模块的第二次尝试。

在不久的将来，我的计划是尝试使用基于 lua 的脚本来描述此策略。

这个主题将在以后的博客文章中进一步讨论，所以我将在这里保持简短。



在上面所有关于 WirePlumber 功能的文本中，

我都提到它提供了提供功能的“模块”。

这是 WirePlumber 的一个关键设计方面。

每个功能都是一个模块，

它基于共享库构建，具有通用功能和接口，允许模块协同工作。

WirePlumber 的公共库基于 GObject，

它允许轻松实现与其他语言的绑定。

虽然当前的模块都是用 C 语言编写的，但存在允许以不同语言实现它们的机制。

![img](images/random_name/WirePlumber-ModularDesign.png)



# wireplumber是什么

WirePlumber 是 PipeWire 的一个强大的会话和策略管理器。

基于模块化设计，使用实现实际管理功能的 Lua 插件，具有高度可配置性和可扩展性。

安装 wireplumber 软件包。它将与其他 PipeWire 会话管理器冲突，并确保它们已卸载。

WirePlumber 的配置由全局 PipeWire 风格的 JSON 对象组成，

例如 `context` 和 `alsa_monitor` 经过修改以更改其行为。

配置文件从 `~/.config/wireplumber/` （用户配置）、

 `/etc/wireplumber/` （全局配置）

和 `/usr/share/wireplumber/` （库存配置）中读取。

WirePlumber 首先读取主配置文件。

这是一个类似 JSON 的文件，

用于设置 PipeWire 上下文、SPA 插件、模块和组件。

在这些组件中，Lua 脚本引擎用于动态修改全局对象。

单实例配置文件位于 `/usr/share/wireplumber/wireplumber.conf` .这是默认配置，它包括一个进程中所有其他配置的功能。



配置 WirePlumber 的推荐方法

是将 SPA-JSON 文件添加到 

 `~/.config/wireplumber/` 

`/etc/wireplumber/` 相应 `wireplumber.conf.d/` 目录。

需要考虑的一些事项是：

如果要覆盖现有配置，请将其从 `/usr/share/wireplumber/` 目标复制到目标，同时保持其名称相同。具有相同名称但位于较低优先级位置的配置文件将被忽略。

否则，如果要添加新配置，则应以大于 50 的数字（例如 `51-my-config.conf` ）开头，因为默认配置主要以字母数字顺序等于或低于 50 完成。

# wireplumber的启动方式

**context.exec**

字典数组。数组中的每个条目都是字典，其中包含要在启动时执行的程序的路径和可选参数。

此数组曾经包含用于启动会话管理器的条目，但此后此操作模式已降级为开发辅助。避免在生产环境中以这种方式启动会话管理器。

==就直接手动执行wireplumber命令启动就可以。==



# 配置

WirePlumber 是一个高度模块化的守护进程。

==就其本身而言，除了加载其配置的组件之外，它不执行任何操作。==

实际的管理逻辑是在这些组件内部实现的。

启动时，WirePlumber 读取其配置文件（与其可能具有的所有片段相结合）并加载所选配置文件中指定的组件。

这配置了操作上下文。

==然后，这些组件接管并驱动整个守护进程的操作。==

## 配置文件

从 WirePlumber 0.5 开始，这是 WirePlumber 读取以加载配置的唯一文件（及其片段 - 见下文）。

过去，WirePlumber 还用来读取从 `wireplumber.conf` 引用的 Lua 配置文件，所有繁重的工作都是在 Lua 中完成的。

现在情况不再是这样，并且不再支持 Lua 配置文件。请参阅从 0.4 迁移配置。

请注意，Lua 仍然是 WirePlumber 的脚本语言，但它仅用于实际脚本编写，而不用于配置。

### spa json格式

此配置文件的格式是 JSON 的变体，

也用于 PipeWire 配置文件（也称为 SPA-JSON）。

该文件由一个未显式键入的全局 JSON 对象和一个部分列表组成，

这些部分本质上是该全局 JSON 对象的键值对。

每个部分通常是一个 JSON 对象，但也可以是一个 JSON 数组。

SPA-JSON 是标准 JSON 的超集，因此任何有效的 JSON 文件也是有效的 SPA-JSON 文件。但是，它比标准 JSON 更宽松。首先，它允许输入不带引号的字符串（ `"` ），除了标准的 `:` 作为键和值之间的分隔符 。这可以使其看起来类似于 INI 文件或人们熟悉的其他自定义配置格式，从而使用户更容易阅读和编辑。



就像 PipeWire 一样，WirePlumber 支持配置片段。

这意味着主配置文件可以拆分为多个文件，

所有这些文件都将被加载并合并在一起。

==这对于允许用户自定义其配置而无需修改主文件非常有用。==

## 配置的section

| 配置名字         | 说明                                                         |
| ---------------- | ------------------------------------------------------------ |
| components       | 一个数组，列出了 WirePlumber 可以加载的组件。                |
| componetns.rules | 也是数组，里面是修改components的一些规则                     |
| profiles         | 可以加载的配置文件，就类似蓝牙的profile那种概念，是一系列配置的组合。目前只有一个main profile。 |
| settings         | 修改wireplumber的行为                                        |
| settings.schema  | 验证修改                                                     |
| 其他             |                                                              |

另外，还有libpipewire来读取并发送给pipewire的部分。

```
context.properties
context.spa-libs
context.modules

```

### 组件类型

组件的主要类型有：

script/lua

一种 Lua 脚本，通常包含一个或多个事件挂钩和/或其他自定义逻辑。这是主要的组件类型，因为 WirePlumber 的业务逻辑主要是用 Lua 编写的。

module

WirePlumber 模块，它是一个可以动态加载的共享库。模块通常提供一些供脚本使用的捆绑逻辑或 WirePlumber 与外部服务之间的一些集成。

pw-module

PipeWire 模块，也是一个可以动态加载的共享库，但扩展了底层 libpipewire 库的功能。在 WirePlumber 上下文中加载 PipeWire 模块对于加载自定义协议扩展或从 PipeWire 守护程序卸载某些功能非常有用。

virtual

虚拟组件只是加载目标，可用于通过定义依赖关系来引入其他组件。它们本身不提供任何功能。请注意，此类组件没有“名称”。

built-in

这些组件是已内置到 WirePlumber 库中的功能部件。他们主要提供内部支持元素和检查。



添加片段以修改默认配置的最简单方法是创建一个名为 `~/.config/wireplumber/wireplumber.conf.d` 的目录并将片段放置在那里。

所有片段文件都需要具有 `.conf` 扩展名，并且必须是有效的 SPA-JSON 文件。片段按字母数字顺序加载，因此您可以通过相应命名来控制它们的加载顺序。建议使用数字前缀作为文件名，例如 `10-my-fragment.conf` 、 `20-my-other-fragment.conf` 等，以便您可以轻松控制它们的加载顺序。

如果您不想附加新规则，而是用新规则覆盖整个数组，则可以通过在数组名称上使用 `override.` 前缀来实现：

```
override.monitor.alsa.rules = [
  {
    matches = [
      {
        device.name = "~alsa_card.*"
      }
    ]
    actions = {
      update-props = {
        api.alsa.use-ucm  = false
      }
    }
  }
]
```

## alsa配置

ALSA 监视器是 WirePlumber 的组件之一。

==该监视器负责为系统上可用的所有 ALSA 卡创建 PipeWire 设备和节点。==

它还管理这些设备的配置。

ALSA 监视器默认启用，可以使用配置文件中的 `monitor.alsa` 功能禁用。

与所有设备监视器一样，该监视器作为 SPA 插件实现，

并且是 PipeWire 的一部分。 

**WirePlumber 只是加载插件并让它完成工作。**

然后，该插件监视 UDev 并为系统上可用的所有 ALSA 卡创建设备和节点对象。

> 这里值得记住的一件事是，在 ALSA 中，“卡”代表物理声音控制器设备，而“设备”是逻辑访问点，代表卡的一部分的一组输入和/或输出。在 PipeWire 中，“设备”直接相当于 ALSA“卡”，而“节点”几乎相当于（接近，但不完全）ALSA“设备”。

### acp

```
monitor.alsa.properties = {
  alsa.use-acp = true
}
```

这将探测设备并配置可用的配置文件、端口和混音设置。

用于执行此操作的代码直接来自 PulseAudio，

提供看起来和感觉完全像 PulseAudio 设备的设备。

跟ACP对等的一个配置是UCM。



## 蓝牙配置

# 会话管理

PipeWire 会话管理器是一个负责做很多事情的工具。

许多人将“会话管理器”一词理解为负责管理节点之间链接的工具，

但这只是众多任务之一。

要了解其整个操作，我们需要首先讨论 PipeWire 的工作原理。

当 PipeWire 启动时，

它会加载在其配置文件中定义的一组模块。

这些模块为 PipeWire 提供功能，

否则它只是一个不执行任何操作的空进程。



正常情况下，PipeWire启动时加载的模块包含对象工厂，

以及允许进程间通信的本机协议模块。

==除此之外，PipeWire 并不真正加载或执行任何其他操作。==

==这是会话管理开始的地方。==



会话管理基本上就是设置 PipeWire 来做一些有用的事情。

这是通过利用 PipeWire 公开的对象工厂来创建一些有用的对象，

然后使用它们的方法来修改并随后销毁它们来实现的。

这些对象包括设备、节点、端口、链路等。

==这项任务需要持续监控和采取行动，==

==对系统使用过程中发生的大量不同事件做出反应。==



WirePlumber 构建在 libwireplumber 库之上，

该库提供了用于表达所有会话管理逻辑的基本构建块。

 Libwireplumber是用C语言编写的，

基于GObject，包装了PipeWire API，

并提供了更高级别和更方便的API。

虽然 WirePlumber 守护程序实现会话管理逻辑，

但也可以在 WirePlumber 守护程序范围之外使用底层库。

这允许创建与 PipeWire 交互的外部工具和 GUI。



该库基于 GObject，具有自省功能，可以在任何支持 GObject 自省的语言中使用。该库还可以作为 C API 提供。



PipeWire 通过 IPC 协议公开多个对象，

例如节点和端口，

其方式很难使用标准面向对象原理进行交互，因为它是异步的。

例如，当创建一个对象时，它的存在是通过协议宣布的，但其属性稍后在辅助消息上宣布。

如果某些东西需要对此对象创建事件做出反应，它通常需要访问对象的属性，

因此它必须等到属性被发送。

这样做可能听起来很简单，而且确实如此，

但是在任何地方都这样做而不是专注于编写实际的事件处理逻辑，这会成为一个乏味的重复过程。



==WirePlumber 的库通过创建代理对象来解决这个问题，==

这些代理对象在每个对象的生命周期中缓存从 PipeWire 接收的所有信息和更新。

然后，它通过 WpObjectManager API 使它们可用，该 API 能够等到某些信息（例如属性）已缓存在每个对象上后再宣布。



Lua 脚本实现了大部分会话管理。 

libwireplumber API 在 Lua 中提供，具有惯用的绑定，这使得编写会话管理逻辑变得非常容易。

选择Lua是因为它是一种非常轻量级的脚本语言，适合嵌入。

它也非常容易学习和使用，并将其绑定到 C 代码。

然而，WirePlumber 可以轻松扩展以支持 Lua 以外的脚本语言。

==整个Lua脚本系统是作为一个模块实现的。==



会话管理就是对事件做出反应并采取必要的操作。这就是为什么 WirePlumber 的逻辑全部构建在事件和钩子上。

## session管理的内容

### 设备启用

启用设备是操作的一个基本领域。

它是通过使用设备监视器对象（或简称“监视器”）来实现的，

这些对象通常作为 PipeWire 中的 SPA 插件实现，

但由 WirePlumber 加载。

他们的任务是发现可用的媒体设备并在 PipeWire 中创建提供与它们交互的方式的对象。

### 设备配置

从计算机的角度来看，大多数设备都具有复杂的功能，

需要对其进行管理才能提供简单流畅的用户体验。

例如，出于这个原因，音频设备被组织成配置文件和路由，

这允许将它们设置为服务于特定的用例。

这些需要由会话管理器进行配置和管理。

### 权限控制

当客户端应用程序连接到 PipeWire 时，

它们需要获得权限才能访问 PipeWire 公开的对象并与其交互。

在某些情况和配置中，会话管理器还负责决定应向每个客户端授予哪些权限。

### node配置

节点是媒体处理的基本元素。

==它们通常由设备监视器或客户端应用程序创建。==

当它们被创建时，它们处于无法链接的状态。

链接它们需要一些配置，

例如配置媒体格式以及随后应公开的端口的数量和类型。

此外，可能需要根据用户偏好设置与节点相关的一些属性和元数据。

所有这些都由会话管理器负责。

### link管理

当节点最终准备好使用时，

会话管理器还负责决定如何将它们链接在一起以便媒体能够流动。

例如，音频播放流节点很可能需要链接到默认音频输出设备节点。

然后，会话管理器还需要==创建所有这些链接并监视可能影响它们的所有条件，==

以便在发生变化时（例如，如果设备断开连接）可以进行动态重新链接。

在某些情况下，由于创建或销毁链路，设备和节点配置也可能需要更改。

### 元数据管理

在操作过程中，PipeWire 和 WirePlumber 都将有关对象及其操作的一些附加属性

存储在这些对象外部的存储中。

这些属性称为“元数据”，

它们存储在“元数据对象”中。

该元数据可以通过 pw-metadata 等工具从外部进行更改，也可以通过其他工具进行更改。

在某些情况下，此元数据需要与会话管理器内部的逻辑进行交互。

最值得注意的是，

选择默认音频和视频输入和输出是通过设置元数据来完成的。

然后，会话管理器需要验证此信息，存储它并在下次重新启动时恢复它，但还要确保在动态插入和拔出设备时默认输入和输出保持有效和合理。



# lua

WirePlumber 使用 Lua 版本 5.4 来实现其引擎。对于较旧的系统，还支持 Lua 5.3。

==可以使用该 `wpexec` 工具运行脚本。==

WirePlumber 的脚本引擎将 lua 脚本沙盒到一个安全的环境中。

在此环境中，以下规则适用：

* 脚本是相互隔离的;一个脚本中的全局变量在另一个脚本中不可见，即使它们实际上是在同一个 `lua_State` 脚本中执行的
* 保存 API 方法的表不可写。虽然这听起来可能很奇怪，但标准 Lua 允许您更改标准 API，例如 `string.format = rogue_format` 在沙盒之外有效。WirePlumber 不允许这样做。
* 标准 Lua API 仅限于安全函数的子集。例如，不允许与文件系统 （io.*） 和进程状态 （例如：os.exit） 交互的函数
* 对象方法不会在公共表中公开。要调用对象方法，您必须使用 Lua 的方法调用语法，即 `object:method(params)`

例如，以下内容无效：

```
-- this will cause an exception
local node = ...
Node.send_command(node, "Suspend")

```

正确的形式是这样的：

```
local node = ...
node:send_command("Suspend")
```



为 WirePlumber 脚本提供支持的 Lua 引擎提供了与 GObject 的直接集成。

您将在 lua 脚本中处理的大多数对象都是包装 GObjects。

为了使用脚本，您首先需要对 GObject 的基本概念（例如信号和属性）有一个基本的了解。

所有 GObject 都具有属性的能力。

在 C 语言中，我们通常使用 g_object_get 来检索它们，g_object_set 来设置它们。

在 WirePlumber 的 lua 引擎中，这些属性作为 Lua 对象的对象成员公开。

GObjects 还具有将事件传递到外部回调的通用机制。

这些事件称为信号。

要连接到信号并处理它，您可以使用 connect 方法：



# wpctl命令

```
Usage:
  wpctl [OPTION?] COMMAND [COMMAND_OPTIONS] - WirePlumber Control CLI

Commands:
  status 
  inspect ID
  set-default ID
  set-volume ID VOL
  set-mute ID 1|0|toggle
  set-profile ID INDEX
  clear-default [ID]
```

## status

没有播放音乐的时候，

```
PipeWire 'pipewire-0' [1.1.81, root@buildroot, cookie:4213201345]
 └─ Clients:
        32. WirePlumber                         [1.1.81, root@buildroot, pid:4004]
        33. WirePlumber [export]                [1.1.81, root@buildroot, pid:4004]
        54. wpctl                               [1.1.81, root@buildroot, pid:5921]

Audio
 ├─ Devices:
 │      36. Built-in Audio                      [alsa]
 │      37. Built-in Audio                      [alsa]
 │  
 ├─ Sinks:
 │      38. Built-in Audio Stereo               [vol: 0.74]
 │  *   40. Built-in Audio Analog Stereo        [vol: 0.74]
 │  
 ├─ Sink endpoints:
 │  
 ├─ Sources:
 │      39. Built-in Audio Stereo               [vol: 0.74]
 │  *   41. Built-in Audio Analog Stereo        [vol: 0.74]
 │  
 ├─ Source endpoints:
 │  
 └─ Streams:

Video
 ├─ Devices:
 │  
 ├─ Sinks:
 │  
 ├─ Sink endpoints:
 │  
 ├─ Sources:
 │  
 ├─ Source endpoints:
 │  
 └─ Streams:

Settings
 └─ Default Configured Node Names:
```

用pw-play播放音乐后

```
# wpctl status
PipeWire 'pipewire-0' [1.1.81, root@buildroot, cookie:4213201345]
 └─ Clients:
        32. WirePlumber                         [1.1.81, root@buildroot, pid:4004]
        33. WirePlumber [export]                [1.1.81, root@buildroot, pid:4004]
        54. pw-cat                              [1.1.81, root@buildroot, pid:13101]
        56. wpctl                               [1.1.81, root@buildroot, pid:13116]

Audio
 ├─ Devices:
 │      36. Built-in Audio                      [alsa]
 │      37. Built-in Audio                      [alsa]
 │  
 ├─ Sinks:
 │      38. Built-in Audio Stereo               [vol: 0.74]
 │  *   40. Built-in Audio Analog Stereo        [vol: 0.74]
 │  
 ├─ Sink endpoints:
 │  
 ├─ Sources:
 │      39. Built-in Audio Stereo               [vol: 0.74]
 │  *   41. Built-in Audio Analog Stereo        [vol: 0.74]
 │  
 ├─ Source endpoints:
 │  
 └─ Streams:
        55. pw-play                                                     

Video
 ├─ Devices:
 │  
 ├─ Sinks:
 │  
 ├─ Sink endpoints:
 │  
 ├─ Sources:
 │  
 ├─ Source endpoints:
 │  
 └─ Streams:

Settings
 └─ Default Configured Node Names:
```

## inspect

```
# wpctl inspect 36
id 36, type PipeWire:Interface:Device
    alsa.card = "0"
    alsa.card_name = "AML-AUGESOUND"
    alsa.driver_name = "amlogic_snd_soc"
    alsa.id = "AMLAUGESOUND"
    alsa.long_card_name = "AML-AUGESOUND"
    api.acp.auto-port = "false"
    api.acp.auto-profile = "false"
    api.alsa.card = "0"
    api.alsa.card.longname = "AML-AUGESOUND"
    api.alsa.card.name = "AML-AUGESOUND"
    api.alsa.path = "hw:0"
    api.alsa.use-acp = "true"
    api.dbus.ReserveDevice1 = "Audio0"
  * client.id = "33"
  * device.api = "alsa"
    device.bus-path = "/sys/devices/platform/auge_sound/sound/card0"
  * device.description = "Built-in Audio"
    device.enum.api = "udev"
    device.form-factor = "internal"
    device.icon-name = "audio-card-analog"
  * device.name = "alsa_card._sys_devices_platform_auge_sound_sound_card0"
  * device.nick = "AML-AUGESOUND"
    device.plugged.usec = "3764562"
    device.string = "0"
    device.subsystem = "sound"
    device.sysfs.path = "/devices/platform/auge_sound/sound/card0"
  * factory.id = "15"
  * media.class = "Audio/Device"
    object.path = "alsa:acp:AMLAUGESOUND"
  * object.serial = "36"
```

## set-default

https://forum.manjaro.org/t/how-do-i-permanently-set-the-default-audio-device-in-manjaro-xfce-with-pipewire/117967/18

这个人想要做的事情跟我的一样，就是想用wpctl来设置默认的sink设备。

但是看起来他没有得到答案。

## settings

```
wpctl settings --save device.routes.default-sink-volume 0.5
```

可以在配置文件里写：

```
wireplumber.settings = {
  device.routes.default-sink-volume = 0.5
}
```



# wpexec

这个是用来执行lua脚本的。相当于一个lua解释器。

随便写一个test.lua，

```
print("hello pw")
```

wpexec test.lua

可以打印，但是会卡住不会自动退出。



# debug 日志

```
wpctl set-log-level D     # enable debug logging for Wireplumber
wpctl set-log-level -     # restore default logging for Wireplumber

wpctl set-log-level 0 4   # enable debug logging for Pipewire daemon
wpctl set-log-level 0 -   # restore default logging for Pipewire daemon
```



```
WIREPLUMBER_DEBUG=2,wp-registry:4,pw.*:4,m-*:4
```

从 WirePlumber 0.3 开始，不再使用 `G_MESSAGES_DEBUG` ，因为 libwireplumber 替换了默认的日志处理程序。

这样启动日志打印比较详细。

```
WIREPLUMBER_DEBUG=4 wireplumber
```



# 运行多个实例

WirePlumber 能够作为单个实例守护程序或多个实例运行，这意味着可以有多个进程，每个进程执行不同的任务。

为了实现多实例设置，可以多次启动 WirePlumber，并在每个实例中加载不同的配置文件。这可以通过使用 `--profile` 命令行选项来选择要加载的配置文件来实现：

```
$ wireplumber --profile=custom
```

当未指定特定配置文件时，将加载 `main` 配置文件。

为了使其更易于使用，提供了一个模板 systemd 单元，该单元以配置文件的名称作为模板参数启动：

```
$ systemctl --user disable wireplumber # disable the "main" instance

$ systemctl --user enable wireplumber@policy
$ systemctl --user enable wireplumber@audio
$ systemctl --user enable wireplumber@camera
$ systemctl --user enable wireplumber@bluetooth
```





# 板端配置文件分析



# wireplumber优点和缺点

## 优点

WirePlumber是专门为GNOME设计的，

这使得它在与GNOME桌面环境集成方面表现出色。

它能够更好地支持GNOME的特性和用户体验。

==WirePlumber支持使用LUA脚本来实现设置和配置规则，==

==这使得用户可以根据自己的需求进行高度定制。==

这种灵活性对于需要复杂配置的用户来说是一个显著优势。

WirePlumber被认为是PipeWire的新一代会话管理器，它结合了PulseAudio和JACK的功能，并增加了视频处理的能力。

WirePlumber可以在多种Linux发行版上安装和配置，包括基于Arch、Ubuntu/Debian等系统的支持。这使得它能够覆盖更多用户群体。

WirePlumber支持蓝牙MIDI设备，这是其在多媒体设备支持方面的一个重要优势。此外，它还支持压缩解码离载，这可以在某些设备上提高性能。

## 缺点

尽管WirePlumber提供了高度的自定义能力，但这也可能导致较高的学习曲线。对于不熟悉LUA脚本的用户来说，配置和维护可能会比较困难。

WirePlumber是为GNOME设计的，因此它可能不适用于所有类型的Linux系统，特别是那些不使用GNOME桌面环境的系统。

相比于一些成熟的框架，如Phonon，WirePlumber可能在社区和文档支持方面还有待提升。新用户可能需要花费更多时间来解决问题。

WirePlumber在灵活性、集成度和功能性方面具有显著优势，但同时也存在一定的局限性和挑战。







WirePlumber 使用 Lua 脚本来实现节点和连接管理的方式

主要体现在其对 Lua 的集成和应用上。

这种集成允许 WirePlumber 利用 Lua 的灵活性和高效性来进行复杂的配置和管理任务。

WirePlumber 的设计包括了对 Lua 脚本的使用，

这些脚本可以用于实现设置和配置规则，

如设备和流的设置和配置，以及基于流的元数据和系统的管理 。

这表明 Lua 脚本在 WirePlumber 中扮演着核心角色，特别是在处理和管理 PipeWire 会话方面。

通过这些 API，开发者可以编写自定义的 Lua 脚本来满足特定的需求，从而实现更细粒度的控制和管理。

总结来说，WirePlumber 中的 Lua 脚本通过提供一个强大且灵活的编程环境，使得用户和开发者能够有效地管理节点和连接。







就是这样！WirePlumber 现在已经检测到我们的 ALSA 接收器和源，并将它们作为节点添加到 PipeWire 图中。它将检测我们添加到图形中的源节点，并将它们链接到 ALSA 接收器节点，输出音频供我们的耳朵欣赏。



与 WirePlumber 的交互将使用 `wpctl` CLI 工具完成。它允许人们使用 `wpctl status` .WirePlumber 控制输出音频的主要方法是设置默认接收器，这可以使用 `wpctl set-default $ID` . `set-volume` 和 `get-volume` `set-mute` 命令公开音量控制。例如，以下是将当前输出音量提高 10% 所需的命令： `wpctl set-volume @DEFAULT_SINK@ 10%+` 。



这2个命令可以用的。有效果。

```
wpctl set-volume @DEFAULT_SINK@ 10%+

wpctl get-volume @DEFAULT_SINK@ 
```



把wireplumber里跟alsa有关系的日志拷贝出来分析。



```
opening fragment file:  /usr/share/wireplumber/wireplumber.conf.d/alsa-vm.conf
	打开这个配置片段文件。看里面内容是就是一个match pci的声卡的。
map factory regex 'api.alsa.*' to 'alsa/libspa-alsa
	映射factory，来自于context.spa-libs配置
 loaded plugin:'/usr/lib/spa-0.2/alsa/libspa-alsa.so'
 	然后就把so载入了。
  loading component 'monitor.alsa.reserve-device [virtual]'
    这个是因为被alsa wants了。
 s-monitors alsa.lua:351:createMonitor: Activating ALSA monitor
 	lua脚本里创建alsa monitor。
 	查找到路径是/usr/share/wireplumber/scripts/monitors/alsa.lua
  section 'monitor.alsa.rules' is used as-is from '/usr/share/wireplumber/wireplumber.conf.d/alsa-vm.conf'
  	从这里读取rules
load lib:'alsa/libspa-alsa' factory-name:'api.alsa.enum.udev'
loaded plugin:'/usr/lib/spa-0.2/alsa/libspa-alsa.so'
../spa/plugins/alsa/alsa-udev.c:712:check_access: /dev/snd/pcmC0D4c accessible:1
	C0D4是loopback-a。为什么最先是这个？
check_access: /dev/snd/pcmC0D4c accessible:1
check_pcm_device_availability: card 0 has 8 PCM device(s)
check_pcm_device_availability: card 0 pcm device pcm0c free
check_pcm_device_availability: card 0 pcm device pcm0p free
check_pcm_device_availability: card 0 pcm device pcm1c free
check_pcm_device_availability: card 0 pcm device pcm1p free
check_pcm_device_availability: card 0 pcm device pcm2c free
check_pcm_device_availability: card 0 pcm device pcm3c free
check_pcm_device_availability: card 0 pcm device pcm3p free
check_pcm_device_availability: card 0 pcm device pcm4c free
emit_added_object_info:     device.bus-path = "/sys/devices/platform/auge_sound/sound/card0"
find_match: 'node.name' fail '(null)' < > '~alsa_input.pci.*'
	这个是不是因为不存在pci接口的声卡？是的。但是没有关系。
Enabling the use of ACP on alsa_card._sys_devices_platform_auge_sound_sound_card0
check_access: /dev/snd/pcmC1D1c accessible:1
emit_added_object_info:     device.bus-path = "/sys/devices/platform/snd_aloop.0/sound/card1"
	loopback声卡的。
Enabling the use of ACP on alsa_card._sys_devices_platform_snd_aloop.0_sound_card1
../spa/plugins/alsa/alsa-acp-device.c:1065:impl_init: probe card hw:0
Unable to find the top-level configuration file '/usr/share/alsa/ucm2/ucm.conf'.
snd_use_case_mgr_open: error: failed to import AML-AUGESOUND use case configuration -2

pa_config_parse: Parsing configuration file '/usr/share/alsa-card-profile/mixer/profile-sets/default.conf'
	这个文件是存在的，是ini格式的。
 spa.alsa confmisc.c:1377:snd_func_refer: Unable to find definition 'cards.0.pcm.front.0:CARD=0'
 	然后接下来就是根据从default.conf读取的各种配置进行解析。
 	大部分都是无效的。
 pa_alsa_open_by_device_string: Trying hw:0,0 with SND_PCM_NO_AUTO_FORMAT 
 	这样依次打开关闭所有的设备。
```

```
Registering DBus media endpoint: /MediaEndpointLE/BAPSource/lc3
Registering DBus media endpoint: /MediaEndpointLE/BAPSink/lc3
Registering DBus media endpoint: /MediaEndpointLE/BAPBroadcastSource/lc3
Registering DBus media endpoint: /MediaEndpointLE/BAPBroadcastSink/lc3
Registering DBus media endpoint: /MediaEndpoint/A2DPSource/aac
Registering DBus media endpoint: /MediaEndpoint/A2DPSink/aac
Registering DBus media endpoint: /MediaEndpoint/A2DPSource/sbc
Registering DBus media endpoint: /MediaEndpoint/A2DPSink/sbc
Registering DBus media endpoint: /MediaEndpoint/A2DPSource/sbc_xq
Registering DBus media endpoint: /MediaEndpoint/A2DPSink/sbc_xq
Registering DBus media endpoint: /MediaEndpoint/A2DPSource/faststream
Registering DBus media endpoint: /MediaEndpoint/A2DPSource/faststream_duplex


wp_state_save: <WpState:0x13df5d0> saving state into /.local/state/wireplumber/default-routes


```

# /.local/state/wireplumber/

```
/ # ls /.local/state/wireplumber/
default-routes     stream-properties
```

这里列出的 `/.local/state/wireplumber/` 目录包含了 WirePlumber 的一些状态信息和配置文件。让我们看一下这些文件的含义：

- **default-routes**: 这个文件可能包含 WirePlumber 当前的默认路由配置。默认路由是指当没有特定路由配置时，WirePlumber 将音频流路由到的默认目的地。可以在这个文件中查看或修改默认路由配置。

- **stream-properties**: 这个文件可能包含了 WirePlumber 当前正在运行的音频流的属性信息。音频流属性描述了每个音频流的特征和配置。你可以在这个文件中查看或修改音频流的属性。

这些文件可能是 WirePlumber 在运行过程中生成和维护的。通过查看这些文件，你可以了解当前 WirePlumber 的配置和状态信息，以及对其进行必要的调整和管理。

# @DEFAULT_SINK@

```
src/tools/wpctl.c:124:  if (allow_def_audio && (g_strcmp0(arg, "@DEFAULT_SINK@") == 0 ||
```

所以这个不是什么特殊的语法，就是一个写死的字符串而已。





WirePlumber 首先读取主配置文件。

这是一个类似 JSON 的文件，

用于设置 PipeWire 上下文、SPA 插件、模块和组件。

==在这些组件中，Lua 脚本引擎用于动态修改全局对象。==

单实例配置文件位于 `/usr/share/wireplumber/wireplumber.conf` .这是默认配置，它包括一个进程中所有其他配置的功能。

配置 WirePlumber 的推荐方法是将 SPA-JSON 文件添加到 或 `~/.config/wireplumber/` 中的 `/etc/wireplumber/` 相应 `wireplumber.conf.d/` 目录。需要考虑的一些事项是：

如果要覆盖现有配置，请将其从 `/usr/share/wireplumber/` 目标复制到目标，同时保持其名称相同。具有相同名称但位于较低优先级位置的配置文件将被忽略

否则，如果要添加新配置，则应以大于 50 的数字（例如 `51-my-config.conf` ）开头，

因为默认配置主要以字母数字顺序等于或低于 50 的文件中完成。

```
wpctl status
查看到默认的sink是48
然后用 wpctl inspect 48 查看信息
```

选择 `device.name` or `node.name` 属性以用于 Lua 配置脚本中 `matches` 的规则。

避免使用 `device.id` ，它是动态的，经常变化。

例如，要更改 ALSA 节点的描述，您需要创建一个文件，例如：

```
/etc/wireplumber/wireplumber.conf.d/51-device-rename.conf (or ~/.config/wireplumber/wireplumber.conf.d/51-device-rename.conf)
monitor.alsa.rules = [
  {
    matches = [
      {
        node.name = "alsa_output.pci-0000_00_1f.3.output_analog-stereo"
      }
    ]
    actions = {
      update-props = {
        node.description = "Laptop"
      }
    }
  }
]
```

# 修改一个alsa节点的名字

例如，要更改 ALSA 节点的描述，您会创建一个文件，如：

```
/etc/wireplumber/wireplumber.conf.d/51-device-rename.conf
```

```
monitor.alsa.rules = [
  {
    matches = [
      {
        node.name = "alsa_output.pci-0000_00_1f.3.output_analog-stereo"
      }
    ]
    actions = {
      update-props = {
        node.description = "Laptop"
      }
    }
  }
]
```

如果要更改蓝牙节点或设备上的某些内容，可以创建一个文件

创建这样的一个文件：

```
/etc/wireplumber/wireplumber.conf.d/52-bluez-rename.conf 
```

内容：

```
monitor.bluez.rules = [
  {
    matches = [
      {
        node.name = "bluez_output.02_11_45_A0_B3_27.a2dp-sink"
      }
    ]
    actions = {
      update-props = {
        node.nick = "Headphones"
      }
    }
  }
]
```

# lua配置切换到json

https://www.collabora.com/news-and-blog/blog/2022/10/27/from-lua-to-json-refactoring-wireplumber-configuration-system/

使用 Lua 作为配置语言有一些优势，

因为它可以轻松且直接地与 Lua 代码和 C 代码集成。

此外，基于规则/条件的设置实现（这是 PipeWire 的特色，即其中的每个实体都是一个对象，每个对象都有属性，这些属性可以用于应用设置）在 Lua 中实现起来非常简便。

然而，存在一些明显的缺点。

举几个例子：

设置无法在运行时更改，因为它们是静态设置，用户可以进行覆盖，但这既不优雅也不直观，而且使用模式验证配置几乎是不可能的。

就其价值而言，我非常享受使用 Lua 作为脚本语言和配置系统。然而，是时候告别将其用作配置系统了。



经过深思熟虑，我们决定使用 PipeWire 的 JSON 语法来定义设置。

这克服了 Lua 配置的缺点，并在整个 PipeWire 生态系统中提供了一种更统一的配置方法。



PipeWire 的 JSON 语法是 JSON 的一种变体，称为“SPA JSON”，它是 PipeWire 内置的。

SPA JSON 解析器是一个非常轻量级的解析器，

主要忽略所有中间字符，

因此可以解析各种变体，包括严格的 JSON。





现在回到新的 JSON 配置系统。

设置现在在主配置文件（wireplumber.conf）中的新部分 "wireplumber.settings" 下定义。

这个部分不是作为一个整体定义的，

而是分布在不同的设置文件（*.conf）下，

位于 `wireplumber.conf.d/` 下。

WirePlumber 将在启动时浏览这些文件并将其缝合在一起。



每个 conf 文件是一个设置、模块和脚本的逻辑分组。

例如：以下是 `device.conf` ，其中包含所有设备相关的配置。

```
# Settings to Track/store/restore user choices about devices

wireplumber.settings = {
  # Below syntax defines key-value pair style settings.
  device.use-persistent-storage = true
  device.auto-echo-cancel = true
  device.echo-cancel-sink-name = echo-cancel-sink
  device.echo-cancel-source-name = echo-cancel-source

  # Below syntax defines a rule/condition based settings.
  device.rules = [
    {
      matches = [
          # Matches all devices
          { device.name = "~*" }
      ]
      actions = {
        update-props = {
          profile_names = "off pro-audio"
        }
      }
    }
  ]
}

# WirePlumber modules and scripts are also loaded from the config files.
wireplumber.components = [
  { name = libwireplumber-module-default-nodes , type = module }
  { name = policy-device-profile.lua, type = script/lua }
]
```

为了方便熟悉 Lua 配置的用户，我整理了以下表格，映射了旧的 Lua 配置文件及其对应的新的 JSON 配置文件：

| Old Lua config file 旧的 Lua 配置文件                        | New JSON config file 新 JSON 配置文件 |
| ------------------------------------------------------------ | ------------------------------------- |
| 10-default-policy.lua                                        | policy.conf                           |
| **40-device-defaults.lua, 50-default-access-config.lua 40 ** | device.conf                           |
| 40-stream-defaults.lua                                       | stream.conf                           |
| 20-default-access.lua                                        | access.conf                           |
| **30-alsa-monitor.lua, 50-alsa-config.lua**                  | alsa.conf                             |
| 30-libcamera-monitor.lua, 50-libcamera-config.lua            | libcamera.conf                        |
| 30-v4l2-monitor.lua, 50-v4l2-config.lua                      | v4l2.conf                             |

您可能已经注意到，在某些情况下，两个 Lua 配置文件（如上加粗所示）被合并成一个 JSON 配置文件。

我们希望这将使功能模块化大为简化。

现在让我们来看看这个新的 JSON 配置系统的系统特性和设计，以及客户端功能。



启动时，WirePlumber 从 .conf 文件==加载所有设置到名为 "sm-settings" 的 PipeWire 元数据对象中。==

Lua 脚本、模块和 WirePlumber 客户端可以使用 PipeWire 元数据工具和 API 在运行时更改设置。

正如您可能知道的，这些命令也可以从命令提示符中发出。

```
pw-metadata -n sm-settings 0 "policy.default.move" true Spa:String:JSON
pw-metadata -n sm-settings 0 "device.echo-cancel-source-name" "echo-cancel-source-bal" Spa:String:JSON
```

上述命令不仅在运行时更改设置，而且还会实时应用到 WirePlumber 上，如下面的部分所解释的。



Lua 脚本、模块或 WirePlumber 客户端，

如果对任何设置感兴趣，也可以订阅回调以了解设置的变化。

这使它们不仅能够知道设置的变化，还可以实时应用这些变化。

让我举个例子来强调这一点。

你必须知道，WirePlumber 会保存流的属性（音量、静音状态等）。

现在，你可以使用以下命令关闭此行为的运行时，无需重启/重置。真棒，不是吗？

```
pw-metadata -n sm-settings 0 stream.restore-props false Spa:String:JSON
```



轻松的用户自定义是这次整个操作最方便的结果。

听起来太正式了？

让我把事情放在合适的角度。

比如说，如果一个用户想要自定义 WirePlumber 的流设置。

他们需要复制流配置文件（ `/usr/share/wireplumber/40-stream-defaults.lua` ），更改他们需要的部分，然后将其放置在 `/etc/wireplumber/40-stream-defaults.lua` ，并重新启动 WirePlumber。

WirePlumber 总是加载这个新的配置文件，而忽略默认的配置文件。

那么，如果这个文件在上游发生了变化呢？

在这种情况下，一旦 WirePlumber 升级，用户很可能会遇到麻烦。

今天，override功能在配置文件级别工作。

override将此扩展到单个设置级别。

这意味着用户只能触及他们感兴趣的设置。我们希望这将使分发包构建者的工作更加轻松。

WirePlumber 设置将遵循 PipeWire 和 WirePlumber 配置的其余部分相同的语法。

换句话说，WirePlumber 设置与其他 PipeWire 配置一样。



如果用户/客户端希望在运行时更改设置（使用 pw-metadata，如在动态设置中所解释的），我们建议考虑启用持久行为（或简单地持久性），这样设置更改将被保存到状态文件中，并在重新启动后被记住。



当持久性启用时，设置将仅从配置文件中读取一次，对于后续重启，将从状态文件中初始化。

请注意，持久性默认是禁用的。

可以通过以下设置在 wireplumber.conf 中启用它。

```
wireplumber.settings = {
  persistent.settings = true
}
```



使用 WirePlumber 库构建的客户端现在能够透明地访问 WirePlumber 守护进程当前正在运行的运行时设置。

向您提出另一种可能性，

用户现在可以在 .conf 中添加新的设置，

或者通过 pw-metadata，

并从他们的脚本/模块中开始查询它们，围绕这些设置构建逻辑。

构建这种开发者友好的功能正是我们持续前进的动力。



JSON 设置允许我们针对模式进行验证。这一功能已被考虑在内，但不会包含在新系统的第一版中，因为还需要更多的工作来完成它。

![img](images/random_name2/WirePlumber-JSON-config-17307062606933.jpg)

如您所见，与 Lua 相比，我们不得不构建了大量的基础设施。我个人在这项工作上已经进行了 2-3 个月。我们相信这一切都是值得的，因为上面描述的功能非常丰富。

# WirePlumber 的事件分发器

https://www.collabora.com/news-and-blog/blog/2023/06/15/wireplumber-event-dispatcher-new-simplified-way-handling-pipewire-events/

事件调度器是一种自定义的 PipeWire 事件调度机制，

旨在解决 WirePlumber 中的许多基本问题。

这个想法是由我的同事兼导师乔治·基亚加达基斯提出的，

他是 WirePlumber 的主要作者，我有幸与他合作。

乔治不仅提出了这个想法，

还对核心 WirePlumber 库（libwireplumber）进行了所有更改，以支持这种机制。

当他接近完成核心更改时，他向我们介绍了这个想法。

我立即认识到这个想法的价值，

并很高兴他让我将所有 Lua 脚本和 WirePlumber 模块移植到新的事件分发器。

我们已经在这个项目上工作了将近七个月。

在这个过程中，我移植了所有脚本和模块，并对核心事件分发器做了一些关键的修改。

完成所有这些工作后，我觉得 WirePlumber 已经成熟，现在准备好处理任何实际世界的问题。



PipeWire 保持一组对象的集合，

如设备、节点、端口和链接，

这些对象通过本地 Unix 套接字上的协议进行查询和更新。

尽管协议本身是同步的，

==但在获取或更新对象信息时，往往需要多个连续的协议调用，==

这意味着任何操作可能需要非平凡的时间。

在此期间，其他 PipeWire 客户端也可能查询和/或更新相同的对象，

从单个客户端的角度来看，这会导致并发问题。

为了解决这些问题，WirePlumber 已被设计为==通过异步对象 API 隐藏协议的复杂性==。

然后，该 API 被模块和脚本消费，用于构建与 PipeWire 对象交互的逻辑。



不幸的是，这个 API 有一些限制。

首先，为了接收这些对象、模块和脚本上的事件通知，需要注册回调。

尽管 WirePlumber 是单线程的，

但没有机制保证这些回调执行的顺序。

这意味着需要对相同事件做出反应的不同模块可能会以随机顺序触发。

其次，对任何 PipeWire 对象进行更改会启动异步操作。

通常，这些更改需要在某些事件的响应下进行，但由于存在多个在相同事件上做出反应的回调在不同模块中，因此有可能所有回调都会开始对同一个 PipeWire 对象进行类似的更改，而没有等待彼此完成。

这可能导致操作之间的干扰，引发问题，并需要额外的处理来防止这些问题。



这个问题通过一个例子解释得更好。

考虑一个新的设备（例如，USB 耳机）连接到系统。

然后，ALSA 设备监控器在 PipeWire 上创建一个新的设备对象。

这在 WirePlumber 中表现为一个新的设备添加信号，触发 policy-device-profile.lua 脚本，该脚本选择并设置设备的配置文件。

在同一信号下，另一个脚本（policy-device-routes.lua）启用设备的路由（即子设备路径，如声音卡上的扬声器或耳机）。

然而，路由依赖于配置文件，

因此理想情况下，首先需要选择配置文件。

否则，路由脚本将为初始设备配置文件选择路由，当第一个脚本更改配置文件时，需要重新评估路由。



当配置被选择时，设备监控器开始创建一个或多个节点，

对应于个人输入和输出（例如，扬声器和麦克风）。

这会产生一个或多个新的节点添加信号。

然后，触发 restore-stream.lua 脚本检查节点是否为流，以便恢复之前存储的流属性，如音量、静音状态、通道映射和通道音量。

在同一信号上，module-default-nodes.c 模块重新计算默认输出和输入，

而 create-item.lua 脚本创建一个会话项对象来控制这个节点。



不幸的是，设备监控器不会等待policy-device-profile.lua   脚本选择配置文件，可能会提前为初始设备配置创建节点。

这意味着，在新添加的节点开始执行其逻辑时，节点实际上可能会被销毁和重新创建，导致所有操作都需要再次执行。



最终，当会话项创建时，会触发一个会话项创建信号，

启动 policy-node.lua 脚本重新扫描图，

并可能将一些节点连接在一起（例如，流节点与设备节点）。

此脚本的逻辑取决于已选择的默认接收器和源。

然而，不能保证 module-default-nodes.c 会更早完成其操作，因此需要检查以确保 policy-node.lua 不将流连接到旧的默认接收器或发送器。

可以看到，有很多信号处理器在监听相同的信号并启动可能相互干扰的操作。

这种情况导致了许多竞态条件，

并需要丑陋的补丁作为解决方法（主要策略脚本，policy-node.lua，充满了这些补丁）。

这也导致了代码中的大量冗余，因为在不同的地方进行了类似的检查。

## 优雅的解决方案：事件分发器

为了解决这个问题，我们提出了一种新的方法：事件调度器。

这种新的机制将所有 PipeWire 事件信号转换为事件对象，

并将这些事件对象推入具有预定义优先级编号的优先队列中。

然后根据这些事件的优先级进行分发，从而实现执行顺序的可预测性。



不同于直接在 pipewire 对象上注册回调的先前方法，

现在所有信号处理器都作为挂钩对象实现，

它们会自己向队列中的事件注册。

这些挂钩之间存在依赖关系，这确保了它们执行的顺序也是可预测的。



钩子可能是同步或异步的。

同步意味着它们只包含一个执行任务并立即完成操作的函数。

异步意味着它们包含多个函数，并对可能需要一些时间才能完成操作的对象执行操作。



在任何情况下，事件分发器只允许一次运行一个挂钩。

对于异步挂钩，这意味着在执行另一个挂钩之前，整个操作需要完成。

这确保了操作之间没有干扰。

事件对象是瞬态的，

意味着它们是响应 PipeWire 事件创建的，

它们被放置在优先队列中，并在分发后被销毁，即所有注册的挂钩都已执行。

另一方面，挂钩对象是持久的，意味着它们总是与事件调度器注册，并等待事件。



每个钩子都可以声明对特定事件的兴趣。

当钩子对事件“感兴趣”时，

意味着 Interest 对象上声明的属性与事件的属性相匹配。

当事件被推入队列时，

对这个事件“感兴趣”的钩子被收集到事件对象上的一个列表中，

并根据它们的相互依赖性进行排序。

当事件被分发时，收集到的钩子将按列表中出现的顺序一个接一个地执行。



事件调度器还支持抢占。

允许更高优先级的事件中断并优先于当前正在处理的较低优先级事件。

在事件处理过程中，

一旦特定事件的钩子执行完毕，

事件调度器会检查队列中是否还有更高优先级的事件等待处理。

如果有，事件调度器会切换当前正在处理的事件，开始执行更高优先级事件相关的钩子。



当乔治第一次提出这个想法时，我们花了些时间去理解。

它需要一些思考。

为了帮助你理解这一点，下面的简短视频演示了在常见场景中事件分发器的工作方式：蓝牙自动切换。

在这个场景中，蓝牙耳机已经连接并设置为 A2DP 配置文件，该配置文件具有高质量音频但麦克风被禁用。

然后，用户开始使用 Zoom 通话，需要音频输入。

WirePlumber 然后自动将耳机切换到 HFP 配置文件，该配置文件允许麦克风工作。



事件调度器不仅解决了我们面临的主要问题，

而且还从根本上改变了我们处理 WirePlumber 的 Lua 脚本的方式。

我们现在将每个脚本视为响应事件的挂钩，

这些事件由响应相同事件的不同挂钩执行一系列操作的一部分。

==这使我们能够将 WirePlumber 想象为响应各种事件的挂钩集合，==

对决策和操作产生微小的影响。



我们已经回顾并重新整理了所有主要任务和脚本，

如 restore-stream、default-nodes、policy-node 等，

通过事件调度器的视角审视它们。

在这个过程中，我们有机会对其进行清理，移除大量 hack，

并将其分解为更小、更易于管理的部分。

结果是 Lua 代码模块化、用户可配置，并且易于扩展。

在我的下一篇文章中，我可能会更详细地讨论策略清理的话题。



这是一个挂钩，

它使用之前挂钩选择的默认 sink 或 source，

并通过更新 PipeWire 元数据来应用它。

目前，这个任务由 WirePlumber 模块，module-default-nodes.c 完成，这个模块不太模块化。

```
SimpleEventHook {
  name = "default-nodes/apply-default-node",
  after = { "default-nodes/find-best-default-node",
            "default-nodes/find-echo-cancel-default-node",
            "default-nodes/find-selected-default-node",
            "default-nodes/find-stored-default-node" },
  interests = {
    EventInterest {
      Constraint { "event.type", "=", "select-default-node" },
    },
  },
  execute = function (event)
    local source = event:get_source ()
    local props = event:get_properties ()
    local def_node_type = props ["default-node.type"]
    local selected_node = event:get_data ("selected-node")

    local om = source:call ("get-object-manager", "metadata")
    local metadata = om:lookup { Constraint { "metadata.name", "=", "default" } }

    if selected_node then
      local key = "default." .. def_node_type

      Log.info ("set default node for " .. key .. " " .. selected_node)

      metadata:set (0, key, "Spa:String:JSON",
          Json.Object { ["name"] = selected_node }:to_string ())
    else
      metadata:set (0, "default." .. def_node_type, nil, nil)
    end
  end
}:register ()
```

这是钩子的解剖结构

- 每个钩子都有一个 `name` 。
- 钩子排序（排序）使用 `after` / `before` 标签控制，灵感来源于 systemd，可以列出必须在当前钩子之前或之后执行的其他钩子的名称，分别对应。
- 钩子可以表示其 `interests` 来选择它们响应的事件。 `EventInterest` 表使用与 `WpObjectInterest` API 相同的 API，该 API 也用于 `ObjectManager` 今天。约束不仅限于事件类型，还可以列出导致此事件的对象的属性，允许更复杂的筛选。
- 每个钩子都有一个主体功能，并被赋予指向 `event` 的引用。这是为了简单的（同步）钩子。异步钩子有一个状态机，其主体包含多个函数。
- 每个钩子最终都是一个对象，被 `register` 事件分发器绑定。

审视这个钩子，

想象一下，如果你想影响选择默认接收器的逻辑。而不是编辑现有的脚本，

你可以在自己的 Lua 源文件中编写你的逻辑作为钩子。

添加 `before = "default-nodes/apply-default-node"` 标签和 `after` 标签，列出所有其他上游钩子（如上所示），就完成了！

你的钩子现在将在显示的钩子执行之后，所有其他选择逻辑已经执行完毕，执行。

在主体函数中，你现在有机会在应用到元数据之前改变选择的默认接收器，而无需更改上游的任何代码。

今天，所有这些逻辑都集中在单一的模块（module-default-nodes.c）中，进行这样的干预需要你理解所有内容并进行更改。



# 探索使用事件分发器的 Lua 脚本

这是关于即将发布的 WirePlumber 0.5 版本的一系列博客文章中的第三篇。

前两篇讨论了配置系统重构以及新事件调度器的介绍。

最新的一篇探索了 WirePlumber 的 Lua 脚本如何通过事件调度器进行转换。

WirePlumber lua 脚本通过事件分发器进行转换，

它们看起来和感觉完全不同。

它们更加模块化和可扩展，几乎没有重复处理，

并且几乎没有 hack。

传统上，它们使用对象管理器 API，正如上一篇博客文章中解释的原因，我们已经将它们转移到了事件分发器。

现在，它们是一系列响应适当事件的挂钩。

对于 WirePlumber 的所有系统脚本（如 policy-node.lua，default-nodes，restore-stream，monitor/alsa.lua 等），

您可以在 PipeWire Media Session 项目中找到它们的.c 对应版本。

在 WirePlumber 的初期，我们将这种 C 逻辑翻译成了 Lua；

当然，这是在考虑了 WirePlumber 元素如 Object Manager 的情况下。

但是随着 Event Dispatcher 的出现，它们已经不再是原来的模样。

在本文中，我将分解它们发生了什么变化。



policy-node.lua 是主要的链接脚本。

它就像整个 pipewire 交响乐的指挥，

因此，为了应对任务的复杂性，它能够从一个单一的 lua 源文件中实现如此多的功能。

让我尽量简洁地总结一下它的功能。

它寻找新启动的流，新增的设备，以及用户偏好的变化，

并重新扫描图形，即扫描所有可连接的节点并连接它们，以便媒体开始通过管道流动（而不是 PipeWire :)）。

整个复杂性都从一个单一的文件中处理，即 policy-node.lua 文件，

主要集中在其中的一个单一函数，即 handleLinkable 函数。

让我尝试概述这个函数的功能。

handleLinkable 尝试为给定的流节点（例如 pw-play/pw-cat 客户端节点）找到目标节点；

为此，它首先查找用户首选的目标，然后是默认目标。

如果两者都不可用，它会查找可用目标中最好的一个。

最后，它准备并链接它们，因此代码并不模块化。



再加上，有很多技巧和相当多的冗余处理。

所有 WirePlumber 模块和脚本都注册了对象管理器回调。

有时它们会为同一个回调注册（例如 node-added，default-nodes-changed）。

由于无法控制这些回调执行的顺序，

模块和脚本被迫添加冗余检查和处理。

由于链接脚本处理这种类型的许多通用对象管理器，

它注册了如此多的回调，

因此存在许多这些冗余检查和处理，

例如 scheduleRescan()被多次调用，从代码的不同部分调用。



这段是 WirePlumber 不太令人愉快的部分。

从我之前的工作公司来，

WirePlumber/PipeWire 的代码和设计看起来相当整洁，

但 rescan()的处理方式对我来说难以接受。

它被调用的事件太多，大多数时候函数会空手而归。

也就是说，它没有进行处理，

更糟糕的是，在处理过程中，由于未满足某些条件或出现了需要中止当前处理的新回调，它会在中途退出。

经常，它会自行排队进行重新扫描并退出，这是设计平庸的典型迹象，

因此，当我们有机会自己清理混乱时，感觉更加满足和值得挽回。



有时，链接脚本会在对象管理器回调中改变对象管理器中 Pipewire 对象的属性/状态，

而其他一些脚本可能依赖于相同对象的状态，

因此代码容易出现像这种情况的竞态条件。

解决这些情况的方法是使用 hack。



当我进行了冗余处理时，

一有扫描事件突然触发，

这就是问题的关键。

在事件分发器的帮助下，现在扫描事件被转换为事件，并被赋予最低优先级，这意味着在处理完所有更高优先级的事件后，它才有机会执行，也就是在所有混乱都平息之后。

欢迎查看上一篇博客中的这个视频，以了解它是如何实现的。



因此，Link放到最后才进行，消除了大部分冗余处理。

policy-node.lua被拆分成多个模块。



rescan.lua 对于重新扫描事件注册了一个挂钩，

该事件的优先级最低，

并为特定的源流节点（例如 pw-play/pw-cat 客户端节点）触发一个 `select-target` 事件。

请注意，只有在处理更高优先级事件（如节点添加/移除等）之后才会捕获重新扫描事件。

如果这让你感到困惑，我再次建议你观看视频来理解其中的关联。



select-event 遍历 `find*`钩子，用来选择target。

选择的目标被准备（prepare-link.lua）并最终链接（link-target.lua）。

有三个 find 钩子，

- 第一个（find-defined-target.lua）寻找定义的目标，
- 如果没有定义的目标，第二个钩子出现并检查定义的目标（find-default-target.lua）。
- 如果目标仍然找不到，第三个钩子（find-best-target.lua）帮助选择最佳目标。



所有钩子按照上述顺序运行，

这得益于它们内置的优先级机制。

钩子使用 `before` 和 `after` 标签定义（灵感来源于 systemd）。

对于更详细的钩子解析，请参阅我们之前的博客文章（查找“一个示例钩子”部分）



用户可以通过选择正确的事件

并使用正确的优先级针对此事件注册自定义挂钩，

从而覆盖 WirePlumber 的默认处理方式。

只需在单独的 Lua 源文件中添加这个新挂钩，

然后在 wireplumber.conf 中添加一条记录。

然后，你的挂钩就会被执行，而无需更改任何上游代码的一行。



例如，find-user-target.lua.example 是一个示例挂钩，

展示了如何添加自定义方法来选择链接的目标。

这是一个针对 select-target 事件注册的挂钩，它将是此事件的第一个挂钩运行。



应用相似的推理，剩余的系统脚本，

如默认节点模块、设备配置选择脚本和设备路由选择脚本，也逻辑地分解为重新扫描、查找和应用。



WirePlumber 用户脚本是一些从较小到相当大的 Lua 代码片段，

主要使用对象管理器编写，这里有一大堆示例。

如果你还没有尝试过，你应该试一试，这是一种通过 WirePlumber Lua API 利用 PipeWire 功能非常简单的方法。



这些脚本只需使用 `wpexec` 运行。

另一种方法是将它们复制到 src/scripts 文件夹，

并在 wireplumber.conf 中添加一条记录。

使用 wpexec，它作为单独的进程运行，

在后一种方法中，它作为 WirePlumber 服务的一部分运行。



现在，对于这种使用场景，我们建议继续使用对象管理器。

然而，如果用户对影响 WirePlumber 守护进程逻辑感兴趣，例如链接、默认节点、配置文件、路由等，我们邀请他/她通过事件和挂钩来实现。

借助事件分发器，WirePlumber 可以轻松地被覆盖或扩展。





您可能希望同时向板载和外部设备输出声音，

即使外部设备不总是插在插孔中也是如此。

为了实现这一目标，我们创建了一个虚拟节点，

该节点始终存在，无论插入了什么硬件。

然后，每当它们被插入时，我们将瞬态硬件（例如 USB 耳机）链接到虚拟节点。

首先创建一个脚本，在登录时运行（这通常可以通过您的窗口管理器的启动功能完成）。

/usr/local/sbin/create-virtual-sink.sh

```
#!/bin/bash

# Create a new sink called Simultaneous Output
pw-cli create-node adapter '{ factory.name=support.null-audio-sink node.name="Simultaneous Output" node.description="Simultaneous Output" media.class=Audio/Sink object.linger=true audio.position=[FL FR] }'

# Connect the normal permanent sound card output to the new sink
pw-link "Simultaneous Output:monitor_FL" alsa_output.pci-0000_05_04.0.analog-stereo:playback_FL
pw-link "Simultaneous Output:monitor_FR" alsa_output.pci-0000_05_04.0.analog-stereo:playback_FR

# Switch the default output to the new virtual sink
wpctl set-default `wpctl status | grep "\. Simultaneous Output" | egrep '^ │( )*[0-9]*' -o | cut -c6-55 | egrep -o '[0-9]*'
```

在上述示例中，最初唯一的输出设备是我们普通的内部声卡（alsa_output.pci-0000_05_04.0.analog-stereo）。你可以通过运行 `wpctl status` 和 `wpctl inspect` 来找到你的卡的标识符。

当您的 USB 耳机插入时，运行以下脚本以将它们链接到虚拟接收器：

link-virtual-sink-headphones.sh

```
#!/bin/bash
# link the virtual sync to your headphones should run when detected by UDEV

# wait a second for the drivers to load
sleep 1s

# link the headphones to your virtual sink
sudo -u user1 env XDG_RUNTIME_DIR=/run/user/1000 pw-link "Simultaneous Output:monitor_FL" alsa_output.usb-Kingston_HyperX_Cloud_Flight_S_000000000001-00.analog-stereo:playback_FL
sudo -u user1 env XDG_RUNTIME_DIR=/run/user/1000 pw-link "Simultaneous Output:monitor_FR" alsa_output.usb-Kingston_HyperX_Cloud_Flight_S_000000000001-00.analog-stereo:playback_FR

# finish and return the code for success
exit 0
```

理想情况下，您会在插入耳机时自动运行此脚本。

Udev 页面上的说明描述了如何为此创建自定义规则。

（请注意，您不能直接运行此脚本 - 因为 UDEV 将在指定的脚本运行后才加载驱动程序。因此，您需要有一个中间脚本，使用一些 nohup 技巧或其他类似方法。）

您还需要修改上述脚本，使 XDG_RUNTIME_DIR 与您的用户 ID 号匹配，并将 user1 替换为您的用户名。

# 一些技巧

如果 WirePlumber 的设置被破坏，可以删除所有用户设置：

```
$ systemctl --user stop wireplumber.service
$ rm -r ~/.local/state/wireplumber # deletes settings
$ systemctl --user start wireplumber.service
```



提高音量，上限为 150%：

```
$ wpctl set-volume -l 1.5 @DEFAULT_AUDIO_SINK@ 5%+
```

降低音量：

```
$ wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%-
```

静音/取消静音音量：

```
$ wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle
```

获取默认音轨的音量级别和静音状态：

```
$ wpctl get-volume @DEFAULT_AUDIO_SINK@
```



如果不希望 Pipewire/Wireplumber 接管您的音频设备，

因为您选择了不同的音频解决方案（例如 Pulseaudio/JACK/ALSA），

但仍然希望它用于屏幕共享/视频目的，

您可以使用 `wireplumber@.service` 模板单元来启用不同的默认配置文件集。

Wireplumber 随附的配置文件允许仅启用视频部分，

并通过启用 `video-only` 模板用户单元来禁用音频集成（包括蓝牙音频）。

# libwireplumber-module-reserve-device 作用

`libwireplumber-module-reserve-device` 是 WirePlumber 中的一个模块，

主要用于管理音频设备的**设备预留（device reservation）**功能。

它通过与 **D-Bus** 的 `org.freedesktop.ReserveDevice1` 接口交互，

确保音频设备的独占使用，避免资源冲突。

---

### **主要作用**

| 功能               | 描述                                                         |
| ------------------ | ------------------------------------------------------------ |
| **设备冲突管理**   | 确保当前音频设备不会被其他音频服务器（如 PulseAudio 或其他 PipeWire 实例）占用。如果设备已被占用，则会进行适当的冲突处理。 |
| **独占访问**       | 如果设备已经被 WirePlumber 预留，其他音频服务尝试访问该设备时会收到资源占用错误，从而保证唯一性和设备稳定性。 |
| **D-Bus 接口支持** | 使用 `org.freedesktop.ReserveDevice1` 协议，通过 D-Bus 与其他音频服务协同工作，支持多音频服务同时运行时的资源管理。 |
| **释放与回收机制** | 当音频设备被释放（如停止使用或服务退出）时，自动解除预留状态，让其他服务可以重新使用该设备。 |

---

### **工作原理**

1. **注册设备到 D-Bus**
   - 当 WirePlumber 启动并加载该模块时，它会将音频设备通过 `org.freedesktop.ReserveDevice1` 接口注册到 D-Bus。

2. **检查设备占用状态**
   - 在分配音频资源前，模块会通过 D-Bus 检查目标设备是否已被占用。如果已被其他服务预留，它可以选择等待、竞争或放弃访问。

3. **协调设备使用**
   - 如果设备由 WirePlumber 成功预留，其它服务（如 PulseAudio）将无法直接访问设备，除非设备被释放或服务退出。

---

### **典型使用场景**

1. **PipeWire 与 PulseAudio 共存**
   - 在同时运行 PipeWire 和 PulseAudio 的系统上，避免这两个服务争抢同一个音频设备。

2. **独占硬件资源**
   - 保证某些音频应用（如实时音频处理程序）对特定硬件的独占访问权限。

3. **多实例 PipeWire**
   - 当运行多个 PipeWire 实例时，防止不同实例冲突访问同一设备。

---

### **配置与使用**

该模块通常在 WirePlumber 的默认配置中启用。如果需要手动加载，可以在 WirePlumber 的配置目录中编辑相关文件：

#### **加载模块**
在 `/etc/wireplumber/main.lua.d/` 添加或修改文件（如 `50-reserve.lua`）：

```lua
reserve_device = require("reserve-device")
reserve_device:activate({
    -- 配置选项（可选）
})
```

#### **模块选项**
可以通过配置文件或动态脚本调整模块行为，例如设置等待策略、设备优先级等。

---

### **调试与验证**

1. **检查模块是否加载**
   
   ```bash
   wireplumber -v
   ```
   查看 `libwireplumber-module-reserve-device` 是否在输出中列出。
   
2. **检查设备预留状态**
   使用 `dbus-monitor` 观察 `org.freedesktop.ReserveDevice1` 接口的调用和状态。

3. **测试冲突处理**
   启动 PulseAudio 和 PipeWire，同时尝试访问同一个设备，观察是否有冲突提示。

---

### **总结**

`libwireplumber-module-reserve-device` 主要用于解决多音频服务之间的资源竞争问题，通过 D-Bus 接口实现设备预留与冲突管理，适用于需要独占音频设备的场景。

# wireplumber是怎么跟驱动协商alsa参数的？

WirePlumber 通过与 PipeWire 的协作，利用 ALSA（Advanced Linux Sound Architecture）接口来与驱动进行参数协商。整个流程分为几个主要步骤，包括节点的创建、设备的发现、参数的设置和验证。

以下是详细的协商流程：

---

### **1. 设备发现与初始化**

#### **1.1 ALSA 设备的枚举**
PipeWire 使用 `libalsa` 枚举系统上的音频设备，并为每个设备创建一个 PipeWire 节点。这些节点表示硬件接口，如 `hw:0,0` 或 `hw:1,0`。

- **设备枚举过程：**
  - ALSA PCM 设备通过 `snd_pcm_open()` 打开。
  - 检测设备支持的方向（如播放、录音）。
  - 创建 PipeWire 节点，标识音频设备。

WirePlumber 通过 `alsa-monitor` 脚本配置监听这些节点，并添加必要的规则和属性。

---

### **2. WirePlumber 与 PipeWire 的节点协商**

#### **2.1 配置规则应用**
WirePlumber 的配置文件定义了哪些设备和节点符合规则，并对这些节点应用特定属性。例如：

```lua
alsa_monitor.rules = {
    {
        matches = {
            { "device.name", "matches", "alsa_card.*" },
        },
        apply_properties = {
            ["api.alsa.period-size"] = 256,
            ["api.alsa.format"] = "S16_LE",
            ["api.alsa.rate"] = 48000,
            ["api.alsa.channels"] = 2,
        },
    },
}
```

- **常见属性：**
  - `period-size`：表示每次硬件中断的帧数。
  - `format`：音频数据格式（如 `S16_LE` 表示 16-bit little-endian）。
  - `rate`：采样率。
  - `channels`：通道数量。

WirePlumber 将这些属性通过 PipeWire 传递到 ALSA。

#### **2.2 节点创建与连接**
PipeWire 为每个音频流创建一个客户端节点。WirePlumber 使用 `node` 监听这些节点，动态调整它们的属性。

---

### **3. 参数协商过程**

#### **3.1 参数协商的触发**
当一个音频流需要与硬件交互时（例如播放或录音），PipeWire 向驱动发送 `hw_params` 请求。

- PipeWire 向 ALSA 驱动发送 `snd_pcm_hw_params()`，传递硬件参数。
- ALSA 驱动尝试设置这些参数，如果失败则返回错误。

#### **3.2 参数优化的过程**
PipeWire 可能会根据驱动反馈调整参数，比如减少通道数或降低采样率，直到找到设备支持的配置。

- **典型参数：**
  - **通道数**：通常是单声道（1）、立体声（2），或更多。
  - **采样率**：常见值如 44100Hz、48000Hz 等。
  - **数据格式**：如 `S16_LE`（16-bit）或 `S24_LE`（24-bit）。
  - **缓冲区大小**：如 `1024` 帧。

#### **3.3 参数设置成功**
当驱动接受参数后，PipeWire 完成流的初始化，开始音频数据传输。

---

### **4. 驱动中的协商逻辑**

#### **4.1 驱动如何处理参数**
ALSA 驱动中的 `hw_params` 实现了参数检查和设置：
- **通道数检查**：如 `params_channels(hw_params)`。
- **采样率检查**：如 `params_rate(hw_params)`。
- **格式检查**：如 `params_format(hw_params)`。

如果某个参数不支持，驱动返回 `-EINVAL`，并向日志报告错误。

#### **4.2 特殊硬件支持**
某些驱动可能支持动态参数调整或固定参数。WirePlumber 可以通过配置适配这些驱动。

---

### **5. 调试与问题排查**

#### **5.1 查看PipeWire节点**
使用 `pw-cli` 查看PipeWire节点属性：
```bash
pw-cli dump Node
```

#### **5.2 检查 ALSA 参数**
使用 `pw-dump` 查看配置的 ALSA 参数：
```bash
pw-dump | grep -A10 "alsa"
```

#### **5.3 查看驱动日志**
使用 `dmesg` 检查驱动日志，了解 `hw_params` 错误原因。

---

### **总结**

WirePlumber 通过 PipeWire 与 ALSA 驱动协商参数，依靠配置规则和驱动反馈动态调整硬件参数。驱动在 `hw_params` 阶段对参数进行验证，并可能返回错误。通过调试工具（如 `pw-cli` 和 `dmesg`），可以排查配置问题并优化参数设置。

# src\config\wireplumber.conf.d.examples\alsa.conf

这个值得分析一下。



# device.name = "~alsa_card.*" 这个匹配规则说明



# src\config\wireplumber.conf.d.examples\device.conf 这个文件的作用

`src/config/wireplumber.conf.d.examples/device.conf` 是 WirePlumber 的一个配置文件，用于管理音频设备的通用规则和行为。它的主要作用是定义如何处理设备节点，包括设备的枚举、管理策略以及设备属性的配置。

以下是文件的作用和常见配置的详细说明：

---

### **1. 文件的主要作用**

| 功能                 | 描述                                                         |
| -------------------- | ------------------------------------------------------------ |
| **设备枚举**         | 定义如何匹配和识别设备，例如 ALSA 声卡、蓝牙音频设备等。     |
| **设备属性设置**     | 为设备节点应用属性（如优先级、显示名称、行为策略等）。       |
| **音频路由和优先级** | 设置设备之间的路由策略和优先级，例如扬声器优先于耳机。       |
| **设备管理规则**     | 定义如何启用、禁用或为设备分配资源，例如在特定场景下切换设备。 |

---

### **2. 常见配置结构**

以下是一个典型的 `device.conf` 配置文件结构示例：

```lua
device = {
    -- 定义如何管理设备
    default_profiles = {
        "output:*",      -- 默认输出设备
        "input:*",       -- 默认输入设备
    },
    -- 匹配规则
    rules = {
        -- 规则 1：匹配 ALSA 声卡设备
        {
            matches = {
                { "device.name", "matches", "alsa_card.*" },
            },
            apply_properties = {
                ["priority.session"] = 100,         -- 会话优先级
                ["device.description"] = "ALSA Audio Device",  -- 设备描述
            },
        },
        -- 规则 2：匹配蓝牙音频设备
        {
            matches = {
                { "device.name", "matches", "bluez_card.*" },
            },
            apply_properties = {
                ["priority.session"] = 50,          -- 蓝牙设备优先级较低
                ["device.description"] = "Bluetooth Audio Device",
            },
        },
    },
}
```

---

### **3. 配置的关键部分解析**

#### **3.1 匹配规则 (`matches`)**
匹配 `device.name` 或其他设备属性，用于识别和分类设备。
- **常见匹配字段**：
  - `device.name`：设备名称（如 `alsa_card.pci-0000_00_1f.3`）。
  - `device.bus`：设备总线类型（如 `pci`、`usb`、`bluetooth`）。
  - `device.subsystem`：子系统（如 `sound`）。
  
#### **3.2 属性设置 (`apply_properties`)**
为匹配的设备应用属性，用于调整设备的行为或描述。
- **常见属性**：
  | 属性名称                 | 描述                                     |
  | ------------------------ | ---------------------------------------- |
  | `priority.session`       | 设备优先级，数值越大优先级越高。         |
  | `device.description`     | 设备描述，用于显示在应用程序中。         |
  | `device.disabled`        | 是否禁用设备（`true` 或 `false`）。      |
  | `api.alsa.disable-batch` | 是否禁用批处理模式，仅适用于 ALSA 设备。 |

---

### **4. 配置示例**

#### **4.1 指定某个 ALSA 声卡为默认设备**
```lua
device = {
    rules = {
        {
            matches = {
                { "device.name", "equals", "alsa_card.pci-0000_00_1f.3" }
            },
            apply_properties = {
                ["priority.session"] = 200,  -- 提高优先级，使其成为默认设备
                ["device.description"] = "Preferred Sound Card",
            },
        },
    },
}
```

#### **4.2 禁用特定设备**
```lua
device = {
    rules = {
        {
            matches = {
                { "device.name", "equals", "alsa_card.pci-0000_00_1b.0" },
            },
            apply_properties = {
                ["device.disabled"] = true,  -- 禁用此设备
            },
        },
    },
}
```

#### **4.3 蓝牙设备低优先级**
```lua
device = {
    rules = {
        {
            matches = {
                { "device.name", "matches", "bluez_card.*" }
            },
            apply_properties = {
                ["priority.session"] = 50,   -- 蓝牙设备优先级低于其他设备
            },
        },
    },
}
```

---

### **5. 验证与调试**

1. **重启 WirePlumber 服务**
   ```bash
   systemctl restart wireplumber
   ```

2. **检查设备属性**
   使用 `pw-cli` 或 `pw-dump` 查看设备属性是否正确应用：
   
   ```bash
   pw-dump | grep -A10 "alsa_card"
   ```
   
3. **查看日志**
   使用 `journalctl` 查看 WirePlumber 日志：
   ```bash
   journalctl -u wireplumber -f
   ```

---

### **总结**

`device.conf` 是 WirePlumber 配置设备行为的关键文件。它通过匹配规则定义设备的属性、优先级和管理策略。修改该文件后，可以实现自定义设备的优先级调整、特定设备禁用或参数优化等功能。在调试过程中，可以通过日志和 `pw-cli` 工具验证配置是否正确应用。

# 反转左右声道的配置

~/.config/wireplumber/wireplumber.conf.d/51-flip-stereo.conf

```
monitor.alsa.rules = [
  {
      matches = [
          # Matches all sources.
          { "node.name" = "~alsa_input.*" },
          ## Matches all sinks.
          { "node.name" = "~alsa_output.*" },
      ],
      actions = {
        update-props = {
          audio.channels = 2,
          audio.position = ["FR", "FL"]
        }
      }
  }
]
```

老的lua方式是这样：~/.config/wireplumber/main.lua.d/51-reverse-channels.lua

```
reverse = {
    matches = {
        {
        -- Matches all sources.
        { "node.name", "matches", "alsa_input.*" },
        },
        {
        -- Matches all sinks.
        { "node.name", "matches", "alsa_output.*" },
        },
    },
    apply_properties = {
        ["audio.channels"]         = 2,
        ["audio.position"]         = "FR,FL",
    },
}

table.insert(alsa_monitor.rules, reverse)
```

https://forum.endeavouros.com/t/where-are-pipewire-config/44753/5



# wpctl set-default

```
#!/bin/bash
# Sets the default sound device
# Set space as the delimiter
IFS=' '

# Read the split words into an array based on space delimiter
read -a strarr < <( wpctl status | grep HDMI )
# We will have to check whether our device is already the default; 
# in that case, the ID entry starts with an asterisk.
# As it is complicated in bash to check if a string contains an asterisk (because it is a wildcard character), 
# checking is only done if the first element of the array is alphanumeric or not 
# Hopefully, wireplumber's IDs will always remain two-digit numbers :)
if [[ ${strarr[1]:0:2} = *[^[:alnum:]]* ]]; then
   foundID="${strarr[2]:0:2}"
   else
   foundID="${strarr[1]:0:2}"
fi
wpctl set-default "${foundID}"
```

https://forum.manjaro.org/t/how-do-i-permanently-set-the-default-audio-device-in-manjaro-xfce-with-pipewire/117967/2

现在linux的桌面环境就是这么混乱。

只能这么去设置default 播放设备。

因为id总是会变化。



`wireplumber`忽略我在 中配置的默认音频接收器和源`pipewire`，

而是选择其自己的默认值。

因此，每次重启后，我都必须运行`wpctl status`以找到所需的音频接收器和源的 ID，

然后运行`wpctl set-default`两次以设置正确的接收器和源。

在 中`/usr/local/etc/pipewire/pipewire.conf`，

我有以下配置，

这是我几个月前从 PulseAudio 切换到 PipeWire 时经过一些谷歌搜索后创建的：

```
context.properties = {
[...]
    # default sink & source
    default.audio.sink = "alsa_output.pci-0000_00_1b.0.analog-stereo"
    default.audio.source = "alsa_input.pci-0000_00_1b.0.analog-stereo"
    default.configured.audio.sink = "alsa_output.pci-0000_00_1b.0.analog-stereo"
    default.configured.audio.source = "alsa_input.pci-0000_00_1b.0.analog-stereo"
}
[...]
context.objects = [
[...]
    # Use the metadata factory to create metadata and some default values.
    { factory = metadata
        args = {
            metadata.name = default-metadata
            metadata.values = [
                { key = default.audio.sink   value = { name = "alsa_output.pci-0000_00_1b.0.analog-stereo" } }
                { key = default.audio.source value = { name = "alsa_input.pci-0000_00_1b.0.analog-stereo" } }
                { key = default.configured.audio.sink   value = { name = "alsa_output.pci-0000_00_1b.0.analog-stereo" } }
                { key = default.configured.audio.source value = { name = "alsa_input.pci-0000_00_1b.0.analog-stereo" } }
            ]
        }
    }
]

```

所以我最大的问题是，我该如何告诉`wireplumber`尊重`pipewire`的配置，或者我如何以及在哪里可以配置`wireplumber`选择为“设置 => 默认配置的设备”的内容？

使用 PulseAudio，这就像两行一样简单...

```plaintext
default-sink = alsa_output.pci-0000_00_1b.0.analog-stereo
default-source = alsa_input.pci-0000_00_1b.0.analog-stereo
```

我不知道你在哪里看到这个例子，但它根本就不应该这样工作。没有组件尊重这些设置。

要配置默认接收器和源，您需要编写一些 alsa 监控规则来提高要选择的设备的优先级。

也许是这样的：

```plaintext
monitor.alsa.rules = [
  {
    matches = [
      {
        node.name = "alsa_output.pci-0000_00_1b.0.analog-stereo"
      }
    ]
    actions = {
      update-props = {
        priority.session        = 1500
      }
    }
  }
  {
    matches = [
      {
        node.name = "alsa_input.pci-0000_00_1b.0.analog-stereo"
      }
    ]
    actions = {
      update-props = {
        priority.session        = 2500
      }
    }
  }
]
```

WirePlumber 确实有一个状态，

并且会记住您在运行时使用 wpctl、pactl、pavucontrol、gnome-settings 或类似工具选择默认设备的时间...

为了忘记这个状态，您需要运行`wpctl clear-default`，

然后它会尊重优先级（直到您使用其中一个工具再次手动选择默认设备）



https://gitlab.freedesktop.org/pipewire/wireplumber/-/issues/644



# wireplumber典型场景举例

在 **WirePlumber** 中，新的配置语法基于 **SPA JSON** 格式，而不是之前的 Lua 脚本。以下是使用新的 SPA JSON 语法来实现典型场景的配置示例，包括如何动态管理设备和音频路由。

------

### **场景 1：为蓝牙设备设置优先级**

目标：当蓝牙耳机连接时，优先将音频输出路由到蓝牙耳机。

#### 配置文件路径

SPA JSON 配置通常位于以下路径：

- 系统级：`/usr/share/wireplumber/`
- 用户级：`~/.config/wireplumber/`

#### 配置文件内容

创建或修改文件 `bluez-policy.json`：

```json
{
  "policy": {
    "name": "bluez-priority-policy",
    "description": "Set priority for Bluetooth devices",
    "rules": [
      {
        "matches": [
          { "node.name": "bluez_sink.*" }
        ],
        "actions": [
          { "action": "set-priority", "priority": 100 }
        ]
      },
      {
        "matches": [
          { "node.name": "alsa_output.*" }
        ],
        "actions": [
          { "action": "set-priority", "priority": 50 }
        ]
      }
    ]
  }
}
```

#### 行为说明

- 蓝牙输出节点（`bluez_sink.*`）的优先级设置为 100。
- ALSA 输出节点（`alsa_output.*`）的优先级设置为 50。
- 当蓝牙耳机连接时，WirePlumber 将优先选择蓝牙设备作为音频输出。

------

### **场景 2：自动路由麦克风**

目标：当 USB 麦克风连接时，自动将其设为默认输入设备。

#### 配置文件内容

创建或修改文件 `usb-mic-policy.json`：

```json
{
  "policy": {
    "name": "usb-mic-policy",
    "description": "Automatically route USB microphone",
    "rules": [
      {
        "matches": [
          { "node.name": "alsa_input.usb-*" }
        ],
        "actions": [
          { "action": "set-default", "role": "input" }
        ]
      }
    ]
  }
}
```

#### 行为说明

- 匹配 USB 输入设备（`alsa_input.usb-*`）时，自动将其设为默认输入设备。

------

### **场景 3：阻止特定设备使用**

目标：阻止某个特定的设备被创建或使用。

#### 配置文件内容

创建或修改文件 `block-device-policy.json`：

```json
{
  "policy": {
    "name": "block-device-policy",
    "description": "Block a specific device",
    "rules": [
      {
        "matches": [
          { "node.name": "alsa_output.pci-0000_00_1f.3.*" }
        ],
        "actions": [
          { "action": "block" }
        ]
      }
    ]
  }
}
```

#### 行为说明

- 禁止 PCI 声卡（`alsa_output.pci-0000_00_1f.3.*`）的音频节点被创建。

------

### **场景 4：配置默认音频设备**

目标：设置特定设备为默认输出设备。

#### 配置文件内容

创建或修改文件 `default-device-policy.json`：

```json
{
  "policy": {
    "name": "default-device-policy",
    "description": "Set a default audio output device",
    "rules": [
      {
        "matches": [
          { "node.name": "alsa_output.pci-0000_00_1b.0.*" }
        ],
        "actions": [
          { "action": "set-default", "role": "output" }
        ]
      }
    ]
  }
}
```

#### 行为说明

- 将 PCI 声卡（`alsa_output.pci-0000_00_1b.0.*`）设置为默认输出设备。

------

### **场景 5：定义自定义规则集合**

目标：创建一个完整的路由策略，包括输入、输出和设备优先级。

#### 配置文件内容

创建文件 `custom-policy.json`：

```json
{
  "policy": {
    "name": "custom-policy",
    "description": "Custom audio routing policy",
    "rules": [
      {
        "matches": [
          { "node.name": "bluez_sink.*" }
        ],
        "actions": [
          { "action": "set-priority", "priority": 90 },
          { "action": "set-default", "role": "output" }
        ]
      },
      {
        "matches": [
          { "node.name": "alsa_output.*" }
        ],
        "actions": [
          { "action": "set-priority", "priority": 80 }
        ]
      },
      {
        "matches": [
          { "node.name": "alsa_input.*" }
        ],
        "actions": [
          { "action": "set-default", "role": "input" }
        ]
      }
    ]
  }
}
```

#### 行为说明

- 设置蓝牙设备为默认输出，优先级为 90。
- 设置 ALSA 设备为次优先输出，优先级为 80。
- 设置 ALSA 输入设备为默认输入。

------

### **启用和验证配置**

1. **放置配置文件**： 将 SPA JSON 文件保存到以下路径之一：

   - 系统级：`/usr/share/wireplumber/`
   - 用户级：`~/.config/wireplumber/`

2. **重新加载 WirePlumber**：

   ```bash
   systemctl --user restart wireplumber
   ```

3. **验证规则是否生效**： 使用以下工具检查节点和路由：

   ```bash
   pw-cli dump
   ```

------

### **总结**

- WirePlumber 的 SPA JSON 语法简单直观，便于规则管理。
- 通过定义匹配规则和动作，可以实现自动设备管理、优先级设置等。
- 配置文件的修改无需重新编译，支持动态加载。

# api.lua

其他lua里用到的lua数据结构，都是在这里可以找到定义的。

所以这个需要重点看一下。

然后还有api.c。实现在这个里面。



# wpexec的实际用途举例

`wpexec` 是 WirePlumber 提供的一个命令行工具，主要用于执行与 PipeWire 相关的操作，通常用于调试、测试和管理 WirePlumber 的各种功能。它允许用户在命令行界面中执行与 WirePlumber 配置和操作相关的任务。

### **常见用途和示例**

1. **调试和测试脚本** `wpexec` 允许用户执行 Lua 脚本或其他配置，来测试 WirePlumber 中的各种规则和配置。这个功能对于开发人员在调试自定义的 WirePlumber 配置时非常有用。

   **示例**：运行一个 Lua 脚本来改变音频设备的行为。

   ```bash
   wpexec "some-lua-script.lua"
   ```

2. **配置和应用自定义规则** 通过 `wpexec`，用户可以在不重新启动 WirePlumber 的情况下动态加载和应用自定义的规则（例如音频设备的优先级或特性设置）。

   **示例**：应用一个自定义规则来调整音频设备的优先级。

   ```bash
   wpexec "Rule{
     matches = { {\"node.name\", \"matches\", \"alsa_output.*\"} },
     apply_properties = { [\"node.priority\"] = 1 }
   }"
   ```

3. **查看和操作 WirePlumber 内部对象** `wpexec` 可以用于查看和操作 WirePlumber 中的对象，如设备、节点、链接等。它可以帮助开发人员和管理员在运行时检查和调整对象状态。

   **示例**：列出所有的设备节点。

   ```bash
   wpexec "for node in context:enumerate_nodes() do print(node.name) end"
   ```

4. **动态加载或卸载模块** `wpexec` 还可以用来动态加载或卸载 WirePlumber 中的模块。在调试和测试过程中，这对于验证模块行为或模块之间的交互非常有帮助。

   **示例**：加载一个模块

   ```bash
   wpexec "context:load_module('module-name')"
   ```

5. **交互式操作** `wpexec` 还可以启动一个交互式的 shell，允许用户通过命令行直接与 WirePlumber 进行交互，实时控制和调试系统。

   **示例**：启动交互式 shell

   ```bash
   wpexec --interactive
   ```

------

### **总结**

`wpexec` 是一个非常灵活的工具，通常用于：

- 调试和测试 WirePlumber 配置和规则。
- 动态管理和调整音频设备行为。
- 在没有重启 WirePlumber 的情况下应用更改。

它特别适用于开发人员和高级用户，允许在不重启 WirePlumber 的情况下实时调整和管理系统配置。

# wireplumber里的alsa.lua这些lua脚本，在什么时候被load到内存，在什么时候被触发执行里面的逻辑？

在 WirePlumber 中，`alsa.lua` 这些 Lua 脚本主要用于配置和管理 ALSA 音频设备的相关操作。它们在 WirePlumber 启动时加载，并且在特定条件下执行脚本中的逻辑。

### 加载时机

1. **启动时加载**：`alsa.lua` 脚本会在 WirePlumber 启动时被加载。WirePlumber 会读取其配置目录中的所有 Lua 脚本（包括 `alsa.lua`），并将它们加载到内存中。这些脚本在 WirePlumber 的初始化过程中被解析。
2. **动态加载**：除了启动时加载，WirePlumber 在运行时也会根据需要动态加载和执行其他 Lua 脚本，尤其是在设备管理、音频流控制等相关事件发生时。

### 触发执行时机

1. **设备事件**：当系统中的 ALSA 设备（如音频卡、PCM 设备等）发生变化时，WirePlumber 会触发与这些设备相关的逻辑。比如，当设备被插入或拔出时，脚本中的逻辑会被执行来更新设备状态、配置音频流等。
2. **配置变更**：当 WirePlumber 的配置发生变化（如动态添加或修改音频源、目标设备等）时，`alsa.lua` 脚本中的相关逻辑也会被触发执行。
3. **蓝牙设备相关事件**：对于蓝牙音频设备，脚本中的逻辑可能在蓝牙设备连接、断开时执行，用于更新与 ALSA 相关的配置。

总结来说，`alsa.lua` 脚本在 WirePlumber 启动时加载，并会在 ALSA 设备事件、配置变化或相关的蓝牙设备事件发生时，触发并执行脚本中的逻辑。

# 配置文件层级

WirePlumber 的配置由全局的 PipeWire 风味 JSON 对象 `context` 和 `alsa_monitor` 组成，

这些对象被修改以改变其行为。

配置文件从 `~/.config/wireplumber/` （用户配置）、 `/etc/wireplumber/` （全局配置）和 `/usr/share/wireplumber/` （出厂配置）读取。



WirePlumber 从读取主配置文件开始。

这是一个类似于 JSON 的文件，

用于设置 PipeWire 上下文、SPA 插件、模块和组件。

这些组件中包括 Lua 脚本引擎，用于动态修改全局对象。



wireplumber里的配置项，只有2个是用context开头的。

其余都是wireplumber开头的。

```
wireplumber.profiles 
wireplumber.components 
	这些组件在连接到pipewire的时候创建。
wireplumber.components.rules
wireplumber.settings.schema
```



# 蓝牙配置

# 注册的gobject类型

就这7个。

```
  g_type_ensure (WP_TYPE_CLIENT);
  g_type_ensure (WP_TYPE_DEVICE);
  g_type_ensure (WP_TYPE_LINK);
  g_type_ensure (WP_TYPE_METADATA);
  g_type_ensure (WP_TYPE_NODE);
  g_type_ensure (WP_TYPE_PORT);
  g_type_ensure (WP_TYPE_FACTORY);
```

# wp_transition 

`WpTransition` 是 WirePlumber 中的一个结构，

主要用于表示异步操作中的过渡过程。

它是一个状态机，每个过渡（transition）包含一系列的步骤，

这些步骤按顺序执行，直到操作完成。

### 主要概念

1. **异步操作**：`WpTransition` 作为一个异步任务，涉及到一系列的“步骤”来完成一个操作。每个步骤可能会启动一个异步操作，并且在操作完成后会触发相应的回调。
2. **步骤和状态机**：每个步骤的执行通过 `WpTransitionClass::get_next_step()` 方法决定下一个要执行的步骤。`WpTransitionClass::execute_step()` 方法则用于执行当前步骤所需的操作。当步骤完成后，`wp_transition_advance()` 被调用以推进到下一个步骤。
3. **错误处理**：如果在任何步骤中发生错误，代码应调用 `wp_transition_return_error()`，以便立即结束过渡操作，并通过 `wp_transition_had_error()` 检查是否发生了错误。
4. **完成状态**：过渡的完成由 `completed` 属性表示，当过渡的最后一步完成或发生错误时，`completed` 属性会被设置为 `TRUE`。这意味着过渡操作已经完成，无论是成功还是失败。此属性只会从 `FALSE` 变为 `TRUE` 一次。

### 属性（`GProperties`）

- completed

   (

  ```
  gboolean
  ```

  )：

  - 该属性表示过渡操作是否已完成。
  - 当过渡操作的最后一步完成，或者调用 `wp_transition_return_error()` 时，`completed` 会被设置为 `TRUE`。
  - 该属性的值从 `FALSE` 变为 `TRUE` 只会发生一次。
  - `GObject` 的 `notify` 信号会在回调被调用后立即触发。

### 工作流程

1. `WpTransition` 会通过多个步骤逐步执行操作。
2. 每个步骤通常会启动一个异步操作。异步操作完成后，步骤会调用 `wp_transition_advance()` 来继续下一个步骤。
3. 如果出现错误，操作会通过 `wp_transition_return_error()` 终止。
4. 通过监控 `completed` 属性的变化，可以知道操作是否已完成。

### 总结

`WpTransition` 是 WirePlumber 中用于管理复杂异步操作的机制，通过一系列步骤和状态机来控制异步任务的执行。这种设计使得 WirePlumber 可以顺序且可靠地执行操作，确保每个操作在步骤之间的过渡顺利进行，并且能够处理可能出现的错误。

#  lua脚本里的ObjectManager

在 **WirePlumber** 的 Lua 脚本中，`ObjectManager` 是一个核心组件，

负责管理与 PipeWire 节点和对象的交互。

它的主要功能是跟踪和管理特定类型的 PipeWire 对象（如设备、节点、端口等），

并为这些对象提供便捷的查询、监听和操作方法。

### **基本功能**

`ObjectManager` 的用途：

- **发现对象：** 根据指定的规则发现 PipeWire 中的对象。
- **监听对象变化：** 当对象被添加、删除或其属性发生变化时触发事件。
- **过滤对象：** 通过设置规则只管理符合条件的对象。

------

### **创建和使用 `ObjectManager`**

#### 1. **创建 `ObjectManager`**

使用 `ObjectManager` 通常需要在 Lua 脚本中创建实例，并指定需要跟踪的对象类型和规则：

```lua
local ObjectManager = require("wireplumber").ObjectManager

-- 创建 ObjectManager 实例
local om = ObjectManager {
  interest = {
    type = "node",          -- 对象类型，例如 node, device, port 等
    Constraint {           -- 属性约束
      "media.class", "matches", "Audio/Sink"  -- 示例：只匹配音频输出设备
    }
  }
}
```

------

#### 2. **启动 `ObjectManager`**

初始化 `ObjectManager` 并使其开始工作：

```lua
om:activate()  -- 激活管理器
```

------

#### 3. **获取对象**

通过 `ObjectManager` 的方法获取已发现的对象列表：

```lua
-- 获取所有符合条件的对象
local objects = om:get_objects()
for _, obj in ipairs(objects) do
  print("Found object: " .. obj.properties["node.name"])
end

-- 获取单个对象
local obj = om:lookup {
  Constraint { "node.name", "matches", "my-audio-node" }
}
if obj then
  print("Found specific object: " .. obj.properties["node.name"])
end
```

------

### **监听对象事件**

通过监听对象事件来处理动态变化：

```lua
-- 监听对象添加事件
om:connect("object-added", function (om, obj)
  print("Object added: " .. obj.properties["node.name"])
end)

-- 监听对象删除事件
om:connect("object-removed", function (om, obj)
  print("Object removed: " .. obj.properties["node.name"])
end)
```

------

### **完整示例：跟踪音频输出设备**

以下是一个简单脚本，跟踪所有音频输出设备的添加和移除：

```lua
local ObjectManager = require("wireplumber").ObjectManager

local om = ObjectManager {
  interest = {
    type = "node",
    Constraint { "media.class", "matches", "Audio/Sink" }
  }
}

om:connect("object-added", function (om, obj)
  print("Audio sink added: " .. obj.properties["node.name"])
end)

om:connect("object-removed", function (om, obj)
  print("Audio sink removed: " .. obj.properties["node.name"])
end)

om:activate()
```

------

### **常用方法**

| 方法名                         | 功能                                 |
| ------------------------------ | ------------------------------------ |
| `om:activate()`                | 激活 `ObjectManager`，开始发现对象。 |
| `om:get_objects()`             | 获取所有符合条件的对象。             |
| `om:lookup(criteria)`          | 根据条件查找特定对象。               |
| `om:connect(signal, callback)` | 监听对象的事件，如添加、移除等。     |

------

### **注意事项**

1. **性能问题：** 如果管理大量对象，确保设置合理的过滤条件以降低开销。
2. **调试输出：** 使用 `obj.properties` 查看对象的所有属性。
3. **事件处理：** 避免在事件回调中执行耗时操作，以免阻塞 PipeWire 的主循环。

如果有更具体的应用场景需求，可以告诉我进一步优化代码！

# 搜索lua的顺序

```
T 00:04:20.905284       wp-base-dirs ../lib/wp/base-dirs.c:171:wp_base_dirs_find_file: test file: /.local/share/wireplumber/scripts/sm-objects.lua
T 00:04:20.905369       wp-base-dirs ../lib/wp/base-dirs.c:171:wp_base_dirs_find_file: test file: /usr/local/share/wireplumber/scripts/sm-objects.lua
T 00:04:20.905437       wp-base-dirs ../lib/wp/base-dirs.c:171:wp_base_dirs_find_file: test file: /usr/share/wireplumber/scripts/sm-objects.lua
```

/.local/share/wireplumber/scripts/sm-objects.lua

注意这个路径。这个就是自定义的lua脚本推荐的位置。

# wp_transition_advance 这个是做什么的？

`wp_transition_advance` 是 WirePlumber 的 C API 中用于管理状态机（State Machine）中的状态转换的一个函数。在 WirePlumber 的模块化架构中，状态机用于表示和管理复杂任务的各个阶段，通过状态的切换来逐步完成任务。

------

### **功能和用途**

- **推进状态：** `wp_transition_advance` 的主要作用是将状态机从当前状态推进到下一个状态。
- **触发回调：** 每次状态变化时，都会触发相应的回调函数（如果设置了回调）。
- **完成任务：** 当所有状态都完成后，状态机会自动完成并清理资源。

------

### **典型使用场景**

状态机在 WirePlumber 中用于管理异步任务，比如设备初始化、资源分配或模块加载。

------

### **函数原型**

```c
void wp_transition_advance(WpTransition *transition);
```

| 参数         | 描述                                 |
| ------------ | ------------------------------------ |
| `transition` | 当前的状态机实例（`WpTransition`）。 |

------

### **工作原理**

1. **创建状态机：** 状态机由 `wp_transition_new()` 创建，并与某个对象关联。
2. **定义各个状态：** 在状态机的实现中，需要定义任务的各个阶段。
3. **推进状态：** 调用 `wp_transition_advance()` 将状态推进到下一个阶段。
4. **完成状态机：** 当所有状态完成时，状态机会自动标记为完成，或者调用 `wp_object_abort()` 以手动终止。

------

### **示例代码**

以下是一个使用状态机完成简单任务的示例：

```c
#include <wireplumber/wireplumber.h>

typedef struct {
  WpTransition parent;
  int step;
} MyTransition;

static void
my_transition_execute_step (WpTransition * transition)
{
  MyTransition *self = (MyTransition *) transition;

  if (self->step == 0) {
    g_print ("Step 0: Initializing\n");
    self->step++;
    wp_transition_advance (transition); // 推进到下一步
  }
  else if (self->step == 1) {
    g_print ("Step 1: Processing\n");
    self->step++;
    wp_transition_advance (transition); // 推进到下一步
  }
  else {
    g_print ("Step 2: Finalizing\n");
    wp_transition_return (transition, WP_TRANSITION_SUCCESS); // 完成状态机
  }
}

static void
start_my_transition (WpObject * obj)
{
  MyTransition *trans = g_object_new (MY_TYPE_TRANSITION, NULL);
  wp_object_set_transition (obj, (WpTransition *) trans);
  wp_transition_advance ((WpTransition *) trans); // 启动状态机
}
```

------

### **关键函数**

| 函数名                       | 描述                                 |
| ---------------------------- | ------------------------------------ |
| `wp_transition_advance()`    | 推进状态机到下一个状态。             |
| `wp_transition_return()`     | 设置状态机的完成状态（成功或失败）。 |
| `wp_object_set_transition()` | 为对象关联一个状态机。               |
| `wp_object_abort()`          | 手动中止状态机并标记为失败。         |

------

### **注意事项**

1. **避免死循环：** 每次推进状态时，确保状态机逻辑最终能完成。
2. **异步操作：** 如果某些状态涉及异步任务，确保任务完成后再调用 `wp_transition_advance()`。
3. **调试：** 使用日志跟踪状态变化，方便调试复杂任务的执行流程。

如果需要更详细的示例或应用场景解释，请告诉我！



# wpctl执行时的日志

```
loaded config '/usr/share/pipewire/client.conf'
```

# 加载自定义lua

```
~/.config/wireplumber/wireplumber.conf.d/99-my-script.conf
```

内容：

```
wireplumber.components = [
  {
    name = my-script.lua, type = script/lua
    provides = custom.my-script
  }
]

wireplumber.profiles = {
  main = {
    custom.my-script = required
  }
}
```

创建/etc/wireplumber/scripts 这个目录。

把my-script放进去。



# wireplumber.profiles

这个里面的feature name，其实就是下面的wireplumber.components里的那些provides。

```
  {
    name = ensure-no-media-session, type = built-in
    provides = check.no-media-session
  }
```



# 原理

PipeWire 会话管理器是一个承担很多任务的工具。

很多人将“会话管理器”理解为一个负责管理节点间连接的工具，

但这只是它众多任务之一。

要理解它的全部运作方式，

我们需要首先讨论 PipeWire 是如何工作的。



当 PipeWire 启动时，它会加载其配置文件中定义的一组模块。

这些模块为 PipeWire 提供功能，

否则它只是一个空进程不做任何事情。

在正常情况下，

PipeWire 启动时加载的模块包含对象工厂，

以及允许进程间通信的原生协议模块。

除此之外，PipeWire 并不会加载或执行其他操作。

这是会话管理开始的地方。



会话管理基本上是设置 PipeWire 使其做一些有用的事情。

这通过利用 PipeWire 暴露的对象工厂来创建一些有用的对象来实现，

然后通过操作它们的方法来修改并稍后销毁它们。

这样的对象包括设备、节点、端口、链接等。

这是一个需要持续监控和采取行动的任务，

需要对系统使用过程中发生的大量不同事件做出反应。

## 会话管理逻辑划分

WirePlumber 中的会话管理逻辑分为 6 个不同的操作区域：

###  设备启用 

启用设备是基本的操作领域。

这通过使用device monitor来实现，

这些对象通常作为 SPA 插件在 PipeWire 中实现，

但由 WirePlumber 加载。

它们的任务是发现可用的媒体设备并在 PipeWire 中创建对象，

以提供与这些设备交互的方式。

### 设备配置

大多数设备从计算机的角度来看会暴露复杂的功能，

为了提供简单流畅的用户体验，

这些功能需要被管理。

例如，音频设备被组织成不同的配置文件和路径，这样可以设置它们以满足特定的使用场景。

这些配置和管理需要由会话管理器来完成。

### client access control

就是权限管理。

### node config

节点是媒体处理的基本元素。

它们通常由设备监视器或客户端应用程序创建。

创建后，节点处于无法链接的状态。

链接它们需要一些配置，

例如配置媒体格式，随后是应暴露的端口数量和类型。

此外，根据用户偏好，可能还需要设置与节点相关的某些属性和元数据。

所有这些都由会话管理器处理。

### link 管理

当节点最终可以使用时，

会话管理器还需要决定它们应该如何连接，

以便媒体能够流过。

例如，音频播放流节点很可能需要连接到默认音频输出设备节点。

然后，会话管理器还需要创建所有这些连接，

并监控所有可能影响它们的条件，

以便在某些事情发生变化时（例如，如果设备断开连接）可以进行动态重新连接。

在某些情况下，由于创建或销毁连接，设备和节点的配置也可能需要更改。

### metadata管理

在运行时，PipeWire 和 WirePlumber 都会在这些对象之外的存储中存储一些==关于对象及其操作的额外属性==。

这些属性被称为“元数据”，

并存储在“元数据对象”中。

这些元数据可以通过 pw-metadata 等工具外部更改，也可以通过其他工具更改。

在某些情况下，这些元数据需要与会话管理器内的逻辑进行交互。

==最明显的是，选择默认的音频和视频输入输出是通过设置元数据来完成的。==

会话管理器随后需要验证这些信息、存储它们并在下次重启时恢复它们，

同时还要确保在动态插入和拔出设备时，默认的输入输出仍然有效和合理。





## libwireplumber

WirePlumber 建立在 libwireplumber 库之上，

该库提供了表达所有会话管理逻辑的基本构建块。

libwireplumber 是用 C 语言编写的，

并基于 GObject，

它封装了 PipeWire API，

并提供了一个更高层次且更方便的 API。

虽然 WirePlumber 服务实现会话管理逻辑，

但底层库也可以在 WirePlumber 服务之外被利用。

这允许创建与 PipeWire 交互的外部工具和 GUI。



PipeWire 通过 IPC 协议暴露了多个对象，

如节点和端口，

==但使用标准面向对象原则与之交互较为困难，==

==因为它是异步的。==

例如，当一个对象被创建时，它的存在会在协议中宣布，但其属性会在后续的次要消息中宣布。

如果需要对这个对象创建事件做出反应，

通常需要访问对象的属性，

因此必须等待属性被发送。

虽然这样做听起来很简单，而且确实如此，

但在所有地方重复进行这种操作而不是专注于编写实际的事件处理逻辑，会变得繁琐。



WirePlumber 的库通过

为每个对象在其生命周期中缓存

从 PipeWire 接收到的所有信息和更新来创建代理对象，

然后通过 WpObjectManager API 使这些信息可用，

该 API 能够在宣布这些信息（例如，属性）之前等待每个对象上的相关信息（例如，属性）已被缓存。



还提供一套用于会话管理的工具。

例如，它提供了 WpSessionItem 类，

可以用于抽象图的一部分并附加一些逻辑。

它还提供了事件与挂钩 API，这是一种以声明方式表达事件处理逻辑的方法。



还提供一套杂项工具，

用于桥接 PipeWire API 和 GObject API，

例如 WpProperties、WpSpaPod、WpSpaJson 等。

这些工具补充了对象模型，使得与 PipeWire 对象的交互更加容易。



WirePlumber 守护进程是在库 API 的基础上实现的，

它的任务是托管实现会话管理逻辑的组件。

本身它除了加载和激活这些组件之外不做其他事情。

实际的逻辑是它们内部实现的。

模块化设计确保可以无需重新实现其余部分就替换特定功能的实现，

从而在目标敏感部分，

如策略管理以及使用非标准硬件方面提供灵活性。

# events和hooks

会话管理就是应对事件并采取必要行动。

因此，WirePlumber 的逻辑全部建立在事件和挂钩之上。

每个事件都有一个source、一个subject和一些property，这些属性包括事件类型。

* `source` 是指创建此事件的 GObject。通常，这指的是 `WpStandardEventSource` 插件。

* `subject` 是可选的目标引用，指本次事件的对象。例如，在一个 `node-added` 事件中， `subject` 将引用刚刚添加的 `WpNode` 对象。一些事件，尤其是仅用于触发动作的事件，没有subject
* `properties` 是一个字典，包含事件信息，包括事件类型，如果存在的话，还包含所有 `subject` 的 PipeWire 属性。
* `event.type` 属性描述事件的性质，例如 `node-added` 或 `metadata-changed` 是一些有效的事件类型。



每个事件也有优先级。

优先级较高的事件会在优先级较低的事件之前被处理。

当两个或两个以上的事件具有相同的优先级时，

它们将按照先进先出的方式处理。

这种逻辑由事件分发器定义。



钩子是代表需要在处理某个事件时执行的可运行动作的对象。

因此，每个钩子都包含一个可以执行的同步或异步函数，

并且每个钩子都有方法将其与特定事件关联起来。

这通常通过声明对特定事件属性或它们的组合的兴趣来实现。

有两大类钩子: `SimpleEventHook` 和 `AsyncEventHook` 。

每个钩子也有一个名称，

可以是任意字符组成的字符串。

此外，它还有两个名字数组，用来声明这个钩子与其他钩子之间的依赖关系。

一个数组称为 `before` ，

另一个称为 `after` 。

 `before` 数组中的钩子名称表示这个钩子必须在那些其他钩子之前执行。

同样， `after` 数组中的钩子名称表示这个钩子必须在那些其他钩子之后执行。

通过这种方式，可以定义在特定事件中钩子的执行顺序。



钩子是长期存在的对象。

它们一旦创建就会被注册到事件分发器中，

附加在事件上并在执行后解除附加。

**钩子不维护任何内部状态，因此钩子的动作完全依赖于事件本身。**



# link policy

WirePlumber 的链接策略负责将 PipeWire 流节点与 PipeWire 设备节点链接（大多数情况），或与其他 PipeWire 流节点链接（监控应用程序）。

PipeWire 流节点始终具有以下之一的媒体类：

* Stream/Output/Audio，例如pw-play
* Stream/Input/Audio，例如pw-record
* Stream/Input/Video:

Pipewire 设备节点总是具有以下之一的媒体类：

* Audio/Sink，例如喇叭。
* Audio/Source，例如mic。
* Video/Source，例如摄像头。

默认情况下，因为我们通常希望将一个流节点与一个设备节点链接起来，

所以在链接两个节点时的链接策略逻辑总是遵循以下分配：

![image-20241231162306714](images/random_name2/image-20241231162306714.png)

之后，一旦为某个流节点选择了一个设备节点的媒体类，

并且有多个设备节点匹配此类媒体类，

WirePlumber 将根据一组优先级选择其中一个：

首先，它会检查是否为所选设备媒体类配置了默认设备节点。

如果有，并且该节点存在，它将把流节点与这样配置的默认节点链接起来。

用户可以使用 `pavucontrol` 或 `wpctl` 等工具为所有 3 种不同的设备媒体类轻松配置默认设备节点。

逻辑实现于 `linking/find-default-target.lua` Lua 脚本中。

如果没有配置默认节点，

或者虽然配置了默认节点但该节点不存在，

WirePlumber 将选择可用的最佳设备节点。

最佳设备节点是具有最高会话优先级且能够到达物理设备的节点。

逻辑实现于 `linking/find-best-target.lua` Lua 脚本中。

如果找不到最优节点，因为系统中没有合适的节点，WirePlumber 将不会链接该流，并向客户端发送“没有可用的目标节点”错误。

## stream node的属性

```
target.object
	stream输出的目标。pw-play --target 设置的就是这个。
node.dont-reconnect
	就是当现在的target断开时，是否自动连接到下一个可用的node。
node.dont-move
node.dont-fallback
node.linger

```

# filter

作为示例，我们将描述如何在 PipeWire 的配置中创建 2 个回环过滤器，

命名为 loopback-1 和 loopback-2，

并将它们与默认音频设备链接，

且使用 loopback-2 过滤器作为链中的最后一个过滤器。

The PipeWire 配置文件对于 2 个过滤器应该像这样：

pipewire.conf.d/loopback-1.conf:

```
context.modules = [
    {   name = libpipewire-module-loopback
        args = {
            node.name = loopback-1-sink
            node.description = "Loopback 1 Sink"
            capture.props = {
                audio.position = [ FL FR ]
                media.class = Audio/Sink
                filter.smart = true
                filter.smart.name = loopback-1
                filter.smart.before = [ loopback-2 ]
            }
            playback.props = {
                audio.position = [ FL FR ]
                node.passive = true
                node.dont-remix = true
            }
        }
    }
]
```

pipewire.conf.d/loopback-2.conf:

```
context.modules = [
    {   name = libpipewire-module-loopback
        args = {
            node.name = loopback-2-sink
            node.description = "Loopback 2 Sink"
            capture.props = {
                audio.position = [ FL FR ]
                media.class = Audio/Sink
                filter.smart = true
                filter.smart.name = loopback-2
            }
            playback.props = {
                audio.position = [ FL FR ]
                node.passive = true
                node.dont-remix = true
            }
        }
    }
]
```

![image-20241231163745201](images/random_name2/image-20241231163745201.png)



# lua

所有的 GObject 都有属性。在 C 语言中我们通常使用 g_object_get 来获取它们，使用 g_object_set 来设置它们。

在 WirePlumber 的 lua 引擎中，这些属性作为 Lua 对象的成员被暴露出来。

GObjects 也有一个通用机制将事件传递给外部回调。这些事件称为信号。要连接到信号并处理它，您可以使用 connect 方法：

# wireplumber的一些新特性

https://www.collabora.com/news-and-blog/blog/2024/02/19/whats-the-latest-with-wireplumber/

我关于 WirePlumber 保持沉默已经有一段时间了。这还要追溯到 2022 年，当时在其设计中发现了一系列问题，我决定重新构建其部分基础，以便让它能够成长。我在那时的这篇帖子中提到了这一点。而长话短说，现在已经是 2024 年了（时间过得真快，谁知道呢？！）。



设计中的主要限制因素是 WirePlumber 最强大的功能：脚本系统。

当我们设计脚本系统时，

假设如果提供一个 API，

允许脚本获取 PipeWire 对象的引用并独立订阅其事件，

那么任何功能都可以轻松构建在其上。

这完全错了，

因为实际情况是，基于脚本构建的组件实际上相互依赖，

有时确保事件处理程序（回调）执行顺序是至关重要的。

此外，我们还意识到编写相对较小的脚本很困难。

大量的逻辑很快就在单个脚本文件中积累起来，使它们很难使用。

这也使得用户无法在不首先复制整个脚本的情况下稍微修改某些行为变得不可能。



解决方案是用不同的方式重做脚本系统。

不再让脚本随意行事，

我们引入了一个中央组件来管理所有 PipeWire 对象的引用，

即“标准事件源”。

此外，我们还增加了一种机制，

让脚本能够通过我们称之为“钩子”的其他对象订阅这些对象的事件。

钩子之间可以有依赖关系，

从而可以排序，并且它们之间可以传递数据，允许它们合作做出决策而不是彼此竞争。

![scripting system old new](images/random_name2/scripting-system-old-new.png)



这是革命性的修改。

在使用这个系统一段时间，并将旧的脚本转换为使用 hooks 之后，一切都变得干净多了，也更容易操作。



在这个过程中，我们还意识到可以引入不源自 PipeWire 对象的虚拟事件，以便运行挂钩链以做出决策。

例如，选择哪个“sink”节点将成为系统的默认音频输出的过程

是通过一个名为“select-default-node”的虚拟事件实现的。

这个事件是在一个响应多个事件的挂钩中生成的，

这些事件可以被解释为潜在的 sink 改变。

当事件生成时，收集可用的 sink 节点及其属性列表，并将其作为事件数据传递给“select-default-node”挂钩。

之后，每个挂钩都会遍历这个列表，并根据一些启发式规则尝试做出决策。

如果挂钩做出了决策，它会将所选节点及其优先级存储在事件数据中。

然后，链条中的下一个挂钩从这里开始，做出自己的决策，

但如果优先级低于之前的优先级，则不会改变结果。

![scripting system default](images/random_name2/scripting-system-default-nodes.png)



正如你可以看出，

这个系统使得用户能够用最少的努力覆盖默认逻辑。

例如，在上面选择默认“sink”的钩子示例中，

用户可以添加一个自定义脚本，

该脚本还对“select-default-node”事件作出反应，

并在现有的钩子链中的特定位置链接，

使用钩子依赖关系。

然后，该钩子可以引入选择默认“sink”的自定义逻辑，并以更高的优先级存储，以覆盖其他钩子做出的决定。

有趣的是，它并不总是需要存储结果；

完全可以在不采取任何行动的情况下返回，并让现有的上游钩子自己做出决定，从而使自定义钩子的逻辑尽可能简单。



有了合适的基础设施，我相信 WirePlumber 现在比以往任何时候都更有条件成长。

首先，即使过了这么长时间，仍然有一些很有意义的功能缺失。

例如，其中一个功能就是能够遵循类似于 JACK 的规则将任意端口连接起来。

迄今为止，WirePlumber 的连接策略是在节点上操作，并在节点之间进行连接操作，而不是端口。

还有一个组件会自动发现这些节点的端口，并一一将它们连接起来。

由于现有的策略是在节点上操作，因此这种功能很容易产生冲突，

但有了新的钩子系统，我相信它们可以协同工作。

另一个重要的缺失功能是适当的访问控制。

我们的访问控制脚本甚至还没有移植到钩子系统中，

所以这是首先要采取的行动。

但更重要的是，依我看来，WirePlumber 需要有机制来维护对象组和客户端组，并确保每次注册表发生变化时，这些对象的权限位能够保持最新状态。

分组将允许我们构建访问控制规则，类似于文件系统中用户组的工作方式。

# xx-api.c

```
./modules/module-file-monitor-api.c
./modules/module-default-nodes-api.c
./modules/module-mixer-api.c
```

有这3个文件是以xx-api.c规律结尾的。

API 插件是提供某些 API 扩展以在脚本中使用的插件。这些插件的名字必须总是以“-api”结尾，这里指定的名字不能包含“-api”扩展。

```
Core.require_api("mixer", function(mixer)
```

那这里取值就只能是mixer、default-nodes、file-monitor这3个了。

# 一个lua脚本可以被多次加载

```
  ## Provide the "default" pw_metadata
  {
    name = metadata.lua, type = script/lua
    arguments = { metadata.name = default }
    provides = metadata.default
  }

  ## Provide the "filters" pw_metadata
  {
    name = metadata.lua, type = script/lua
    arguments = { metadata.name = filters }
    provides = metadata.filters
  }
```

# 我通过WIREPLUMBER_DEBUG=5打开wireplumber的debug时，会导致pipewire的debug同时被打开，怎样只打开wireplumber的debug？

```
export WIREPLUMBER_DEBUG="E,pw.*:E,spa.*:E,mod.*:E,T"
wireplumber
```

这样就可以。

字符串的解读是：

```
第一个E，表示所有的默认都是E。
逗号是分隔符。
最后的T是剩下的。
```



查找conf文件是顺序。

```
test file: /var/wireplumber/wireplumber.conf
test file: /etc/xdg/wireplumber/wireplumber.conf
test file: /etc/wireplumber/wireplumber.conf
lookup 'wireplumber.conf', return: 
```

```
opening fragment file: /usr/share/wireplumber/wireplumber.conf.d/alsa-vm.conf
opening fragment file: /etc/wireplumber/wireplumber.conf.d/10-alsa-disable-scan.conf
```

解析conf文件

```
section 'context.properties' is not defined
section 'context.spa-libs' is used as-is from '/etc/wireplumber/wireplumber.conf'
section 'context.modules' is used as-is from '/etc/wireplumber/wireplumber.conf'


parsed 6 context.spa-libs items
loaded module libpipewire-module-rt
loaded module libpipewire-module-protocol-native
loaded module libpipewire-module-metadata

wp_feature_activation_transition_get_next_step

wp_registry_attach
这里注册了几十个这样的对象。
registry_global: <WpCore:0x1738988> global:34 perm:0x1c8 type:PipeWire:Interface:Client/3 -> WpClient

然后进入下一个大步骤：STEP_LOAD_COMPONENTS
I 11:05:04.533256            wp-core ../lib/wp/core.c:544:wp_core_activate_execute_step: <WpCore:0x1738988> parsing & loading components for profile [main]...

```



以loading component进行搜索。一共有81处。

```
lib/wp/private/internal-comp-loader.c
664:  { "settings-instance", load_settings_instance },

built-in的就这3个。
  { "ensure-no-media-session", ensure_no_media_session },
  { "export-core", load_export_core },
  { "settings-instance", load_settings_instance },
};
```

ensure_no_media_session

```
这个函数检查系统中是否正在运行`pipewire-media-session`。
它创建一个`WpObjectManager`对象，
设置一个回调函数，当`pipewire-media-session`被安装时触发。
如果`pipewire-media-session`正在运行，函数会返回一个错误。
```

这里指定了wireplumber在metadata里的设置的名字。就是sm-settings

```
{
    name = settings-instance, type = built-in
    arguments = { metadata.name = sm-settings }
    provides = support.settings
  }
```

lua虚拟机的初始化

```
modules\module-lua-scripting\module.c
wp_lua_scripting_plugin_enable函数
	self->L = wplua_new ();
```

这个函数`wplua_new`用于创建一个新的Lua状态机（`lua_State`）。

它首先检查是否已经注册了资源，

如果没有，则注册资源。

然后，它初始化Lua状态机，打开标准库，初始化一些GObject和闭包相关的函数。

最后，它创建一个哈希表并将其存储在Lua注册表中，并设置引用计数为1。

函数返回创建的Lua状态机。

io禁用就是没有加载io库。

![image-20250102201011489](images/random_name2/image-20250102201011489.png)

# execute_step在什么时候执行？

lib/wp/transition.c里被调用。

wp_transition_advance函数里。

空闲时会通过这里调用。

```
wp_core_idle_add (core, &priv->idle_advnc_source,
        G_SOURCE_FUNC (wp_object_advance_transitions), g_object_ref (self),
        g_object_unref);
```



idle_advnc_source是每个WpObject都有的属性。

```
struct _WpObjectPrivate
{
  /* properties */
  guint id;
  GWeakRef core;

  /* features state */
  WpObjectFeatures ft_active;
  GQueue *transitions; // element-type: WpFeatureActivationTransition*
  GSource *idle_advnc_source;
  GWeakRef ongoing_transition;
};
```

wp_object_update_features 这个函数看起来是更新object的状态的。

![image-20250102192224421](images/random_name2/image-20250102192224421.png)



这个函数wp_object_update_features用于更新对象的活跃特性。

它接受三个参数：self（对象本身）、activated（新激活的特性）和deactivated（刚刚被停用的特性）。

函数首先检查对象的类型是否正确，

然后更新对象的活跃特性。

接着，如果活跃特性发生了变化，函数会发送一个通知。

最后，如果有正在进行的转换或队列中有待处理的转换，函数会添加一个空闲回调函数来推进转换。



step枚举有这些：

```
typedef enum {
  /*! the initial and final step of the transition */
  WP_TRANSITION_STEP_NONE = 0,
  /*! returned by _WpTransitionClass::get_next_step() in case of an error */
  WP_TRANSITION_STEP_ERROR,
  /*! starting value for steps defined in subclasses */
  WP_TRANSITION_STEP_CUSTOM_START = 0x10
} WpTransitionStep;
```

每个object内部自己从WP_TRANSITION_STEP_CUSTOM_START开始去定义自己的。

例如core.c的。

```
enum {
  STEP_CONNECT = WP_TRANSITION_STEP_CUSTOM_START,
  STEP_LOAD_COMPONENTS,
};
```

core的它有2个状态。

1、connect。

2、load Component。



# wp_metadata_set

这个函数用于设置元数据（metadata）对象的属性值。

它接受五个参数：

元数据对象自身、

主题ID、

键、

类型

值。

通过设置键和值，可以添加或更新元数据属性；

设置键或值为NULL，可以删除对应的元数据属性；

同时设置键和值为NULL，可以删除主题ID对应的所有元数据属性。

# C代码里的ObjectManager

```
WpObjectManager *om = wp_object_manager_new ();

添加感兴趣的事件
  wp_object_manager_add_interest (om, WP_TYPE_CLIENT,
      WP_CONSTRAINT_TYPE_PW_GLOBAL_PROPERTY,
      "application.name", "=s", "pipewire-media-session", NULL);
  g_signal_connect_object (om, "installed",
      G_CALLBACK (ensure_no_media_session_om_installed), task, 0);
  wp_core_install_object_manager (core, om);
```



# _wplua_init_gboxed

这个函数 `_wplua_init_gboxed` 初始化了一个 Lua 元表（metatable）叫做 "GBoxed"。

这个元表包含三个函数：

`__gc`（垃圾回收）、`__eq`（相等比较）和 `__index`（索引访问）。

这些函数分别对应 `_wplua_gvalue_userdata___gc`、 `_wplua_gvalue_userdata___eq` 和 `_wplua_gboxed___index` 函数。

# _wplua_init_gobject

这个代码片段是用于初始化Lua中的GObject元表（metatable）。它定义了GObject元表中的几个元方法（metamethod），包括：

*   `__gc`：垃圾回收函数
*   `__eq`：相等判断函数
*   `__index`：索引函数，用于获取GObject的属性
*   `__newindex`：新索引函数，用于设置GObject的属性
*   `__tostring`：转换为字符串函数

这些元方法将被注册到名为"GObject"的元表中，并将被用于处理GObject类型的Lua对象。

# _wplua_init_closure

这个函数 `_wplua_init_closure` 的作用是在 Lua 的全局注册表中创建一个名为 "wplua_closures" 的键值对。值是通过 `_wplua_closure_store_new` 函数创建的 `WpLuaClosureStore` 类型的实例，并使用 `wplua_pushboxed` 函数将其推入 Lua 栈中。

# wp_lua_scripting_api_init

这段代码是一个C函数，名为`wp_lua_scripting_api_init`，它接受一个`lua_State *`类型的参数`L`。

该函数的主要功能是初始化Lua脚本的API。它创建了一个新的Lua状态`L`，并设置了一些全局变量，例如`GLib`、`I18n`、`WpLog`、`WpCore`、`WpPlugin`等。

然后，它调用了一些其他的函数来注册不同类型的对象的方法，例如`G_TYPE_SOURCE`、`WP_TYPE_OBJECT`、`WP_TYPE_PROXY`等。

最后，它加载了一个名为`URI_API`的Lua脚本，并执行它。如果加载或执行脚本时出现错误，它会打印一个错误消息。

总的来说，这段代码的目的是为了初始化Lua脚本的API，使得Lua脚本可以访问和操作一些常用的对象和函数。

# autoswitch-bluetooth-profile.lua

这个 Lua 脚本用于自动切换蓝牙设备的配置文件。

它监控蓝牙设备和音频流的状态，

当音频流连接到==蓝牙设备的回环源节点==时，

自动切换设备的配置文件到 HSP/HFP 模式；

当音频流断开连接时，

自动切换设备的配置文件回 A2DP 模式。

脚本使用 WirePlumber 框架来管理蓝牙设备和音频流。

# device.api

只有bluez5这一种情况：

Constraint { "device.api", "=", "bluez5" },



# Constraint types

| type      | value                                                        |
| --------- | ------------------------------------------------------------ |
| pw-global | [`WP_CONSTRAINT_TYPE_PW_GLOBAL_PROPERTY`](https://julian.pages.freedesktop.org/wireplumber/library/c_api/obj_interest_api.html#c.WpConstraintType.WP_CONSTRAINT_TYPE_PW_GLOBAL_PROPERTY) |
| pw        | [`WP_CONSTRAINT_TYPE_PW_PROPERTY`](https://julian.pages.freedesktop.org/wireplumber/library/c_api/obj_interest_api.html#c.WpConstraintType.WP_CONSTRAINT_TYPE_PW_PROPERTY) |
| gobject   | [`WP_CONSTRAINT_TYPE_G_PROPERTY`](https://julian.pages.freedesktop.org/wireplumber/library/c_api/obj_interest_api.html#c.WpConstraintType.WP_CONSTRAINT_TYPE_G_PROPERTY) |

# apply-profile

是在选择得到profile之后。

```
  after = { "device/find-stored-profile", "device/find-preferred-profile", "device/find-best-profile" },

```

选择是顺序是：

* 先看文件里存储的。
* 再看优先的。
* 再选择最合适的。

然后一步成功了，后面的就不执行。

# session-item怎么理解

session-item是 high level对象，用来包装下面的pipewire对象。

并且管理它们。

例如，一个session-item可以管理一个node，

负责配置node的PortConfig和Format param。

也可以管理2个node之间的link。

session_item_configure 对应lua的configure，只有这里调用了。

```
src/scripts/node/create-item.lua
100:        -- configure item
101:        if not item:configure (configProperties (node)) then
102:          transition:return_error ("failed to configure item for node "
```



# 蓝牙连接时create device

是靠bluez.lua里的逻辑来完成的。



# linking-utils.lua

总共300行代码。

整个文件是形成一个table。lutils

里面有一个子table。si_flags。



```
get_flags
	参数是id。拿到id对应的flag。
clear_flags
	
unwrap_select_target_event
	解包event。
canPassthrough
	检查两个节点（si和si_target）是否可以进行直接传递（passthrough）
checkFollowDefault
	检查是否需要忽略节点属性中的默认目标设置。
lookupLink
	在对象管理器中查找两个会话项（si_id 和 si_target_id）之间的链接。
isLinked
	检查目标是否已链接，并返回链接状态和是否为独占链接。
getNodePeerId
canLink
findDefaultLinkable
checkPassthroughCompatibility
haveAvailableRoutes
sendClientError

```

checkFollowDefault这种驼峰的函数，区别是它的第一个参数不是self。

所以是通过点号来调用，而不是冒号。



本节中的钩子分为3个子类别。

第一类

包括由图中的更改触发的钩子。

其中一些是任务 安排“重新扫描链接”事件，

这是优先级最低的事件，

并且 它的目的是扫描所有可链接的会话项目

并将它们链接起来 到特定目标。

“重新扫描链接”事件始终计划运行 一个循环中   所有的图形变化一次。

这是通过标记事件来实现的 如module-standard-event-source中已经安排的那样；

然后清除此标志 通过在此事件上运行的钩子。



# 在监听到蓝牙device和node出现后，进行link的操作

在 **WirePlumber** 中，监听蓝牙设备和节点的出现后，自动创建 `link` 的流程如下。以下代码演示了如何监听设备和节点事件，并在满足条件时进行 `link` 的操作。

------

### 核心思路

1. **监听蓝牙设备与节点事件**：
   - 利用 WirePlumber 的 Lua API 监听设备和节点的创建事件。
2. **判断设备类型**：
   - 检查是否是蓝牙设备（通过设备名称、媒体角色等属性判断）。
3. **创建 `link`**：
   - 确认合适的 `source` 和 `sink` 节点后，创建链接。

------

### 实现步骤

以下代码示例监听到蓝牙设备的出现后，查找相应的 `Node`，并创建 `link`：

#### 1. 脚本代码

```lua
-- Import core object
local core = Core("core")

-- Table to store found nodes
local bluetooth_nodes = {}

-- Function to create link between nodes
local function create_link(source_id, sink_id)
    local link = pw.Link {
        ["link.output.node"] = source_id,
        ["link.input.node"] = sink_id,
    }

    link:connect() -- Connect the link
    print("Created link between source node " .. source_id .. " and sink node " .. sink_id)
end

-- Function to handle new nodes
local function handle_new_node(node)
    local props = node.properties
    if props and props["device.api"] == "bluez5" then
        print("Bluetooth Node Detected: " .. props["node.description"])
        table.insert(bluetooth_nodes, node)

        -- Check if source and sink nodes exist
        if #bluetooth_nodes >= 2 then
            local source = bluetooth_nodes[1].id
            local sink = bluetooth_nodes[2].id
            create_link(source, sink)
        end
    end
end

-- Monitor for new nodes
core:connect()

core:connect_signal("object-added", function(_, obj)
    if obj.type == "pw.Node" then
        handle_new_node(obj)
    end
end)

print("Listening for Bluetooth nodes...")
```

------

#### 2. 代码解析

| 功能                  | 说明                                                         |
| --------------------- | ------------------------------------------------------------ |
| `core:connect_signal` | 监听 `object-added` 事件，当新对象（如 `Node`）被添加时触发。 |
| `props["device.api"]` | 检查设备类型是否为蓝牙 (`bluez5`)。                          |
| `create_link`         | 使用 `pw.Link` 对象创建音频流的链接。                        |
| `table.insert`        | 将发现的蓝牙节点存储到 `bluetooth_nodes` 表中。              |

------

### 测试方法

1. **脚本加载**：

   - 将脚本保存为 `bluetooth_link.lua` 并放置到 WirePlumber 的 `scripts` 目录。

2. **启用脚本**：

   - 修改 

     ```
     main.lua
     ```

     ：

     ```lua
     script.load("bluetooth_link.lua")
     ```

3. **启动服务并观察日志**：

   - 重启 WirePlumber：

     ```bash
     systemctl --user restart wireplumber
     ```

   - 查看日志：

     ```bash
     journalctl --user -u wireplumber -f
     ```

4. **连接蓝牙设备**：

   - 连接蓝牙耳机或音频设备，观察是否创建 `link`。

------

### 注意事项

1. **确保蓝牙支持**：
   - PipeWire 已正确配置 `bluez5` 支持。
2. **检查蓝牙节点属性**：
   - 使用 `pw-cli` 确认节点的 `device.api` 和 `node.description`。
3. **错误处理**：
   - 添加异常处理，避免设备缺失或节点未完全初始化导致的错误。

------

如果需要进一步扩展，比如对特定设备做匹配或动态移除 `link`，可以继续调整代码逻辑！

# script_finish_activation

这个函数是 Lua 脚本中 `Script.finish_activation` 函数的实现。

它的作用是通知 WirePlumber 插件脚本已经完成激活过程，并更新插件的状态。

# lua里定时

```
tags = {}

function checkpoint(x)
  log:warning("xhl -- Loading my script "..x)
  table.insert(tags, x)
end

Core.timeout_add(100, function()
  checkpoint("timeout1")
  return false
end)

Core.timeout_add(200, function()
  checkpoint("timeout2")
  return false
end)

Core.timeout_add(300, function()
  checkpoint("timeout3")
  assert(#tags == 3)
  assert(tags[1] == "timeout1")
  assert(tags[2] == "timeout2")
  assert(tags[3] == "timeout3")
  return false
end)

```

# GObject Integration

### GObject Integration (Lua API) 总结

WirePlumber 的脚本引擎通过 Lua 提供了对 **GObject** 的直接集成。

该页面详细描述了如何在 Lua 脚本中操作 GObject，

包括属性、信号、方法调用以及类型转换。

以下是该页面内容的总结：

---

### 1. **GObject 属性 (Properties)**

GObject 的属性在 Lua 中被当作对象成员来访问和修改：

- **读取属性**：  
  使用类似表的语法读取属性值。
  
  ```lua
  local proxy = function_that_returns_a_wp_proxy()
  local proxy_id = proxy["bound-id"]
  print("Bound ID: " .. proxy_id)
  ```
  
- **设置属性**：  
  直接通过赋值修改可写属性。
  ```lua
  local mixer = ...
  mixer["scale"] = "cubic" -- 设置属性为枚举值 "cubic"
  ```

---

### 2. **GObject 信号 (Signals)**

GObject 使用**信号**机制向外部回调发送事件：

- **连接信号**：  
  使用 `connect` 方法连接信号到回调函数。
  
  ```lua
  proxy:connect("bound", function(p, id)
    print("Proxy " .. tostring(p) .. " bound to " .. tostring(id))
  end)
  ```
  - `connect` 的参数：
    - `signal_name`：信号名称，例如 `"signal-name::detail"`。
    - `callback`：信号触发时调用的 Lua 函数。
  
- **调用动作信号 (Action Signals)**：  
  使用 `call` 方法调用动作信号。
  
  ```lua
  local id = default_nodes:call("get-default-node", "Audio/Sink")
  local volume = mixer:call("get-volume", id)
  Debug.dump_table(volume)
  ```
  - `call` 方法的返回值由信号提供。

---

### 3. **类型转换 (Type Conversions)**

在 Lua 和 C/GObject 之间，脚本引擎自动完成数据类型的转换：

#### C 到 Lua 的转换：
| **C 类型**               | **Lua 类型**             |
| ------------------------ | ------------------------ |
| `gchar`, `gint`, `guint` | `integer`                |
| `gfloat`, `gdouble`      | `number`                 |
| `gboolean`               | `boolean`                |
| `gchar*`                 | `string`                 |
| `WpProperties*`          | `table` (键值对)         |
| `GVariant*`              | Lua 原生类型（递归转换） |

#### Lua 到 C 的转换：
| **Lua 类型** | **C 类型**                           |
| ------------ | ------------------------------------ |
| `integer`    | `gint`, `guint`, `gint64`            |
| `number`     | `gfloat`, `gdouble`                  |
| `boolean`    | `gboolean`                           |
| `string`     | `gchar*`                             |
| `table`      | `WpProperties*`, `GVariant` 字典类型 |

#### GVariant 转换：
- **从 GVariant 到 Lua**：支持递归转换，包括字典和数组。
- **从 Lua 到 GVariant**：Lua 表被转换为字典 (`a{sv}`)，整数键会被转为字符串。

---

### 4. **闭包 (Closures)**

Lua 函数可以作为 GClosure 传递到 C 函数中，脚本引擎会自动包装。GClosure 被销毁时，Lua 的引用也会被释放。

**注意**：  
Lua 引擎停止时，所有由该引擎创建的 GClosure 都会被无效化。

---

### 5. **引用计数 (Reference Counting)**

- Lua 中 GObject 的引用由底层的 GObject 引用计数机制管理。
- Lua 引用计数管理的是绑定的 `userdata` 对象，而非底层的 GObject 本身。

**示例：**

```lua
local obj = FooObject() -- 创建一个 GObject 实例
obj = nil -- 释放 Lua 引用，GObject 最终被销毁
```

**注意事项**：
- 当 Lua 的垃圾收集器未运行时，`nil` 并不会立即销毁对象。
- **循环引用风险**：闭包引用 GObject 的局部变量可能导致内存泄漏。

**示例 (危险用法)：**

```lua
local om = ObjectManager(...)
om:connect("objects-changed", function(obj_mgr)
  for obj in om:iterate() do
    do_stuff(obj)
  end
end)
om = nil -- ObjectManager 被闭包引用，无法释放
```

---

### 主要用途

GObject 集成允许开发者通过 Lua 脚本动态配置和管理 WirePlumber 的行为，支持以下功能：
- 操作 GObject 属性和信号。
- 与 C 插件和 API 交互。
- 动态实现会话管理和音频路由逻辑。

---

### 总结

该文档提供了深入的技术细节，帮助开发者利用 WirePlumber 的 Lua 脚本功能来高效管理音频会话。通过对 GObject 的集成，开发者能够以更直观的方式操作底层的 PipeWire 功能模块。

# constraint

这是一个枚举类型的定义，用于指定约束类型。它定义了四种约束类型：

*   `WP_CONSTRAINT_TYPE_NONE`：无效的约束类型
*   `WP_CONSTRAINT_TYPE_PW_GLOBAL_PROPERTY`：约束应用于对象的PipeWire全局属性
*   `WP_CONSTRAINT_TYPE_PW_PROPERTY`：约束应用于对象的PipeWire属性
*   `WP_CONSTRAINT_TYPE_G_PROPERTY`：约束应用于对象的GObject属性

# core api

该网页是 **WirePlumber 0.5.7 文档**中关于 **Lua Core API** 的部分，主要描述了 **Core API** 提供的功能，用于在 Lua 脚本中与 WirePlumber 核心进行交互。以下是内容的总结：

---

### **核心概述**
- **`WpCore` API**：  
  Core 对象本身并未直接暴露给 Lua 脚本，但通过一组静态函数可以访问核心功能。
- 主要功能包括：获取核心属性和信息、事件调度、同步、加载 API 插件、测试功能等。

---

### **暴露的函数**

1. **`Core.get_properties()`**  
   - 获取核心的属性。  
   - 返回一个表（Lua 表），包含 WirePlumber 的客户端对象在 PipeWire 全局注册表中的属性。  
   - **返回值类型**：`table`。

2. **`Core.get_info()`**  
   - 获取核心的信息。  
   - 返回一个表，包含以下字段：
     - `cookie`：远程会话的标识符。
     - `name`：远程核心的名称。
     - `user_name`：远程用户的名称。
     - `host_name`：远程主机的名称。
     - `version`：远程 WirePlumber 的版本。
     - `properties`：远程核心的属性。
   - **返回值类型**：`table`。

3. **`Core.idle_add(callback)`**  
   - 在事件循环空闲时调用指定的 `callback` 函数。  
   - **参数**：  
     - `callback`：回调函数（返回值为 `true` 继续调用，`false` 停止调用）。  
   - **返回值类型**：`GSource`（可通过 `GSource.destroy()` 停止回调）。

4. **`Core.timeout_add(timeout_ms, callback)`**  
   - 在指定的 `timeout_ms` 毫秒后调用 `callback` 函数。  
   - **参数**：  
     - `timeout_ms`：超时时间（毫秒）。  
     - `callback`：回调函数（返回值为 `true` 继续调用，`false` 停止调用）。  
   - **返回值类型**：`GSource`（可通过 `GSource.destroy()` 停止回调）。

5. **`GSource.destroy(self)`**  
   - 用于销毁由 `Core.idle_add()` 或 `Core.timeout_add()` 返回的 `GSource` 对象，停止回调执行。

6. **`Core.sync(callback)`**  
   - 与 PipeWire 同步事务状态后执行回调函数。  
   - **参数**：  
     - `callback`：同步完成后调用的函数，接收一个参数（错误消息字符串或 `nil`）用于指示同步是否出错。

7. **`Core.quit()`**  
   - 退出当前的 `wpexec` 进程。  
   - **注意**：仅在脚本运行于 `wpexec` 环境中有效，在主 WirePlumber 守护进程中会仅打印警告且无效。

8. **`Core.require_api(..., callback)`**  
   - 加载指定的 API 插件并运行回调函数。  
   - **参数**：  
     - `...`：API 插件名称列表（不包含 `-api` 后缀）。  
     - `callback`：插件加载完成后调用的函数，接收插件引用作为参数。  
   - **注意**：仅在脚本运行于 `wpexec` 环境中有效。

9. **`Core.test_feature(feature)`**  
   - 测试当前 WirePlumber 配置是否提供指定功能。  
   - **参数**：  
     - `feature`：功能名称（字符串）。  
   - **返回值类型**：`boolean`（`true` 表示功能存在，`false` 表示不存在）。

---

### **附加说明**
- **事件调度相关**：  
  - `Core.idle_add()` 和 `Core.timeout_add()` 返回的 `GSource` 对象可以通过 `GSource.destroy()` 停止回调，适用于停止重复执行的操作或中止闲置任务。
  
- **API 插件加载**：  
  - `Core.require_api()` 用于动态加载扩展 API（如 `mixer-api`），加载完成后可以通过回调函数调用插件功能。

- **同步与退出**：  
  - `Core.sync()` 用于确保脚本与 PipeWire 的同步状态一致。  
  - `Core.quit()` 用于退出运行的 `wpexec` 脚本，但在主守护进程中无效。

---

### **适用场景**
- **脚本化的核心操作**：  
  提供核心属性、信息的查询和操作功能，适合动态管理 WirePlumber 的运行状态。
- **事件驱动的编程**：  
  通过 `idle_add` 和 `timeout_add` 实现基于事件循环的编程，适用于处理异步任务。
- **扩展功能管理**：  
  支持动态加载 API 插件，增强 WirePlumber 脚本的功能。

# log api

### Debug Logging — WirePlumber 0.5.7 概述

WirePlumber 0.5.7 文档中的调试日志部分提供了一系列用于记录日志的方法和构造函数，主要用于脚本开发。

#### 主要内容

1. **构造函数**
   
   - **`Log.open_topic(topic)`**: 打开一个日志主题。主题的名称作为参数传入，返回一个日志主题对象。
   
   **示例代码**:
   ```lua
   local obj_log = Log.open_topic("s-linking")
   obj_log:info(obj, "an info message on obj")
   obj_log:debug("a debug message")
   ```
   
2. **日志方法**
   - **`Log.warning(object, message)`**: 记录警告消息。
   - **`Log.notice(object, message)`**: 记录通知消息。
   - **`Log.info(object, message)`**: 记录信息消息。
   - **`Log.debug(object, message)`**: 记录调试消息。
   - **`Log.trace(object, message)`**: 记录跟踪消息。

   每个方法的参数可以选择性地包含一个对象和一条消息。

3. **调试工具**
   - **`Debug.dump_table(t)`**: 将表的所有内容递归打印到标准输出，用于调试目的。

#### 使用示例

通过这些方法，开发者可以有效地记录和管理脚本中的日志，帮助调试和监控程序的运行状态。

### 结论

WirePlumber 的调试日志 API 为开发者提供了强大的工具来记录和管理日志信息，有助于在开发和维护过程中更好地理解程序的行为。

# Object Manager

### Object Manager — WirePlumber 0.5.7 概述

WirePlumber 0.5.7 文档中的对象管理器部分提供了一个用于管理和监控对象的 API，允许开发者收集符合特定条件的对象，并在这些对象被创建或销毁时接收通知。

#### 主要内容

1. **构造函数**
   - **`ObjectManager(interest_list)`**: 构造一个新的对象管理器，接受一个包含一个或多个兴趣对象的表作为参数。对象管理器将管理所有匹配指定兴趣的对象。

   **示例代码**:
   
   ```lua
   streams_om = ObjectManager {
       Interest {
           type = "node",
           Constraint { "media.class", "matches", "Stream/*", type = "pw-global" },
       },
       Interest {
           type = "node",
           Constraint { "media.class", "matches", "Audio/*", type = "pw-global" },
           Constraint { "device.routes", "equals", "0", type = "pw" },
       },
   }
   ```
   
2. **方法**
   - **`ObjectManager.activate(self)`**: 激活对象管理器，并使预先存在的符合兴趣的对象可用。
   - **`ObjectManager.get_n_objects(self)`**: 返回对象管理器管理的对象数量。
   - **`ObjectManager.iterate(self, interest)`**: 返回所有符合指定兴趣的管理对象的迭代器。
   - **`ObjectManager.lookup(self, interest)`**: 查找并返回第一个符合兴趣的管理对象。

#### 使用示例

开发者可通过这些方法灵活地管理对象，处理对象的创建和销毁，并根据需求进行过滤和查找。

### 结论

WirePlumber 的对象管理器 API 为开发者提供了强大的工具来管理和监控对象，有助于在复杂的音频和视频处理场景中实现高效的资源管理。

# interest



### Object Interest — WirePlumber 0.5.7 详细概述

#### 1. **介绍**
`Interest` 对象用于声明对特定对象或对象集合的兴趣，并提供过滤功能。这在 `ObjectManager` 中被广泛使用，同时也适用于其他需要遍历或查找特定对象的方法。

#### 2. **构造**
- **`Interest(decl)`**: 用于创建 `Interest` 对象。参数为一个包含兴趣声明的表。兴趣由 GType 和一组约束组成。

  **示例**:
  
  ```lua
  local om = ObjectManager {
      Interest {
          type = "node",
          Constraint {
              "node.name", "matches", "alsa*",
              type = "pw-global"
          },
          Constraint {
              "media.class", "equals", "Audio/Sink",
              type = "pw-global"
          },
      }
  }
  ```

#### 3. **兴趣的组成**
- **GType**: 兴趣的类型，指定要匹配的对象类型（如节点、设备等）。
- **约束**: 约束是一个包含属性名、操作符及其值的表。约束通过严格的顺序定义。

#### 4. **约束**
- **构造**: 约束同样通过表构造，必须包括：
  - **属性名**（subject）: 要匹配的属性的名称。
  - **操作符**（verb）: 匹配操作，如 `equals`、`matches` 等。
  - **值**（object）: 操作符所需的值。

  **操作符示例**:
  - `equals` (`=`)
  - `not-equals` (`!`)
  - `in-list` (`c`)
  - `in-range` (`~`)
  - `matches` (`#`)
  - `is-present` (`+`)
  - `is-absent` (`-`)

#### 5. **约束类型**
- 约束可以指定应用于的属性列表类型：
  - `pw-global`: 全局属性
  - `pw`: PipeWire 属性
  - `gobject`: GObject 属性

  **示例约束**:
  ```lua
  Constraint {
      "node.id", "equals", 42, type = "pw-global"
  }
  ```

#### 6. **方法**
- **`Interest.matches(self, obj)`**: 检查特定对象是否与兴趣匹配。可以接受 GObject 或可转换为 `WpProperties` 的表。

  **返回值**: 布尔值，指示对象是否匹配兴趣。

#### 7. **使用示例**
开发者可以通过 `Interest` 对象和约束灵活地管理对象。例如，可以在 `ObjectManager` 中使用兴趣对象来匹配特定类型的音频节点或设备。

# PipeWire Proxies

### PipeWire Proxies — WirePlumber 0.5.7 概述

WirePlumber 0.5.7 文档中的“PipeWire Proxies”部分介绍了与 PipeWire 对象交互的 Lua API，包括代理、节点、端口、客户端和元数据的操作。

#### 主要内容

1. **Proxy**
   - `Proxy` 对象提供了与 `WpProxy` 绑定的方法。
   - **方法**:
     - **`get_interface_type(self)`**: 获取代理类型及其版本。

2. **PipeWire Object**
   - `PipewireObject` 绑定了 `WpPipewireObject`，允许操作 PipeWire 对象。
   - **方法**:
     - **`iterate_params(self, param_name)`**: 枚举指定的参数。
     - **`set_param(self, param_name, pod)`**: 设置指定的参数为新的值。

3. **Global Proxy**
   - `GlobalProxy` 绑定了 `WpGlobalProxy`。
   - **方法**:
     - **`request_destroy(self)`**: 请求销毁该全局代理。

4. **PipeWire Node**
   - `Node` 绑定了 `WpNode`，用于管理节点相关操作。
   - **方法**:
     - **`get_state(self)`**: 获取节点的当前状态。
     - **`get_n_input_ports(self)`**: 获取输入端口的数量。
     - **`get_n_output_ports(self)`**: 获取输出端口的数量。
     - **`iterate_ports(self, interest)`**: 迭代匹配兴趣的端口。
     - **`lookup_port(self, interest)`**: 查找匹配兴趣的端口。
     - **`send_command(self, command)`**: 向节点发送命令。

5. **PipeWire Port**
   - `Port` 绑定了 `WpPort`，用于管理端口。
   - **方法**:
     - **`get_direction(self)`**: 获取端口的方向。

6. **PipeWire Client**
   - `Client` 绑定了 `WpClient`，用于管理客户端操作。
   - **方法**:
     - **`update_permissions(self, perms)`**: 更新客户端权限。

7. **PipeWire Metadata**
   - `Metadata` 绑定了 `WpMetadata`，用于管理元数据。
   - **方法**:
     - **`iterate(self, subject)`**: 创建元数据迭代器。
     - **`find(self, subject, key)`**: 查找指定键的元数据值。

### 结论
WirePlumber 的 PipeWire Proxies API 提供了丰富的功能以与 PipeWire 对象进行交互，支持节点、端口、客户端及元数据的管理，极大地增强了音频和视频处理的灵活性与控制能力。

# default node

### Default Nodes Scripts — WirePlumber 0.5.7 概述

WirePlumber 0.5.7 文档中的“Default Nodes Scripts”部分介绍了用于选择默认音频源和音频接收节点的脚本，及其用户偏好的管理。

#### 主要内容

1. **脚本功能**
   - 这些脚本负责扫描所有可用节点并根据特定逻辑为其分配优先级。每个类别中优先级最高的节点将被设置为默认节点。

2. **钩子机制**
   - 通过“rescan-for-default-nodes”事件实现节点的重新扫描。
   - **钩子**:
     - **`default-nodes/rescan-trigger`**: 监控图形变化并调度“rescan-for-default-nodes”。
     - **`default-nodes/rescan`**: 在“rescan-for-default-nodes”事件触发时，推送“select-default-node”事件，用于每个需要默认节点的类别（音频接收、音频源、视频源）。

3. **图形变化触发的钩子**
   - **`default-nodes/rescan-trigger`**: 当有链接添加/删除或 `default.configured.*` 元数据更改时触发。
   - **`default-nodes/store-configured-default-nodes`**: 存储用户选择的默认节点。
   - **`default-nodes/metadata-added`**: 恢复 `default.configured.*` 值。

4. **“select-default-node”事件**
   - 这是一个高优先级事件，用于选择给定类别的默认节点。
   - 每个钩子负责查找该类别中优先级最高的节点。可选择节点列表由“default-nodes/rescan”钩子提前计算，并传递给每个“select-default-node”钩子。

5. **事件属性**
   - **`default-node.type`**: 相关默认节点的元数据键后缀（如 `audio.sink`、`audio.source`、`video.source`）。

6. **事件数据交换**
   - **`available-nodes`**: 所有可选择节点的 JSON 数组。
   - **`selected-node`**: 被选中节点的名称。
   - **`selected-node-priority`**: 选中节点的优先级。

### 结论
Default Nodes Scripts 在 WirePlumber 中提供了自动选择和管理默认音频和视频节点的机制，确保用户的偏好能够得到有效管理和应用。通过钩子机制，系统能够实时响应节点的变化，优化用户体验。

# Device Profile/Route Management Scripts 

### Device Profile/Route Management Scripts — WirePlumber 0.5.7 概述

WirePlumber 0.5.7 文档中的“Device Profile/Route Management Scripts”部分介绍了用于为每个设备选择适当配置文件和路由的脚本。

#### 主要内容

1. **脚本功能**
   - 这些脚本负责根据设备的状态选择合适的配置文件和路由。

2. **钩子机制**
   - 钩子在图形变化时被触发，具体包括：
     - **`device/select-profile`**: 设备添加或配置文件枚举变化时调度“select-profile”事件。
     - **`device/select-route`**: 设备添加或路由枚举变化时更新设备信息缓存并调度“select-routes”事件。
     - **`device/store-user-selected-profile`**: 当配置文件参数变化时存储用户选择的配置文件。
     - **`device/store-or-restore-routes`**: 路由参数变化时存储或恢复路由选择。

3. **选择配置文件事件**
   - **高优先级事件**，用于为给定设备选择配置文件。
   - 事件“subject”是设备（`WpDevice`）对象。
   - **交换事件数据**:
     - **`selected-profile`**: 要设置的选定配置文件，类型为包含配置文件参数属性的 JSON 对象。

4. **选择路由事件**
   - **高优先级事件**，用于为给定配置文件选择路由。
   - 事件“subject”是设备（`WpDevice`）对象。
   - **事件属性**:
     - **`profile.changed`**: 如果选择了新配置文件，则为 true；如果仅更改了可用路由，则为 false。
     - **`profile.name`**: 当前活动配置文件的名称。
     - **`profile.active-device-ids`**: 活动设备 ID 的 JSON 数组，用于选择路由。

   - **交换事件数据**:
     - **`selected-routes`**: 要设置的选定路由，类型为映射，键为设备 ID，值为包含路由索引及属性的 JSON 对象。

### 结论
Device Profile/Route Management Scripts 在 WirePlumber 中提供了一种动态选择和管理设备配置文件及路由的机制，确保系统能够根据设备状态自动调整设置，优化用户体验。通过钩子机制，系统能够实时响应设备的变化。

# Linking Scripts

### Linking Scripts — WirePlumber 0.5.7 概述

WirePlumber 0.5.7 文档中的“Linking Scripts”部分介绍了用于在节点之间创建链接的逻辑，这些脚本负责决定哪些链接需要创建。

#### 主要内容

1. **脚本功能**
   - 这些脚本主要用于处理节点之间的连接逻辑，决定如何创建链接。

2. **钩子机制**
   - 钩子分为三个子类别，主要用于响应图形中的变化。它们的功能包括：
     - **调度“rescan-for-linking”事件**：这是一个低优先级事件，目的是扫描所有可链接的会话项并将它们链接到特定目标。
     - **选择每个可链接目标**：通过推送“select-target”事件来处理，这个事件的优先级高，因此在目标选择期间不会处理其他图形变化。

3. **钩子触发的事件**
   - **`linking/rescan-trigger`**: 当可链接会话项（SI）添加、移除或元数据变化时触发，调度“rescan-for-linking”事件。
   - **`linking/linkable-removed`**: 移除可链接会话项时，销毁相关链接。
   - **`linking/follow`**: 当用户更改默认源/接收器时调度“rescan-for-linking”。
   - **`linking/move`**: 当节点目标元数据属性变化时调度“rescan-for-linking”。
   - **`linking/rescan-media-role-links`**: 活动或非活动角色基础链接，基于角色优先级和操作。

4. **事件处理顺序**
   - **“rescan-for-linking”钩子**:
     - **`m-standard-event-source/rescan-done`**: 清除调度标志。
     - **`linking/rescan`**: 为每个可链接的会话项调度选择目标。

5. **选择目标的钩子**
   - **`linking/find-defined-target`**: 选择由 `target.object` 属性或元数据明确定义的目标。
   - **`linking/find-filter-target`**: 如果主题是过滤节点，选择过滤器节点的目标。
   - **`linking/find-media-role-target`**: 根据流的媒体角色和目标的设备意图角色选择目标。
   - **`linking/find-default-target`**: 选择默认源/接收器作为目标。
   - **`linking/find-best-target`**: 根据优先级选择目标。

6. **链接创建流程**
   - **`linking/prepare-link`**: 检查是否需要断开现有链接，并确保目标可用。
   - **`linking/link-target`**: 创建会话项以在主题可链接项和选定目标之间创建链接。

### 结论
Linking Scripts 在 WirePlumber 中提供了一种自动化的方式来管理节点之间的链接，确保在节点状态变化时能够有效地更新连接。通过钩子机制，系统能够灵活响应图形的变化，优化音频和视频流的处理。

# linkable

它具体是怎么工作的？

```
Constraint { "event.session-item.interface", "=", "linkable" },
```

C语言里的是这里：

```
modules/module-standard-event-source.c
136:          "event.session-item.interface", "linkable");
```

link_new

```
static void
request_destroy_link (gpointer data, gpointer user_data)
{
  WpLink *link = WP_LINK (data);

  wp_global_proxy_request_destroy (WP_GLOBAL_PROXY (link));
}
```



# request_destroy



# transition 

transition是一个异步操作。

跟GTask类似。

包含一个内部状态机。

包含一系列的steps。

get_next_step

execute_step

step完成后，必须在step处理函数里调用advance函数来走到下一步。



# Object Manager

提供一种收集一组object的方法。

当前符合某些条件的对象被create或者destroy的时候，会收到通知。

管理了4种object：

* 远程pipewire在registry上广播的对象。这些对象被绑定到WpGlobalProxy。
* 通过wireplumber在pipewire里创建的global对象。
* wireplumber里创建的pipewire对象，并且进行了export。
* wireplumber特有的对象，例如plugin、factory、session item。

# 蓝牙设备的创建过程

```
monitor = createMonitor()
	monitor = SpaDevice("api.bluez5.enum.dbus", config.properties)
	monitor:connect("create-object", createDevice)
		createDevice(parent, id, type, factory, properties)
			这些参数：
				parent表示什么？应该就是monitor本身。
				是一个spadevice。
			device = SpaDevice(factory, properties)
			device:connect("create-object", createNode)
				createNode(parent, id, type, factory, properties)
					这里的parent就是Device
	monitor:activate(Feature.SpaDevice.ENABLED)
```



# 参考资料

1、arch wiki

https://wiki.archlinux.org/title/WirePlumber

2、官方文档

https://pipewire.pages.freedesktop.org/wireplumber/

3、

https://www.collabora.com/news-and-blog/blog/2020/05/07/wireplumber-the-pipewire-session-manager/