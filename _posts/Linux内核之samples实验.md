---
title: Linux内核之samples实验
date: 2018-03-19 09:35:30
tags:
	- Linux内核

---



内核代码目录下有个samples目录，下面的例子都是编译成ko的。

基于的环境是我的mylinuxlab。



# 编译

1、配置。menuconfig里，kernel Hacking里，选上samples的。

2、make kernel

3、make modules。



# 例子分类

例子有比较多。我们选关键的看。

1、kobject。

2、kfifo。

其他感觉目前还不太感兴趣。

# kobject

运行效果：

```
/mnt # insmod kobject-example.ko 
/mnt # lsmod
kobject_example 16384 0 - Live 0x7f000000
/sys/kernel # cd kobject_example/
/sys/kernel/kobject_example # ls
bar  baz  foo
/sys/kernel/kobject_example # cat bar
0
/sys/kernel/kobject_example # cat baz
0
/sys/kernel/kobject_example # cat foo
0
```

可以看到是在/sys/kernel目录下生成了一个目录kobject_example。

下面有3个文件foo、bar、baz。

我用在我的hello这个模块的基础上把这个例子写一遍来熟悉代码。

我的这种模块代码，我都用xxx作为前缀。

xxx_kobject_init这样。可以上传到我自己的github上保存。



# kset

```
/sys/kernel/xxx_kset # ls
aa  bb  cc
/sys/kernel/xxx_kset # cat aa
cat: read error: Is a directory
/sys/kernel/xxx_kset # cd aa/
/sys/kernel/xxx_kset/aa # ls
aa
/sys/kernel/xxx_kset/aa # cat aa
0
/sys/kernel/xxx_kset/aa # echo 2 > aa
/sys/kernel/xxx_kset/aa # cat aa
2
/sys/kernel/xxx_kset/aa # 
```

