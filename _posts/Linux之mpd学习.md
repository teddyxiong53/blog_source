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
	音量减20
volume 50 
	音量设置为50，不带加减号，则表示为目标值，而不是偏移量。
	
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





playlist怎么用呢？

我直接这样添加：

```
/userdata/mpd/playlists # mpc add http://192.168.0.103/UrlPlayer.mp3    
error adding http://192.168.0.103/UrlPlayer.mp3: Unsupported URI scheme 
```

https://github.com/MusicPlayerDaemon/MPD/issues/599

http://mightyohm.com/forum/viewtopic.php?t=21



我的板端的mpd用mpd --version查看的信息如下：

```
/userdata/mpd/playlists # mpd --version                                       
Music Player Daemon 0.20.15                                                   
                                                
Database plugins:                                                             
 simple proxy                                                                 
                                                                              
Storage plugins:                                                              
 local                                                                        
                                                                              
Decoders plugins:                                                             
 [mad] mp3 mp2                                                                
 [pcm]                                                                        
                                                                              
Filters:                                                                      
                                                                              
                                                                              
Tag plugins:                                                                  
 id3tag                                                                       
                                                                              
Output plugins:                                                               
 null fifo alsa recorder                                                      
                                                                              
Encoder plugins:                                                              
 null wave                                                                    
                                                                              
Input plugins:                                                                
 file alsa                                                                    
                                                                              
Playlist plugins:                                                             
 extm3u m3u pls xspf asx rss cue embcue                                       
                                                                              
Protocols:                                                                    
 file:// alsa://                                                              
                                                                              
Other features:                                                               
 avahi epoll iconv inotify ipv6 tcp un                                        
```

那么看协议，就是不支持http的，只支持file和alsa的协议。

但是看支持m3u的，看看能不能用这个来做。

我这样操作。

```
/userdata/mpd/playlists # echo "http://192.168.0.103/UrlPlayer.mp3" > 1.m3u  
/userdata/mpd/playlists # mpc update                                         
Updating DB (#3) ...                                                         
volume:100%   repeat: off   random: off   single: off   consume: off         
/userdata/mpd/playlists # mpc ls                                             
1                                                                            
/userdata/mpd/playlists # mpc lsplaylist                                     
1                                                                            
```

但是mpc add不行。

```
/userdata/mpd/playlists # mpc ls |mpc add   
error adding 1: No such directory           
```

我在笔记本上查看，支持的协议有很多。包括http的。说明是支持的。

可能是板端编译的时候，没有打开。

```
Protocols:
 file:// http:// https:// mms:// mmsh:// mmst:// mmsu:// gopher:// rtp:// rtsp:// rtmp:// rtmpt:// rtmps:// smb:// nfs:// cdda:// alsa://
```

进buildroot里的mpd配置里，里面确实有不少的东西，默认没有选curl的，我选配上。重新编译看看。

现在看已经可以了：

```
Protocols:                         
 file:// http:// https:// alsa://  
```

要播放：

```
mpc add http://192.168.0.103/UrlPlayer.mp3
mpc play
```

就可以。



数据库是用sqlite的。



```
1、当前music和playlists目录都是空的。先执行: mpc add http://localhost/lizhi.mp3
2、mpc ls。这个是查看music目录下和playlists目录下的东西。所以是空的。
3、mpc playlist。这个是查看当前播放列表的。所以是可以看到这样的内容：
	root@thinkpad:/var/lib/mpd# mpc playlist
	http://localhost/lizhi.mp3
	add的歌曲，默认是添加到当前的playlist。
	但是这个playlist没有被保存成文件。
	怎样才能保存成文件呢？
4、现在就执行mpc play，就可以播放了。

我当前还是希望可以保存且累加歌曲到当前列表。
继续添加：
	mpc add http://localhost/UrlPlayer.mp3
现在看是有两首歌曲了。	
root@thinkpad:/var/lib/mpd# mpc playlist
http://localhost/lizhi.mp3
http://localhost/UrlPlayer.mp3
执行mpc save list1.m3u

root@thinkpad:/var/lib/mpd/playlists# ls
list1.m3u.m3u
root@thinkpad:/var/lib/mpd/playlists# cat list1.m3u.m3u 
http://localhost/lizhi.mp3
http://localhost/UrlPlayer.mp3
可见，是把当前歌单保存到了playlist目录下。而且会自动给你加上m3u的后缀。所以我当前多了一个后缀。

现在mpc ls，可以看到
root@thinkpad:/var/lib/mpd# mpc ls
list1.m3u
跟mpc lsplaylist一样的效果。

执行mpc clear后，当前歌单被清空。所以再执行mpc play就没有任何作用。
这时候，需要mpc load list1这样来重新导入playlist。mpc play才有效果。

```

