---
title: 百度dma（1）
date: 2018-12-20 16:11:44
tags:
	- 蓝牙
---



node.js的版本，在树莓派上跑，也可以在我的Ubuntu笔记本上跑。

dma运行。

```
Error: Cannot find module 'protobufjs'
```

安装。

```
npm install protobufjs
```

会自动下载编译不少的东西。

```
 npm install bluetooth-hci-socket
```

这个安装不成功。

```
fatal error: libudev.h: 没有那个文件或目录
```

```
sudo apt-get install libudev-dev
```

编译还是不过。

再试一下这个来安装。

```
npm install "https://github.com/jrobeson/node-bluetooth-hci-socket/#fix-builds-for-node-10"
```

这样可以成功。

运行报错。

```
teddy@teddy-ThinkPad-SL410:~/work/nodejs/dma_protocol-master/demo_perpheral_js$ UUID and NAME loaded: 0000FE04-0000-1000-8000-00805F9B34FB AirPods
BLE stateChanged to: poweredOn
advertisingStart: success
setServices:
[ PrimaryService {
    uuid: '0000FE0400001000800000805F9B34FB',
    characteristics: [ [DmaRxCharacteristic], [DmaTxCharacteristic] ] } ]
listen started { uuid: '51DBA109-5BA9-4981-96B7-6AFE132093DE', channel: 10 }
Something wrong happened!: [Error: Couldn't bind bluetooth socket. errno:98]
```



我的笔记本上安装很顺利，但是最后无法蓝牙连接上。

现在树莓派上试一下。

安装上问题更多一点。

报错：

```
Error: Could not locate the bindings file. Tried:
```

尝试解决：

```
npm install node-opus --save --unsafe-perm
```

这个可以起来了。

```
Something wrong happened!: Error: Cannot connect to SDP Daemon. errno: 2
```

这个是需要让树莓派的bluetoothd以兼容模式运行。

```
sudo vi /etc/systemd/system/bluetooth.target.wants/bluetooth.service
```

这里加上-C。表示兼容模式。

```
ExecStart=/usr/lib/bluetooth/bluetoothd -C
```

然后重启服务。

```
sudo systemctl daemon-reload
sudo systemctl restart bluetooth
sudo chmod 777 /var/run/sdp
```



看config.js里，有这个：

```
    //supportedTransports:["BLUETOOTH_LOW_ENERGY","BLUETOOTH_RFCOMM"],
    supportedTransports:["BLUETOOTH_LOW_ENERGY"],
```

是不是应该打开RFCOMM的呢？



参考资料

1、Unified Remote: Bluetooth: Could not connect to SDP

https://askubuntu.com/questions/775303/unified-remote-bluetooth-could-not-connect-to-sdp