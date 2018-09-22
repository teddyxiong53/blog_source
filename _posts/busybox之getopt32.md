---
title: busybox之getopt32
date: 2018-09-22 13:58:17
tags:
	- Linux

---



原型是：

```
u32 getopt32(char **argv, const char *applet_opts, ...);
```

使用举例：

```
u32 flags = getopt32(argv, "rnug");
```

这样导致的结果是：字母r是设置flags的bit0，n设置flags的bit1，以次类推。

getopt32函数返回的时候，会把全局变量optind设置值。

这样你就可以这样操作：

```
argc -= optind;
argv += optind;
```

如果某个选项后面需要带参数，则在字母后面加上“:”.

```
char *pointer_to_arg_for_a;
char *pointer_to_arg_for_b;
char *pointer_to_arg_for_c;
char *pointer_to_arg_for_d;
flags = getopt32(argv, "a:b:c:d:", &pointer_to_arg_for_a,&pointer_to_arg_for_b, &pointer_to_arg_for_c, &pointer_to_arg_for_d);
```

如果某个选项后面的参数是可选的，就带上“::”。

```
-oparam 而不是-o param（中间不能有空格）。
```



还有一个长选项的版本。

```
u32 getopt32long(char **argv, char *applet_opts, ...);
```

使用举例：

```
char applet_longopts[] = 
	"verbose\0" No_argument "v";
```

格式是：

```
"name\0" has_arg val
```



