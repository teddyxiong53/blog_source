---
title: Linux之inode分析
date: 2017-05-25 22:44:06
tags:

	- Linux

	- inode

---

要理解inode，就要先从文件存储说起。硬盘上读写的最小单位是512字节，叫做一个扇区。而一般在操作硬盘的时候，还不是以扇区为单位的，因为还是小了点，会导致操作比较繁琐，所以把单位继续扩大，一般以4K字节作为处理单位，叫做一个块。也就是8个扇区组成一个块。

文件的实际数据内容就存放在块里。那么文件的元信息放哪呢？就是文件的创建时间、修改时间这些，我们得找个地方放才行啊。好，就是我们要讲的inode。一般翻译为索引节点。

我们可以用stat来查看一个文件的inode信息，如下：

```
teddy@teddy-ubuntu:~/test/c-test$ stat Makefile 
  文件："Makefile"
  大小：240             块：8          IO 块：4096   普通文件
设备：801h/2049d        Inode：792664      硬链接：1
权限：(0744/-rwxr--r--)  Uid：( 1000/   teddy)   Gid：( 1000/   teddy)
最近访问：2017-05-18 23:38:53.929345140 +0800
最近更改：2017-05-18 23:38:49.890330782 +0800
最近改动：2017-05-18 23:38:49.885345117 +0800
创建时间：-
```

这么说，文件除了文件名之外的信息，都存在inode里。

归根结底，inode也是存在硬盘上。在格式化硬盘的时候，os会自动把硬盘分为两个区域，一个是数据区，存放文件数据，一个是inode区，存放inode。

一个inode一般是128字节或者256字节。一个硬盘能够有多少个inode，在格式化的时候就确定了。一般是每1KB或者2KB的空间，就给分配一个inode。

假如有一块硬盘，大小是1GB，一个inode大小是128字节，每1KB给一个inode，那么inode区域要占用128MB。

可以用命令`df -i`来查看系统的inode总数和已经使用的数量。

如果系统里的小文件很多，那么很可能出现磁盘还没有满，但是已经无法创建文件的情况，因为inode被耗尽了。

每个inode都一个号码，os就是用inode号码来识别不同的文件。

Linux里是使用inode号码而不是文件名来识别文件。

用户打开一个文件，在Linux内部的处理过程是这样的：

1. 系统找到这个文件名对应的inode号码。
2. 通过inode号码，获取inode信息。
3. 根据inode信息，找到文件数据所在的block，读取数据。

可以用`ls -i 1.txt`这样来得到文件的inode号码。



基于inode这个点，可以衍生出两个概念：硬链接和软链接。

一般情况下，文件名和inode是一一对应的。但是Linux允许多个文件名指向同一个inode。

```
teddy@teddy-ubuntu:~/test/tmp$ touch 1.txt
teddy@teddy-ubuntu:~/test/tmp$ ls
1.txt
teddy@teddy-ubuntu:~/test/tmp$ ls -i 1.txt 
802317 1.txt
teddy@teddy-ubuntu:~/test/tmp$ ln 1.txt 1_1.txt
teddy@teddy-ubuntu:~/test/tmp$ ls -i
802317 1_1.txt  802317 1.txt
teddy@teddy-ubuntu:~/test/tmp$ ln -s 1.txt 1_2.txt 
teddy@teddy-ubuntu:~/test/tmp$ ls -i
802317 1_1.txt  802410 1_2.txt  802317 1.txt
teddy@teddy-ubuntu:~/test/tmp$ 
```



因为Linux下的inode和文件名分离，这个机制导致了一些特别的现象：

1. 有时候，文件名包含了特殊字符，导致无法正常删除，可以通过删除inode节点来间接删除文件。
2. 给文件改名，inode还是保持不变。



