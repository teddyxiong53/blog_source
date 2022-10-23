---
title: linphone学习（1）
date: 2020-02-20 13:45:51
tags:
	- 音频

---

1

# linphone基本情况

linphone是Linux Phone的缩写。

是法国人写的。man查看帮助，可以看到是法语的。

是一个免费的voip以及sip客户端。

可以进行声音和视频通话。

可以通过软交换或者IP-PBX通话。

也可以用来做即时通信。

有图形界面，也可以在命令行上使用。

底层的协议是RTP协议。

linphone在开源世界里，是一个常用的通信工具。

现在新增了群组通话功能。



# 搭建sip服务器

在基于sip协议进行voip通话时，需要搭建sip服务器。

opensips

从官网下载LTS版本。

2.4版本是一个LTS版本。网上不少的文章都是基于这个来讲解的。



https://opensips.org/pub/opensips/2.4.7/

需要的依赖：

```
sudo apt-get install libncurses5-dev libncursesw5-dev libxml2-dev
```

安装mysql支持。安装时，提示设置root的密码。设置为最简单的那个。

```
 sudo apt-get install libmysqlclient-dev   mysql-client mysql-server
```

执行make menuconfig。

改动2个点就可以了：

```
1、需要打开db_mysql
2、指定prefix为/usr/local/opensips
```

menuconfig的结果，保存在Makefile.conf文件里。

参考官方文档进行编译：

https://www.opensips.org/Documentation/Install-CompileAndInstall-2-4

编译安装：

```
make all -j4
sudo make install
```

安装后的目录情况：

```
root@teddy-ThinkPad-SL410:/usr/local/opensips# tree
.
├── etc
│   └── opensips
│       ├── opensips.cfg
│       ├── opensipsctlrc
│       └── osipsconsolerc
├── lib64
│   └── opensips
│       ├── modules
│       └── opensipsctl
│           ├── opensipsctl.base
│           ├── opensipsctl.ctlbase
│           ├── opensipsctl.fifo
│           ├── opensipsctl.sqlbase
│           ├── opensipsctl.unixsock
│           └── opensipsdbctl.base
├── sbin
│   ├── opensips
│   ├── opensipsctl
│   ├── opensipsdbctl
│   ├── opensipsunix
│   ├── osipsconfig
│   └── osipsconsole
└── share
```

修改/usr/local/opensips/etc/opensips/opensipsctlrc

主要目的是配置mysql的。还有配置ip地址。

然后是修改opensips.cfg文件。

这个最好是重新生成一个。

代码目录下执行menuconfig，选择生成配置脚本。

然后把得到的cfg文件，拷贝到/usr目录下去，替换默认的opensips.cfg。

在这个基础上进行修改。

改完后，执行命令检查一下配置：

```
opensips -C
```

创建数据库。

```
opensipsdbctl create
```

启动服务：

```
opensipsctl start
```

添加账号。

```
opensipsctl add 1000 1000
opensipsctl add 2000 2000 
```

我把台式机Ubuntu作为服务器，笔记本和手机作为2个通话设备。可以正常进行通话。



Ubuntu下安装linphone。

```
sudo apt-get install linphone
```





# linphone交叉编译

上面已经验证了linphone的通路。

接下来就看怎么把linphone移植到板子上。

其实主要就是交叉编译。

从官方wiki可以看到，可以支持嵌入式板子。

```
embedded targets : Yocto, Xamarin
```

buildroot里也有的。

版本是3.6的。

```
--disable-strict --disable-video
LINPHONE_DEPENDENCIES = host-pkgconf libeXosip2 speex
--disable-gtk_ui
LINPHONE_DEPENDENCIES += host-intltool host-gettext
LINPHONE_CONF_OPTS += --enable-alsa
LINPHONE_DEPENDENCIES += alsa-lib
LINPHONE_CONF_OPTS += --disable-libv4l1 --disable-libv4l2
```



linphone需要upnp来支持什么功能？

https://www.linphone.org/news/linphone-upnp

这里有说明，没有仔细看，似乎是跟NAT有关的。

先不关注这个点，libupnp选配上的。



linphone的命令行上，怎么配置呢？

