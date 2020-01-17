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



参考资料

1、

https://blog.csdn.net/liao20081228/article/details/80347889

2、解决“NoExtraConfDetected: No .ycm_extra_conf.py file detected”问题

https://blog.csdn.net/u014070086/article/details/88692896

3、为YCM配置ycm_extra_conf.py脚本

https://www.jianshu.com/p/5aaae8f036c1