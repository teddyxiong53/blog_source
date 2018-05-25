---
title: dueros之Python版本
date: 2018-05-18 21:40:05
tags:
	- dueros

---



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

