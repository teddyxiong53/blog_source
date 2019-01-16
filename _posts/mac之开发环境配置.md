---
title: mac之开发环境配置
date: 2019-01-16 13:22:59
tags:
	- mac
---



安装iterm2，把iterm2设置为默认的终端工具。

下载地址是：http://iterm2.com

在菜单点击iterm2==>设置iterm2为默认终端就好了。

下载solarize配色。

解压好。

然后在iterm2==>profiles==>colors==>右下角color preset==>选择import==>选择下载的solarize配色。

安装on-my-zsh。

```
sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
```

会提示你输入密码的。

配置zsh。

运行文件是~/.zshrc。

可以修改这个文件，我把我的bash_profile加到这里。

这样我自己的设置还能继续生效。

配置zsh的插件。插件目录是~/.oh-my-zsh目录。

on-my-zsh已经带了一大堆的theme和插件了。

可以自己尝试去打开试一试。

默认只打开了git插件。

安装autojump。

```
brew install autojump
```

把下面的代码加入到.zshrc里。

```
[[ -s $(brew --prefix)/etc/profile.d/autojump.sh ]] && . $(brew --prefix)/etc/profile.d/autojump.sh
```

还需要zshrc里的plugins里面加上autojump。

的确挺好用的。

zsh换主题。

agnoster这个主体很好看。但是默认改了会有显示问题。

因为需要安装字体才行。

安装字体后，还在iterm2里进行设置。



参考资料

1、Mac 开发环境配置

https://www.jianshu.com/p/b5bdf9302789

2、Mac下的效率工具autojump

https://www.cnblogs.com/LeeScofiled/p/7860144.html

3、主题乱码解决。

https://gist.github.com/kevin-smets/8568070