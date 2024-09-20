---
title: docker（1）
date: 2020-12-05 11:32:30
tags:
	- docker
---

1

这个主要是把docker日常的疑问解答汇总起来。

1. 正确做法就是两个容器。每个容器只干一件事情
2. docker 有 log driver，可以接 rsyslog/logstash
3. nginx 用官方镜像，配置文件单独拿出来，同时发送配置文件 + docker-compose.yml 到远程服务器，在 docker-compose 里面用 volume 挂进去

4. build 的 tag 不要用一样的 pho-fpm:v1，使用 my-project-php:commit_hash 或者 git tag 作为标记，每次不一样

要进行精细管理，不要的容器和镜像都及时删除掉。





# 进入正在运行的容器的shell

```
docker exec -it 5a7b46c7fe5b bash
```

5a7b46c7fe5b是容器的id。

# docker容器没有起来，怎么查看日志

```
docker logs mysql-test
```

mysql-test是容器的名字。



# docker安装mysql

运行

```
docker run -itd --name mysql-test -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123456 mysql
```

访问

```
 Can't connect to local MySQL server through socket '/var/run/mysqld/mysqld.sock'
```

进入容器的shell

```
 docker exec -it mysql-test /bin/bash
```

看里面的/etc/mysql/my.conf内容：

```
[mysqld]
pid-file        = /var/run/mysqld/mysqld.pid
socket          = /var/run/mysqld/mysqld.sock
datadir         = /var/lib/mysql
secure-file-priv= NULL

# Custom config should go here
!includedir /etc/mysql/conf.d/
```

这里可以看到mysqld.sock的目录是在/var/run/mysqld目录下，

但是这个目录，我们并没有挂载主机目录，

下面我们重新运行mysql容器，挂载相应的容器，如下所示：

```
docker run --name=mysql-test -it -p 3306:3306 -v /opt/data/mysql/mysqld:/var/run/mysqld -v /opt/data/mysql/db:/var/lib/mysql -v /opt/data/mysql/conf:/etc/mysql/conf.d -v /opt/data/mysql/files:/var/lib/mysql-files -e MYSQL_ROOT_PASSWORD=040253 --privileged=true -d mysql
```

没有起来，看docker的错误日志：

```
2020-12-05T06:06:39.269714Z 0 [ERROR] [MY-010946] [Server] Failed to start mysqld daemon. Check mysqld error log.
2020-12-05 06:06:39+00:00 [ERROR] [Entrypoint]: Unable to start server.
```

去掉-d选项再运行。

看到错误。

```
[ERROR] [MY-011300] [Server] Plugin mysqlx reported: 'Setup of socket: '/var/run/mysqld/mysqlx.sock' failed, can't create lock file /var/run/mysqld/mysqlx.sock.lock'
```



我下载5.7版本的吧。

```
docker pull mysql:5.7
```

我创建这样的目录，来存放挂载的数据。

```
~/docker-volume/mysql
```

运行：

```
docker run -d -p 3306:3306  -e MYSQL_ROOT_PASSWORD=040253 --name mysql-test -v /root/docker-volume/mysql/my.cnf:/etc/mysql/my.cnf -v /root/docker-volume/mysql/db:/var/lib/mysql mysql:5.7
```

但是在主机里连接还是提示

Can't connect to local MySQL server through socket '/var/run/mysqld/mysqld.sock'

进入到docker里，可以看到这个文件。

```
root@a8b11d7f2d42:/var/run/mysqld# ls -lh
total 4.0K
srwxrwxrwx 1 mysql mysql 0 Dec  5 06:23 mysqld.sock
```

在stackoverflow上找到一个简单办法来解决。

指定tcp方式，就没有问题了。

```
mysql -u root -p --protocol=tcp
```

但是这个无法用WordPress连接过来。

算了mysql，我还是用原生的。这个是一定需要的。

就安装5.7版本。



https://stackoverflow.com/questions/23234379/installing-mysql-in-docker-fails-with-error-message-cant-connect-to-local-mysq



https://blog.csdn.net/zzddada/article/details/94742832



# docker安装WordPress

这个需要你另外在拉取mysql的。

```
docker run -it -e WORDPRESS_DB_HOST=localhost:3306 -e WORDPRESS_DB_USESR=root -e WORDPRESS_DB_PASSWORD=040253 -p 8080:80 -d wordpress  
```



```
mkdir -p $HOME/.config/wordpress
```

这个的关键是自己写docker-compose来做。

wordpress镜像默认是带了apache的。wordpress:fpm这个版本是才是纯的。

但是这个弄起来也问题较多。