所以就这样操作就好了。



# 配置为网络方式

mpc -h 192.168.0.104 play 这样只是进行了远程的控制而已。

并不会让声音传递到本机上来。



配置audio_output为http，应该怎样做呢？

这样得到是一个ogg的stream。

需要这样进行点播。

```
 http://192.168.1.2:8000/mpd.ogg
```

这样无疑是难以保证不同的客户端的同步性的。



# 蓝牙方式

需要一个.asoundrc文件。默认是在/var/lib/mpd/.asoundrc。

内容如下：

```
defaults.bluealsa {
	interface "hci0"
	device "xx:xx" # addr
	profile "a2dp"
}
```

然后需要修改mpd.conf文件。

```
audio_output {
	type "alsa"
	name "My ALSA Device"
}
audio_output {
	type "alsa"
	name "ALSA Bluetooth Headset"
	device "bluealsa"
	mixer_type "software"
}
```

# 系统音量控制

每次mpc play，都是默认100%的音量。

amixer sset Master 设置的系统音量，对于mpd的音量完全没有起作用。

这个是为什么？

网上看到一个人说自己的没法用mpd调节音量，是因为他的mixer_type是hardware。改成software就可以了。

```
audio_output {                             
    type            "fifo"                 
        name            "my pipe"          
        path            "/tmp/snapfifo"    
        format          "48000:16:2"       
        mixer_type      "software"         
}                                          
```



# 用库函数来进行播放控制

当前是使用mpc命令的方式进行控制的。

这种方式有几个问题：

1、效率低。

2、处理其实也并不方便，尤其是在获取一些播放信息的时候，解析字符串反而麻烦。而且不够健壮。

所以打算用库函数的方式来做。

对应的库是libmpdclient。在buildroot里有带。

先跑一下test/main.c的。看看运行效果。可以符合我的预期，就按照这个文件来改。

这个库的变化还比较大。

既然当前buildroot里默认带的是2.10的，那就以这个版本为准进行分析。

src/example.c也值得分析一下。而且这个比test那个更好些。



client.h这个是总的头文件，把其他头文件都包含在里面了。我们编程的时候，只需要包含这个头文件就好了。

```
Use mpd/client.h instead.
```



## 主要的头文件

```
async.h
	异步操作接口。
audio_format.h
	里面就一个结构体。
	struct mpd_audio_format 
		3个成员：采样率，格式，通道数。
capabilities.h
	一些send和recv函数。
client.h
	总头文件。
compiler.h
	定义了一些编译器相关的宏。
connection.h
	声明了一些mpd_connection_xx函数。
database.h
	一些send和recv函数。
directory.h
	一些mpd_directory_xx函数。
	
status.h
	获取mpd的运行状态。
	
```



## 主要的结构体

```
struct mpd_settings
	表示一个mpd服务器的信息。
	4个成员：
	host
	port
	password
	timeout

struct mpd_pair 
	这个是键值对，表示从mpd收到的键值对。
	
struct mpd_connection 
	这个是最重要的结构体。包含内容也稍微多点。
	struct mpd_settings
		服务器配置。
	struct mpd_error_info error;
		最近的一个错误。
	struct mpd_async *async;
		这个是连接的backend。
	struct timeval timeout;
		这个是所有命令的超时时间。
		如果mpd在这个时间内没有回复，则认为连接断开了。
	struct mpd_parser *parser;
		这个是用来解析mpd返回的内容的。
	bool receiving;
		表示是否正在接收mpd的返回内容。
	bool sending_command_list;
		是否正在进行发送命令。
	bool sending_command_list_ok;
		是否在用这个标志进行发送。
	bool discrete_finished;
		这个还需要进一步理解。
	char *request;
```



