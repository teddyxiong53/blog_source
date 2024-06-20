---
title: macos（1）
date: 2019-01-08 13:37:25
tags:
	- mac

---



# 按键

终于还是买了一个MacBook，按键操作上还不习惯。

看看怎么才能高效使用。

3个修饰键：

command：相当于windows的ctrl。command+c就是复制。给图形界面做辅助的。

option：相当于windows的alt。

control：终端下面的作用是ctrl键的作用，例如ctrl+c是终止。这个键也是主要在终端下面用的。

```
Control在命令行（Shell、EMACS等）下是有特定的的快捷键的，OSX作为Unix系统，将这些快捷键在GUI系统中也保留了下来：Control+A（行首）、Control+E（行尾）、Control+B（方向左）、Control+F（方向右）、Control+P（方向上）、Control+N（方向下）、Control+D（向后删除，可理解为Windows上的Delete）、Control+H（向前删除，可理解为Backspace）、Control+K（可理解为剪切）、Control+Y（可理解为黏贴）
```

可以简单的认为，Command是和图形界面相关的快捷键，Control多与命令行界面相关。

从新的修饰键引入这个角度上讲，Command的引入，要比Windows上的Win键严谨、有效的多。

1、一些快捷键在GUI下和命令行下的意义冲突，例如Control+C；

2、Windows键引入，带来的快捷键非常少，在Windows7之前的操作系统中，只有Win+D，Win+M以及单独按Win键激活开始菜单等相当少得几个，几乎可有可无，直到Win7开始才有所改善（WIn+Space、Win+方向、Win+数字、Win+Tab、Win+X、Win+B)。

```
一句话解释：
Ctrl系列快捷键功能在计算机图形界面出现之前的命令行界面已有定义；Windows图形界面还是使用Ctrl键，但对各种组合的功能涵义进行了重新定义；而Mac OS的图形界面新设计了一个键Command来负责。
```

微软造Windows的时候没怎么考虑用户还需要使用命令行模式，所以无视冲突直接复用了Ctrl键，重新定义了一大套快捷键功能。

而Mac OS X属于*nix家族，需要两者兼容，所以另造了Command键（有段时间也是苹果徽标键）负责图形界面快捷键，而Ctrl保留给命令行界面（亦渐渐承担了一些不会发生冲突的图形界面功能）。

至于现代Linux流行发行版（以图形界面作为主要工作模式之一的），考虑到市面上键盘的流行程度，不得不沿用Windows的Ctrl键用法。



总之，在图形界面下，就当control不存在，在终端里，就当command不存在。



如果用的是windows键盘，怎么统一按键位置？不至于让自己很分裂？



早起的unix键盘布局，是hhkb键盘的布局。



# 翻墙

v2ray可以。

clashx也可以。我是用这个。



# 配置搜狗输入法





# 配置brew源



# 配置wine



# 下载工具

FDM。



# 大写锁定

windows键盘连接到MacBook。

capslock键的功能是这样：

1、短按。是切换中英文。

2、长按半秒。打开关闭大写锁定。



# 安装虚拟机

算了，放弃了。我的需求不大。空间也不太够。



# 必备软件列表

calibre：电子书软件。跟kindle配合。





# 浏览器

chrome浏览器总是有些地方不顺手。我找了各种插件，还是无法解决我的痛点。

搜狗浏览器又没有mac版本。而QQ浏览器有mac版本。

QQ浏览器的使用体验跟搜狗的差不多。

所以现在就全面切到QQ浏览器了。

反正我qq系的软件用得也挺多。我对腾讯还谈不上讨厌。

chrome虽然很强大，但是我只要在做开发相关的事情时才用。

我的账号体系都是基于qq的，所以切换到QQ浏览器也是很顺畅的。

从此搜狗浏览器退出我的应用包了。



# 网站

https://www.isofts.org/

这个网站很好。很多软件。

以后主要就从这里下载了。

# 电脑管家

腾讯出了柠檬电脑管家。

不过也只能清理一下垃圾。

先安装。

# sudo不要输入密码

```
sudo vi /etc/sudoers
```

把这句修改：

```
#%admin ALL=(ALL) ALL 修改为：
%admin ALL=(ALL) NOPASSWD: NOPASSWD: ALL
```



# 命令行和Linux兼容

现在默认是不兼容的。用起来很别扭。

```
brew install coreutils
```

