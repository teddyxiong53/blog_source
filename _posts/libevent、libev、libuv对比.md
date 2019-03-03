---
title: libevent、libev、libuv对比
date: 2019-03-02 10:44:17
tags:
	- 网络

---



```
简单说，是这样的关系：
1、libevent，最早出现。使用广泛。
2、libev。去掉了libevent里对windows的支持，代码更加简洁了。
3、libuv。更换了底层机制，也兼容了windows。

libuv，是目前实用的。libev用得不多。
```



参考资料

1、简单对比 Libevent、libev、libuv

https://yq.aliyun.com/articles/611321

