---
title: 音频之bluealsa
date: 2019-06-17 15:10:51
tags:
	- 音频

---

--

# 最新状态

目前的现状是，为了从蓝牙设备传输音频或将音频传输到蓝牙设备，

必须安装通用音频服务器，

例如 PipeWire 或 PulseAudio，

或者使用已弃用且无人维护的 BlueZ 版本 4。

BlueALSA 专为小型、低功耗、专用音频或音频/视频系统而设计，

在这些系统中不需要 PulseAudio 或 PipeWire 的高级音频管理功能。

目标系统必须能够在其所有音频应用程序直接与 ALSA 连接的情况下正常运行，

并且一次只有一个应用程序使用每个蓝牙音频流。

在此类系统中，BlueALSA 在现有 ALSA 声卡支持的基础上添加了蓝牙音频支持。

请注意，这意味着应用程序受到 ALSA API 功能的限制，并且无法使用 PulseAudio 和 PipeWire 等音频服务器的高级音频处理功能。



# RK3308里的bluealsa

用rk3308的做项目。

eq_drc_process里，用到了bluealsa。看看这个是什么东西。

简单来说，bluealsa就是bluez和alsa之间的一个代理，用来把二者连续起来，来实现蓝牙播放功能。

In general, BlueALSA acts as a proxy between BlueZ and ALSA.

bluealsa是一个进程，在系统启动阶段被创建。

会在dbus里注册一个名字叫org.bluealsa的服务。

集成了bluealsa的设备，既可以作为一个音箱来播放音乐，也可以连接一个外部音箱来进行播放。

连接外部音箱进行播放：

```
aplay -D bluealsa:SRV=org.bluealsa,DEV=XX:XX:XX:XX:XX:XX,PROFILE=a2dp 1.wav
```

也可以录音。

```
arecord -D bluealsa capture.wav
```



依赖的库

```
alsa-lib
bluez > 5.0
glib
sbc
libdbus
```



配置文件，在/usr/share/alsa/alsa.conf.d/20-bluealsa.conf

```
# BlueALSA integration setup

defaults.bluealsa.interface "hci0"
defaults.bluealsa.profile "a2dp"
defaults.bluealsa.delay 20000
defaults.bluealsa.battery "yes"

ctl.bluealsa {
	@args [ HCI BAT ]
	@args.HCI {
		type string
		default {
			@func refer
			name defaults.bluealsa.interface
		}
	}
	@args.BAT {
		type string
		default {
			@func refer
			name defaults.bluealsa.battery
		}
	}
	type bluealsa
	interface $HCI
	battery $BAT
}

pcm.bluealsa {
	@args [ HCI DEV PROFILE DELAY ]
	@args.HCI {
		type string
		default {
			@func refer
			name defaults.bluealsa.interface
		}
	}
	@args.DEV {
		type string
		default {
			@func refer
			name defaults.bluealsa.device
		}
	}
	@args.PROFILE {
		type string
		default {
			@func refer
			name defaults.bluealsa.profile
		}
	}
	@args.DELAY {
		type integer
		default {
			@func refer
			name defaults.bluealsa.delay
		}
	}
	type plug
	slave.pcm {
		type bluealsa
		interface $HCI
		device $DEV
		profile $PROFILE
		delay $DELAY
	}
	hint {
		show {
			@func refer
			name defaults.namehint.extended
		}
		description "Bluetooth Audio Hub"
	}
}
```



bt_start.sh里，这样用的：

```
bluealsa --profile=a2dp-sink & 
sleep 1
bluealsa-aplay --profile-a2dp 00:00:00:00:00:00 &
```

这样完全可以正常播放歌曲。

先看bluealsa这个程序的代码实现。对应的入口是src/main.c。

bluealsa-aplay的代码在utils/aplay.c里。做的事情很简单，就是读取数据，写入到default设备里。

我要做的就是把写入default设备的行为，改为写入fifo。

不过还是先把bluealsa-aplay的代码细节看懂再动手。

代码不到700行。还有大量的参数处理。

main函数流程：

```
1、g_dbus_connection_new_for_address_sync
	建立对G_BUS_TYPE_SYSTEM的连接。
2、bluealsa_open("hci0")，返回一个fd。
	本质是打开一个蓝牙socket。
3、bluealsa_subscribe
	订阅add和remove这2个事件。
4、注册信号处理：
	main_loop_stop
5、进入主循环。
	把第二步得到的fd，添加到poll里来监听POLLIN。
	poll
	recv
	bluealsa_get_transports
		拿到数据。
	这一层循环主要是处理连接。
	数据发送靠创建一个线程，然后再线程里再循环poll进行处理。
	
```

我尽量改动少一些。



运行打印：

```
/userdata # ./bluealsa-aplay --profile-a2dp 00:00:00:00:00:00 -v
Selected configuration:
  HCI device: hci0
  PCM device: default
  PCM buffer time: 500000 us
  PCM period time: 100000 us
  Bluetooth device(s): ANY
  Profile: A2DP
./bluealsa-aplay: ../src/shared/ctl-client.c:102: Connecting to socket: /var/run/bluealsa/hci0
./bluealsa-aplay: ../src/shared/ctl-client.c:126: Subscribing for events: 101
./bluealsa-aplay: aplay.c:575: Starting main loop
./bluealsa-aplay: aplay.c:597: Fetching available transports
./bluealsa-aplay: aplay.c:597: Fetching available transports                              
```

手机连接时：

```
./bluealsa-aplay: aplay.c:661: Creating PCM worker 08:D4:6A:78:68:D7
./bluealsa-aplay: ../src/shared/ctl-client.c:102: Connecting to socket: /var/run/bluealsa/hci0
./bluealsa-aplay: ../src/shared/ctl-client.c:341: Requesting PCM open for 08:D4:6A:78:68:D7
./bluealsa-aplay: aplay.c:328: Starting PCM loop
```

