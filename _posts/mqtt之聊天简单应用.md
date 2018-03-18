---
title: mqtt之聊天简单应用
date: 2017-10-08 23:25:40
tags:
	- mqtt
	- iot

---



mqtt可以用来做简单的聊天应用。

写一个client.py，内容如下。

```
#!/usr/bin/python

import paho.mqtt.client as mqtt
import json

def on_connect(client, userdata, flags, rc):
    print("connected with result code " + str(rc))
    client.subscribe("chat")
    client.publish("chat", json.dumps({"user":user, "say":"hello, everyone!"}))
    
def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    print(payload.get("user") + ":" + payload.get("say"))
    

if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    
    HOST = "127.0.0.1"
    client.connect(HOST, 1883, 60)
    user = raw_input("please input name:")
    client.user_data_set(user)
    
    client.loop_start()
    
    while True:
        str = raw_input(user)
        if str:
            client.publish("chat", json.dumps({"user":user, "say":str}))

```

测试：

1、开2个shell窗口，分别运行这个client.py脚本。

2、然后就可以在两个窗口进行聊天了。

