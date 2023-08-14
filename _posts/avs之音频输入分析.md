---
title: avs之音频输入分析
date: 2018-11-10 14:59:19
tags:
	- avs
---

--

是靠portaudio来做的录音。

```
void InteractionManager::microphoneToggle()
	m_micWrapper->startStreamingMicrophoneData();
```



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



我发现自己一直忽略基础的一点，音频设备在哪里打开的？

 This is in an HTTP multipart format where the first part is the JSON message, followed by a second part that is the user's LCPM16 speech from the microphone.  



从字面上看，应该是AudioProvider来提供的。

录音也是靠gstreamer来做的。



AttachmentReader

InProcessAttachmentReader

SDSTypeReader

SharedDataStream里的Reader。它的read函数，就是取pcm数据的地方。

那么怎么把这个pcm数据交给http去发送的呢？每次交多少数据呢？

从AttachmentReaderSource.cpp里看。

```
auto size = m_reader->read(info.data, info.size, &status, std::chrono::milliseconds(1));
```

这里，另外还有MediaPlayer，是仅有的2个使用了handleReadData的地方。

```
gboolean BaseStreamSource::onReadData(gpointer pointer) {
    return static_cast<BaseStreamSource*>(pointer)->handleReadData();
}
```

而onReadData。在这里调用。

```
void BaseStreamSource::updateOnReadDataHandler() {
	g_timeout_add(interval, reinterpret_cast<GSourceFunc>(&onReadData), this);
```

g_timeout_add这个是glib里的函数。

这个相当于一个周期运行的定时器。



再看这个函数。

```
m_needDataHandlerId = g_signal_connect(appsrc, "need-data", G_CALLBACK(onNeedData), this);
```

这个函数是gstreamer的函数。相当于注册事件到一个按钮这种行为。



BaseStreamSource是我们要重点关注的一个类。

IStreamSource 这个是什么，I表示输入吗？

AttachmentReaderSource这个应该就是网上取下来的音频的对应类。



只有这里用到了IStreamSource 

```
void MediaPlayer::handleSetIStreamSource
```

这个还是要靠调试才能发现是怎么进行输入的。



InProcessSDS

这个的含义是，在一个进程里的SDS数据。

SDS只有一个生产者，多个消费者。

目前消费者限制为10个。



靠的还是PortAudio。

PortAudioMicrophoneWrapper

跟sds是这样关联起来的。

```
std::shared_ptr<alexaClientSDK::sampleApp::PortAudioMicrophoneWrapper> micWrapper =
        alexaClientSDK::sampleApp::PortAudioMicrophoneWrapper::create(sharedDataStream);
```

在PortAudioCallback里，进行的write操作。



对这里，可以简单理解为一个数组，writer往里面写，reader从里面读。

只不过是机制相当于数组要完善健壮一些。

目前是没有看到reader进行read操作。

有3个地方调用了read函数。

```
1、gboolean AttachmentReaderSource::handleReadData() {
2、ESP里。这个不看。
3、std::size_t InProcessAttachmentReader::read(
```

handleReadData只有一个地方调用了。靠的是g_idle_add来做的。

```
gboolean BaseStreamSource::onReadData(gpointer pointer) {
    return static_cast<BaseStreamSource*>(pointer)->handleReadData();
}
```

在这里调用的。

```
void BaseStreamSource::installOnReadDataHandler() {
```



IStreamSource这个是对std::istream的包装，是处理音频文件的。

跟音频输入没有关系。

只被这一个地方调用。

```
void MediaPlayer::handleSetIStreamSource(
```



关于remote的判断。

```
/**
     * Indicates whether a source is local or remote from the perspective of the MediaPlayer (e.g. playing out of the
     * SDS is local, playing a URL is remote).
     *
     * @return A boolean indicating whether the source is from a remote or local source
     */
    virtual bool isPlaybackRemote() const = 0;
```



```
RequireShutdown
	SourceInterface
		BaseStreamSource
			IStreamSource：这个就直接给MediaPlayer用了。
				
```



AudioItem

是一个struct，里面嵌套了struct，没有函数。

只有AudioPlayer用到了。

```
std::deque<AudioItem> m_audioItems;
```



参考资料

1、

https://developer.amazon.com/zh/docs/alexa-voice-service/speechrecognizer.html

2、AVS中PCM音频数据是怎么存放到audio attachment中的？

https://forums.developer.amazon.com/questions/32451/avs%E4%B8%ADpcm%E9%9F%B3%E9%A2%91%E6%95%B0%E6%8D%AE%E6%98%AF%E6%80%8E%E4%B9%88%E5%AD%98%E6%94%BE%E5%88%B0audio-attachment%E4%B8%AD%E7%9A%84.html

3、g_signal_connect

https://blog.csdn.net/datamining2005/article/details/78443645