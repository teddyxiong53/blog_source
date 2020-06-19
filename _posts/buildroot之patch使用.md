---
title: buildroot之patch使用
date: 2020-03-19 09:34:11
tags:
	- buildroot
---

1

现在需要对snapcast的代码进行一点修改，当前package是指向github目录的。

所以不能直接改代码，所以就想通过patch的方式来做。

看看怎么操作。

1、先把解压一份没有修改的代码。文件夹名字写成xxx.orig。

2、diff -u  xxx.orig/aaa.c xxx/aaa.c > 0001-some-reason.patch

文件内容如下：

```
Index: shairport-sync-3.1.6/rtsp.c
--- shairport-sync-3.1.6.orig/rtsp.c  2017-12-14 07:41:56.000000000 +0800
+++ shairport-sync-3.1.6/rtsp.c      2020-06-18 10:25:49.642178585 +0800
@@ -1877,6 +1877,7 @@
   debug(1, "RTSP conversation thread %d terminated.", conn->connection_number);
   //  please_shutdown = 0;
   conn->running = 0;
+  system("echo stop > /tmp/airplay_state");
   return NULL;
 }
 
@@ -2095,6 +2096,7 @@
         die("Failed to create RTSP receiver thread %d!", conn->connection_number);
       debug(3, "Successfully created RTSP receiver thread %d.", conn->connection_number);
       conn->running = 1; // this must happen before the thread is tracked
+      system("echo play > /tmp/airplay_state");
       track_thread(conn);
     }
   }


```

注意最后要有一个空行。

不然会提示警告。

测试：

```
make shairport-sync-dirclean # 清除当前的目录。
make shairport-sync-extract # 重新解压。
make shairport-sync-patch # 打补丁。
```



参考资料

1、

https://stackoverflow.com/questions/6382986/how-to-apply-patches-to-a-package-in-buildroot