做得比较复杂。



这篇文章才完整全面。

把这篇文章吃透。

https://xzos.net/docker-install-wordpress/



这个是docker官网的教程。

https://docs.docker.com/compose/wordpress/

直接把官网的贴过了。马上就运行正常。

这样安装是真的非常简单。

但是如何迁移数据呢？



# 官方例子

https://docs.docker.com/samples/



# docker-ce和docker-io的区别

`docker-ce` is provided by docker.com, `docker.io` is provided by Debian.

# 修改docker的配置

是在/etc/docker/daemon.json里进行。

修改后要重启docker服务。

# 运维角度看docker

从运维的角度来说，我们需要掌握 Docker 的镜像下载、运行新的容器、登录新容器、在容器内运行命令，以及销毁容器。

当我们安装 Docker 的时候，会涉及两个主要组件：Docker 客户端和 Docker daemon（有时也被称为“服务端”或者“引擎”）。

daemon 实现了 Docker 引擎的 API。



使用 Linux 默认安装时，客户端与 daemon 之间的通信是通过本地 IPC/UNIX Socket 完成的（/var/run/docker.sock）



# 查看系统的docker信息

docker system info

```
Containers: 9
 Running: 2
 Paused: 0
 Stopped: 7
Images: 93
Server Version: 18.09.7
Storage Driver: overlay2
 Backing Filesystem: extfs
 Supports d_type: true
 Native Overlay Diff: true
```

选择存储驱动并正确地配置在 Docker 环境中是一件重要的事情，特别是在生产环境中。



大部分 Linux 存储驱动不需要或需要很少的配置。但是，Device Mapper 通常需要合理配置之后才能表现出良好的性能。

如果需要的是开箱即用并且对性能没什么要求，那么这种方式是可行的。但这并不适用于生产环境。实际上，默认方式的性能很差，并不支持生产环境。





# swarm是什么

Swarm 是 Docker 官方提供的一款集群管理工具，

其主要作用是把若干台 Docker 主机抽象为一个整体，

并且通过一个入口统一管理这些 Docker 主机上的各种 Docker 资源。

Swarm 和 Kubernetes 比较类似，但是更加轻，具有的功能也较 kubernetes 更少一些。



Docker Swarm 包含两方面：

一个企业级的 Docker 安全集群，以及一个微服务应用编排引擎。

集群方面，Swarm 将一个或多个 Docker 节点组织起来，使得用户能够以集群方式管理它们。

以往，Docker Swarm 是一个基于 Docker 引擎之上的独立产品。

自 Docker 1.12 版本之后，它已经完全集成在 Docker 引擎中，执行一条命令即可启用。

到 2018 年，除了原生 Swarm 应用，它还可以部署和管理 Kubernetes 应用。



从集群角度来说，一个 Swarm 由一个或多个 Docker 节点组成。

这些节点可以是物理服务器、虚拟机、树莓派（Raspberry Pi）或云实例。

唯一的前提就是要求所有节点通过可靠的网络相连。



节点会被配置为管理节点（Manager）或工作节点（Worker）。

管理节点负责集群控制面（Control Plane），进行诸如监控集群状态、分发任务至工作节点等操作。

工作节点接收来自管理节点的任务并执行。



关于集群管理，最大的挑战在于保证其安全性。搭建 Swarm 集群时将不可避免地使用 TLS，因为它被 Swarm 紧密集成。

在安全意识日盛的今天，这样的工具值得大力推广。Swarm 使用 TLS 进行通信加密、节点认证和角色授权。自动密钥轮换（Automatic Key Rotation）更是锦上添花！其在后台默默进行，用户甚至感知不到这一功能的存在。





Docker Swarm简介

http://c.biancheng.net/view/3176.html



人们认为容器不擅长持久化工作或者持久化数据，很大程度上是因为容器在非持久化领域上表现得太出色。



容器支持的重启策略包括 always、unless-stopped 和 on-failed。

always 策略是一种简单的方式。除非容器被明确停止，比如通过 `docker container stop` 命令，否则该策略会一直尝试重启处于停止状态的容器。



Docker 的核心思想就是如何将应用整合到容器中，并且能在容器中实际运行。

将应用整合到容器中并且运行起来的这个过程，称为“容器化”（Containerizing），有时也叫作“Docker化”（Dockerizing）。



应用容器化的过程大致分为如下几个步骤：

- 获取应用代码。
- 分析 Dockerfile。
- 构建应用镜像。
- 运行该应用。
- 测试应用。
- 容器应用化细节。
- 生产环境中的多阶段构建。
- 最佳实践。

