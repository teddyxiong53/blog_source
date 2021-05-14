---
title: avs（3）
date: 2018-10-10 11:17:51
tags:
	- 智能音箱

---



# CertifiedSender

会把消息持久化，然后一直发送直到成功。

存储消息依赖的是MessageStorageInterface。

也是存到数据库里。

主要是这2个类用到。

AlertsCapabilityAgent

SettingsUpdatedEventSender



# 播放控制

PlaybackRouterInterface

PlaybackRouter

播放暂停，都是发消息给云端的。

onContextAvailable里，取放入到队列里的按键事件。

在ContextManager::updateStatesLoop里调用。

contextManager被这些模块用到了。

1、PostConnectSynchronizer



# 分析跟avs服务端建立连接的过程

就在SampleApplication的最后。

```
    // Connect once configuration is all set.
    std::string endpoint;
    sampleAppConfig.getString(ENDPOINT_KEY, &endpoint);

    client->connect(m_capabilitiesDelegate, endpoint);

    // Send default settings set by the user to AVS.
    client->sendDefaultSettings();
```



HTTP2Transport::networkLoop



# CapabilitiesDelegate

CapabilitiesDelegate

这个主要的接口就是注册能力。





```
sqlite> select * from settings;
locale|en-US
```

```
sqlite> select * from messages
   ...> ;
1|{"event":{"header":{"namespace":"Settings","name":"SettingsUpdated","messageId":"ec23757f-aa80-4a73-9ac4-412c70785923"},"payload":{"settings":[{"key":"locale","value":"en-US"}]}}}
sqlite> 
```



```
m_contextManager->getContext
```



# PostConnectSynchronizer

这个类的作用是：

post状态同步信息给avs服务器。



# HTTP2Transport

MessageRouter::enable()这个调用MessageRouter::createActiveTransportLocked会调用HTTP2Transport的connect函数。

```
void AVSConnectionManager::enable() {
    m_isEnabled = true;
    m_messageRouter->enable();
}
```

```
void DefaultClient::onCapabilitiesStateChange(
    CapabilitiesObserverInterface::State newState,
    CapabilitiesObserverInterface::Error newError) {
    if (CapabilitiesObserverInterface::State::SUCCESS == newState) {
        m_connectionManager->enable();
    }
}
```



InteractionManager和UserInputManager二者的关系是什么？



# sampleApp命名空间下的类有哪些？

1、ConnectionObserver。

2、ConsolePrinter。

3、ConsoleReader。

4、GUIRenderer。

5、InteractionManager。

6、KeywordObserver。

7、PortAudioMircrophoneWrapper。

8、SampleApplication。

9、UIManager。

10、UserInputManager。



avs里，用move函数的，是因为对应的指针是unique_ptr的。而且定义的是时候是auto局部变量。



感觉avs的提示音体系不明显。

到现在还没有找到哪里开始建立

授权地址是：

```
static const std::string DEFAULT_LWA_BASE_URL = "https://api.amazon.com/auth/O2/";
```



AuthDelegateInterface

一种实现是CBLAuthDelegate

开始授权流程：

```
handleStarting
```

然后getRefreshTokenFailed。

然后handleRequestingCodePair

然后requestCodePair。这里有一个doPost行为。

然后InternetConnectionMonitor:startMonitoring这个是在构造函数里调用的。

方法是读取这个地址：

```
static const std::string S3_TEST_URL = "http://spectrum.s3.amazonaws.com/kindle-wifi/wifistub.html";
```

帮助信息。

