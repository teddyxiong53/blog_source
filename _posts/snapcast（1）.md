---
title: snapcast（1）
date: 2020-03-11 11:45:28
tags:
	- 音视频

---

1

要在板端运行snapcast。所以想要集成到buildroot里编译。

自己手动建立一个local的目录来编译。

依赖了avahi。buildroot里有这个，在network application下面，选择好，编译就可以了。
依赖了flac。buildroot里也有。
依赖了beast，这个是基于boost写的一个http和websocket库。

到这里有点走不下去了。

还是先在我的笔记本上编译看看。

需要先看snapcast的编译过程。

不clone submodule的东西。

手动安装相关依赖。

报错，先安装这2个。

```
sudo apt-get install libavahi-client-dev libsoxr-dev
```

再报错：

```
boost/asio.hpp: 没有那个文件或目录
```

我的笔记本上需要安装boost。上面这个错误是boost asio需要安装。

```
sudo apt-get install -y libasio-dev
```

提示会安装这些内容：

```
libboost-date-time-dev libboost-date-time1.58-dev libboost-dev libboost-regex-dev libboost-regex1.58-dev libboost-regex1.58.0 libboost-serialization1.58-dev libboost-serialization1.58.0
  libboost1.58-dev
```

再编译：

```
client_connection.hpp:76:10: error: ‘promise’ in namespace ‘std’ does not name a template type
     std::promise<std::unique_ptr<msg::BaseMessage>> promise_;
```

这个手动在hpp文件里加上：

```
#include <future>
```

再编译：

```
提示io_context.hpp找不到。
目前安装的boost里还真没有。
```



直接根据github上的说明，完全安装操作说明来做，看看buildroot里能不能正常编译。

专门有个snapos，基于buildroot做的。

对应的代码：https://github.com/badaix/snapos

1、下载buildroot。我当前有一份。树莓派3的。刚好可以用。

2、下载snapos。这个很少，就是一些配置信息。

3、定义snapos为external组件。

```
cd /home/hlxiong/work2/buildroot/buildroot-rpi3
make BR2_EXTERNAL=/home/hlxiong/work2/buildroot/buildroot-rpi3/../snapos/buildroot-external/ snapos_rpi3_defconfig
```

> make menuconfig

在最外层的external options里，可以看到配置：

```
     *** Snapcast OS (in /home/hlxiong/work2/buildroot/snapos/buildroot-external) ***   
 [*] Snapcast                                                                           
 [*]   Snapclient                                                                       
 [ ]   Snapserver                                                                       
 [ ] snap-mpd                                                                           
```

执行make。

编译需要时间。先看一下相关的配置。

```
hlxiong@hlxiong-VirtualBox:~/work2/buildroot/snapos/buildroot-external$ tree
.
├── board
│   └── raspberrypi
│       ├── common
│       │   ├── post-build.sh
│       │   └── post-image.sh
│       ├── raspberrypi1
│       │   ├── genimage.cfg
│       │   └── post-image.sh
│       └── raspberrypi2
│           ├── genimage.cfg
│           └── post-image.sh
├── Config.in
├── configs
│   ├── snapos_rpi2_defconfig
│   ├── snapos_rpi3_defconfig
│   ├── snapos_rpi4_defconfig
│   └── snapos_rpi_defconfig
├── external.desc
├── external.mk
├── package
│   ├── snapcast
│   │   ├── Config.in
│   │   ├── S99snapclient
│   │   ├── S99snapserver
│   │   └── snapcast.mk
│   └── snap-mpd
│       ├── Config.in
│       ├── mpd.conf
│       ├── playlists
│       │   └── einslive.m3u
│       ├── S95mpd
│       └── snap-mpd.mk
└── README.md
```

重点是看package目录下的snapcast.mk。

依赖是这么写的：

```
SNAPCAST_DEPENDENCIES = libogg alsa-lib avahi 
# libstdcpp libatomic libflac libvorbisidec
# 这几个都被注释掉了的。
```

