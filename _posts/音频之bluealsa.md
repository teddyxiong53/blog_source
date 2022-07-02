---
title: 音频之bluealsa
date: 2019-06-17 15:10:51
tags:
	- 音频

---

--

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