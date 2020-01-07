---
title: buildroot之不同编译类型的分析
date: 2020-01-06 10:17:08
tags:
	-buildroot

---

1

buildroot集成了大量的第三方的开源软件包，这些软件使用的编译build工具分为几类，buildroot是如何进行处理的？

我们在package目录下，运行如下命令：

```
grep -nwr "\$(eval" .
```

可以搜索出这么几类编译方法：

```
$(eval $(cmake-package))

$(eval $(autotools-package))

$(eval $(generic-package))
$(eval $(python-package))

$(eval $(kernel-module))
$(eval $(rebar-package))
```

我们各选取一个简单的例子进行分析。

cmake

uhttpd使用的就是cmake的。我们打开package/uhttpd/uhttpd.mk文件。

cmake是我目前最喜欢的编译工具。

cmake-package的实现是在package/pkg-cmake.mk里。



代码管理工具也分为几类

git

参考资料

1、

