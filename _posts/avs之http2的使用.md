---
title: avs之http2的使用
date: 2018-11-02 16:29:19
tags:
	- avs
---



跟http2相关的类，有4个。

HTTP2Stream

HTTP2StreamPool

HTTP2Transport

HTTP2TransportFactory



#HTTP2Transport

这个是最基础的类。

HTTP2Transport实现了4个接口：

1、TransportInterface。主要是connect和send方法。

2、PostConnectObserverInterface。一个方法：onPostConnected

3、PostConnectSendMessageInterface。一个方法：sendPostConnectMessage

4、AuthObserverInterface。一个方法：onAuthStateChange。

这个类本身的主要方法：

establishConnection。



downchannelStream是一个get请求。

```
 m_downchannelStream = m_streamPool.createGetStream(url, authToken, m_messageConsumer);
```



#HTTP2Stream

这个类是很独立的。是对libcurl的封装。

主要方法：

initGet

initPost

getCurlHandle

getResponseCode

主要接口都是给HTTP2StreamPool用的。

createGetStream

createPostStream

getStream

releaseStream



HTTP2Transport有个HTTP2Stream的成员变量。

在初始化的时候构造。构造需要的参数是一个count，一个attach manager。



# HTTP2StreamPool

对stream的包含是：

```
std::vector<std::shared_ptr<HTTP2Stream>> m_pool; 指针向量。
std::mutex m_mutex;
const int m_maxStreams;
static unsigned int m_nextStreamId;
```



# HTTP2TransportFactory

被void MessageRouter::enable()调用了create方法。

attachmentManager参数，是从DefaultClient里构造的。





是靠libcurl打开http2的option来做的。

# 往外发送的流程

```
m_streamPool.createPostStream(url, authToken, request, m_messageConsumer);
```

stream poll里，最多10个。

```
const static int MAX_STREAMS = 10;
```

这个poll的概念是这样实现的，是一个vector。

```
std::vector<std::shared_ptr<HTTP2Stream>> m_pool;
```



ping是新建了一个stream，收到回复后，销毁stream。

是一个get请求。



libcurl的东西，都是一次性的。

用完就销毁的。



每5分钟ping一次，ping的超时是30秒。



directive的，也是一个get stream。

url是：https://avs.alexa.com/v201607207/directives

建立连接的超时时间的60秒。



event是post出去的。



一个消息请求，可以添加一个附件reader。

判断能不能往外发送消息，需要这个条件。一个event如果发了，还没有收到回复，就不能发下一个。

```
bool HTTP2Transport::canProcessOutgoingMessage() {
    for (auto entry : m_activeStreams) {
        auto stream = entry.second;
        // If we have an event that still hasn't received a response code then we cannot send another outgoing message.
        if (isEventStream(stream) && (stream->getResponseCode() == 0)) {
            return false;
        }
    }
    // All outstanding streams (if any) have received a response, the next message can now be sent.
    return true;
}
```

是不是event stream的判断。

```
bool HTTP2Transport::isEventStream(std::shared_ptr<HTTP2Stream> stream) {
    return stream != m_downchannelStream && stream != m_pingStream;
}
```

由此可以看到，系统里是有3种http2 stream的。

1、媒体流。

2、event。

3、ping。

在主循环的开头，会对stream进行清理。

```
cleanupFinishedStreams();
cleanupStalledStreams();//超时的。
```



```
void HTTP2Transport::cleanupFinishedStreams() {
    CURLMsg* message = nullptr;
    do {
        int messagesLeft = 0;
        message = m_multi->infoRead(&messagesLeft);
        if (message && CURLMSG_DONE == message->msg) {
            if (m_downchannelStream && m_downchannelStream->getCurlHandle() == message->easy_handle) {
                if (!isStopping()) {
                    notifyObserversOnServerSideDisconnect();//注意这个函数。
                }
                releaseDownchannelStream(true);
                continue;
            }
```

在服务器端断连后，会进行这个操作。重新创建连接。

```
void MessageRouter::onServerSideDisconnect(std::shared_ptr<TransportInterface> transport) {
    std::unique_lock<std::mutex> lock{m_connectionMutex};
    if (m_isEnabled) {
        setConnectionStatusLocked(
            ConnectionStatusObserverInterface::Status::PENDING,
            ConnectionStatusObserverInterface::ChangedReason::SERVER_SIDE_DISCONNECT);
        createActiveTransportLocked();
    }
}
```



ping超时是30秒。

CurlEasyHandleWrapper

```
HTTP2Stream里：
avsCommon::utils::libcurlUtils::CurlEasyHandleWrapper m_transfer;
HttpPost里：
CurlEasyHandleWrapper m_curl;

```

超时时间。100ms或者10ms。

```
/// Timeout for curl_multi_wait
const static std::chrono::milliseconds WAIT_FOR_ACTIVITY_TIMEOUT(100);
/// Timeout for curl_multi_wait while all HTTP/2 event streams are paused.
const static std::chrono::milliseconds WAIT_FOR_ACTIVITY_WHILE_STREAMS_PAUSED_TIMEOUT(10);
```

什么时候用HttpPut？

只有能力总代理用到了这个 。

```
m_capabilitiesDelegate = alexaClientSDK::capabilitiesDelegate::CapabilitiesDelegate::create(
        authDelegate, miscStorage, httpPut, config, deviceInfo);
```

```
publishCapabilities这个函数里是唯一用到的地方。
```

