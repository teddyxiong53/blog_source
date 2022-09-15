---
title: Linux之patch
date: 2019-05-16 14:38:11
tags:
	- Linux

---



需要用到2个命令：

1、diff。

2、patch。



# 单个文件补丁

生成补丁：

```
diff -uN v1/1.c v2/1.c > xx.patch
```



我们进行测试看看。

```
hlxiong@hlxiong-VirtualBox:~/work/test/patch$ tree
.
├── v1
│   └── 1.c
├── v2
│   └── 1.c
```

新建v1和v2这2个目录，下面就放1.c这个一个文件。

v1里的1.c这么写：

```
void func(int a) {
    printf("val:%d\n", a);
}
```

v2里的1.c这么写：（我在printf那一行增加了一个空格）

```
#include <stdio.h>
void func(int a) {
    printf("val:%d\n",  a);
}
```

用命令生成：

```
diff -uN v1/1.c v2/1.c > xx.patch
```

查看xx.patch文件：

```
hlxiong@hlxiong-VirtualBox:~/work/test/patch$ cat xx.patch 
--- v1/1.c      2019-05-17 14:43:40.935622788 +0800
+++ v2/1.c      2019-05-17 14:44:09.068062966 +0800
@@ -1,3 +1,5 @@
+#include <stdio.h>
 void func(int a) {
-    printf("val:%d\n", a);
+    printf("val:%d\n",  a);
 }
+
```

补丁文件的格式是这样：

```
补丁头
	最上面两行。
	分别是---和+++开头。
	表示要打补丁的文件。
	---开头的表示旧文件。
	+++开头的表示新文件。
	如果补丁是针对目录的补丁，则会有多个补丁头。
	
块
	块是以@@开头的部分。结束是下一个补丁头的前面。
	-1,3 +1,5 的意思是：
	块下面的每一行，会有三种可能开头：
	+、-、空格。
	+表示增加的。
	-表示删除的。
	空格表示没有改变的。
```

看看怎么打补丁。

```
hlxiong@hlxiong-VirtualBox:~/work/test/patch$ patch -p0 < xx.patch 
patching file v1/1.c
```

补丁的还原：

再执行一次这个命令就可以。会提示你是否还原，输入y就好。

```
patch -p0 < xx.patch 
```

这样会在v1目录下生成一个1.c.orig文件。内容是改后的。

```
hlxiong@hlxiong-VirtualBox:~/work/test/patch$ patch -p0 < xx.patch 
patching file v1/1.c
Reversed (or previously applied) patch detected!  Assume -R? [n] y
hlxiong@hlxiong-VirtualBox:~/work/test/patch$ ls
v1  v2  xx.patch
hlxiong@hlxiong-VirtualBox:~/work/test/patch$ cd v1
hlxiong@hlxiong-VirtualBox:~/work/test/patch/v1$ ls
1.c  1.c.orig
```





-p0是什么意思？

-pN表示跳过N层目录。

因为我们是在当前目录下生成的patch文件，也是在当前目录下执行patch命令。

所以-p0就可以了。一般我们都用p0就可以了。不要切到目录下面去。

我们如果到v1目录下去执行patch命令的话。

```
hlxiong@hlxiong-VirtualBox:~/work/test/patch/v1$ patch -p1 < ../xx.patch 
patching file 1.c
```



# 文件夹补丁

在上面的基础上，在v2目录下，新建2.c文件。

```
hlxiong@hlxiong-VirtualBox:~/work/test/patch$ tree
.
├── v1
│   └── 1.c
├── v2
│   ├── 1.c
│   └── 2.c
```

2.c的内容：

```
void func2() {

}
```



生成补丁：

```
diff -auNr v1 v2 > xx.patch
```

补丁内容：

```
diff -auNr v1/1.c v2/1.c
--- v1/1.c      2019-05-17 15:06:23.356912571 +0800
+++ v2/1.c      2019-05-17 14:44:09.068062966 +0800
@@ -1,3 +1,5 @@
+#include <stdio.h>
 void func(int a) {
-    printf("val:%d\n", a);
+    printf("val:%d\n",  a);
 }
+
diff -auNr v1/2.c v2/2.c
--- v1/2.c      1970-01-01 08:00:00.000000000 +0800
+++ v2/2.c      2019-05-17 15:07:28.462326911 +0800
@@ -0,0 +1,3 @@
+void func2() {
+
+}
```

我应用补丁，为什么是把2/2.c给删掉了呢？

这个就必须进入到v1目录下去执行了。

```
hlxiong@hlxiong-VirtualBox:~/work/test/patch$ diff -auNr v1 v2 > xx.patch
hlxiong@hlxiong-VirtualBox:~/work/test/patch$ cd v1
hlxiong@hlxiong-VirtualBox:~/work/test/patch/v1$ patch -p1 < ../xx.patch 
patching file 2.c
hlxiong@hlxiong-VirtualBox:~/work/test/patch/v1$ ls
1.c  2.c
```







# 参考资料

1、补丁(patch)的制作与应用

http://linux-wiki.cn/wiki/zh-hans/%E8%A1%A5%E4%B8%81(patch)%E7%9A%84%E5%88%B6%E4%BD%9C%E4%B8%8E%E5%BA%94%E7%94%A8

2、linux patch 命令小结

https://blog.csdn.net/wh_19910525/article/details/7515540