# 减小镜像体积



对于 Docker 镜像来说，过大的体积并不好！

越大则越慢，这就意味着更难使用，而且可能更加脆弱，更容易遭受攻击。

鉴于此，Docker 镜像应该尽量小。对于生产环境镜像来说，目标是将其缩小到仅包含运行应用所必需的内容即可。问题在于，生成较小的镜像并非易事。

不同的 Dockerfile 写法就会对镜像的大小产生显著影响。



常见的例子是，每一个 RUN 指令会新增一个镜像层。因此，通过使用 && 连接多个命令以及使用反斜杠（\）换行的方法，将多个命令包含在一个 RUN 指令中，通常来说是一种值得提倡的方式。

另一个问题是开发者通常不会在构建完成后进行清理。当使用 RUN 执行一个命令时，可能会拉取一些构建工具，这些工具会留在镜像中移交至生产环境。

有多种方式来改善这一问题——比如常见的是采用建造者模式（Builder Pattern）。但无论采用哪种方式，通常都需要额外的培训，并且会增加构建的复杂度。

建造者模式需要至少两个 Dockerfile，一个用于开发环境，一个用于生产环境。



首先需要编写 Dockerfile.dev，它基于一个大型基础镜像（Base Image），拉取所需的构建工具，并构建应用。

接下来，需要基于 Dockerfile.dev 构建一个镜像，并用这个镜像创建一个容器。

这时再编写 Dockerfile.prod，它基于一个较小的基础镜像开始构建，并从刚才创建的容器中将应用程序相关的部分复制过来。

整个过程需要编写额外的脚本才能串联起来。

这种方式是可行的，但是比较复杂。



多阶段构建（Multi-Stage Build）是一种更好的方式！

多阶段构建能够在不增加复杂性的情况下优化构建过程。



首先注意到，Dockerfile 中有 3 个 FROM 指令。每一个 FROM 指令构成一个单独的构建阶段。

各个阶段在内部从 0 开始编号。不过，示例中针对每个阶段都定义了便于理解的名字。

- 阶段 0 叫作 storefront。
- 阶段 1 叫作 appserver。
- 阶段 2 叫作 production。



storefront 阶段拉取了大小超过 600MB 的 node:latest 镜像，然后设置了工作目录，复制一些应用代码进去，然后使用 2 个 RUN 指令来执行 npm 操作。

这会生成 3 个镜像层并显著增加镜像大小。指令执行结束后会得到一个比原镜像大得多的镜像，其中包含许多构建工具和少量应用程序代码。

appserver 阶段拉取了大小超过 700MB 的 maven:latest 镜像。然后通过 2 个 COPY 指令和 2 个 RUN 指令生成了 4 个镜像层。

这个阶段同样会构建出一个非常大的包含许多构建工具和非常少量应用程序代码的镜像。

production 阶段拉取 java:8-jdk-alpine 镜像，这个镜像大约 150MB，明显小于前两个构建阶段用到的 node 和 maven 镜像。

这个阶段会创建一个用户，设置工作目录，从 storefront 阶段生成的镜像中复制一些应用代码过来。

之后，设置一个不同的工作目录，然后从 appserver 阶段生成的镜像中复制应用相关的代码。最后，production 设置当前应用程序为容器启动时的主程序。

重点在于 COPY --from 指令，它从之前的阶段构建的镜像中仅复制生产环境相关的应用代码，而不会复制生产环境不需要的构件。

还有一点也很重要，多阶段构建这种方式仅用到了一个 Dockerfile，并且 `docker image build` 命令不需要增加额外参数。

最终，无须额外的脚本，仅对一个单独的 Dockerfile 执行 `docker image build` 命令，就创建了一个精简的生产环境镜像。

多阶段构建是随 Docker 17.05 版本新增的一个特性，用于构建精简的生产环境镜像。



# 数据迁移

我在一台机器上搭建的网站，基于docker。想要迁移到另外一个机器上，保证数据不丢失，应该怎么操作？

这篇文章讲得很清楚。

http://pbeta.me/docker-volume-migrate/

# 给Dockerfile传递参数

好的，下面是一个简单的 Dockerfile 示例，它将创建一个基于 Alpine Linux 的镜像，并在其中创建一个新用户，并打印该用户的 UID 和 GID。

```Dockerfile
FROM alpine:latest

ARG MY_UID
ARG MY_GID

# 添加构建参数传递的用户和组
RUN addgroup -g ${MY_GID} mygroup && \
    adduser -D -u ${MY_UID} -G mygroup myuser

# 打印用户和组的信息
RUN echo "UID of myuser: $(id -u myuser)" && \
    echo "GID of myuser: $(id -g myuser)"

USER myuser

CMD ["sh"]
```

