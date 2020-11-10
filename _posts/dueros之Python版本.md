---
title: dueros之Python版本
date: 2018-05-18 21:40:05
tags:
	- dueros

---



# 先跑起来

先要授权。

```
teddy@teddy-ThinkPad-SL410:~/work/dueros/python/DuerOS-Python-Client-master$ ./auth.sh 
A web page should is opened. If not, go to http://127.0.0.1:3000 to start
{"expires_in":2592000,"refresh_token":"22.ba1b5da40c9b260a553bcad7cd0f8891.315360000.1855970949.1711386190-10189374","access_token":"21.999ead980123127f75c65580e44d5243.2592000.1543202949.1711386190-10189374","session_secret":"f0c0c7ca11a4c2ce18bd2760b4cc1d4f","session_key":"9mnRfQO7MXZ\/RnryFP6bJcc8Jlmc+ewM3deg+i2H4s6lgeVZpDCrCzWo2xPTBhekKEJ\/u1CYLc7FEyWh9S5zPZS5MW35tOwqvhc=","scope":"basic"}
```

然后用

enter_trigger_start.sh来运行。

按一下回车键，就相当于唤醒了音箱。目前交互是正常的。

```
hlxiong@hlxiong-VirtualBox:~/work/test/dueros/DuerOS-Python-Client$ cat ~/.dueros.json 
{
    "dueros-device-id": "EddyLiu-1d2dd765aa6642c9ad37370aa60e5c41", 
    "access_token": "21.4692dd1f1564f744f874c5d5701094ba.2592000.1561097983.1711386190-10189374", 
    "expiry": "Fri Jun 21 06:19:43 2019", 
    "client_id": "5GFgMRfHOhIvI0B8AZB78nt676FeWA9n", 
    "client_secret": "eq2eCNfbtOrGwdlA4vB1N1EaiwjBMu7i", 
    "refresh_token": "22.f9f533a639fb4d311f628d6f8424c444.315360000.1873865983.1711386190-10189374"
}
```



# 代码分析

代码在这里。

https://github.com/MyDuerOS/DuerOS-Python-Client.git

```
teddy@teddy-ubuntu:~/work/dueros/DuerOS-Python-Client-master$ tree
.
├── app
│   ├── app_config.py
│   ├── auth.py
│   ├── enter_trigger_main.py
│   ├── framework
│   │   ├── __init__.py
│   │   ├── mic.py
│   │   └── player.py
│   ├── __init__.py
│   ├── resources
│   │   └── du.mp3
│   ├── snowboy
│   │   ├── demo2.py
│   │   ├── demo3.py
│   │   ├── demo_arecord.py
│   │   ├── demo.py
│   │   ├── demo_threaded.py
│   │   ├── __init__.py
│   │   ├── requirements.txt
│   │   ├── resources
│   │   │   ├── alexa
│   │   │   │   ├── alexa_02092017.umdl
│   │   │   │   ├── alexa-avs-sample-app
│   │   │   │   │   └── alexa.umdl
│   │   │   │   └── SnowboyAlexaDemo.apk
│   │   │   ├── alexa.umdl
│   │   │   ├── common.res
│   │   │   ├── ding.wav
│   │   │   ├── dong.wav
│   │   │   ├── snowboy.umdl
│   │   │   └── snowboy.wav
│   │   ├── snowboydecoder_arecord.py
│   │   ├── snowboydecoder.py
│   │   ├── snowboydetect.py
│   │   ├── _snowboydetect.so
│   │   ├── snowboythreaded.py
│   │   └── xiaoduxiaodu_all_10022017.umdl
│   ├── utils
│   │   ├── __init__.py
│   │   ├── mic_data_saver.py
│   │   └── prompt_tone.py
│   └── wakeup_trigger_main.py
├── auth.sh
├── enter_trigger_start.sh
├── LICENSE
├── README.md
├── readme_resources
│   └── 代码结构.png
├── sdk
│   ├── auth.py
│   ├── configurate.py
│   ├── dueros_core.py
│   ├── __init__.py
│   ├── interface
│   │   ├── alerts.py
│   │   ├── audio_player.py
│   │   ├── __init__.py
│   │   ├── notifications.py
│   │   ├── playback_controller.py
│   │   ├── screen_display.py
│   │   ├── speaker.py
│   │   ├── speech_recognizer.py
│   │   ├── speech_synthesizer.py
│   │   └── system.py
│   ├── resources
│   │   ├── alarm.wav
│   │   └── README.md
│   └── sdk_config.py
└── wakeup_trigger_start.sh
```

3个工具脚本都是shell脚本。

目录2个。

1、app。

2、sdk。

授权的调用过程：

```
auth.sh
	app/auth.py
		sdk/auth.py
```

保存的授权信息在主目录下的.dueros.json里。

```
teddy@teddy-ThinkPad-SL410:~$ cat .dueros.json 
{
    "dueros-device-id": "EddyLiu-07c24d76c26d49608e7b39f9a86d8c3b", 
    "access_token": "21.999ead980123127f75c65580e44d5243.2592000.1543202949.1711386190-10189374", 
    "expiry": "Mon Nov 26 03:29:09 2018", 
    "client_id": "5GFgMRfHOhIvI0B8AZB78nt676FeWA9n", 
    "client_secret": "eq2eCNfbtOrGwdlA4vB1N1EaiwjBMu7i", 
    "refresh_token": "22.ba1b5da40c9b260a553bcad7cd0f8891.315360000.1855970949.1711386190-10189374"
}
```



先看看授权是怎么做的。

需要一个client id和一个client secret。

调用的是

