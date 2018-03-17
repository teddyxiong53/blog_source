---
title: Ubuntu之允许挂载nfs
date: 2018-03-16 18:35:42
tags:
	- Ubuntu

---



开发板上要通过挂载服务器上的目录，但是现在提示了不允许。

看看如何解决这个问题。

1、安装nfs服务。

```
sudo apt-get install nfs-kernel-server
```

2、配置nfs服务。

编辑/etc/exports文件。

当前这个文件里都只是注释。

加入下面这一行。

```
/home/teddy/work/mylinuxlab/nfs  *(rw,sync,no_subtree_check,no_root_squash)
```

我们要保证有这个目录存在。没有就新建。

3、重启服务。

```
sudo  /etc/init.d/rpcbind restart 
sudo /etc/init.d/nfs-kernel-server restart 
```

4、在板端进行挂载。

```
mount -t nfs -o tcp,nolock 192.168.0.1:/home/teddy/work/mylinuxlab/nfs  /mnt
```

现在就可以挂载成功了。

```
/ # df -h
Filesystem                Size      Used Available Use% Mounted on
192.168.0.1:/home/teddy/work/mylinuxlab/nfs
                         90.4G     34.6G     51.2G  40% /mnt
```





