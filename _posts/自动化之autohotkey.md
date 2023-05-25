---
title: 自动化之autohotkey
date: 2023-05-09 15:05:11
tags:
	- 自动化
---

--

直接参考帮助文档来学习。

是开源的，代码在这里：

https://github.com/AutoHotkey/AutoHotkey

从这里看，

https://github.com/ahkscript/awesome-AutoHotkey

ahk脚本还比较完备，可以写http server等东西。



# 运行HelloWorld

新建一个hello.ahk文件。

```
#z::Run "https://www.autohotkey.com"  ; Win+Z

^!n::  ; Ctrl+Alt+N
{
    if WinExist("Untitled - Notepad")
        WinActivate
    else
        Run "Notepad"
}
```

然后用命令行里ahk.exe hello.ahk来运行。

这样启动了一个后台进程。

这个脚本的逻辑是：你按下ctrl+alt+N键，则打开notepad程序。



# 参考资料

1、

这个文档已经过时了。不匹配。例子跑不起来。

https://wyagd001.github.io/zh-cn/docs/Hotkeys.htm