---
title: qemu按ctrl-c退出的问题解决
date: 2021-06-03 16:13:11
tags:
	- qemu

---

--

我是这样运行qemu的

```
qemu-system-arm -M vexpress-a9 -smp 1 -m 64 -kernel zImage -dtb vexpress-v2p-ca9.dtb -drive file=rootfs.ext2,if=sd,format=raw -append "console=ttyAMA0,115200 rootwait root=/dev/mmcblk0" -net nic,model=lan9118 -net user -serial stdio
```

我是需要图形界面的。

当前有个问题，就是我前台运行一个程序，如果想要ctrl+c进行结束，就导致当前qemu直接退出了。

可以这样解决：

```
-serial stdio
改成：
-serail mon:stdio
```

这样就可以了。



参考资料

1、

https://www.coder.work/article/6907536