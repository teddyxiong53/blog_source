title: Linux的devpts分析
date: 2017-05-02 19:43:35
tags:
- devpts

在构建rootfs的时候，经常看到devpts这个东西，其具体含是什么呢？
一般我们在Linux下看到的控制台，是由多个设备来共同实现的。分别是`/dev/ttyN`（tty0对应console设备，tty1和tty2对应的就是虚拟的console了），我们可以用Alt+Fn来在这些console之间切换。
而`/dev/pts`是给远程登录（包括telnet和ssh等）后所创建的目录，这个目录下放的是控制台设备文件。因为远程登录的数量是难以预先知道的，所以`/dev/pts`其实是动态生成的。

pts是pseudo terminal slave的意思，对应的是ptmx（master）。它们一起构成了pty（虚拟终端）。

```
echo "xhl" > /dev/console
```

这可以得到跟`echo "xhl"`一样的效果。

`echo "xhl" > /dev/tty`也是一样的效果。

如何看到当前自己使用的是哪个tty呢？

用tty命令就行，如下：

```
teddy@teddy-ubuntu:/dev/pts$ echo "xhl" > /dev/pts/0
teddy@teddy-ubuntu:/dev/pts$ tty
/dev/pts/6
teddy@teddy-ubuntu:/dev/pts$ echo "xhl" > /dev/pts/6
xhl
```



