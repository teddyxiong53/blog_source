---
title: qt之Q_GADGET
date: 2021-06-10 14:20:11
tags:
	- qt

---

--

对于那些没有继承自QObject但却想拥有反射能力的类型，Q_GADGET是Q_OBJECT的轻量化版本。

和Q_OBJECT一样，Q_GADGET也必须出现在类定义的私有区域。

有Q_GADGET时，可以有Q_ENUM, Q_PROPERTY 和Q_INVOKABLE，但不能有signals和slots。

Q_GADGET使类成员staticMetaObject可用。



参考资料

1、

https://blog.csdn.net/qq_43248127/article/details/101635247