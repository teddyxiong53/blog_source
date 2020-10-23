---
title: AIUI对接
date: 2020-09-29 14:10:30
tags:
	- 音箱

---

1

现阶段 AIUI 提供以语音交互为核心的交互解决方案，全链路聚合了**语音唤醒、语音识别、语义理解、内容（信源）平台、语音合成**等模块。可以应用于智能手机（终端）、机器人、音箱、车载、智能家居、智能客服等多种领域，让产品不仅能听会说，而且能理解会思考。

目前有如下接入方式有，Android、iOS、Windows、Linux SDK，基于 HTTP 协议的 WebAPI，以及软硬一体的AIUI 评估板（量产板）、讯飞魔飞智能麦克风。



**语音唤醒**是指通过4-6个音节的唤醒词，将设备从不对外部声音进行识别的休眠状态唤醒为接受并识别外部声音的交互状态。讯飞的语音唤醒具有小尺寸，低功耗，高唤醒的特点。并且用户可自定义唤醒词，

**单个设备最高支持8个唤醒词同时使用。**

语音降噪、回声消除、全双工交互为 AIUI 评估板（量产版）、讯飞魔飞智能麦克风、讯飞多麦克风阵列中特有的功能。

移动设备和其它普通开发板，受限于硬件能力，暂时无法实现语音降噪和全双工交互能力。

**全双工交互**指在设备扬声器发声时，且不关闭麦克风的情况下，用户可以打断设备的播放，进行语音识别和语义理解。

```
在全双工时，用户与音响的沟通如下：

用户：叮咚叮咚，今天的天气怎么样

音响：今天合肥市晴，20~26摄氏度，紫外线……

用户：（打断音响说法）明天呢

音响：明天合肥多云，22~27摄氏度，紫外线指数强，较适宜运动。

~~~~~~
区别在于第二次对话时，用户无需再说唤醒词，可以自然的进行对话。
```



## 持续录音，连续识别

AIUI 支持两种识别模式：单轮交互模式（Oneshot）和 全双工模式（Continue）



1. 基于 VAD 的自动断句或按下说的单轮交互模式。如手机 APP 或者语音电视遥控器等单麦克风设备，一般使用按下说的单轮交互，此时需要用户或程序主动触发录音，交互特点是一次触发一次响应。
2. 持续开启语音监听和识别的全双工模式。在此模式下需要设备具有较好的回声消除效果。如使用麦克风阵列的硬件，智能音箱，智能耳机等产品。**交互特点是一次触发后，可以根据业务需求保持交互状态10秒~120秒**，实现一次触发多次响应。

两种识别模式各有优劣，产品应当根据具体的产品形态和使用场景进行设计。



持续交互（continue）即全双工交互，在一次唤醒后，可以保持一段时间的唤醒（一般小于60秒），在这段时间内，可以直接与机器交互，免去唤醒词以后，会使得人机交互更加自然。



如果开发者不想集成 SDK，或者硬件性能较低，但支持 HTTP 协议时，可以选择 WebAPI 方案，WebAPI 上传音频文件，返回识别和语义理解结果。

WebAPI 的缺点是开发者需要自己实现音频流文件的前后端点判断和切割，然后再上传到 AIUI 服务器



AIUI 应用默认配置了一个语义情景模式`main`。目前 AIUI 一个应用支持配置最多10个情景模式。情景模式分为语义情景模式和翻译情景模式。



## progressive 流式识别

progressive 流式识别简称 pgs，在关闭该选项时，云端 VAD 会在用户说完一句话时返回一次识别结果。 打开该选项时，云端会在识别一句话的过程中，返回多次识别结果，并不断自动修正，

开发者如果希望在界面上实时展示修正结果以提高用户体验，可以打开该选项。

（这个对于有图形界面的有用）

##  兜底

AIUI 语义在某些语境下不能覆盖用户的所有问答，因此推出了兜底业务，AIUI 目前的兜底业务包括讯飞闲聊、图灵机器人、视频搜索、无回复兜底。



# websocket方式

https://github.com/IflytekAIUI/DemoCode/tree/master/websocket

基于 WebSocket 协议之上的实时 AIUI 交互接口协议

主要包括三个阶段：连接的建立和实时通信阶段和连接的断开。

本接口是基于会话的短连接接口，用户每次交互前需要新建连接，会话完成后，讯飞侧断开连接。单次会话过程中支持流式交互，即客户端不断上传音频等数据，讯飞侧不断下发服务结果。

