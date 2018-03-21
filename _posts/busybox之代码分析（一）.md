---
title: busybox之代码分析（一）
date: 2018-03-21 14:45:12
tags:
	- busybox

---



这个写成系列文章。



busybox的执行的入口位置是libbb/appletlib.c的main函数。
我们在这个函数的最前面加上打印：

```
int i=0;
for(i=0;i<argc; i++)
{
    printf("xhl -- argv[%d]:%s \n", i,argv[i]);
}
```

运行效果是这样：

```
populate the dev dir...
 xhl -- argv[0]:/bin/busybox 
 xhl -- argv[1]:mdev 
 xhl -- argv[2]:-s 
drop to shell...
 xhl -- argv[0]:/bin/busybox 
 xhl -- argv[1]:sh 
sh: can't access tty; job control turned off
/ # input: ImExPS/2 Generic Explorer Mouse as /devices/fpga:07/serio1/input/input2

/ # ls
 xhl -- argv[0]:ls 

/ # pwd
/
/ # cc
sh: cc: not found
/ # vi 
 xhl -- argv[0]:vi 
```

可以看到有的命令进入到这个入口了，而pwd却没有进到这个入口。
busybox里的命令分为3种，我们以ls、pwd、arp这3条命令为例进行分析。

```
 IF_LS(APPLET_NOEXEC(ls, ls, BB_DIR_BIN, BB_SUID_DROP, ls))
 IF_PWD(APPLET_NOFORK(pwd, pwd, BB_DIR_BIN, BB_SUID_DROP, pwd))
 IF_ARP(APPLET(arp, BB_DIR_SBIN, BB_SUID_DROP))
```

`APPLET`由busybox创建子进程。
`APPLET_NOEXEC`由fork来创建子进程。
`APPLET_NOFORK`不创建子进程，只调用相关函数，相当于buildin的。效率最高。在linux里fork和exec是很耗时的。
buildin的命令在busybox/shell/ash.c里。

```
static const struct builtincmd builtintab[] = {
	{ BUILTIN_SPEC_REG      "."       , dotcmd     },
	{ BUILTIN_SPEC_REG      ":"       , truecmd    },
```

定义为builtincmd，不能用tab键进行补全。

有的也被定义为APPLET_NOFORK，但是不是builtincmd。例如basename。

他们的定义是这样的：

```
# define APPLET(name,l,s)                    { #name, #name, l, s },
# define APPLET_ODDNAME(name,main,l,s,help)  { #name, #main, l, s },
# define APPLET_NOEXEC(name,main,l,s,help)   { #name, #main, l, s, 1 },
# define APPLET_NOFORK(name,main,l,s,help)   { #name, #main, l, s, 1, 1 },
```

对应的结构体定义是：

```
struct bb_applet {
	const char *name;
	const char *main;
	enum bb_install_loc_t install_loc;
	enum bb_suid_t need_suid;
	//前面4个成员都是一样的。下面2个，就是2个标志。
	unsigned char noexec;
	unsigned char nofork;
};
```

noexec和nofork，这2个都可以通过配置项来关闭。

所以是可有可无的东西。不是关键性的东西。

用途在这里：

```
spawn_and_wait(char **argv)//有些命令的xxx_main函数会调用到这里。
	if (APPLET_IS_NOFORK(a))
			return run_nofork_applet(a, argv);
	if (APPLET_IS_NOEXEC(a)) {
			fflush_all();
			run_applet_no_and_exit(a, argv[0], argv);
	rc = spawn(argv);//可以都走到。如果什么两个特性被关闭的话。
```



下面分析一下入口的main函数。

```
{
	1、lbb_prepare。就取得错误码。
	2、从argv[0]得到applet_name。
	3、解析/etc/busybox.conf文件，一般没有这个文件。
	4、run_applet_and_exit(applet_name, argv);
	{
		1、看是否以busybox开头的。是，则执行busybox_main。例如busybox --install -s
		2、find_applet_by_name
		3、run_applet_no_and_exit
	}
}
```



下面分析一下basename.c这个文件的内容，看一个简单的命令的实现。

```
int basename_main(int argc, char **argv)
{
    if(argv[1] && strcmp(argv1[1],"--") == ) {
        argv++;
        argc--;
    }
    if(argc-2 >=2) {
        bb_show_usage();
    }
    char *s = xxxx;//str process
    m = strlen(s);
    s[m++]="\n";
    int ret = full_write(STDOUT_FILENO, s, m) ;
    if(ret != m) {
        return 1;//fail
    } else {
        return 0;
    }
}
```

很简单，跟我们写普通的用户态程序基本没有区别。







