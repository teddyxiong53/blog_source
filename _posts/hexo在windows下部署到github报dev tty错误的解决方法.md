---
title: hexo在windows下部署到github报/dev/tty错误的解决方法
date: 2016-10-03 12:42:22
tags: 
	- hexo
	- github
---
在windows下部署hexo到github，总是报/dev/tty找不到设备。
我的博客的_config.yml文件的部署部分是这样的：
```
deploy:
	type: git
	repo: https://github.com/teddyxiong53/teddyxiong53.github.io
	branch: master
```

折腾了好久，终于发现只要这样改就好了。
```
deploy:
	type: git
	repo: git@github.com:teddyxiong53/teddyxiong53.github.io.git
	branch: master
```

然后再hexo d，可以看到部署成功了。
```
$ hexo d
INFO  Deploying: git
INFO  Clearing .deploy_git folder...
INFO  Copying files from public folder...
On branch master
nothing to commit, working directory clean
Branch master set up to track remote branch master from git@github.com:teddyxiong53/teddyxiong53.github.io.git.
To git@github.com:teddyxiong53/teddyxiong53.github.io.git
 + 0d54a3d...b35fb80 HEAD -> master (forced update)
INFO  Deploy done: git
```