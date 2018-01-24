---
title: Linux之cloud-lab使用
date: 2018-01-19 21:20:28
tags:
	- Linux
	- tinylab

---



泰晓科技有个cloud-lab，是基于docker搭建的一个linux内核实验环境。感觉很强大。我要把这个环境掌握起来。

先按照http://tinylab.org网站上的教程，把linux-lab的环境搭建好。就是下载过程比较耗时间，我大概是花了2个多小时才下载完成。不过你可以先做点别的事情。

运行效果是回启动浏览器，里面可以启动命令行终端。感觉很强大。所以我现在把这个命令的执行流程梳理一遍。

这套脚本写得也比较复杂强大，可以作为脚本的学习材料。

先从tools/docker目录下的脚本开始看。

从choose这个脚本看起。

# choose脚本

1、可以带一个参数，也可以不带。不带的话，脚本会列出来给你选择。参数是lab的名字。例如linux-lab这种。

2、所有脚本都依赖一个TOP_DIR目录，就是cloud-lab目录这一层。

3、调用config脚本。

4、当前的LAB名字是保存在labs/.current_lab文件里。

5、打印的选择是通过configs目录下的子目录罗列得到的。

6、输入选择对应的lab。

7、调用download_submodule进行下载。

进入到labs/rtthread-lab目录，执行git checkout master。

git submodule update 

git pull



# config脚本

1、先得到user，希望不要是root用户。

2、发现没有安装docker，就进行安装。

3、定义了很多的目录变量。定义了很多的工具函数。

4、那个登陆的网页内容写在这里。

# run脚本



# 看rtthread-lab的运行

以这个作为分析的切入点。因为这个内容相对比较少，容易分析。

1、运行。

```
./tools/docker/run rtthread-lab
```

运行后会自动打开浏览器。并且登陆到一个Ubuntu系统。这个Ubuntu是在一个docker里运行的。

登陆进去后，是在/labs/rtthread-lab目录下。这里有rt-thread目录、Makefile、README.md。

可以根据README.md的内容进行操作。

2、编译并运行。

```
make config #会打开一个menuconfig界面。
make build #进行编译
make boot #会在qemu里运行rt-thread。
```

分析一下qemu虚拟的板子的情况。

虚拟机里的/labs目录跟cloud-lab/labs目录下的内容一样。

看Makefile里的东西。

1、板子名字是vexpress-a9.

2、BSP名字是qemu-vexpress-a9

3、NET_DEV的名字是lan9118 

4、对应的bs目录是rt-thread/bsp/qemu-vexpress-a9目录。

5、运行命令的：

```
qemu-system-arm -M $(BOARD) -net nic,model=$(NET_DEV) -net tap -kernel $(BSP_DIR)/rt-thread.elf
```

#系统分析

看看我系统里当前的docker镜像情况：

```
y-ubuntu:~/work/txkj/cloud-lab/tools/docker$ docker images
REPOSITORY                 TAG                 IMAGE ID            CREATED             SIZE
mysql                      latest              f008d8ff927d        4 days ago          409 MB
nginx                      latest              3f8a4339aadd        3 weeks ago         108 MB
debian                     jessie              2fe79f06fa6d        5 weeks ago         123 MB
tinylab/rtthread-lab       latest              368c82e9e776        6 weeks ago         1.96 GB
tinylab/linux-lab          latest              aa7f721a29af        8 weeks ago         3.6 GB
tinylab/cloud-ubuntu-web   latest              0b8b06cb2338        2 months ago        555 MB
ubuntu                     latest              7b9b13f7b9c0        7 months ago        118 MB
hello-world                latest              48b5124b2768        12 months ago       1.84 kB
training/webapp            latest              6fae60ef3446        2 years ago         349 MB

```

`tinylab/cloud-ubuntu-web`这个是什么情况呢？

看来泰晓科技做了不少的docker镜像。

```
teddy@teddy-ubuntu:~/work/txkj/cloud-lab$ docker search tinylab
NAME                                               DESCRIPTION                                     STARS     OFFICIAL   AUTOMATED
tinylab/linux-lab                                  Qemu Based Linux Kernel Development Lab         2                    
tinylab/linux-0.11-lab                             Qemu/Bochs Based Linux 0.11 Development Lab     2                    
tinylab/cloud-ubuntu-vm                            Ubuntu with Qemu and Bochs                      1                    
tinylab/cloud-ubuntu-web                           Ubuntu with web clients for telnet/ssh/VNC      1                    
tinylab/markdown-lab                               Markdown for slides,resume,books,articles       1                    
tinylab/cs630-qemu-lab                             Qemu Based Assembly Learning Lab for CS630      1                    
tinylab/tinylab.org                                Jekyll website lab for http://tinylab.org       0                    
tinylab/cloud-ubuntu                               Ubuntu with LXDE,x11vnc,ssh and fail2ban        0                    
tinylab/cloud-ubuntu-proxy_client_transparent      Transparent proxy client                        0                    
tinylab/cloud-ubuntu-markdown                      Ubuntu with markdown support                    0                    
tinylab/qing-lab                                   Ubuntu for computer courses learning            0                    
tinylab/cloud-ubuntu-cn                            Ubuntu with Chinese display support             0                    
tinylab/cloud-ubuntu-vm_embedded                   Ubuntu with qemu,bochs,gcc,gdb,tftp,nfs...      0                    
tinylab/cloud-ubuntu-dev_cn_input                  Ubuntu dev lab with Chinese input support       0                    
tinylab/cloud-ubuntu-proxy_client                  Proxy Client                                    0                    
tinylab/cloud-ubuntu-vm_embedded_markdown                                                          0                    
tinylab/cloud-ubuntu-dev_cn                        Ubuntu with Chinese display support             0                    
tinylab/cloud-ubuntu-cn_input                      Ubuntu with Chinese input support               0                    
tinylab/cloud-ubuntu-dev                           Ubuntu with development support                 0                    
tinylab/cloud-ubuntu-proxy_server                  Proxy Server                                    0                    
tinylab/cloud-ubuntu-vm_embedded_markdown_jekyll                                                   0                    
tinylab/cloud-ubuntu-tproxy_client                 Ubuntu client with transparent proxy confi...   0                    
tinylab/cloud-ubuntu-jekyll                        Ubuntu with Jekyll website environment          0                    
tinylab/cloud-ubuntu-reverse_proxy                 Reverse Proxy                                   0                    
tinylab/cloud-ubuntu-proxy_relay                   Proxy relay,bridge of another proxy server      0 
```

