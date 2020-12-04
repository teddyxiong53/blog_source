---
title: WordPress（一）docker搭建
date: 2018-01-26 10:50:48
tags:
	- WordPress
	- docker

---



想要研究一下WordPress，但是不想在系统里安装，前段时间刚好学习了docker，就用docker环境来搭建。

一个原则：我不想拉一堆的docker 镜像。我想要一个镜像解决。

不过，好像没有看到这种现成的镜像，我就自己写Dockerfile来做一个。

2020年12月2日16:23:20

其实有的。

拉取测试看看。

docker-compose.yml 文件。

```
version: '3.3'
services:
  db:
     image: mysql:5.7
     container_name: "wordpress_mysql"
     volumes:
       - $PWD/db:/var/lib/mysql
     restart: always
     environment:
       MYSQL_ROOT_PASSWORD: 040253
       MYSQL_DATABASE: wordpress
       MYSQL_USER: root
       MYSQL_PASSWORD: 040253
  wordpress:
     depends_on:
       - db
     image: wordpress:latest
     container_name: "wordpress"
     ports:
       - "80:80"
     restart: always
     environment:
       WORDPRESS_DB_HOST: db:3306
       WORDPRESS_DB_USER: root
       WORDPRESS_DB_PASSWORD: 040253
       WORDPRESS_DB_NAME: wordpress
     volumes:
       - $PWD/wp-content:/home/teddy/wordpress-site

```

然后docker-compose up就可以。

数据库连不上。



参考资料

1、

https://www.cnblogs.com/superzhan/p/11791140.html

