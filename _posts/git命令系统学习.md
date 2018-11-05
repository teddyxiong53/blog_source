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







#参考资料

1、git_toturial

https://gist.github.com/guweigang/9848271

2、常用 Git 命令清单

http://www.ruanyifeng.com/blog/2015/12/git-cheat-sheet.html