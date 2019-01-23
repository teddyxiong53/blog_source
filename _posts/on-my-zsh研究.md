---
title: on-my-zsh研究
date: 2019-01-16 14:12:59
tags:
	- zsh
---



一直用基本的bash，现在在配置mac的开发环境的时候，发现zsh还真的很好用。

所以研究一下，在Linux上也用起来。

代码在这：

https://github.com/robbyrussell/oh-my-zsh

官网在：https://ohmyz.sh/

重点看插件的用法。

插件分类：

```
生产力
FS jumping
build工具。
nodejs
python
macos
misc
```

生产力

```

```



# ubuntu安装zsh

```
sudo apt-get install zsh
```

查看版本。

````
hlxiong@hlxiong-VirtualBox:~$ zsh --version
zsh 5.1.1 (x86_64-ubuntu-linux-gnu)
````

修改默认的sh。

```
chsh -s $(which zsh)
```

不用用sudo来执行chsh，否则就是改的root用户的。

修改密码文件/etc/passwd。把自己的sh改成zsh的。

还有要把root用户的改成/bin/zsh。这个跟sudo chsh -s $(which zsh)效果是一样的。

注销重新登陆。





安装oh-my-zsh。也不用用sudo权限。

```
sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
```

这样之后，你的脚本默认启动就是执行.zshrc了。而不是之前的.bashrc。

所以需要把自己的环境变量的修改代码挪过来。



安装autojump。

```
sudo apt-get install autojump
```

在~/.zshrc的最后一行加上：

```
. /usr/share/autojump/autojump.sh
```

安装zsh的语法高亮插件。

```
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git
echo "source ${(q-)PWD}/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh" >> ${ZDOTDIR:-$HOME}/.zshrc
```

改了zshrc的都需要source一下来生效。

安装语法历史记录插件。

```
git clone git://github.com/zsh-users/zsh-autosuggestions $ZSH_CUSTOM/plugins/zsh-autosuggestions
```

需要修改~/.zshrc文件。

把这个插件加进去。本来默认只开启了git插件的。

```
plugins=(git zsh-autosuggestions)
```

然后还需要在zshrc的最后一行加上：

```
source $ZSH_CUSTOM/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh
```

然后还需要配置主题。

```

```







参考资料

1、Ubuntu 16.04下安装zsh和oh-my-zsh

https://www.cnblogs.com/EasonJim/p/7863099.html

