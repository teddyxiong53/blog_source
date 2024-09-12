---
title: windows上SD卡显示黄色感叹号无法读取
date: 2020-12-14 16:11:30
tags:
	- windows
---



本质是因为SD卡的分区导致的。

磁盘管理可以看到。

解决办法：放到Linux上，删除SD卡的所有分区，然后新建一个主分区。

然后放到windows上，分配一个新的卷标。

然后就可以识别了。



跟我的读卡器也有关系。

换一个读卡器也正常。



参考资料

http://blog.sina.com.cn/s/blog_8d0c71600102uzqx.html