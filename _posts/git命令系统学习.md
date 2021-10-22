---
title: git命令系统学习
date: 2018-11-05 10:32:21
tags:
	- git
typora-root-url: ..\
---



现在对git用得较多，所以需要把所有命令系统学习一遍了。

刚好我自己也搭建了一个git服务器。正好配合起来学习。

关于git的数据流，看这张图就够了。

![](/images/git数据流图.jpg)

概念：

1、workspace。工作区。

2、index。或者叫stage，本地暂存区。

3、repo。本地仓库。

4、remote。远程仓库。



# 新建代码库

```
hlxiong@hlxiong-VirtualBox:~/work/test/git/xxx$ git init 
初始化空的 Git 仓库于 /home/hlxiong/work/test/git/xxx/.git/
```

这个相当于帮你新建目录，然后再在里面做。

```
hlxiong@hlxiong-VirtualBox:~/work/test/git/yyy$ git init yyy
初始化空的 Git 仓库于 /home/hlxiong/work/test/git/yyy/yyy/.git/
```

```
hlxiong@hlxiong-VirtualBox:~/work/test/git/xxx/.git$ tree
.
├── branches
├── config
├── description
├── HEAD
├── hooks
│   ├── applypatch-msg.sample
│   ├── commit-msg.sample
│   ├── post-update.sample
│   ├── pre-applypatch.sample
│   ├── pre-commit.sample
│   ├── prepare-commit-msg.sample
│   ├── pre-push.sample
│   ├── pre-rebase.sample
│   └── update.sample
├── info
│   └── exclude
├── objects
│   ├── info
│   └── pack
└── refs
    ├── heads
    └── tags

9 directories, 13 files
```



# 配置

配置在.gitconfig文件里，这个文件主目录有一个，每个项目下也可以有。

```
[user]
    email = xionghanliang@dossav.com
    name = xionghanliang
[color]
    ui = auto
```

查看配置。

```
hlxiong@hlxiong-VirtualBox:~/work/test/git/xxx$ git config --list
user.email=xionghanliang@dossav.com
user.name=xionghanliang
color.ui=auto
core.repositoryformatversion=0
core.filemode=true
core.bare=false
core.logallrefupdates=true
```

加入配置。如果要全局生效，加上`--global`选项。

```
hlxiong@hlxiong-VirtualBox:~/work/test/git/xxx$ git config user.name "xhl"
hlxiong@hlxiong-VirtualBox:~/work/test/git/xxx$ git config user.email "xhl@xxx.com"
hlxiong@hlxiong-VirtualBox:~/work/test/git/xxx$ git config --list
user.email=xionghanliang@dossav.com
user.name=xionghanliang
color.ui=auto
core.repositoryformatversion=0
core.filemode=true
core.bare=false
core.logallrefupdates=true
user.name=xhl
user.email=xhl@xxx.com
```

# 增加和删除文件

```
hlxiong@hlxiong-VirtualBox:~/work/test/git/xxx$ touch f1.c
hlxiong@hlxiong-VirtualBox:~/work/test/git/xxx$ mkdir d1 
hlxiong@hlxiong-VirtualBox:~/work/test/git/xxx$ cd d1
hlxiong@hlxiong-VirtualBox:~/work/test/git/xxx/d1$ ls
hlxiong@hlxiong-VirtualBox:~/work/test/git/xxx/d1$ touch d1_f1.c
hlxiong@hlxiong-VirtualBox:~/work/test/git/xxx/d1$ cd ..
hlxiong@hlxiong-VirtualBox:~/work/test/git/xxx$ git add .
hlxiong@hlxiong-VirtualBox:~/work/test/git/xxx$ git status
位于分支 master

初始提交

要提交的变更：
  （使用 "git rm --cached <文件>..." 以取消暂存）

        新文件：   d1/d1_f1.c
        新文件：   f1.c
```



````
git add .  # 把本地所有文件都添加到暂存区
git add f1.c # 把指定文件添加到暂存区。
git add d1 # 把d1目录添加到暂存区
````

git add -p f1.c。-p选项表示，添加每个变化前都会要求确认。

```
hlxiong@hlxiong-VirtualBox:~/work/test/git/xxx$ git add -p f1.c 
diff --git a/f1.c b/f1.c
index e69de29..6067a18 100644
--- a/f1.c
+++ b/f1.c
@@ -0,0 +1,4 @@
+void func1()
+{
+}
+
Stage this hunk [y,n,q,a,d,/,e,?]? y
<stdin>:9: new blank line at EOF.
+
warning: 1 行有空白字符误用。
```

```
hlxiong@hlxiong-VirtualBox:~/work/test/git/xxx$ git rm f1.c
error: 下列文件索引中有变更
    f1.c
（使用 --cached 保留本地文件，或用 -f 强制删除）
hlxiong@hlxiong-VirtualBox:~/work/test/git/xxx$ git rm f1.c -f
rm 'f1.c'
hlxiong@hlxiong-VirtualBox:~/work/test/git/xxx$ git status
位于分支 master

初始提交

要提交的变更：
  （使用 "git rm --cached <文件>..." 以取消暂存）

        新文件：   d1/d1_f1.c

hlxiong@hlxiong-VirtualBox:~/work/test/git/xxx$ 
```

