---
title: avs（2）
date: 2018-08-24 15:22:35
tags:
	- 音箱

---



AudioPlayer的焦点管理。



DirectiveRouter

指令路由。



里面的缩写解释：

1、ACL。Alexa通信库。完成各种网络通信的。

2、ADSL。Alexa指令排序库。管理每个指令的生命周期。

3、AFML。Activity焦点管理库。焦点是基于频道的。

4、AIP。音频输入处理。

5、ASP。音频信号处理。

6、SDS。共享数据流。

7、WWE。唤醒词引擎。

8、CA。能力代理。

其中唤醒词和ASP的库的方式提供，其余都是源代码方式提供。

这些缩写也对应了AVS系统里的主要模块。数据流转的过程是这样的。

其他缩写：

CBL：Code Based Link。在授权这里用。



代码目录结构：



AuthObserverInterface

授权观察者。



handleAuthorizationFlow

这个是授权状态机处理。



编译过程分析



在Ubuntu上运行avs。

前提：

1、Ubuntu是16.04的。

2、有Mic和音箱。



你需要先在Amazon上注册一个开发者账号。

然后创建一个Alexa设备，编辑security profile。

把product id和client id要复制保存下来，后面有用。



这个是一个较老的sample。提供比较完整。不过现在转成维护的了。

https://github.com/amzn/alexa-avs-raspberry-pi/archive/master.zip



avs的命名空间分析。

https://alexa.github.io/avs-device-sdk/namespaces.html

这里有说明。

```
最外层就是AlexaClientSDK。
命名空间跟目录层次是一样的。

```



```
AVSMessage
	AVSDirective
```

DefaultClient

这个相当于音箱端的抽象了。相当于dueros的dcsSdk。

```
using AudioInputStream = utils::sds::InProcessSDS;
```



播放，是通过回放路由来决定播放哪个的。

```
void InteractionManager::playbackPlay() {
    m_executor.submit([this]() { m_client->getPlaybackRouter()->playButtonPressed(); });
}
```

涉及PlaybackController这个类。



AVSConnectionManager

这个在acl里是重要类。



初始化过程分析：

SampleApplication::initialize这里开始。

这个函数的唯一参数是配置文件。

1、先把配置文件读取出来，json处理解析。

2、AlexaClientSDKInit::initialize，这个主要就是调用curl_global_init。

另外创建了一个http内容分析工厂，作为下面这些

3、创建m_speakMediaPlayer。创建了一个gst循环。

4、创建m_audioMediaPlayer。跟上面一样。

5、创建m_notificationsMediaPlayer。一样。

6、创建m_bluetoothMediaPlayer。一样。

7、创建m_ringtoneMediaPlayer。一样。

8、创建m_alertsMediaPlayer。一样。

9、创建一堆的SpeakerInterface，是把上面这些播放器进行类型转化得到。

10、createMediaPlayersForAdapters。这个函数当前效果会直接返回成功。

11、创建alertStorage、messageStorage、notificationsStorage、settingsStorage、miscStorage、bluetoothStorage。

12、创建HttpPut。这里会进行curl的初始化。

13、创建userInterfaceManager。

14、创建customerDataManager。

15、创建deviceInfo。

16、创建authDelegateStorage。

17、创建authDelegate。需要用到authDelegateStorage和deviceInfo

18、创建m_capabilitiesDelegate。要用到authDelegate

19、把userInterfaceManager添加给authDelegate做授权观察者，添加给m_capabilitiesDelegate做能力观察者。

20、创建internetConnectionMonitor。这个是用来监听网络连通性的。

21、创建DefaultClient。这个几乎把上面的对象都传递进去做参数了。这个很长，下面单独分析。

22、DefaultClient把设置观察者、Speaker Manager观察者、Notification观察者都设置为userInterfaceManager。

23、创建sharedDataStream。这个是一个buffer。

24、创建tapToTalkAudioProvider、holdToTalkAudioProvider、wakeWordAudioProvider。

25、创建micWrapper。

26、创建m_keywordDetector。

27、创建m_interactionManager。

28、DefaultClient把对话状态观察者设置为m_interactionManager

29、创建m_userInputManager。

30、设置endpoint，就是服务器的访问地址。

31、连接。client->connect。

32、设置默认参数。



