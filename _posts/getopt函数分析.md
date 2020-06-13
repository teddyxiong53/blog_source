---
title: getopt函数分析
date: 2020-06-11 14:24:08
tags:
	- Linux

---

1

getopt是标准C库里为支持命令行选项功能而提供的函数。

对应的头文件是getopt.h。

头文件提供了这些东西：

```
3个函数：
	getopt
	getopt_long
	getopt_long_only
3个宏
	no_argument 0
	required_argument 1
	optional_argument 2
1个结构体
	struct option {
		char *name;
		int has_arg;//就是上面那3个宏。
		int *flag;//基本是NULL
		int val;//短选项的ASCII码。一般是'h'这样。也可以不是。因为毕竟这样个数有限。可以使用任意整数值。
	};
1个指针
	extern char* optarg;
4个int变量
	extern int optind, opterr, optopt, optreset;
	optind：表示写一个被解析的选项的index。处初始值是1 。
```



getopt

这个是只支持单字符的选项 。

```
原型：
	int getopt(int argc, char **argv, const char *optstring);
参数：
	就3个。意思就很明显了。
返回值：
	如果找到对应的选项，返回的是对应的选项字符。例如，-h的话，就返回'h'
	如果所有选项都解析完了，返回-1 。
	如果碰到非法的选项，则返回'?'
	如果选项缺了参数，那么就要看optstring里是用什么符号来分割的，如果是用':'分割，就返回':'，否则返回'?'
	
```

getopt_long

这支持短选项和长选项。

```
原型：
	int getopt_long(int argc, char * const argv[],
                  const char *optstring,
                  const struct option *longopts, int *longindex);
参数1
参数2：
	参数个数和参数值。
参数3：
	短选项字符串。
参数4：
	长选项字符串。
参数5：
	长选项的index。
	可以给NULL。
```



典型使用：

```
const char *opts = "hVvi:d:";
const struct option longopts[] = {
	{"help", no_argument, NULL, 'h'},
	{"version", no_argument, NULL, 'V'},
	{"verbose", no_argument, NULL, 'v'},
	{"hci", requried_argument, NULL, 'i'},
	{"pcm", required_argument, NULL, 'd'},
	{"pcm-buffer-time", required_argument, NULL, 3},
	{0,0,0,0}
};
int opt;
while((opt = getopt_long(argc, argv, opts, longopts, NULL)) != -1) {
	switch(opt) {
	case 'h':
		//
	case 3://"pcm-buffer-time"
		//
		
	}
}
if(opt == argc ) {
	goto usage;//这个说明解析错误。
}

```

