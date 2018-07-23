---
title: Linux之start-stop-daemon
date: 2018-06-28 19:10:28
tags:
	- Linux

---



一个例子。

```
start-stop-daemon -S -q -m -p $TEST_MAIN_PIDFILE -b -x $TEST_MAIN_DAEMON
```

