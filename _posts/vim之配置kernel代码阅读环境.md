---
title: vim之配置kernel代码阅读环境
date: 2020-01-07 13:23:08
tags:
	- vim

---

1

只安装需要的插件，尽量少。

界面也简单点。就3部分：文件、主体、符号。

只用来读代码，不写。

需要的功能：

```
符合列表
	就是本文件的函数、变量。
	taglist插件。
	这个是基于ctags的。所以需要先安装ctags才能用。
文件列表
	NERDTree插件。
多个窗口
	winmanager插件。
最近打开的文件列表
	MiniBufExplorer插件。
括号匹配跳转
	surround插件。
```

配套工具

```
ctags
	生成符号。，跳转需要依赖这个。
	安装：
	sudo apt-get install ctags 
	在kernel目录下，执行ctags -R。生成所有的符号。
cscope
	sudo apt-get install cscope 
	这个是生成索引。
	cscope-indexer -r
	ctags和cscope一起安装，使用起来会更加方便。
```

把索引文件导入到vim中。



插件安装，我使用vim-plug，这个因为是mini的，简单。

但是对应的下载地址被墙了。

还是用vundle吧。vundle也是要raw.githubusercontent.com的东西。

我想办法弄了个梯子。

继续用vim.plug来做。

下载plug.vim文件。

```
curl -fLo ~/.vim/autoload/plug.vim --create-dirs \
    https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
```

使用vim-plug安装vim插件的方式，跟vundle非常类似。

都是在~/.vimrc里。增加以`call plug#begin(PLUGIN_DIRECTORY)`开始，以`plug#end()`结尾的配置段。

下面是一个典型的配置。

