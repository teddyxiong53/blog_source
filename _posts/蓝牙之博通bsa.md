---
title: 蓝牙之博通bsa
date: 2021-04-30 14:44:34
tags:
	- 蓝牙
---

--

博通的bsa代码，是博通自己的蓝牙框架，跟bluez、bluedroid是并列的关系。

使用了bsa，则linux不能同时用bluez。

跟bluez类似，也是CS架构。

bluez里是bluetoothd进程作为守护进程。

bsa里是bsa_server作为守护进程。

bsa不开源，bsa_server直接提供的二进制。

vendor\broadcom\brcm-bsa\3rdparty\embedded\bsa_examples\linux\ 

这个目录下，有app_manager等源代码。

看看bsa的启动脚本。

/etc/wifi/ap_name

这个名字从哪里来？

```
/etc/init.d # cat /etc/bsa/config/bt_configure.txt
bt_name=MusicBox-b2f1ec0c0376
debug=0
```

这里有代码

https://github.com/hardkernel/buildroot_linux_amlogic_brcm-bsa/tree/aml64_buildroot_master/3rdparty/embedded/bsa_examples/linux



aml_musicBox 

这个进程从哪里来？作用是什么？

./vendor/broadcom/brcm-bsa/3rdparty/embedded/bsa_examples/linux/aml_musicBox

这个代码目录编译得到。

我估计是跟bluez-alsa类似的东西，用来连接蓝牙播放音乐的。

在板端对应的配置目录

```
/etc/bsa # find -name "*"
.
./tx_test_file.txt
./config
./config/bt-avk-fifo
./config/bt-daemon-socket
./config/bt_config.xml
./config/aml_musicBox_socket
./config/ble_local_keys
./config/bt_configure.txt
./config/bt_ble_client_devices.xml
./44k8bpsStereo.wav
```

bt_config.xml里，配置了本机的蓝牙信息。

```
<X_BROADCOM_COM_BluetoothAdapter>
  <bt_config>
    <enable>1</enable>
    <visible>1</visible>
    <connectable>1</connectable>
    <local_name>MusicBox-b2f1ec0c0376</local_name>
    <bd_addr>BE:EF:BE:EF:12:67</bd_addr>
    <class_of_device>00:04:24</class_of_device>
    <pin_code>0000</pin_code>
    <pin_len>4</pin_len>
    <io_capabilities>1</io_capabilities>
    <root_path>./pictures</root_path>
  </bt_config>
</X_BROADCOM_COM_BluetoothAdapter>
```



rtk的蓝牙

配置文件在这个目录

```
/etc/bluetooth
```

```
# cat main.conf 
[General]
Name=MusicBox-ac5d5c0c3e7a
DiscoverableTimeout = 0
PairableTimeout = 0
Debug=0
Device=rtk

[Policy]
ReconnectUUIDs=0000110a-0000-1000-8000-00805f9b34fb, 00001112-0000-1000-8000-00805f9b34fb
ReconnectAttempts=7
ReconnectIntervals=1,2,4,8,16,32,64
AutoEnable=true
```

rtk的启动脚本是这个拷贝改名得到的。

```
./amlogic/bluez5-utils/bluez5_utils.mk:99:      cp -f $(TARGET_DIR)/usr/bin/bluez_tool.sh $(TARGET_DIR)/etc/init.d/S44bluetooth
```

默认是以audio sink的模式启动的

```
service_up()
{
	if [ $mode = "ble" ];then
		BLE_SERVICE
	elif [ $mode = "source" ];then
		A2DP_SOURCE_SERVICE
	else
		A2DP_SINK_SERVICE
	fi
}
```



参考资料

1、

