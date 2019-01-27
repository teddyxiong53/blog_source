---
title: vue之vue-cli使用
date: 2019-01-27 15:55:27
tags:
	- vue

---



vue-cli是一个基于vue进行快速开发的完整系统。

提供这些功能：

```
1、搭建交互式的项目框架。
2、快速开始零配置原型开发。
3、一个运行时依赖，有这些特点：
	可升级
	基于webpack构建，并带有合理的默认配置。
	可以通过项目内的扩展文件进行配置。
	可以通过插件进行扩展。
4、一个丰富的官方插件集合。
5、一套完全图形化的创建和管理vue项目的用户界面。
```



这个系统的组件

```
1、cli
	是一个全局安装的npm包。提供了终端里的vue命令。
	vue create
	vue serve
	vue ui
2、cli-service cli服务
	是一个开发环境依赖。是一个npm包。
	局部安装在每个项目里。
	cli服务是基于webpack和webpack-dev-server上的。
3、cli插件。
	
```



安装：

```
1、需要nodejs版本高于8.9
```

```
npm install -g @vue/cli
```

```
teddy@ubuntu:~$ vue -V
2.9.6
```



# 快速原型开发

你可以用vue serve和vue build这2个命令对单个*.vue文件进行快速原型开发。

需要额外安装一个全局的扩展。

```
npm install -g @vue/cli-service-global
```

vue serve的缺点是他需要安装全局依赖，这使得它在不同的机器上的一致性不能得到保障。

所以只能进行快速原型开发。



创建hello-world。

```
teddy@ubuntu:~/work/test/vue$ vue create hello-world

  vue create is a Vue CLI 3 only command and you are using Vue CLI 2.9.6.
  You may want to run the following to upgrade to Vue CLI 3:
```

需要这样来升级：

```
  npm uninstall -g vue-cli
  npm install -g @vue/cli
```



# 参考资料

1、中文手册

https://cli.vuejs.org/zh/guide/