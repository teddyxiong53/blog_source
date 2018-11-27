---
title: avs之directive处理过程
date: 2018-11-27 10:19:24
tags:
	- avs

---



核心类是DirectiveSequencer。

这里进行指令的解析和分发。

这里有一个死循环线程receivingLoop。



然后调用DirectiveProcessor的m_directiveProcessor->onDirective(directive);



MessageInterpreter，receive函数里，调用m_directiveSequencer->onDirective(avsDirective); 

这里就是socket收到消息。这里是后续处理的起源地。

MessageInterpreter唯一相关的类，就是AVSConnectionManager

```
m_connectionManager->addMessageObserver(messageInterpreter);
```

AVSConnectionManager收到消息，就通知MessageInterpreter执行receive。

```
void AVSConnectionManager::receive(const std::string& contextId, const std::string& message) {
    std::unique_lock<std::mutex> lock{m_messageObserverMutex};
    std::unordered_set<std::shared_ptr<avsCommon::sdkInterfaces::MessageObserverInterface>> observers{
        m_messageObservers};
    lock.unlock();

    for (auto observer : observers) {
        if (observer) {
            observer->receive(contextId, message);//这里。
        }
    }
}
```



而AVSConnectionManager收到消息的来源，是MessageRouter::consumeMessage。

而consumeMessage，是MimeParser::partEndCallback(void* userData) 这里调用的。

```
    switch (parser->m_currDataType) {
        case MimeParser::ContentType::JSON:
            // Check there's data to send out, because in a re-drive we may skip a directive that's been seen before.
            if (parser->m_directiveBeingReceived != "") {
                parser->m_messageConsumer->consumeMessage( //这里。
                    parser->m_attachmentContextId, parser->m_directiveBeingReceived);
```

一切的起源在这里：http Response里解析内容。

```
    if (HTTPResponseCode::SUCCESS_OK == stream->getResponseCode()) {
        MimeParser::DataParsedStatus status = stream->m_parser.feed(data, numChars);
```

