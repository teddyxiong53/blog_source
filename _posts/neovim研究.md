---
title: neovim研究
date: 2023-01-06 17:20:32
tags:
	- vim
---

--

电脑的基于electron的程序太多了。16G的内存都不够用了。

非常卡，决定找一个vscode的轻量级替代品。

neovim现在比较流行，研究一下。

这个使用lua作为配置语法。而且neovim是全新重写的。

网上很多人配置都很漂亮，研究一下。

参考这个来学习。

https://learnku.com/articles/68258

从这里下载。

https://github.com/neovim/neovim/releases/download/stable/nvim-linux64.tar.gz

需要先安装packer.nvim（这个插件lua写的）

```
git clone --depth 1 https://github.com/wbthomason/packer.nvim\
 ~/.local/share/nvim/site/pack/packer/start/packer.nvim
```

然后下载这个配置

```
git clone https://github.com/leslie255/nvim-config.git ~/.config/nvim
```

然后nvim打开，会有一些错误提示，不管，这个是因为需要的插件没有安装好。

输入：`:PackerInstall`来安装插件。

一共39个插件，都是基于lua的。很快就安装好了。

使用了外置的lsp server来做语法解析。

用这个来搭建这个外部的lsp server。

https://github.com/neovim/nvim-lspconfig



这个插件是用openai来自动生成代码。

https://github.com/aduros/ai.vim



neovim是C语言写的。



参考资料

1、

https://www.xwxwgo.com/post/2022/01/18/neovim%E5%BC%80%E5%8F%91%E7%8E%AF%E5%A2%83%E9%85%8D%E7%BD%AE/