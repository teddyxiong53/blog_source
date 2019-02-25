---
title: cpp之PRId64
date: 2019-02-25 16:50:17
tags:
	- cpp

---



在c++代码里看到这种写法。

```
#define __STDC_FORMAT_MACROS
#include <inttypes.h>
#undef __STDC_FORMAT_MACROS
```

这个主要是为了64位的打印。

```
#include <inttypes.h>
printf("%" PRId64 "\n", value);
// 相当于64位的：
printf("%" "ld" "\n", value);
// 或32位的：
printf("%" "lld" "\n", value);
```



参考资料

1、C++中正确使用PRId64

https://blog.csdn.net/win_lin/article/details/7912693