---
title: Python之egg
date: 2018-06-17 14:53:31
tags:
	- Python

---



#编写代码 

新建一个xhl-egg的目录。结构如下：

```
teddy@teddy-ubuntu:~/work/test/python/xhl-egg$ tree
.
├── bee
│   └── __init__.py
└── setup.py
```

`__init__.py`内容：

```
def hello():
	return 'hello xhl-bee'
	
def add(x, y):
	return x+y
```

setup.py内容：

```
#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
		name='bee',
		version='0.0.1',
		keywords = ('xhl', 'egg'),
		description = 'a simple egg',
		license = 'MIT License',
		url = 'http://teddyxiong53.github.com',
		author = 'teddyxiong53',
		author_email = '1073167306@qq.com',
		packages = find_packages(),
		include_package_data = True,
		platforms = 'any',
		install_requires = [],
)
```

# 打包

比较流行的打包方式有两种：

```
python setup.py bdist_egg #这种是用easy_install来安装的。
python setup.py sdist  #这种是用pip来安装的。
```

我们就选择sdist这一种吧。

```
teddy@teddy-ubuntu:~/work/test/python/xhl-egg$ python setup.py sdist
running sdist
running egg_info
creating bee.egg-info
writing bee.egg-info/PKG-INFO
writing top-level names to bee.egg-info/top_level.txt
writing dependency_links to bee.egg-info/dependency_links.txt
writing manifest file 'bee.egg-info/SOURCES.txt'
reading manifest file 'bee.egg-info/SOURCES.txt'
writing manifest file 'bee.egg-info/SOURCES.txt'
warning: sdist: standard file not found: should have one of README, README.rst, README.txt, README.md

running check
creating bee-0.0.1
creating bee-0.0.1/bee
creating bee-0.0.1/bee.egg-info
copying files to bee-0.0.1...
copying setup.py -> bee-0.0.1
copying bee/__init__.py -> bee-0.0.1/bee
copying bee.egg-info/PKG-INFO -> bee-0.0.1/bee.egg-info
copying bee.egg-info/SOURCES.txt -> bee-0.0.1/bee.egg-info
copying bee.egg-info/dependency_links.txt -> bee-0.0.1/bee.egg-info
copying bee.egg-info/top_level.txt -> bee-0.0.1/bee.egg-info
Writing bee-0.0.1/setup.cfg
creating dist
Creating tar archive
removing 'bee-0.0.1' (and everything under it)
```

现在目录结构是这样：

```
teddy@teddy-ubuntu:~/work/test/python/xhl-egg$ tree
.
├── bee
│   └── __init__.py
├── bee.egg-info
│   ├── dependency_links.txt
│   ├── PKG-INFO
│   ├── SOURCES.txt
│   └── top_level.txt
├── dist
│   └── bee-0.0.1.tar.gz
└── setup.py

3 directories, 7 files
```

多了bee.egg-info和dist这2个目录。

```
teddy@teddy-ubuntu:~/work/test/python/xhl-egg/bee.egg-info$ cat PKG-INFO 
Metadata-Version: 1.0
Name: bee
Version: 0.0.1
Summary: a simple egg
Home-page: http://teddyxiong53.github.com
Author: teddyxiong53
Author-email: 1073167306@qq.com
License: MIT License
Description-Content-Type: UNKNOWN
Description: UNKNOWN
Keywords: xhl,egg
Platform: any
```

```
teddy@teddy-ubuntu:~/work/test/python/xhl-egg/bee.egg-info$ cat SOURCES.txt 
setup.py
bee/__init__.py
bee.egg-info/PKG-INFO
bee.egg-info/SOURCES.txt
bee.egg-info/dependency_links.txt
bee.egg-info/top_level.txt
```

```
teddy@teddy-ubuntu:~/work/test/python/xhl-egg/bee.egg-info$ cat top_level.txt 
bee
```



然后是注册egg。

```
teddy@teddy-ubuntu:~/work/test/python/xhl-egg$ python setup.py register
running register
running egg_info
writing bee.egg-info/PKG-INFO
writing top-level names to bee.egg-info/top_level.txt
writing dependency_links to bee.egg-info/dependency_links.txt
reading manifest file 'bee.egg-info/SOURCES.txt'
writing manifest file 'bee.egg-info/SOURCES.txt'
running check
We need to know who you are, so please choose either:
 1. use your existing login,
 2. register as a new user,
 3. have the server generate a new password for you (and email it to you), or
 4. quit
Your selection [default 1]: 
```

我们选择2 

