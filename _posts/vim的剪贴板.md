---
title: vim的剪贴板
date: 2016-10-23 16:55:34
tags:
	- vim
---
vim的剪贴板是个有点复杂的东西。按照大家在windows下的使用经验，系统剪贴板只有一个，你再次复制，你上次复制的东西就不见了。但是vim的剪贴板跟我们的这个经验不符，vim里有多个剪贴板。
剪贴板在vim另外有个名字，叫做寄存器（register）。在vim里输入`:reg`就可以查看当前的寄存器的情况。例如我的vim当前是这样的：
```
:reg
--- 寄存器 ---
""   ^J
"0   ^J
"1   ^Ild main.o src/f1.o -o main^J
"2   false^J
"3   false^J
"4   false^J
"5   false^J
"6   deb http://mirrors.hust.edu.cn/ubuntu/ wily main restricted universe multiverse^Jdeb http://mirrors.hust.edu.cn/ubuntu/ wily-security main
"7   # deb cdrom:[Ubuntu 15.10 _Wily Werewolf_ - Release i386 (20151021)]/ wily main restricted^J^J# See http://help.ubuntu.com/community/Upgrad
"8    See ttp://help.ubuntu.com/community/UpgradeNotes for how to upgrade to^J# newer versions of the distribution.^Jdeb http://cn.archive.ubunt
"9   h^J^J#
"-   false
"%   Makefile
"/   ass
```
最好使用小写字母来做寄存器的名字，因为有些大写字母的寄存器被vim系统占用了。
要使用寄存器之前，先要按一个`"`。例如复制当前行到寄存器k里面，应该这样按`"kyy`。
你要把寄存器k里面的内容粘贴的话，就这样按`"kp`。


