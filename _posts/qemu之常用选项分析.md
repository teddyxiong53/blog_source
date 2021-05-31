---
title: qemu之常用选项分析
date: 2018-01-20 21:36:53
tags:
	- qemu

---



之前在Ubuntu12.04上安装qemu出现了很多的问题，很多东西也弄得不清楚。现在我安装了一个16.04的Ubuntu，重新把qemu再学习一遍。

# 安装

```
sudo apt-get install qemu
```

下载了大概240M的内容。

安装后，看是2.5.0的 。

# 常用选项

下面这些内容，都可以在man qemu-system-arm里看到。

## 一般选项

-M：板子的名字。可以用`qemu-system-arm -M ?`来查看支持的板子有哪些。

-fda file

-fdb file

-hda file

-hdb file

-hdc file

-hdd file ：这些都是指定硬盘和软盘对应的文件。

-cdrom file 

-boot [a、c、d]：指定从哪个盘启动。a表示软盘。c表示硬盘，d表示cd-rom。

-m xxx：指定内容多大。默认是128M的。

-smp n：指定多少个cpu。最多是255个。

-nographic：禁止图形输出，只有命令行界面。

## 网络选项

`-net nic[,vlan=n][,macaddr=addr]`

创建一个新的网卡，并和n号vlan（n从0开始）进行连接。

`-net user`

使用用户模式的网络堆栈，这样就不需要管理员权限来运行了。

`-net tap`

叫TAP网络接口。

一个组合的简单例子：

```
qemu linux.img -net nic -net tap
```

## Linux启动选项

-kernel xxx：指定内核镜像。

-append cmdline：指定cmdline

-initrd file：指定initrd。



# 实际总结

查看某个板子支持的网卡是什么。

```
teddy@teddy-ubuntu:~/work/txkj/cloud-lab/labs/linux-lab/qemu$ qemu-system-arm -net nic,model=help -M vexpress-a9
pulseaudio: set_sink_input_volume() failed
pulseaudio: Reason: Invalid argument
pulseaudio: set_sink_input_mute() failed
pulseaudio: Reason: Invalid argument
qemu: Supported NIC models: lan9118
```