通过tab补全，发现板端有两个linphone相关的命令。

linphonec和linphonecsh。

linphonecsh是封装linphonec的一个工具。



```
/ # linphonec -h
NLS disabled.
ERROR: bad arguments

usage: linphonec [-c file] [-s sipaddr] [-a] [-V] [-d level ] [-l logfile]
linphonec -v

  -b  file             specify path of readonly factory configuration file.
  -c  file             specify path of configuration file.
  -d  level            be verbose. 0 is no output. 6 is all output
  -l  logfile          specify the log file for your SIP phone
  -s  sipaddress       specify the sip call to do at startup
  -a                   enable auto answering for incoming calls
  -V                   enable video features globally (disabled by default)
  -C                   enable video capture only (disabled by default)
  -D                   enable video display only (disabled by default)
  -S                   show general state messages (disabled by default)
  --wid  windowid      force embedding of video window into provided windowid (disabled by default)
  -v or --version      display version and exits.
/ # linphonecsh -h
Usage:
linphonecsh <action> [arguments]
where action is one of
        init            : spawn a linphonec daemon (first step to make other actions)
                        followed by the arguments sent to linphonec
        generic         : sends a generic command to the running linphonec daemon
                        followed by the generic command surrounded by quotes,
                         for example "call sip:joe@example.net"
        register        : register; arguments are
                        --host <host>
                        --username <username>
                        --password <password>
        unregister      : unregister
        dial            : dial <sip uri or number>
        status          : can be 'status register', 'status autoanswer' or 'status hook'
        soundcard       : can be 'soundcard capture', 'soundcard playback', 'soundcard ring',
                         followed by an optional number representing the index of the soundcard,
                         in which case the soundcard is set instead of just read.
        exit            : make the linphonec daemon to exit.
/ #
```



```
linphonec [-c file] [-s sipaddr] [-a] [-V] [-d level ] [-l logfile]
```

板端执行这个命令：

```
linphonec -s sip:1000@172.16.4.205 -d 6 -a
```

手机是设置为1000/1000这个用户名和密码的。

可以拨通手机并接听。

板端的身份是：`sip:root@172.16.4.136`。这个是自动根据系统信息生成的。

用户是root用户，后面是ip地址。

这样运行：

```
linphonec  -d 6 -a
```

我们可以根据之前手机的通话记录，从手机向板端拨打电话。





参考资料如果你的SIP服务已经部署到生产环境（通常使用linux操作系统），这时我们通常只能使用命令行模式，那么xlite就无法使用。此时我推荐使用linphonec。



执行linphone程序会在home目录下生成一个.linphonerc文件。这个就是配置信息。

```
[rtp]
download_ptime=0

[sip]
media_encryption=none
default_proxy=0

[video]
display=1
capture=1
automatically_initiate=1
automatically_accept=1
show_local=0
self_view=0
device=V4L2: /dev/video0
size=cif

[net]
download_bw=0
upload_bw=0
adaptive_rate_control=1

[GtkUi]
videoselfview=0
advanced_ui=1
uri0="chuizi" <sip:1000@172.16.2.149>

[sound]
playback_dev_id=ALSA: default device
ringer_dev_id=ALSA: default device
capture_dev_id=ALSA: default device
echocancellation=1
mic_gain_db=0.000000

[proxy_0]
reg_proxy=<sip:2000@172.16.2.149>
reg_identity=sip:2000@172.16.2.149
reg_expires=3600
reg_sendregister=1
publish=0
dial_escape_plus=0

[auth_info_0]
username=2000
userid=2000
passwd=2000
realm="172.16.2.149"

[friend_0]
url="chuizi" <sip:1000@172.16.2.149>
pol=accept
subscribe=1

[call_log_0]
dir=0
status=3
from=<sip:2000@172.16.2.149>
to="chuizi" <sip:1000@172.16.2.149>
start_date_time=1582189384
duration=5
quality=-1.000000
video_enabled=0
call_id=2065069723
```

因为我的板子的rootfs是只读的。

可以指定一下配置文件的生成路径。

```
touch /data/linphonerc
linphonec -c /data/linphonerc -d 6 -a
```

