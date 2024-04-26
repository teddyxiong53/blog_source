---
title: git（1）
date: 2017-10-09 19:16:08
tags:
	- git

---



没有系统学习git的使用，有时候会跟github打交道。把碰到的问题及解决记录下来。

# 取指定版本的代码

先把代码clone下来。

然后git log。找到对应版本的sha字符串。

然后git checkout sha字符串就好了。

但是这样就完全回退到指定版本了，怎么再继续到较新的版本呢？现在本地已经看不到更多的log信息了。

我觉得还是要下载多份，一份完全不动。只能用这种方式来做了。

这样查看版本，比较清晰。

```
git log --pretty=oneline
```



## 放弃本地修改，强制更新

```
git reset hard
```

# 查看某个文件的修改历史

```
git log -- xx.c
```

# git remote命令

1、查看远程的仓库情况。列出已经存在的远程分支。

```
git remote
```

后面加上-v，则得到更加详细的信息。



git远程建立仓库。

# git命令思维导图

这里，可以帮助梳理思路。

https://zhuanlan.zhihu.com/p/59616525

# 常用命令速查

# 全局忽略.vscode目录

因为使用vscode，经常会在目录下产生.vscode目录，在一个个仓库下去加.gitignore就太麻烦了。

可以全局忽略这个目录。

参考这个做就好了。

https://blog.csdn.net/zhangchilei/article/details/105538854

# git am的用法

 因为在git使用当中，会有很多时候别人（供应商或者其他的开发人员）发过来一系列的**patch**，这些patch通常的是类似这样的名字：

```
0001--JFFS2-community-fix-with-not-use-OOB.patch
0002--Community-patch-for-Fix-mount-error-in.patch
```

里面包含了提交的日志，作者，日期等信息。

你想做的是把这些patch引入到你的代码库中，

最好是也可以把日志也引入进来， 方便以后维护用

传统的打patch方式是

```
 patch -p1 < 0001--JFFS2-community-fix-with-not-use-OOB.patch
```

这样来打patch，但是这样会把这些有用的信息丢失。

由于这些**patch显然是用git format-patch来生成的**，

所以用git的工具应该就可以很好的做好。

git-am 就是作这件事情。

在使用git-am之前， 你要首先git am –abort 一次，

来放弃掉以前的am信息，

这样才可以进行一次全新的am。

不然会遇到这样的错误。

```
.git/rebase-apply still exists but mbox given.
```



在解决完冲突以后， 比如用git add来让git知道你已经解决完冲突了。

- 如果你发现这个冲突是无法解决的， 要撤销整个am的东西。 可以运行git am –abort，
- 如果你想只是忽略这一个patch，可以运行git am –skip来跳过这个patch.

# hooks脚本

## 常用的git hook脚本有哪些

Git 提供了一系列的钩子（hooks），它们在 Git 仓库的特定事件发生时触发。这些钩子位于 `.git/hooks` 目录下，通常以.sample结尾，表示它们是示例文件。要启用一个钩子，你需要去掉.sample后缀，并确保它们是可执行的。
以下是一些常用的 Git 钩子：
1. **pre-commit**: 在 `git commit` 执行前触发，可以用来检查代码风格、运行测试、检查日志消息格式等。
2. **post-commit**: 在 `git commit` 执行后触发，通常用于通知或记录提交信息。
3. **pre-push**: 在 `git push` 执行前触发，可以用来检查推送是否满足某些条件，比如是否有足够的测试覆盖率。
4. **post-push**: 在 `git push` 执行后触发，可以用来清理工作副本或通知团队成员。
5. **pre-receive**: 在服务器端接收推送之前触发，可以用来阻止不满足特定条件的推送，比如提交消息格式错误或推送的分支不符合命名规范。
6. **post-receive**: 在服务器端接收推送后触发，可以用来部署应用程序、发送通知邮件等。
7. **update**: 与 `pre-receive` 类似，但在每个更新的引用上触发。它接收旧对象名称、新对象名称和引用名称作为参数。
8. **post-update**: 在 `git push` 成功更新引用后触发，可以用来更新服务器上的辅助文件或通知用户。
9. **pre-merge-commit**: 在 `git merge` 执行前触发，可以用来检查合并是否应该进行。
10. **applypatch-msg**: 在 `git am` 应用补丁前触发，可以用来检查补丁的提交消息。
11. **commit-msg**: 在 `git commit` 创建提交对象前触发，可以用来修改提交消息。
12. **pre-applypatch**: 在 `git am` 应用补丁后触发，可以用来运行测试。
13. **pre-auto-gc**: 在自动垃圾回收前触发，可以用来防止垃圾回收在某些情况下运行。
这些钩子为自定义 Git 工作流程提供了极大的灵活性。开发团队可以根据自己的需求编写相应的脚本来增强代码的质量控制和流程管理。



# 参考资料

1、git命令之git remote的用法

https://www.cnblogs.com/wuer888/p/7655856.html

2、菜鸟教程

http://www.runoob.com/git/git-branch.html

3、

https://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000/0013744142037508cf42e51debf49668810645e02887691000