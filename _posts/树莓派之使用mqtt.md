---
title: 树莓派之实用mqtt
date: 2017-09-21 20:59:16
tags:
	- 树莓派
	- mqtt

---



mosquitto是一个实现了mqtt3.1协议的代理服务器。这个词比mosquito（蚊子）多了一个t。



# 1、 在树莓派上安装mosquitto

`wget http://mosquitto.org/files/source/mosquitto-1.3.4.tar.gz`

然后是解压编译安装。编译会出现下面的错误：

1、找不到`openssl/ssl.h`

解决方法：`sudo apt-get install libssl-dev`。

2、找不到`ares.h`

修改config.mk中的WITH_SRV:=yes，改为WITH_SRV:=no

3、`fatal error: uuid/uuid.h: No such file or directory`

这个是因为没有uuid的库。

解决方法：`sudo apt-get install uuid-dev`。

sudo make install。安装支持。

# 2、 基本使用

启动mosquitto服务。v参数表示verbose。

这个shell，我们叫A窗口。

```
pi@raspberrypi:~/work/iot/mqtt/mosquitto-1.4.5$ mosquitto -v
1505999684: mosquitto version 1.4.5 (build date 2017-09-21 13:04:13+0000) starting
1505999684: Using default config.
1505999684: Opening ipv4 listen socket on port 1883.
1505999684: Opening ipv6 listen socket on port 1883.

```



再开一个shell窗口，叫B窗口。使用mosquitto_sub报错了。

```
pi@raspberrypi:~$ mosquitto_sub -v -t gpio -h 127.0.0.1
mosquitto_sub: error while loading shared libraries: libmosquitto.so.1: cannot open shared object file: No such file or directory
pi@raspberrypi:~$ 
```

解决方法：

创建一个软链接：

`sudo ln -s /usr/local/lib/libmosquitto.so.1 /usr/lib/libmosquitto.so.1`

更新一下链接配置。`sudo ldconfig`。

这时，我们看之前启动mosquitto服务的那个shell下面打印了这些：

```
1506000222: New connection from 127.0.0.1 on port 1883.
1506000222: New client connected from 127.0.0.1 as mosqsub/9126-raspberryp (c1, k60).
1506000222: Sending CONNACK to mosqsub/9126-raspberryp (0, 0)
1506000222: Received SUBSCRIBE from mosqsub/9126-raspberryp
1506000222:     gpio (QoS 0)
1506000222: mosqsub/9126-raspberryp 0 gpio
1506000222: Sending SUBACK to mosqsub/9126-raspberryp
```

再起一个shell窗口。叫做窗口C。到目前总共起了3个shell窗口了。

这个是为了发布一条消息。

```
mosquitto_pub -t gpio -h 127.0.0.1 -m "{\"pin\":17,\"value\":0}"
```

这时候，窗口A产生了下面的打印。

```
1506000282: Received PINGREQ from mosqsub/9126-raspberryp
1506000282: Sending PINGRESP to mosqsub/9126-raspberryp
1506000324: New connection from 127.0.0.1 on port 1883.
1506000324: New client connected from 127.0.0.1 as mosqpub/9139-raspberryp (c1, k60).
1506000324: Sending CONNACK to mosqpub/9139-raspberryp (0, 0)
1506000324: Received PUBLISH from mosqpub/9139-raspberryp (d0, q0, r0, m0, 'gpio', ... (20 bytes))
1506000324: Sending PUBLISH to mosqsub/9126-raspberryp (d0, q0, r0, m0, 'gpio', ... (20 bytes))
1506000324: Received DISCONNECT from mosqpub/9139-raspberryp
1506000324: Client mosqpub/9139-raspberryp disconnected.
```

窗口B产生了下面的打印。

```
pi@raspberrypi:~$ mosquitto_sub -v -t gpio -h 127.0.0.1
gpio {"pin":17,"value":0}
```



# 3、 高级一点的玩法

下面我们借助python-gpio库，通过mqtt消息来实现gpio端口的控制。

首先在树莓派上安装paho-mqtt。

`sudo pip install paho-mqtt`

然后写一个Python脚本，名字叫mqtt_ctrl_gpio.py。内容如下：

```
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import json

pins = [17]

def gpio_setup():
	GPIO.setmode(GPIO.BCM)
	for pin in pins:
		GPIO.setup(pin, GPIO.OUT)
		GPIO.output(pin, GPIO.LOW)
		
def gpio_destroy():
	for pin in pins:
		GPIO.outpu(pin, GPIO.LOW)
		GPIO.setup(pin, GPIO.IN)
		
def on_connect(client, userdata, flags, rc):
	print "connected with result code" + str(rc)
	client.subscribe("gpio")
	
def on_message(client, userdata, msg):
	print msg.topic + " " + str(msg.payload)
	gpio = json.loads(str(msg.payload))
	if gpio['pin'] in pins:
		if gpio['value'] == 0:
			GPIO.output(gpio['pin'], GPIO.LOW)
		else:
			GPIO.output(gpio['pin'], GPIO.HIGH)

if __name__ == "__main__":
	client = mqtt.Client()
	client.on_connect = on_connect
	client.on_message = on_message
	gpio_setup()
	try:
		client.connect("127.0.0.1", 1883, 60)
		client.loop_forever()
	catch KeyboardInterrupt:
		client.disconnect()
		gpio_destroy()
```

在一个shell窗口里运行这个脚本，这个脚本的地位就相当于上面的mosquitto_sub程序的作用。

