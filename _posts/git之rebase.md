---
title: git之rebase
date: 2021-04-21 16:42:07
tags:
	- git

---

--

rebase在git中是一个非常有魅力的命令，

使用得当会极大提高自己的工作效率；

相反，如果乱用，会给团队中其他人带来麻烦。

它的作用简要概括为：

可以对**某一段线性提交历史**进行编辑、删除、复制、粘贴；

**因此，合理使用rebase命令可以使我们的提交历史干净、简洁！**



**前提：不要通过rebase对任何已经提交到公共仓库中的commit进行修改（你自己一个人玩的分支除外）**



现在我们在测试分支上添加了四次提交，我们的目标是把最后三个提交合并为一个提交：



所以，虽然此时HEAD所指向的内容正是我们所需要的，

但是master分支是没有任何变化的，

`git`只是将C~E部分的提交内容复制一份粘贴到了master所指向的提交后面，

我们需要做的就是将master所指向的提交id设置为当前HEAD所指向的提交id就可以了，即:

```undefined
git checkout master
git reset --hard  0c72e64
```



解决方法：

敲git rebase 然后按提示执行就行了，

如果rebase 发生冲突的话，则修改，修改完后git add -u filename，

然后git rebase --continue ，直到没有冲突为止。不需要commit 。



参考资料

1、

https://www.jianshu.com/p/4a8f4af4e803

2、git push 出现 you are not allowed to upload merges 错误提示

https://blog.csdn.net/muxidreamtohit/article/details/43408127