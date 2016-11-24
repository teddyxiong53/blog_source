---
title: 树莓派FM电台搭建
date: 2016-11-12 17:20:20
tags:
	- 树莓派
---

本文介绍用树莓派搭建一个FM小型电台。使用的是树莓派3代。

1. 下载代码。
这个是源代码。https://github.com/ChristopheJacquet/PiFmRds

这个需要依赖一个第三方库，叫libsndfile。http://pan.baidu.com/s/1kV2G9Vp
如果没有libsndfile，PiFmRds运行时会报错的，无法启动。

2. 编译。
libsndfile的编译：
```
tar -xvzf libsndfile-1.0.25.tar.gz
cd libsndfile-1.0.25
./configure
make
sudo make install
```
PiFmRds的编译：
```
cd PiFmRds/src
make clean
make
```

3. 运行。
在`PiFmRds/src`目录下，`././pi_fm_rds -audio sound.wav`。就可以运行。
但是我的板子是总是报这个错误。
```
./pi_fm_rds: error while loading shared libraries: libsndfile.so.1: cannot open shared object file: No such file or directory
```
我看库文件在lib目录下都有，我就直接把libsndfile的静态库拷贝到当前目录用来链接。
把Makefile里修改一下，加上`-L./ -lm -lsndfile`：
```
app: rds.o waveforms.o pi_fm_rds.o fm_mpx.o control_pipe.o mailbox.o
	$(CC) -o pi_fm_rds rds.o waveforms.o mailbox.o pi_fm_rds.o fm_mpx.o control_pipe.o -L./ -lm -lsndfile
```
再运行，又报错：
```
Failed to open /dev/mem: Permission denied.
Terminating: cleanly deactivated the DMA engine and killed the carrier.
```
那就用sudo来运行。果然就好了。默认是发射107.9MHz的频率。
```
pi@raspberrypi:~/work/fm/src/PiFmRds-master/src $ sudo ./pi_fm_rds -audio sound.wav
Using mbox device /dev/vcio.
Allocating physical memory: size = 3403776     mem_ref = 5     bus_addr = fd7b0000     virt_addr = 0x76a45000
ppm corr is 0.0000, divider is 1096.4912 (1096 + 2012*2^-12) [nominal 1096.4912].
Using audio file: sound.wav
Input: 228000 Hz, upsampling factor: 1.00
1 channel, monophonic operation.
Created low-pass FIR filter for audio channels, with cutoff at 12000.0 Hz
PI: 1234, PS: <Varying>.
RT: "PiFmRds: live FM-RDS transmission from the RaspberryPi"
Starting to transmit on 107.9 MHz.
```
4. 收听。
打开手机上的收音机应用，搜索到107.9MHz的频率，就可以收听了。
可以在树莓派的GPIO的7号管脚上插一根杜邦线，当天线用。






