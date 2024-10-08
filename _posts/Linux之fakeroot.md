---
title: Linux之fakeroot
date: 2022-10-20 19:07:33
tags:
	- Linux

---

--

fakeroot - run a command in an environment faking root privileges for file manipulation

它主要用来打包或者用来生成image，

假如没有fakeroot，要做具有root权限文件的包的话，需要做的事情既多又麻烦， 

首先切换到root权限，修改目录中所有文件为root权限，打包， 完了之后还需要把权限改回来。

有fakeroot就很方便了，在fakeroot环境中，**只需要做打包动作，里边的所有文件自动的都是root权限。**

fakeroot的一般用法是fakeroot -- script， script是shell脚本，把需要再root权限执行的命令写在脚本里边。

进入fakeroot环境，文件的owner和group自动变为root。 exit 退出fakeroot， 文件的owner和group还原。
退出fakeroot后就返回普通用户状态，fakeroot只在运行过程中起作用。



# buildroot里的fakeroot使用

在fs/common.mk里

```
>>>   Generating filesystem image rootfs.cpio
>>>   Generating filesystem image rootfs.ext2
>>>   Generating filesystem image rootfs.tar
```

是要生成一个fakeroot脚本，在这个目录下：

```
hanliang.xiong@walle01-sz:~/work/a113x2/code14/output/a5_av400_a6432_release/build/buildroot-fs$ tree
.
├── cpio
│   └── fakeroot
├── ext2
│   └── fakeroot
├── full_devices_table.txt
├── full_users_table.txt
└── tar
    └── fakeroot
```

例如，看cpio/fakeroot的内容：

```
set -e
chown -h -R 0:0 $output/build/buildroot-fs/cpio/target
chown -h -R 1000:1000 '$output/build/buildroot-fs/cpio/target//var/run/dbus'
$output/host/bin/makedevs -d $output/build/buildroot-fs/full_devices_table.txt $output/build/buildroot-fs/cpio/target
if [ ! -e $output/build/buildroot-fs/cpio/target/init ]; then 
    /usr/bin/install -m 0755 "fs/cpio"/init $output/build/buildroot-fs/cpio/target/init; 
fi
mkdir -p $output/build/buildroot-fs/cpio/target/dev
mknod -m 0622 $output/build/buildroot-fs/cpio/target/dev/console c 5 1


cd $output/build/buildroot-fs/cpio/target \
&& cat /mnt/fileroot/hanliang.xiong/work/a113x2/code14/buildroot/"board/amlogic/mesona5_av400/initramfs/ramfslist-32-ext2" \
| grep -v "^#" | cpio --quiet -o -H newc >$output/images/rootfs.cpio
```

简单说，就是打包一个rootfs.cpio。通过ramfslist-32-ext2来指定打包的内容，另外还创建了一些device。

命令是这样调用的：

```
PATH=$$(BR_PATH) FAKEROOTDONTTRYCHOWN=1 $$(HOST_DIR)/bin/fakeroot -- $$(FAKEROOT_SCRIPT)
```





# /usr/lib/libfakeroot-sysv.so

与faked通讯的库文件是/usr/lib/libfakeroot/libfakeroot-sysv.so，

但是/usr/lib/libfakeroot-sysv.so也是存在的。

这个文件是在fakeroot中运行suid程序所必须的。 

fakeroot中会设定LD_LIBRARY_PATH环境变量。

设定LD_LIBRARY_PATH后LD_PRELOAD就不需要是完整路径了。

但是如果LD_PRELOAD不使用完整路径，suid的程序会忽略LD_LIBRARY_PATH而直接在/lib与/usr/lib中寻找LD_PRELOAD指定的库文件。

如果LD_PRELOAD指定的文件没有找到这个suid的程序就会启动失败。

所以会存在/usr/lib/libfakeroot-sysv.so这样一个suid的dummy库，

在运行suid程序的时候通过LD_PRELOAD加载这个库，就跟没有加载任何东西一样，正常执行。

 * 普通的程序 使用LD_LIBRARY_PATH=/usr/lib/libfakeroot LD_PRELOAD=libfakeroot-sysv.so，通过preload加载/usr/lib/libfakeroot/libfakeroot-sysv.so的与faked通讯 * suid的程序 无视LD_LIBRARY_PATH， 使用LD_PRELOAD=libfakeroot-sysv.so，通过preload加载/usr/lib/libfakeroot-sysv.so，因为这是一个dummy库，就与这个库不存在一样，程序正常执行。



# 参考资料

1、fakeroot

https://blog.csdn.net/dongkun152/article/details/88534669