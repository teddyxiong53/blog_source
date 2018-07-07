---
title: Python之pipenv
date: 2018-06-28 19:10:28
tags:
	- Python

---



看requests的代码里的Makefile，看到这么一句。

```
init:
	pip install pipenv --upgrade
	pipenv install --dev --skip-lock
```

pipenv是什么？从名字上看跟虚拟环境有关系的。

跟virtualenv是什么关系？



pipenv是Kenneth Reitz写的一个命令行工具。

Kenneth Reitz是requests的作者，Pipfile的主要推动者。

pipenv包括：

1、Pipfile。用来替换简陋的requirements.txt。

2、pip。

3、click。

4、requests。

5、virtualenv。



Pipfile是TOML格式，而不是简单的txt文本。

TOML是一种新的配置文件，跟ini、json这些是一个类型的东西。



一个项目对应一个Pipfile。

支持开发环境和正式环境的区别。默认提供default和development区分。

提供版本锁支持。村委Pipfile.lock。

click是Flask作者写的库。

安装：

```
sudo pip install pipenv
```

在使用pipenv之前，应该忘记pip的存在。

新建一个pipenvtest目录。在这个目录下进行操作。

创建一个环境。

```
pipenv --python 2.7
```

安装一个包看看。

```
pipenv install requests
```

当前目录下就这些东西：

```
hlxiong@hlxiong-VirtualBox:~/work/test/pipenvtest$ tree
.
├── Pipfile
└── Pipfile.lock

0 directories, 2 files
```



```
hlxiong@hlxiong-VirtualBox:~/work/test/pipenvtest$ pipenv graph
requests==2.19.1
  - certifi [required: >=2017.4.17, installed: 2018.4.16]
  - chardet [required: >=3.0.2,<3.1.0, installed: 3.0.4]
  - idna [required: >=2.5,<2.8, installed: 2.7]
  - urllib3 [required: >=1.21.1,<1.24, installed: 1.23]
```

Pipfile内容：

```
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[dev-packages]

[packages]
requests = "*"

[requires]
python_version = "2.7"
```



# 参考资料

1、Python新利器之pipenv

https://www.jianshu.com/p/00af447f0005

2、TOML简介 (转) - 孤独信徒 - 博客园

https://www.cnblogs.com/unqiang/p/6399136.html