WebSocket 握手阶段主要用于业务参数声明和权限校验，参数在握手请求的 url 中指定，握手请求和参数必须符合 websocket 协议规范（rfc6455）。握手成功后，服务端会保持连接 120s，超过 120s 讯飞主动断开连接。同时，讯飞侧有连接的保活监测，连续 30s 无数据交互，讯飞主动断开连接

```
ws[s]://wsapi.xfyun.cn/v1/aiui
```

Websocket 连接建立之后，进入实时通信阶段，此时客户端的主动操作有两种：上传数据和上传结束符，被动操作有两种：接收结果和错误信息

## 上传数据

在交互过程中，客户端不断构造 binary message 发送到服务端，内容是音频或文本的二进制数据。注意，分片上传时，总分片数需小于 3000，且 speex 音频每次发送的字节数应为 speex_size 的整数倍。

## 上传结束符上传结束符

在音频或文本数据上传完成后，客户端需构造一个特殊的 binary message 发送到服务端，作为发送数据结束标志，内容是字符串 "--end--" 的二进制数据。 音频最大长度不超过 60s，大小不超过 2 MB，文本最长长度不超过 1000 字节

## 接收结果

在交互过程中，服务端不断返回 text message 到客户端，包含识别、语义、后处理、vad检测等结果。当所有结果发送完毕后，服务端断开连接，交互结束

### 连接的断开

会话正常结束或异常结束时，连接的断开都是由讯飞侧发起，客户端不应主动断开连接； 连接断开有以下情况：

1. 会话正常结束，讯飞侧会在 is_finish = true 的结果下发完成后，断开连接；
2. 会话报错，讯飞侧会在下发错信息（action="error"且code不为"0")完成后，断开连接；
3. 会话超时，在连接总时长超过 2min 或连续 30s 无数据交互时，讯飞侧会断开连接。

无论上传的数据是否有效，客户端都不应主动断开连接。如果客户要中断数据上传，必须通过发送 end 指令(--end--)实现，此时讯飞会在下发完相应结果后断开连接



- continues和oneshot交互模式有什么不同？

> continues适用于一次唤醒多次交互的方式；oneshot支持一次唤醒一次交互的方式。在有麦克风阵列的移动端continues交互模式体验更加方便，在需要按住按钮说话的移动端oneshot交互模式更加适用。开发者可以根据自己的产品特性和功能进行甄选。





# AIUI SDK

看头文件。

AIUI.h

```
IAIUIEvent
IAIUIMessage
AIUIListener
	==IAIUIListener
IAIUIAgent
AIUISetting
```

我在我的笔记本上运行下载的demo。

编译：

```
samples/aiui_sample$ ./64bit_make.sh 
```

运行：

```
export LD_LIBRARY_PATH=$(pwd)/../../libs/x64/
./build/demo
```

通过命令行按键输入来进行交互的。

输入c，创建一个agent。但是当前是失败的。

看代码，是json解析失败。

看这个配置文件里，有注释。把注释去掉，还是一样。

这个代码写得非常不健壮，实际上是因为需要cd到build目录下执行才对。

当前就是配置文件根本没有找到。所以解析当然是不对的。

运行：

```
export LD_LIBRARY_PATH=$(pwd)/../../libs/x64/
cd ./build; ./demo
```

消息是这样用的。

```
void AIUITester::wakeup()
{
	if (NULL != agent)
	{
		IAIUIMessage * wakeupMsg = IAIUIMessage::create(AIUIConstant::CMD_WAKEUP);
		agent->sendMessage(wakeupMsg);
		wakeupMsg->destroy();
	}
}
```

通过给agent发送命令的方式来做。

start命令：在stop后，如果需要再次启动，则需要明确调用start。默认不需要调用start就可以用。

不能替换appid。替换后，创建agent就报错。错误码是10407，是说appid跟appkey不一致。

但是又没有找到哪里有appkey的。

当前发送文本就报错。

```
wrt
writeText
EVENT_ERROR:10103
 ERROR info is sub=, sid=cida1600ebc@dx000b12db5451040001
```



这个是sdk的文档。

https://doc.iflyos.cn/aiui/sdk/mobile_doc/#windows-linux-sdk%E6%8E%A5%E5%8F%A3

```
"tts": {
		"play_mode": "sdk",     // 播放模式，取值：sdk（内部播放，默认），user（外部自行播放）
```

可以发送给agent的消息。

https://doc.iflyos.cn/aiui/sdk/mobile_doc/msg_event.html#aiuimessage

云端接收的还是这种格式的数据。

```
aplay -c 1 -r 16000 -f S16_LE ./build/AIUI/audio/test.pcm
```

