---
title: mpd代码分析
date: 2020-05-28 14:06:19
tags:
	- Linux
---

1

现在要把mpd的代码阅读一下，这样碰到问题解决也会快一些。

```
#ifdef HAVE_ICU

void
IcuInit();
```

这个icu是ICU - International Components for Unicode的意思。

有一个软件包叫icu。

官网在这。是处理Unicode相关事务的。

http://site.icu-project.org/

# src目录

```
Android
	有3个类。Context、Environment、LogListener。
archive
	具体用途后续才清楚。
	下面有个plugins目录。
AudioCompress
	下面就一个c文件。compress.c。
client
	代表了一个mpd client实例。
command
	处理命令相关。
config
	配置相关。
db
	数据库相关。下面也有一个plugins目录。
decoder
	解码器。下面也有一个plugins目录。
encoder
	编码器。
event
	事件相关。
filter
	过滤器。下面也有一个plugins目录。
fs
	文件系统相关。
haiku
	下面就3个脚本。
input
	输入相关。下面有plugins目录。
java
	估计是为了跟java对接用的几个类。
lib
	下面有20个子目录。
mixer
	混音器相关。下面有plugins目录。
neighbor
	局域网相关。下面有plugins目录。
net
	网络相关。
output
	输出相关，下面有plugins目录。
pcm
	这个下面都有几十个类。
player
	这个下面只有几个类。
playlist
	播放列表相关。下面有个plugins目录。
protocol
	估计是实现mpd协议的几个类。
queue
	歌单操作。
song
	歌曲相关。
sticker
	歌曲标签。这个名字用得有点怪。用tag不好吗？
storage
	存储相关。有plugins目录。
system
	系统相关。
tag
	还真有一个tag目录。
thread
	线程相关。
time
	时间相关。
unix
util
win32
```

除了上面这些目录，在src根目录下，还有很多的c++文件。

```
 find -name "*.cxx" |wc -l
```

这样统计，是578个文件。

hxx文件是733个。

总共是1311个文件。



从ConfigOption这枚举类看，有这些可配置项：

```
music目录
playlist目录
符号链接
db文件
sticker文件
log file
pid file
state file
restore paused
user
group
bind to address
port
log level
zero conf name
zero conf enable
password
local permission
default perm
audio output format
mixer type
replay gain
volume normalization
samplerate converter
audio buffer size
buffer before play
http proxy
conn timeout
max conn
max playlist length
charset
id3v1 encoding
metadata to use
save absolute paths
gapless mp3 playback
auto update
auto update depth

```

ConfigBlockOption这个枚举类，是那些可以用大括号括起来的较复杂的配置，而不是单行的那种。

```
audio output
decoder
input
playlist plugin
resampler
audio filter
database
neighbors
```



依赖了boost库。

# Partition

```
/**
 * A partition of the Music Player Daemon.  It is a separate unit with
 * a playlist, a player, outputs etc.
 */
struct Partition
```



参考资料

1、