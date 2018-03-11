---
title: Linux之insmod分析
date: 2018-03-11 15:25:05
tags:
	- Linux

---



现在从busybox里的insmod命令的实现入手，看看insmod的过程中发生了什么。

linux2.6版本相比于之前的2.4版本，发生了很多的革命性的改变，linux2.6持续了8年的更新。

在module这一块，也有分水岭式的改变。

所以在busybox代码里，我们可以看到这种代码：

```
#if ENABLE_FEATURE_2_4_MODULES
```

这个指的就是linux2.4版本的风格的意思。不过我们都关掉的。

```
lsmod_main
	1、argv[1]就是文件名。拿到。
	2、bb_init_module(filename)
		try_to_mmap_module：使用mmap来做。可以配置关闭。我看默认的关闭的，不分析先。
		xmalloc_open_zipped_read_close，不mmap，就用这个。
			就是分配了一块内存，把module的内容读取放到内存上。
		init_module
			syscall(__NR_init_module, mod, len, opts)
```

然后就是进入到kernel里了。

```
init_modulue
	copy_module_from_user
	load_module
		module_sig_check
		elf_header_check
		layout_and_allocate
		
```



# 参考文章

1、insmod过程详解

http://blog.csdn.net/chrovery/article/details/51088425

