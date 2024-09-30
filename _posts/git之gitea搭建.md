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



在 GitHub 上发起 PR（Pull Request）并被对方接收后，你可以通过以下步骤将对方的仓库的代码和提交日志同步到你自己的仓库：

### 步骤

1. **添加远程仓库**：
   如果你还没有将对方的仓库添加为远程仓库，使用以下命令：

   ```bash
   git remote add upstream <对方仓库的URL>
   ```

   将 `<对方仓库的URL>` 替换为对方仓库的 Git URL。

2. **获取最新代码**：
   获取对方仓库的最新提交和分支信息：

   ```bash
   git fetch upstream
   ```

3. **合并代码**：
   切换到你的主分支（通常是 `main` 或 `master`）：

   ```bash
   git checkout main
   ```

   然后将对方的主分支合并到你的分支中：

   ```bash
   git merge upstream/main
   ```

   如果对方的分支是 `master`，请相应地替换 `upstream/main` 为 `upstream/master`。

4. **推送到你的仓库**：
   将合并后的代码推送到你自己的 GitHub 仓库：

   ```bash
   git push origin main
   ```

### 确保代码和提交日志一致

通过上述步骤，你的仓库将与对方的仓库同步，同时保留所有的提交日志。这样，你的提交历史将与对方的仓库保持一致。

### 额外提示

- 如果你在合并时遇到冲突，请解决冲突后再进行提交。
- 确保在合并前，你的本地分支是最新的，以避免不必要的冲突。

通过这些步骤，你能确保你的代码和提交日志与对方的仓库一致。

# 通过drone来实现持续集成

https://www.cnblogs.com/Gitea/p/drone.html



# gitness和gitea对比

Gitness 和 Gitea 都是开源的代码托管平台，支持 Git 版本控制和团队协作，但它们在功能、架构和特定场景下的表现存在一些差异。以下是两者的详细对比：

| **对比维度**   | **Gitness**                                                  | **Gitea**                                                   |
| -------------- | ------------------------------------------------------------ | ----------------------------------------------------------- |
| **主要功能**   | Git 代码托管、CI/CD 集成、权限管理、审查流程                 | Git 代码托管、Wiki、Issue 跟踪、代码审查、CI/CD 集成        |
| **开发语言**   | Go 语言                                                      | Go 语言                                                     |
| **设计理念**   | 主要关注 CI/CD 集成和 DevOps 流程，旨在提供开箱即用的现代化开发流程 | 轻量级、易于安装，目标是成为简单、快速、易用的 Git 托管平台 |
| **CI/CD 支持** | 内置 CI/CD 流水线功能，深度集成 DevOps 工作流                | 通过集成 Drone 等外部工具实现 CI/CD 功能                    |
| **权限管理**   | 支持细粒度的权限控制，适合大规模团队管理和协作               | 提供基本的权限管理，适合中小型团队                          |
| **UI 界面**    | 现代化 UI，界面简洁，注重开发体验                            | 界面简洁易用，但设计风格较为传统                            |
| **扩展性**     | 关注 DevOps 的深度集成，可能扩展性有限                       | 支持插件系统，具备较好的扩展性，社区贡献活跃                |
| **部署与维护** | 适合 DevOps 场景，需要更多资源支持                           | 轻量级，部署和维护相对简单，资源占用较少                    |
| **社区与支持** | 较新兴的项目，社区和文档支持相对较少                         | 成熟的开源项目，社区活跃，文档丰富                          |
| **适用场景**   | 适合需要集成 CI/CD 和 DevOps 工作流的企业和开发团队          | 适合中小型团队或个人开发者，需要简单的 Git 托管和协作       |

### 总结：
- **Gitness**：侧重于集成 DevOps 和 CI/CD 流程，适合需要一体化开发和运维的团队，特别是追求现代开发工具链的企业用户。
- **Gitea**：轻量级、简单易用，适合需要 Git 托管、代码审查和基本协作功能的中小型团队或个人开发者，且其扩展性较好，社区资源丰富。

两者的选择取决于你的团队需求。如果你注重 CI/CD 和开发流程的集成，**Gitness** 是不错的选择；而如果你需要的是简单、高效的 Git 托管平台，**Gitea** 可能更适合。

# Gitea Actions

从gitea1.19版本开始，actions就成为了内置的CI/CD方案。

跟其他的CI/CD方案一样，Gitea不会自己运行Job。

而是把Job委托给Runner。

Gitea Actions的Runner被称为act runner。

它 是一个独立的程序，是go语言编写的。

它是基于nektos/act的一个分支。

由于Runner是独立部署的，可能存在潜在的安全问题。

为了避免这些问题，需要遵循下面这2个基本原则：

* 不要使用你不信任的Runner。
* 不要为了你不信任的组织提供Runner。

对于企业内部，不用考虑这个，因为天然就是信任安全的。

## 设置

从1.21.0开始，Actions默认是开启的。

我当前是1.20.4版本。

需要在配置文件里添加：

```
[actions]
ENABLED=true
```



你需要下载act runner这程序的二进制文件。

https://dl.gitea.com/act_runner/

在运行act_runner之前，你需要先把它注册到你的gitea上。

对二者进行关联。

```
./act_runner register --no-interactive --instance <instance> --token <token>
```

instance对应你的gitea的运行地址。

token用于身份验证。

一个token只能被注册一次。

token跟gitea不同级别的实体对应。

全局级别的：从xx/admin/actions/runner的页面获取token。

组织级别的：xx/<org>/settings/actions/runner的页面获取token。

仓库级别的：从xx/yy/zz/settings/actions/runner的页面获取token。xx是域名，yy是username，zz是仓库名。

即使开启了全局的runner。每个仓库本身的action还是需要手动去打开的。

到仓库的设置里打开action即可。



# nektos/act分析

https://github.com/nektos/act

这个是gitea的action的

https://nektosact.com/