```
+----------------------------------------------------------------------------+
|                                  Options:                                  |
| Tap to talk:                                                               |
|       Press 't' and Enter followed by your query (no need for the 'Alexa').|
| Hold to talk:                                                              |
|       Press 'h' followed by Enter to simulate holding a button.            |
|       Then say your query (no need for the 'Alexa').                       |
|       Press 'h' followed by Enter to simulate releasing a button.          |
| Stop an interaction:                                                       |
|       Press 's' and Enter to stop an ongoing interaction.                  |
| Playback Controls:                                                         |
|       Press '1' for a 'PLAY' button press.                                 |
|       Press '2' for a 'PAUSE' button press.                                |
|       Press '3' for a 'NEXT' button press.                                 |
|       Press '4' for a 'PREVIOUS' button press.                             |
| Settings:                                                                  |
|       Press 'c' followed by Enter at any time to see the settings screen.  |
| Speaker Control:                                                           |
|       Press 'p' followed by Enter at any time to adjust speaker settings.  |
| Firmware Version:                                                          |
|       Press 'f' followed by Enter at any time to report a different        |
|       firmware version.                                                    |
| Info:                                                                      |
|       Press 'i' followed by Enter at any time to see the help screen.      |
| Reset device:                                                              |
|       Press 'k' followed by Enter at any time to reset your device. This   |
|       will erase any data stored in the device and you will have to        |
|       re-register your device.                                             |
|       This option will also exit the application.                          |
| Quit:                                                                      |
|       Press 'q' followed by Enter at any time to quit the application.     |
+----------------------------------------------------------------------------+
```



当前我的还是有错误，进入到一个受限模式。

```
###############################################################
#       UNRECOVERABLE CAPABILITIES API ERROR: FORBIDDEN       #
#       Entering limited interaction mode.                    #
###############################################################
```

是需要根据github上的issue里的说明，在security profile里，选择other platform，而不是用默认的web方式。

下面是授权成功的打印。