就用了ogg的方式。

基于cmake方式来编译的。

```
$(eval $(cmake-package))
```

snapcast.mk里，没有定义编译的行为，只定义了install的相关行为。

Config.in是这么写的：

```
select BR2_PACKAGE_AVAHI
select BR2_PACKAGE_AVAHI_DAEMON
select BR2_PACKAGE_BOOST
select BR2_PACKAGE_DBUS
select BR2_PACKAGE_FLAC
select BR2_PACKAGE_LIBVORBIS
select BR2_PACKAGE_OPUS
```

当前我手动在自己的buildroot下配置snapcast的编译，是报了这个错误：

```
control_session_http.hpp:72:39: 错误：‘tcp_stream’不是‘beast’的成员
```

这个是需要安装boost asio的文件才行的。还要boost beast的文件。

但是当前buildroot里并没有搜索到这2个的配置项。

先编译看看能不能成功。

```
Incorrect selection of kernel headers: expected 4.15.x, got 4.19.x
```

support/scripts/check-kernel-headers.sh 这个脚本报的错误。

为什么会这样呢？

当前buildroot的版本是：2018.02.7, 2018年10月份发布的。

需要的是4.15版本的，但是得到了4.19版本的。

内核的版本是snapos里的defconfig。

它指定的内核是：

```
$(call github,raspberrypi,linux,raspberrypi-kernel_1.20190819-1)/linux-raspberrypi-kernel_1.20190819-1.tar.gz
```

需要的内核版本又是从哪里来的呢？

现在是在make linux-headers这一步。

当前是谁在调用check-kernel-headers.sh？

```
./toolchain/helpers.mk
```

这个脚本要2个参数，第一个是目录`/home/hlxiong/work2/buildroot/buildroot-rpi3/output/host/arm-buildroot-linux-gnueabihf/sysroot`。第二个参数是4.15，

它自己又是封装成了一个check_kernel_headers_version函数。

这2个地方调用了：

```
./package/linux-headers/linux-headers.mk:127:   $(call check_kernel_headers_version,\
./toolchain/toolchain-external/pkg-toolchain-external.mk:537:   $$(call check_kernel_headers_version,\
```

目标版本号从这个宏得到：BR2_TOOLCHAIN_HEADERS_AT_LEAST

```
./.config:373:BR2_TOOLCHAIN_HEADERS_AT_LEAST="4.15"
```

目前toolchain里可以配置的最新的header版本就是4.15的。

我下载最新的buildroot来做这个吧。

最新的版本是2020.02 

这个buildroot包倒是不大,因为就是一些配置文件。

最新版本的头文件就不会有问题了。

编译看看。

现在dl下的规则变化了：每个包都放到自己的单独的目录下了。

不过很多要求的软件的版本也都升级了。所以之前下载的包意义也不是很大。重新下吧。

只是内核的，因为是特定的版本，所以可以重复利用一下。看看它会生成什么目录，我手动停止编译，把之前的压缩包放进去再继续编译。

alsa的库是ftp下载的，好像ssr代理对ftp的没有起作用。

我直接手动下载放到对应的目录下。可以。

下载的boost是1.72版本的。



```
BR2_ROOTFS_POST_BUILD_SCRIPT="$(BR2_EXTERNAL_SNAPOS_PATH)/board/raspberrypi/common/post-build.sh board/raspberrypi3/post-build.sh"
BR2_ROOTFS_POST_IMAGE_SCRIPT="$(BR2_EXTERNAL_SNAPOS_PATH)/board/raspberrypi/common/post-image.sh board/raspberrypi3/post-image.sh"
BR2_ROOTFS_POST_SCRIPT_ARGS="--add-pi3-miniuart-bt-overlay --add-wlan0 --add-audio --speedup-boot --raise-volume --mount-boot"
```

重点看看这些。

