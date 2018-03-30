---
title: vim编程环境配置（3）
date: 2018-03-30 17:29:12
tags:
	- vim

---



还是决定网上找一个一键配置的脚本来做。我用熟练就好了。

https://github.com/ma6174/vim-deprecated

地址在这里。

```
wget -qO- https://raw.github.com/ma6174/vim/master/setup.sh | sh -x
```

用这个命令一键安装，在Ubuntu16.04上，正常安装完成。没有报错。

在SecureCRT远程登录的终端里，会显示一个黑条。不好看。

这个是因为高亮了所在的列导致的。

找到`set cuc`。注释掉就好了。

下面是一些设置的意思。

```
set et 这个是为了把tab替换为空格。
" 不在单词中间折行
set lbr

set fo+=mB 
打开断行模块对亚洲语言支持。 m 表示允许在两个汉字之间断行， 即使汉字之间没有出现空格。 B 表示将两行合并为一行的时候， 汉字与汉字之间不要补空格。 该命令支持的更多的选项请参看用户手册。

set showmatch, 简写为set sm
set wildmenu 能帮你在命令行补全函数，带你走进补全的文明时代。但是要求laststus >= 2

```

