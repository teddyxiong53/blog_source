---
title: pulseaudio研究（1）
date: 2021-11-29 11:07:33
tags:
	- 音频

---

--

ubuntu里，默认启动的pulseaudio是这样的：

```
/usr/bin/pulseaudio --start --log-target=syslog
```

PulseAudio是用于[Linux](https://so.csdn.net/so/search?from=pc_blog_highlight&q=Linux)，POSIX和Windows系统的网络低延迟声音服务器。

配置文件

```
~/.config/pulse/daemon.conf, 
/etc/pulse/daemon.conf
```



实时和高优先级计划

为了最大程度地降低播放过程中丢失的风险，

如果基础平台支持，建议使用实时调度运行PulseAudio。

这使PulseAudio守护程序的调度等待时间与系统负载分离，

因此是确保PulseAudio在需要其重新填充硬件播放缓冲区时始终获得CPU时间的最佳方法。

不幸的是，这在大多数系统上都是安全隐患，

因为PulseAudio是作为用户进程运行的，

并且为用户进程提供实时调度特权总是伴随着用户滥用其锁定系统的风险-这可能是由于创建进程而造成的。

实时有效地禁用了抢占。

为了最大程度地降低风险，PulseAudio默认情况下不会启用实时调度。

但是，建议在受信任的系统上启用它。

为此，请使用--realtime（请参见上文）启动PulseAudio或在daemon.conf中启用相应的选项。

由于获取实时调度是大多数系统上的特权操作，因此需要对系统配置进行一些特殊更改，以允许主叫用户使用它们。

有两个选项：

   在较新的Linux系统上，系统资源限制RLIMIT_RTPRIO（有关更多信息，请参见setrlimit（2））可用于允许特定用户获取实时调度。可以在/etc/security/limits.conf中进行配置，建议资源限制为9。

   或者，可以为PulseAudio二进制设置SUID根位。然后，守护程序将在启动时立即放弃root特权，但是保留CAP_NICE功能（在支持该功能的系统上），但前提是主叫用户是Pulse-rt组的成员（请参见上文）。对于所有其他用户，所有功能将立即删除。该解决方案的优势在于，实时特权仅授予PulseAudio守护程序，而不授予所有用户进程。

   或者，如果认为锁定机器的风险太大而无法启用实时调度，则可以启用高优先级调度（即，负好级别）。
   可以通过在启动PulseAudio时传递--high-priority（请参见上文）来启用它，也可以使用daemon.conf中的适当选项来启用它。只有设置了适当的资源限制RLIMIT_NICE（有关更多信息，请参见setrlimit（2））（可能在/etc/security/limits.conf中配置），才能启用负的尼斯级别。建议将资源限制为31（对应于不错的-11级）。



# 环境变量

```
   $ PULSE_SERVER：服务器字符串，指定客户端请求声音服务器连接且未明确要求特定服务器时要连接的服务器。服务器字符串是由空格分隔的服务器地址的列表，依次尝试。服务器地址由一个可选的地址类型说明符(unix:, tcp:, tcp4:, tcp6:)组成，后跟路径或主机地址。主机地址可以包括可选的端口号。服务器地址可以用{}中的字符串作为前缀。在这种情况下，以下服务器地址为ig-
   除非前缀字符串等于本地主机名或计算机ID（/ etc / machine-id），否则不进行操作。

   $ PULSE_SINK：当客户端创建回放流且未明确要求特定接收器时，要连接到的接收器的符号名称。

   $ PULSE_SOURCE：客户端创建记录流且未明确要求特定来源时要连接的来源的符号名称。

   $ PULSE_BINARY：使用服务器自动生成时运行的PulseAudio可执行文件的路径。

   $ PULSE_CLIENTCONFIG：用于客户端配置的应读取的文件路径，而不是client.conf（请参见上文）。

   $ PULSE_COOKIE：包含PulseAudio身份验证cookie的文件的路径。默认为~/.config/pulse/cookie。

   这些环境设置（如果已设置）优先于client.conf中的配置设置（请参见上文）。

```

# /etc/pulse/daemon.conf



```
   daemonize =
   启动后进行守护程序。布尔值，默认为no。--daemonize命令行选项优先。

   fail =
   如果配置脚本default.pa中的任何指令失败，则无法启动。采用布尔型参数，默认为yes。--fail命令行选项优先。

   allow-module-loading =
   启动后允许/禁止加载模块。这是一项安全功能，如果禁用此功能，请确保启动完成后，不能再将其他模块加载到PulseAudio服务器中。建议在启用系统实例时禁用此功能。请注意，如果启用此选项，某些功能（如自动热插拔支持）将无法使用。采用布尔型参数，默认为yes。--disallow-module-loading命令行选项优先。

   allow-exit =
   允许/禁止根据用户请求退出。默认为是。

   resample-method =
   要使用的重采样算法。使用src-sinc最佳质量，src-sinc-中等质量，src-sinc最快，src-零阶保持，src-linear，琐碎，speex-float-N，speex-fixed-N中的一种，ffmpeg，soxr-mq，soxr-hq，soxr-vhq。分别参见libsamplerate和speex的文档以获取有关不同src-和speex-方法的说明。琐碎的方法是最基本的算法。如果您的CPU紧张，请考虑使用此功能。另一方面，它们的质量最差。Speex重采样器采用整数质量设置，范围为0..10（不好...好）。它们以两种形式存在：固定和浮动。前者使用定点数，后者使用浮点数。在大多数台式机CPU上，浮点重采样器要快得多，而且它的质量也稍好一些。soxr系列方法基于libsoxr，libsoxr是SoX声音处理实用程序中的重采样器库。mq变体在这三个中表现最佳。Soq开发人员认为，hq较为昂贵，并且被认为是每个样本最多16位音频的最佳选择。vhq变量比hq精度更高，并且更适合于较大的样本。与其他重新采样器（例如speex）相比，Soxr重新采样器通常在更少的CPU上提供更好的质量。缺点是它们会给输出增加明显的延迟（通常最多20毫秒左右，在极少数情况下会更长）。有关所有可用重采样器的完整列表，请参见dump-resample-methods的输出。默认为speex-float-1。--resample-method命令行选项优先。

   prevent-resampling =
   如果设置，请尝试配置设备以避免重新采样。这仅在支持重新配置其速率的设备上以及没有其他流正在播放或捕获音频的设备上起作用。该设备的配置速率也不会低于默认采样率和备用采样率。

   enable-remixing =
   如果禁用，则永远不会将通道上混或下混到不同的通道映射。而是仅进行简单的基于名称的匹配。默认为是。

   remixing-use-all-sink-channels =
   如果启用，则在重新混合时使用所有接收器通道。否则，请重新混合到再现所有源通道所需的最小接收器通道集。（这对LFE混音没有影响。）默认为是。

   enable-lfe-remixing =
   如果在上混或下混时禁用，则忽略LFE通道。禁用此选项后，仅当输入LFE通道可用时，输出LFE通道也将获得信号。如果没有输入LFE通道可用，则输出LFE通道将始终为0。如果没有输出LFE通道可用，则将忽略输入LFE通道上的信号。默认为否。

   lfe-crossover-freq = 
   LFE滤波器的交叉频率（以Hz为单位）。将其设置为0以禁用LFE滤波器。预设为0。

   use-pid-file =
   在运行时目录中创建PID文件（$XDG_RUNTIME_DIR/pulse/pid）。如果启用此功能，则可以使用--kill或--check之类的命令。如果您计划每个用户启动一个以上的PulseAudio进程，则最好禁用此选项，因为它实际上会禁用多个实例。采用布尔型参数，默认为yes。--use-pid-file命令行选项优先。

   cpu-limit =
   如果禁用，则即使在受支持的平台上也不要安装CPU负载限制器。在调试/分析PulseAudio以禁用干扰的SIGXCPU信号时，此选项很有用。
   接受布尔参数，默认为no。--no-cpu-limit命令行参数优先。

   system-instance =
   作为系统级实例运行守护程序，需要root特权。接受布尔参数，默认为no。--system命令行参数优先。

   local-server-type =
   如果不需要，请不要使用此选项！当前仅当您希望D-Bus客户端使用远程服务器时，此选项才有用。在将来的版本中可能会删除此选项。如果只想在系统模式下运行PulseAudio，请使用system-instance选项。此选项将用户，系统之一或不作为参数。这本质上是system-instance选项的副本。不同之处在于none选项，当您要将远程服务器与D-Bus客户端一起使用时，该选项很有用。如果同时定义了this和system-instance，则此选项优先。默认为设置的系统实例。

   enable-shm =
   启用通过POSIX或memfd共享内存的数据传输。采用布尔型参数，默认为yes。--disable-shm命令行参数优先。

   enable-memfd =
   启用memfd共享内存。采用布尔型参数，默认为yes。

   shm-size-bytes =
   设置守护程序的共享内存段大小（以字节为单位）。如果未指定或设置为0，它将默认为某些系统特定的默认值，通常为64 MiB。请注意，通常不需要更改此值，除非您运行的OS内核不执行内存过量使用。

   lock-memory =
   将整个PulseAudio进程锁定到内存中。当与实时调度结合使用时，这可能会增加drop-out安全性，但这会占用其他进程大量的内存，因此可能会大大降低系统速度。默认为否。

   flat-volumes =
   启用“平坦”音量，即，在可能的情况下，使接收器音量等于与其连接的输入的最大音量。采用布尔型参数，默认为yes。

```

# client.conf



# pacmd

这个是在运行时动态调整pulseaudio的配置。

描述
该工具可用于在运行期间自省(introspect)或重新配置正在运行的PulseAudio声音服务器。

它连接到声音服务器，并提供了一个简单的实时shell，

可用于输入在default.pa配置脚本中也可以理解的命令。

要退出活动shell，请使用ctrl + d。

请注意，shell程序内的“exit”命令将告知PulseAudio守护程序本身关闭！

如果在命令行上传递了任何参数，它们将被传递到活动shell中，该shell将处理命令并退出。



PulseAudio 是在GNOME 或 KDE等桌面环境中广泛使用的音频服务。

它在内核音频组件（比如ALSA 和 OSS）和应用程序之间充当代理的角色。

由于Arch Linux默认包含ALSA，PulseAudio经常和ALSA协同使用。



# 启动和退出

少数情况下PulseAudio在启动X11时没有自动启动，可运行下面的命令启动：

```
$ pulseaudio --start
```

运行下面的命令可以终止PulseAudio：

```
$ pulseaudio --kill
```

正如之前所说, 如果用户安装了桌面环境，PulseAudio很可能通过 `/etc/X11/xinit/xinitrc.d/pulseaudio`文件或者 `/etc/xdg/autostart/`目录下的文件自动启动



Linux 下的音频框架实在让人吐槽无力，OSS、eSound、aRts、ALSA、PulseAudio……这回又冒出来一个 JACK，实在是把人折磨死了。

不过，Linux 发展到今天，PulseAudio 已经足够好用了，

作为普通用户，只要把 PulseAudio 安装上之后，使用默认配置就好，

基本不会再遇到过去常见的各种软件不出声的问题了。

JACK 是为专业音频处理设计的，对于普通日常使用而言，它并不好用。

如果你不打算在 Linux 下做音频相关处理的话，坚持用 PulseAudio 就好。



Linux的声音系统或许是最无序的子系统部分！

作为Server来说，声音无足轻重，无人问津，

而作为桌面来说太多的实现方案，各有各的长出和不足，

ALSA经过多年的发展，基本统一了Linux声卡硬件驱动层的借口，

OSS日渐退出，但是在ALSA之上的各个应用层面，方案和软件之多让人咋舌！

ESD，aRts, JACK,GStreamer, 这些系统组件各个为战，实现了不同的功能，

ESD是GNOME的声音服务器，

而aRts是KDE的，

JACK可以处理一些底层的应用，

GStreamer是GNOME平台比较新的Code和Decode的中间层，向声音服务器输送解码后的RAW Audio，

还有很多程序，比如Xine和Mplayer，他们的声音处理完全是独自完成的，从编解码到输出到ALSA驱动，应用程序全包办了，不需其他的中间层！

这就使整个声音系统显的极其复杂和杂乱无章！

PulseAudio（以前叫Polypaudio）是一个跨平台的，可通过网络工作的声音服务，其一般使用于Linux和FreeBSD操作系统。

它可以用来作为一种简易改进的开放声音后台（ESD）替换。

PulseAudio声音服务器试图以全新的架构来提供新的声音处理架构，希望能像ALSA统一底层那样一统声音应用领域！



简单地说，Android是用了一个Google自己开发的中间层API来让APP和声音驱动（ALSA或者HAL封闭驱动）通信的。在早期，它是个ALSA的插件；现在则命名为AudioFlinger。

无论是什么方式，实际上APP是以访问中间层API的方式让自己发出声音的，而这个API，却成了Android整个音频系统的噩梦。



虽然PulseAudio是开源软件，但开源不等于免费，PulseAudio很可能是针对企业收费的。

这里会导致一个两头难的问题：

大厂商不掏钱 就用，可能会吃官司；而用了，会导致一系列连锁反应，这个会在后面介绍。

小厂商可以完全不鸟什么商业授权，但是本身的孱弱的开发能力不足以对 Android做二次开发。





# 参考资料

1、

https://blog.csdn.net/qq_42138566/article/details/108626378

2、

https://wiki.archlinux.org/title/PulseAudio_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)

3、

http://edyfox.codecarver.org/html/jack_alsa_pulse_walkthrough.html

4、

https://www.liangzl.com/get-article-detail-184781.html

5、

https://www.linuxidc.com/Linux/2019-02/156865.htm