---
title: qemu之append问题解决
date: 2018-03-18 21:38:10
tags:
	- qemu

---



我在用qemu来运行linux的时候，我加上-append参数后，运行就没有打印出来。

现在我知道是为什么了。我感觉是，qemu -append这里传递的bootargs是最后的，会覆盖前面的bootargs。

所以，需要在-append后面把bootargs写完整。尤其要写上console=ttyAMA0这一个。

```
-append "console=ttyAMA0 lpj=3805180 initcall_debug=1"
```

这样就没有问题。