你可以使用以下命令来构建这个 Docker 镜像，并传递 UID 和 GID 参数：

```bash
docker build --build-arg MY_GID=$(id -g) --build-arg MY_UID=$(id -u) -t my_test_image .
```

然后，你可以运行这个镜像，并进入容器进行测试：

```bash
docker run -it --rm my_test_image
```

这样你就可以在容器内看到用户和组的 UID 和 GID 了。

# 确保docker内外uid一样来确保修改文件的权限问题

就看这个就好了。靠gosu这个工具来做的。

https://github.com/T-Firefly/buildroot-builder/blob/master/Dockerfile

我基于这个进行的测试：

```
docker build  -t my_test_image .
docker run -it --rm  -e USER_ID=$UID -v $(pwd):/home/br my_test_image
```

# 基于docker搭建统一的开发环境

大多数人可能都遇到过这样一个问题，在本地开发好功能后，部署到服务器，或者其他人拉到本地接着开发时，会出现功能用不了的情况。

大多数时候是由于系统不同，依赖出现差异而导致的。因此，为了解决这个问题，基于 Docker 构建统一开发环境的需求便产生了。

## 使用 Docker 的好处

- 部署方便：平常要搭建环境常常需要耗费几个小时，而且，对于团队协作时来说，每有新人进来，都需要浪费这可以避免的时间，而且搭建环境时，也常常会产生的各种问题，导致项目代码运行异常。如果使用了 Docker 的话，只需最开始的人写好开发容器，其他人只需要 pull 下来，即可完成项目环境的搭建，能有效避免无意义的时间浪费。
- 隔离性：我们时常会在一台电脑部署多个项目环境，若是直接安装的话，彼此间有可能会造成干扰，比如一个项目需要 Node.js 14，有的又需要 Node.js 12，若是直接在本机部署的话，总是不能共存的，而是用 Docker 的话，则可以避免该问题。Docker 还能确保每个应用程序只使用分配给它的资源（包括 CPU、内存和磁盘空间）。一个特殊的软件将不会使用你全部的可用资源，要不然这将导致性能降低，甚至让其他应用程序完全停止工作。



### 编写 Dockerfile

安装完 Docker 之后，接下来我们便可以来编写我们自己的项目开发环境了。本文将以前端开发环境为例，构建 Dockerfile。

包含环境：

- node.js 14.17
- npm 6.14
- yarn 1.22



# docker  run --privileged 这个参数的作用

`--privileged` 参数是在运行 Docker 容器时可选的一个选项。它的作用是提供容器内部的进程对主机系统的更高权限，允许容器中的进程访问主机上的特权操作。

具体来说，`--privileged` 参数将允许容器内的进程访问主机上的所有设备，并且能够执行特权操作，比如修改主机上的网络配置、加载内核模块等。这样的权限可能会对主机的安全性造成潜在的风险，因此建议谨慎使用。

通常情况下，只有在确实需要在容器内执行特权操作，并且理解可能带来的安全风险时，才会使用 `--privileged` 参数。

# -v /var/run/docker.sock:/var/run/docker.sock 这样有什么作用

`-v /var/run/docker.sock:/var/run/docker.sock` 这个参数用于将 Docker 守护进程的 UNIX 套接字（UNIX socket）绑定到容器内的相同路径上。这样做的作用是让容器内的进程可以与宿主机上的 Docker 守护进程进行通信。

具体来说，这个参数通常用于在容器内部运行 Docker CLI 命令，使得容器内的命令可以直接与宿主机上的 Docker 引擎进行交互。这样做可以实现一些特定的功能，比如在容器内启动其他容器、管理容器、构建镜像等。

总之，通过将 Docker 守护进程的 UNIX 套接字映射到容器内部，可以实现容器内与宿主机上 Docker 引擎的交互，从而使得容器内的操作可以直接影响到宿主机上的 Docker 守护进程。

# dockerfile里的cmd和entrypoint区别

`CMD` 和 `ENTRYPOINT` 是 Dockerfile 中用来指定容器启动时执行的命令的指令，但它们有不同的用途和行为。

### `CMD`

- **用途**：用于提供容器启动时的默认命令和参数。
- **可被覆盖**：如果在 `docker run` 命令中提供了其他命令或参数，`CMD` 会被覆盖。
- **格式**：
  - **Shell 格式**：`CMD command param1 param2`
  - **Exec 格式**：`CMD ["executable", "param1", "param2"]`

