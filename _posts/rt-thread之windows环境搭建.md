---
title: rt-thread之windows环境搭建
date: 2020-10-28 13:12:30
tags:
	- rt-thread
---

1

下载rt-thread源代码。

下载env工具。解压放好。

下载tap网卡。tap安装后，会产生这样一个网卡。

![image-20201028131737299](../images/random_name/image-20201028131737299.png)

选中，按F2，选择给这个网卡重命名为qemu。

然后把有线网卡，右键选择共享，选中共享给qemu网卡。

把下面这个目录添加到PATH环境变量。

D:\work\rt-thread-study\env\tools\qemu\qemu32

双击打开env.exe文件。

![image-20201028134253251](../images/random_name/image-20201028134253251.png)

会弹出命令行界面。

在命令行界面，切换到bsp/qemu-vexpress-a9目录下，执行scons进行编译。

在命令行解码，执行qemu。就可以运行。

默认sd.bin没有被格式化的。

在rt-thread里，执行格式化：

```
mkfs sd0
```

然后关闭当前命令行窗口。

然后再启动。SD卡就可以正常使用了。

现在网卡还没有正常工作。

打开qemu.bat文件。

在qemu命令的最后面加上：

```
-net nic -net tap,ifname=qemu
```

重新启动qemu。

板端得到的ip地址如下。电脑上的qemu网卡是192.168.137.1 

![image-20201028135019719](../images/random_name/image-20201028135019719.png)

现在板端可以ping通www.baidu.com

网络正常。

然后我们添加新的package。

改了online package配置后，需要执行：`pkgs --update`。才会执行下载代码到本地的操作。

scons --menuconfig没有。

scons --pyconfig。这个有。这个是图形界面的。不过内容差不多。

可以直接有个命令，menuconfig来进行配置。



我比较好奇，他们这套工具是怎样搭建起来的？

 

# 使用vscode来调试

在上面的基础上继续。

生成一些配置信息。这样会生成vscode的json配置文件。把rt-thread的头文件路径配置好。

```
scons --target=vsc -s
```

启动vscdoe。必须在env的命令行界面里执行`code .`这样才能在启动后在vscode的终端里使用scons命令。

在vscode里启动rt-thread。

```
.\qemu.bat
```

单步调试。

打开qemu-dbg.bat文件。

在qemu-system-arm前面加上start。

但是我设置断点不能调试。

# 抓包

现在有qemu网卡。抓包就很容易了。

# telnet

可以打开Telnet服务端。远程过去操作。

# GUI

![img](../images/random_name/1443823-20180720160043491-2047179579.png)

配置后要记得pkgs --update。

不然编译会报错。

然后正常编译运行。可以看到示例的界面。

gui的代码：

https://github.com/RT-Thread-packages/gui_engine



参考资料

1、使用 QEMU 运行 RT-Thread

https://www.rt-thread.org/document/site/tutorial/qemu-network/qemu_setup/qemu_setup/

2、教程ppt

https://www.rt-thread.org/document/site/tutorial/qemu-network/qemu_setup/qemu_setup.pdf

3、使用vscode调试

https://www.rt-thread.org/document/site/tutorial/qemu-network/qemu_vscode/qemu_vscode.pdf

4、运行gui

https://www.cnblogs.com/shirleyxu/p/9342071.html

