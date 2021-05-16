---
title: docker之watchtower
date: 2021-05-16 11:58:34
tags:
	- docker
---

--

这个是我监听jd-script这个容器情况，的确进行了正常的更新操作。

```
time="2021-05-15T14:50:10Z" level=info msg="Found new nevinee/jd:v4 image (0576a6e75fe2)"
time="2021-05-15T14:50:10Z" level=info msg="Stopping /jd-script (c01538a6b98d) with SIGTERM"
time="2021-05-15T14:50:15Z" level=info msg="Creating /jd-script"
time="2021-05-15T14:50:15Z" level=info msg="Removing image 7269df858c7e"
```

这个日志是从portainer里，watchtower容器的log看到的。

更新容器，并没有把手动放进容器的东西弄丢。

我放进去的panel还在的。

要指定监听的目标容器，只需要在启动watchtower的时候，docker run命令的后面加上：-c xx yy 这样就可以指定监听xx和yy这2个容器了。



参考资料

1、

https://www.cnblogs.com/-wenli/p/14059611.html