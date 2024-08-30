---
title: git之gitea搭建
date: 2022-01-08 12:27:11
tags:
	- git

---

--

# 基本搭建

最近看到gitea这个简单实用的git服务软件，是国人开发的 ，然后还看了B站上的一个分享相关技术的视频，加了对应的QQ群。所以产生了一些兴趣。是用go语言写的。相比于gitlab和github实用ruby语言，go语言我希望能够了解一些实际的项目，而且go语言也是我希望了解的。

所以打算通过gitea这个项目来加深对go语言和git的了解和掌握。

gitea的主要特色就是安装部署非常简单。

我就在我的服务器上来安装部署，通过宝塔来安装和配置服务访问。做成一个实用的服务。自己可以用一用。

我尽量不通过docker的方式。

数据库就实用sqlite。这样更方便把握，性能不是我的追求，我现在是希望所有的部分都足够小，可以掌握。

二进制在这里

https://dl.gitea.io/gitea/1.15.9

上面这个地址下载速度非常慢。

不如用下面这个地址的。

https://github.com/go-gitea/gitea/releases

运行

```
./gitea web -p 3456
```

然后访问这个地址，就会进入到配置界面。

我放在gitea_dir下面执行gitea程序。

选择sqlite数据库。

默认的文件路径是

```
home/ubuntu/gitea_dir/data/gitea.db
```

默认的仓库根目录

```
/home/ubuntu/gitea_dir/data/gitea-repositories
```

然后就可以访问了。可以注册登录，可以创建仓库。界面比较简洁。

然后可以看看代码。

# 配置

就修改custom/app.ini的内容。

因为我是在一个我自己不具备管理员权限的服务器上进行操作。

http端口用3456，ssh端口用2222

在app.ini修改，使用gitea内置的ssh服务器，而不是系统的ssh服务器。

```
DISABLE_SSH = false
SSH_PORT         = 2222
START_SSH_SERVER = true
```

app.ini修改好之后，只需要

# 把一个github上的项目提交到自己的gitea服务器上

将一个GitHub上的项目提交到自己的Gitea服务器上，可以按照以下步骤操作：

1. **从GitHub克隆项目**
2. **在Gitea上创建一个新的仓库**
3. **将项目推送到Gitea仓库**

### 详细步骤

#### 1. 从GitHub克隆项目

```bash
git clone https://github.com/username/repository.git
cd repository
```

#### 2. 在Gitea上创建一个新的仓库

1. 登录到你的Gitea服务器。
2. 创建一个新的仓库，记住仓库的URL，例如 `http://gitea.example.com/username/repository.git`。

#### 3. 将项目推送到Gitea仓库

```bash
# 添加Gitea仓库为远程仓库
git remote add gitea http://gitea.example.com/username/repository.git

# 推送到Gitea仓库
git push -u gitea master
```

### 总结

| 步骤              | 命令/操作                                                    |
| ----------------- | ------------------------------------------------------------ |
| 克隆GitHub项目    | `git clone https://github.com/username/repository.git`       |
| 进入项目目录      | `cd repository`                                              |
| 在Gitea上创建仓库 | 在Gitea上手动创建新仓库，并记住其URL                         |
| 添加Gitea远程仓库 | `git remote add gitea http://gitea.example.com/username/repository.git` |
| 推送到Gitea仓库   | `git push -u gitea master`                                   |

这样，你就可以将GitHub上的项目提交到自己的Gitea服务器上了。

# gitea上的项目同步到github

https://docs.gitea.com/zh-cn/usage/repo-mirror

# sync fork

gitea目前不支持这个功能。

github是支持的。

就是在web上同步原始仓库到你fork的仓库。



# PR操作流程

在网页上PR已经会了。

但是因为gitea缺少sync fork机制。所以需要本地操作。

我需要在本地先跟原始仓库同步代码，然后push到我fork后的仓库里。这样来达到同步的目的。

但是怎么来跟原始仓库同步呢？

需要加一个remote。

如果只有origin没有upstream，需要使用“git remote add upstream+源项目地址“”的命令增加上游代码库

```
git remote add upstream  http://rd03-sz:3456/hanliang.xiong/test1.git
```



```
git fetch upstream
```

