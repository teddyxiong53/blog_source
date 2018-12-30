---
title: Linux之wine安装配置
date: 2018-12-30 14:28:25
tags:
	- Linux

---



要在Linux上工作，有些windows下的工具，还是需要，通过wine来进行安装吧。

这个是官网。https://www.winehq.org/

现在最新版本是wine4.0-rc4。

安装还有点麻烦。安装下面的步骤来做。

1、64位系统开启32位架构支持。

```
sudo dpkg --add-architecture i386
```

2、下载添加仓库秘钥。

```
wget -nc https://dl.winehq.org/wine-builds/winehq.key
sudo apt-key add winehq.key
```

3、添加仓库。

这个是针对18.04的。

```
sudo apt-add-repository 'deb https://dl.winehq.org/wine-builds/ubuntu/ bionic main'
```

16.04的用这个：

```
sudo apt-add-repository 'deb https://dl.winehq.org/wine-builds/ubuntu/ xenial main'
```

我的是16.04的。运行。报了错。

```
ModuleNotFoundError: No module named 'apt_pkg'
```

需要安装这个：

```
sudo apt-get install python-apt
```

还是不行。根本原因是，我的python3安装了2个版本，一个3.5的，一个3.6的。

```
$ cd /usr/lib/python3/dist-packages/
$ sudo cp apt_pkg.cpython-35m-x86_64-linux-gnu.so apt_pkg.cpython-36m-x86_64-linux-gnu.so 
```

这个做了就好了。

继续回到wine的安装。

4、更新一下。

```
sudo apt-get update
```

直接更新是更新不下来的。

需要设置apt-get代理。

从Ubuntu10.04开始，就不使用http_proxy来做apt-get的代理了。

在/etc/apt目录下，新建apt.conf文件。写入下面的内容。

```
Acquire::https::proxy "https://127.0.0.1:8123/";
Acquire::http::proxy "http://127.0.0.1:8123/";
```

```
2018-12-30 15:05:32 INFO     connecting archive.canonical.com:80 from 127.0.0.1:41286
2018-12-30 15:05:45 WARNING  timed out
```

不能跳过这一步。还是挂着代理过了。

5、安装。

```
sudo apt install --install-recommends winehq-stable
```

这个要下载几百兆东西。

到这里安装就完成了。

下载要配置。

```
winecfg
```

不用用root权限运行。

会到~目录下生成一个.wine目录。

结构是这：

```
hlxiong@hlxiong-VirtualBox:~/.wine$ tree -L 1
.
├── dosdevices
├── drive_c
├── system.reg
├── userdef.reg
└── user.reg
```

输入regedit，可以得到一个跟windows一样 的注册表编辑器。

wineconsole，可以得到一个windows命令行。



使用。

```
wine xxx.exe
```

xxx可以是安装程序，也可以直接运行的。

安装clover。运行不正常。因为clover对explorer.exe依赖非常大。







参考资料

1、wine安装＋中文配置＋使用总结贴

https://blog.csdn.net/zzxian/article/details/7166572

2、安装 WineHQ 安装包

https://wiki.winehq.org/Ubuntu_zhcn

3、更换python版本后出现 No module named "apt_pkg"

https://blog.csdn.net/jaket5219999/article/details/78464310

4、

http://wiki.ubuntu.org.cn/WineGuide