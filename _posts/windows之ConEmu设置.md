---
title: windows之ConEmu设置
date: 2018-07-31 11:28:29
tags:
	- windows

---



需要在Windows下用ConEmu来连接adb。

但是不能补全。研究一下。

http://cmder.net/



设置用git bash来启动。

设置，Startup，Specific named task。选择bash。



分析cmder mini版本的文件构成。

```
hlxiong@hlxiong-VirtualBox:~/work/tmp/cmder_mini$ tree -L 2
.
├── bin
│   ├── alias.bat
│   └── Readme.md
├── Cmder.exe
├── config：这里存放所有的配置文件。
│   ├── ConEmu.xml
│   └── Readme.md
├── icons
├── LICENSE：用MIT协议开源。
├── vendor：这个目录最重要。
│   ├── clink
│   ├── clink-completions
│   ├── clink.lua
│   ├── cmder_exinit
│   ├── conemu-maximus5
│   ├── init.bat
│   ├── lib
│   ├── profile.ps1
│   ├── psmodules
│   ├── Readme.md
│   ├── sources.json
│   └── user-aliases.cmd.example
└── Version 1.3.6.678：空文件，用文件名来标记版本。
```

运行后，config目录下会生成一些文件。



补全靠的是clink。这个需要设置：

设置，Features，use Clink in prompt。

会提示你找不到，你需要做的是把Z:\work\tmp\cmder_mini\vendor\clink目录下的内容拷贝到Z:\work\tmp\cmder_mini\vendor\conemu-maximus5\ConEmu\clink

这样启动后，有一些不同，但是adb shell还是不能补全。



# 跟msys2结合

什么是msys2？

msys2是在mingw的基础上增加了一些其他的东西，例如包管理器。它的包管理器是pacman。





我之前下载的都是cmder。现在我直接下载conemu看看。

https://www.fosshub.com/ConEmu.html



adb shell里不能补全的锅，应该是adb自己的。我的当前的adb版本是1.0.32 。

下载这个，是1.0.40的。果然就是可以补全的。

https://dl.google.com/android/repository/platform-tools_r28.0.0-windows.zip

解压后，全部放到C:\Windows\system目录下就可以了。

#参考资料

1、官网帮助

https://conemu.github.io/en/SettingsEnvironment.html

2、在 Conemu 中使用 WSL

https://rabbit52.com/2018/03/wsl-on-conemu/

3、

https://www.jianshu.com/p/b691b48bcee3

4、How to enable 256-color console Vim syntax highlight in ConEmu

https://conemu.github.io/en/VimXterm.html

5、Conemu, Msys2 工具整合，提升windows下控制台工作效率

http://www.bubuko.com/infodetail-2507958.html

6、windows搭建gcc开发环境(msys2)

https://blog.csdn.net/qiuzhiqian1990/article/details/56671839

7、msys2配置记录

https://www.jianshu.com/p/c740b71e7775