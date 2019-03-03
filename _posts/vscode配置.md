---
title: vscode配置
date: 2018-12-19 20:32:25
tags:
	- 编辑器

---



现在vscode特别火。学习一下这个编辑器的使用方法。

# 常用快捷键

F1：可以搜索各种东西。很好。



# 配置vim模式

有一个插件，就是vim模式的，安装后，reload一下插件就可以生效。

怎么把esc键remap一下呢？esc键太远了。

看到网上都是映射到`jj`上。

先按一下F1，找到user settings。然后改这个。

```
"vim.insertModeKeyBindings": [
     {
         "before": ["j", "j"],
         "after": ["<esc>"]
     }
]
```

让vim模式可以跟系统剪切板交互。

在user settings里，勾选useSystemClipboard。

# 打开空白显示

我习惯看到空格和tab键。

在user setting里搜索whitespace。就可以看到，勾选就好了。



# 配置文件的位置

C:\Users\Administrator\AppData\Roaming\Code\User\settings.json

我的当前是这样：

```
{
    "workbench.colorTheme": "Default Light+",
    "editor.minimap.enabled": false,
    "vim.insertModeKeyBindings": [
     {
         "before": ["j", "j"],
         "after": ["<esc>"]
     }
    ],
    "vim.useSystemClipboard": true,
    "files.trimTrailingWhitespace": true,
    "editor.renderWhitespace": "all"
}
```

# nodejs补全

搜索插件node.js，安装第一个就好了。



# 安装PlatformIO插件

这样开发esp8266就很方便了。



#配置调试html

搜索安装debugger for chrome



# workspace概念

在当前目录，右键，选择vscode打开目录。

如果进行了某些配置，会在当前目录下生成.vscode目录。里面放了一些配置。

典型的是有tasks.json、launch.json这2个文件。



# C语言自动补全

我一般都是在windows下工作。

但是我的开发是需要linux的。

vscode，在linux下，是可以很方便地进行stdio.h这些头文件及函数名进行补全的。

我觉得把linux的头文件拷贝到windows，然后把目录加入到vscode的索引目录下，应该是可以做到的。



# 配置python环境

1、安装插件。

2、记得import，不import对应的库，就不会补全的。

3、右键，有运行的选项。



# 配置python3环境

1、头部写上

```
#!/usr/bin/env python3
```

2、用python3语法写代码。

```
def func() ->int:
    return 1
print(func())
```

pylint提示出错。

3、把鼠标移动到错误上，根据提示安装python3的pylint。安装好后，reload一下vscode就好了。

在windows上，我的python环境都是靠anaconda来安装的。

安装了python2.7和python3.6的。

还是写python3语法的文件，出错，在左下角点击选择python版本就好了。



# 设置护眼色

https://blog.csdn.net/Lean_on_Me/article/details/84552487



# vue文件增加html补全

只需要在json配置文件里加上这个：

```
"files.associations": {
        "*.vue": "html"
    }
```





# 参考资料

1、

https://stackoverflow.com/questions/37777417/how-to-use-vim-key-bindings-with-visual-studio-code-vim-extension/38604086

2、How to use clipboard for Vim in VSCode

https://codeyarns.com/2018/04/26/how-to-use-clipboard-for-vim-in-vscode/

3、vscode调试html页面，及配置说明

https://www.cnblogs.com/codeww/p/7667543.html