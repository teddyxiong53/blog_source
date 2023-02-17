---
title: Linux内核之jiffies
date: 2020-05-31 10:37:20
tags:
	- Linux内核

---



在include/linux/jiffies.h里。

```
extern u64 __jiffy_data jiffies_64;
extern unsigned long volatile __jiffy_data jiffies;
```

volatile修饰，是告诉编译器不要对这个变量进行优化。

我们一般是通过包含`<linux/sched.h>`来间接包含。

jiffies，我们只能进行读。靠定时器的中断来进行jiffies值的累加。

对于32位cpu，1000的HZ值。大概50天，jiffies会溢出。



参考资料

1、linux 使用 jiffies 计数器

https://www.cnblogs.com/fanweisheng/p/11141978.html

2、jiffies溢出与时间先后比较-time_after,time_before

https://blog.csdn.net/jk110333/article/details/8177285

3、

https://www.cnblogs.com/zhangshenghui/p/7069702.html