我们重点看看client->connect做了什么。

就做了一件事情。发布能力。publishCapabilitiesAsyncWithRetries

是个异步函数。



下面看DefaultClient的初始化函数。

1、创建m_dialogUXStateAggregator。对话状态聚合。

2、创建attachmentManager。

3、创建contextManager。

4、创建m_postConnectSynchronizerFactory。

5、创建transportFactory。把m_postConnectSynchronizerFactory做参数。

6、创建m_messageRouter。消息路由。

7、创建m_connectionManager。

8、创建m_certifiedSender。

9、创建m_exceptionSender。

10、创建m_directiveSequencer。

11、创建messageInterpreter。消息解释器。

12、把上面的消息解释权注册到m_connectionManager->addMessageObserver

13、创建m_registrationManager。

14、创建m_audioActivityTracker。

15、创建m_audioFocusManager。焦点管理。

16、创建m_userInactivityMonitor。

17、创建m_audioInputProcessor。

18、创建m_speechSynthesizer。语音合成。

19、创建m_playbackController。

20、创建m_playbackRouter。

21、创建m_audioPlayer。

22、创建m_alertsCapabilityAgent。

23、创建m_notificationsCapabilityAgent。

24、创建settingsUpdatedEventSender。

25、创建m_settings。

26、创建m_speakerManager。

27、创建m_externalMediaPlayer。和上面的关系是m_speakerManager->addSpeaker(m_externalMediaPlayer)

28、创建endpointHandler

29、创建systemCapabilityProvider。

30、给m_directiveSequencer添加各种指令handler。

addDirectiveHandler的前提是：实现DirectiveHandlerInterface接口。大家都是通过继承CapabilityAgent（这里面继承了DirectiveHandlerInterface）。

```
m_speechSynthesizer
m_audioPlayer
m_externalMediaPlayer
m_audioInputProcessor
m_alertsCapabilityAgent
endpointHandler
m_userInactivityMonitor
m_speakerManager
m_notificationsCapabilityAgent
m_bluetooth
```

31、给能力代理注册各种能力。

```
capabilitiesDelegate->registerCapability
包括：
m_alertsCapabilityAgent
m_audioActivityTracker
m_audioPlayer
m_bluetooth
m_notificationsCapabilityAgent
m_playbackController
m_settings
m_speakerManager
m_audioInputProcessor
m_speechSynthesizer
systemCapabilityProvider
m_templateRuntime
m_visualActivityTracker
```





# DefaultClient函数分析

1、stopForegroundActivity

```
这个是调用到FocusManager里的同名函数。
```



# Alerts分析

AlertScheduler

AlertObserverInterface：就是状态变化监听。

Alert

AlertStorageInterface

AlertsCapabilityAgent





闹钟的状态有：

1、ready。

2、started。

3、stopped。

4、snoozed。

5、completed。

6、past_due。

7、focus_entered_foreground

8、focus_entered_background

9、error。

停止的原因有：

1、unset。

2、avs_stop

3、local_stop。

4、shutdown。

5、log_out。

传递给服务器的，代表闹钟的上下文的结构体。

ContexInfo。

```
成员有3个：
1、token。
2、type。
3、time。
```

# 指令处理过程

DirectiveSequencer，这里有个线程死循环。

```
std::thread(&DirectiveSequencer::receivingLoop, this);
```

阻塞调节是queue为空。

```
receiveDirectiveLocked
	handleDirectiveWithPolicyHandleImmediately。在DirectiveRouter里
		getHandlerAndPolicyLocked，获取到策略。
		根据策略调用handleDirectiveImmediately
		例如调用到AlertsCapabilityAgent::handleDirectiveImmediately
			executeHandleDirectiveImmediately
				就是解析json数据。
				如果是set alert，就设置闹钟。
				
```



目前从我阅读的dueros和avs来看，流程其实还好，就是c++的语法复杂。

观察者的onXxxChanged函数，不能耗时，所以需要submit到线程来异步执行。























# 参考资料

1、android音乐播放器的音频焦点控制

https://blog.csdn.net/weijun421122/article/details/44937259

2、Amazon 智能音箱 AVS Device SDK 架构详解 （智能音箱的通用架构）

https://www.wandianshenme.com/play/avs-device-sdk-architecture-overview/