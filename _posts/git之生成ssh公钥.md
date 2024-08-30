---
title: git之生成ssh公钥
date: 2020-04-14 14:39:51
tags:
	- git
---

--

许多git服务器都使用了ssh公钥进行认证。

为了向git服务器提供ssh公钥，如果你还没有公钥，就需要先生成一份。

这个生成公钥的过程，在不同的os上都是一样的操作。

首先，你需要确认自己是否已经拥有密钥。

到~/.ssh目录下去查看。

例如这样：

```
hlxiong@hlxiong-VirtualBox:~/.ssh$ tree
.
├── id_rsa
├── id_rsa.pub
└── known_hosts
```

id_rsa这个就是私钥。id_rsa.pub这个就是公钥。

这个就是有。

如果没有这个目录或者文件，也没有关系，我们执行命令来生成一下就好了。

你安装了git后，它附带帮你把这个工具生成了。

这个工具叫ssh-keygen。

执行：

```
ssh-keygen -o
```

提示你输入密码，不用输入，直接回车。

然后我们把得到的id_rsa.pub文件，发送给git服务器的管理员。



参考资料

1、服务器上的 Git - 生成 SSH 公钥

https://git-scm.com/book/zh/v2/%E6%9C%8D%E5%8A%A1%E5%99%A8%E4%B8%8A%E7%9A%84-Git-%E7%94%9F%E6%88%90-SSH-%E5%85%AC%E9%92%A5