断开连接时：

```
./bluealsa-aplay: aplay.c:344: Device marked as inactive: 08:D4:6A:78:68:D7
./bluealsa-aplay: aplay.c:597: Fetching available transports
./bluealsa-aplay: ../src/shared/ctl-client.c:383: Closing PCM for 08:D4:6A:78:68:D7
./bluealsa-aplay: aplay.c:240: Exiting PCM worker 08:D4:6A:78:68:D7
```

现在删除带pcm的内容。

把snd_pcm_t 替换为int fifo_fd。

buffer处理可以简化。

当前播放数据可以通过fifo发送出去。

但是效果有点问题。

速度似乎被加快了。

还有一些杂音。

每次从蓝牙read到的数据是2560 。这个buffer可以分配小一些。

应该是snapclient从fifo里拿到数据，都当48000/S16_LE/2 的来处理。

而蓝牙播放的，不一定是这样的。

所以我应该在写入fifo之前，把音频数据重采样为目标格式。

当前可以正常播放，说明拿到的就是pcm数据了。

我怎么才能知道当前的音乐的格式呢？

不知道板端的蓝牙音频能不能统一设置格式。

我自己对收到的数据进行重采样，这种思路感觉行不通。

在bluealsa代码目录下，搜索”44100“。

```
./src/transport.c:561:                          return 44100;
./src/transport.c:578:                          return 44100;
```

看看transport.c里做了些什么。

transport_get_sampling这个函数里，可以得到格式。

```
unsigned int transport_get_sampling(const struct ba_transport *t)
```

A2DP的编码有这么几种，基本上应该就是SBC的。

```
#define A2DP_CODEC_SBC			0x00
#define A2DP_CODEC_MPEG12		0x01 这个是MP3
#define A2DP_CODEC_MPEG24		0x02 这个是AAC
#define A2DP_CODEC_ATRAC		0x03  这个是苹果的。
```

bluealsa执行过，然后杀掉，重新启动，就不行。

```
/userdata # bluealsa --profile=a2dp-sink
bluealsa: Couldn't initialize controller thread: Bad file descriptor
```

找到解决方法了。删除这个文件就好了。

```
 rm /var/run/bluealsa/hci0
```

目前只注册了SBC这一种。

```
bluealsa: bluez.c:677: Registering endpoint: /A2DP/SBC/Sink/1
```

其他的几种编码都没有使能。



```
./bluealsa: bluez.c:540: Configuration: channels: 2, sampling: 44100
```



bluealsa里，sbc解码的地方，这里可以做文章，进行重采样。

这些门门道道也不少。



```
#define BLUEALSA_MAX_CLIENTS 7
```



# 在Ubuntu上编译

为了方便分析代码，我在Ubuntu上进行编译测试看看。

```
git clone https://github.com/Arkq/bluez-alsa
```

先进行配置

```
autoreconf --install
```

这样才能得到configure脚本。

看看有哪些选项。

```
./configure --help
```

```
./configure --enable-debug --enable-debug-time --enable-aac --enable-aplay --enable-test
```

提示我的系统没有安装bluez。

到这里下载最新的bluez。代码只有不到2M。

http://www.bluez.org/release-of-bluez-5-54-and-5-53/

编译安装了还是提示没有bluez。

```
No package 'bluez' found
```

是因为需要安装

```
sudo apt-get install libbluetooth-dev libsbc-dev
```

现在编译完成。

执行bluealsa。提示错误：

```
./bluealsa: E: Couldn't acquire D-Bus name: org.bluealsa
```

网上看的信息是，启动了多个bluealsa的实例导致的。

但是我并没有启动多个实例。可能是其他的进程占用了。

我进入Ubuntu的图形界面，把蓝牙的任务栏图标退出。

还是一样的问题。



# 代码分析

总体上来说，是跟普通的tcp网络编程非常类似。

new一个socket，bind、listen。

然后等待客户端连接上来（最多支持7个client）

用poll来处理io。

```
├── at.c
├── at.h
├── bluealsa.c 
├── bluealsa.h  一个结构体ba_config。2个函数：config_init、config_free。
├── bluez.c
├── bluez.h  定义了几个UUID宏。3个函数：register_a2dp/hfp、bluez_subscribe_signals
├── bluez-a2dp.c 
├── bluez-a2dp.h  几个结构体常量。
├── bluez-iface.c 
├── bluez-iface.h 2个结构体常量。
├── ctl.c
├── ctl.h 3个函数：ctrl_thread_init/free/event。
├── hfp.h 一下宏和枚举。
├── io.c  
├── io.h  io_thread_a2dp_sink_sbc。这样的几个函数。
├── main.c
├── rfcomm.c
├── rfcomm.h
├── shared
│   ├── ctl-client.c
│   ├── ctl-client.h
│   ├── ctl-client.lo
│   ├── ctl-proto.h
│   ├── ffb.c
│   ├── ffb.h fifo buffer的意思。
│   ├── log.c
│   ├── log.h
│   ├── rt.c
│   ├── rt.h
│   └── rt.lo
├── transport.c
├── transport.h 定义了很多重要结构体和函数。
├── utils.c
└── utils.h
```

最重要的是transport.c和ctl.c和io.c这3个文件。

ctl.c

```
定义了各个cmd函数：
	ctl_thread_cmd_ping
控制主线程
	void *ctl_thread(void *arg)
		这里用poll进行io处理。
		
```

io.c

```

```

## bluealsa进程分析

struct ba_config 这个结构体相当于全局的context。

各种配置、flag、运行状态都放到这个里面。

这个设计理念倒是跟我的习惯比较接近。

就是名字上有点怪，其实不只是config。更加相当于一个context。

最多可以连接7个client。

poll的fd个数，就是7+2, 2表示的是控制信息的通路。

默认都的配置监听POLLIN，也就是read事件。

