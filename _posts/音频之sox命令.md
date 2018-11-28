---
title: 音频之sox命令
date: 2018-11-28 19:42:15
tags:
	- 音频

---



sox是Sound eXchange的意思。man手册里写的是，音频信号处理的瑞士军刀。

我现在用audacity生成一个3秒的正弦波音频，保存为1.wav文件。

sox默认不支持mp3（囧，这么基础的都不支持，怎么好意思说自己是瑞士军刀呢？）

但是可以通过安装一个支持库来做到。

```
sudo apt-get install libsox-fmt-mp3
```



# 格式转换

wav转mp3。用法很简单，其他格式化也类似。

```
 sox 1.wav 1.mp3
```

# 调整音频速度

```
 sox 1.wav 1_faster.wav speed 1.5
```

# 连接2个文件

```
sox 1.wav 1_faster.wav 11.wav
```



sox带了play和rec这2个命令，可以进行播放和录音。



# 参考资料

1、SoX使用手册（中文版）

https://blog.csdn.net/p222p/article/details/77624046