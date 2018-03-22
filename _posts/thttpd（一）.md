---
title: thttpd（一）
date: 2018-03-22 10:40:21
tags:
	- thttpd

---



现在要在我的mylinuxlab上运行thttpd。

1、配置。

```
./configure  --build=x86_64-ubuntu-linux --host=arm-linux-gnueabihf CC=arm-linux-gnueabihf-gcc
```

其实没用。这里有问题。

我还是手动到生成的Makefile里把CC改成arm-linux-gnueabihf-gcc，改一个地方就好。然后重新编译。

2、拷贝运行。

```
/mnt/thttpd/tinyhttpd # ./thttpd
./thttpd: unknown user - 'nobody'
```

看看是哪里要求nobody。

是默认的user就是配置为nobody的。

看看树莓派上的nobody是什么情况。

```
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
```

加上，重启mylinuxlab，再运行就正常了。

# thttpd配置项

```
/mnt/thttpd/tinyhttpd # ./thttpd -h
usage:  ./thttpd [-C configfile] [-p port] [-d dir] [-r|-nor] [-dd data_dir] [-s|-nos] [-v|-nov] [-g|-nog] [-u user] [-c cgipat] [-t throttles] [-h host] [-l logfile] [-i pidfile] [-T charset] [-P P3P] [-M maxage] [-V] [-D]
```

```
1、-C 配置文件。
2、-p 端口号。默认80 。
3、-d 就是html文件放的文件夹。默认是当前目录。
4、-r chroot。
5、-nor 就是不用chroot
6、-dd 数据目录。这个是没有chroot的时候用。跟-d那个是一样的效果。
7、-s 检查软链接
8、-nos。不要检查软链接。
9、-v vhost打开。
10、-nov vhost别打开。
11、-g 全局密码。
12、-nog 不要全局密码。
13、-u 指定user。默认是nobody。
14、-c 指定cgi pattern。
15、-t 阈值。
16、-h 指定hostname
17、-l 指定log文件。可以指定为-，表示就在stdout输出。
18、-i 指定pid文件。
19、-T 指定字符集。
20、-P P3P（不知道是啥）
21、-M max age
22、-V 打印版本。
23、-D debug模式运行。
```

指定选项比较麻烦。我们就写成配置文件吧。

一个简单的配置文件是这样：

```
# open debug mode
debug
dir=/var/www/html
chroot
user=nobody
port=80
logfile=/var/log/thttpd.log
pidfile=/var/run/thttpd.pid
```

保存/etc/thttpd.conf文件。

重新运行。

提示没有/var/run目录。新建。

这样在这个目录下回自动生成utmp文件。

然后syslogd.pid也会生成。

看log文件。

```
/var/log # cat thttpd.log 
192.168.0.1 - - [22/Mar/2018:03:36:35 +0000] "GET / HTTP/1.1" 200 311 "" "curl/7.47.0"
```











