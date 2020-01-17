---
title: 《奔跑吧Linux内核》环境搭建
date: 2020-01-17 09:23:19
tags:
	- Linux
---

1

下载代码：

```
git clone https://github.com/figozhang/runninglinuxkernel_4.0
```

下载完，大概1.3G。

在我的笔记本上搭建，安装的是Ubuntu16.04 32位版本。

根据目录下面的《实验前必读- 重要说明_v1.3.pdf》说明，先到 `_install_arm32`目录下创建一个console节点。

```
cd _install_arm32； mkdir dev; cd dev; sudo mknode console c 5 1 
```

执行run_debian_arm32.sh脚本，提示没有工具链：

```
make: arm-linux-gnueabi-gcc：命令未找到
```

输入arm-linux-gnueabi-gcc，系统提示：

```
teddy@teddy-ThinkPad-SL410:~/work/runninglinux/runninglinuxkernel_4.0$ arm-linux-gnueabi-gcc
程序“arm-linux-gnueabi-gcc”尚未安装。 您可以使用以下命令安装：
sudo apt install gcc-arm-linux-gnueabi
```

安装工具链：

```
sudo apt install gcc-arm-linux-gnueabi
```

另外把binutils也安装一下。

```
sudo apt-get install binutils-arm-linux-gnueabi
```

再执行编译：

```
./run_debian_arm32.sh build_kernel
```

大概10分钟就可以编译好。

然后构造rootfs。

```
sudo ./run_debian_arm32.sh build_rootfs
```

运行一下，看看能不能跑起来：

```
./run_debian_arm32.sh run
```

开机大概花了1分钟。

是用systemd来启动的。apt-get工具都做进来了。算是一个非常完整的系统。

登录名是root，密码是123 。

内存和磁盘都是1G。



重新启动耗时还是很长。

看了一下rootfs_debian_arm32目录，不是基于busybox的，工具都单独的。这个是因为rootfs_debian_xx的就是基于debian的。

run.sh里的是基于busybox的。

如果不是debian的，需要自己手动进行make。

```
# 配置
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabi- vexpress_defconfig
# 编译
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabi- -j2
# 编译设备树
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabi- dtbs
# 运行
./run.sh arm32
```

这个得到的就是基于busybox的。

进入系统，可以看到把电脑的磁盘都挂载过来了。这样操作就很方便了。

```
/ # df -h
Filesystem                Size      Used Available Use% Mounted on
tmpfs                    42.7M         0     42.7M   0% /tmp
tmpfs                    42.7M         0     42.7M   0% /dev
kmod_mount               98.3G     43.7G     49.6G  47% /mnt
```



基于命令行来进行内核调试

需要2个shell窗口。都需要在代码目录下。

第一个shell窗口

```
./run.sh arm32 debug
```

第二个shell窗口。

```
arm-none-eabi-gdb -tui vmlinux
# 进入到gdb之后，执行下面的操作
target remote localhost:1234
b start_kernel
c # 必须用c，r在这种模式下不支持
```

然后就可以单步调试了。



安装eclipse调试环境

在shell里直接输入java，看到提示jdk版本。选择openjdk-8的进行安装。

```
sudo apt-get install openjdk-8-jre-headless
```

安装eclipse和eclipse-cdt

```
sudo apt-get install eclipse eclipse-cdt
```

安装arm版本的gdb

```
sudo apt install gdb-arm-none-eabi
```

这个需要消耗600M左右的空间。

我用apt-get安装的eclipse感觉版本太低了。

卸载掉。

```
sudo apt-get remove eclipse*
```

The last 32 bit release of Eclipse was 2018-09. 

从这里下载。

https://www.eclipse.org/downloads/download.php?file=/technology/epp/downloads/release/2018-09/R/eclipse-cpp-2018-09-linux-gtk.tar.gz

把eclipse解压放在这个目录下。

```
/home/teddy/tools/eclipse
```

加入到path里。

在32位的Ubuntu16.04里，eclipse运行有很多问题，都没法正常使用。

只能放弃在我的笔记本上用eclipse调试。



参考下面这篇文章来使用vscode来调试。

https://www.jameskozlowski.com/index.php/2016/06/18/arm-gdb-debugging-with-visual-studio-code/



尝试用vscode来调试。

新建调试配置如下，launch.json：

```
{
    // 使用 IntelliSense 了解相关属性。 
    // 悬停以查看现有属性的描述。
    // 欲了解更多信息，请访问: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [

        {
            "name": "Debug",
            "type": "gdb",
            "request": "attach",
            "executable": "${workspaceRoot}/vmlinux",
            "target": "localhost:1234",
            "remote":true,
            "cwd": "${workspaceRoot}",
            "valuesFormatting": "parseText"
        }
    ]
}
```

这样可以连接到对应的进程上，但是无法执行。

执行提示出错：

```
cannot execute this command while the selected thread is running .
```

上面并没有指定arm-none-eabi-gdb。怎么指定？

改成下面这样：

```
{
    // 使用 IntelliSense 了解相关属性。 
    // 悬停以查看现有属性的描述。
    // 欲了解更多信息，请访问: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [

        {
            "name": "Debug",
            "type": "gdb",
            "request": "attach",
            "executable": "${workspaceRoot}/vmlinux",
            "target": "localhost:1234",
            "remote": true,
            "cwd": "${workspaceRoot}",
            "valuesFormatting": "parseText",
            "gdbpath": "/usr/bin/arm-none-eabi-gdb",
            "autorun": [
                "b start_kernel",
                "c"
            ]
        }
    ]
}                                                  
```

这些配置有生效，但是还是没有达到预期效果。

知道了，把上面的autorun里的"c"去掉就好了。

可以正常调试了。

但是变量的内部结构无法体现处理，结构体部分看到里面的值。

可以右键选择添加到watch里查看。

看看能不能更新vscode得到改善，发现新版本都不支持32位系统了。





参考资料

1、ubuntu下安装eclipse IDE for C/C++ developers

https://www.cnblogs.com/amanlikethis/p/3401370.html