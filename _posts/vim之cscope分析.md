---
title: vim之cscope分析
date: 2020-02-13 10:54:08
tags:
	- vim

---

--

有了ctags，为什么还需要cscope？

因为ctags当前可以帮我们完成的是：调整到符合定义处。

但是我们还有这种需求：找出函数被哪些地方调用了。

对于这个需求，ctags无能为力。

cscope最早是由贝尔实验室开发的，后面用bsd协议开源了。

最常用的命令：

```
cscope -Rbq
```

参数的记忆就是：惹不起。

会生成3个文：

```
cscope.out
	基本符号的索引
cscope.in.out
cscope.po.out
	这2个都是为了加快索引速度。
```

具体的操作快捷键是怎样的？

```

```



# 搜索函数的所有调用位置并输出到quickfix窗口里，方便一条条查看



# 参考资料

1、这个视频教程不错。

https://www.bilibili.com/video/BV1q64y1M7sW/