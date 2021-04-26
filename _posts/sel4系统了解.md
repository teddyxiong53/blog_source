---
title: sel4系统了解
date: 2021-04-26 11:36:34
tags:
	- 系统
---

--

越大的系统潜在的bug就越多，

所以微内核在减少bug方面很有优势，

seL4是世界上最小的内核之一。

但是seL4的性能可以与当今性能最好的微内核相比。

作为微内核，seL4为应用程序提供少量的服务，

如创建和管理虚拟内存地址空间的抽象，线程和进程间通信IPC。

这么少的服务靠8700行C代码搞定。

**seL4是高性能的L4微内核家族的新产物，**

它具有操作系统所必需的服务，如线程，IPC，虚拟内存，中断等。

除了微内核，seL4另一大特色是完全的形式验证。

seL4的实现总是严格满足上一抽象层内核行为的规约，

它在任何情况下都不会崩溃以及执行不安全的操作，

甚至可以精确的推断出seL4 在所有情况下的行为，这是了不起的。

研究发现常用的攻击方法对seL4无效，

如恶意程序经常采用的缓存溢出漏洞。

使用面向过程语言Haskell实现了一个内核原型，

用它来参与形式验证，最后根据它，用C语言重新实现内核，作为最终内核。

 顺便提一句，seL4有两只team，

kernel team和verification team，

而连接这两个team的是 Haskell prototype。

在用C开发内核的过程中，seL4对使用C进行了如下限制：
1. 栈变量不得取引用，必要时以全局变量代替
2. 禁止函数指针
3. 不支持union

对seL4的formal verification（形式验证）分为两步：

abstract specification（抽象规范）和executable specification（可执行规范）之间，executable specification和implementation（实现）之间。

有两个广泛的方法来进行formal verification：

 model checking（全自动）和交互式数学证明（interactive mathematical proof ），

后者需要手工操作。

seL4验证使用的形式数学证明来自Isabelle/HOL，属于后者。

具体来说seL4的形式验证步骤：
1. 写出IPC、syscall、调度等所有微内核对象（kernel object）的abstract specification（in Isabelle）
2. 写出如上对象的executable specification（in Haskell），并证明其正确实现了第一步的abstract specification，利用状态机的原理，abstract specification的每一步状态转换，executable specification都产生唯一对应的状态转换。
3. 写C实现。通过一个SML写的C-Isabelle转换器，和Haskabelle联合形式证明C代码和第二步的Haskell定义语义一致。


seL4的实现被证明是**bug-free**（没有bug）的，

比如不会出现缓冲区溢出，空指针异常等。

还有一点就是，C代码要转换成能直接在硬件上运行的二进制代码，seL4可以确保这个转换过程不出现错误，可靠。

seL4是世界上第一个（到目前也是唯一一个）从很强程度上被证明是安全的OS。



参考资料

1、开源微内核seL4

https://blog.csdn.net/BlueCloudMatrix/article/details/46772171