---
title: git之bare仓库
date: 2021-04-25 15:29:34
tags:
	- git
---

--

一般来说，一个裸库往往被创建用于作为大家一起工作的共享库，

每一个人都可以往里面push自己的本地修改。

一般来讲，**作为远端备份或公共版本库时**，应该使用git init --bare。

git init 用于本地代码库，跟文件夹下包括所有的源代码。

新建仓库步骤：通过cd进入文件夹目录，通过ls列出文件夹，mkdir新建一个文件夹，进入此文件夹，通过git init --bare初始化仓库。

设置git对应的branch，否则不能正常更新和提交

git branch --set-upstream master origin/master



从裸仓库 clone 下来的本地仓库可以进行正常的 `push` 操作， 

但是从一般仓库 clone 下来的本地仓库却不行。

 这也正是裸仓库存在的意义。 

**裸仓库一般情况下是作为远端的中心仓库而存在的。**



参考资料

1、git仓库init时用bare参数的区别

https://www.jianshu.com/p/22dda0896d38

2、

https://segmentfault.com/a/1190000007686496/