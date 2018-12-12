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



# 查看我的手机

```
import bluetooth

target_name = "xhl_bt"
target_address = None

nearby_devices = bluetooth.discover_devices()

for bdaddr in nearby_devices:
    if target_name == bluetooth.lookup_name( bdaddr ):
        target_address = bdaddr
        break

if target_address is not None:
    print "found target bluetooth device with address ", target_address
else:
    print "could not find target bluetooth device nearby"
```



查看我的手机是否在附近。

```
teddy@teddy-ThinkPad-SL410:~/work/bt$ python test.py 
could not find target bluetooth device nearby
teddy@teddy-ThinkPad-SL410:~/work/bt$ python test.py 
found target bluetooth device with address  B4:0B:44:F4:16:8D
```

这里用到的函数就是discover_devices。



#socket编程

pybluez支持两种socket对象：rfcomm和L2CAP 。

我不能实验成功。因为我只有一个蓝牙设备。蓝牙不能自己连自己。

具体见文章，socket的建立和连接方法是跟tcpip的类似的。

# SDP协议操作

做一个sdp的server。

这么写：

```
import bluetooth

server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

port = bluetooth.get_available_port( bluetooth.RFCOMM )
server_sock.bind(("",port))
server_sock.listen(1)
print "listening on port %d" % port

uuid = "1e0ca4ea-299d-4335-93eb-27fcfe7fa848"
bluetooth.advertise_service( server_sock, "FooBar Service", uuid )

client_sock,address = server_sock.accept()
print "Accepted connection from ",address

data = client_sock.recv(1024)
print "received [%s]" % data

client_sock.close()
server_sock.close()
```

运行有问题。

```
teddy@teddy-ThinkPad-SL410:~/work/bt$ python test.py 
Traceback (most recent call last):
  File "test.py", line 7, in <module>
    port = bluetooth.get_available_port( bluetooth.RFCOMM )
AttributeError: 'module' object has no attribute 'get_available_port'
```

网上找了一下，说是get_available_port过时了。用bind到port0来替代。

还是不行，还有说需要让bluetoothd用兼容模式运行。

修改/etc/systemd/system/下面的蓝牙的文件，在bluetoothd后面加上-C。表示兼容模式运行。

然后重启蓝牙服务。

```
teddy@teddy-ThinkPad-SL410:~$ sudo systemctl restart bluetooth.service
Warning: bluetooth.service changed on disk. Run 'systemctl daemon-reload' to reload units.
teddy@teddy-ThinkPad-SL410:~$ sudo systemctl daemon-reload
```

还需要添加Profile。

````
sudo sdptool add SP
````

但是做了这些，还是不行。



# 参考资料

1、Linux 端蓝牙调试

https://blog.csdn.net/qq_18150497/article/details/51989161

2、from bluepy import btle

https://github.com/IanHarvey/bluepy/issues/197

3、MIT系列文章

https://people.csail.mit.edu/albert/bluez-intro/x264.html