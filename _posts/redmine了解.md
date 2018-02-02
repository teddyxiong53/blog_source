---
title: redmine了解
date: 2018-02-01 21:34:25
tags:
	- redmine
---



# 安装

1、下载redmine的源代码。github上有。

2、安装配置mysql。我已经安装过了。

```
mysql -u root -p  
CREATE DATABASE redmine CHARACTER SET utf8;  
CREATE USER redmine IDENTIFIED BY 'password'; 
GRANT ALL PRIVILEGES ON *.* TO 'redmine'@'localhost' IDENTIFIED BY 'password';
```

3、安装ruby。我的ruby已经安装过了。

```
sudo apt-get install ruby rubygems ruby1.8-dev ruby1.9.1-dev libmysqlclient-dev imagemagick libmagickwand-dev
```

4、配置ruby的gem源。

查看当前的gem源。gem是ruby的包管理工具。

```
teddy@teddy-ubuntu:~$ gem source
*** CURRENT SOURCES ***

https://rubygems.org/
```

这个好像是没有文件可以编辑。只能用命令来修改。

先删除当前配置。最后那个斜杠不能少。

```
teddy@teddy-ubuntu:~$ gem source -r https://rubygems.org/
https://rubygems.org/ removed from sources
```

添加国内的源。都说淘宝的稳定，但是我连接不上，用了这个。

```
teddy@teddy-ubuntu:~$ gem sources -a http://gems.ruby-china.org/
http://gems.ruby-china.org/ added to sources
```

5、安装bundler。bundler是ruby的依赖管理工具。

```
sudo gem install bundler -V
```

6、在redmine代码目录下执行：

```
bundle install --without development test
```

但是卡住没反应。看网上说要安装ruby-dev。安装一下。





