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

C:\Users\Administrator\AppData\Roaming\Code\User

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



# 参考资料

1、

https://stackoverflow.com/questions/37777417/how-to-use-vim-key-bindings-with-visual-studio-code-vim-extension/38604086

2、How to use clipboard for Vim in VSCode

https://codeyarns.com/2018/04/26/how-to-use-clipboard-for-vim-in-vscode/