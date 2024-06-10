---
title: mac之开发环境配置
date: 2019-01-16 13:22:59
tags:
	- mac
---



# Iterm2

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

# 命令行配置为gnu命令

https://cotes.page/posts/use-gnu-utilities-in-mac/

```
brew install coreutils
brew install findutils
brew install gnu-sed
brew install gnu-indent
brew install gnu-tar
brew install gnu-which
brew install gnutls
brew install grep
brew install gzip
brew install screen
brew install watch
brew install wdiff --with-gettext
brew install wget
brew install less
brew install unzip
```

## 覆盖系统自带命令

`Homebrew` 安装的命令工具默认放置在 `/usr/local/opt/`，而系统自带 BSD 工具的路径为 `/usr/bin/`。当安装的 GNU 命令与系统自带命令重复时，用前缀 `g` 可以指定使用 GNU 版本，如：

```
$ gsed    # 使用 GNU 版本的 sed (gnu-sed)

$ sed     # 使用 BSD 版的 sed
```

如果想省去 `g` 前缀，在环境变量 `PATH` 中把 GNU 工具的执行路径放置于 `/usr/bin` 之前即可（在安装命令工具的时候，输出日志就有指示）。原理是在系统扫描可执行路径时，会使用第一个符合条件的值：

# zsh的profile

不是.zsh_profile，而是.zprofile。

# 安装docker

https://www.runoob.com/docker/macos-docker-install.html



# 参考资料

1、Mac 开发环境配置

https://www.jianshu.com/p/b5bdf9302789

2、Mac下的效率工具autojump

https://www.cnblogs.com/LeeScofiled/p/7860144.html

3、主题乱码解决。

https://gist.github.com/kevin-smets/8568070