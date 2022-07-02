---
title: Linux之shell监听文件变化
date: 2022-01-05 13:51:01
tags:

	- Linux

---

--

```
inotifywait -mrq --format '%e' --event create,delete,modify ./value
```



参考资料

1、

https://www.its404.com/article/mingongge/110507794