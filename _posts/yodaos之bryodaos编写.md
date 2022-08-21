---
title: yodaos之bryodaos编写
date: 2022-08-20 16:30:08
tags:
	- yodaos

---

--

为了让自己更加深入掌握yodaos。并自己尝试做一个完整的repo管理项目。

我决定开始把yodaos的代码，移植到buildroot上。

这个的工作量还比较大，估计要占用我一段时间的周末和下班时间。

先慢慢做吧。动起来最重要。

也不要把太多的东西牵扯进来。

一切都尽量简化。

只使用github、repo。

gerrit、自动集成等，就暂时不涉及。

buildroot就使用buildroot-external机制。

把新增的package都放到外面，但是如果buildroot有需要改动的，我还是直接在buildroot里改（但是这个改动应该不多）。

硬件就使用树莓派3b。

# 8月20日

## 账号准备

bryodaos：读作BR yodaos。br表示buildroot。

这个新注册的账号使用teddyxiong53@sina.com的邮箱注册。

bryodaos上创建一个组织。

把我的主账号teddyxiong53邀请进去。

后续主要由teddyxiong53来负责提交代码。

看看是否行得通。

创建这个组织。

https://github.com/br-yodaos

邀请teddyxiong53加入这个组织。

而且可以选择邀请加入的人的身份，我把teddyxiong53设置为这个project的owner。

## 创建基础仓库

首先就是bryodaos-manifest仓库。

然后要把buildroot fork过来。

然后创建buildroot-external仓库。

先编译一个树莓派3b的基础镜像出来。

然后就开始慢慢往上面加仓库。



我现在有个问题，就是我的服务器上默认是git工作账号。

我现在做这个，是要用个人账号来做。

所以需要一个方式快速切换账号。

但是实际上很麻烦。

为了不把我的服务器搞乱。

我决定这个操作都在windows下执行吧。

windows下，默认就是1073167306@qq.com的账号。

现在添加ssh key到github.com。可以通过ssh把代码下载下来。

然后就看repo工具能不能在git bash里使用。

我电脑是安装了python的。

还是麻烦。

我另外有一台Ubuntu的笔记本，我有root权限，可以随便使用。

看看能不能把Ubuntu笔记本和服务器的目录打通。

我在Ubuntu笔记本下另外创建一个用户，就叫hanliang.xiong。

挂载不允许。

没有权限。



# 参考资料

