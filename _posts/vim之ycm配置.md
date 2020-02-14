---
title: vim之ycm配置
date: 2020-01-10 10:03:08
tags:
	- vim

---

1

ycm是比较复杂的插件。所以专门写一篇文章来梳理。

我已经通过vim.plug安装好了这个插件。因为要github下载不少的东西，所以用梯子下载是比较合适的，不然太慢了。

目前我什么都没有配置，打开一个C代码，输入，可以看到有提示补全，但是系统的头文件里的结构体的成员还不能提示，所以就还需要进行配置。

在.vimrc里加上这两行：

```
let g:ycm_global_ycm_extra_conf='~/.ycm_extra_conf.py'
let g:ycm_comfirm_extra_conf=0
```

新建~/.ycm_extra_conf.py，内容如下：

```
import os
import ycm_core

flags = [
         '-Wall',
         '-Wextra',
         '-Werror',
         '-Wno-long-long',
         '-Wno-variadic-macros',
         '-fexceptions',
         '-DNDEBUG',
         '-std=c++11',
         '-x',
         'c++',
         '-I',
         '/usr/include',
         '-isystem',
         '/usr/lib/gcc/x86_64-linux-gnu/5/include',
         '-isystem',
         '/usr/include/x86_64-linux-gnu',
         '-isystem'
         '/usr/include/c++/5',
         '-isystem',
         '/usr/include/c++/5/bits'
         ]

SOURCE_EXTENSIONS = [ '.cpp', '.cxx', '.cc', '.c', ]

def FlagsForFile( filename, **kwargs ):
     return {
              'flags': flags,
              'do_cache': True
              }

```

现在打开c文件，就可以看到系统头文件的补全效果了。

但是对于复杂工程，里面自己有很多的层次的头文件。ycm总是提示找不到对应的头文件。

网上有答案说是在ycm的py配置文件里加上：

```
'-isystem', '/yourdir'
```

我加了这个，还是一样的 ，提示找不到。

搜索头文件的顺序是：`-I`指定目录、`-isystem`指定目录、标准系统目录。

-isystem是gcc的参数。

YCM配置文件的查找顺序是当前目录>上层目录>...>根目录>YCM全局目录。



现在要面对的就是多种插件的相互融合的问题。

例如代码跳转，目前有的插件有：

```
SrcExpl
	enter进入，空格返回。
vim本身
	gf：进入头文件。
	ctrl+6 文件返回。
	ctrl+] 跳转 ctags应该就是这个了吧。
	ctrl +t返回。
ycm
	
```

目前我的ycm配置还只有4行。

```
" ================= ycm 配置======================
let g:ycm_global_ycm_extra_conf='~/.ycm_extra_conf.py'
let g:ycm_comfirm_extra_conf=0
" 修改tab补全，我要把tab键让给UltiSnips用。
let g:ycm_key_list_select_completion = ['<c-n>', '<Down>']
let g:ycm_key_list_previous_completion = ['<c-p>', '<Up>']
```

这个还必须靠工具才能完成这个头文件目录的添加工作。

https://github.com/rdnetto/YCM-Generator

用来根据你的项目build系统，生成一个合适的ycm_extrap_conf.py文件。

ycm-generator的安装方法，它也是一个插件。

把下面的内容添加到vimrc里。

```
Plug 'rdnetto/YCM-Generator', { 'branch': 'stable'}
```

好像也不太好用。



头文件找不到的文件，只需要把内核代码的include指定到ycm_extra_conf.py里。

跳转我定义到ctrl+h上。

返回是ctrl+6 。这个是vim本身的，本质是最近的2个文件之间切换。



跳转头文件，可以用我映射的ctrl+h这个跳转到定义的按键。但是这个的返回就不能用ctrl+t了。用ctrl+6的话，如果进了多个头文件，就没法正常返回了。用ctrl+o是可以的。



跳转到函数定义，可以用ctrl+]。



我现在用这个来进行内核驱动的编写。发现有不少的问题。

有些符号解析出错，导致后面的无法正常补全。

头文件还继续添加一些到ycm_extra_conf.py。

估计还需要配置一下ycm。





这个时候, YCM终于可以用了. 写了一个test.cpp, 简单试了下, 不管是补全和跳转, 都很给力, 完全符合自己的预期. 另外YCM还有语法检查的功能, 但是我觉得错误标记太丑, 就给关了(let g:ycm_enable_diagnostic_signs = 0). 



通过YcmDebugInfo查看信息。

还以YcmDiags这样看文件在哪里。

当前我有把include的路径填错的问题。



默认是用 CTRL+SPACE 来触发补全的，中文操作系统下，CTRL+SPACE被系统劫持用作输入法切换，无法正确传到终端，所以一般要改成 CTRL+Z：

看了这么多，还是觉得有必要看一下官方的资料。



我只的ycm_extra_conf.py里写的是c++的，需要修改一下，改成C语言的。



现在跳转头文件，跳到了mips的分支里去了。这个怎么处理呢？



VIM底部显示当前编辑文件绝对路径

https://blog.csdn.net/emdfans/article/details/49308529



自动补全匹配括号引号。

切换文件的时候，总是提示当前文件没有保存，需要切换文件的时候自动保存。

```
set autowriteall
```



ycm中文文档

https://blog.csdn.net/liao20081228/article/details/80347889



ctags

```
ctags [options] [file(s)]
```

选项有：

```

```



参考资料

1、

https://blog.csdn.net/liao20081228/article/details/80347889

2、解决“NoExtraConfDetected: No .ycm_extra_conf.py file detected”问题

https://blog.csdn.net/u014070086/article/details/88692896

3、为YCM配置ycm_extra_conf.py脚本

https://www.jianshu.com/p/5aaae8f036c1



https://www.cnblogs.com/yinghao1991/p/6517071.html

https://ops.tips/gists/navigating-the-linux-kernel-source-with-youcompleteme/

[原创][YCM] YouCompleteMe安装完全指南

这篇文章讲了解决问题的方法。

https://www.cnblogs.com/HGtz2222/p/5175151.html