```
struct mpd_async 
	表示跟mpd通信的后端。
	4个成员。
	int fd
		这个是跟mpd通信的一个tcp socket。
	struct mpd_error_info error;
		
	struct mpd_buffer input;
		
	struct mpd_buffer output;
	
struct mpd_buffer
	这个3个成员。
	read/write index
	char buffer[4096]
	
```

如果指定host为NULL，那么就表示进行本地的mpd连接件。那么就退而使用本地socket。

```
#define DEFAULT_SOCKET "/var/run/mpd/socket"
```

不过我当前的配置文件里有：

```
bind_to_address         "/var/lib/mpd/socket"
```

io机制是用的select。

跟mpd的通信协议是基于字符串的。

连上来之后，有一个欢迎信息。

```
#define MPD_WELCOME_MESSAGE	"OK MPD "
```

然后是检查密码。



```
enum mpd_state 
	mpd播放暂停。
	有4个值。
	unknown
	stop
	play
	pause
```



## 主要的接口

连接相关

```

mpd_connection_new(NULL, 0, 30000)
	建立连接。
	参数1：是主机名。NULL表示本机。
	参数2：端口号。0表示使用默认。
	参数3：超时时间。ms为单位。
mpd_connection_get_error(conn) != MPD_ERROR_SUCCESS
	判断是否有错误。
mpd_connection_get_error_message(conn)
	获取错误信心。返回字符串。
mpd_connection_free(conn)
	释放连接。
```

状态相关

```
status = mpd_run_status(conn);
	获取状态。
mpd_status_free(status);
	处理完后要释放掉。
	里面还有指针。

mpd_status_get_state(status) == MPD_STATE_PAUSE
	获取播放状态。
```



文档在这：https://www.musicpd.org/doc/libmpdclient/index.html



一切操作的前提，是跟mpd建立一个mpd_connection连接。

所以很多函数的第一个参数，都是mpd_connection指针。



尽量基于同步机制来做。这样会比较简单。

mpd_run_status 这个相当于把发送和接收合并成一个函数了。就用这个就好了。

```
struct mpd_status *
mpd_run_status(struct mpd_connection *connection)
{
	return mpd_run_check(connection) && mpd_send_status(connection)
		? mpd_recv_status(connection)
		: NULL;
}
```

总体风格就是这样，mpd_run_xx相当于mpd_send_xx + mpd_recv_xx。

我们就只使用mpd_run_xx函数就可以了。



## player.h

这个头文件是我们需要重点关注的。

这里面的run函数有：

```
mpd_run_current_song
	获取当前歌曲信息。
mpd_run_play
	这个是播放。
mpd_run_play_pos
	这个是从指定的位置处开始播放。
mpd_run_play_id
	这个是指定歌曲id进行播放。
mpd_run_stop
	停止播放。
mpd_run_toggle_pause
	播放暂停切换。
mpd_run_pause
	暂停。
mpd_run_next
mpd_run_previous
mpd_run_seek_pos
mpd_run_seek_id
```



要获取当前的播放信息，还是需要mpd_song和mpd_status这2个一起组合得到。

mpd_song里面都是静态的信息，没有动态信息。就是歌手、专辑、时长这些信息。



写到后面，我发现libmpdclient里，缺少了mpc代码里不少的东西。

例如对当前歌曲进行seek操作。是对应seekcur这个命令，而这个命令在libmpdclient里没有。

我发现，自己写，可能短时间内健壮性比不上mpc命令的方式。

所以，还是先用命令来的方式来做吧。

mpc命令也并不是效率很低。



发现还是不能频繁大量调用mpc命令，这个命令是每次都建立socket连接，然后端口。

而我使用gmrender来实现dlna播放功能，这个里面有大量频繁的查询操作，导致系统了有一大堆的处于timed wait状态的socket。这个很不好。

所以我还是决定继续自己实现。



测试发现一个问题，就是我当前针对不同的模式，mpd用了不同的配置文件，其实是可以共用一个配置文件的。

mpd可以控制切换不同的输出通道的。