在~/.bash_profile里加上这一行。

```
export PATH="$(brew --prefix coreutils)/libexec/gnubin:/usr/local/bin:$PATH"
```

现在基本工具的就工作正常了。

然后安装其他的基本工具。

```
brew install binutils
brew install diffutils
brew install ed --default-names
brew install findutils --with-default-names
brew install gawk
brew install gnu-indent --with-default-names
brew install gnu-sed --with-default-names
brew install gnu-tar --with-default-names
brew install gnu-which --with-default-names
brew install gnutls
brew install grep --with-default-names
brew install gzip
brew install screen
brew install watch
brew install wdiff --with-gettext
brew install wget
brew install bash
brew install emacs
brew install gdb  # gdb requires further actions to make it work. See `brew info gdb`.
brew install gpatch
brew install m4
brew install make
brew install nano
```

放到脚本里，一次执行。



# brew国内加速

为了在中国大陆加速 Homebrew 的使用，可以配置 Homebrew 使用国内镜像源。以下是详细的配置步骤：

**1. 替换 Homebrew 源**

```bash
# 替换 Homebrew 源
git -C "$(brew --repo)" remote set-url origin https://mirrors.ustc.edu.cn/brew.git
```

**2. 替换 Homebrew Core 源**

```bash
# 替换 Homebrew Core 源
brew tap --custom-remote --force-auto-update homebrew/core https://mirrors.ustc.edu.cn/homebrew-core.git
```

**3. 替换 Homebrew Bottles 源**

```bash
# 替换 Homebrew Bottles 源
echo 'export HOMEBREW_BOTTLE_DOMAIN=https://mirrors.ustc.edu.cn/homebrew-bottles' >> ~/.bash_profile
source ~/.bash_profile
```

**4. 更新 Homebrew 配置**

```bash
# 更新 Homebrew 配置
brew update
```

**5. 验证配置**

可以通过以下命令来验证配置是否正确：

```bash
# 查看 Homebrew 源
git -C "$(brew --repo)" remote -v

# 查看 Homebrew Core 源
brew tap

# 查看环境变量
echo $HOMEBREW_BOTTLE_DOMAIN
```

通过以上步骤，可以有效加速 Homebrew 在中国大陆的使用。以下是步骤的简要总结：

| **步骤**                    | **命令**                                                     |
| --------------------------- | ------------------------------------------------------------ |
| 1. 替换 Homebrew 源         | `git -C "$(brew --repo)" remote set-url origin https://mirrors.ustc.edu.cn/brew.git` |
| 2. 替换 Homebrew Core 源    | `brew tap --custom-remote --force-auto-update homebrew/core https://mirrors.ustc.edu.cn/homebrew-core.git` |
| 3. 替换 Homebrew Bottles 源 | `echo 'export HOMEBREW_BOTTLE_DOMAIN=https://mirrors.ustc.edu.cn/homebrew-bottles' >> ~/.bash_profile` |
| 4. 更新 Homebrew 配置       | `brew update`                                                |
| 5. 验证配置                 | `git -C "$(brew --repo)" remote -v` `brew tap` `echo $HOMEBREW_BOTTLE_DOMAIN` |

这样配置后，Homebrew 会使用国内镜像源来加速软件包的下载和安装。

# brew的一些术语

https://chuquan.me/2023/08/27/understand-the-design-of-homebrew/

# brew打开详细的打印

经常安装就是需要进行源代码编译。

但是默认又没有什么打印，有什么卡住很久，不知道发生了什么。

所以最好是可以看到详细的安装打印。

```
brew install --verbose --debug xx
```

这样就可以了。



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

1、

https://www.logcg.com/archives/564.html

2、怎样统一 Windows 和 Mac 上的快捷键使用体验？

https://www.zhihu.com/question/27564773

3、为什么苹果公司不将 Mac 的 command 键和 control 键合并？

https://www.zhihu.com/question/19814844

4、

https://bbs.feng.com/read-htm-tid-11683407.html

5、macOS安装GNU命令行工具

https://blog.csdn.net/orangleliu/article/details/47357339

6、Mac 开发环境配置

https://www.jianshu.com/p/b5bdf9302789

7、Mac下的效率工具autojump

https://www.cnblogs.com/LeeScofiled/p/7860144.html

8、主题乱码解决。

https://gist.github.com/kevin-smets/8568070