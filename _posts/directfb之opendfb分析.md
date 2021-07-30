---
title: directfb之opendfb分析
date: 2021-07-28 10:05:33
tags:
	- gui

---

--

我最感兴趣的是，opendfb怎么完全去掉c++代码的。

通过source insight查看，的确class都被去掉了。

```
CoreDFB_Initialize
	DirectFB::ICore_Real real( core_dfb, obj );
```

被改成这样调用了：

```
ICoreReal real;
ICore *super = (ICore *)&real;
ICoreRealInit( &real, core_dfb, obj );
```

这么看，的确是全部手动把C++的内容改成了C语言的了。

把class都改成了struct。