```
2018-10-13 07:53:25.389 [  2] 5 HttpPost:doPostSucceeded:code=200
2018-10-13 07:53:25.389 [  2] 5 CBLAuthDelegate:receiveTokenResponse:code=200
2018-10-13 07:53:25.389 [  2] 5 CBLAuthDelegate:mapHTTPStatusToError:code=200,error=SUCCESS
2018-10-13 07:53:25.389 [  2] 5 CBLAuthDelegate:setAuthError:authError=SUCCESS
2018-10-13 07:53:25.389 [  2] 5 CBLAuthDelegate:setRefreshToken
2018-10-13 07:53:25.389 [  2] 5 SQLiteCBLAuthDelegateStorage:setRefreshToken
2018-10-13 07:53:26.201 [  2] 5 CBLAuthDelegate:handleRefreshingToken
2018-10-13 07:53:26.201 [  2] 5 CBLAuthDelegate:requestRefresh
2018-10-13 07:53:26.530 [  2] 5 HttpPost:doPostSucceeded:code=200
2018-10-13 07:53:26.531 [  2] 5 CBLAuthDelegate:receiveTokenResponse:code=200
2018-10-13 07:53:26.531 [  2] 5 CBLAuthDelegate:mapHTTPStatusToError:code=200,error=SUCCESS
2018-10-13 07:53:26.531 [  2] 5 CBLAuthDelegate:setAuthError:authError=SUCCESS
2018-10-13 07:53:26.531 [  2] 5 CBLAuthDelegate:setRefreshToken
2018-10-13 07:53:26.531 [  2] 5 SQLiteCBLAuthDelegateStorage:setRefreshToken
2018-10-13 07:53:27.115 [  2] 5 CBLAuthDelegate:setAuthState:newAuthState=REFRESHED
2018-10-13 07:53:27.115 [  2] 9 CBLAuthDelegate:callingOnAuthStateChange:state=REFRESHED,error=SUCCESS
###########################
#       Authorized!       #
###########################

2018-10-13 07:53:29.509 [  7] 5 CapabilitiesDelegate:setCapabilitiesState:newCapabilitiesState=SUCCESS
2018-10-13 07:53:29.509 [  7] 9 CapabilitiesDelegate:callingOnCapabilitiesStateChange:state=SUCCESS,error=SUCCESS
2018-10-13 07:53:29.510 [  7] 0 MessageRouter:connectionStatusChanged:reason=ACL_CLIENT_REQUEST,newStatus=PENDING
2018-10-13 07:53:29.510 [  7] 5 CBLAuthDelegate:addAuthObserver:observer=0x7f38b4101818
2018-10-13 07:53:29.511 [  8] 0 PostConnectSynchronizer:doPostConnect
2018-10-13 07:53:29.511 [  5] 1 AlertsCapabilityAgent:executeOnConnectionStatusChanged:status=PENDING,reason=ACL_CLIENT_REQUEST
#############################
#       Connecting...       #
#############################

2018-10-13 07:53:29.511 [  8] 5 PostConnectSynchronizer:setState:from=IDLE,to=RUNNING
2018-10-13 07:53:29.511 [  8] 3 HTTP2Transport:setupDownchannelStream:url=https\://avs-alexa-na.amazon.com/v20160207/directives
2018-10-13 07:53:29.511 [  9] 5 PostConnectSynchronizer:mainLoop
2018-10-13 07:53:29.511 [  9] 5 PostConnectSynchronizer:setState:from=RUNNING,to=FETCHING
2018-10-13 07:53:29.511 [  a] 5 NotificationsCapabilityAgent:provideState:stateRequestToken=1
2018-10-13 07:53:29.511 [  6] 5 NotificationsCapabilityAgent:executeProvideState:sendToken=true,stateRequestToken=1
2018-10-13 07:53:29.511 [  a] 5 AudioActivityTracker:provideState
2018-10-13 07:53:29.512 [  a] 9 SpeechSynthesizer:provideState:token=1
2018-10-13 07:53:29.512 [  a] 0 AudioPlayer:provideState:stateRequestToken=1
2018-10-13 07:53:29.512 [  b] 9 ContextManager:updateStateLocked:action=updatedState,namespace=SpeechRecognizer,name=RecognizerState
2018-10-13 07:53:29.512 [  8] 0 HTTP2StreamPool:getStream:streamId=1,numAcquiredStreams=1
2018-10-13 07:53:29.512 [  d] 0 AudioPlayer:executeProvideState:sendToken=true,stateRequestToken=1
2018-10-13 07:53:29.512 [  d] 9 ContextManager:updateStateLocked:action=updatedState,namespace=AudioPlayer,name=PlaybackState
2018-10-13 07:53:29.512 [  e] 5 AudioActivityTracker:executeProvideState
2018-10-13 07:53:29.512 [  e] 9 ContextManager:updateStateLocked:action=updatedState,namespace=AudioActivityTracker,name=ActivityState
2018-10-13 07:53:29.512 [  c] 0 SpeechSynthesizer:executeProvideState:stateRequestToken=1
2018-10-13 07:53:29.512 [  c] 9 ContextManager:updateStateLocked:action=updatedState,namespace=SpeechSynthesizer,name=SpeechState
2018-10-13 07:53:29.512 [  f] 0 ExternalMediaPlayer:executeProvideState:sendToken=true,stateRequestToken=1
2018-10-13 07:53:29.512 [  6] 9 ContextManager:updateStateLocked:action=updatedState,namespace=Notifications,name=IndicatorState
2018-10-13 07:53:29.513 [  f] 9 ContextManager:updateStateLocked:action=updatedState,namespace=ExternalMediaPlayer,name=ExternalMediaPlayerState
2018-10-13 07:53:29.513 [  f] 0 ExternalMediaPlayer:executeProvideState:sendToken=true,stateRequestToken=1
2018-10-13 07:53:29.513 [  f] 9 ContextManager:updateStateLocked:action=updatedState,namespace=Alexa.PlaybackStateReporter,name=playbackState
2018-10-13 07:53:29.513 [  a] 9 ContextManager:buildContextIgnored:namespace=AudioActivityTracker,name=ActivityState
2018-10-13 07:53:29.513 [  a] 5 ContextManager:buildContextSuccessful
2018-10-13 07:53:29.513 [  a] 5 PostConnectSynchronizer:onContectAvailable
2018-10-13 07:53:29.513 [  a] 5 PostConnectSynchronizer:setState:from=FETCHING,to=SENDING
2018-10-13 07:53:29.513 [  a] 0 EventBuilder:buildJsonEventString:messageId=d09b1a09-d522-4da5-8ddb-63cd9813db79,namespace=System,name=SynchronizeState
2018-10-13 07:53:29.514 [  a] 9 HTTP2Transport:enqueueRequest
2018-10-13 07:53:30.881 [  8] 0 HTTP2Stream:receivedRequestId:value=x-amzn-requestid\: 0a93fcfffe1ce4a4-0000659c-003942ed-ea811cd9f66c3dd7-ced9c39f-1
2018-10-13 07:53:30.881 [  8] 0 HTTP2Transport:processNextOutgoingMessage
2018-10-13 07:53:30.881 [  8] 0 HTTP2StreamPool:getStream:streamId=3,numAcquiredStreams=2
2018-10-13 07:53:30.881 [  8] 9 HTTP2Transport:insertActiveStream:handle=0x7f38fc0eceb0
2018-10-13 07:53:31.510 [  8] 0 HTTP2Stream:receivedRequestId:value=x-amzn-requestid\: 0a93fcfffe1ce4a4-0000659c-003942ed-ea811cd9f66c3dd7-ced9c39f-3
2018-10-13 07:53:31.510 [  8] 5 PostConnectSynchronizer:onSendCompleted:status=SUCCESS_NO_CONTENT
2018-10-13 07:53:31.510 [  8] 5 PostConnectSynchronizer:stop
2018-10-13 07:53:31.510 [  8] 5 PostConnectSynchronizer:setState:from=SENDING,to=STOPPING
2018-10-13 07:53:31.510 [  9] 5 PostConnectSynchronizer:mainLoopReturning
2018-10-13 07:53:31.511 [  8] 5 PostConnectSynchronizer:setState:from=STOPPING,to=STOPPED
2018-10-13 07:53:31.511 [  8] 0 MessageRouter:connectionStatusChanged:reason=ACL_CLIENT_REQUEST,newStatus=CONNECTED
2018-10-13 07:53:31.511 [  8] 0 HTTP2Transport:cleanupFinishedStream:streamId=3,result=204
2018-10-13 07:53:31.511 [  8] 0 HTTP2StreamPool:releaseStream:streamId=3,numAcquiredStreams=1
2018-10-13 07:53:31.511 [  8] 0 CurlEasyHandleWrapper:reset:responseCode=HTTP_RESPONSE_SUCCESS_NO_CONTENT
2018-10-13 07:53:31.511 [  5] 1 AlertsCapabilityAgent:executeOnConnectionStatusChanged:status=CONNECTED,reason=ACL_CLIENT_REQUEST
########################################
#       Alexa is currently idle!       #
########################################

2018-10-13 07:53:31.511 [  8] 0 PostConnectSynchronizer:~PostConnectSynchronizer
2018-10-13 07:53:31.511 [  8] 5 PostConnectSynchronizer:stop
2018-10-13 07:53:31.511 [  8] 5 PostConnectSynchronizer:stopIgnored:reason=alreadyStopped
2018-10-13 07:53:31.511 [ 10] 9 HTTP2Transport:enqueueRequest
2018-10-13 07:53:31.511 [  8] 0 HTTP2Transport:processNextOutgoingMessage
2018-10-13 07:53:31.511 [  8] 0 HTTP2StreamPool:getStream:streamId=5,numAcquiredStreams=2
2018-10-13 07:53:31.511 [  8] 9 HTTP2Transport:insertActiveStream:handle=0x7f38fc0eceb0
2018-10-13 07:53:31.901 [  8] 0 HTTP2Stream:receivedRequestId:value=x-amzn-requestid\: 0a93fcfffe1ce4a4-0000659c-003942ed-ea811cd9f66c3dd7-ced9c39f-5
2018-10-13 07:53:31.901 [  8] 0 HTTP2Transport:cleanupFinishedStream:streamId=5,result=204
2018-10-13 07:53:31.901 [  8] 0 HTTP2StreamPool:releaseStream:streamId=5,numAcquiredStreams=1
2018-10-13 07:53:31.901 [  8] 0 CurlEasyHandleWrapper:reset:responseCode=HTTP_RESPONSE_SUCCESS_NO_CONTENT

```