#### 示例：

```dockerfile
FROM ubuntu
CMD ["echo", "Hello, World!"]
```

### `ENTRYPOINT`

- **用途**：用于定义容器的主命令，通常是容器的主要功能。
- **不易被覆盖**：如果在 `docker run` 中提供了其他命令，这些命令会作为参数传递给 `ENTRYPOINT` 指定的命令，而不会覆盖它。
- **格式**：
  - **Shell 格式**：`ENTRYPOINT command param1 param2`
  - **Exec 格式**：`ENTRYPOINT ["executable", "param1", "param2"]`

#### 示例：

```dockerfile
FROM ubuntu
ENTRYPOINT ["echo"]
```

### 结合使用

可以将 `ENTRYPOINT` 和 `CMD` 结合使用，以便提供默认参数给 `ENTRYPOINT`：

```dockerfile
FROM ubuntu
ENTRYPOINT ["echo"]
CMD ["Hello, World!"]
```

在这种情况下，`docker run` 会执行 `echo Hello, World!`。如果在 `docker run` 中提供其他参数，例如：

```bash
docker run my-image "Goodbye!"
```

则会执行 `echo Goodbye!`。

### 总结

- **`CMD`** 是默认命令，可以被覆盖。
- **`ENTRYPOINT`** 是主要命令，不易被覆盖，适合用于实现容器的主要功能。



# 通过docker包装的方式运行一下echo hello ，跟直接本地执行echo hello，效率对比

通过 Docker 容器运行 `echo hello` 与直接在本地执行 `echo hello` 的效率对比可以从以下几个方面进行分析：

### 1. 启动时间

- **Docker 容器**：
  - 启动 Docker 容器需要一定的时间，包括创建容器、分配网络和文件系统等资源。
  - 即使是一个简单的命令，Docker 也需要处理这些开销。

- **本地执行**：
  - 直接在命令行中执行 `echo hello` 几乎是瞬时的，因为不需要任何额外的开销。

### 2. 资源消耗

- **Docker 容器**：
  - Docker 会消耗额外的资源（如内存和 CPU）来管理容器环境。
  - 每次运行都需要加载 Docker 引擎及其相关资源。

- **本地执行**：
  - 直接执行 `echo hello` 只占用非常少的系统资源，几乎可以忽略不计。

### 3. 输出延迟

- **Docker 容器**：
  - 由于启动和环境设置，可能会有轻微的输出延迟。

- **本地执行**：
  - 输出几乎是即时的。

### 4. 总结

- **效率**：
  - 直接在本地执行 `echo hello` 效率更高，几乎没有延迟和开销。
  - 使用 Docker 容器运行 `echo hello` 的效率较低，主要由于容器启动和资源管理的开销。

### 结论

对于简单的命令，如 `echo hello`，直接在本地执行明显更高效。如果只是需要执行简单的命令，Docker 的开销会使得其效率较低。Docker 更适合用于需要隔离、依赖管理或多环境部署的复杂应用场景。

如果您还有其他问题或想要更深入的讨论，请告诉我！

# buildroot docker编译环境搭建

https://hub.docker.com/r/amllinux/buildroot



# FROM scratch 代表了什么

`FROM scratch` 是 Dockerfile 中的一个特殊指令，表示构建一个完全空的基础镜像。它通常用于以下几个场景：

### 1. **构建最小化镜像**

- **无任何基础层**：使用 `FROM scratch` 创建的镜像不包含任何操作系统层或预装的库。这使得最终镜像的体积非常小，适合对安全性和性能有高要求的应用。

### 2. **静态编译的应用**

- **静态链接**：通常与 Go 或 Rust 等语言一起使用，这些语言能够生成静态链接的可执行文件。这样的可执行文件不依赖外部库，可以直接在 `scratch` 镜像中运行。

### 3. **提高安全性**

- **攻击面减小**：由于没有操作系统或其他软件的支持，使用 `FROM scratch` 的镜像可以减少潜在的安全漏洞，从而提高应用的安全性。

### 示例

下面是一个简单的 Dockerfile 示例，展示了如何使用 `FROM scratch`：

```dockerfile
FROM scratch
COPY myapp /myapp
CMD ["/myapp"]
```

在这个示例中，`myapp` 是一个静态编译的二进制文件，直接从 `scratch` 镜像中运行。

### 总结

使用 `FROM scratch` 适合需要高效、轻量和安全的容器化应用，特别是在构建静态链接的可执行文件时。

# 参考资料

1、怎么才是 docker 最佳实践

https://www.v2ex.com/t/542393