---
title: Linux之mpd学习
date: 2020-01-16 15:37:19
tags:
	- Linux
---

1

mpd是Media Player Daemon的缩写。

是一个C/S结构的音乐播放器。mpd作为一个守护进程运行于后台。

管理playlist和数据库。

客户端是mpc。



安装：

```
sudo apt-get install mpd mpc
```

mpd的配置文件是/etc/mpd.conf

去掉注释后，剩下的是这样：

```
music_directory         "/var/lib/mpd/music"
playlist_directory              "/var/lib/mpd/playlists"
db_file                 "/var/lib/mpd/tag_cache"
log_file                        "/var/log/mpd/mpd.log"
pid_file                        "/run/mpd/pid"
state_file                      "/var/lib/mpd/state"
sticker_file                   "/var/lib/mpd/sticker.sql"
user                            "mpd"
bind_to_address         "localhost"
input {
        plugin "curl"
}
audio_output {
        type            "alsa"
        name            "My ALSA Device"
}
filesystem_charset              "UTF-8"
id3v1_encoding                  "UTF-8"
```

我们加上：

```
zeroconf_enabled "yes"
```

但是零配置需要改一些其他的配置。所以还是先不打开。这个不是当前的重点。



配置文件有2个地方，一个全局的，一个用户的。

```
/etc/mpd.conf
~/.config/mpd/mpd.conf
```



mpc update

这个命令是为了根据music目录下的文件，来更新database。

也可以配置auto_update 为yes，这样当music目录有改动的时候，就会自动更新数据库。



bind_to_address         "any" # 默认是localhost，这个应该是相当于0.0.0.0 



感觉需要看一下mpc的代码，不然操作总感觉不对劲。

有个gnu mpc库，是浮点数计算的，我说在这个里面怎么找不到main函数。

应该是mpd-mpc这个才是。代码很少。

所以看mpc的没有用。还是要看mpd的。

mpd的代码就比较多了，有1300个文件左右。

用C++写的。

另外还有一个库，libmpdclient。

在mpc里使用的mpd/client.h这个头文件，就是在这个库里面的。



这样手动启动：

```
teddy@teddy-ThinkPad-SL410:/var/lib/mpd$ sudo mpd --stdout --no-daemon --verbose /etc/mpd.conf
config_file: loading file /etc/mpd.conf
path: SetFSCharset: fs charset is: UTF-8
libsamplerate: libsamplerate converter 'Fastest Sinc Interpolator'
vorbis: Xiph.Org libVorbis 1.3.5
opus: libopus 1.1.2
sndfile: libsndfile-1.0.25
wildmidi: configuration file does not exist: /etc/timidity/timidity.cfg
adplug: adplug 2.2.1
db: reading DB
curl: version 7.47.0
curl: with GnuTLS/3.4.10
avahi: Initializing interface
avahi: Client changed to state 2
avahi: Client is RUNNING
avahi: Registering service _mpd._tcp/Music Player
avahi: Service group changed to state 0
avahi: Service group is UNCOMMITED
state_file: Loading state file /var/lib/mpd/state
inotify: initializing inotify
inotify: watching music directory
avahi: Service group changed to state 1
avahi: Service group is REGISTERING
avahi: Service group changed to state 2
avahi: Service 'Music Player' successfully established.
```

看到注册了avahi服务。

其他的机器，如何去发现`_mpd._tcp`这个服务？



我当前在music目录下有一个UrlPlayer.mp3的文件。删除掉这个文件，mpd这边打印了下面的内容。我是打开了auto_update的。所以自动更新了数据库。

```
client: [0] opened from 127.0.0.1:54780
client: [0] process command "listall """
client: [0] command returned 0
client: [0] closed
update: spawned thread for update job id 1
inotify: updating '' job=1
update: starting
update: removing UrlPlayer.mp3
simple_db: removing empty directories from DB
simple_db: sorting DB
simple_db: writing DB
update: finished
client: [1] opened from 127.0.0.1:54782
client: [1] process command "listall """
client: [1] command returned 0
client: [1] closed
```

随便放了5首歌曲到music目录下。

mpd这边打印了。

```
update: spawned thread for update job id 2
inotify: updating '' job=2
update: starting
update: reading /李志 - 关于郑州的记忆 (2016 unplugged).mp3
update: added /李志 - 关于郑州的记忆 (2016 unplugged).mp3
update: reading /李志 - 春末的南方城市 (2016 unplugged).mp3
update: added /李志 - 春末的南方城市 (2016 unplugged).mp3
update: reading /李志 - 定西 (2016 unplugged).mp3
update: added /李志 - 定西 (2016 unplugged).mp3
update: reading /李志 - 大象 (2016 unplugged).mp3
update: added /李志 - 大象 (2016 unplugged).mp3
update: reading /李志 - 杭州 (2016 unplugged).mp3
update: added /李志 - 杭州 (2016 unplugged).mp3
simple_db: removing empty directories from DB
simple_db: sorting DB
simple_db: writing DB
update: finished
```



mpc命令的格式：

```
mpc [options] <cmd> [args]
```

不带任何命令和参数，等价于mpc status。打印当前的状态。

参数：

```
-q ： 不要打印。
-v ： verbose
-h ： 指定host。
-p ： 指定port。
```

命令：

```
add
	后面跟文件名。
	从数据库里添加到播放列表。
insert
	是插入到当前歌曲后面，而add是放到末尾。
clear
	清空播放列表。
crop
	删除所有文件，除了当前在播放的这首。
current
	显示当前播放的歌曲名。
del pos
	删除第几首歌曲。
load file
	这个是载入播放列表。
ls [dir]
	列出music目录下的所有歌曲。
lsplaylists
	列出所有播放列表。
outputs
	查看
play [pos]
	播放歌曲，可以指定第几首。
pause
	暂停。
playlist
	查看播放列表。
prev
	播放前一首。
random on/off
	随机播放。
repeat on/off
	这个是指什么重复？
single on/off
	单曲循环。
consume on/off
	consume模式是什么？
rm file
	删除一个playlist。
save file
	保存播放列表。效果是这样。
	├── playlists
    └── mysongs1.list.m3u
seek 20%
seek 00:01:03
	都可以。
shuffle
	打乱歌单内容。
stats
	统计你的使用情况。
toggle
	播放暂停切换。
volume -20

```

依赖的环境变量：

```
MPD_HOST
MPD_PORT
```



当前播放打印：

```
output: Failed to open mixer for 'My ALSA Device'
```

```
sudo apt-get remove pulseaudio
```

网上看了一下，看起来是 pulseaudio和alsa的关系。

有两种方法：

1、卸载pulseaudio。

2、或者mpd配置使用pulseaudio。

我使用了卸载pulseaudio的方式。果然正常了。





参考资料

1、Arch Linux下使用Mpd+Mpc

https://www.linuxidc.com/Linux/2008-10/17031.htm

2、Creating a home music server using mpd

这个还比较高级。

https://feeding.cloud.geek.nz/posts/home-music-server-with-mpd/

3、mpd: Failed to read mixer for 'My ALSA Device': no such mixer control: PCM

参考这篇文章的解决了播放错误的问题。

https://askubuntu.com/questions/383449/mpd-failed-to-read-mixer-for-my-alsa-device-no-such-mixer-control-pcm