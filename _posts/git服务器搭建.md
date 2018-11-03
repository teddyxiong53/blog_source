---
title: git服务器搭建
date: 2018-11-01 11:12:19
tags:
	- git

---



首先要添加git用户。

/home/hlxiong/work2/git_server

这个目录作为git服务器的路径。

```
sudo chown git:git git_server/
```

把这个目录给git。

然后切换到root用户。

在这个目录下，新建example1和example2 这2个目录。

```
root@hlxiong-VirtualBox:/home/hlxiong/work2/git_server/example1# git init example1.git --bare
初始化空的 Git 仓库于 /home/hlxiong/work2/git_server/example1/example1.git/
```

克隆下来。

```
hlxiong@hlxiong-VirtualBox:~/work/test/git$ git clone git@127.0.0.1:/home/hlxiong/work2/git_server/example1/example1.git
正克隆到 'example1'...
The authenticity of host '127.0.0.1 (127.0.0.1)' can't be established.
ECDSA key fingerprint is SHA256:7v41RGPB5Yh9sLGT6kPWS9AGXubHlxvcopUMI5n1jeI.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '127.0.0.1' (ECDSA) to the list of known hosts.
git@127.0.0.1's password: 
warning: 您似乎克隆了一个空仓库。
检查连接... 完成。
```



参考资料

1、Git 服务器搭建

http://www.runoob.com/git/git-server.html