```
{ /* initialize (mark as closed) all sockets */
		size_t i;
		for (i = 0; i < sizeof(config.ctl.pfds) / sizeof(*config.ctl.pfds); i++) {
			config.ctl.pfds[i].events = POLLIN;
			config.ctl.pfds[i].fd = -1;
		}
	}
```

`/var/run/state/bluealsa/hci0`。

创建ctl_thread，这个thread改名为bactl。

```
pthread_setname_np(config.ctl.thread, "bactl");
```





```
struct ba_device  对应一个手机这样的设备。持有一个hashtable，对应多个transport。
struct ba_pcm   一个音频流的表示。
struct ba_transport 可以是a2dp、sco、rfcomm传输中的一种。
```

bluez_profile_new_connection的时候，device_get时，进行device_new，创建一个ba_device，来表示连接过来的手机。



# test-server.c

看一下这个例子。



# 加入状态控制

希望可以通过按键来控制蓝牙的播放暂停。

另外需要获取蓝牙的播放状态。

在utils/aplay.c里，有一个pause_device_player函数。可以看到里面是使用dbus来执行暂停的。

```
	sprintf(obj, "/org/bluez/%s/dev_%2.2X_%2.2X_%2.2X_%2.2X_%2.2X_%2.2X/player0",
			ba_interface, dev->b[5], dev->b[4], dev->b[3], dev->b[2], dev->b[1], dev->b[0]);
	msg = g_dbus_message_new_method_call("org.bluez", obj, "org.bluez.MediaPlayer1", "Pause");
```

这里有python通过dbus来进行蓝牙控制的例子。

https://github.com/elsampsa/btdemo

这样可以调节蓝牙音量。

```
dbus-send --print-reply --system --dest=org.bluez /org/bluez/xxxx/yyyy/dev_zz_zz_zz_zz_zz_zz org.bluez.Control.VolumeUp
```

where "xxxx" **seems** to be the PID for *bluetoothd*, "yyyy" is the adapter (like "hci0"), "zz_zz_zz..." represents the MAC address of the controlled device (headset, speakers, etc.) separated by underscores, and '*VolumeUp*' is replaced with '*VolumeDown*' to decrease volume.

所以，我的方法，就是不用跟bluealsa进行通信，只需要在自己的主进程新建一个dbus连接，直接跟bluez通信进行控制就好了。

在bluez/test目录下有一个simple-player的python脚本。可以看看。



dbus-send --system --print-reply --dest=org.bluez /org/bluez/hci0 org.freede
sktop.DBus.Introspectable.Introspect



```
dbus-send --system --print-reply --type=method_call --dest='org.bluez' '/org/bluez/hci0/dev_C8_85_50_B1_C8_6B/fd0' org.freedesktop.DBus.Properties.Set string:"org.bluez.MediaTransport1" string:"Volume" variant:uint16:127
```



dbus-send --system --print-reply --dest=org.bluez /org/bluez/hci0/dev_54_A4_93_A0_00_08 org.bluez.MediaControl1.Play

这个命令，格式上应该是对的。

我看很多文章都是这么说的。

但是当前不能工作，提示找不到方法。

知道原因了。

dev_后面跟的蓝牙地址，不是板端的蓝牙地址，而是手机的蓝牙地址。

改了就可以正常播放了。

bluez/tools下面还有一个bluetooth-player的工具。是交互式的。可以进行很方便的控制。

```
[bluetooth]# help
Available commands:
        list            List available players
        show [player]   Player information
        select <player> Select default player
        play [item]     Start playback
        pause           Pause playback
        stop            Stop playback
        next            Jump to next item
        previous        Jump to previous item
        fast-forward            Fast forward playback
        rewind          Rewind playback
        equalizer <on/off>      Enable/Disable equalizer
        repeat <singletrack/alltrack/group/off> Set repeat mode
        shuffle <alltracks/group/off>   Set shuffle mode
        scan <alltracks/group/off>      Set scan mode
        change-folder <item>    Change current folder
        list-items [start] [end]        List items of current folder
        search string   Search items containing string
        queue <item>    Add item to playlist queue
        show-item <item>        Show item information
        quit            Quit program
```

我可以把这个整理一下。把代码整合到我的主进程里。

不搞这么复杂了。

直接拼接cmd来通过dbus-send来做。

参考bluez/doc/media-api.txt文档。

获取状态：

```
dbus-send --system --print-reply --dest=org.bluez /org/bluez/hci0/dev_08_D4_6A_78_68_D7/player0  org.freedesktop.DBus.Properties.Get  string:org.bluez.MediaPlayer1 string:Status 
```

暂停。

```
dbus-send --system --print-reply --dest=org.bluez /org/bluez/hci0/dev_08_D4_6A_78_68_D7 org.bluez.MediaControl1.Pause
```

但是还需要监听蓝牙的连接事件。这个所以最后还是用dbus来编程。

buildroot里有一个dbus-cpp目录，就是http://downloads.sourceforge.net/project/dbus-cplusplus/dbus-c++/0.9.0



```
src/device.c:device_remove_connection() g_dbus_emit_property_changed, interface: org.bluez.Device1, name:Connected
```



碰到一下麻烦的死机问题，还是靠命令来做。

在这个目录下，有生成这样的一些内容，应该可以利用。

54:A4:93:A0:00:08 这个是板端的蓝牙地址。

08:D4:6A:78:68:D7 这个是我手机的地址。

还有两个是其他连接过本设备的设备地址。不管。

```
/userdata/cfg/lib/bluetooth # find -name "*"
.
./54:A4:93:A0:00:08
./54:A4:93:A0:00:08/settings
./54:A4:93:A0:00:08/cache
./54:A4:93:A0:00:08/cache/08:D4:6A:78:68:D7
./54:A4:93:A0:00:08/cache/A8:5B:78:6B:5C:7F
./54:A4:93:A0:00:08/cache/00:1A:7D:DA:71:11
./54:A4:93:A0:00:08/08:D4:6A:78:68:D7
./54:A4:93:A0:00:08/08:D4:6A:78:68:D7/info
./54:A4:93:A0:00:08/08:D4:6A:78:68:D7/attributes
./54:A4:93:A0:00:08/A8:5B:78:6B:5C:7F
./54:A4:93:A0:00:08/A8:5B:78:6B:5C:7F/info
```

