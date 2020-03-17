---
title: 渗透之mhn搭建
date: 2020-03-14 14:55:28
tags:
	- 渗透

---

1

自己在服务器上搭建一个mhn看看。

它可以快速部署、使用，也能够快速的从节点收集数据。

mhn中文名称叫现代密网。

它简化了蜜罐的部署，同时便于收集和统计蜜罐的数据。

mhn提供了多种蜜罐，你只需要复制执行一些命令，就可以完成蜜罐的部署。

而蜜罐的数据的收集，是靠开源的hpfeeds协议来获取。



mhn服务器的要求：



把mhn的提交日志看一遍。

项目创建于2013年12月20日。

最开始加进来的就是flask。

通过flask搭建的web应用，提供了一些http api，你可以用来：

1、下载一个部署脚本。

2、连接和注册。

3、下载snort规格。

4、发送入侵检测日志。

允许admin：

1、查看攻击列表。

2、管理snort规则。



mhn可以在Ubuntu16.04上运行。

安装：

```
git clone https://github.com/pwnlandia/mhn.git
./install.sh
```

install.sh这个脚本写得比较简单好懂。

支持的系统就写了debian和centos。

因为看到条件判断是这样写的：

```
if [ -f /etc/debian_version ]; then
if [ -f /etc/redhat-release ]; then
```

有让你选择是否继承splunk。这个是一个公司提供的服务。

Splunk Universal Forwarder 8.0.2.1 Remote Data Collection

进行数据转发的。

看了脚本内容，发现对路径写得比较死。必须放在/opt/mhn目录下。

感觉脚本写得还是不够健壮。执行过程中出了不少的错误。

```
+ bash install_mongo.sh
+ '[' -f /etc/debian_version ']'
++ lsb_release -r -s
+ '[' 2020.1 == 14.04 ']'
++ lsb_release -r -s
+ '[' 2020.1 == 16.04 ']'
++ lsb_release -r -s
+ '[' 2020.1 == 18.04 ']'
+ echo -e 'ERROR: Unknown OS\nExiting!'
ERROR: Unknown OS
Exiting!
```

我安装在ecs里的明明是Ubuntu16.04，但是不知道为什么lsb_release得到的不是这个字符串。

改脚本里的判断。继续安装看看。

mongodb又起不来。

算了。还是改成用docker来运行吧。

```
RUN  sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN  apt-get clean
```

```
docker build -t mhn .
```



docker运行也出错。我在本机的Ubuntu笔记本上用docker安装试一下。

本地docker安装正常。

这样运行：

```
sudo docker run -i -p 10000:10000 -p 80:80 -p 3000:3000 -p 8089:8089 \
-e SUPERUSER_EMAIL=1073167306@qq.com \
-e SUPERUSER_PASSWORD=123456 \
-e SERVER_BASE_URL="http://172.16.2.168 " \
-e HONEYMAP_URL="http://172.16.2.168:3000" \
mhn
```

但是怎么访问使用呢？





参考资料

1、Mhn现代蜜网

https://ipot.sec-wiki.com/article/2015-05-07-mhn.html