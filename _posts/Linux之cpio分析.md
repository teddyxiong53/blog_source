---
title: Linux之cpio分析
date: 2020-04-16 15:35:01
tags:

	- Linux

---

1

cpio是Linux下的一个命令。

用来把文件打包进行archive，或者从archive里解包。

cpio跟tar这些打包文件的不同在于，**它甚至可以把/dev下的东西都打包进archive。**

不过cpio有个问题，就是它不会自己家去找文件来备份。

怎么办？用find来配合它工作。

在/boot下的initrd就是一个用cpio打包起来的文件。

```
file /boot/initrd.img-4.13.0-43-generic 
/boot/initrd.img-4.13.0-43-generic: ASCII cpio archive (SVR4 with no CRC)
```

我们可以用cpio把这个文件解包开来，看看有什么内容。

```
hlxiong@hlxiong-VirtualBox:~/work/test/cpio$ cpio -idmv < /boot/initrd.img-4.13.0-43-generic 
.
kernel
kernel/x86
kernel/x86/microcode
kernel/x86/microcode/AuthenticAMD.bin
```

解开来，得到的实际上就是一个AuthenticAMD.bin文件。

打包命令：

```
find ./* | cpio -H newc -o > test.cpio
```





# 参考资料

1、linux 下cpio使用

https://blog.csdn.net/lhl_blog/article/details/7910145