settings，这个存放的板端蓝牙的信息。

```
[General]
Discoverable=false
```

```
/userdata/cfg/lib/bluetooth/54:A4:93:A0:00:08/08:D4:6A:78:68:D7 # cat attributes

[1]
UUID=00002800-0000-1000-8000-00805f9b34fb
Value=1801
EndGroupHandle=3

[20]
UUID=00002800-0000-1000-8000-00805f9b34fb
Value=1800
EndGroupHandle=26
```

```
/userdata/cfg/lib/bluetooth/54:A4:93:A0:00:08/08:D4:6A:78:68:D7 # cat info
[LinkKey]
Key=2FB66E483917F783F80584C1FBAEE996
Type=4
PINLength=0

[General]
Name=cG-SOe6:niZa7XDL:b8Sii
Class=0x5a020c
SupportedTechnologies=BR/EDR;
Trusted=false
Blocked=false
Services=00001105-0000-1000-8000-00805f9b34fb;0000110a-0000-1000-8000-00805f9b34fb;0000110c-0000-1000-8000-00805f9b34fb;0000110d-0000-1000-8000-00805f9b34fb;0000110e-0000-1000-8000-00805f9b34fb;00001112-0000-1000-8000-00805f9b34fb;00001116-0000-1000-8000-00805f9b34fb;0000111f-0000-1000-8000-00805f9b34fb;0000112f-0000-1000-8000-00805f9b34fb;00001132-0000-1000-8000-00805f9b34fb;00001200-0000-1000-8000-00805f9b34fb;00001800-0000-1000-8000-00805f9b34fb;00001801-0000-1000-8000-00805f9b34fb;

[DeviceID]
Source=1
Vendor=196
Product=5025
Version=4096
```

看连接前后，attributes和info文件都没有变化。

那么这里也没有什么利用价值。

是在哪里指定这些文件的生成路径的呢？

bluetoothd的main.conf，并没有放到板端。



/usr/lib/bluetooth/plugins

板端没有这个目录。是因为插件没有单独编译成so文件，而是跟bluetoothd打包在一起了。

```
hlxiong@hlxiong-VirtualBox:~/work2/rk3308_no_modify/buildroot/output/rockchip_rk3308_wb220b_release$ grep -nwr "rk_bt_sink_pause" .
匹配到二进制文件 ./target/usr/lib/libDeviceIo.so
./host/aarch64-rockchip-linux-gnu/sysroot/usr/include/DeviceIo/RkBtSink.h:27:int rk_bt_sink_pause(void);
匹配到二进制文件 ./host/aarch64-rockchip-linux-gnu/sysroot/usr/lib/libDeviceIo.so
```

rk有一个包，在external/deviceio目录下。

但是这个只有库文件和头文件。不具备通用性。

先实现我的需求再说吧。可移植性以后再说。

发现其实并不可用。估计rk自己都没有维护。

还是回到用命令的方式。

可用用`hcitool con`来查看连接状态。

```
Connections:
        > ACL 08:D4:6A:78:68:D7 handle 1 state 1 lm MASTER AUTH ENCRYPT
/userdata # hcitool con
Connections:
```

搞定了。就用命令行的方式。



# 问题解决

```
		case 6 /* --a2dp-force-mono */ :
			config.a2dp_force_mono = true;
			break;
		case 7 /* --a2dp-force-audio-cd */ :
			config.a2dp_force_44100 = true;
			break;
		case 8 /* --a2dp-volume */ :
			config.a2dp_volume = true;
			break;

```

# 关闭打开服务

现在要进行一个连接断开的操作。





```
a2dp-codecs.h
	定义了codec的宏定义和结构体。sbc这些。
a2dp-rtp.h
	2个结构体。
at.c
at.h
	rfcomm at命令。
bluealsa.c
bluealsa.h
	ba_config这个核心结构体。
	init和free函数。
bluez-a2dp.c
bluez-a2dp.h
	定义结构体bluez_a2dp_sbc
bluez-iface.c
bluez-iface.h
	gdbus结构体。就这2个。
	const GDBusInterfaceInfo bluez_iface_endpoint;
	const GDBusInterfaceInfo bluez_iface_profile;
bluez.c
bluez.h
	这3个函数
	void bluez_register_a2dp(void);
    void bluez_register_hfp(void);
    int bluez_subscribe_signals(void);
ctl.c
ctl.h
	控制处理线程。
hfp.h
io.c
io.h
	io处理线程。
main.c
rfcomm.c
rfcomm.h
transport.c
transport.h
	ba_transport 这个核心结构体。
	ba_device
	ba_pcm
utils.c
utils.h
```

# 代码知识点

```

涉及的知识点
1、getopt_long
	多次调用可以的。
2、一个全局config的风格。
3、pthread的各种函数使用。
	pthread_setname_np给线程改名。
	
4、group的使用。
5、glib hashtable。
6、hci_dev蓝牙编程。
7、控制线程和io线程分开的处理方式。
8、unix socket的使用。
9、pipe的使用，ctl thread里。
10、gdbus的使用。
11、通过gdbus跟bluez通信。
12、sigaction
13、glib mainloop。
14、alsa plugin的写法。
15、pthread之cancel用法

```

# 按文件分析代码

先读main.c