```
call plug#begin('~/.vim/plugged')
Plug 'junegunn/vim-easy-align'
Plug 'junegunn/vim-github-dashboard'
Plug 'SirVer/ultisnips' | Plug 'honza/vim-snippets'
Plug 'scrooloose/nerdtree', {'on': 'NERDTreeToggle'}
Plug 'tpope/vim-fireplace', {'for': 'clojure'}
Plug 'rdnetto/YCM-Generator', {'branch' :'stable'}
Plug 'nsf/gocode', {'tag': 'v.20150303', 'rtp': 'vim'}
Plug 'junegunn/fzf', {'dir': '`/.fzf', 'do': './install --all'}
Plug '~/my-prototype-plugin' 
call plug#end()
```

下面的是解释：

```
Plug 'junegunn/vim-easy-align'
	这个是以简写的方式提供的github地址，完整的是：
	(https://github.com/junegunn/vim-easy-align
Plug 'SirVer/ultisnips' | Plug 'honza/vim-snippets'
	这个是靠管道符号把2个插件写在一行。
Plug 'scrooloose/nerdtree', {'on': 'NERDTreeToggle'}
	这个按需加载。在NERDTreeToggle命令被调用的时候，加载插件。
Plug 'tpope/vim-fireplace', {'for': 'clojure'}
	这个是编辑clojure类型的文件时才加载。
Plug 'rdnetto/YCM-Generator', {'branch' :'stable'}
	指定使用这个插件的stable分支。
Plug 'nsf/gocode', {'tag': 'v.20150303', 'rtp': 'vim'}
	指定使用某个tag。rtp描述了vim插件的子目录。
Plug 'junegunn/fzf', {'dir': '`/.fzf', 'do': './install --all'}
	dir指定了这个插件单独存放的目录。do选项相当于post操作。
Plug '~/my-prototype-plugin' 
	本地不用github托管的vim插件。
```

写好了配置文件。然后怎么安装呢？

在vim的命令行模式下，输入：

```
:PlugInstall [xx yy]
```

后面不带名字，是安装所有，带上名字，就是安装名字指定的插件。

```
:PlugStatus 
	查看当前插件的状态。
:PlugUpgrade
	更新插件。
```



我安装的插件：

```
call plug#begin('~/.vim/plugged')
Plug 'wesleyche/SrcExpl'
call plug#end()
```

我先只安装SrcExpl这个插件。这个是一个居住在芝加哥的华人写的。

先只安装这一个。

安装后，再打开vim，没有什么变化。

这个插件的作用是：

```
显示声明和定义，ctags支持的语言
可以用鼠标和按键来进行跳转。
自动创建和更新tag文件。
```

设置举例

```
" 下面表示F8的作用映射为SrcExplToggle加回车。
nmap <F8> : SrcExplToggle<CR>

let g:SrcExpl_winHeight=8
let g:SrcExpl_refreshTime=100
let g:SrcExpl_jumpKey = "<ENTER>"
let g:SrcExpl_gobackKey = "<SPACE>"

let g:SrcExpl_pluginList = [
	\ "__Tag_List__",
	\ "_NERD_tree_",
	\ "Source_Explorer"
\ ]

```

发现什么只用SrcExpl是不够的，它依赖了其他的插件。

```
call plug#begin('~/.vim/plugged')
Plug 'preservim/nerdtree'
Plug 'vim-scripts/taglist.vim'
Plug 'wesleyche/SrcExpl'
call plug#end()
```

现在都安装好了。用xxToggle，都分别打开对应的窗口。

但是快捷键不行。那就是按键映射没有起作用。

在图形界面下是可以的。我在securecrt远程的不可以。

查看配置文件也能知道，ctrl+JKIL，分别是向左、下、上、右切换窗口。如果希望修改按键，可以再修改 vimrc 中的配置。（这个配置方式就类似wasd这样来做方向键一样的逻辑）。

Enter进入，空格返回。

当前我的配置文件是这样：

```
set nocompatible

call plug#begin('~/.vim/plugged')
Plug 'preservim/nerdtree'
Plug 'vim-scripts/taglist.vim'
Plug 'wesleyche/SrcExpl'
call plug#end()

" ================= 基本配置======================
" 设置文字编码
set fenc=utf-8
set fencs=utf-8,gb18030,gbk,gb2312
" 打开行号
set number
" 关闭兼容老版本的vim，如果兼容老版本vim，则方向键不能使用，所以最好关闭

" 语法着色打开
syntax on
syntax enable

" 打开自动缩进
set autoindent
set smartindent

" c indent ,对C语言编程
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
" 搜索高亮
set hlsearch



" ================= ctags配置======================
" 最后这个分号不能少。有特殊意义。
set tags=tags;
set autochdir
" ================= cscope配置======================
set csto=0
set cst

" ================= taglist配置======================
filetype on
nmap <F7> :TlistToggle<CR>
let Tlist_Ctags_Cmd="/usr/bin/ctags"
let Tlist_Inc_Winwidth=0
let Tlist_Exit_OnlyWindow=0
let Tlist_Auto_Open = 1
let Tlist_Use_Right_Window = 1

" ================= SrcExpl 配置======================
nmap <F8> :SrcExplToggle<CR>
nmap <C-J> <C-W>h
nmap <C-K> <C-W>j
nmap <C-I> <C-W>k
nmap <C-L> <C-W>l

let g:SrcExpl_winHeight = 8
let g:SrcExpl_refreshTime = 100 "ms
let g:SrcExpl_jumpKey = "<ENTER>"
let g:SrcExpl_gobackKey = "<SPACE>"
let g:SrcExpl_isUpdateTags = 0

" ================= nerdtree 配置======================
let NERDTreeWinPos = "left"
nmap <F9> :NERDTreeToggle<CR>

```





当前securecrt的语法着色显示不出来。

需要选iterm，而不是之前的vt100的。这样就可以有颜色了。

现在环境好了。看代码还可以。



还差一点，保存当前的环境。

关闭vim后，再次打开，希望可以恢复之前的环境，这样就可以接着看，不至于让思路断掉。



## vim显示空格和tab

网上复制的代码，有时候空格有问题。

所以希望可以明确看出空格和tab。这样才能避免问题。

最简单的方法是：

```
:set list
```

这个是会显示$和^的。看起来不好看。

可以这样：

```
:set listchars=tab:>-,trail:-
```

这个的效果是用`-`来显示空格和tab。也不是很好。

在vimrc最后加上这几行。

```
highlight ExtraWhitespace ctermbg=red guibg=darkgreen
autocmd ColorScheme * highlight ExtraWhitespace ctermbg=red guibg=red
match ExtraWhitespace /\s\+$\| \+\ze\t/
```

在输入时，会用色块先显示。但是在输入完成后，色块就消失了。

这个可以很简单显示所有的空白字符。

```
:set syntax=whitespace
```

找到一个最佳实践。

只需要下面这两行就够了。

```
:set listchars=eol:¬,tab:>·,trail:~,extends:>,precedes:<,space:␣
:set list
```

整理一下。把这个整理成一个快捷键。

用leader键，然后加上s来表示吧。

不用，直接把上面一行写入到vimrc里。set list这个直接输入吧。反正不多。



需要一个比较好的机制来同步我的vimrc文件。

# 参考奔跑吧Linux内核的配置

这个是专门配置用来分析内核的，所以很符合我的需求。

这个还是同时使用了ctags和cscope。

tag插件是用tagbar。这个是跟taglist类似的。

关键是内核为我们做好了生成这些的准备。需要先输入环境变量。

```
export ARCH=arm
export SUBARCH=arm
export CROSS_COMPILE=arm-linux-gnueabihf-
make vexpress_defconfig
make tags cscope TAGS
```





参考资料

1、Vim轻量高效插件管理神器vim-plug介绍-Vim插件(9)

https://vimjc.com/vim-plug.html

2、linux学习9，配置vim，NERD_tree，Source Explorer, Tag List 插件的使用

主要参考这篇做的。

https://blog.popkx.com/linux-learning-9-configuring-vim-nerd_tree-source-explorer-tag-list-plug-in-usage/

3、所需即所获：像 IDE 一样使用 vim

https://www.bookstack.cn/read/use_vim_as_ide/README.md