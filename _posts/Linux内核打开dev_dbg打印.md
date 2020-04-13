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



参考资料

1、

https://blog.csdn.net/renlonggg/article/details/79467437