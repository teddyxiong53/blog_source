---
title: 蓝牙之bluetoothctl工具使用
date: 2018-12-14 16:59:35
tags:
	- 蓝牙

---



现在树莓派和手机已经连接了。

现在从手机给树莓派发送一个文件。

安装

```
apt-get install obexpushd
```

运行，然后手机上点击分享文件，选择蓝牙就可以了。

```
root@raspberrypi:/etc/systemd/system# mkdir /ble_receive
root@raspberrypi:/etc/systemd/system# obexpushd -B -o /ble_receive -n
obexpushd 0.11.2 Copyright (C) 2006-2010 Hendrik Sattler
This software comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.
Listening on bluetooth/[00:00:00:00:00:00]:9
Creating file "/ble_receive/ceshitest.txt"
```



参考资料

1、

https://www.cnblogs.com/zjutlitao/p/9589661.html

2、树莓派体验6 - 文件传输方式 - 蓝牙

https://blog.csdn.net/messidona11/article/details/71514283