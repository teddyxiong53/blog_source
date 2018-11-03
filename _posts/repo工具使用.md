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



# 服务器搭建

repo是一个将多个git tree进行系统管理的工具。

repo本身不是一个版本管理工具。

它只是用了manifest.git 对多个工程进行统一管理。

在repo sync的时候，xml文件里指定的工程都被sync下来。

新建测试目录结构如下。

```
hlxiong@hlxiong-VirtualBox:~/work/test/repo$ tree 
.
├── repo-client
└── repo-server
    ├── external
    │   ├── example1
    │   └── example2
    └── manifest.git
        └── default.xml
```





```
hlxiong@hlxiong-VirtualBox:~/work/test/repo/repo-client$ repo init -u ~/work/test/repo/repo-server/manifest.git/
Get https://gerrit.googlesource.com/git-repo/clone.bundle
Get https://gerrit.googlesource.com/git-repo
remote: Finding sources: 100% (20/20)
remote: Total 20 (delta 6), reused 20 (delta 6)
展开对象中: 100% (20/20), 完成.
来自 https://gerrit.googlesource.com/git-repo
   b3133a3..36391bf  master     -> origin/master
Get /home/hlxiong/work/test/repo/repo-server/manifest.git/
remote: 对象计数中: 12, 完成.        
remote: 压缩对象中: 100% (8/8), 完成.        
remote: Total 12 (delta 2), reused 0 (delta 0)        
来自 /home/hlxiong/work/test/repo/repo-server/manifest
 * [新分支]          master     -> origin/master

Your identity is: xionghanliang <xionghanliang@dossav.com>
If you want to change this, please re-run 'repo init' with --config-name

repo has been initialized in /home/hlxiong/work/test/repo/repo-client
```



但是repo sync不行。

```
hlxiong@hlxiong-VirtualBox:~/work/test/repo/repo-client$ repo sync
Fetching project external/example2
fatal: '/home/hlxiong/work/test/repo-server/external/example2' does not appear to be a git repository
fatal: Could not read from remote repository.
```

我另外开启我本机上的git服务器。



但是git仓库和repo怎么关联起来呢？



现在就需要在repo-server里操作。

```
hlxiong@hlxiong-VirtualBox:~/work/test/repo/repo-server/external/example1$ git push
fatal: 没有配置推送目标。
或通过命令行指定 URL，或用下面命令配置一个远程仓库

    git remote add <名称> <地址>

然后使用该远程仓库名执行推送

    git push <名称>
```

这里就涉及到git远程仓库的使用了。ex1是一个short name。后面是完整路径。

```
hlxiong@hlxiong-VirtualBox:~/work/test/repo/repo-server/external/example1$ git remote add ex1 git@127.0.0.1:/home/hlxiong/work2/git_server/example1/example1.git
hlxiong@hlxiong-VirtualBox:~/work/test/repo/repo-server/external/example1$ git remote
ex1
```

进行push操作看看。

```

hlxiong@hlxiong-VirtualBox:~/work/test/repo/repo-server/external/example1$ git push ex1
warning: push.default 尚未设置，它的默认值在 Git 2.0 已从 'matching'
变更为 'simple'。若要不再显示本信息并保持传统习惯，进行如下设置：

  git config --global push.default matching

若要不再显示本信息并从现在开始采用新的使用习惯，设置：

  git config --global push.default simple

当 push.default 设置为 'matching' 后，git 将推送和远程同名的所有
本地分支。

从 Git 2.0 开始，Git 默认采用更为保守的 'simple' 模式，只推送当前
分支到远程关联的同名分支，即 'git push' 推送当前分支。

参见 'git help config' 并查找 'push.default' 以获取更多信息。
（'simple' 模式由 Git 1.7.11 版本引入。如果您有时要使用老版本的 Git，
为保持兼容，请用 'current' 代替 'simple'）

fatal: 当前分支 master 没有对应的上游分支。
为推送当前分支并建立与远程上游的跟踪，使用

    git push --set-upstream ex1 master
```

失败了。

按照提示操作。

```
git push --set-upstream ex1 master
```

然后我可以在我的git-client测试目录下，进行git pull了。

```
hlxiong@hlxiong-VirtualBox:~/work/test/git/example1$ git log
fatal: 您的当前分支 'master' 尚无任何提交
hlxiong@hlxiong-VirtualBox:~/work/test/git/example1$ git pull
git@127.0.0.1's password: 
remote: 对象计数中: 4, 完成.
remote: 压缩对象中: 100% (2/2), 完成.
remote: Total 4 (delta 0), reused 0 (delta 0)
展开对象中: 100% (4/4), 完成.
来自 127.0.0.1:/home/hlxiong/work2/git_server/example1/example1
 * [新分支]          master     -> origin/master
hlxiong@hlxiong-VirtualBox:~/work/test/git/example1$ 
hlxiong@hlxiong-VirtualBox:~/work/test/git/example1$ ls
1.txt  2.txt
```



现在还是提示example2不是一个git目录。

```
lxiong@hlxiong-VirtualBox:~/work/test/repo/repo-client$ repo sync
Fetching project external/example2
fatal: '/home/hlxiong/work/test/repo-server/external/example2' does not appear to be a git repository
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
```

这个看起来是路径问题。

```
/home/hlxiong/work/test/repo-server/external/example2
```

