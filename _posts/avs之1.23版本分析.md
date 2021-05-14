---
title: avs之1.23版本分析
date: 2021-05-07 19:24:34
tags:
	- avs
---

--

2021年3月，avs升级到了1.23版本。

功能越来越完善，代码也越来越复杂。

抽象越来越多。阅读起来更加费力。

还是按场景分析，先从一个切入点来从上到下走一遍流程。

还是以闹钟的为例。

# 初始化流程里闹钟相关

## SampleApplication

里的initialize函数里：

有2个地方，

一个是闹钟播放器。

这个是创建播放器，然后返回接口，这就是面向接口编程的模式。

```
auto alertsMediaInterfaces = createApplicationMediaPlayer(httpContentFetcherFactory, false, "AlertsMediaPlayer");
```

一个是闹钟存储。这个很明显。没什么好说的。

```
auto alertStorage =
        alexaClientSDK::acsdkAlerts::storage::SQLiteAlertStorage::create(config, audioFactory->alerts());
```

播放器有3种选择：

1、GSTREAMER_MEDIA_PLAYER。linux默认实现。

2、ANDROID_MEDIA_PLAYER。Android默认实现。

3、CUSTOM_MEDIA_PLAYER。自己实现。

## DefaultClient

create函数

```
stubAudioPipelineFactory->addApplicationMediaInterfaces(
        acsdkAlerts::ALERTS_MEDIA_PLAYER_NAME, alertsMediaPlayer, alertsSpeaker);
```

initialize函数

```
m_alertsCapabilityAgent =
        manufactory->get<std::shared_ptr<acsdkAlertsInterfaces::AlertsCapabilityAgentInterface>>();
```

这个是Diagnotics里，用来打印alert相关信息的。

```
addAlertsObserver(deviceProperties);
```



初始化流程中，就上面2个地方。

# 目录分析

下面看看alert分布在哪些目录下。

用`find -name "*Alert*"`命令搜索。

```
./capabilities/Alerts
	这个目录下最多。
./capabilities/Alerts/acsdkAlerts/include/acsdkAlerts/Alert.h
./capabilities/Alerts/acsdkAlerts/include/acsdkAlerts/AlertsCapabilityAgent.h
./capabilities/Alerts/acsdkAlerts/include/acsdkAlerts/AlertScheduler.h
./capabilities/Alerts/acsdkAlerts/include/acsdkAlerts/AlertsComponent.h
./capabilities/Alerts/acsdkAlerts/include/acsdkAlerts/Storage/AlertStorageInterface.h
./capabilities/Alerts/acsdkAlerts/include/acsdkAlerts/Storage/SQLiteAlertStorage.h
./capabilities/Alerts/acsdkAlerts/src/Alert.cpp
./capabilities/Alerts/acsdkAlerts/src/AlertsCapabilityAgent.cpp
./capabilities/Alerts/acsdkAlerts/src/AlertScheduler.cpp
./capabilities/Alerts/acsdkAlerts/src/AlertsComponent.cpp
./capabilities/Alerts/acsdkAlerts/src/Storage/SQLiteAlertStorage.cpp
```

```
./ApplicationUtilities/Resources/Audio/src/AlertsAudioFactory.cpp
./AVSCommon/SDKInterfaces/include/AVSCommon/SDKInterfaces/Audio/AlertsAudioFactoryInterface.h
```



```
./capabilities/Alerts/acsdkAlertsInterfaces
./capabilities/Alerts/acsdkAlertsInterfaces/include/acsdkAlertsInterfaces
./capabilities/Alerts/acsdkAlertsInterfaces/include/acsdkAlertsInterfaces/AlertObserverInterface.h
./capabilities/Alerts/acsdkAlertsInterfaces/include/acsdkAlertsInterfaces/AlertsCapabilityAgentInterface.h

```

# Alert类之间关系

```
Alert
	有3个子类。
	Alarm
	Reminder
	Timer
	这3个子类，自己并没有实现什么，只是getTypeName返回值不一样。
	构造函数都是直接调用的Alert构造函数。
```

## Alert类

闹钟状态：枚举。

闹钟停止原因：枚举。

StaticData：初始化后就不会再变的数据。2个成员：token、数据库里的item id。

DynamicData：循环次数，时间点，状态。

闹钟上下文：token、类型、iso8601形式的时间点。



# Annotated机制分析

原型：

```
template <typename Annotation, typename Type>
struct Annotated {
```



Annotated是一个shared_ptr包装类。

定义一个shared_ptr，指向Type类型。

wrapper的类型，通过Annotation type来区分。

使用场景是：

你有同一个接口的多个实例。但是想要通过类型而不是指针值来区分它们。

一个例子

```
const acsdkManufactory::Annotated<
            avsCommon::sdkInterfaces::AudioFocusAnnotation,
            avsCommon::sdkInterfaces::FocusManagerInterface>& audioFocusManager
```

# Component机制

这个class，封装了这样的code：implement了一个或多个接口，依赖了0个或多个接口。

## ComponentAccumulator

组件累加器。

是一个builder风格的辅助类。



# alexa-discovery

这个是什么功能？

从名字上看，是发现。估计是设备发现相关的。

通知alexa设备信息和它连接的endpoint。

通知内容包括能力，连接信息，以及其他metadata。

http2连接的设备，在它这一边实现这个接口。

不像其他的能力，这个能力在endpoint这边不需要实现。

就是这样一个json消息

```
{
    "event" : {
        "header": {
            "namespace": "Alexa.Discovery",
            "name": "AddOrUpdateReport",
            "payloadVersion": "3",
            "messageId": "11",
            "eventCorrelationToken" : ""
        },
        "payload": {
```

# 音量问题

发现开机后，avs的音量总是100。

音量应该是从gstreamer里获取处理的。

但是是软音量。



音量操作虽然在Gstreamer和ALSA中都有，但彼此并无调用关系。
**Gstreamer中的音量调整是用软件改变PCM数据实现的，可称为软音量。**
与之相对的是音频硬件功放经扬声器所产生的音量，是为硬音量。
ALSA的音量可以是软音量，也可以是硬音量。





# 参考资料

1、

https://developer.amazon.com/en-US/docs/alexa/alexa-voice-service/alexa-discovery.html