```
main
	log_open
	bluealsa_config_init：初始化全局ba_config结构体
	hci_devlist：获取所有的hci设备
	free(hci_devs); 使用后又释放掉
	bluealsa_ctl_thread_init
		创建/var/run/bluealsa目录。
		创建socket(PF_UNIX 这个socket。
		chmod为0660
		chown为audio组的
		listen在socket上。
		对event创建pipe。
		创建ctl_thread ，修改名字为bactl
	g_dbus_address_get_for_bus_sync 拿到地址
	g_dbus_connection_new_for_address_sync 用地址连接
	bluez_subscribe_signals
		g_dbus_connection_signal_subscribe 用这个函数进行订阅
			订阅了2个消息：InterfacesAdded、PropertiesChanged
	bluez_register_a2dp
		bluez_register_a2dp_endpoint 用这个注册了sbc解码能力
			g_dbus_message_new_method_call
			g_dbus_connection_send_message_with_reply_sync
	bluez_register_hfp
	注册SIGTERM、SIGINT，用main_loop_stop函数处理
		main_loop_stop里退出主循环
	g_main_loop_new
	g_main_loop_run(loop);
		这里死循环
		
ctl_thread函数
	while 1
		poll(config.ctl.pfds 阻塞读取事件
		recv 得到request结构体
		从commands 命令数组里找到对应的命令进行处理。
		
commands 命令数组处理的命令分类
	ctl_thread_cmd_ping
		回复一个pong。
	ctl_thread_cmd_subscribe
		往config.ctl.subs 里填入事件
		回复success。
	ctl_thread_cmd_list_devices
		先回复device list
		再回复success
	ctl_thread_cmd_list_transports
		先回复transports list
		再回复success
```

transport的概念

对应了结构体ba_transport

有3种类型：A2DP、sco、rfcomm。

还对应了profile：A2DP source/sink、hfp ag/hf。

transport状态有：idle、pending、active、paused、limbo。

消息是一个union，包含了A2DP、rfcomm、sco这3种情况。

例如a2dp的包括了：

```
ch1_mute
ch2_mute
ch1_volume
ch2_volume
delay
ba_pcm结构体
cconfig codec的配置
```

一个release函数。



transport api

```
transport_new
	不单独调用。
	只被transport_new_a2dp和transport_new_rfcomm调用。
transport_new_a2dp
	只被bluez_endpoint_set_configuration调用。
		bluez_endpoint_method_call
```



endpoint的概念

```
SelectConfiguration
SetConfiguration
ClearConfiguration
Release
```

https://download.tizen.org/misc/media/conference2012/wednesday/bayview/2012-05-09-0900-0940-bluez-_plugging_the_unpluggable.pdf

https://git.kernel.org/pub/scm/bluetooth/bluez.git/tree/doc



# A2DP RTP 说明

A2DP（Advanced Audio Distribution Profile）和 RTP（Real-time Transport Protocol）是用于音频传输的两个不同的协议或标准，通常在蓝牙音频传输和网络音频流传输中使用。让我分别解释它们：

1. **A2DP（Advanced Audio Distribution Profile）**：
   - A2DP 是一种蓝牙配置文件，旨在支持高质量音频流的传输。它通常用于蓝牙音频耳机、音箱、汽车音响系统等设备中。
   - A2DP 允许音频设备通过蓝牙连接进行高质量音频流传输，例如音乐或语音通话。
   - A2DP 协议定义了音频编解码器的规范，以及如何在蓝牙连接上传输音频流。它支持多种音频编解码器，例如SBC（Subband Coding）、AAC（Advanced Audio Coding）等。
   - A2DP 还支持立体声音频和多通道音频传输，允许用户在蓝牙音频设备之间共享音频。

2. **RTP（Real-time Transport Protocol）**：
   - RTP 是一种网络协议，用于在 IP 网络上实时传输音频、视频和其他多媒体数据。它通常与 RTCP（Real-time Transport Control Protocol）一起使用，用于监控和控制媒体流。
   - RTP 的主要目标是提供实时性，确保多媒体数据以低延迟传输。它还处理丢包、流同步、时序和时间戳等问题。
   - RTP 协议是面向连接的，但不保证可靠性。它通常用于多媒体通信，其中一些数据丢失也是可以接受的，但延迟必须尽量降低。

在某些情况下，A2DP 和 RTP 可以结合使用，特别是在蓝牙音频传输中。

例如，当你使用蓝牙音箱或耳机时，A2DP 可用于传输音频数据，

而 RTP 可用于在 IP 网络上传输音频流。

这种组合允许你在不同设备之间以高质量和实时性传输音频。总之，A2DP 和 RTP 是两个不同的协议，但它们通常在多媒体和音频传输中一起使用。

# 简介

BlueALSA是一个开源项目，旨在为Linux系统提供蓝牙音频支持。它允许用户通过蓝牙连接将音频从其设备（比如手机、电脑等）传输到支持蓝牙音频的外部设备（如蓝牙扬声器、耳机等）上。

这个项目的主要功能包括：

1. **蓝牙音频支持：** BlueALSA允许用户使用蓝牙连接将音频传输到外部蓝牙音频设备上，实现无线音频传输。
  
2. **高质量音频传输：** 它支持多种音频编解码器，包括SBC、AAC、aptX、LDAC等，使得用户可以根据设备和需求选择合适的音频编解码器以获得更好的音频质量。

3. **易于使用和配置：** BlueALSA提供了一组命令行工具和配置选项，使得用户可以相对容易地进行配置和管理。

4. **开源和自由：** 作为开源项目，BlueALSA提供了代码和文档，让开发者和用户可以自由地使用、修改和定制。

总的来说，BlueALSA是一个使得Linux系统用户能够方便地使用蓝牙连接外部音频设备的工具，提供了灵活的配置和高质量的音频传输功能。

# 发展历史

BlueALSA是在Linux平台上为蓝牙音频设备提供支持的项目，其发展历史可以简要概括如下：

1. **初期阶段：** BlueALSA的开发始于对蓝牙音频支持的需求。在Linux系统中，原生的蓝牙支持（BlueZ）并不包含对高级音频传输（A2DP）的完整支持，这促使了开发者开始着手创建一个独立的项目来填补这个空白。

