---
title: muduo之log分析
date: 2019-11-27 16:38:51
tags:
	- cpp
---

1

就从这一行开始看：

```
LOG_SYSFATAL << "sockets::bindOrDie";
```

Logger类：

```
构造函数：
	有4个。
	1、2个参数。file和line。
	2、3个参数。多了level。
	3、4个参数。多了level和const char *func
	4、3个参数。多了是否abort。
对外接口：
	setLogLevel
	setTimeZone
```

Impl类

```
构造函数：
	1个。
	参数4个：
		1、level。
		2、old_errno。
		3、SourceFile。
		4、line。
成员变量：
	1、时间戳。
	2、LogStream。
	3、level。
	4、line。
	5、SourceFile。
```

LogStream类

```
构造函数：
	默认的。
成员变量：
	Buffer。FixedBuffer类型的。尺寸有4K和4M两种。默认4K的。
对外接口：
	就是override了很多的<<，参数类型各种都覆盖到了。
	
```

FixedBuffer类：

```
构造函数：
	一个。
	没有参数。
	里面调用函数：setCookie(cookieStart);
	就是设置回调函数，cookieStart目前是个空实现。
成员变量：
	data。就是4K的数组。 char data_[SIZE];
```



loglevel，本来单词长度是不同的，通过加空格，都统一为6个字符的。

时间戳的都是time_.microSecondsSinceEpoch()这个来获取的。

前端都是把内容放到了一个buffer里。

后端是如何取数据的？

默认的输出是Logger::OutputFunc g_output = defaultOutput;

默认是输出到stdout。

每次输出日志，都经历了一次构造和析构（因为是临时匿名对象）。是靠析构里进行的g_output操作。

临时匿名对象这一点很关键。因为这种对象是马上销毁。如果是有名对象，析构的顺序，跟变量定义的顺序是相反的，这样就会导致后面的日志先输出。这个显然是不对的。

```
Logger::~Logger()
{
  impl_.finish();
  const LogStream::Buffer& buf(stream().buffer());
  g_output(buf.data(), buf.length());
  if (impl_.level_ == FATAL)
  {
    g_flush();
    abort();
  }
}
```

那么如果我要把日志写入到文件，应该怎么做呢？

在AsyncLogging_test.cc里，有示例。

```
off_t kRollSize = 500*1000*1000;

muduo::AsyncLogging* g_asyncLog = NULL;
muduo::AsyncLogging log(::basename(name), kRollSize);
log.start();
g_asyncLog = &log;

void asyncOutput(const char* msg, int len)
{
  g_asyncLog->append(msg, len);
}

muduo::Logger::setOutput(asyncOutput);
```

总的来说，是这样：

```
1、定义个AsyncLogging对象log，调用它的start函数。相当于启动了一个后端线程。
2、定义个一个output函数，函数里调用log的append函数。
	output函数设置给Logger模块。
```



AsyncLogging类

```
成员变量：
	
```

LogFile类：

```

```



日志的初始化：

靠环境变量。

```
Logger::LogLevel initLogLevel()
{
  if (::getenv("MUDUO_LOG_TRACE"))
    return Logger::TRACE;
  else if (::getenv("MUDUO_LOG_DEBUG"))
    return Logger::DEBUG;
  else
    return Logger::INFO;
}
```

Logger类主要控制日志的级别。

内部实现靠Impl类来做。



参考资料

1、

https://blog.csdn.net/u014303647/article/details/88630117