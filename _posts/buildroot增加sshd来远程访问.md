---
title: buildroot增加sshd来远程访问
date: 2020-03-19 11:55:11
tags:
	- buildroot
---

--

先直接选中openssh。编译烧录。

我下面碰到的问题，很多都是因为rootfs只读导致的。但是没有办法。rootfs只能只读，空间不够。

ps查看，发现没有sshd没有起来。

手动执行一下sshd，显示提示要绝对路径执行，以支持exec。然后又是报了`Privilege separation user sshd does not exist `

```
sshd re-exec requires execution with an absolute path 
/ # which sshd                                        
/usr/sbin/sshd                                        
/ # /usr/sbin/sshd                                    
Privilege separation user sshd does not exist 
```

网上看了解决方法，是需要/etc/passwd和/etc/group里增加sshd的用户信息。

```
Edit the file /etc/passwd and add the below line:
sshd:x:74:74:Privilege-separated SSH:/var/empty/sshd:/sbin/nologin
and the below line in the /etc/group file
sshd:x:74:
```

按照这个操作了。还是不行。

提示没有key。

```
/ # /usr/sbin/sshd                                    
Could not load host key: /etc/ssh/ssh_host_rsa_key    
Could not load host key: /etc/ssh/ssh_host_dsa_key    
Could not load host key: /etc/ssh/ssh_host_ecdsa_key  
Could not load host key: /etc/ssh/ssh_host_ed25519_key
sshd: no hostkeys available -- exiting.               
```

我看一下/etc/init.d/里的sshd启动脚本，看看怎么做的。需要先使用ssh-keygen。之前之所以没有生成，还是因为rootfs只读。

目前已经把/etc/ssh mount --bind到一个可写的目录了。

手动执行一下：`/usr/bin/ssh-keygen -A  `

现在生成了对应的key了。

```
start() {                          
        # Create any missing keys  
        /usr/bin/ssh-keygen -A     
                                   
        printf "Starting sshd: "   
        /usr/sbin/sshd             
        touch /var/lock/sshd       
        echo "OK"                  
}                                  
```

算了，太麻烦了。我还是用telnetd来做了。这个简单多了。



参考资料

1、Starting sshd: Privilege separation user does not exist

http://linuxhelp-kavanathai.blogspot.com/2011/08/starting-sshd-privilege-separation-user.html