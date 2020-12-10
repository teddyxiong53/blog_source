---
title: 物联网之ActorCloud
date: 2020-12-09 16:28:30
tags:
	- electron
---



说明：最后没有跑起来。有些代码没有开源。

ActorCloud是一个物联网后台程序。

代码：

https://github.com/actorcloud/ActorCloud

先看看在单节点上部署。

# 安装依赖

## TimescaleDB

这个是基于postgresql的。需要postgresql的版本高于10，我的已经满足这个调节。

安装timescaledb插件

```
# Add PPA
$ sudo add-apt-repository ppa:timescale/timescaledb-ppa
$ sudo apt-get update
# Now install appropriate package for PG version
$ sudo apt install -y timescaledb-postgresql-10
```

启用插件

```
sudo timescaledb-tune
```

重启postgresql

```
sudo service postgresql restart
```

进入到psql命令行，新建数据库。

```
CREATE DATABASE actorcloud;
```

新建角色。

```
CREATE USER actorcloud WITH ENCRYPTED PASSWORD '040253';
```

给这个角色分配权限。

```
ALTER ROLE "actorcloud" WITH LOGIN;  # 允许角色登录
ALTER ROLE "actorcloud" WITH SUPERUSER; # 设置角色为超级管理员
ALTER ROLE "actorcloud" WITH CREATEDB; # 允许角色创建数据库
ALTER ROLE "actorcloud" WITH CREATEROLE; # 允许角色创建角色
```

授予数据库权限。

```
grant all privileges on database actorcloud to actorcloud;
```

## emq x安装

这个是mqtt broker。

在新主机上首次安装 EMQ X 之前，需要设置 EMQ X 镜像库。 之后，您可以从镜像库安装和更新 EMQ X 。

先安装必要的工具。

```
sudo apt install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common
```

添加emqx的官方gpg密钥。

```
curl -fsSL https://repos.emqx.io/gpg.pub | sudo apt-key add -
```

验证密钥。

```
sudo apt-key fingerprint 3E640D53
```

添加仓库。

```
sudo add-apt-repository \
    "deb [arch=amd64] https://repos.emqx.io/emqx-ce/deb/ubuntu/ \
    $(lsb_release -cs) \
    stable"
```

更新一下，然后安装。

```
 sudo apt update
 sudo apt install emqx
```

但是更新失败。

```
错误:11 https://repos.emqx.io/emqx-ce/deb/ubuntu xenial/stable amd64 Packages
  Hash 校验和不符
命中:12 http://repo.aptly.info nightly InRelease    
正在读取软件包列表... 完成    
E: 仓库 “http://ppa.launchpad.net/jonathonf/python-3.6/ubuntu xenial Release” 没有 Release 文件。
N: 无法安全地用该源进行更新，所以默认禁用该源。
```

直接从官网下载安装包。

```
wget https://www.emqx.io/downloads/broker/v4.2.3/emqx-ubuntu16.04-4.2.3-x86_64.deb
```

安装成功了。



然后修改emqx的配置文件。

启动，失败。

网上找了一下，可能是emqx的版本太高了。

卸载掉当前的emq，下载文档里描述的3.1.0版本。

但是官网没有。接近的是3.2.7的。

```
wget https://www.emqx.io/downloads/broker/v3.2.7/emqx-ubuntu16.04-v3.2.7_amd64.deb
```

这样就可以启动了。

```
teddy@thinkpad:~/work/ActorCloud-study$ emqx_ctl status
Node 'emqx@127.0.0.1' is started
emqx 3.2.7 is running
```

访问emqx的dashboard，地址是类似这样：

http://192.168.1.102:18083/

用户名：admin，密码：public。

可以在emqx_dashboard.conf里修改。

进入dashboard，点击plugins，把emqx_auth_http和emqx_web_hook启动。

# rule engine安装

依赖pulsar，这个是消息队列。

```
# 获取 apache pulsar 2.2.0 安装包
$ wget https://archive.apache.org/dist/pulsar/pulsar-2.2.0/apache-pulsar-2.2.0-bin.tar.gz
# 解压(默认 /opt 目录)
$ tar -zxvf apache-pulsar-2.2.0-bin.tar.gz -C /opt
# 重命名
$ mv /opt/apache-pulsar-2.2.0 /opt/pulsar
```

压缩包下载用wget不行，在浏览器里下载。有300M之多。

然后把ActorCloud下面的deploy下面的stream目录拷贝到/opt/pulsar目录下。

改名为rule_engine。

（因为实际的目录情况跟文档描述不一样了。）



# server安装

这个需要Python3.6版本及以上的版本。

我当前已经安装好了。

安装pipenv。通过这种方式来调用pip，可以保证是安装到python3的目录下。

```
sudo python3 -m pip install pipenv
```

```
pipenv install --skip-lock
```

进入到actorcloud/server目录下，执行：

```
python3 -m pipenv install --skip-lock
```

这个会创建一个虚拟python环境，可以避免污染系统的python环境。

然后安装依赖。

```
To activate this project's virtualenv, run pipenv shell.
Alternatively, run a command inside the virtualenv with pipenv run.
```

激活虚拟环境：

```
pipenv shell
```

退出虚拟环境

```
deactivate
```

# nginx配置

把deploy下面nginx的配置，拷贝到/etc/nginx目录下。覆盖。

然后访问：http://localhost

可以看到已经是跳转到ActorCloud的页面了。

# 运行rule engine

发现跑不起来。



参考资料

1、官方中文文档

https://docs.actorcloud.io/zh/installation/single_node.html

