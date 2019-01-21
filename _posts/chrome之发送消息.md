---
title: chrome之发送消息
date: 2019-01-21 14:13:12
tags:
	- chrome

---



由于content-script运行在web页面的上下文里。属于web页面的组成部分。

而不是chrome扩展的一部分。

但是content-scripts又往往需要跟插件的其他部分进行通信。



一次性请求与响应

```
chrome.runtime.sendMessage(obj, function(response){})
```



参考资料

1、Chrome浏览器扩展开发系列之十三：消息传递Message

https://www.cnblogs.com/champagne/p/4848520.html