---
title: cpp之RAII机制
date: 2018-09-25 13:58:17
tags:
	- cpp

---



RAII是Resource Acquisition Is Initialization。资源获取就是初始化。

这个是cpp的一种管理资源，避免泄漏的惯用法。

cpp标准保证任何情况下，已构造的对象最终会销毁。也就是说，析构函数最后会被调用。



RAII是一种思路。

这种就是RAII 的一种应用。

```
class MutexLockGuard: nocopyable {
public:
	MutexLockGuard(MutexLock& mutex): mutex_(mutex) {
		mutex_.lock();
	}
	~MutexLockGuard() {//注意这里是在析构函数里进行解锁的。这个技巧很好。
		mutex_unlock();
	}
private:
	MutexLock& mutex_;
};
```



参考资料

RAII

https://baike.baidu.com/item/RAII





