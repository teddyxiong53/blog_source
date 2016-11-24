---
title: linux系统里的重要文件和信息
date: 2016-11-05 10:33:36
tags:
	- linux
---
linux系统的正常运行需要使用大量与系统有关的数据文件，例如口令文件`/etc/passwd`和组文件`/etc/group`就是经常被各种程序使用的2个文件。每次使用`ls -l`都会读取口令文件的。
由于历史原因，这些文件都是文本文件，使用的是标准IO进行操作，如果一个系统上用户很多，则顺序扫描口令文件要花很长时间。所以现在就要改变为非文本文档的方式，但是为了兼容性，还是需要继续提供文本文件的接口。
#1. 口令文件
下面列出几行口令文件内容来进行分析。
```
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
teddy:x:1000:1000:teddy,,,:/home/teddy:/bin/bash
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
```
每一行的格式分析。用冒号做为字段的分隔符。一共7个字段。
用户名:密码:用户ID:组ID:用户全名:用户的主目录:用户的登陆shell


* 一定有一个root用户存在。用户ID和组ID都是0，是超级用户。
* 密码字段在以前是明文的，就写在这个文件里，太危险了。现在只是放一个x做占位符。真正的密码加密后保存在`/etc/shadow`里。
* 有些字段可以是空的。
* 有些用户不是让人用来登陆的，而是为了给某些服务用的，所以要禁止有人用这些用户名来进行登陆。解决的办法是把登陆shell字段设为/dev/null或者/bin/false或者/bin/true或者/usr/sbin/nologin。
* nobody是一个特别的用户，使得任何人都可以登陆到系统，他的用户ID和组ID是65534，只能访问所有人都可以读写的文件。
* `teddy,,,`这个是全名。完整形式是这样`名字,办公室地址,办公室电话,家庭电话`。字段可以为空。你如果用finger程序来看用户信息时，就会用到这个字段了。命令用法`finger -p teddy`。
#2. 阴影口令文件
cat /etc/shadow，截取一部分如下。
```
teddy:$6$RK5SJHnG$xmILFo3GGDC.MEEqa2Tc0Bd4df6Nlwpwv0clWuwWXetzh1/ocrPHBsfoV6h4FFT5xUEAJSdhqMC5ri.3rzY4d/:16908:0:99999:7:::
sshd:*:16959:0:99999:7:::
gitadmin:$6$TwqmXjCi$I1apIVre29zCewLsxiQOmQuZt2WRxbezWUZc3dflTJ7hX8somX7vE0QjcbXaPMbbrHrFDsF2OOmzqvon579Yn1:16959:0:99999:7:::
```
字段的格式是：
用户名:加密后的密码:最近更改密码的日期（从1970年1月1日起过的天数）:密码要过多少天才能被修改（0表示随时可以修改）:必须在指定天数内修改密码（99999表示不限制）:密码修改提前警告天数:密码过期多少天内还可以继续使用:保留字段

#3. 组文件
```
nopasswdlogin:x:127:
teddy:x:1000:
sambashare:x:128:teddy
gitadmin:x:1001:
```
格式是这样：用户名:密码:组号:用户列表。字段可以为空。
#4. 其他数据文件
```
/etc/hosts -- 就是大名鼎鼎的hosts文件，在翻墙和跳过视频广告时有用
/etc/networks --记录网络信息的文件。
/etc/protocols --主机支持的协议有哪些。
/etc/services -- 主机所提供的服务有哪些。
```

#5. 用户登录信息记录
有2个文件，utmp和wtmp。utmp记录当前登录到系统的用户有哪些。wtmp则是跟踪登录和注销事件 。
可以用cat /var/run/utmp 和cat /var/log/wtmp来查看内容。




