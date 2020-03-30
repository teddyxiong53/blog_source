---
title: Linux之coreutils
date: 2020-03-27 13:11:11
tags:
	- Linux

---

1

coreutils代表的是一个gnu操作系统上的基本的文件、shell和文本操作工具。

是所有gnu操作系统都必须有的基本工具。

可以在Linux上用`info coreutils`查看具体信息。

```
介绍
common options
整个文件的输出
	cat
	tac
	nl
	od
	base32
	base64
格式化文件内容
	fmt
	pr
	fold
部分文件输出
	head
	tail
	split
	csplit
	
计算文件校验
	wc
	sum
	cksum
	md5sum
	sha1sum
	sha2
排序文件
	sort
	shuf
	uniq
	comm
	ptx
	tsort
filed操作
	cut
	paste
	join
字符操作
	tr
	expand
	unexpand
目录查看
	ls
	dir
	vdir
	dircolors
基本操作
	cp 
	dd
	install
	mv
	rm
	shred
特殊文件类型
	mkdir
	rmdir
	unlink
	mkfifo
	mknod
	ln
	link
	readlink
改变文件属性
	chgrp
	chown
	chmod
	touch
磁盘使用
	df
	du
	stat
	sync
	truncate
打印文本
	echo
	printf
	yes
条件
	false
	true
	test
	expr
重定向
	tee
文件名操作
	dirname
	basename
	pathchk
	mktemp
	realpath
工作上下文
	pwd
	stty
	printenv
	tty
用户信息
	id
	logname
	whoami
	groups
	users
	who
	
系统上下文
	date
	arch
	nproc
	uname
	hostname
	hostid
	uptime
selinux上下文
	chcon
	runcon
修改命令调用
	chroot
	env
	nice
	nohup
	stdbuf
	timeout
进程控制
	kill
延迟
	sleep
数字操作
	factor
	numfmt
	seq
文件权限
日期输入格式
打开toolbox
```



公共选项

```
退出状态
	0表示成功，1表示失败。
备份选项
	有些gnu程序可以选择进行备份，例如cp、install、ln、mv这些操作。
	-b
	--backup[=METHOD]
	method可以有：none、off、existing、never、simple等。
	
block size
	有些gnu程序，例如df、du、ls。可以指定显示size，用block来做单位。
浮点数
	
信号
概念辨析
随机数
target目录
尾部的斜杠
遍历符号
对/特殊处理
标准一致性
multi-call调用

```



参考资料

1、官网

http://www.gnu.org/software/coreutils/