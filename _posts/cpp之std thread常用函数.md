---
title: cpp之std thread常用函数
date: 2018-10-13 10:58:51
tags:
	- cpp
---





延时

```
std::this_thread::sleep_for(std::chrono::seconds(2))
```

detach

```
std::thread t(independentThread);
t.detach();
```

