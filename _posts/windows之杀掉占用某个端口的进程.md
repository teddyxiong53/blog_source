---
title: windows之杀掉占用某个端口的进程
date: 2018-09-28 21:32:03
tags:
	- windows

---



```
netstat -ano | findstr 1080
看到对应的pid xxx
tasklist | findstr xxx
这样就可以看到对应的名字。
杀掉。
taskkill.exe -pid xxx -F
```

