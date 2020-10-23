---
title: vlc（1）
date: 2019-12-27 13:28:08
tags:
	- 音频

---

1

vlc是VideoLan Client的缩写。

Ubuntu默认安装的2.2.2版本。也算比较新的版本。

vlc还集成了服务器功能。可以做流媒体服务器。

vlc最强大的功能就是流媒体相关功能。

采用多线程并行解码架构。

vlc播放一个视频分为4个步骤：

1、access。

2、demux

3、decode

4、output。



vlc可以处理的流类型有：

1、es。ElementaryStream。

2、ps。ProgramStream。

3、ts。TransportStream。

cvlc，只是对vlc的命令行一个简单包装，是一个脚本，里面就一行代码：

```
exec /usr/bin/vlc -I "dummy" "$@"
```



选项

```
--xx：全局的，多字母选项。
-x：全局的，单字母选项。
:x：以冒号开头的，之对流起作用。
```

支持的url：

```
file:///path/file
http://host:port/file
ftp://host:port/file
mms://host:port/file
screen://  屏幕捕获
dvd://device
vcd://device
cdda://device
udp://src@bind_addr:port

```

```
--audio, --no-audio
--no-interact
	不用启动界面。
```



## 播放器查看日志的方法

不需要去找文件，直接点击菜单：视图-- 添加 -- 控制台。

就会弹出cmd窗口，里面就实时有日志。

## vlc播放搭建rtsp服务

依次点击菜单：

媒体 -- 流 -- 添加一个mp3文件 -- 然后根据情况选择需要的东西。后面的提示比较明显了。



## 用vlc把m3u8流下载成mp4文件

https://blog.csdn.net/saddyyun/article/details/85245135



## 代码编译



代码是vlc-3.0.4的。

执行configure。

```
configure: WARNING: No package 'lua5.2' found, trying lua 5.1 instead
checking for LUA... no
configure: WARNING: No package 'lua5.1' found, trying lua >= 5.1 instead
checking for LUA... no
configure: WARNING: No package 'lua' found, trying manual detection instead
```

当前安装的lua是5.3的。

安装5.2版本的。

```
sudo apt-get install lua5.2 lua5.2-dev
```

现在继续报错。

```
configure: error: Could not find liba52 on your system:
```

安装这个库。

```
 sudo apt-get install liba52-0.7.4-dev
```

还报错。

```
configure: error: Package requirements (xcb-composite) were not met:
```



```
sudo apt-get install libxcb-composite0-dev 
```

```
configure: error: Package requirements (xcb-xv >= 1.1.90.1) were not met:
```

现在configure通过了。

make出错了。是PIC问题。

重新configure。

```
./configure --with-pic
```

```
configure: error: Could not find liba52 on your system: you may get it from http://liba52.sf.net/. Alternatively you can use --disable-a52 to disable the a52 plugin.
```

```
./configure --with-pic --disable-a52
```

继续报错。

```
No package 'xcb-composite' found
```



```
sudo apt-get install libxcb-composite0-dev libxcb-glx0-dev libxcb-dri2-0-dev libxcb-xf86dri0-dev libxcb-xinerama0-dev libxcb-render-util0-dev libxcb-xv0-dev
```

报错

```
configure: WARNING: Library libchromaprint >= 0.6.0 needed for chromaprint was not found
checking for protoc... no
checking for CHROMECAST... yes
configure: error: protoc compiler needed for chromecast was not found
```

遇到这个问题的时候，可以在./configure后面加上–disable-chromecast.在这里能这样做

现在这样配置：

```
./configure --with-pic --disable-a52 --disable-chromecast
```

这样configure就成功了。

编译报错。

```
/usr/bin/ld: /usr/local/lib/libavformat.a(allformats.o): relocation R_X86_64_32 against `.bss' can not be used when making a shared object; recompile with -fPIC
/usr/local/lib/libavformat.a: error adding symbols: Bad value
collect2: error: ld returned 1 exit status
```

那就不能with-pic。

这样配置：

```
./configure  --disable-a52 --disable-chromecast
```

还是不行。

可能是我的ffmpeg安装有问题。

我重新编译安装ffmpeg。



## 代码目录分析

```
teddy@thinkpad:~/work/vlc/vlc-3.0.4$ tree -L 1 -d
.
├── autotools
├── bin  vlc等工具的入口代码。
├── compat 一些函数的封装。
├── contrib 
├── doc
├── extras
├── include
├── lib
├── m4
├── modules
├── po
├── share
├── src
└── test
```



参考资料

1、请问一下vlc player如何查看log日志文件？

https://zhidao.baidu.com/question/197995350001691165.html

2、Windows上通过VLC播放器搭建rtsp流媒体测试地址操作步骤

https://blog.csdn.net/fengbingchun/article/details/90450017

3、怎么用VLC播放器将m3u8链接视频下载到本地

https://blog.csdn.net/saddyyun/article/details/85245135

4、Compiling VLC on Linux: Error couldnt find Lua

https://stackoverflow.com/questions/9925363/compiling-vlc-on-linux-error-couldnt-find-lua

5、

https://blog.csdn.net/c_guolin/article/details/38537687