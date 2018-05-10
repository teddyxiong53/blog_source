---
title: cpp之auto关键字
date: 2018-05-09 19:21:32
tags:
	- cpp

---



c++98就已经有auto这个关键字了。

之前的auto关键字基本是没用的。

但c++11把内涵扩大了。就是可以不明确指定变量的类型了。

这样写代码会简洁一些。

一般是在循环变量那里用。

```
    for (auto configFile : configFiles) {
        if (configFile.empty()) {
            alexaClientSDK::sampleApp::ConsolePrinter::simplePrint("Config filename is empty!");
            return false;
        }
```



# 参考资料

1、C++11特性：auto关键字

https://www.cnblogs.com/QG-whz/p/4951177.html