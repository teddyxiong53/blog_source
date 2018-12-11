---
title: bluez之Python操作
date: 2018-12-11 22:06:34
tags:
	- 蓝牙

---



```\
git clone https://github.com/IanHarvey/bluepy.git
cd bluepy
python setup.py build
python setup.py install
```

上面这个会重新编译安装bluez的。我已经有了。我没有必要按照这个来。我直接pip安装就好了。

```
sudo pip install bluepy
```



先用hci的工具确认一下蓝牙设备是正常的。

然后我们写下面的测试脚本。

```
#!/usr/bin/python

from __future__ import print_function
import sys
import binascii
from bluepy import btle
import os

ble_conn = None

class MyDelegate(btle.DefaultDelegate):

    def __init__(self, conn):
        btle.DefaultDelegate.__init__(self)
        self.conn = conn

    def handleNotification(self, cHandle, data):
        data = binascii.b2a_hex(data)
        print("Notification:", str(cHandle), " data ", data)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            pass
        elif isNewData:
            print("\nDiscovery:", "MAC:", dev.addr, " Rssi ", str(dev.rssi))


def ble_connect(devAddr):
    global ble_conn
    if not devAddr is None and ble_conn is None:
        ble_conn = btle.Peripheral(devAddr, btle.ADDR_TYPE_PUBLIC)
        ble_conn.setDelegate(MyDelegate(ble_conn))
        print("connected")

def ble_disconnect():
    global ble_conn
    ble_conn = None
    print("disconnected")


if __name__ == '__main__':

    ble_mac = "00:1A:7D:DA:71:13"

    # scan 
    scanner = btle.Scanner().withDelegate(MyDelegate(None))
    timeout = 10.0
    devices = scanner.scan(timeout)
    for dev in devices:
        if dev.addr == ble_mac:
            print("\nDiscovery:", "MAC:", dev.addr, " Rssi ", str(dev.rssi))
            for (adtype, desc, value) in dev.getScanData():
                print ("  %s(0x%x) = %s" % (desc, int(adtype), value))
            break

    # connect  
    ble_connect(ble_mac)
    # write , set listen
    snd_content_str = """\x01\x00"""
    ble_conn.writeCharacteristic(handle, snd_content_str)

    # wait notification  
    ble_conn.waitForNotifications(2.0)

    # disconnect 
    ble_disconnect()

```

然后保存为test.py。

```
sudo python test.py
```

注意，蓝牙相关操作，都要用root权限。

当前运行还是会报错。

```
teddy@teddy-ThinkPad-SL410:~/work/bt$ sudo python test.py 
Traceback (most recent call last):
  File "test.py", line 57, in <module>
    ble_connect(ble_mac)
  File "test.py", line 31, in ble_connect
    ble_conn = btle.Peripheral(devAddr, btle.ADDR_TYPE_PUBLIC)
  File "/usr/local/lib/python2.7/dist-packages/bluepy/btle.py", line 361, in __init__
    self._connect(deviceAddr, addrType, iface)
  File "/usr/local/lib/python2.7/dist-packages/bluepy/btle.py", line 410, in _connect
    "Failed to connect to peripheral %s, addr type: %s" % (addr, addrType))
bluepy.btle.BTLEException: Failed to connect to peripheral 00:1A:7D:DA:71:13, addr type: public
```



# 参考资料

1、Linux 端蓝牙调试

https://blog.csdn.net/qq_18150497/article/details/51989161

2、from bluepy import btle

https://github.com/IanHarvey/bluepy/issues/197