mpd必须不要被我的进程频繁杀掉，没有这个必要，当前杀掉mpd，导致连接的socket断开。

切换输出，是用这个命令：

```
{"toggleoutput", 1, -1,   0,    cmd_toggle_output, "<output # or name> [...]", "Toggle output(s)"},
```

配置文件里，把name指定为有规律的名字。

```
audio_output {
    type            "fifo"
    name            "output_snapfifo"
    path            "/tmp/snapfifo"
    format          "48000:16:2"
    mixer_type      "software"
}
audio_output {
    type        "alsa"
    name        "output_alsa"
    mixer_type      "software"
}
```

其实是可以同时从多个通道进行输出的。

```
/ # mpc outputs                         
Output 1 (output_snapfifo) is enabled   
Output 2 (output_alsa) is enabled   

/ # mpc toggleoutput output_alsa        
Output 1 (output_snapfifo) is enabled   
Output 2 (output_alsa) is disabled      
```

对应的函数是mpd_run_disable_output和mpd_run_enable_output。



## 调试问题

## 不要用send接口，用run接口

send发送不严格。run做了严格的检查。

## song的tag获取

```
std::string MpdPlayer::getTag(const struct mpd_song *song, enum mpd_tag_type type)
{
    unsigned i = 0;
	const char *value;
	while ((value = mpd_song_get_tag(song, type, i++)) != NULL) {
        return value;
    }
}
```

这样来获取。其他的方式，会内存错误。

但是这个还是会导致内存错误。我先用一个string对象包装一下再返回。

酷狗通过dlna传递过来的歌曲，获取不到title等tag信息。

## 报错

在使用中，碰到了这些错误。

```
reason:Cannot send a new command while receiving another response
```

这个还比较常见。

看代码，就是在mpd_run_check里做的。

```
mpd_run_check(struct mpd_connection *connection)
{
	assert(connection != NULL);

	if (mpd_error_is_defined(&connection->error))
		return false;

	if (connection->sending_command_list) {
		mpd_error_code(&connection->error, MPD_ERROR_STATE);
		mpd_error_message(&connection->error,
```

这个是因为还在等待回复的时候，又发了下一条命令导致的错误。

要避免非常频繁地发送命令。



播放完当前歌曲自动切换到下一首的时候，怎么主动对外报告这个信息？

mpd有没有主动向外报告这个事件？

没有这个事件。

## 经验

mpd_connection_new来创建一个到mpd的连接。

mpd_connection_free来释放这个连接。

大部分函数都是返回bool类型来表示成功失败，要看具体的错误细节，用下面这些函数：

```
mpd_connection_get_error
	返回枚举。
mpd_connection_get_error_message
	返回字符串。
mpd_connection_get_server_error
	返回枚举，这个是mpd端的错误，而不是客户端的错误。
```

不严重的错误，可以用mpd_connection_clear_error来清除。



# mpd协议

这个是在mpd代码的doc目录下的protocol.rst文件里。

基于字符串行进行通信。字符串编码是UTF-8的。

当前client连接到server，server回复。

```
OK MPD 0.12.2
```

后面的数字是当前mpd的版本号。

如果参数包含空格，那么就用用双引号包裹起来。

server回复的格式。

```
foo: bar
OK
```

前面是一些键值对，最后是一个OK。

也可以带上二进制数据。

```
foo: bar
binary: 42
<42 bytes data>
OK
```

如果是出错信息。

```
ACK [error@command_listNum] {current_command} message_text
```

看一个交互的例子。

client发给server。

```
command_list_begin
volume 86
play 10240
status
command_list_end
```

server回复给client。

```
ACK [50@1] {play} song doesn't exist: "10240"
```

表示错误码是50，命令索引为1（第0条是设置volume那条），对应就是“play 10240”这条命令。



## command list

上面的例子就是一个command list。

command list是以`command_list_begin`或者`command_list_ok_begin`开头。

以`command_list_end`结尾。

是要把所有命令都读取了才一起执行的，而不是读取一条执行一条。

返回的结果，是把所有的命令的返回拼接起来的。

如果所有命令都成功，返回OK。

如果有一条执行失败了，则后面的不再执行。直接返回。