这里test后面还有一个repo目录。

改好了这些，可以repo sync。

```
hlxiong@hlxiong-VirtualBox:~/work/test/repo/repo-client$ repo sync
Fetching project external/example2
remote: 对象计数中: 3, 完成.        
remote: 压缩对象中: 100% (2/2), 完成.        
remote: Total 3 (delta 0), reused 0 (delta 0)        
来自 /home/hlxiong/work/test/repo/repo-server/external/example2
 * [新分支]          master     -> repo-server/master
Fetching project external/example1
remote: 对象计数中: 4, 完成.        
remote: 压缩对象中: 100% (2/2), 完成.        
remote: Total 4 (delta 0), reused 0 (delta 0)        
来自 /home/hlxiong/work/test/repo/repo-server/external/example1
 * [新分支]          master     -> repo-server/master

```

接下来就是要在repo-client里，修改内容，然后提交到git-server目录下去。

```
hlxiong@hlxiong-VirtualBox:~/work/test/repo/repo-client/external/example1$ git remote add ex1 git@127.0.0.1:/home/hlxiong/work2/git_server/example1/example1.git
hlxiong@hlxiong-VirtualBox:~/work/test/repo/repo-client/external/example1$ git remote
ex1
repo-server
```

```
hlxiong@hlxiong-VirtualBox:~/work/test/repo/repo-client/external/example1$ git push ex1
warning: push.default 尚未设置，它的默认值在 Git 2.0 已从 'matching'
变更为 'simple'。若要不再显示本信息并保持传统习惯，进行如下设置：

  git config --global push.default matching

若要不再显示本信息并从现在开始采用新的使用习惯，设置：

  git config --global push.default simple

当 push.default 设置为 'matching' 后，git 将推送和远程同名的所有
本地分支。

从 Git 2.0 开始，Git 默认采用更为保守的 'simple' 模式，只推送当前
分支到远程关联的同名分支，即 'git push' 推送当前分支。

参见 'git help config' 并查找 'push.default' 以获取更多信息。
（'simple' 模式由 Git 1.7.11 版本引入。如果您有时要使用老版本的 Git，
为保持兼容，请用 'current' 代替 'simple'）

fatal: 您当前不在一个分支上。
现在为推送当前（分离头指针）的历史，使用

    git push ex1 HEAD:<远程分支名字>

hlxiong@hlxiong-VirtualBox:~/work/test/repo/repo-client/external/example1$ git push ex1 HEAD:master
git@127.0.0.1's password: 
对象计数中: 2, 完成.
Delta compression using up to 4 threads.
压缩对象中: 100% (2/2), 完成.
写入对象中: 100% (2/2), 297 bytes | 0 bytes/s, 完成.
Total 2 (delta 0), reused 0 (delta 0)
To git@127.0.0.1:/home/hlxiong/work2/git_server/example1/example1.git
   3475657..f45ae72  HEAD -> master
```

可以推送上去了。

另外在git-client目录下pull一下，就可以看到了。

```
hlxiong@hlxiong-VirtualBox:~/work/test/git/example1$ ls
1.txt  2.txt
hlxiong@hlxiong-VirtualBox:~/work/test/git/example1$ git pull
git@127.0.0.1's password: 
remote: 对象计数中: 2, 完成.
remote: 压缩对象中: 100% (2/2), 完成.
remote: Total 2 (delta 0), reused 0 (delta 0)
展开对象中: 100% (2/2), 完成.
来自 127.0.0.1:/home/hlxiong/work2/git_server/example1/example1
   3475657..f45ae72  master     -> origin/master
更新 3475657..f45ae72
Fast-forward
 3.txt | 0
 1 file changed, 0 insertions(+), 0 deletions(-)
 create mode 100644 3.txt
hlxiong@hlxiong-VirtualBox:~/work/test/git/example1$ tree
.
├── 1.txt
├── 2.txt
└── 3.txt

0 directories, 3 files
```



然后我在git-client里，进行提交。

然后在repo-client里，进行repo sync。看看能不能把内容弄下来。

```
hlxiong@hlxiong-VirtualBox:~/work/test/repo/repo-client/external/example1$ ls
1.txt  2.txt
hlxiong@hlxiong-VirtualBox:~/work/test/repo/repo-client/external/example1$ git pull ex1 master
git@127.0.0.1's password: 
来自 127.0.0.1:/home/hlxiong/work2/git_server/example1/example1
 * branch            master     -> FETCH_HEAD
更新 3475657..0c72566
Fast-forward
 3.txt | 0
 4.txt | 0
 2 files changed, 0 insertions(+), 0 deletions(-)
 create mode 100644 3.txt
 create mode 100644 4.txt
hlxiong@hlxiong-VirtualBox:~/work/test/repo/repo-client/external/example1$ ls
1.txt  2.txt  3.txt  4.txt
```



但是我repo sync会导致内容被丢掉。为什么？

```
hlxiong@hlxiong-VirtualBox:~/work/test/repo/repo-client$ repo sync
Fetching project external/example2
Fetching project external/example1

external/example1/: discarding 2 commits
```



如果要把本地的 master 分支推送到 origin 服务器上（再次说明下，克隆操作会自动使用默认的 master 和 origin 名字）





# 参考资料

1、Repo工具的使用

https://blog.csdn.net/davidsky11/article/details/23291483