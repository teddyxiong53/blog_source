---
title: menuconfig代码分析
date: 2022-12-07 17:36:19
tags:
	- C语言

---

--

menuconfig经常用，但是改得比较少。

现在看toybox的代码。觉得有必要把menuconfig连同Kconfig这一套一起梳理一下。

这个是从linux kernel里扒出来的。

```
teddy@teddy-VirtualBox:~/work/test/toybox-0.8.8/kconfig$ tree 
.
├── android_miniconfig
├── conf.c
├── confdata.c
├── expr.c
├── expr.h
├── freebsd_miniconfig
├── kconfig-language.txt
├── lex.zconf.c -> lex.zconf.c_shipped
├── lex.zconf.c_shipped
├── lkc.h
├── lkc_proto.h
├── lxdialog
│   ├── BIG.FAT.WARNING
│   ├── checklist.c
│   ├── check-lxdialog.sh
│   ├── dialog.h
│   ├── inputbox.c
│   ├── menubox.c
│   ├── textbox.c
│   ├── util.c
│   └── yesno.c
├── macos_miniconfig
├── Makefile
├── mconf.c
├── menu.c
├── README
├── symbol.c
├── util.c
├── zconf.hash.c -> zconf.hash.c_shipped
├── zconf.hash.c_shipped
├── zconf.tab.c -> zconf.tab.c_shipped
└── zconf.tab.c_shipped
```

conf.c会编译出conf文件。

mconf.c会编译出mconf文件。

看这里的Makefile。

kconfig的语法这里有官方文档，看这个就够了。不用到处去找了。

kconfig\kconfig-language.txt

生成mconf的编译规则：

```
kconfig/mconf: kconfig/zconf.tab.c kconfig/lex.zconf.c kconfig/zconf.hash.c
	$(HOSTCC) -o $@ kconfig/mconf.c kconfig/zconf.tab.c \
		kconfig/lxdialog/*.c -lcurses
```

生成conf的编译规则：

```
kconfig/conf: kconfig/zconf.tab.c kconfig/lex.zconf.c kconfig/zconf.hash.c
	$(HOSTCC) -o $@ kconfig/conf.c kconfig/zconf.tab.c
```

generated/Config.in的生成

```
generated/Config.in: toys/*/*.c scripts/genconfig.sh
	scripts/genconfig.sh
```

所以要看scripts/genconfig.sh做了什么。

generated/Config.in就是把各种帮助信息都提取放进来了。

```
for i in $(ls -1 $DIR/*.c)
    do
      # Grab the config block for Config.in
      echo "# $i"
      $SED -n '/^\*\//q;/^config [A-Z]/,$p' $i || return 1
      echo
    done
```

我手动对一个文件进行展开看看。

```
teddy@teddy-VirtualBox:~/work/test/toybox-0.8.8$ sed -n '/^\*\//q;/^config [A-Z]/,$p' toys/lsb/dmesg.c
config DMESG
  bool "dmesg"
  default y
  help
    usage: dmesg [-Cc] [-r|-t|-T] [-n LEVEL] [-s SIZE] [-w]

    Print or control the kernel ring buffer.

    -C  Clear ring buffer without printing
    -c  Clear ring buffer after printing
    -n  Set kernel logging LEVEL (1-9)
    -r  Raw output (with <level markers>)
    -S  Use syslog(2) rather than /dev/kmsg
    -s  Show the last SIZE many bytes
    -T  Human readable timestamps
    -t  Don't print timestamps
    -w  Keep waiting for more output (aka --follow)
```

编译的语句是这个：

```
toybox generated/unstripped/toybox: $(KCONFIG_CONFIG) *.[ch] lib/*.[ch] toys/*/*.c scripts/*.sh Config.in
	scripts/make.sh
```

所以要看make.sh这个脚本。

这一套做法还是非常晦涩难懂的。

涉及到太多的命令了。

menuconfig这一套逻辑，有没有更现代的方式来做？

scons有没有办法做menuconfig这样的操作？

有没有办法基于json来做这一套配置？

这个global是怎么生成的？因为默认的toys.h里，这个是展开后什么都没有的。

```
GLOBALS(
  int unused;
)
```

看make.sh里，有这个：

```
function getglobals()
{
  for i in toys/*/*.c
  do
    # alas basename -s isn't in posix yet.
    NAME="$(echo $i | $SED 's@.*/\(.*\)\.c@\1@')"
    DATA="$($SED -n -e '/^GLOBALS(/,/^)/b got;b;:got' \
            -e 's/^GLOBALS(/_data {/' \
            -e 's/^)/};/' -e 'p' $i)"
    [ -n "$DATA" ] && echo -e "// $i\n\nstruct $NAME$DATA\n"
  done
}
```

手动执行这些命令看看效果。

```
echo toys/lsb/dmesg.c | sed 's@.*/\(.*\)\.c@\1@'
```

这个得到的就是dmesg这个字符串。

```
sed -n -e '/^GLOBALS(/,/^)/b got;b;:got' \
            -e 's/^GLOBALS(/_data {/' \
            -e 's/^)/};/' -e 'p' toys/lsb/dmesg.c
```

这个得到的是：

```
_data {
  long n, s;

  int use_color;
  time_t tea;
};
```

最后拼接得到的是：

```
struct dmesg_data {
  long n, s;

  int use_color;
  time_t tea;
};
```

最后还有一个步骤，就是定义一个变量，叫this。

```
extern union global_union {
	struct log_data log;
	struct demo_number_data demo_number;
	struct hello_data hello;
	//...
};
union global_union this;
```

然后这里的TT

```
void dmesg_main(void)
{
  TT.use_color = isatty(1);
```

是在generated\flags.h里生成的。

```
#ifdef FOR_dmesg
#define CLEANUP_dmesg
#ifndef TT
#define TT this.dmesg
#endif
```

这样整个流程都理顺了。



参考资料

1、

