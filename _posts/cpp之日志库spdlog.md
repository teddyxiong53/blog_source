---
title: cpp之日志库spdlog
date: 2020-01-16 10:10:19
tags:
	- cpp
---

1

代码在这里。

https://github.com/gabime/spdlog

看github上的官方wiki就好了。

不用clone，clone很大，下载压缩包只有300K左右。

编译是基于cmake的。

```
mkdir build
cd build && cmake .. && make
```

从example来看接口的使用方法。

下面只列出基本的用法，复杂的方式可以随时参考example的来写。

基本用法：

```
spdlog::info("this is info");
spdlog::warn("this is warn");
```

设置日志级别

```
spdlog::set_level(spdlog::level::info);
```

设置日志模式

```
spdlog::set_pattern("[%H:%M:%S %z] [%^%L%$] [thread %t] %v");
```

`[%^%L%$]`这个是打印level的。%v这个是打印后面的内容的。

切换回默认的格式：

```
spdlog::set_pattern("%+");
```

格式化输出

```
spdlog::info("welcom {} to {}, today is {} day of this year", "xhl", "shenzhen", 5);
```

打印二进制内容

```

```

集成到我的dossos里。

这个就用静态库的方式就好了。

# 最佳实践

就rotate记录到文件里。这个对于嵌入式是最合适的方式。因为空间有限。

还要是异步的。这样就不会影响程序的执行速度。

这样就是具有实用价值的使用方式。

希望每3秒刷一次日志到文件。

在崩溃的时候，也要刷一下。

```
#ifdef USE_SPDLOG
#include "spdlog/spdlog.h"
#include "spdlog/async.h"
#include "spdlog/sinks/rotating_file_sink.h"
auto mylog = spdlog::rotating_logger_mt<spdlog::async_factory>("dossos", "asynclog.txt", 1024, 3);//这里1024字节，表示文件大小（为了测试方便，设置很小），3表示会切分3个文件，依次滚动覆盖。
void  sig_handler(int signo)
{
    printf("get sigint \n");
    // spdlog::drop_all();
    exit(0);
}
void test_spdlog()
{
    signal(SIGINT, sig_handler);
    spdlog::set_level(spdlog::level::info);
    mylog->flush_on(spdlog::level::err);
    spdlog::flush_every(std::chrono::seconds(3));
    for(int i=0;i<100;i++) {
        mylog->info("this is log in async mode {}", i);
    }
}
#endif
```

切分文件是这样的：

```
假设设置文件名字为xx.txt。
切分为3个。
那么依次会有4个文件。
xx.txt里总是最新的。
xx.1.txt
xx.2.txt
xx.3.txt
```





参考资料

1、

https://github.com/gabime/spdlog/wiki/1.-QuickStart

2、spdlog的简单封装和使用

https://www.cnblogs.com/LuckCoder/p/11171609.html