改名字。

```
git mv f1.c f11.c
```

# 代码提交

默认就是git commit -m "xxx"

git commit -a 。这个会直接提交，会弹出编辑界面，让你填写提交信息的。



# 分支

查看本地分支。

```
hlxiong@hlxiong-VirtualBox:~/work/test/git/xxx$ git branch
* master
```

列出所有远程分支。

```
hlxiong@hlxiong-VirtualBox:~/work/test/git/xxx$ git branch -r
hlxiong@hlxiong-VirtualBox:~/work/test/git/xxx$ 
```

列出本地和远程的所有分支。

```
hlxiong@hlxiong-VirtualBox:~/work/test/git/xxx$ git branch -a
* master
```



# git remote命令

我的git server在/home/hlxiong/work2/git_server目录。里面git init xxx。

```
hlxiong@hlxiong-VirtualBox:~/work/test/git/xxx$ git remote add xxx git@127.0.0.1:/home/hlxiong/work2/git_server/xxx
```



然后就可以提交到这个地址了。

```
hlxiong@hlxiong-VirtualBox:~/work/test/git/xxx$ git push  --set-upstream xxx master
git@127.0.0.1's password: 
对象计数中: 4, 完成.
Delta compression using up to 4 threads.
压缩对象中: 100% (2/2), 完成.
写入对象中: 100% (4/4), 271 bytes | 0 bytes/s, 完成.
Total 4 (delta 0), reused 0 (delta 0)
To git@127.0.0.1:/home/hlxiong/work2/git_server/xxx
 * [new branch]      master -> master
分支 master 设置为跟踪来自 xxx 的远程分支 master。
```

开始报错了。

```
hlxiong@hlxiong-VirtualBox:~/work/test/git/xxx$ git push  --set-upstream xxx master
git@127.0.0.1's password: 
对象计数中: 4, 完成.
Delta compression using up to 4 threads.
压缩对象中: 100% (2/2), 完成.
写入对象中: 100% (4/4), 271 bytes | 0 bytes/s, 完成.
Total 4 (delta 0), reused 0 (delta 0)
remote: error: refusing to update checked out branch: refs/heads/master
remote: error: By default, updating the current branch in a non-bare repository
remote: error: is denied, because it will make the index and work tree inconsistent
remote: error: with what you pushed, and will require 'git reset --hard' to match
remote: error: the work tree to HEAD.
remote: error: 
remote: error: You can set 'receive.denyCurrentBranch' configuration variable to
remote: error: 'ignore' or 'warn' in the remote repository to allow pushing into
remote: error: its current branch; however, this is not recommended unless you
remote: error: arranged to update its work tree to match what you pushed in some
remote: error: other way.
remote: error: 
remote: error: To squelch this message and still keep the default behaviour, set
remote: error: 'receive.denyCurrentBranch' configuration variable to 'refuse'.
To git@127.0.0.1:/home/hlxiong/work2/git_server/xxx
 ! [remote rejected] master -> master (branch is currently checked out)
error: 无法推送一些引用到 'git@127.0.0.1:/home/hlxiong/work2/git_server/xxx'
```

网上查了下，是需要在git server目录下，执行这个：

```
root@hlxiong-VirtualBox:/home/hlxiong/work2/git_server/xxx# git config --bool core.bare true
```

另外新建一个目录，xxx_clone。来进行clone和pull操作。

```
hlxiong@hlxiong-VirtualBox:~/work/test/git/xxx_clone/xxx$ git pull
git@localhost's password: 
Permission denied, please try again.
git@localhost's password: 
remote: 对象计数中: 4, 完成.
remote: 压缩对象中: 100% (2/2), 完成.
remote: Total 4 (delta 0), reused 0 (delta 0)
展开对象中: 100% (4/4), 完成.
来自 localhost:/home/hlxiong/work2/git_server/xxx
 * [新分支]          master     -> origin/master
hlxiong@hlxiong-VirtualBox:~/work/test/git/xxx_clone/xxx$ ls
d1  f1.c
hlxiong@hlxiong-VirtualBox:~/work/test/git/xxx_clone/xxx$ git log
commit b54a995f6e8d75c146cd47fe649e10f61d14fdcd
Author: xhl <xhl@xxx.com>
Date:   Mon Nov 5 11:40:50 2018 +0800

    first commit
```

#config子命令

查看config。我觉得应该是后面的同名的覆盖前面的同名的。例如username。

```
hlxiong@hlxiong-VirtualBox:~/work/test/git/xxx$ git config -l
user.email=xionghanliang@dossav.com
user.name=xionghanliang
color.ui=auto
core.repositoryformatversion=0
core.filemode=true
core.bare=false
core.logallrefupdates=true
user.name=xhl
user.email=xhl@xxx.com
remote.xxx.url=git@127.0.0.1:/home/hlxiong/work2/git_server/xxx
remote.xxx.fetch=+refs/heads/*:refs/remotes/xxx/*
branch.master.remote=xxx
branch.master.merge=refs/heads/master
```

看看当前的git目录内容。

