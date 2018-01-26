---
title: alpine（一）常用命令
date: 2018-01-26 14:49:26
tags:
	- alpine
	- Linux

---



现在看看alpine的基本使用。

https://wiki.alpinelinux.org/wiki/Tutorials_and_Howtos

这篇文章写得非常详尽了。



# apk

apk是alpine的包管理软件。

```
#1. 安装
apk add --update xxx
#2. 卸载
apk del xxx
#3. 搜索
apk search xxx
#4. 更新，update 和upgrade也是可以用的。

```

够用了。

软件包是用tar.gz的压缩包的格式存储的。包括程序、配置文件、依赖metadata。扩展名字是apk。

一个仓库就是很多apk的集合。

仓库的索引文件是APKINDEX.tar.gz。一个目录包含了这个文件，才能被认为是一个仓库。

apk工具可以从多个仓库安装软件。

配置仓库地址的文件是：

```
vm-alpine-0:/etc/apk# cat repositories 
#/media/cdrom/apks
http://dl-cdn.alpinelinux.org/alpine/v3.7/main
#http://dl-cdn.alpinelinux.org/alpine/v3.7/community
#http://dl-cdn.alpinelinux.org/alpine/edge/main
#http://dl-cdn.alpinelinux.org/alpine/edge/community
#http://dl-cdn.alpinelinux.org/alpine/edge/testing

http://dl-cdn.alpinelinux.org/alpine/v3.7/main
#http://dl-cdn.alpinelinux.org/alpine/v3.7/community
#http://dl-cdn.alpinelinux.org/alpine/edge/main
#http://dl-cdn.alpinelinux.org/alpine/edge/community
#http://dl-cdn.alpinelinux.org/alpine/edge/testing

http://dl-cdn.alpinelinux.org/alpine/v3.7/main
#http://dl-cdn.alpinelinux.org/alpine/v3.7/community
#http://dl-cdn.alpinelinux.org/alpine/edge/main
#http://dl-cdn.alpinelinux.org/alpine/edge/community
#http://dl-cdn.alpinelinux.org/alpine/edge/testing

http://dl-cdn.alpinelinux.org/alpine/v3.7/main
#http://dl-cdn.alpinelinux.org/alpine/v3.7/community
#http://dl-cdn.alpinelinux.org/alpine/edge/main
#http://dl-cdn.alpinelinux.org/alpine/edge/community
#http://dl-cdn.alpinelinux.org/alpine/edge/testing
```

本地缓存：

```
vm-alpine-0:/var/cache/apk# tree
.
├── APKINDEX.70c88391.tar.gz
├── alpine-mirrors-3.5.6-r0.8d1fdd02.apk
├── installed
├── openssh-7.5_p1-r8.88dad8a1.apk
├── openssh-client-7.5_p1-r8.d31298cd.apk
├── openssh-keygen-7.5_p1-r8.306e94f1.apk
├── openssh-server-7.5_p1-r8.73feab0f.apk
├── openssh-server-common-7.5_p1-r8.cdeb5d9b.apk
├── openssh-sftp-server-7.5_p1-r8.deb7e718.apk
└── tree-1.7.0-r1.ee603c38.apk

0 directories, 10 files
```

# setup系列脚本

这些脚本放在/sbin目录下。



# 用户查看

```
vm-alpine-0:/usr/share/webapps# cat /etc/passwd
root:x:0:0:root:/root:/bin/ash
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
adm:x:3:4:adm:/var/adm:/sbin/nologin
lp:x:4:7:lp:/var/spool/lpd:/sbin/nologin
sync:x:5:0:sync:/sbin:/bin/sync
shutdown:x:6:0:shutdown:/sbin:/sbin/shutdown
halt:x:7:0:halt:/sbin:/sbin/halt
mail:x:8:12:mail:/var/spool/mail:/sbin/nologin
news:x:9:13:news:/usr/lib/news:/sbin/nologin
uucp:x:10:14:uucp:/var/spool/uucppublic:/sbin/nologin
operator:x:11:0:operator:/root:/bin/sh
man:x:13:15:man:/usr/man:/sbin/nologin
postmaster:x:14:12:postmaster:/var/spool/mail:/sbin/nologin
cron:x:16:16:cron:/var/spool/cron:/sbin/nologin
ftp:x:21:21::/var/lib/ftp:/sbin/nologin
sshd:x:22:22:sshd:/dev/null:/sbin/nologin
at:x:25:25:at:/var/spool/cron/atjobs:/sbin/nologin
squid:x:31:31:Squid:/var/cache/squid:/sbin/nologin
xfs:x:33:33:X Font Server:/etc/X11/fs:/sbin/nologin
games:x:35:35:games:/usr/games:/sbin/nologin
postgres:x:70:70::/var/lib/postgresql:/bin/sh
cyrus:x:85:12::/usr/cyrus:/sbin/nologin
vpopmail:x:89:89::/var/vpopmail:/sbin/nologin
ntp:x:123:123:NTP:/var/empty:/sbin/nologin
smmsp:x:209:209:smmsp:/var/spool/mqueue:/sbin/nologin
guest:x:405:100:guest:/dev/null:/sbin/nologin
nobody:x:65534:65534:nobody:/:/sbin/nologin
chrony:x:100:101:chrony:/var/log/chrony:/sbin/nologin
lighttpd:x:101:102:lighttpd:/var/www/localhost/htdocs:/sbin/nologin
mysql:x:102:103:mysql:/var/lib/mysql:/sbin/nologin
```

