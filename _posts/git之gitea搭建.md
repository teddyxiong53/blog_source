---
title: git之gitea搭建
date: 2022-01-08 12:27:11
tags:
	- git

---

--

最近看到gitea这个简单实用的git服务软件，是国人开发的 ，然后还看了B站上的一个分享相关技术的视频，加了对应的QQ群。所以产生了一些兴趣。是用go语言写的。相比于gitlab和github实用ruby语言，go语言我希望能够了解一些实际的项目，而且go语言也是我希望了解的。

所以打算通过gitea这个项目来加深对go语言和git的了解和掌握。

gitea的主要特色就是安装部署非常简单。

我就在我的服务器上来安装部署，通过宝塔来安装和配置服务访问。做成一个实用的服务。自己可以用一用。

我尽量不通过docker的方式。

数据库就实用sqlite。这样更方便把握，性能不是我的追求，我现在是希望所有的部分都足够小，可以掌握。

二进制在这里

https://dl.gitea.io/gitea/1.15.9

上面这个地址下载速度非常慢。

不如用下面这个地址的。

https://github.com/go-gitea/gitea/releases

运行

```
./gitea web -p 3456
```

然后访问这个地址，就会进入到配置界面。

我放在gitea_dir下面执行gitea程序。

选择sqlite数据库。

默认的文件路径是

```
home/ubuntu/gitea_dir/data/gitea.db
```

默认的仓库根目录

```
/home/ubuntu/gitea_dir/data/gitea-repositories
```

然后就可以访问了。可以注册登录，可以创建仓库。界面比较简洁。

然后可以看看代码。



参考资料

1、