```
--add-pi3-miniuart-bt-overlay
	这个是为了串口，因为蓝牙和串口是冲突的，所以要设置一下。
--add-wlan0
	如果/etc/network/interfaces里面没有wlan0，把wlan0加进去。
--add-audio
	这个是在post-image.sh里使用的。
	修改config.txt里来的内容。
--speedup-boot
	这个是为了加快启动速度，也是修改config.txt的内容的。
--raise-volume
	修改默认的alsa音量。
--mount-boot
	Adding mount point for /boot to /etc/fstab
	挂boot分区。
```

编译完了，没有报错。花了3个多小时。

搜索了一下，发现是有tcp_stream的库的。

```
boost/beast/core/tcp_stream.hpp
```

但是1.66版本里，就没有这个头文件。

所以问题的关键就是要升级boost的版本。

镜像288M。



镜像在树莓派上运行测试一下。

运行不起了。

1、首先是需要修改config.txt，在最后加上enable_uart=1，不然都不知道有没有启动成功。

2、现在是死机了。

```
[    2.319902] VFS: Cannot open root device "mmcblk0p2" or unknown-block(179,2): error -117
[    2.329571] mmc1: new high speed SDIO card at address 0001
[    2.333880] Please append a correct "root=" boot option; here are the available partitions:
[    2.333894] 0100            4096 ram0 
[    2.333901]  (driver?)
[    2.342349] usb 1-1: new high-speed USB device number 2 using dwc_otg
[    2.356700] 0101            4096 ram1 
[    2.363965] Indeed it is in host mode hprt0 = 00001101
```

这个是SD卡的分区没有识别出来。

我把这个卡放到Ubuntu笔记本上看一下，也是无法识别的。可能是卡的问题。

换一张SD卡看看。可以正常启动。

Login with user `root` and password `snapcast`

修改/etc/wpa_supplicant.conf。然后杀掉wpa_supplicant进程，重新启动这个进程。

就可以获取到ip地址。

然后怎么验证板端的snapclient是否已经正常工作呢？

目前我在树莓派里只配置了snapclient的。

这个client启动的参数，是从/etc/default/snapclient这个文件里读取的。

默认是空的。

我还是笔记本做snapserver，播放当前实时录音。

```
snapclient -h 172.16.4.205
```

这样可以通，实时的录音可以传递过来。





snapcast怎样跟mpd搭配起来的？



# 使用

snap server的audio input是一个命名管道，叫/tmp/snapfifo。

所有被送进这个管道的数据都会被分发给所有的client。

一个典型的使用snapcast的方法，就是用mpd。它可以配置一个命名管道来作为音频输出。



工作原理

snap-server从/tmp/snapfifo里读取数据包，这些数据包被打上了时间标记。

支持的数据编码格式有：

```
pcm
flac
vorbis
opus
```

通过tcp把数据发送给snap-client。

每个client都跟server持续进行时间同步。

每一个收到的数据包，先被解码，然后放到一个buffer里。

根据server的时间，数据包在合适的时候发送给alsa进行播放。

典型的时间偏差不超过0.2ms。



在Ubuntu下的安装

apt-get是安装不了的。

snapcast的release页面有amd64的deb包。下载，用dpkg进行安装。

snapserver的配置文件在/etc/snapserver.conf。

最关键的一个参数是：

```
stream = pipe:///tmp/snapfifo?name=default
#stream = tcp://127.0.0.1?name=mopidy_tcp
```

在同一台机器上测试。

启动server，不用带任何参数，

```
snapserver
```

启动client，也不用带任何参数。默认参数可以正常工作。

```
snapclient
```



我们现在在server上，执行：

```
sudo cat /dev/urandom > /tmp/snapfifo
```

这样是播放了杂音。

我们可以直接录音，录音参数要指定一下，不然就是杂音。

```
sudo arecord -f S16_LE -r 48000 -c 2 > /tmp/snapfifo 
```

播放实时录音，是可以通的。



# 自己编译的树莓派系统分析