```
hlxiong@hlxiong-VirtualBox:~/work/test/git/xxx/.git$ tree
.
├── branches
├── COMMIT_EDITMSG 这里放的就是每次提交写的内容。
├── config 这个就是配置信息。
├── description
├── HEAD
├── hooks
│   ├── applypatch-msg.sample
│   ├── commit-msg.sample
│   ├── post-update.sample
│   ├── pre-applypatch.sample
│   ├── pre-commit.sample
│   ├── prepare-commit-msg.sample
│   ├── pre-push.sample
│   ├── pre-rebase.sample
│   └── update.sample
├── index
├── info
│   └── exclude
├── logs
│   ├── HEAD
│   └── refs
│       ├── heads
│       │   └── master
│       ├── remotes
│       │   └── xxx
│       │       └── master
│       └── stash
├── objects
│   ├── 3a
│   │   └── 292d056756b06f7c143a9991732dcf7381bdca
│   ├── 60
│   │   └── 67a1855fd68c4f3f6d85b7a0425c0a63f77dd1
│   ├── 6a
│   │   └── 4992154d916e13f9f1e936b1adb2e4911ae593
│   ├── 81
│   │   └── e827e83bb185f51cb34d35efe207908f012566
│   ├── b5
│   │   └── 4a995f6e8d75c146cd47fe649e10f61d14fdcd
│   ├── be
│   │   └── 2acc8b760274da8c0e81eec263fcb5e51a5724
│   ├── c2
│   │   └── 18bd2155e3ee3e7284b3583817c9db2f510b86
│   ├── cb
│   │   └── 02db2d6a678c119d6c6b5ec807ac2914675af2
│   ├── e6
│   │   └── 9de29bb2d1d6434b8b29ae775ad8c2e48c5391
│   ├── info
│   └── pack
├── ORIG_HEAD
└── refs
    ├── heads
    │   └── master
    ├── remotes
    │   └── xxx
    │       └── master
    ├── stash
    └── tags
```

```
hlxiong@hlxiong-VirtualBox:~/work/test/git/xxx/.git$ cat config 
[core]
        repositoryformatversion = 0
        filemode = true
        bare = false
        logallrefupdates = true
[user]
        name = xhl
        email = xhl@xxx.com
[remote "xxx"]
        url = git@127.0.0.1:/home/hlxiong/work2/git_server/xxx
        fetch = +refs/heads/*:refs/remotes/xxx/*
[branch "master"]
        remote = xxx
        merge = refs/heads/master
```

```
hlxiong@hlxiong-VirtualBox:~/work/test/git/xxx/.git$ cat HEAD 
ref: refs/heads/master
```

```
hlxiong@hlxiong-VirtualBox:~/work/test/git/xxx/.git$ cat ORIG_HEAD 
b54a995f6e8d75c146cd47fe649e10f61d14fdcd
hlxiong@hlxiong-VirtualBox:~/work/test/git/xxx/.git$ git log
commit b54a995f6e8d75c146cd47fe649e10f61d14fdcd
Author: xhl <xhl@xxx.com>
Date:   Mon Nov 5 11:40:50 2018 +0800

    first commit
```

```
hlxiong@hlxiong-VirtualBox:~/work/test/git/xxx/.git/logs$ ls
HEAD  refs
hlxiong@hlxiong-VirtualBox:~/work/test/git/xxx/.git/logs$ cat HEAD 
0000000000000000000000000000000000000000 b54a995f6e8d75c146cd47fe649e10f61d14fdcd xhl <xhl@xxx.com> 1541389250 +0800    commit (initial): first commit
```



# cheat git

用cheat工具看到的信息。一条条分析。

新建一个f2.c， stash表示隐藏。

```
git add --all
```



```
git stash save "new f2.c, stash it"
```

```
hlxiong@hlxiong-VirtualBox:~/work/test/git/xxx$ git stash list
stash@{0}: On master: new f2.c, stash it
```

这样修改的内容，就不会被提交到服务器。

可以取消隐藏。

```
hlxiong@hlxiong-VirtualBox:~/work/test/git/xxx$ git stash apply stash@{0}
位于分支 master
您的分支与上游分支 'xxx/master' 一致。
要提交的变更：
  （使用 "git reset HEAD <文件>..." 以取消暂存）

        新文件：   f2.c

```

清空本地改动。

```
hlxiong@hlxiong-VirtualBox:~/work/test/git/xxx$ git reset --hard
HEAD 现在位于 b54a995 first commit
```



# 一些git问题解答

命令 **git cherry-pick** 通常用于把特定提交从存储仓库的一个分支引入到其他分支中。常见的用途是从维护的分支到开发分支进行向前或回滚提交。

这与其他操作（例如：合并（merge）、变基（rebase））形成鲜明对比，后者通常是把许多提交应用到其他分支中。 小结：

```text
git cherry-pick <commit-hash>
```





参考资料

https://zhuanlan.zhihu.com/p/45280433



# 参考资料

1、git_toturial

https://gist.github.com/guweigang/9848271

2、常用 Git 命令清单

http://www.ruanyifeng.com/blog/2015/12/git-cheat-sheet.html