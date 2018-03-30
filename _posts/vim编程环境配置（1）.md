---
title: vim编程环境配置（1）
date: 2016-10-22 22:40:50
tags:
	- vim
typora-root-url: ..\
---
要在linux玩得很溜，vim是必须要迈过的一道坎，要迈过这道坎，就得抛弃其他的编程工具，把vim作为主力编辑器来使用。但是基本的vim环境用来编程无疑是非常简陋的，效率低下，使用起来非常痛苦。到目前为止，也在几台电脑上分别配置过vim编程环境，但是有时候又下载了太多的插件，导致各种混乱。而反复配置，也浪费时间精力。所以写这篇文章进行梳理，遵守的基本原则是：简单易懂，配置可以迁移到其他的电脑上。不求最强大，但求最简单实用。最后形成的配置文件放到github上保存。以下内容是在Ubuntu上完成。

### 1. 基本配置
在不安装任何插件的前提下，先把vim配置得漂亮一点。语法着色、行号这些都打开。
在个人主目录下，vim相关的文件和目录有：

```
.vim/                 .vimswap/
.vimbackup/           .vimundo/
.vim-fuf-data/        .vimviews/
.viminfo              .vimrc               
```
你需要关心的是.vim目录和.vimrc文件。其余的不管。
.vimrc在每次启动vim的时候执行，.vim目录是放vim插件的目录。

打开.vimrc文件（默认应该是空的），把下面的内容拷贝进去。双引号表示注释。
```
" 设置文字编码
set fenc=utf-8
set fencs=utf-8,gb18030,gbk,gb2312
" 打开行号
set number
" 关闭兼容老版本的vim，如果兼容老版本vim，则方向键不能使用，所以最好关闭
set nocompatible
" 语法着色打开
syntax on

" 打开自动缩进
set autoindent
set smartindent
set cindent
" 缩进宽度
set tabstop=4
set softtabstop=4
set shiftwidth=4
"建议开启expandtab选项，会自动将tab扩展很空格，代码缩进会更美观
set expandtab

" 输入括号引号等符号时显示配对的那一半
set showmatch
" 让输入的命令显示出来。
set showcmd
" 显示vim当前处于的模式
set showmode
" 增量搜索，就是搜索时不需要回车就开始进行查找
set incsearch

```
上面这些是最基本的配置，这样进行简单的代码编写就还凑合。
### 2. 变量和函数的跳转
这个功能在阅读代码时很需要，这个要依赖一个第三方工具来实现。工具叫ctags。
安装ctags：
```
 sudo apt-get install ctags 
```
建立一个测试小工程，目录如下所示。
```
teddy@teddy-ubuntu:~/test/vim-test$ tree
.
├── include
│   └── f1.h
├── main.o
├── Makefile
└── src
    └── f1.c
```
main.c内容：
```
#include "f1.h"

void main()
{
		func1();
}
```
f1.c内容：
```
#include "f1.h"
#include <stdio.h>


void func1()
{
		printf("func1 is called \n");
}
```
在当前目录下输入：
```
ctags -R *
```
则在当前目录下生成一个tags文件，然后你vim main.c 。光标定位到func1符号上，按Ctrl+]就可以挑战到func1函数上。再按Ctrl+t就又回来。
为了更好地在不同工程工程里查阅代码，可以往.vimrc里加入这两句。
```
" 最后这个分号不能少。有特殊意义。
set tags=tags;
set autochdir
```
这些就是ctags的简单使用。
ctags的局限性：***只能查看函数和变量的定义，不能看调用情况。***
如果要调用情况，就要请出下一位帮手，cscope。
cscope可以认为是ctags的增强版本，因为它可以比ctags做更多的事情。
安装方法：
```
sudo apt-get install cscope
```
cscope的学习先放着。
### 3. 符号列表
一个IDE肯定要可以把当前文件的符号列出来，vim怎么来实现这个功能呢？
好，我们到这里要开始给vim安装插件了。使用符号列表，需要安装taglist的插件。
下载链接在这里：http://vim-taglist.sourceforge.net/index.html 。
下载下来后，是一个zip包。解压开，里面有个一个plugin目录和docs目录，全部拷贝到.vim目录下。
taglist插件依赖ctags，ctags我们已经安装，且在测试工程里已经生成了tags文件了。
插件放好了，然后需要再.vimrc里加一些配置，才能正常工作。
```
let Tlist_Show_One_File=1
let Tlist_Exit_OnlyWindow=1
let Tlist_Ctags_Cmd="/usr/bin/ctags"
" 把打开关闭符号列表窗口的命令映射到F4快捷键上。这样使用比较方便。
nnoremap <silent><F4> :TlistToggle<CR>
```
关于vim按键的映射，另外再写文章详细说明。

