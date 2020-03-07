---
title: Linux之命令行音乐播放器对比
date: 2020-03-05 15:55:28
tags:
	- 音视频

---

1

从buildroot的menuconfig里audio application里一个个看。搜索相关信息，罗列如下。

```
bellogio
	这个是openmax il这个音频框架的实现。
madplay
	 MPEG audio decoder and player
	 叫这个名字，是基于libmad。
	mad是Mpeg Audio Decoder。
	这个不是很合适。
mpd/mpc
	这个是Linux里比较好的。
mplayer
	是可以播放视频的软件。
	播放http上的音乐没有问题。
	这个会不会太大了。
vlc
ffplay
```

在Linux下有很多不错的音乐播放器，强大的如amarok，简单的如bmp，而我更喜欢mpc（需要安装MPD），简洁是我选择它的理由。

每次开机自动打开守护程序MusicPD（简称mpd），这如同一个潜在的点歌器，

终端下用mpc就能选听自己喜欢的歌曲，不需要任何界面，也不必为音乐播放器单开一个桌面。



mpc用法

配置文件/etc/mpd.conf 。没有什么特别的。

/var/lib/mpd/music

```
1、先拷贝一首歌曲放到music目录下。
2、mpc update。这个命令是必须的。
3、mpc play
4、mpc listall | mpc add 把所有的歌曲添加到播放列表。
```

```
mpc volume +20 //音量加20
```

mpd是用boost c++写的。

buildroot里的编译出来可以运行。

但是add url有问题。

```
/userdata # mpc add https://music.163.com/#/song?id=28815250&market=baiduqk               
/userdata # error adding https://music.163.com/#/song?id=28815250: Unsupported URI scheme 
                                                                                          
[1]+  Done(1)                    mpc add https://music.163.com/#/song?id=28815250         
/userdata # mpc add http://172.16.4.205:8000/examples1.ogg                                
error adding http://172.16.4.205:8000/examples1.ogg: Unsupported URI scheme               
```

笔记本上安装的版本，添加url没有问题，但是解码有问题。

```
teddy@teddy-ThinkPad-SL410:/var/lib/mpd$ mpc next
volume: n/a   repeat: off   random: off   single: off   consume: off
ERROR: Failed to decode http://172.16.4.205:8000/examples1.ogg
```



总的来说，我觉得，mpd这一套太麻烦了。不符合我的需求。



cmus

```
sudo apt-get install cmus
```

https://github.com/cmus/cmus/wiki

这个是用vi类似的操作来控制的。

也复杂了。



vorbis-tools

```
sudo apt-get install vorbis-tools
```

这里有个ogg123的工具。

用来跟icecast配合简直是绝配。两个都是只支持ogg格式的。

这个工具要用上。



mpg123

这个专门用来播放mp3文件的。很好。



mplayer

也是要前台播放才行。



试一下madplay。

所有的命令行播放器，都要是占据console前台运行。



我最后的保底选择是ffplay和vlc。



参考资料

1、MPC+MPD+Conky听音乐

https://www.jianshu.com/p/2d5884a6d317

2、命令行音频播放器

这里推荐的都很不错。

https://ubuntuqa.com/article/1775.html