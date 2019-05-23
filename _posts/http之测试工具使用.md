---
title: http之测试工具使用
date: 2019-05-22 16:21:51
tags:
	- http

---



经常需要进行一些简单的内容测试。看看哪些方法可以做。

# nc

```
nc localhost 80
```

然后输入：

```
GET / HTTP/1.1
# 输入回车，表示结束符。
```

# telnet

```
telnet localhost 80
```

然后输入：

```
GET / HTTP/1.1
# 输入回车，表示结束符。
```



参考资料

1、

