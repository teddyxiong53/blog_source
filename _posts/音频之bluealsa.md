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



参考资料

1、

https://github.com/Arkq/bluez-alsa

2、基于树莓派连接天猫精灵方糖

https://www.xiangquba.cn/2020/03/29/raspberrypi_tmall_bot/

3、bluez-alsa as the default device

https://bbs.archlinux.org/viewtopic.php?id=221232