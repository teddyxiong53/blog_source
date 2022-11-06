---
title: flask之flask-security
date: 2022-11-05 14:01:32
tags:
	- flask

---

--

从这里开始看

https://flask-security.readthedocs.io/en/3.0.0/



flask-security可以让你快速给自己的应用添加常用的安全机制。

包括：

* 基于session的认证。
* role管理。
* password hash。
* basic http auth
* 基于token的auth。
* 基于token的账号激活。
* 基于token的密码找回。
* 用户注册。
* 登陆track。
* json/ajax支持。



你可以通过各种flask插件来实现上面这些目的。包括：

* flask-login。
* flask-mail。
* flask-principal
* flask-wtf。
* itsdangerous
* passlib

还有可选的数据库接口，有：

* flask-sqlalchemy。
* flask-mongoengine。
* flask-peewee。
* ponyorm。

# feature

## 基于session的基础auth

这个是基于flask-login来完成的。

## 基于role的访问控制

是基于flask-principal来完成。

## 密码hash

是基于passlib来完成。

## basic http auth

通过装饰器来完成。

# 配置

```
核心配置
	SECURITY_KEY
		这个实际是flask的一部分。
		flask-security用它来给所有的token签名。
	SECURITY_BLUEPRINT_NAME
		指定security对应的blueprint的名字。默认是security这字符串。
	SECURITY_URL_PREFIX
		访问security对应的blueprint的prefix url。默认是空。
	
```

# Model

涉及的数据库模型有

最少有2个对象：

```
User
Role

```