这样运行，看到文件里被写入了如下内容：

```
[rtp]                   
download_ptime=0        
                        
[sip]                   
media_encryption=none   
                        
[video]                 
display=0               
capture=0               
show_local=0            
                        
[net]                   
download_bw=0           
upload_bw=0             
```



linphonec，不带任何参数，则是进入到一个交互命令行。

```
linphonec> help                                                      
Commands are:                                                        
---------------------------                                          
      help      Print commands help.                                 
      call      Call a SIP uri or number                             
     calls      Show all the current calls with their id and status. 
      chat      Chat with a SIP uri                                  
 terminate      Terminate a call                                     
    answer      Answer a call                                        
     pause      pause a call                                         
    resume      resume a call                                        
  transfer      Transfer a call to a specified destination.          
conference      Create and manage an audio conference.               
      mute      Mute microphone and suspend voice transmission.      
    unmute      Unmute microphone and resume voice transmission.     
playbackga      Adjust playback gain.                                
  duration      Print duration in seconds of the last call.          
autoanswer      Show/set auto-answer mode                            
     proxy      Manage proxies                                       
 soundcard      Manage soundcards                                    
    webcam      Manage webcams                                       
      ipv6      Use IPV6                                             
       nat      Set nat address                                      
      stun      Set stun server address                              
  firewall      Set firewall policy                                  
 call-logs      Calls history                                        
    friend      Manage friends                                       
      play      play a wav file                                      
    record      record to a wav file                                 
      quit      Exit linphonec                                       
```

板端执行linphonec，进入交互模式。

手机给板端打电话，板端响铃，输入answer接听。

打印了这些错误：

```
linphonec> answer                                                         
Connected.                                                                
linphonec> Call 1 with <sip:1000@172.16.4.205> connected.                 
Media streams established with <sip:1000@172.16.4.205> for call 1 (audio).
linphonec> ortp-error-snd_pcm_avail_update: Broken pipe                   
ortp-error-*** alsa_can_read fixup, trying to recover                     
ALSA lib pcm.c:8882:(snd_pcm_recover) overrun occurred                    
ortp-error-snd_pcm_avail_update: Broken pipe                              
```

这里的问题跟我的完全一样。看到是说通过升级linphone版本解决了。这个是11年的帖子了。但是也提到修改alsa的缓冲区。

https://linphone-developers.nongnu.narkive.com/9JhuwgV1/linphone-3-1-0-ortp-error-alsa-can-read-fixup-trying-to-recover

这个也提到了修改alsa的缓冲区。

http://blog.sina.com.cn/s/blog_5234e34c0100wx4d.html

改了了，板端还是如此。可以确定改动已经编译到板端了。

板端可以这样注册到服务器。

```
register sip:2000@172.16.4.205 sip:2000@172.16.4.205 2000
```

格式是：`register <sip identity> <sip proxy> <password>`。



# 笔记本上手动编译linphone



在阿里云服务器上编译opensips。

运行的时候，报错：

```
ERROR: PID file /var/run/opensips.pid does not exist -- OpenSIPS start failed
```

看/var/log/syslog：

```
Feb 21 13:31:45 xhl-ecs /usr/local/opensips/sbin/opensips[28996]: ERROR:core:udp_init_listener: bind(2e, 0x7f86f109f744, 16) on 120.24.238.146: Cannot assign requested address
Feb 21 13:31:45 xhl-ecs /usr/local/opensips/sbin/opensips[28996]: ERROR:core:trans_init_all_listeners: failed to init listener [120.24.238.146], proto udp
Feb 21 13:31:45 xhl-ecs /usr/local/opensips/sbin/opensips[28996]: ERROR:core:main: failed to init all SIP listeners, aborting
Feb 21 13:31:45 xhl-ecs /usr/local/opensips/sbin/opensips[28996]: INFO:core:cleanup: cleanup
```

是因为我在配置文件力量设置的120.24.238.146这个地址对于内部是不可用的。

改了就可以启动了。

但是用公网ip是连不上去的。

这个的根本原因，大概是公网的问题。

为什么阿里云的公网ip不能用ifconfig看到，而且不能在命令行里使用呢？



在linphone.org上注册一个用户名。

