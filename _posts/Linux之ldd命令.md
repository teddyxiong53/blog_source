---
title: Linux之ldd命令
date: 2019-07-06 15:23:37
tags:
	- Linux
---

1

我对这个命令产生兴趣，是因为gstreamer的库太多了。

我需要知道哪些动态库是必须的。

```
teddy@teddy-ThinkPad-SL410:~/work/test/gstreamer/test$ ldd a.out 
        linux-gate.so.1 =>  (0xb77c7000)
        libgstreamer-1.0.so.0 => /usr/lib/i386-linux-gnu/libgstreamer-1.0.so.0 (0xb7659000)
        libgobject-2.0.so.0 => /usr/lib/i386-linux-gnu/libgobject-2.0.so.0 (0xb75fa000)
        libglib-2.0.so.0 => /lib/i386-linux-gnu/libglib-2.0.so.0 (0xb74d1000)
        libpthread.so.0 => /lib/i386-linux-gnu/libpthread.so.0 (0xb74b4000)
        libc.so.6 => /lib/i386-linux-gnu/libc.so.6 (0xb72fe000)
        libgmodule-2.0.so.0 => /usr/lib/i386-linux-gnu/libgmodule-2.0.so.0 (0xb72f8000)
        libm.so.6 => /lib/i386-linux-gnu/libm.so.6 (0xb72a3000)
        librt.so.1 => /lib/i386-linux-gnu/librt.so.1 (0xb729a000)
        libdl.so.2 => /lib/i386-linux-gnu/libdl.so.2 (0xb7295000)
        libffi.so.6 => /usr/lib/i386-linux-gnu/libffi.so.6 (0xb728c000)
        libpcre.so.3 => /lib/i386-linux-gnu/libpcre.so.3 (0xb7216000)
        /lib/ld-linux.so.2 (0x8000d000)
```

