---
title: avs之音频输入分析
date: 2018-11-10 14:59:19
tags:
	- avs
---



AudioProvider

AudioInputStream

SharedDataStream 这个是一个类模板。



executeRecognize这个函数是如何把输入音频上传到avs服务器的呢？

创建了一个reader。

```
m_reader = avsCommon::avs::attachment::InProcessAttachmentReader::create(
```

看这个read函数如何调用的。

```
std::size_t InProcessAttachmentReader::read(
```



这个是音频输入的缓冲区的情况。

```
size_t bufferSize = alexaClientSDK::avsCommon::avs::AudioInputStream::calculateBufferSize(
        BUFFER_SIZE_IN_SAMPLES, WORD_SIZE, MAX_READERS);
    auto buffer = std::make_shared<alexaClientSDK::avsCommon::avs::AudioInputStream::Buffer>(bufferSize);
    std::shared_ptr<alexaClientSDK::avsCommon::avs::AudioInputStream> sharedDataStream =
        alexaClientSDK::avsCommon::avs::AudioInputStream::create(buffer, WORD_SIZE, MAX_READERS);
```

先看buffer size的计算方法。

缓冲区的容量是15秒的音频数据。

最多10个reader。

```
(16000*15, 2, 10)

```



分析tap唤醒后的工作流程。

调用到recognize函数。

```
m_audioInputProcessor->recognize(tapToTalkAudioProvider, capabilityAgents::aip::Initiator::TAP, beginIndex);
```

还是看不出持续采集声音，不断往上送这个过程。



参考资料

1、

https://developer.amazon.com/zh/docs/alexa-voice-service/speechrecognizer.html

