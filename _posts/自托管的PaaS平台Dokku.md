---
title: 自托管的PaaS平台Dokku
date: 2024-05-09 19:53:11
tags:
	- python
---

--

# 简介

Dokku 是一个自托管的平台即服务（PaaS）工具，它可以让你在自己的服务器上轻松部署和管理应用程序。以下是 Dokku 的一些主要特点和功能：

1. **轻量级和简单易用：** Dokku 是一个轻量级的 PaaS 工具，使用简单、易于部署和管理。它的设计灵感来自于 Heroku，提供了类似的部署体验，但更加灵活和自由。

2. **基于 Docker：** Dokku 基于 Docker 和 Docker 镜像构建，使用 Docker 容器来隔离和运行应用程序。它利用了 Docker 的轻量级虚拟化技术，使得每个应用程序都运行在独立的容器中，并且可以轻松地构建和部署自定义的 Docker 镜像。

3. **支持多种编程语言和框架：** Dokku 支持多种编程语言和框架，包括 Python、Node.js、Ruby、Go 等。你可以使用 Dokku 来部署和管理各种类型的应用程序，从简单的静态网站到复杂的 Web 应用程序都可以轻松应对。

4. **插件系统：** Dokku 提供了丰富的插件系统，可以扩展和定制其功能。你可以通过安装插件来添加额外的功能和特性，例如数据库支持、日志管理、监控和警报等。

5. **自动化部署：** Dokku 支持自动化部署，可以通过 Git 或其他版本控制系统来触发部署过程。你可以将应用程序的代码存储在 Git 仓库中，并使用 Dokku 来自动构建和部署应用程序。

6. **易于扩展：** Dokku 提供了一系列命令行工具和 API 接口，可以方便地管理和监控应用程序。你可以使用命令行工具来执行各种操作，例如部署、启动、停止、重启应用程序等。

总的来说，Dokku 是一个简单、灵活、易于部署和管理的自托管 PaaS 工具，适用于个人开发者、小团队和中小型企业，可以帮助他们快速构建和部署应用程序，提高开发和部署效率。

# 发展历史

Dokku 的发展历史可以追溯到 2013 年左右，以下是 Dokku 主要的发展历程：

1. **初期阶段（2013年）：** Dokku 最初由 Jeff Lindsay 创建，灵感来自于 Heroku。它最初是一个开源项目，旨在提供类似于 Heroku 的自托管部署平台。初期版本的 Dokku 主要关注于 Docker 容器技术的集成和简化。

2. **开源社区贡献（2014年）：** 随着 Dokku 的知名度和用户基础的增长，越来越多的开发者开始为 Dokku 做出贡献。社区贡献的插件和功能不断丰富，使得 Dokku 变得更加强大和灵活。

3. **稳定版本发布（2015年）：** 在经过一段时间的开发和测试之后，Dokku 发布了稳定版本，正式向用户提供了稳定可靠的自托管部署解决方案。这个版本增加了对 Docker 和容器化技术的更多支持，并改进了用户界面和部署体验。

4. **持续改进和增强（2016年至今）：** 自发布稳定版本以来，Dokku 持续进行改进和增强，引入了更多的功能和特性。这些改进包括对多种编程语言和框架的支持、更好的插件系统、更简单的部署流程等。Dokku 还积极响应用户的反馈和需求，不断改进和优化产品。

总的来说，Dokku 作为一个开源项目，经历了多年的发展和演变，逐渐成为了一个功能强大、稳定可靠的自托管部署平台。它受到了广大开发者和用户的欢迎和青睐，为他们提供了方便快捷的应用程序部署解决方案。随着技术的不断发展和用户需求的变化，Dokku 仍然在不断改进和演进，致力于为用户提供更好的产品和服务。

# 官网文档

https://dokku.com/docs/getting-started/installation/

# 安装

```
# 下载官方安装脚本
wget -NP . https://dokku.com/install/v0.34.8/bootstrap.sh
sudo DOKKU_TAG=v0.34.8 bash bootstrap.sh
```



```
! If using virtualhost routing is desired (eg. my-app => my-app.dokku.me), set a global domain for your server:

     dokku domains:set-global dokku.me
```



```
cat ~/.ssh/id_rsa.pub | ssh root@SERVER_IP dokku ssh-keys:add admin
# 添加后打印
SHA256:P9Kf4xDy+zsP/hP+pvzOMxIxnOMLPZHQOx+TjSPzy0Q
```



```
dokku domains:set-global SERVER_IP
# SERVER_IP 这里是你服务器的ip或者域名。
```

- 若使用 IP 地址，可通过 `sslip.io` 生成动态子域名（如 `10.0.0.2.sslip.io`）



通过插件安装数据库支持

```
# 安装 PostgreSQL 插件
sudo dokku plugin:install https://github.com/dokku/dokku-postgres.git

# 创建数据库实例
dokku postgres:create mydatabase
dokku postgres:link mydatabase myapp
```

以nodejs的部署为例。

```
git clone https://github.com/heroku/node-js-sample.git
cd node-js-sample
git remote add dokku dokku@your-domain:test
git push dokku master
```

我部署这个的时候，卡了很久，应该网络有问题。

容器内部不能使用外面的代理？

如果push的时候，中途取消。

需要unlock，不如再次直接push会失败。

```
ssh dokku@xxx.sslip.io apps:unlock test
```

xxx是我的公网ip地址。

最后还是推送完成了。得到这样的访问地址：

http://test.xxx.sslip.io/

所以这个test，就是应用的名字。

