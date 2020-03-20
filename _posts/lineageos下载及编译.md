---
title: lineageos下载及编译
date: 2020-03-18 10:44:11
tags:
	- lineageos
---

1

首先下载repo工具，直接把下面的语句粘贴到shell执行就好了。要梯子。

```
mkdir ~/bin
PATH=~/bin:$PATH
curl https://storage.googleapis.com/git-repo-downloads/repo > ~/bin/repo
chmod a+x ~/bin/repo
```

创建目录。

```
mkdir lineageos_src
cd lineageos_src
```

初始化仓库，后面的分支必须带。而且需要先配置好你的git信息，就是email和username。没有配置会明确提示你进行配置的。

```
repo init -u https://mirrors.tuna.tsinghua.edu.cn/git/lineageOS/LineageOS/android.git -b cm-14.1
```

修改配置。现在目录下的配置文件位置是这个样子。

```
teddy@thinkpad:/media/teddy/seagate/lineageos_src/.repo$ tree -L 2
.
├── manifests
│   ├── default.xml
│   ├── README.mkdn
├── manifest.xml
```

主要是在default.xml里。

把上面这些行改成下面这样：

```
  4   <remote  name="github"
  5       fetch="github.com/" />
  6   <remote 
  7             name="lineage"
  8             fetch="https://mirrors.tuna.tsinghua.edu.cn/git/lineageOS/"
  9             review="review.lineageos.org"
 10       />
 11   <remote  name="private"
 12            fetch="ssh://git@github.com" />
 13   
 14   <remote  name="aosp"
 15            fetch="https://aosp.tuna.tsinghua.edu.cn"
 16            review="android-review.googlesource.com"
 17            revision="refs/tags/android-7.1.2_r36" />
 18   
 19   <default revision="refs/heads/cm-14.1"
 20            remote="lineage"
 21            sync-c="true"
 22            sync-j="4" />
```

然后关闭梯子。开始同步代码。

```
repo sync
```

部分仓库例如`Lineage_framework_base`同步的时候会出现bundle错误，这时候可以使用命令`repo sync --no-clone-bundle`进行同步就没有问题了

慢慢下载吧。用一个就的Ubuntu笔记本来下载，我放着一直不关机的。看看多久可以下载好。

需要切换到python3.6版本来使用repo。

同步的时候，有打印一些这个。

```
error: RPC failed; curl 56 GnuTLS recv error (-54): Error in the pull function.
```

网上说这样配置：

```
git config --global http.postBuffer 20000000
```

试一下。

还是有这种错误。

再增加将下面的配置试一下：

```
git config --global http.postBuffer 524288000
git config --global core.compression -1    
```

在~/.bashrc里加上：

```
export GIT_TRACE_PACKET=1
export GIT_TRACE=1
export GIT_CURL_VERBOSE=1
```

再试一下。

还是有这种问题。

stackoverflow上有说说，用openssl来重新编译git就可以解决这个问题。

学到一个Ubuntu下载源代码的最方便的方式：

```
sudo apt-get source git
```

这样就自动帮我们把代码下载下来还解压好了。真方便。

安装git依赖的东西

```
sudo apt-get build-dep git
```

```
sudo apt-get install libcurl4-openssl-dev
```

重新编译安装了git，再试一下。

现在gnutls的倒是没有了，但是openssl的报错了。问题的本质还是一样的。

```
* SSL read: error:00000000:lib(0):func(0):reason(0), errno 104
* Closing connection 0
error: RPC failed; curl 56 SSL read: error:00000000:lib(0):func(0):reason(0), errno 104
fatal: The remote end hung up unexpectedly
fatal: 过早的文件结束符（EOF）
fatal: index-pack failed
```





参考资料

1、lineageOS 源代码镜像使用帮助

https://mirror.tuna.tsinghua.edu.cn/help/lineageOS/

2、Git 克隆错误‘RPC failed; curl 56 Recv failure....’ 及克隆速度慢问题解决

https://blog.csdn.net/qq_34121797/article/details/79561110?depth_1-utm_source=distribute.pc_relevant.none-task&utm_source=distribute.pc_relevant.none-task

3、

https://devopscube.com/gnutls-handshake-failed-aws-codecommit/