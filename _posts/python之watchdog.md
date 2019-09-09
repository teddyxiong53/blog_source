---
title: python之watchdog
date: 2019-09-07 12:01:48
tags:
	- python

---

1

这个是用来监控文件系统变化的。

典型用途是，配置文件有变化时，自动重新载入文件。

看一个简单例子。

```
import sys,time,logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

logging.basicConfig(level=logging.DEBUG)

path = sys.argv[1] if len(sys.argv)>1 else '.'
event_handler = LoggingEventHandler()
observer = Observer()
observer.schedule(event_handler, path, recursive=True)
observer.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
```

核心的概念是：event和handler、observer。

event有：

```
FileSystemEvent
主要是下面的事件。

create
delete
modify
move

```



参考资料

1、

https://pythonhosted.org/watchdog/quickstart.html#a-simple-example