2. **项目启动和基本功能：** BlueALSA项目在解决蓝牙音频支持方面取得了进展，最初提供了基本的功能，允许用户通过蓝牙连接将音频传输到外部设备上。

3. **功能扩展和优化：** 随着时间的推移，BlueALSA进行了多次更新和改进，添加了对更多蓝牙音频编解码器的支持，提高了音频传输的稳定性和质量，并逐步改进了用户体验和配置选项。

4. **社区贡献和开源生态系统：** BlueALSA是一个开源项目，因此吸引了许多开发者和社区成员的贡献。社区的积极参与带来了更多的功能改进、Bug修复和对新硬件的支持。

5. **持续发展和更新：** BlueALSA在不断发展，以适应新的Linux发行版、蓝牙协议的更新以及用户需求的变化。不断更新的版本带来更好的性能、兼容性和功能。

整体来说，BlueALSA是一个不断发展和改进的项目，通过不断的更新和社区的参与，为Linux系统提供了强大的蓝牙音频支持，使得用户能够更方便地使用蓝牙连接外部音频设备。

# 代码架构

BlueALSA的代码架构主要涉及两个方面：蓝牙连接管理和音频处理。

1. **蓝牙连接管理：** 这部分代码负责处理蓝牙连接、设备发现、配对和通信。它包含了与BlueZ（Linux上蓝牙协议栈）交互的代码，以建立和管理蓝牙连接。BlueALSA利用BlueZ的功能来处理蓝牙设备之间的通信，确保音频数据能够通过蓝牙连接进行传输。

2. **音频处理：** BlueALSA的另一部分代码负责音频数据的处理和传输。这包括音频编解码器的支持，以及将音频数据从源（例如文件、音乐应用程序等）传输到蓝牙音频设备的代码。它还可能包含对不同音频格式的转换和处理，以确保音频能够正确地在蓝牙连接上传输和播放。

整个架构通常以模块化和分层的方式设计，以便于扩展和维护。这种设计允许BlueALSA适应不同的蓝牙设备、音频编解码器和Linux系统的变化，并且使得新功能的添加相对容易。

# aptx介绍

aptX是一种由Qualcomm开发的音频编解码技术，旨在提供更高质量的蓝牙音频传输。

它被设计用于提供比标准的蓝牙音频编解码器更好的音频质量，尤其是在音频传输的压缩和解压缩方面。

主要特点包括：

1. **高音质传输：** aptX通过改进蓝牙音频的压缩算法，提供更高的音频质量，能够实现接近无损音质的传输，相比标准的SBC编解码器，其音质更为清晰和逼真。

2. **低延迟：** 它还具有较低的音频传输延迟，这对于需要实时音频传输的应用（如视频观看、游戏等）非常重要，可以减少音频和视频之间的不同步现象。

3. **宽容度：** aptX在面对蓝牙传输中的一些干扰和信号丢失时具有较强的容错性，能够在一定程度上提供更稳定的音频传输。

4. **适应性：** 这种编解码技术可以适应不同的音频参数，如比特率、声道数和采样率等，以适应不同的音频设备和需求。

aptX技术是专门为提升蓝牙音频质量而设计的，让用户在使用蓝牙耳机、扬声器等设备时能够获得更好的音质和更低的延迟，提高了音频传输的表现。

# LDAC

LDAC是由Sony开发的一种无损音频编解码技术，用于在蓝牙设备间传输高分辨率音频。LDAC的主要特点和优势包括：

1. **高音质传输：** LDAC致力于提供高品质的音频传输，支持高分辨率的音频，能够传输更多的音频数据，提供更接近无损音质的体验。

2. **可调的比特率：** LDAC采用可变比特率技术，允许根据信号质量和连接稳定性动态调整比特率。这使得LDAC能够在不同的环境下（比如信号强弱不同的蓝牙连接）保持音质和稳定性。

3. **多种码率选择：** LDAC支持三种不同的码率（330kbps、660kbps、990kbps），允许用户根据需求选择不同的音质和稳定性。

4. **低延迟模式：** LDAC还提供了低延迟模式，可以在保持较高音质的同时，实现较低的传输延迟。这对于需要实时音频的应用（如观看视频、玩游戏）非常有帮助。

5. **广泛的兼容性：** 虽然最初由Sony开发，但LDAC技术已经被开放给其他厂商，并得到了一些Android设备和其他蓝牙产品的支持。

总的来说，LDAC致力于在蓝牙音频传输中提供更高质量的音频，尤其是在音质、稳定性和适应性方面，为用户提供更优秀的无线音频体验。

# 双声道和立体声是什么区别

在音频领域中，“双声道”和“立体声”是描述多声道音频的术语，它们有着细微但显著的区别：

1. **双声道（Dual Channel）：** 双声道音频指的是两个独立的声道（左声道和右声道），每个声道可以携带不同的音频信息。在双声道音频中，左右声道可以分别传输不同的声音内容，提供了左右定位的音频体验。

2. **立体声（Stereo）：** 立体声通常也是指两个声道，但与双声道略有不同。==立体声更侧重于在两个声道之间的声音分布和定位。它通过将声音以不同的方式混合到左右声道中，以模拟空间感和深度感==，从而在音频播放时产生更加立体的感觉，让听者感知到音频的立体位置和深度。

总的来说，双声道和立体声都指的是具有两个声道的音频，但立体声更强调在两个声道之间创造空间感和立体感的效果，而双声道更注重于两个独立声道中的不同音频内容。立体声通常会利用声音混合和处理技术，使得音频在听觉上更为丰富和立体化。

# MPEG_LAYER_MP1/2/3

这些宏定义可能是用于标识MPEG音频编码中不同的层级。

