---
title: Linux之dropbear
date: 2018-04-14 09:36:26
tags:
	- Linux

---



# dropbear是什么

dropbear是一个小巧的ssh服务器和客户端。

跟openssh相比，更加简洁小巧，占用内存更少。

一个用户登录，openssh会开2个进程，而dropbear只开一个。

可以在兼容posix的平台上运行。使用MIT协议开源。

一般应用在路由器。



服务端是：dropbear。

客户端是：dbclient。

秘钥生成程序：dropbearkey。

工具：dropbearconvert。用来转换openssh的秘钥。

源代码下载

https://matt.ucc.asn.au/dropbear/



我在我的mylinuxlab里做实验。

先把源代码交叉编译。

```
./configure \
    CC=arm-linux-gnueabihf-gcc --enable-static \
	CFLAGS="-Wno-error " \
    --target=arm-linux-gnueabihf \
    --host=arm-linux-gnueabihf 
```

报错了。

```
configure: error: *** zlib missing - install first or check config.log ***
```

这个需要下载源代码来安装zlib。

http://zlib.net/zlib-1.2.8.tar.gz

配置编译：

```
cd zlib-1.2.8/
./configure --prefix=/home/teddy/work/ssh/zlib_install
```

然后手动修改Makefile。

把CC、LDSHARED、CPP都改成arm-linux-gnueabihf-gcc

然后make和make install。

然后修改dropbear的configure。

```
./configure \
    CC=arm-linux-gnueabihf-gcc --enable-static \
	CFLAGS="-Wno-error " \
    --target=arm-linux-gnueabihf \
    --host=arm-linux-gnueabihf --with-zlib=/home/teddy/work/ssh/zlib_install \
    --prefix=/home/teddy/work/ssh/dropbear_install
```

编译得到的东西：

```
teddy@teddy-ubuntu:~/work/ssh/dropbear_install$ tree
.
├── bin
│   ├── dbclient
│   ├── dropbearconvert
│   └── dropbearkey
├── sbin
│   └── dropbear
└── share
    └── man
        ├── man1
        │   ├── dbclient.1
        │   ├── dropbearconvert.1
        │   └── dropbearkey.1
        └── man8
            └── dropbear.8

```

把bin和sbin的东西，放到mylinuxlab里的rootfs里。

运行报错：

```
~ # dropbear
dropbear: error while loading shared libraries: libz.so.1: cannot open shared object file: No such file or directory
~ # 
```

我们需要把前面编译得到的libz的so文件拷贝到mylinuxlab里。

```
~ # mkdir /etc/dropbear
~ # cd /etc/dropbear/
/etc/dropbear # dropbearkey -t rsa -f dropbear_rsa_host_key
```

一定要先生成key。才能执行dropbear。

默认是在22号端口上。

Ubuntu下的客户端，也用dropbear的，我把对应的代码都编译对应的x86版本。

```
teddy@teddy-ubuntu:~/work/ssh/dropbear_install_x86/bin$ ./dbclient root@192.168.0.2 

Host '192.168.0.2' is not in the trusted hosts file.
(ssh-rsa fingerprint md5 42:7f:73:5c:e6:67:18:5e:53:1d:d6:3c:82:e4:19:70)
Do you want to continue connecting? (y/n) y
root@192.168.0.2's password: 
root@192.168.0.2's password: 
```

现在提示要密码，但是我没有密码啊。

可以通过秘钥来免密登陆。





```
#重新建立公钥文件
dropbearkey -t dss -f /etc/dropbear/dropbear_dss_host_key
dropbearkey -t rsa -s 1024 -f /etc/dropbear/dropbear_rsa_host_key

#生存公钥Key
dropbearkey -y -f /etc/dropbear/dropbear_rsa_host_key >> /etc/dropbear/authorized_keys_my
vim /etc/dropbear/authorized_keys_my #删除第一行和第三行
```

不过还是不行。

算了。

我的mylinuxlab里有添加带密码的用户teddy。

```
teddy@teddy-ubuntu:~/work/ssh/dropbear_install_x86/bin$ ./dbclient teddy@192.168.0.2 

Host '192.168.0.2' is not in the trusted hosts file.
(ssh-rsa fingerprint md5 fc:46:aa:a7:42:35:51:ea:39:da:0c:98:54:78:82:64)
Do you want to continue connecting? (y/n) y
teddy@192.168.0.2's password: 
/etc/profile executed!
~ $ 
~ $ 
```

这样就可以登陆进去了。

一个基本的通路就建立起来了。



另外，给root用户设置一个密码也很简单。

passwd root。设置密码，然后就可以ssh来登陆了，这种方式更加简单。



# 参考资料

1、百度百科

https://baike.baidu.com/item/dropbear/3701186?fr=aladdin

2、dropbear过程讲解及数据传输过程及如何建立CA

http://blog.51cto.com/10968002/1917755

3、Mips下交叉编译dropbear

https://blog.csdn.net/dxm2025/article/details/42489291

4、dropbear实现免密码ssh登录方法

http://blog.sina.com.cn/s/blog_6f06e2eb0102v5ar.html

5、ssh登录提示RSA Host key认证失败的解决方法

https://blog.csdn.net/thdsea4/article/details/74942327