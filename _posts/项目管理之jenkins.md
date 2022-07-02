---
title: 项目管理之jenkins
date: 2021-04-08 17:10:07
tags:
	- 项目管理

---

--

https://github.com/jenkinsci/jenkins

先看看docker搭建一个。

```
docker pull jenkins/jenkins:lts
```

运行

```
docker run -p 8080:8080 -p 5000:5000 --name jenkins \
-u root \
-v /home/amlogic/jenkins_home:/var/jenkins_home \
-d jenkins/jenkins:lts
```

使用这个命令查看默认的密码，是随机字符串

```
docker logs jenkins
```

如下面这样

```

Jenkins initial setup is required. An admin user has been created and a password generated.
Please use the following password to proceed to installation:

337dbc2420c341e1b91fd56450bee01e

```

然后访问8080端口，会弹出窗口让你输入密码，把上面的随机密码粘贴进去。

下一步是安装插件，使用默认的插件。这一步需要一点时间。

然后就是创建一个管理员用户。

当前版本是：Jenkins 2.263.2

但是创建这一步会卡住很久。

刷新页面，继续用admin进行操作。

然后把admin的密码改了。

登陆进去，进行系统设置，发现有很多的插件安装没有成功。

直接选择升级到新版本。

然后我在gitlab里创建一个c_test的项目。

里面就放一个main.c。里面打印一行。

jenkins也创建一个项目。选择构建行为是shell。写上:gcc main.c

然后执行构建。

gcc找不到。进入到容器，安装gcc。

执行构建，代码是放在这个目录下了。

```
/var/jenkins_home/workspace/c_test
```

# jenkins跟gitlab结合





# 参考资料

1、

https://blog.csdn.net/wgl04193410/article/details/108615795

