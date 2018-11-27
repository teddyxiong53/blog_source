---
title: avs之Task模型
date: 2018-10-16 16:11:35
tags:
	- avs

---



有3个类：

TaskQueue。最基础，只依赖std库。

TaskThread。依赖TaskQueue。

Executor，这里面聚合了TaskQueue和TaskThread。

```
Executor::Executor() :
        m_taskQueue{std::make_shared<TaskQueue>()},
        m_taskThread{memory::make_unique<TaskThread>(m_taskQueue)} {
    m_taskThread->start();
}
```



