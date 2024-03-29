---
title: AList研究
date: 2024-03-20 10:26:17
tags:
	- 玩机

---

--

# 基本信息

代码

https://github.com/alist-org/alist

官网：

https://alist.nn.ci/zh/guide/#support-storage

典型网站：

http://sbtx.cc/

# alist在windows下安装使用

https://blog.csdn.net/stone0823/article/details/131776112

# webdav 是什么

WebDAV（Web Distributed Authoring and Versioning）是一种基于HTTP/HTTPS协议的扩展，

用于在远程==服务器上进行文件管理和协作==。

它允许用户通过网络对远程服务器上的文件进行读写操作，类似于使用本地文件系统。

WebDAV 最初由IETF（Internet Engineering Task Force）开发，并于1999年被批准为RFC 2518标准。

其目的是使互联网上的用户能够==方便地共享和编辑网络上的文档。==

WebDAV的主要功能包括：

1. **文件管理：** 用户可以通过WebDAV协议在远程服务器上创建、删除、移动和重命名文件和文件夹。
  
2. **远程编辑：** 用户可以通过支持WebDAV的应用程序直接在远程服务器上编辑文档，而无需先将其下载到本地计算机。

3. **属性管理：** WebDAV允许用户为文件和文件夹定义自定义属性，并对这些属性进行管理。

4. **锁定机制：** 它提供了锁定机制，以防止多个用户同时编辑同一文件导致的冲突。

WebDAV通常用于构建基于Web的文件管理系统，或用于实现基于云存储的协作工具，例如在线文档编辑器和团队协作平台。

## 相关的开源软件

以下是一些与WebDAV相关的开源软件：

1. **Apache HTTP Server：** Apache是一个流行的开源Web服务器，它提供了对WebDAV的支持，可以通过模块启用此功能。

2. **nginx：** Nginx是另一个流行的开源Web服务器，它也可以通过相应的模块支持WebDAV功能。

3. **OwnCloud：** OwnCloud是一个开源的云存储平台，它提供了WebDAV协议的支持，允许用户通过网络进行文件管理和协作。

4. **Nextcloud：** Nextcloud是OwnCloud的一个分支，它也是一个开源的云存储和协作平台，提供了WebDAV支持以便用户访问和管理文件。

5. **PyDAV：** PyDAV是一个用Python编写的开源WebDAV服务器实现，可以用于搭建自己的WebDAV服务器。

6. **SabreDAV：** SabreDAV是一个用PHP编写的开源WebDAV服务器框架，它可以帮助开发者构建符合WebDAV标准的服务器应用程序。

7. **OpenKM：** OpenKM是一个开源的文档管理系统，它提供了对WebDAV的支持，可以通过WebDAV协议访问和管理存储在OpenKM中的文件。

这些开源软件提供了搭建和管理WebDAV服务器或集成WebDAV功能到应用程序中的解决方案。

