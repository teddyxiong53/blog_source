---
title: C语言之MISRA编码标准
date: 2023-09-20 10:59:11
tags:
	- C语言
---

--

MISRA C是由汽车产业软件可靠性协会（MISRA）提出的C语言开发标准。其目的是在增进嵌入式系统的安全性及可移植性。针对C++语言也有对应的标准MISRA C++。

MISRA C一开始主要是针对汽车产业，不过其他产业也逐渐开始使用MISRA C：包括航天、电信、国防、医疗设备、铁路等领域中都已有厂商使用MISRA C。

MISRA C的第一版《Guidelines for the use of the C language in vehicle based software》是在1998年发行，一般称为MISRA-C:1998.。MISRA-C:1998有127项规则，规则从1号编号到127号，其中有93项是必需要求，其余的34项是推荐使用的规则。

在2004年时发行了第二版的MISRA C的第一版《Guidelines for the use of the C language in critical systems》（或称作MISRA-C:2004），其中有许多重要建议事项的变更，其规则也重新编号。MISRA-C:2004有141项规则，其中121项是必需要求，其余的20项是推荐使用的规则。规则分为21类，从“开发环境”到“运行期错误”。

2012年发布第三版，为当前最新有效的C语言规范版本，称为MISRAC:2012。 

Misra C不能100%保证程序不出问题，但是能尽可能的预防，总结一下，基本上使用Misra C具有以下五个维度的优势：

提升可靠性

提升可读性

提升可移植性

提升可维护性

提升安全性


参考资料

1、MISRA C-2012规则中文版

https://blog.csdn.net/WJKING3/article/details/122303342