输入一个t，相当于唤醒音箱。然后进入listen和think状态。

看看打印。



# UserInactivityMonitor

这个类的作用是：

一个小时发送一次。

buildJsonEventString

# DialogUXStateAggregator

这个是聚合器。



# SpeechSynthesizer

看看语音合成是怎么做的 。



# 按下play后的执行过程

```
1、输入按键1，调用m_interactionManager->playbackPlay();
2、在InteractionManager里，调用m_client->getPlaybackRouter()->playButtonPressed()。
3、在PlaybackRouter里，调用observer->onButtonPressed(button);这个做的事情就是把button推入到一个队列里。
4、从队列里取按键的有PlaybackController::onContextAvailable
这里m_messageSender->sendMessage。把按键发送到服务器端。

```



# 消息路由如何工作的？

1、在DefaultClient里构造的。

```
m_messageRouter = std::make_shared<acl::MessageRouter>(authDelegate, attachmentManager, transportFactory);
```

参数里的传输工厂是m_postConnectSynchronizerFactory。



# ContextManager如何工作？

主要就上一个线程updateStatesLoop。

不断在更新状态。

ContextManager::sendContextAndClearQueue

里面会调用onContextAvailable



# 测试网络连接的情况

默认每5分钟测试一次，读取一个网页，查找里面的一个字符串。



