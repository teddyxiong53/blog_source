---
title: 音频之bluealsa
date: 2019-06-17 15:10:51
tags:
	- 音频

---

1

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



参考资料

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