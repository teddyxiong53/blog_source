---
title: cpp之unique_lock和lock_guard区别
date: 2018-10-12 19:47:51
tags:
	- cpp
---



这2个的作用一样。unique_lock更加灵活，但是要多占用一点空间。

我使用中发现，有些地方只能用unique_lock。

cond.wait里只能用unique_lock。

```
std::unique_ptr<std::function<void()>> TaskQueue::pop() {
	std::unique_lock<std::mutex> queueLock{m_queueMutex};//这里就只能用unique_lock。
	auto shouldNotWait = [this]() {
		return m_shutdown || !m_queue.empty();
	};
	if(!shouldNotWait()) {
		m_queueChanged.wait(queueLock, shouldNotWait);
	}
	if(!m_queue.empty()) {
		auto task = std::move(m_queue.front());
		m_queue.pop_front();
		return task;
	}
	return nullptr;
}
```



# 参考资料

1、C++11 std::unique_lock与std::lock_guard区别及多线程应用实例

https://blog.csdn.net/tgxallen/article/details/73522233