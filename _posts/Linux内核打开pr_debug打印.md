---
title: Linux内核打开dev_dbg打印
date: 2020-04-10 16:29:51
tags:
	- Linux

---

1

dev_dbg本质是上是调用了printk KERN_DEBUG。

要打开dev_dbg，需要2步：

第一步：

```
你调试的文件中必然包含了<linux/device.h>，或者<linux /paltforam_device.h>，后者包含了前者，在包含此头文件之前，使用#define DEBUG 1 来打开调试开关
```

第二次：

调整打印级别。



原来，三个宏作为判断条件决定了pr_debug到底采用哪种用法：
第一种用法，如果定义了CONFIG_DYNAMIC_DEBUG，就使用动态debug机制dynamic_pr_debug();
第二种用法，如果定义了DEBUG，就使用printk(KERN_DEBUG...)
第三种用法，默认情况下，不打印。


参考资料

1、

https://blog.csdn.net/renlonggg/article/details/79467437

2、

https://blog.csdn.net/helloanthea/article/details/25330809

3、

https://www.cnblogs.com/pengdonglin137/p/4621576.html