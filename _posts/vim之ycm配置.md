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



参考资料

1、

https://blog.csdn.net/liao20081228/article/details/80347889

2、解决“NoExtraConfDetected: No .ycm_extra_conf.py file detected”问题

https://blog.csdn.net/u014070086/article/details/88692896