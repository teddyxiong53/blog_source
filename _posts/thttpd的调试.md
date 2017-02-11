---
title: thttpd的调试
date: 2017-01-10 20:06:23
tags:
	- thttpd
---
thttpd是一个小巧的web server，用c语言写的，在嵌入式领域使用很多，现在在pc上进行调试学习。
作者的简历在这里：`http://acme.com/resume.html`。是个大牛，在1993年和1996年两次获得Usenix终身成就奖，值得我等膜拜学习。维基百科的地址：`https://en.wikipedia.org/wiki/Jef_Poskanzer`。
作者的官网就是搭建在一台普通的电脑上，运行也很良好可靠。
他的twitter地址：`https://twitter.com/jef_poskanzer?lang=en`。瞄了一下，居然发了40000+条的微博。


他的用途广泛的开源代码除了thttpd，还有一个是pbmplus。

# 1. 环境准备
从thttpd官网下载最新的代码。网址是http://www.acme.com/software/thttpd/
当前最新版本是2.2.7，代码压缩包只有500K左右。
解压后先`./configure`，再make。在当前目录得到可执行文件thttpd。我们先不要用make install安装到系统目录。
直接在当前目录进行调试。

# 2. 初步运行
```
$ ./thttpd
```
这样运行，看不到任何的打印，用ps查看，对应的进程也没有起来，肯定是退出了。thttpd的错误输出是通过syslog来做的，所以在当前的shell查看看不到错误打印。
我们当前运行没有指定任何的参数，所以默认的错误输出是`/var/log/syslog`。我们可以用`tail -f /var/log/syslog`来动态地监视这个文件里新产生的内容。
从log信息里看到，是没有权限。我们切换成root用户后，再执行命令，也可以用sudo来执行。
```
# ./thttpd
```
我当前的系统80端口运行了其他的服务器，所以启动会再次失败。我们现在可以加参数来指定端口号。
```
# sudo ./thttpd -i  ./pid.txt -D -h 192.168.19.150 -p 8880 -d ./
```
这样启动就成功了，`-D`是用调试模式来启动。现在用浏览器来访问`http://192.168.19.150:8880/index.html`就可以看到效果了。
这里我有碰到一个问题，提示403错误，因为我习惯把文件权限都改成777的，所以index.html也被加上了执行权限，thttpd提示index.html不是合法的CGI文件，就报错了。把权限改成666就好了。

把index.html删掉或者改名为index.html.bak。访问`http://192.168.19.150:8880/`，则得到是当前目录的文件列表。如果文件有图片或者视频，图片可以直接点开，avi视频点击的效果则提示下载。


# 3. thttpd的一些介绍
通过上面的简单使用，我们对thttpd已经有了一个直观上的认识。
下面罗列一些从网上（主要是官网上）查询到的一些知识，后面会在针对这些知识在代码中去找实现，这样就有一个参照。


## 3.1 基于URL的流量控制
这一点官方特别进行了强调。这具体是指什么呢？在使用上是这么做的。启动thttpd的时候加上`-t throttle_file`参数，在文件里写上下面这样的内容：
```
# throttle file for www.acme.com

**              2000-100000  # limit total web usage to 2/3 of our T1,
                             # but never go below 2000 B/s
**.jpg|**.gif   50000        # limit images to 1/3 of our T1
**.mpg          20000        # and movies to even less
jef/**          20000        # jef's pages are too popular
```
这个文件的语法风格非常简单，是linux下的配置文件惯用的风格。
流量控制，就是限制某些URL的访问速度，避免占用过多的带宽。thttpd一直在持续统计阀门文件里列举的各种模式里的流量，如果发现流量超出设置值了，就返回503错误，让用户稍后再试。（这样带来了体验的下降）
限制流量和不限制流量，对于cpu的负载并没有太大的区别，主要是考虑带宽。

## 3.2 CGI支持
thttpd支持CGI 1.1的规范。
最好把cgi文件都放在同一个目录，方便进行权限控制。




# 4. 代码初步分析
我们就按main函数的流程，一个个分析碰到的值得分析的知识点。

1. `openlog( cp, LOG_NDELAY|LOG_PID, LOG_FACILITY );`
这个是打开syslog功能，第一个参数是运行的程序的名字，第二个参数的当前值，NDELAY表示马上写入不要延迟写，`LOG_PID`表示把pid也写入到log里。
2. `tzset();`
这个函数使用环境变量TZ的当前设置把值赋给3个全局变量，daylight、timezone和tzname。
```
teddy@teddy-ubuntu:~/test/thttpd-2.27/cgi-bin$ export TZ=Asia/Shanghai
teddy@teddy-ubuntu:~/test/thttpd-2.27/cgi-bin$ date
2017年 01月 10日 星期二 23:17:14 CST
teddy@teddy-ubuntu:~/test/thttpd-2.27/cgi-bin$ export TZ=Asia/Tokyo
teddy@teddy-ubuntu:~/test/thttpd-2.27/cgi-bin$ date
2017年 01月 11日 星期三 00:17:23 JST
```
3. 

# 5. thttpd的实用要点
前面的学习都是调试，如果要真正让thttpd工作起来，就要进行安装，并进行正确的配置。

# 5.1 最简单的安装
下载代码configure并且make后，就可以用make install进行安装。


