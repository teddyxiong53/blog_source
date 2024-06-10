---
title: macos跟树莓派环境操作记录
date: 2024-06-08 13:30:09
tags:
	- 树莓派

---



现在是用macOS + 树莓派4b作为主要的实验环境。

# macos免密码登陆到树莓派并且远程编辑树莓派文件

思路就是使用sshfs。

```undefined
brew cask install osxfuse
brew install sshfs
```

当前我的macos版本是v11的，还比较低，安装有版本太老的提示。

https://www.jianshu.com/p/1f0ab12c52ab

# 树莓派上启动vscode-server

这个方式好

https://www.cnblogs.com/congtou001/p/remote_development_on_rpi.html

就用这个进行代码修改。

看起来cpu占用率也不高。

我目前只做python代码修改。不涉及c/c++，这个不怎么占用CPU。