![taglist使用情况](/images/taglist使用情况.jpg)

### 4. 多个文件的打开和切换
在写代码的时候，肯定会有同时编辑多个文件的需求，vim怎么同时打开多个文件呢？
有两种方法：
* 在启动vim的时候，`vim -p main.c src/f1.c` 。这样就可以把这2个文件同时打开。-p是将文件用标签显示出来。切到下一个文件的快捷键是ctrl+6。还可以用gt切到下一个标签页，gT切到上一个标签页。
* 在vim已经启动后，要另外打开新的文件。`:tabe include/f1.h`。这样就可以了。用tabe打开的文件也会显示一个标签。如果要新建一个文件，则是`tabnew test.c`这样。
  一般都是用多标签页来打开多个文件，但是如果想要对比看2个文件，则用2个窗口来打开2个文件比较好。
  `vim -o main.c src/f1.c` 这样就可以，用-o选项。
  在打开多个文件的时候，如果用`:q`来退出，则每次只能退出一个文件，`:qa`这样就可以退出所有文件了。
  如果要同时保存所有文件，用`:wall`来保存。
  当然还有一种需求是打开当前目录，去里面选择文件进行打开。输入`:Ex`。Ex是Explore是缩写，你也可以把命令写全了。
  `:ls`是看当前打开了哪些文件。
  所以打开多个文件，是不需要安装插件的，也不需要改.vimrc文件，只需要使用vim的参数即可实现。

### 5. 编辑环境的保存和恢复
你打开了很多的文件进行编辑，然后你关机了，你下次还是需要再次打开这些文件，如果再重新用命令一个个打开，那就太费劲了。vim可以把我们当前的vim的状态保存起来，以便下次再打开。
要恢复之前的编辑环境，你需要再退出的时候保存两种不同的信息，一种是会话信息，另外一种是viminfo信息。
* 会话信息里保存了所有窗口的视图，外加全区设置。
* viminfo保存了命令行历史等各种操作历史信息。
  保存会话的方法：
  `:mksession myproj` 就可以了。
  读取会话的方法：
  `vim -S myproj`这样就可以了。
  viminfo的暂时不管。

### 6. 自动补全
这个对于程序员来说太重要了，不然那么多的函数变量哪记得住。这个功能要用到插件。我们使用autocomplpop插件。
这个插件只能进行普通的单词补全，对于结构体成员这种还没法补全，那个需要另外一个插件。
下载地址：http://www.vim.org/scripts/script.PHP?script_id=1879 
解压开后，直接把内容拷贝到.vim目录下。
下载用vim打开一个c文件，进行编辑，就可以看到补全效果。
结构体成员变量的补全用OmniCppComplete这个插件。
下载地址：http://www.vim.org/scripts/script.php?script_id=1520
安装方法一样，解压后放到.vim目录下去。
不过这个还需要配置一下.vimrc文件。把下面的内容放到.vimrc里。
```
let OmniCpp_MayCompleteDot=1    "  打开  . 操作符
let OmniCpp_MayCompleteArrow=1  "打开 -> 操作符
let OmniCpp_MayCompleteScope=1  "打开 :: 操作符
let OmniCpp_NamespaceSearch=1   "打开命名空间
let OmniCpp_GlobalScopeSearch=1
let OmniCpp_DefaultNamespace=["std"]
let OmniCpp_ShowPrototypeInAbbr=1  "打开显示函数原型
let OmniCpp_SelectFirstItem = 2"自动弹出时自动跳至第一个
```
OmniCppComplete的补全需要依赖tags文件，对于printf这种系统函数呢，你可以提前生成一个tags文件。
命令如下：
```
ctags -I __THROW --file-scope=yes --langmap=c:+.h --languages=c,c++ --links=yes --c-kinds=+p --fields=+S  -R -f ~/.vim/systags /usr/include /usr/local/include
```
然后就放在.vim目录下，并且在.vimrc再加入下面这一句。
```
set tags+=~/.vim/systags
```
到了这一步，一个简单使用的C开发IDE就OK了。




