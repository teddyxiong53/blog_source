---
title: Linux之errno实现分析
date: 2017-10-02 13:58:17
tags:
	- Linux

---



Linux的errno，实际上不是一个我们通常认为的整型值，而是通过整型指针来取值的。这样可以做到线程安全。（？？）

```
extern int *__errno_location();
#define errno (*__errno_location ())
```