如果是以command_list_ok_begin开头的，那么成功的时候，返回的是list_OK，而不是OK。



## 范围

有些命令，例如delete命令，会指定一个范围。

```
delete start:end
```

## 过滤

有些命令，例如find和searchadd，使用一个过滤规则。

## tags



## 窍门

有时候，用户有这种需求：

当前是用random方式进行播放，但是想要把一首歌曲插到当前歌单的最前面进行播放。

mpd可以支持这种操作。

实现的方式是给歌曲一个优先级。

对应的命令是priod和priodid。

默认情况下，优先级都是0.



操作歌单里的歌曲，有两种方式：

1、通过songid来操作。

2、通过song在playlist里的pos来操作。

使用songid的方式更安全一些。

```
mpc play [pos]
mpc playid [songid]
```



```
mpc add http://1.mp3
mpc addid http://1.mp3 1
```

```
mpc delete 0
mpc deleteid 12

mpc move 0 1
mpc moveid 2 3 
```

```
mpc prio 1 1 
mpc prioid 1 2
```



查询mpd状态

clearerror

清除当前的status里的错误信息。每次调用播放相关命令的时候，会自动执行这个。

currentsong

显示当前歌曲的信息。获取tag信息就靠这个了。





mpd里有个consume的概念，这个具体是指什么？

我从名字上理解，感觉是把当前播放完的歌曲移除掉。如果可以实现这个功能，那么我插播一些信息就可以很方便地进行实现了。

实际测试了一些，的确是这种效果。

```
consume {STATE} [2]
Sets consume state to STATE, STATE should be 0 or 1. When consume is activated, each song played is removed from playlist.
```



# mpd支持dlna

看配置文件里，有这个：

```
ifeq ($(BR2_PACKAGE_MPD_UPNP),y)
MPD_DEPENDENCIES += expat libupnp
MPD_CONF_OPTS += --enable-upnp
else
MPD_CONF_OPTS += --disable-upnp
endif
```

mpd直接进行dlna播放，是否可行呢？

用“mpd dlna”做关键字进行搜索。找到的还是upmpdcli这个作为mpd的前端来进行dlna支持的。

# 播放aac

mpd安装默认的配置编译出来，是不能正常播放aac文件的。

我用ffmpeg插件来看看。编译后，播放aac文件，没有声音。

查看/var/log/mpd.log文件里：

```
ffmpeg/aac: Estimating duration from bitrate, this may be inaccurate
```

从网上搜索，这个是ffmpeg解码aac的问题。



mpd的插件里，选配上faad2的插件就可以解码aac的了。

FAAD2 is an open source MPEG-4 and MPEG-2 AAC decoder



ffmpeg系列-解决ffmpeg获取aac音频文件duration不准

https://blog.csdn.net/u013470102/article/details/80880079



# playlist处理

现在需要保存多个歌单，播放过程中根据需要在不同的playlist之间切换。

/var/lib/mpd/state  这个文件，在mpc clear的时候，会变化。

```
/ # cat /var/lib/mpd/state            
sw_volume: 100                        
audio_device_state:1:output_snapfifo  
state: stop                           
random: 0                             
repeat: 0                             
single: 0                             
consume: 0                            
crossfade: 0                          
mixrampdb: 0.000000                   
mixrampdelay: -1.000000               
playlist_begin                        
playlist_end                          
```

执行mpc ls | mpc add的时候，lizhi.aac是放在music目录下。default是一个歌单的名字。

```
May 26 10:09 : client: process command "add "lizhi.aac""
May 26 10:09 : client: command returned 0
May 26 10:09 : client: process command "add "default""
May 26 10:09 : exception: No such directory
```

play/pause这些操作，会触发/var/lib/mpd/state的变化。

我应该是可以用inotify来监听这个文件的变化，来得到mpd的状态变化事件。

```
播完歌单的事件。
播放完成的时候，mpd.log里记录了。
May 26 13:20 : player: played "https://api.testiot.dossav.com/storage/mp3/030920200924465e659ade933ac.aac"

在state文件里记录了：
playlist_begin
song_begin: https://api.testiot.dossav.com/storage/mp3/030920200924465e659ade933ac.aac
mtime: 0
song_end
song_begin: https://api.testiot.dossav.com/storage/mp3/030920200924465e659ade933ac.aac
mtime: 0
song_end
song_begin: https://api.testiot.dossav.com/storage/mp3/030920200924465e659ade933ac.aac
mtime: 0
song_end
playlist_end
```

