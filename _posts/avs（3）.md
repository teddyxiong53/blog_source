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



#播放控制

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



#PostConnectSynchronizer

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



参考资料

1、Understanding the Amazon Alexa APIs for In-Vehicle Use: Part II

http://blog.abaltatech.com/understanding-the-amazon-alexa-apis-for-in-vehicle-use-part-ii

2、

https://github.com/alexa/avs-device-sdk/issues/743