- `MPEG_LAYER_MP1`、`MPEG_LAYER_MP2`、`MPEG_LAYER_MP3`：这些宏可能分别代表MPEG音频编码中的不同层级。MPEG音频编码器通常支持多个层级，不同的层级有不同的音频压缩方法和技术。

    - `MPEG_LAYER_MP1 (1 << 2)`：可能表示MPEG音频编码的第一层级，也称为MPEG-1 Audio Layer I。这是最早的MPEG音频层级之一。
    
    - `MPEG_LAYER_MP2 (1 << 1)`：可能表示MPEG音频编码的第二层级，也称为MPEG-1 Audio Layer II或MPEG-2 Audio Layer II。这一层级通常用于CD音质或数字广播中。
    
    - `MPEG_LAYER_MP3 1`：可能表示MPEG音频编码的第三层级，也称为MPEG-1 Audio Layer III。MP3是最广为人知的MPEG音频编码层级之一，它实现了更高的压缩比，适用于音乐存储和在线传输。

这些宏定义可能用于在软件中标识和选择特定的MPEG音频编码层级，以便根据不同的要求和设备支持选择合适的编码层级。

# AAC_OBJECT_TYPE_MPEG2_AAC_LC	

这些宏定义代表不同的AAC（Advanced Audio Coding）音频编码器中的对象类型（Object Type）。AAC是一种常见的高级音频编码标准，被广泛用于音乐存储、流媒体和音频广播中。这些宏可能表示不同的AAC编码器对象类型：

- `AAC_OBJECT_TYPE_MPEG2_AAC_LC (0x80)`：可能代表MPEG-2 AAC低复杂度（Low Complexity）对象类型。这个对象类型通常用于MPEG-2标准中的AAC编码。

- `AAC_OBJECT_TYPE_MPEG4_AAC_LC (0x40)`：可能代表MPEG-4 AAC低复杂度对象类型。这种对象类型通常用于MPEG-4标准中的AAC编码，是MPEG-4标准的一部分。

- `AAC_OBJECT_TYPE_MPEG4_AAC_LTP (0x20)`：可能代表MPEG-4 AAC长时预测（Long Term Prediction）对象类型。AAC-LTP是MPEG-4标准中的一种高级编码技术，用于提高音频编码的性能。

- `AAC_OBJECT_TYPE_MPEG4_AAC_SCA (0x10)`：可能代表MPEG-4 AAC可变采样率（Scaleable Sample Rate）对象类型。这种对象类型允许编码器根据音频内容动态地调整采样率，以便更有效地压缩音频。

这些宏定义可能用于在AAC编码器中指定和选择特定的编码对象类型，以便根据不同的编码需求和设备支持选择合适的编码方式。

# HSP的音频网关服务具体是指什么

HSP（Headset Profile）是一种蓝牙配置文件，用于支持免提耳机等设备与手机或其他音频源设备之间的通信。HSP定义了一种简单的单向音频通信协议，允许通信设备（例如手机）与耳机等音频输出设备进行通信。

在HSP中，有两个角色：

1. **Headset（耳机）：** 这是接收音频的设备，通常是耳机或听筒等音频输出设备。它负责接收从音频网关（手机或其他支持HSP的设备）发送过来的音频。

2. **Audio Gateway（音频网关）：** 这是发送音频的设备，通常是手机或其他音频源设备。音频网关负责发送音频流到耳机或听筒等设备。

HSP的音频网关服务（Audio Gateway Service）是指在HSP配置文件中音频网关（手机或其他支持HSP的设备）提供的服务。该服务负责将音频流发送到免提耳机等设备。它实现了音频数据的传输和控制，允许音频源设备（如手机）将音频数据传输到耳机等设备上，实现通话或音频播放。

总的来说，HSP的音频网关服务是HSP配置文件中用于发送音频流的部分，它使得手机或其他支持HSP的设备能够将音频数据发送到耳机等音频输出设备上。

# hsp和hfp有什么区别

HSP（Headset Profile）和HFP（Hands-Free Profile）都是蓝牙配置文件，用于蓝牙设备之间的音频通信，特别是用于电话通话和音频播放。

**HSP（Headset Profile）**：
- **功能：** HSP主要用于提供基本的单向音频通信，通常用于耳机、听筒等设备。它仅支持基本的音频传输功能，没有麦克风或通话控制功能。
- **音频传输：** HSP支持从音频网关（通常是手机）到耳机等设备的音频传输。
- **控制功能：** 由于其主要用途是提供音频输出，因此HSP缺乏通话控制、麦克风和其他高级电话功能。

**HFP（Hands-Free Profile）**：
- **功能：** HFP是为了支持更全面的通话功能而设计的，不仅包括音频传输，还包括麦克风、通话控制和其他电话相关的功能。
- **音频传输：** 与HSP类似，HFP也支持从音频网关到耳机的音频传输，但同时也支持从耳机到音频网关的音频传输，以支持双向通话。
- **通话控制：** HFP包括通话控制，例如接听/挂断电话、调整音量等功能。它还支持语音识别和其他电话功能，使得设备可以更全面地与手机等音频源进行交互。

总体而言，HSP和HFP都用于蓝牙音频通信，==但HFP提供更多的电话控制和麦克风支持，适用于需要更全面通话功能的设备，比如蓝牙免提设备。而HSP更适用于只需简单音频输出的设备，如耳机或听筒。==



# bluealsa的asrsync作用是什么

用来做时间同步的。

对外的接口就2个：

```
#define asrsync_init(asrs, sr) do { asrs.rate = sr; asrs.frames = 0; \
	gettimestamp(&asrs.ts0); asrs.ts = asrs.ts0; } while(0)

int asrsync_sync(struct asrsync *asr, unsigned int frames);
```

用采样率来同步时间。

核心在这里：

```
	/* maintain constant rate */
	difftimespec(&asrs->ts0, &ts, &ts);
	if (difftimespec(&ts, &ts_rate, &asrs->ts_idle) > 0) {
		nanosleep(&asrs->ts_idle, NULL);
		rv = 1;
	}

```