# 如何运行测试代码？

在build目录下，make help看看。

```
hlxiong@hlxiong-VirtualBox:~/work/avs/sdk-folder/sdk-build$ make help
The following are some of the valid targets for this Makefile:
... all (the default if no target is provided)
... clean
... depend
... list_install_components
... install
... rebuild_cache
... edit_cache
... install/strip
... unit
... ContinuousSubmit
... ContinuousCoverage
... ContinuousTest
... ContinuousBuild
... ContinuousMemCheck
... Nightly
... NightlyTest
... NightlyUpdate
```

我们就以TimerTest为例，进行测试看看。

```
make TimerTest
```

```
lxiong@hlxiong-VirtualBox:~/work/avs/sdk-folder/sdk-build$ find -name TimerTest
./AVSCommon/Utils/test/TimerTest
hlxiong@hlxiong-VirtualBox:~/work/avs/sdk-folder/sdk-build$ ./AVSCommon/Utils/test/TimerTest
2018-10-15 08:14:08.178 [  1] I sdkVersion: 1.7.1
Running main() from gtest_main.cc
[==========] Running 18 tests from 1 test case.
[----------] Global test environment set-up.
[----------] 18 tests from TimerTest
[ RUN      ] TimerTest.singleShot
[       OK ] TimerTest.singleShot (33 ms)
[ RUN      ] TimerTest.multiShot
[       OK ] TimerTest.multiShot (151 ms)
[ RUN      ] TimerTest.multiShotWithDelay
[       OK ] TimerTest.multiShotWithDelay (166 ms)
[ RUN      ] TimerTest.forever
[       OK ] TimerTest.forever (150 ms)
[ RUN      ] TimerTest.slowTaskLessThanPeriod
[       OK ] TimerTest.slowTaskLessThanPeriod (256 ms)
[ RUN      ] TimerTest.slowTaskGreaterThanPeriod
[       OK ] TimerTest.slowTaskGreaterThanPeriod (197 ms)
[ RUN      ] TimerTest.slowTaskGreaterThanTwoPeriods
[       OK ] TimerTest.slowTaskGreaterThanTwoPeriods (200 ms)
[ RUN      ] TimerTest.endToStartPeriod
[       OK ] TimerTest.endToStartPeriod (387 ms)
[ RUN      ] TimerTest.stopSingleShotBeforeTask
[       OK ] TimerTest.stopSingleShotBeforeTask (30 ms)
[ RUN      ] TimerTest.stopSingleShotDuringTask
[       OK ] TimerTest.stopSingleShotDuringTask (62 ms)
[ RUN      ] TimerTest.stopSingleShotAfterTask
[       OK ] TimerTest.stopSingleShotAfterTask (78 ms)
[ RUN      ] TimerTest.stopMultiShot
[       OK ] TimerTest.stopMultiShot (123 ms)
[ RUN      ] TimerTest.startRunningBeforeTask
2018-10-15 08:14:10.015 [  1] E Timer:startFailed:reason=timerAlreadyActive
[       OK ] TimerTest.startRunningBeforeTask (31 ms)
[ RUN      ] TimerTest.startRunningDuringTask
2018-10-15 08:14:10.092 [  1] E Timer:startFailed:reason=timerAlreadyActive
[       OK ] TimerTest.startRunningDuringTask (60 ms)
[ RUN      ] TimerTest.startRunningAfterTask
[       OK ] TimerTest.startRunningAfterTask (77 ms)
[ RUN      ] TimerTest.deleteBeforeTask
[       OK ] TimerTest.deleteBeforeTask (0 ms)
[ RUN      ] TimerTest.deleteDuringTask
[       OK ] TimerTest.deleteDuringTask (64 ms)
[ RUN      ] TimerTest.startRunningAfterStopDuringTask
[       OK ] TimerTest.startRunningAfterStopDuringTask (92 ms)
[----------] 18 tests from TimerTest (2158 ms total)

[----------] Global test environment tear-down
[==========] 18 tests from 1 test case ran. (2160 ms total)
[  PASSED  ] 18 tests.
```





