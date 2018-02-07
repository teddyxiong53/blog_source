---
title: LFS了解
date: 2018-02-07 15:43:59
tags:
	- Linux

---



LFS是指Linux From Scratch。是指从源代码开始编译搭建一整套的linux系统。

这个概念很早接触到了，但是一直没有想去弄。因为下载代码太多，而且按照国内这网络环境下载速度不会快。

但是现在我有兴致了。但是还是不打算动手。先把文档过一遍。

我希望搭建的是一个小型，但是带完整包管理系统的linux系统。像alpine那样。



# 1.遵循的标准

1、posix.1-2008 。

2、文件系统层次标准。FHS。

3、linux标准基础。LSB。

```
LSB有5个独立的标准：
1、内核。
2、C++。
3、桌面。
4、运行时语言。
5、输出。
```

LFS网站为了大家能够更加方便的进行搭建，给大家提供了这些满足LSB要求的软件包：

1、内核相关。

```
bash
bc
binutils
coreutils
diffutils
file
findutils
gawk
grep
gzip
m4
man-db
ncurses
procps
psmisc
sed
shadow
tar
util-linux
zlib
```

2、C++。

就一个gcc。

3、LSB运行时语言。

就一个perl。

4、LSB输出。

没有。



另外，还有一个组织，叫BLFS，就是Beyond Linux From Scratch。

他们提供个软件包有：

1、内核。

```
at
batch
cpio
ed
fcrontab
initd-tools
lsb_release
pam
pax
sendmail
time
```

2、C++。

没有。

3、LSB桌面。

```
atk
cario
desktop-file-utils
freetype
fontconfig
glib2
gtk+2
icon-naming-utils
libjpeg
libpng
libxml2
mesalib
pango
qt4
xorg
```

3、LSB运行时语言。

Python。

4、LSB输出。

CUPS。

5、LSB多媒体。

```
alsa libraries
nspr
nss
openssl
java
xdg-utils
```

# 2. 选用软件包的理由

LFS构建处理的系统，不是最小的系统。而是一个完整系统。

下面列出为什么选用这些软件的理由。

1、acl。

访问控制列表。定义文件和目录的访问权限。

2、attr。

管理文件系统的属性。

3、autoconf。

4、automake。

5、bc。

构建linux内核需要这个。

6、binutils。

包括了链接器、汇编器等。

7、bison。

包含了yacc的gnu版本。

8、bzip2

9、check。

临时用。

10、coreutils。

文件管理核心命令集合。

11、d-bus。

提供消息总线。systemd依赖了它。

12、dejagnu。

临时用。测试其他程序的。

13、diffutils。

14、e2fsprogs。

处理ext文件系统的工具。

15、expat。一个xml解析工具。

16、expect。

17、file。

18、findutils。

19、flex。

20、gawk。

21、gcc。

22、gdbm。gnu数据库管理。man-db依赖了它。

23、gettext。国际化要用到的。

24、gmp。提供任意精度数值运算的数学库。编译gcc会用到它。

25、gperf。systemd依赖了它。

26、grep。

27、groff。格式化文本的工具。man的内容就是它格式化的。

28、grub。

29、gzip。

30、iana-etc。提供了网络服务和协议的数据。

31、inetutils。

32、intltool。

33、iproute2。

34、kbd。包含了键盘映射文件。

35、kmod。

36、less。

37、libcap。posix相关。

38、libpipeline。man-db依赖了它。

39、libtool。gnu通用库支持脚本。

40、linux kernel。

41、m4。文本宏处理器。

42、make。

43、man-db。

44、man-pages。

45、mpc。

46、mpfr。

47、ncurses。

48、patch。

49、perl。

50、pkg-config。

51、procps-ng。

52、psmisc。

53、readline。

54、sed。

55、shadow。

56、systemd。

57、tar。

58、tcl。

59、texinfo。

60、util-linux。

61、vim。

62、xml::parser

63、xz utils。

64、zlib。

# 3. 宿主机的要求





