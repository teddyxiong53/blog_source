---
title: rt-thread环境搭建
date: 2016-11-26 22:08:12
tags:
	- rt-thead
---
下面总结在linux环境下进行rtthead的开发的步骤。
# 1. 下载代码
官网的代码下载地址在这里。http://www.rt-thread.org/page/31.html
github上也有，但是下载速度较慢，建议用官网地址下载。
当前最新的稳定版本是2.1的，我们就下载这个。代码压缩包大概50M。

# 2. 编译工具及环境准备
为了方便进行调试，我们选择用qemu模拟仿真的方式来做。这样就省去了下载到板端运行的步骤，因为我们当前的主要目标是熟悉rtthread的特点。
我们使用linux下的工具链来进行编译，这样看起来会清晰很多，整个环境就比较透明，不像在windows下用Keil IDE来做，很多地方不透明，改动起来比较麻烦。
工具链我之前有安装32位的arm交叉编译工具链，我是打算用mini2440的模拟环境，所以工具链就不需要另外安装了。
我的linux是Ubuntu14.04的。安装了qemu。

# 3. 代码配置
解压后的代码目录：
```
teddy@teddy-ubuntu:~/work/rtt/rt-thread-2.1.0$ tree -L 1 
.
├── AUTHORS
├── bsp
├── ChangeLog_CN.md
├── components
├── COPYING
├── documentation
├── examples
├── include
├── libcpu
├── README.md
├── src
└── tools

8 directories, 4 files
```
我们进入到bsp/mini2440里。需要修改的文件是rtconfig.py和rtconfig.h。rtconfig.py配置的是工具链。rtconfig.h配置的是控制编译的宏。
rtconfig.py
```
CROSS_TOOL 	= 'gcc' #这里要改

if os.getenv('RTT_CC'):
    CROSS_TOOL = os.getenv('RTT_CC')

if  CROSS_TOOL == 'gcc':
    PLATFORM 	= 'gcc'
    EXEC_PATH 	= '/home/teddy/rpi/rpi/bin/' #这里要改成你的工具链安装的目录。


...
if PLATFORM == 'gcc':
    # toolchains
    PREFIX = 'arm-linux-gnueabihf-' #这里改成你的工具链的名字。
```




