---
title: busybox之usage生成过程分析
date: 2018-03-21 13:59:35
tags:
	- busybox

---



busybox的usage信息是如何生成的？

这个过程有点绕，一下子看不出来。现在我慢慢分析一遍。

最后实现的地方，是include/usage.h里。

这里已经是成型的宏定义了。例如这样：

```
#define xzcat_trivial_usage \
       "[FILE]..." \

#define xzcat_full_usage "\n\n" \
       "Decompress to stdout" \
```

但是搜索不到那里引用了这个东西。

```
teddy@teddy-ubuntu:~/work/mylinuxlab/busybox/busybox-1.27.2$ grep -nwr "xzcat_full_usage" .
./include/usage.h:131:#define xzcat_full_usage "\n\n" \
./archival/bbunzip.c:580://usage:#define xzcat_full_usage "\n\n"
```

因为不是直接用的。

看applets/usage.c里。

```
#define MAKE_USAGE(aname, usage) { aname, usage },
static struct usage_data {
	const char *aname;
	const char *usage;
} usage_array[] = {
#include "applets.h"
};
```

这个相当于得到了一个数组。

```
name    help
xxx      xxx_help(这里简单帮助和详细帮助是挨着放的，用一个指针访问)
...
```

查找help具体信息，都是在usage_array这个数组里去找的。

usage.c，还有一个类似的usage_pod.c。

都是2个独立的进程。是在pc上执行的，用来处理帮助信息的。

编译过程中，把帮助信息，写入在docs/busybox.pod文件里。

我加的那个打印信息，也被输出到这里了。这个是usage_pod.c输出的。

```
Currently available applets include:

xhl -- func:main, line:53 
	[, [[, acpid, add-shell, addgroup, adduser, adjtimex, arp, arping,
	ash, awk, base64, basename, beep, blkdiscard, blkid, blockdev,
```

下面就是完整帮助信息。

每一条的格式是这样的：

```
=item B<adduser>

adduser [OPTIONS] USER [GROUP]

Create new user, or add USER to GROUP

	-h DIR		Home directory
	-g GECOS	GECOS field
	-s SHELL	Login shell
	-G GRP		Group
	-S		Create a system user
	-D		Don't assign a password
	-H		Don't create home directory
	-u UID		User id
	-k SKEL		Skeleton directory (/etc/skel)
```

所有命令的help信息是统一处理的。

bb_show_usage这个函数。

帮助信息还是被压缩的，因为有很多的空格，其实压缩空间还是很大的。

每次都是把所有信息都解压。

显示帮助信息的过程就是这样的。

那么帮助的最原始的地方写在哪里？

就是usage.h里的信息从哪里来。

是靠scripts/gen_build_files.sh把每个c文件里的这些注释部分提取出来。

```
//usage:#define ls_trivial_usage
//usage:	"[-1AaCxd"
```

以`//usage:`开头的注释。

所以，你要加注释信息，就是加在你的命令C文件里。按照这种格式来写就好了。

不过，你一般不用在busybox里加自己的命令。因为你可以写普通的用户态程序。

busybox里添加，反而很多限制。