当前日志里，并没有打印语音识别的内容。

也没有听到任何的播报。

合成的tts也是这种格式的。

碰到一个问题，就是我之前是用自己的邮箱申请注册的账号，注册的一个设备，得到一个appid。然后就可以下载对应的sdk。（sdk里把appid和appkey写死到里面了）

我后面用公司的邮箱注册的设备，不能在上一次生成下载的sdk里直接改动。

而是需要重新生成sdk。这样才能正常运行。

而且，非常坑的是，默认都不配置打开NLP的。在控制台把需要的功能都打开再生成sdk。

这样就可以看到基本正常的交互逻辑。

```
EVENT_VAD:BOS
EVENT_RESULT:iat
EVENT_RESULT:nlp
EVENT_RESULT:tts
EVENT_VAD:EOS
```

输入叮咚叮咚，这个是不能被云端理解 的，所以兜底逻辑工作了。

```
{
	"intent": {
		"answer": {
			"answerType": "BottomQA",
			"emotion": "default",
			"question": {
				"question": "叮咚叮咚",
				"question_ws": "叮咚/UO//  叮咚/UO//"
			},
			"text": "说详细一点吧，我想和你好好聊天。",
			"topicID": "NULL",
			"type": "T"
		},
		"no_nlu_result": 0,
		"operation": "ANSWER",
		"rc": 0,
		"service": "iFlytekQA",
		"serviceCategory": "BottomQA",
		"serviceName": "iFlytekQA",
		"serviceType": "preventive",
		"sid": "cida711d891@dx000b12db619e010001",
		"text": "叮咚叮咚",
		"uuid": "cida711d891@dx000b12db619e010001",
		"voice_answer": [{
			"content": "说详细一点吧，我想和你[w1]好好聊天。",
			"type": "TTS"
		}]
	}
}
```

answer里的type字段：

```
显示的类型，通过这个类型，可以确定数据的返回内容和客户端的显示内容，默认值为 T 。 T：text数据 U：url数据 TU：text+url数据 IT：image+text数据 ITU：image+text+url数据
```

tts返回的json

```
{
	"data": [{
		"content": [{
			"cancel": "0",
			"cnt_id": "0",
			"dte": "pcm",
			"dtf": "audio/L16;rate=16000",
			"dts": 0,
			"error": "",
			"frame_id": 1,
			"text_end": 16,
			"text_percent": 47,
			"text_seg": "﻿说详细一点吧，",
			"text_start": 0,
			"url": "0"
		}],
		"params": {
			"cmd": "iat-kc-tts",
			"lrst": "0",
			"rstid": 1,
			"sub": "tts"
		}
	}]
}
```



关于实时的tts合成，实际上是可以的。

配置

```
	// 合成参数
	"tts": {
		"play_mode": "user",     // 播放模式，取值：sdk（内部播放，默认），user（外部自行播放）
		"buffer_time": "0",     // 音频缓冲时长，当缓冲音频大于该值时才开始播放，默认值：0ms
		"stream_type": "3",     // 播放音频流类型，取值参考AudioManager类，默认值：3
		"audio_focus": "0"      // 播放音频时是否抢占焦点，取值：1, 0（默认值）
	},
```

代码里，这里拿到的就是音频数据。

```
const char* data = event.getData()->getBinary(cnt_id.c_str(), &dataLen);
```

0表示第一帧，1表示中间帧，2表示尾帧。如果合成音频数据一帧就下发完毕，dts：3



## 问题

现在连接失败。需要抓aiui.log。把msc.cfg修改为下面这样。这样才能看到aiui.log的日志内容。

```
## Copyright (C) 2001-2016 iFLYTEK.
## Use ';' and '#' character for notation
## Note: Commands in this cfg file is case sensitive

[aiui]


[logger]
##如果用户指定的日志文件路径无效，那么MSC在运行中将不会记录日志信息
aiui-file                        = aiui.log
aiui-maxsize                     = -1
aiui-level                       = -1
file                             = msc.log
title                            = Mobile Speech Client
level                            = -1
output                           = -1
filter                           = -1
style                            = -1
flush                            = 0
maxsize                          = 100000000
overwrite                        = 1
maxfile                          = 10
cache                            = 3
```



# AIUI语义协议



参考资料

1、

https://doc.iflyos.cn/aiui/whitepaper/#%E4%BA%A7%E5%93%81%E5%AE%9A%E4%B9%89

2、

http://bbs.xfyun.cn/forum.php?mod=viewthread&tid=38759&extra=

