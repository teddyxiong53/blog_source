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

密码当成设置的是我最简单的那个密码。



我发现我的做法有些问题。

就是我总是切换到root用户来操作。这个很麻烦，应该也不是正常做法。

git是一个可登陆用户吗？

不是，无法su git。

梳理一下。



# 重新搭建

git支持4种不同的传输协议。

1、本地协议。

2、https协议。

3、ssh协议。

4、git协议。



## 本地协议

这个是最简单的，一般是做测试用的。

服务端：

```
sudo mkdir -p /git/repo
sudo git init --bare /git/repo/test.git
```

客户端：

```
cd ~/work/test/git
git clone /git/repo/test.git
```

然后我们可以进行正常的push和pull操作。

```
echo "aaa" > 1.txt
git add .
git commit -m "add 1.txt"
sudo git push # 不加sudo，会push失败。因为没有权限。
```

## ssh方式

```
 git clone git@localhost:/home/git/repo/sample.git
```

也很简单。



参考资料

1、Git 服务器搭建

http://www.runoob.com/git/git-server.html

2、搭建自己的 Git 服务器

https://www.aneasystone.com/archives/2018/12/build-your-own-git-server.html