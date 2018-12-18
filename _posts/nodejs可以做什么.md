---
title: nodejs可以做什么
date: 2018-12-17 21:56:17
tags:
	- nodejs

---



nodejs实际上可以做一些什么事情？



可以写桌面应用。

https://github.com/electron/electron-quick-start

https://electronjs.org/docs/tutorial/first-app



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



# 参考资料

1、

https://github.com/noble/node-bluetooth-hci-socket/issues/84