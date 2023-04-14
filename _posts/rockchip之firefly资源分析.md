---
title: rockchip之firefly资源分析
date: 2021-08-18 15:18:33
tags:
	- rockchip

---

--

代码放在github上

从这里下载

```
repo init --repo-url=https://github.com/FireflyTeam/repo -u https://github.com/FireflyTeam/manifests
```

只有36个project，不算多。

去代码会失败，我单独去buildroot部分吧。

repo sync buildroot

make一下，看到.config里，默认这个也是有的。

BR2_PACKAGE_IFUPDOWN_SCRIPTS=y

之所以不慢，我估计是没有启动ap方式的配网。



```
#!shell
$ mkdir -p ~/prj/Firefly-RK3308
$ cd ~/prj/Firefly-RK3308
$ 7zr x Firefly-RK3308_Linux_SDK_git_20181008.7z
$ git reset --hard
```

解压后只有一个.git目录。所以需要git reset才能看到代码。

下面的readme里有说明。

然后可以看从gitlab来更新代码。

```
#!shell
$ git pull gitlab firefly:firefly
```

可以在这里在线浏览代码。

[https://gitlab.com/TeeFirefly/rk3308-linux](https://gitlab.com/TeeFirefly/rk3308-linux) 

# 参考资料

1、

https://www.t-firefly.com/doc/product/info/267.html

2、

https://www.codenong.com/cs106544012/