# UIManager和UserInputManager

这2个是不同的。

UIManager里面主要就是各种打印。主要处理输出。如果有led灯什么的，也是需要在这里加。

继承了一大堆的观察者类。

然后还每个状态都定义了一个成员变量。



UserInputManager主要是处理按键输入。按键输入的在这里加。

InteractionManager

这个主要是函数被UserInputManager调用，里面都是submit的方式来处理的。



# 状态变化

语音输入状态有：

AudioInputProcessorObserverInterface

1、idle。

2、expecting_speech。

3、recognizing。

4、busy。

语音输出状态：

SpeechSynthesizerObserverInterface

1、playing。

2、finished。

3、gaining_focus。

4、losing_focus。

呈现给用户的状态是DialogUXState：

1、idle。

2、listening。

3、thinking。

4、speaking。

5、finished。



avs的thinking时间是5秒，而dueros的是8秒。

```
DialogUXStateAggregator(std::chrono::milliseconds timeoutForThinkingToIdle = std::chrono::seconds{5});
```



# http

这些类，都只有一个接口create。

```
HTTPContentFetcherInterfaceFactoryInterface
	HTTPContentFetcherFactory：create调用下面的构造方法。
		LibCurlHttpContentFetcher 这里就是实现了。
			CurlEasyHandleWrapper
```



# HttpPut

HttpPutInterface

里面就一个doPut函数。

HttpPut

实现doPut函数。另外有一个CurlEasyHandleWrapper成员变量。

# HttpPost

HttpPostInterface

3个doPost函数。

HttpPost

实现doPost。

# HTTPResponse

2个成员：一个long code，一个string的body。



共用一个httpPut，httpPost则不是。



# AttachmentManager

AttachmentManagerInterface

2个方法：

createWriter

createReader

AttachmentManager



很多的对象，内部都有一个循环。

# AudioActivityTracker

这个类是把焦点信息报告给avs服务器的。



# 系统架构

输入AIP

输出speechSynthesizer

播放器：m_playbackController

m_audioPlayer

闹钟

m_alertsCapabilityAgent

数据流：sds。



# AudioProvider

有3种：

1、按一下按键的。

2、按住按键的。

3、唤醒词的。

# AudioFormat

1、枚举Encoding。lpcm和opus两种。

2、枚举Layout。间隔和非间隔。

3、枚举。Endianness。大端小端。

4、几个成员变量。



# sds

这个主要是被各种模板嵌套，搞得非常复杂。

但是还是要啃下来。



# 焦点

会获取焦点的模块有：

1、闹钟。

```
void AlertsCapabilityAgent::acquireChannel() 
```

2、AIP。

3、AudioPlayer。

4、蓝牙播放器。

5、语音输出。



# AIP

如何把输入的语音取出来的？

以tap方式唤醒为例。

调用到DefaultClient里的notifyOfTapToTalk

```
m_audioInputProcessor->recognize
```



# HTTP2Transport

networkLoop

这个主循环。要方式的数据，都放到队列，通过这个死循环来处理。

HTTP2Stream

HTTP2Transport

HTTP2StreamPool



# CurlMultiHandleWrapper



# 蓝牙是如何工作的？





参考资料

1、Understanding the Amazon Alexa APIs for In-Vehicle Use: Part II

http://blog.abaltatech.com/understanding-the-amazon-alexa-apis-for-in-vehicle-use-part-ii

2、

https://github.com/alexa/avs-device-sdk/issues/743