这些内容，也可以在dockerhub网站上找到：

https://hub.docker.com/search/?isAutomated=0&isOfficial=0&page=1&pullCount=0&q=tinylab&starCount=0

cloud-ubuntu-web的在这里：

https://hub.docker.com/r/tinylab/cloud-ubuntu-web/

看描述信息里写的是：带有web client的Ubuntu，用来通过telnet、ssh、vnc来进行登陆。

这个Ubuntu内部集成了gateone和novnc。

gateone是一个web-based ssh。后台部分是用Python实现的。前端是用js和websockets。

安装过程：

```
1、依赖Python和tornado。
2、安装pip
$ wget  --no-check-certificate https://bootstrap.pypa.io/get-pip.py
$ sudo python get-pip.py
3、安装tornado
sudo pip install tornado

```

http://tinylab.org/how-to-deploy-cloud-labs/

这篇文章有对cloud-lab的架构层次进行分析。

云实验环境，目前形成了三个层次的抽象：

1、cloud Ubuntu。

2、cloud lab

3、labs

## cloud Ubuntu

cloud Ubuntu不仅实现了一系列的基础镜像。而且提供了进一步快速扩展其他镜像的框架。

到目前，cloud Ubuntu实现了13个基础镜像。

1、最基础的是cloud-ubuntu。提供了基础的ssh和vnc服务。

2、cloud-ubuntu-web。这个提供了gateone和novnc。

# linux-lab使用

## 目录分析

boards：放着vexpress-a9等板子的内核config配置文件。还有一个Makefile，里面也是配置项。

buildroot：

prebuilt：这里放了编译好的镜像。直接可以用，就是因为默认用了这里的镜像。



## readme文件分析

1、查看有哪些可选的东西。

```
make list
```

会列出6种板子。

## Makefile分析

这个的Makefile写得比较长。

1、选项V判断。看是否开启verbose模式。

2、board如果没有配置，就用vexpress-a9的。

3、会把boards/vexpress-a9下面的Makefile include进来。



在docker里改文件，就是改到了外面的文件里了。

docker里，再启动了一个qemu虚拟机。

make boot启动过程打印分析

是通过uboot引导的。

uboot是2015.07的版本。

dram是128M。

flash也是128M。

带一个MMC接口。

网卡是smc911x-0

kernel启动地址是6000 3000这里。

linux版本是4.6.7的。

镜像大小是3.9M，没有压缩。

initrd放在6000 9000这里。

大小是1.3M。

load entry是0000 0000 

设备树展开在6050 0000这里。

armv7的核心。

machine model是V2P-CA9

是一个单核CPU。

arm versatile express

是arm官方推出用来加快开发和降低新的soc设计风险的。

关键特性：

1、支持多种arm处理器。

2、大内存，支持丰富的外设，以太网、usb、PCI、显示。

3、支持完整的CoreSight调试和跟踪。

4、linux发行版本。

5、用户手册。

vexpress主要是面向soc设计者，所以板子的设计方法也很特别。采用了主板+子板的设计结构。

主板提供各种外围接口，子板提供CPU核心。

##自己编译并执行

使用vexpress-a9来进行编译。

1、make BOARD=vexpress-a9

```
Makefile的默认目标是board。它的行为是：
1、把板子的名字存到当前目录下一个叫.board_config的文件里。
2、打印板子的信息。
```

2、make root-defconfig

```
做的事情是：
1、依赖root checkout和root patch
2、root checkout是进入到buildroot目录进行git checkout操作。
3、在当前代码都是下载好的情况下，执行10几秒就完成了。
```

3、make root

```
我碰到了错误。说legacy配置问题。
谷歌查了一下。说是要进行menuconfig，手动关闭这些选项。强制进行这个操作，是因为要你清楚这个变化。
里面就是把最后一项默认是打开的，你要手动关闭这一项。然后保存退出。
再执行就好了。
但是执行过程非常耗时，还是要到网上下载不少的东西，网速又慢。我睡了一觉，起来看到已经编译通过了。
从output/arm/buildroot-2016.05-cortext-a9/images目录下的文件来看，是花了3个小时左右才生成的。
```

4、make kernel

```
也是报错。需要先make kernel-config就好了。
编译只要几分钟。
```

5、make modules && make modules-install

```
都没有做事情。提示是最新的。用make modules-list查看，只有一个叫ldt的东西。
```

6、make boot

```
会出现启动卡住在Starting kernel ...处。
```