这段代码是一个用于时间同步的函数`asrsync_sync`的实现。以下是对代码的解释：

1. 函数的参数`asrs`是指向时间同步结构体（`asrsync`）的指针，用于存储时间同步所需的状态和数据。
2. `frames`参数是自上一次调用该函数以来的帧数，表示音频传输期间经过的帧数。
3. 函数首先将传入的帧数累加到同步结构体中的`frames`变量中，表示总的帧数。
4. 接下来，==函数通过计算帧数与采样率的比例，将其转换为时间戳==（`ts_rate`）。
5. 函数获取当前时间戳（`ts`）并计算自上一次同步以来的时间间隔（`asrs->ts_busy`）。
6. 函数计算出维持恒定采样率所需的时间间隔（`asrs->ts_idle`）。如果当前时间间隔大于所需时间间隔，则函数通过调用`nanosleep`函数进行阻塞，以保持恒定采样率。
7. 最后，函数更新时间戳（`asrs->ts`）并返回适当的值，表示同步是否成功以及是否需要阻塞。

通过调用`asrsync_sync`函数，可以在音频传输过程中实现时间同步，确保音频数据以恒定的采样率进行处理。这对于实现音频播放的同步和质量非常重要。

# bluealsa 和bluealsa-aplay是什么关系

bluealsa是一个后台进程。

bluealsa-aplay是前台的控制命令。

他们通过自己定义的一套简单的协议进行通信。

通信渠道是一个unix socket。

通信协议就是简单的结构体。

bluealsa-aplay发送消息给bluealsa，bluealsa再通过dbus发送dbus消息给bluez。这个就是通信的完整链路。

通信协议部分的代码是在shared目录下：

```
ctl-client.h
	提供了一些bluealsa_xx的接口，相当于给前台应用提供的API。
	包括：open hci设备，subscribe事件。
	open/close/pause/drain transport
	set transport delay/volume
ctl-proto.h
	struce request 这个是主要的。
	还有一些msg_xx。
	msg_transport
	msg_device
	msg_status
	等等
ctl-socket.h
	这个主要是给hfp用的。不管。
```

播放蓝牙音乐时，是创建了一个thread，把收到的数据write到pcm里。



# bluealsa 命令参数说明

`bluealsa`命令用于启动和管理蓝牙音频服务。以下是`bluealsa`命令的一些常用参数及其说明：

```
Usage: bluealsa [OPTION]...

Options:
  -h, --help              Display help message.
  -V, --version           Display version information.

  -i, --hci=hciX          HCI device to use.
  -a, --address=XX:XX:XX:XX:XX:XX
                          Local Bluetooth adapter address.
  -p, --profile=NAME      Bluetooth profile:
                            a2dp-sink   A2DP audio sink
                            a2dp-source A2DP audio source
                            hsp-sco     HSP/HFP audio gateway
                            hfp-hf      HFP hands-free unit
                            hfp-ag      HFP audio gateway
  -n, --pcm-name=NAME    PCM device name.
  -d, --pcm-dev=NAME     PCM device directory.
  -t, --pcm-type=TYPE    PCM device type:
                            null    Null (empty) PCM device
                            pipe    Pipe PCM device
                            shm     Shared memory PCM device
                            file    File PCM device
  -m, --mtu=SIZE          Set BT socket MTU.
  -q, --quiet             Suppress any messages.
  -D, --debug             Enable debugging messages.

  -v, --verbose           Increase verbosity level.
  -c, --config=FILE       Load configuration from FILE.
```

- `-h, --help`: 显示帮助信息。
- `-V, --version`: 显示版本信息。
- `-i, --hci=hciX`: 指定要使用的HCI设备。
- `-a, --address=XX:XX:XX:XX:XX:XX`: 指定本地蓝牙适配器地址。
- `-p, --profile=NAME`: 指定要使用的蓝牙音频配置文件。
- `-n, --pcm-name=NAME`: 指定PCM设备名称。
- `-d, --pcm-dev=NAME`: 指定PCM设备目录。
- `-t, --pcm-type=TYPE`: 指定PCM设备类型。
- `-m, --mtu=SIZE`: 设置蓝牙套接字的最大传输单元。
- `-q, --quiet`: 静默模式，抑制所有消息。
- `-D, --debug`: 启用调试消息。
- `-v, --verbose`: 增加详细程度。
- `-c, --config=FILE`: 从指定的配置文件加载配置。

这些参数允许您配置`bluealsa`服务以满足特定的需求，例如选择蓝牙音频配置文件、指定PCM设备名称和类型，设置套接字MTU等。

# 音频传输过程

```
(w->pcm_fd = bluealsa_open_transport(w->ba_fd, &w->transport)) 
```



# 参考资料

1、

https://github.com/Arkq/bluez-alsa

2、基于树莓派连接天猫精灵方糖

https://www.xiangquba.cn/2020/03/29/raspberrypi_tmall_bot/

3、bluez-alsa as the default device

https://bbs.archlinux.org/viewtopic.php?id=221232

4、In Bluez A2DP: how can I modify the default audio sample rate

https://stackoverflow.com/questions/26202409/in-bluez-a2dp-how-can-i-modify-the-default-audio-sample-rate

5、

https://raspberrypi.stackexchange.com/questions/107097/bluealsa-couldnt-acquire-d-bus-name-org-bluealsa

6、

https://stackoverflow.com/questions/28191350/is-there-any-way-to-control-connected-bluetooth-device-volume-in-linux-using-com

7、Playing BlueZ on the D-Bus

https://www.landley.net/kdocs/ols/2006/ols2006v1-pages-421-426.pdf

8、**树莓派连接天猫精灵蓝牙音箱-篇1**

https://bbs.hassbian.com/thread-5375-1-1.html