地址是：sip:teddyxiong53@sip.linphone.org

这样就避免了自己搭建服务器了。

是用手机号注册的。



# 树莓派测试

现在我把环境这样来搭建：

```
笔记本做服务器
树莓派：客户端
手机：客户端

可以正常通话，声音正常。
```

双向声音都正常。

虽然有打印几行这个：

```
2020-02-21 15:30:18:891 ortp-error-snd_pcm_avail_update: Broken pipe
2020-02-21 15:30:18:891 ortp-error-*** alsa_can_read fixup, trying to recover
2020-02-21 15:30:21:936 ortp-error-snd_pcm_avail_update: Broken pipe
2020-02-21 15:30:21:936 ortp-error-*** alsa_can_read fixup, trying to recover
2020-02-21 15:30:42:375 ortp-error-snd_pcm_avail_update: Broken pipe
```



在用我的板子进行测试。

启动linphonec的时候，打印了这些错误。

```
ALSA lib conf.c:5000:(snd_config_expand) Unknown parameters 0           
ALSA lib control.c:1373:(snd_ctl_open_noupdate) Invalid CTL default:0   
ALSA lib conf.c:5000:(snd_config_expand) Unknown parameters 0           
ALSA lib pcm.c:3060:(snd_pcm_open_noupdate) Unknown PCM default:0       
ALSA lib conf.c:5000:(snd_config_expand) Unknown parameters 0           
ALSA lib pcm.c:3060:(snd_pcm_open_noupdate) Unknown PCM default:0       
ALSA lib conf.c:5000:(snd_config_expand) Unknown parameters 7           
ALSA lib control.c:1373:(snd_ctl_open_noupdate) Invalid CTL default:7   
ALSA lib conf.c:5000:(snd_config_expand) Unknown parameters 7           
ALSA lib pcm.c:3060:(snd_pcm_open_noupdate) Unknown PCM default:7       
ALSA lib conf.c:5000:(snd_config_expand) Unknown parameters 7           
ALSA lib pcm.c:3060:(snd_pcm_open_noupdate) Unknown PCM default:7       
```



Ubuntu上安装的默认就是3.6.1的。板端的编译得到的也是3.6.1的。

板端运行为什么会报错？

snd_config_expand 这个函数是在alsa lib力量的conf.c里。

板端单独用arecord和aplay进行录音播放都是正常的。



看linphone的官方仓库。

https://gitlab.linphone.org/BC/public/liblinphone

看buildroot里下载的路径，是在这个下面，3.9的算是比较新的。

http://download-mirror.savannah.gnu.org/releases/linphone/3.9.x/sources/

换成3.9.1的看看。

```
configure: error: Package requirements (belle-sip >= 1.4.0) were not met:
```

这个包在buildroot里没有，那就自己添加到buildroot里。

```

```

Belle-sip is a modern library implementing SIP (RFC 3261) transport, transaction and dialog layers.

编译belle-sip，又依赖了这个。

```
 Please install antlr3 version > 3.2
```

但是这个是一个java工具。

```
sudo apt-get install antlr3 
```



# 自己编译3.6.1

```
./configure --disable-video --disable-werror
```

还是有各种依赖库的版本兼容问题。

暂时不编译了。



试一下x-lite的。



1、【SIP】opensips 服务器搭建测试 2016-02-25 09:09:38

https://blog.csdn.net/jhope/article/details/53129122?utm_source=distribute.pc_relevant.none-task

2、

https://blog.csdn.net/qq_38631503/article/details/80005454

3、官方wiki

https://wiki.linphone.org/xwiki/wiki/public/view/Linphone/

4、

http://www.novell.com/zh-cn/documentation/sled10/userguide_kde_sp1/data/sec_linphone_config.html

5、freeswitch系列三     SIP软电话xlite、linphonec接入kamailio+freeswitch

这篇文章里有linphone的配置文件生成。

https://blog.csdn.net/hry2015/article/details/77484236

6、搭建SIP服务器所需资源

https://www.jianshu.com/p/dc37f6559bef

7、openips环境搭建

这个提到了mediaproxy。

https://blog.csdn.net/u011857683/article/details/78622151