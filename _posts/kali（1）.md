---
title: kali（1）
date: 2020-03-09 09:16:28
tags:
	- kali

---

1

现在重新学习一下kali的使用。

安装两套：

1、MacBook下，用虚拟机安装。64位版本。

2、Ubuntu下，安装kali工具包。这个是直接在笔记本物理机上安装。64位版本。

MacBook下安装的是2019.4版本，这个是目前的最新版本。

# Ubuntu安装kali

有个工具，叫katoolin，就是用在在Ubuntu下安装kali工具的。

```
git clone https://github.com/LionSec/katoolin
```

这个就是一个python脚本。

```
sudo  cp katoolin/katoolin.py /usr/bin/katoolin 
sudo chmod 777 /usr/bin/katoolin 
```

然后sudo katoolin执行。

```
这个会提供一个文字菜单让你选择。
另外有2个命令：
gohome和back。可以在菜单之间回退。
```

现在选择安装所有的软件。所有的都是提示。

```
E: 无法定位软件包 acccheck
E: 无法定位软件包 automater
E: 无法定位软件包 dnmap
E: 无法定位软件包 fragroute
```

```
deb http://mirrors.aliyun.com/kali kali main non-free contrib
deb-src http://mirrors.aliyun.com/kali kali main non-free contrib
deb http://mirrors.aliyun.com/kali-security kali/updates main contrib non-free
```

修改source.list文件，把上面的源添加进去。

还是不行。

```
sudo add-apt-repository universe
```

可以看到是自动配置的东软的镜像。

mirrors.neusoft.edu.cn



在我的阿里云服务器上安装试一下。也是一样，有很多包找不到。

我退一步，先只安装metasploit的。

安装好了metasploit 。





参考资料

1、如何在Ubuntu中安装Kali Linux安全测试工具

https://www.linuxidc.com/Linux/2018-11/155269.htm

2、kali sudo apt install 无法定位软件包

https://blog.csdn.net/dongyanwen6036/article/details/77488653