```
Your selection [default 1]: 
2
Username: teddyxiong53
Password: 
 Confirm: 
   EMail: 1073167306@qq.com
Registering teddyxiong53 to https://upload.pypi.org/legacy/
Server response (405): Method Not Allowed
```

不成功。我们还是到官网上通过网页的方式进行注册吧。

https://pypi.org/account/register/

然后是上传我们的包到pypi上。

还是失败。我们还是通过网页的方式进行上传吧。

```
teddy@teddy-ubuntu:~/work/test/python/xhl-egg$ python setup.py sdist bdist_egg upload
running sdist
running egg_info
writing bee.egg-info/PKG-INFO
writing top-level names to bee.egg-info/top_level.txt
writing dependency_links to bee.egg-info/dependency_links.txt
reading manifest file 'bee.egg-info/SOURCES.txt'
writing manifest file 'bee.egg-info/SOURCES.txt'
warning: sdist: standard file not found: should have one of README, README.rst, README.txt, README.md

running check
creating bee-0.0.1
creating bee-0.0.1/bee
creating bee-0.0.1/bee.egg-info
copying files to bee-0.0.1...
copying setup.py -> bee-0.0.1
copying bee/__init__.py -> bee-0.0.1/bee
copying bee.egg-info/PKG-INFO -> bee-0.0.1/bee.egg-info
copying bee.egg-info/SOURCES.txt -> bee-0.0.1/bee.egg-info
copying bee.egg-info/dependency_links.txt -> bee-0.0.1/bee.egg-info
copying bee.egg-info/top_level.txt -> bee-0.0.1/bee.egg-info
Writing bee-0.0.1/setup.cfg
Creating tar archive
removing 'bee-0.0.1' (and everything under it)
running bdist_egg
installing library code to build/bdist.linux-x86_64/egg
running install_lib
running build_py
creating build
creating build/lib.linux-x86_64-2.7
creating build/lib.linux-x86_64-2.7/bee
copying bee/__init__.py -> build/lib.linux-x86_64-2.7/bee
creating build/bdist.linux-x86_64
creating build/bdist.linux-x86_64/egg
creating build/bdist.linux-x86_64/egg/bee
copying build/lib.linux-x86_64-2.7/bee/__init__.py -> build/bdist.linux-x86_64/egg/bee
byte-compiling build/bdist.linux-x86_64/egg/bee/__init__.py to __init__.pyc
creating build/bdist.linux-x86_64/egg/EGG-INFO
copying bee.egg-info/PKG-INFO -> build/bdist.linux-x86_64/egg/EGG-INFO
copying bee.egg-info/SOURCES.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
copying bee.egg-info/dependency_links.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
copying bee.egg-info/top_level.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
zip_safe flag not set; analyzing archive contents...
creating 'dist/bee-0.0.1-py2.7.egg' and adding 'build/bdist.linux-x86_64/egg' to it
removing 'build/bdist.linux-x86_64/egg' (and everything under it)
running upload
Password: 
Submitting dist/bee-0.0.1.tar.gz to https://upload.pypi.org/legacy/
Upload failed (403): Invalid or non-existent authentication information.
error: Upload failed (403): Invalid or non-existent authentication information.
```

打开网站，发现提示说我的邮箱没有验证，点击重新发送邮件，验证通过。

我再用命令行的方式上传看看。还是失败。

看到官网教程里：https://packaging.python.org/tutorials/packaging-projects/

提到要用一个叫twine的工具来进行上传。我试一下。

```
sudo pip install --user --upgrade twine
```

再用twine进行上传。

```
teddy@teddy-ubuntu:~/work/test/python/xhl-egg$ twine upload --repository-url https://test.pypi.org/legacy/ dist/*
Uploading distributions to https://test.pypi.org/legacy/
Enter your username: teddyxiong53
Enter your password: 
Uploading bee-0.0.1-py2.7.egg
100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 3.98k/3.98k [00:03<00:00, 1.21kB/s]
HTTPError: 403 Client Error: Invalid or non-existent authentication information. for url: https://test.pypi.org/legacy/
teddy@teddy-ubuntu:~/work/test/python/xhl-egg$ 
```

成功了。

我们看看怎么用pip来下载安装这个库。

```
pip install --index-url https://test.pypi.org/simple/ xhl-egg
```

但是说找不到。

先不管了。



# 参考资料

1、怎样制作一个 Python Egg

http://liluo.org/blog/2012/08/how-to-create-python-egg/

将python包上传到PyPI

https://blog.csdn.net/libbyandhelen/article/details/78808959

制作 python 第三方包到 pypi,需要审核吗？

https://www.v2ex.com/t/188479