可以读取最后一行。看看是不是playlist_end。

每次按播放，这个state文件内容都会被清空。

所以这个内容不会很长。

经实际测试，不能用inotify来监听state文件的变化。

因为state文件变化时，inode也变化了。

所以inotify无法跟踪这样的变化。



现在就只能尝试进行更加细致的歌单操作来达到目的。



优先级从0到255，数字越大，优先级越高。默认都是0 。

A priority is an integer between 0 and 255. The default priority of new songs is 0.

优先级只在random模式下有效。



# mpd支持samba

现在有个需求，就是让板端直接播放samba服务器上的文件。

samba服务器还是有密码的。

```
ifeq ($(BR2_PACKAGE_MPD_LIBSMBCLIENT),y)
MPD_DEPENDENCIES += samba4
MPD_CONF_OPTS += --enable-smbclient
else
MPD_CONF_OPTS += --disable-smbclient
endif
```

配置上是要求这个。

我先配置上编译跑一下看看，然后先用不需要密码的samba服务器测试一下。

先用vlc来测试一下samba上的文件是否可以播放。

在一台已经通过用户名和密码验证连接了目标samba服务器的电脑上。使用vlc直接播放下面的地址：

```
smb://172.16.2.3/public/music/1.mp3
```

可以正常播放。

而在一台没有保存过目标samba服务器的电脑上用vlc播放这个地址，则报错：

```
open failed for '172.16.2.3/public/music/1.mp3' (Permission denied)
```

所以进行正常播放的前提，就是板端需要先进行连接认证，保存这个认证信息。



所以，当前是先要搞清楚，Linux作为samba 客户端，连接其他的samba服务器的时候，应该怎样操作。

我在板端执行执行：

```
 smbclient -L //172.16.2.3
```

提示下面的错误：

```
smbclient: Can't load /etc/samba/smb.conf - run testparm to debug it
```

所以，首先是需要生成一个smb.conf。

我先在我的笔记本上做实验。基本通路通了再看板端的情况。

现在在笔记本的mpd.conf里，配置：

```
music_directory  "smb://172.16.2.121/homes/music"
```

重新启动mpd。看mpd.log里打印这个：

```
smbclient: smbc_opendir('smb://SAMBA') failed: Invalid argument
```

当前认证操作肯定是还没有。

但是也不知道知道在哪里填认证信息。

当前为什么打印“smb://SAMBA”呢？不是应该打印我填入的ip地址吗？

mpd依赖了libsmbclient。

这个库是samba4-4.7.4下的一部分。



# mpc更新到最新版本

在阅读官网文档的时候，发现有些命令，在当前我的版本上是找不到的。

我当前的是0.27的。

到官网看，mpc的最新版本是0.33的。

下载源代码。这个编译体系是meson+ninja。

```
meson . output
ninja -C output
sudo ninja -C output install
```

meson是通过pip来安装，依赖python3。所以我把默认Python改成python3才行。

ninja也需要升级到最新版本。到官网下载二进制文件，放到/usr/bin目录下就好。



# 官网文档

mpd的编译需要c++14、boost的支持。

还有对应的插件库。

使用meson和ninja进行编译。

## 配置文件写法

每一行的格式是：

```
key "value"
```

value要用引号括起来。

可以include其他的配置文件。



## 配置music目录

当你播放本地文件的时候，你需要把文件放在music目录下。

默认情况下，mpd运行在music目录下使用软连接。

除了使用本地文件，你还可以使用storage插件来访问服务器上的文件。

例如，配置在smb服务器上的music，可以这样：

```
music_directory "smb://ip/music_dir"
```

你还可以使用多个存储插件来组成一个虚拟的music目录。访问分布在不同的位置的music。

## 配置数据库插件

当一个music目录被配置的食盒，一个数据库插件也就被使用了。

可以在mpd.conf里这样配置：

```
database {
	plugin "simple"
	path "/var/lib/mpd/db"
}
```

