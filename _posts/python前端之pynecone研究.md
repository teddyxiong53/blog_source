---
title: python前端之pynecone研究
date: 2023-01-20 22:47:31
tags:
	- Python

---



我用的掘金的浏览器插件给我推荐了这个项目

https://github.com/pynecone-io/pynecone

看起来是跟pywebio类似的东西。研究一下。

# 安装及运行

安装：

```
pip3 install -U pynecone-io
```

得到一个命令，叫pc。

创建一个项目。

```
mkdir myapp
cd myapp
pc init
```

如果是第一次运行pc这个命令，这个命令会自动下载安装bun这个js运行时。

这个命令会初始化这样的目录结构：

```
.
├── assets
│   └── favicon.ico
├── myapp
│   ├── __init__.py
│   ├── myapp.py
└── pcconfig.py

```

默认监听在3000端口。



看了一下代码，感觉比pywebio使用上要复杂一些，但是带来的好处感觉不出来。

先不学了。



# 相关资料

这个是他们的官网的代码，也是用pynecone写的。

https://github.com/pynecone-io/pcweb

这个的官方的example。

https://github.com/pynecone-io/pynecone-examples

# 参考资料

1、官方文档

https://pynecone.io/docs/getting-started/introduction