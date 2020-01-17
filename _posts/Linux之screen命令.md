---
title: Linux之screen命令
date: 2020-01-16 15:52:19
tags:
	- Linux
---

1

用vim编辑文件，很自然产生了分出半屏来执行shell命令的需求。

screen就可以帮助我实现这个功能。

安装：

```
sudo apt-get install screen
```

执行，执行输入screen就可以，但是建议带上名字：

```
screen -S xhl
```

screen启动后，会创建第一个窗口，也就是窗口0 ，并在其中打开一个shell。

所以输入screen之后，你看到的是马上回到了shell界面，但是实际上你已经进入到screen的世界了。

screen后面，你可以加上自己的命令，例如，用vi打开文件：

```
screen vi 1.txt
```

我们这样执行一下：

```
screen -S xhl
# 然后在screen里，再执行一个screen，打开vi
screen vi 1.txt
```

按一下ctrl+a，然后按w。在下面会列出当前打开的窗口。

```
0-$ bash  1*$ vi   
```

离开会话和恢复会话。

```
离开会话
	ctrl+a，再按一下d
恢复会话
	screen -ls
	
```

用了一下，感觉不是很好。所以不继续了。

转向tmux。





参考资料

1、

https://www.cnblogs.com/mchina/archive/2013/01/30/2880680.html