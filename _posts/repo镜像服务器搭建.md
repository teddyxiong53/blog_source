---
title: repo镜像服务器搭建
date: 2020-04-14 14:21:51
tags:
	- repo

---

1

现在使用repo都是在client端操作，想知道服务端那边的操作。

所以自己搭建一个服务，看看是怎样操作的。

就在我的Ubuntu笔记本上进行搭建。

为了方便操作，直接`su - root`了来进行操作。

```
apt-get install openssh-server git keychain
```

keychain是为了生成公钥私钥的。

然后添加一个名字叫git的用户。

```
adduser git
```

切换到git用户登陆。

```
su - git
```

下载gitolite的代码，这个是用来搭建git服务器的。

```
git clone https://github.com/sitaramc/gitolite.git
```

```
mkdir /home/git/bin
# 如果提示权限问题，则以teddy的身份来进行拷贝操作。
cp /home/teddy/.ssh/id_rsa.pub /home/git
```

```
/home/git/gitolite/install -to /home/git/bin
```

```
/home/git/bin/gitolite setup -pk /home/git/id_rsa.pub
```

把管理员的id_rsa文件拷贝到/home/git/.ssh目录下，并改名为teddy。

修改一下teddy这个文件的权限。

```
chown git:git teddy
chmod 600 .ssh/teddy
```



# lindenis项目举例

这个是一个linux开发板。项目相对来说没有那么复杂。

可以作为学习材料。

```
repo init -u https://github.com/lindenis-org/manifest.git -b v831 -m v833-lindenis.xml
```

https://github.com/lindenis-org/manifest.git 这个是github上一个仓库。里面就放的一个xml文件。

这个仓库的一个分支叫v831，这个分支下，有v833-lindenis.xml文件。

所以，并不存在一个repo服务器。

repo的xml文件，也只是一个普通的git仓库。



参考资料

1、REPO镜像服务器的搭建

https://blog.csdn.net/u011365633/article/details/78451565?utm_source=blogxgwz0