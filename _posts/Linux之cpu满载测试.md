---
title: Linux之cpu满载测试
date: 2019-07-26 14:07:19
tags:
	- gnome

---



下面的命令，可以让cpu的占有率达到100%。

```
for i in `seq 1 $(cat /proc/cpuinfo |grep "processor" |wc -l)`; do dd if=/dev/zero of=/dev/null & done
```



参考资料

1、[Linux小技巧] 一行命令让CPU占用率达到100％

https://blog.csdn.net/robertsong2004/article/details/36879233