目前树莓派上插着一个usb的摄像头和耳机。

arecord录音可以。

修改密码：passwd root。

aplay播放不行。

```
ALSA lib pcm_dmix.c:1089:(snd_pcm_dmix_open) unable to open slave
```

用speaker-test测试也是一样的。

```
speaker-test -w 1.wav 
```

但是前面通过snapclient可以播放的。

我把mpd进程杀掉，还是不能播。

可以了。因为播放的card1，录音的是card0的。

/root/.asoundrc这样写：

```
pcm.!default {
        type hw
        card 1
}

ctl.!default {
        type hw
        card 0
}
```

就可以了。

现在录音和播放都正常。



数据通路是这样：

```
播放软件 --> /tmp/snapfifo --> snapserver --> 网络 --> snapclient --> alsa
```



mpd怎样进行结合。

编辑mpd.conf文件。让mpd的数据流入到/tmp/snapfifo。

因为mpd默认是输出给alsa的。所以我们需要修改audio_output这个的属性。

改成下面这样：

```
audio_output {
    type            "fifo"
    name            "my pipe"
    path            "/tmp/snapfifo"  # 重点是这一行。
    format          "48000:16:2"
    mixer_type      "software"
}
```

为了测试mpd，我们可以这样来测试。这个是一个在线电台的地址。

```
echo "http://wdr-1live-live.icecast.wdr.de/wdr/1live/live/mp3/128/stream.mp3" > /var/lib/mpd/playlists/einslive.m3u
```

但是当前并没有播放。

不用mpd，有没有什么问题？

用了可以带来什么好处？

我的需求：

1、播放音乐。

2、播放实时语音。



现在笔记本做snapserver，用mpc播放音乐。

树莓派做snapclient。

运行碰到的问题：

1、树莓派的时间不对，连不上服务器。改了时间就好了。

2、播放没有声音。打印这些。

```
2020-03-13 13-44-52 [Info] My MAC: "b8:27:eb:00:4e:ca", socket: 6
2020-03-13 13-44-52 [Err] Exception in Controller::worker(): read_some: End of file
2020-03-13 13-44-52 [Err] Controller::onException: read_some: End of file
```

笔记本自己做client，也没有声音。

问题应该是mpd的问题。

我用arecord > /tmp/snapfifo 。这样可以有声音。

就是audio_output那几行配置，我输入的不行，感觉没有写错。

拷贝配置粘贴过来就正常了，有声音了。

现在树莓派这边也可以得到声音了。

但是效果很不好，一点都不连贯。

笔记本上自己连自己也是一样不连贯。

说明：

1、跟时间没有关系。

2、跟网络没有关系。



这是为什么呢？

是格式问题吗？

现在所有的设备都是卡的。

试一下其他的播放器。

也是一样的。

这就是不可用的状态。

我记得之前并没有这样。

版本问题？

当前笔记本上的版本，是dpkg安装的deb包。0.18.1版本的。

我buildroot里编译的版本是0.17.1的。

手机apk看到也是0.17.1的。

因为默认系统里就已经启动了snapserver和snapclient了。

我后面启动的就冲突了。

现在我自己的板子、手机、树莓派都可以勉强播放。

很多时候都是出错的时候。

经常报End of file的错误。手机和板子上都有碰到。

https://github.com/badaix/snapcast/issues/61

这里提到了同样的问题。看起来需要统一版本。

我把电脑上的版本，也降级到0.17.1的。

我自己编译这个版本。

基于cmake来编译。虽然也可以支持make编译。

```
libflac-dev 
```

运行报这个错。

```
2020-03-13 15-49-03 [Err] Exception: unknown codec: flac
2020-03-13 15-49-03 [Notice] daemon terminated.
```

snapserver.conf里改成ogg的先。

可以正常了。

播放效果还可以。

有时候会持续一段时间，所有的设备都没有数据播出。











参考资料

1、代码下的文档

