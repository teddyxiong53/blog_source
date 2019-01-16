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
sudo chsh -s $(which zsh)
```

注销重新登陆。

```

```



安装oh-my-zsh。

```
sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
```