## 配置neighbor插件

所有的neighbor插件默认都是禁用的。

要使能的话，这样进行配置：

```
neighbors {
	plugin "smbclient"
}
```

## 配置input插件

```
input {
	plugin "curl"
	proxy "socks://120.0.0.1:1080"
}
```

## 配置input cache

input cache，就是用来提前缓存要播放的歌曲。

是缓存到内存里。这样可以避免网络导致的卡顿，也可以让硬盘不用一直工作。

```
input_cache {
	size "1 GB"
}
```

mpd通过监听SIGHUP信号来情况这个input_cache。

## 配置解码插件

大部分的解码插件不需要配置，默认的配置就能正常工作。

如果要配置的话，如下：

```
decoder {
	plugin "wildmidi"
	config_file "/etc/timidity/timidity.cfg"
}
```

## 配置编码插件

比较少用。

## 配置audio output

这个很常用。

```
audio_output {
	type "alsa"
	name "my alsa device"
	device "default"
}
```

## 配置filter

这个是用来修改audio stream的。

```
filter {
	plugin "volume"
	name "software volume"
}
```

filter后续会被合并到audio output里面。

## 配置playlist插件

```
playlist_plugin {
	name "m3u"
	enabled "true"
}
```



## client connection

是通过bind_to_address这个配置来做的。

可以罗列多个bind_to_address来绑定到多个。



## state文件

state文件是mpd存储和恢复状态的。这样在重启的时候，就可以恢复之前的状态。

这个不是必选项。

有2个配置项：

```
state_file "/var/lib/mpd/state"
state_file_interval "120"
```

## 资源限制

```
connection_timeout
	默认60s，如果超过这个时间没有通信，则断开。
max_connections
	默认100个。
max_playlist_length
	playlist最多多少首歌曲。默认16384首。
max_command_list_size
	默认2M。
max_output_buffer_size
	默认8M。
```



## 高级配置



## 使用mpd

最简单的启动方式，就是

```
mpd
```

不带任何参数就可以启动。

停掉的方式：

```
mpd --kill
```

从代码看，处理了这3个信号。

```
	SignalMonitorRegister(SIGINT, {&loop, HandleShutdownSignal});
	SignalMonitorRegister(SIGTERM, {&loop, HandleShutdownSignal});

	SignalMonitorRegister(SIGHUP, {nullptr, handle_reload_event});
```

你往music目录下放入一些文件，然后执行

```
mpd update
```

根据文件的多少和机器的速度，这个操作花费的时间不同。

你可以把其他的路径挂载到music目录。

```
mpc mount my_nfs nfs://192.168.1.4/export/mp3
mpc mount my_udisk udisks://uuid
mpc umount my_udisk
```

查看neighbor

```
mpc listneighbors
```

我当前的版本不支持这个命令。

## metadata

当扫描或者播放一首歌曲的食盒，mpd会解析歌曲的metadata。

## queue

队列，就是当前的播放歌曲列表。

mpc playlist查看到的就是。







参考资料

1、Arch Linux下使用Mpd+Mpc

https://www.linuxidc.com/Linux/2008-10/17031.htm

2、Creating a home music server using mpd

这个还比较高级。

https://feeding.cloud.geek.nz/posts/home-music-server-with-mpd/

3、mpd: Failed to read mixer for 'My ALSA Device': no such mixer control: PCM

参考这篇文章的解决了播放错误的问题。

https://askubuntu.com/questions/383449/mpd-failed-to-read-mixer-for-my-alsa-device-no-such-mixer-control-pcm

4、

https://cheat.readthedocs.io/en/latest/mpd.html

5、mpd+mpc配置

https://my.oschina.net/diefrom/blog/347666?p={{page}}

6、树莓派打造私人电台

https://lmbj.net/blog/raspberry-pi-build-private-fm-radio/

7、MPD

https://wiki.gentoo.org/wiki/MPD

8、mpd协议

https://www.musicpd.org/doc/html/protocol.html

9、用电脑小主机自己做数字播放器 – MPD+LMS篇 

http://blog.sina.com.cn/s/blog_537a660c0102wa6r.html

10、官网文档

https://www.musicpd.org/doc/html/user.html