```
login(client_id, client_secret)
```

网址可以是自己搭建的本地服务器。

```
webbrowser.open('http://127.0.0.1:3000')
```

看起来这个login没有做什么。

```
def login(client_id, client_secret):
    '''
    初始化Tornado　web server
    :param client_id: 开发者信息
    :param client_secret: 开发者信息
    :return:
    '''
    application = tornado.web.Application([(r".*", MainHandler,
                                            dict(output=configurate.DEFAULT_CONFIG_FILE, client_id=client_id,
                                                 client_secret=client_secret))])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(3000)
    tornado.ioloop.IOLoop.instance().start()
    tornado.ioloop.IOLoop.instance().close()
```

关键是get函数。

往百度的token_url和oauth_url发了请求，把数据保存到本地。

之所以要用一个webserver，是用来redirect数据到百度服务器的。



先不管，继续看看。

这个是用enter键来触发唤醒的。

```
# ./enter_trigger_start.sh
```

main函数：

```
	# 创建录音设备（平台相关）
    audio = Audio()
    # 创建播放器（平台相关）
    player = Player()
    # 构造一个dueros的实例。
    dueros = DuerOS(player)
    # 设置指令监听回调。
    # 这个回调就是打印指令。
    dueros.set_directive_listener(directive_listener)
    
    audio.link(dueros)

    dueros.start()
    audio.start()
```



```
audio --> dueros --> player
```



使用的是gst来进行声音的播放的。

这个产品的逻辑上来说，其实是很简单的。

就是录音，往服务器发，收到返回结果，播放出来。就这么几步。

都不带转弯的。

# 打开唤醒词

这个直接运行会报错。

网上查了，说是因为是树莓派的，需要重新编译对应的_snowboydetector.so文件。

但是官网说只支持64位的Ubuntu。

算了。暂时不管这个了。



# DuerOS类分析

这个是在dueros_core.py文件里。

这个是聚合性质的类。



## 初始化函数

成员变量：

1、事件队列event_queue。

2、语音识别speech_recognizer。

3、语音合成speech_synthesizer。

4、音频播放器audio_player。

5、speaker。

6、alerts。

7、system。



下面是按键唤醒后，什么都不说，等到超时的时候，然后播放没有听到你说了什么时的打印。

```
INFO:sdk.dueros_core:Found 212 bytes of None application/json, first_payload_block=True
INFO:sdk.dueros_core:Found 0 bytes of None application/json, first_payload_block=False
INFO:sdk.dueros_core:Finished downloading JSON
INFO:root:云端下发directive:{u'header': {u'dialogRequestId': u'7790d0aa194845a3b359dc8ce600c033', u'namespace': u'ai.dueros.device_interface.voice_input', u'name': u'StopListen', u'messageId': u'b580fc3a269b478dbf4fe6f9adfd1be7'}, u'payload': {}}
INFO:SpeechRecognizer:StopCapture
INFO:root:[DuerOS状态]正在思考.........
INFO:sdk.dueros_core:wait for response
INFO:hyper.http20.connection:Received unhandled event <WindowUpdated stream_id:0, delta:320>
INFO:hyper.http20.connection:Received unhandled event <WindowUpdated stream_id:5, delta:320>
INFO:hyper.http20.connection:Received unhandled event <WindowUpdated stream_id:0, delta:24>
INFO:sdk.dueros_core:status code: 200
INFO:sdk.dueros_core:Found 388 bytes of None application/json, first_payload_block=True
INFO:sdk.dueros_core:Found 0 bytes of None application/json, first_payload_block=False
INFO:sdk.dueros_core:Finished downloading JSON
INFO:sdk.dueros_core:Found 0 bytes of <4487999> application/octet-stream, first_payload_block=True
INFO:sdk.dueros_core:Found 3132 bytes of <4487999> application/octet-stream, first_payload_block=False
INFO:sdk.dueros_core:Found 0 bytes of <4487999> application/octet-stream, first_payload_block=False
INFO:sdk.dueros_core:Finished downloading application/octet-stream which is <4487999>
INFO:sdk.dueros_core:write audio to 4487999.mp3
INFO:root:云端下发directive:{u'header': {u'dialogRequestId': u'7790d0aa194845a3b359dc8ce600c033', u'namespace': u'ai.dueros.device_interface.voice_output', u'name': u'Speak', u'messageId': u'NWQwNGJhMzExYzgwMjE4NDc='}, u'payload': {u'url': u'cid:4487999', u'token': u'eyJib3RfaWQiOiJ1cyIsInJlc3VsdF90b2tlbiI6IjdlNzdiMjU5YzEyZjg4OGEwMDBjZDYzNzQ0NzE3YjdjIiwiYm90X3Rva2VuIjoibnVsbCIsImxhdW5jaF9pZHMiOlsiIl19', u'format': u'AUDIO_MPEG'}}
INFO:root:[DuerOS状态]正在播放........
INFO:root:[DuerOS状态]结束
INFO:root:[DuerOS状态]结束
INFO:sdk.dueros_core:wait for response
INFO:hyper.http20.connection:Received unhandled event <WindowUpdated stream_id:0, delta:1247>
INFO:sdk.dueros_core:status code: 204
```

看看上面把播报音频下载成文件再播放的过程。



# 参考资料

1、【DuerOS开发日记】2.打造属于自己的小度(1)：使用PythonSDK

https://blog.csdn.net/b735098742/article/details/78445969

2、运行./wakeup_trigger_start.sh报错

https://github.com/MyDuerOS/DuerOS-Python-Client/issues/10

3、snowboy官网文档

http://docs.kitt.ai/snowboy/