---
title: AzureRTOS
date: 2021-06-03 13:37:11
tags:
	- rtos

---

--

https://github.com/azure-rtos/threadx

```
git clone https://github.com/azure-rtos/threadx.git
mkdir build
cd build
cmake  -DCMAKE_TOOLCHAIN_FILE=cmake/cortex_m4.cmake ../
make
```

这样只是得到静态库libthreadx.a。

连sample都没有编译出来。也没用说明怎么编译。



参考资料

