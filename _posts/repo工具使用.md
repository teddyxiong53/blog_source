---
title: repo工具使用
date: 2018-10-11 10:34:51
tags:
	- 工具

---



repo是谷歌开发的，用来管理Android代码的工具，是用Python对git进行了包装的工具。

简化了对多个git版本库的管理。

repo的使用流程是这样的：

1、初始化。基于xml文件。./repo/manifest.xml。

```
repo init
```

2、repo sync。

同步项目里的某一个部分，

repo sync xxx。



git也带了submodule，也是可以管理多个工程的。

为什么不用呢？

因为git的submodule有很多的坑。难以管理复杂的工程。

需要repo管理的，都是多个开源项目集合起来的。



# 服务器搭建

新建repo目录，下面新建repo_client和repo_server这2个子目录。

```
hlxiong@hlxiong-VirtualBox:~/work/test/repo$ tree -L 1
.
├── repo_client
└── repo_server
```

## repo_server

目录结构如下：

```
hlxiong@hlxiong-VirtualBox:~/work/test/repo/repo_server$ tree
.
├── manifest.git
│   └── default.xml
├── pro1
│   └── 1.txt
└── pro2
    └── 2.txt
```

过程：

```
mkdir manifest.git
git init
touch default.xml
```

default.xml内容：

```
<?xml version="1.0" ?>
<manifest>
	<remote name="repo_server" fetch="/home/hlxiong/work/test/repo/repo_server" />
	<default revision="master" remote="repo_server" />
	<project name="pro1" path="pro1" />
	<project name="pro2" path="pro2" />
</manifest>
```

然后

```
git add .
git commit -m "add default.xml"
```

pro1和pro2这2个目录也都是git目录。进行git init和git commit。

这样，server端就搭建好了。

## repo_client

先执行repo init，是为了下载repo工具。

```
repo init 
```

得到.repo目录。

```
修改里面的.repo/repo/repo
```

把url修改一下：

```
REPO_URL = "/home/hlxiong/work/test/repo/repo_server"
```

然后，新建一个软连接。

```
repo -> .repo/repo/repo
```

执行

```
./repo init -u /home/hlxiong/work/test/repo/repo_server/manifest.git
```

然后执行

```
./repo sync
```

就可以了。



# 实验

基于上面搭建的环境，进行常用命令的学习。

repo_client下的.repo目录内容：

```
manifests
manifests.git
manifest.xml -> manifests/default.xml
project.list
	这个里面就2行，写着pro1和pro2 。
project-objects
projects
	这个下面有pro1.git和pro2.git目录。
repo
```



## repo info

```
hlxiong@hlxiong-VirtualBox:~/work/test/repo/repo_client$ ./repo info
Manifest branch: master
Manifest merge branch: refs/heads/master
Manifest groups: all,-notdefault
----------------------------
Project: pro1
Mount path: /home/hlxiong/work/test/repo/repo_client/pro1
Current revision: master
Local Branches: 0
----------------------------
Project: pro2
Mount path: /home/hlxiong/work/test/repo/repo_client/pro2
Current revision: master
Local Branches: 0
----------------------------
```



我到pro1目录下，修改1.txt。

然后这么把这个修改提交呢？

repo status可以看到变化。

```
hlxiong@hlxiong-VirtualBox:~/work/test/repo/repo_client$ ./repo status
project pro1/                                   (*** NO BRANCH ***)
 M-     1.txt
```

repo diff也可以看到，更加详细一点。

## repo list

```
hlxiong@hlxiong-VirtualBox:~/work/test/repo/repo_client$ ./repo list
pro1 : pro1
pro2 : pro2
```







repo就是管理多个git仓库的工具。

需要一个manifest.xml文件来指定git目录从哪里下载，下载到什么位置。

用project标签来指定仓库。

另外还有remote标签。

```
remote标签
	指定远程查看名字和地址。
project
	指定每一个子项目的信息。
	path：下载到的位置。
	name：相对于remote的路径。
	copyfile标签。
	linkfile标签
default：
	？

```



# 提交上传代码

如果本地代码有修改，需要提交上传。

1、先到对应的project目录下，git commit。

2、repo upload进行上传。如果远程git仓库，你有可写权限，也可以直接在git目录下push就行了。





remote fetch



# 参考资料

1、Repo工具的使用

https://blog.csdn.net/davidsky11/article/details/23291483

2、

https://www.zhihu.com/question/27000882

3、如何使用repo/git提交代码

https://blog.csdn.net/zhanglianyu00/article/details/56845462

4、简易repo服务器搭建

https://blog.csdn.net/eastmoon502136/article/details/72598297

5、

https://www.jianshu.com/p/9c57696165f3

6、repo: manifest.xml: What does the fetch=“..” mean?

https://stackoverflow.com/questions/18251358/repo-manifest-xml-what-does-the-fetch-mean