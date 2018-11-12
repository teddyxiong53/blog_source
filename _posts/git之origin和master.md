---
title: git之origin和master
date: 2018-11-10 11:48:24
tags:
	- git

---



在clone完成后，git会自动为你把远程仓库命名为origin。origin相当于一个别名。

可以用git remote -v查看远程仓库的信息。

```
hlxiong@hlxiong-VirtualBox:~/work/test/git/xxx$ git remote -v
xxx     git@127.0.0.1:/home/hlxiong/work2/git_server/xxx (fetch)
xxx     git@127.0.0.1:/home/hlxiong/work2/git_server/xxx (push)
```

git push origin。

一般等价于git push。

更加完整的命令是git push -u origin master。

也可以这样push：

```
git push git@github.com:username/project.git
```



而master，是本地的仓库的名字。







参考资料

1、GIT 的ORIGIN和MASTER分析

https://www.cnblogs.com/MarkTang/p/5759554.html

2、git push origin与git push -u origin master的区别

https://blog.csdn.net/JackLiu16/article/details/80952650