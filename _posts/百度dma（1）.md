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



现在我从其他地方找到一条可行的获取device info的命令。

```
10,00,05,08,14,12,01,32,
```

把这个用16进制，从蓝牙spp串口工具发送到板端。

板端有反应。

```
pi@raspberrypi:~/work/node/dma/dma_protocol-master/demo_perpheral_js$ sudo node index-rfcomm.js 
listen started { uuid: '51DBA109-5BA9-4981-96B7-6AFE132093DE', channel: 2 }
Client: B4:0B:44:F4:16:8D connected!
write version header: <Buffer@0x2ceb578 fe 04 01 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00>
write length: 20  all: 60
Received data from client:  <Buffer@0x2d0fab0 10 00 05 08 14 12 01 32>
buffer size: 8
{ headerLength: 3,
  version: 1,
  streamId: 0,
  reserveBits: 0,
  payloadLength: 5 }
onWriteRequest dmaMessage: { command: 'GET_DEVICE_INFORMATION',
  requestId: '2',
  sign2: '',
  rand2: '' }
delete all length:  8
send dma message: { command: 'GET_DEVICE_INFORMATION_ACK',
  requestId: '2',
  sign2: '',
  rand2: '',
  response: 
   { errorCode: 'SUCCESS',
     deviceInformation: 
      { supportedTransports: [Array],
        supportedAudioFormats: [Array],
        serialNumber: 'ble_test_wp20_sn',
        name: 'xhl_rpi',
        deviceType: 'HEADPHONE',
        manufacturer: 'baidu',
        model: 'xhl_rpi',
        firmwareVersion: '1.0',
        softwareVersion: '1.0',
        initiatorType: 'TAP',
        productId: '1udLzmTG2KGmKGmPkwZZe1gm',
        classicBluetoothMac: '50:1A:A5:CB:D9:F0',
        disableHeartBeat: true,
        enableAdvancedSecurity: false,
        supportFm: false,
        otaVersion: '',
        noA2dp: false,
        noAtCommand: false,
        supportBlePair: false },
     payload: 'deviceInformation' },
  payload: 'response' }
Received data from client:  <Buffer@0x2d0fab0 10 00 05 08 14 12 01 32>
buffer size: 8
{ headerLength: 3,
  version: 1,
  streamId: 0,
  reserveBits: 0,
  payloadLength: 5 }
onWriteRequest dmaMessage: { command: 'GET_DEVICE_INFORMATION',
  requestId: '2',
  sign2: '',
  rand2: '' }
delete all length:  8
send dma message: { command: 'GET_DEVICE_INFORMATION_ACK',
  requestId: '2',
  sign2: '',
  rand2: '',
  response: 
   { errorCode: 'SUCCESS',
     deviceInformation: 
      { supportedTransports: [Array],
        supportedAudioFormats: [Array],
        serialNumber: 'ble_test_wp20_sn',
        name: 'xhl_rpi',
        deviceType: 'HEADPHONE',
        manufacturer: 'baidu',
        model: 'xhl_rpi',
        firmwareVersion: '1.0',
        softwareVersion: '1.0',
        initiatorType: 'TAP',
        productId: '1udLzmTG2KGmKGmPkwZZe1gm',
        classicBluetoothMac: '50:1A:A5:CB:D9:F0',
        disableHeartBeat: true,
        enableAdvancedSecurity: false,
        supportFm: false,
        otaVersion: '',
        noA2dp: false,
        noAtCommand: false,
        supportBlePair: false },
     payload: 'deviceInformation' },
  payload: 'response' }
Received data from client:  <Buffer@0x2d0fab0 10 00 05 08 14 12 01 32>
buffer size: 8
{ headerLength: 3,
  version: 1,
  streamId: 0,
  reserveBits: 0,
  payloadLength: 5 }
onWriteRequest dmaMessage: { command: 'GET_DEVICE_INFORMATION',
  requestId: '2',
  sign2: '',
  rand2: '' }
delete all length:  8
send dma message: { command: 'GET_DEVICE_INFORMATION_ACK',
  requestId: '2',
  sign2: '',
  rand2: '',
  response: 
   { errorCode: 'SUCCESS',
     deviceInformation: 
      { supportedTransports: [Array],
        supportedAudioFormats: [Array],
        serialNumber: 'ble_test_wp20_sn',
        name: 'xhl_rpi',
        deviceType: 'HEADPHONE',
        manufacturer: 'baidu',
        model: 'xhl_rpi',
        firmwareVersion: '1.0',
        softwareVersion: '1.0',
        initiatorType: 'TAP',
        productId: '1udLzmTG2KGmKGmPkwZZe1gm',
        classicBluetoothMac: '50:1A:A5:CB:D9:F0',
        disableHeartBeat: true,
        enableAdvancedSecurity: false,
        supportFm: false,
        otaVersion: '',
        noA2dp: false,
        noAtCommand: false,
        supportBlePair: false },
     payload: 'deviceInformation' },
  payload: 'response' }
(node:25884) [DEP0005] DeprecationWarning: Buffer() is deprecated due to security and usability issues. Please use the Buffer.alloc(), Buffer.allocUnsafe(), or Buffer.from() methods instead.
write length: 134  all: 194
write length: 268  all: 462
```



nodejs版本可以学习的点：

```
opus_recorder目录
	1、buffermanager.js。基础文件的写法。Buffer的操作。
	2、recorder.js。function定义类，prototype定义。子进程产生和pipe。模块main函数。
base_channel.js：继承。方法override。
config.js：配置文件写法。
dma.js：静态方法定义。protobuf使用。
dma_recorder.js：没有使用。但是可以看里面的Promise串联用法。
index.js：ble用法。
index-rfcomm.js	：spp用方法。	
```



参考资料

1、Unified Remote: Bluetooth: Could not connect to SDP

https://askubuntu.com/questions/775303/unified-remote-bluetooth-could-not-connect-to-sdp