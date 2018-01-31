---
title: archlinux（一）
date: 2018-01-31 18:44:16
tags:
	- archlinux

---



# 安装

arch的安装让人一上来就一头雾水。真不知道设计者是怎么想的。

正常的过程不应该是一个脚本，用户按照提示一步步走吗。官网上那么多的步骤是咋回事。

如果说这个设置为了阻止小白用户使用这个系统，那么设计者做得很成功。

吐槽归吐槽。开始动手吧。

我是在VMware里安装，应该没什么问题。

1、插入iso文件，启动后，进入到booting arch后的界面。你会看到一个install.txt文件。懒得看，上网看排版更好。

2、然后是要检查你的引导方式，默认应该都是mbr+bios的。不用做什么。

3、保证是联网的。ok。

4、分区。用fdisk，我的硬盘没有分区，建立一个主分区就好了。

5、格式化分区：`mkfs.ext4 /dev/sda1`

6、把sda1挂载到/mnt/boot目录上。

7、配置镜像源。文件是/etc/pacman.d/mirrorlist。

用清华和浙大的源。

```
Server = http://mirrors.tuna.tsinghua.edu.cn/archlinux/$repo/os/$arch
Server = http://mirrors.zju.edu.cn/archlinux/$repo/os/$arch
```

8、安装基本包。

```
pacstrap /mnt/boot base base-devel
```

然后就会联网下载内容。

从提示看，还要下载200多M的内容。为啥不放在安装盘里呢？那安装盘里500多M都是什么内容？









