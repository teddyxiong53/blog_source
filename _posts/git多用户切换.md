---
title: git多用户切换
date: 2022-08-20 17:13:08
tags:
	- git

---

--

切换账号分两种情况：

1、http方式。

2、ssh/git方式。

http方式，直接通过配置用户名和邮箱进行修改即可。

ssh方式，则需要通过切换秘钥来实现。

如果是用git（ssh）方式clone代码，那修改git配置中的用户和邮箱就无效了，必须通过切换秘钥的方式来切换用户





生成秘钥：

```
ssh-keygen -t rsa -C "1073167306@qq.com"
```

然后在路径上，修改为id_rsa2的，不要把本来的覆盖了。

把这个id_rsa2.pub，上传到github上。



```
eval `ssh-agent -s`
Agent pid 1629870
```



现在我用git的方式下载我的仓库，还是失败的。

```
git clone git@github.com:br-yodaos/bryodaos-manifest.git
Cloning into 'bryodaos-manifest'...
git@github.com: Permission denied (publickey).
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
```

我把邮箱给出配置ssh 公钥的邮箱也还是不行。



以下命令可以检查当前用户：

```
ssh -T git@github.com
```

以下命令可以检查当前秘钥：

```
ssh-add -l
```

我查看怎么是没有呢？我明显配置了2个的。

```
ssh-add -l
The agent has no identities.
```

要看github官方这个说明。

https://docs.github.com/cn/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent



参考资料

1、

https://blog.csdn.net/weixin_45332196/article/details/117555354

2、

https://blog.csdn.net/lqlqlq007/article/details/80613272