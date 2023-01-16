---
title: spacevim研究
date: 2023-01-12 12:15:31
tags:
	- vim

---

spacevim是国人写的一套开箱即用的vim集成环境。

目标是做到开箱即用的基于vim的IDE。

安装

```
curl -sLf https://spacevim.org/cn/install.sh | bash
```

SpaceVim 的默认配置文件为 `~/.SpaceVim.d/init.toml`。下面为一简单的配置示例。 如果需要查阅更多 SpaceVim 配置相关的信息，请阅读 SpaceVim 用户文档。

SpaceVim 的配置文件有两种，一种是全局配置文件(`~/.SpaceVim.d/init.toml`)， 另外一种是项目专属配置文件，即为项目根目录的配置(`.SpaceVim.d/init.toml`)。

我们可以这样理解，在全局配置文件里，主要设置一些常规的选项和模块， 比如 `shell` 模块、`tags` 模块。 项目专属配置文件则通常用来配置跟当前项目相关的模块及选项，比如对于 python 项目， 可以在项目专属配置文件里启用 `lang#python` 模块。



这样操作的好处在于，当处理多个不同语言项目是，不需要频繁更新配置文件，也不用担心载入过多的冗余插件，和无关的语言模块。

# 使用文档

## 核心思想

四大核心思想：记忆辅助、可视化交互、一致性、社区驱动。

**记忆辅助**

所有快捷键，根据其功能的不同分为不同的组， 以相应的按键作为前缀，例如 `b` 为 buffer 相关快捷键前缀， `p` 为 project 相关快捷键前缀，`s` 为 search 相关快捷键前缀， `h` 为 help 相关快捷键前缀。

**可视化交互**

创新的实时快捷键辅助系统，以及查询系统， 方便快捷查询到可用的模块、插件以及其它更多信息。

**一致性**

相似的功能使用同样的快捷键，这在 SpaceVim 中随处可见。 这得益于明确的约定。其它模块的文档都以此为基础。

**社区驱动**

社区驱动，保证了 bug 修复的速度，以及新特性更新的速度。

## 显著特性

详细的文档：通过`:h SpaceVim`来查看帮助。

优雅简洁的界面。

保证手指不离开主键盘区。使用空格键作为前缀键。

快捷键辅助系统：当你的输入出现停滞，就会弹出提示。

更快的启动：受益于dein.vim，90%的插件都是按需载入的。

更少的肌肉损伤：频繁使用空格键。

更易扩展。

完美支持neovim：受益于neovim的特性，运行在neovim下体验会更好。



# 快捷键

这个列举了常用的快捷键。

https://github.com/Jackiexiao/10-minutes-to-SpaceVim/blob/master/README-zh.md

SpaceVim中的快捷键都容易记忆，窗口（window）就是w，文件（file）就是f，缓冲区（buffer）就是b，Tab管理就是t。再加上按SPC键后，每个功能都有字母提示，几乎不用再去找某个功能的文档。

# 取消相对行号

在`~/.SpaceVim.d/init.toml`的option下面，加上：

```
relativenumber = false
```

# 怎么进行工程和会话管理



# 参考资料

1、

https://spacevim.org/cn/documentation/#%E6%A0%B8%E5%BF%83%E6%80%9D%E6%83%B3

2、

https://chengpengzhao.com/2021-10-06-vim-sheng-ji-neovim/