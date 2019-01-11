---
title: Python之pypi
date: 2018-06-17 14:54:59
tags:
	- Python

---



pypi是PYthon Package Index的缩写。

就是Python官方的第三方库的仓库。

所有人都可以从这里下载需要的库，也可以上传自己的库。

pypi推荐使用pip工具来进行管理。

网站在这里：https://pypi.org/

上面显示目前有14万个项目。大概100万个release。

130万个文件，28万用户。

怎么上传自己的包到pypi上？是否需要审核？

先要注册账号。我之前已经注册过了。

官方提供了一个打包的教程。

https://packaging.python.org/



新建目录结构如下：

```
hlxiong@hlxiong-VirtualBox:~/work/test/pypi/xhl_example_pkg$ tree
.
├── LICENSE
├── README.md
├── setup.py
└── xhl_example_pkg
    └── __init__.py
```

license就就拷贝Apache的。

setup.py是setuptools需要的脚本。

告诉setuptools这些信息：

1、名字。

2、版本。

3、需要包含的文件。

setup.py我们这样写。

```

```

执行命令：

```
python setup.py sdist bdist_wheel
```

```
hlxiong@hlxiong-VirtualBox:~/work/test/pypi/xhl_example_pkg$ python setup.py sdist bdist_wheel
running sdist
running egg_info
creating xhl_example_pkg.egg-info
writing xhl_example_pkg.egg-info/PKG-INFO
writing top-level names to xhl_example_pkg.egg-info/top_level.txt
writing dependency_links to xhl_example_pkg.egg-info/dependency_links.txt
writing manifest file 'xhl_example_pkg.egg-info/SOURCES.txt'
reading manifest file 'xhl_example_pkg.egg-info/SOURCES.txt'
writing manifest file 'xhl_example_pkg.egg-info/SOURCES.txt'
running check
creating xhl_example_pkg-0.0.1
creating xhl_example_pkg-0.0.1/xhl_example_pkg
creating xhl_example_pkg-0.0.1/xhl_example_pkg.egg-info
copying files to xhl_example_pkg-0.0.1...
copying README.md -> xhl_example_pkg-0.0.1
copying setup.py -> xhl_example_pkg-0.0.1
copying xhl_example_pkg/__init__.py -> xhl_example_pkg-0.0.1/xhl_example_pkg
copying xhl_example_pkg.egg-info/PKG-INFO -> xhl_example_pkg-0.0.1/xhl_example_pkg.egg-info
copying xhl_example_pkg.egg-info/SOURCES.txt -> xhl_example_pkg-0.0.1/xhl_example_pkg.egg-info
copying xhl_example_pkg.egg-info/dependency_links.txt -> xhl_example_pkg-0.0.1/xhl_example_pkg.egg-info
copying xhl_example_pkg.egg-info/top_level.txt -> xhl_example_pkg-0.0.1/xhl_example_pkg.egg-info
Writing xhl_example_pkg-0.0.1/setup.cfg
creating dist
Creating tar archive
removing 'xhl_example_pkg-0.0.1' (and everything under it)
running bdist_wheel
running build
running build_py
creating build
creating build/lib.linux-x86_64-2.7
creating build/lib.linux-x86_64-2.7/xhl_example_pkg
copying xhl_example_pkg/__init__.py -> build/lib.linux-x86_64-2.7/xhl_example_pkg
installing to build/bdist.linux-x86_64/wheel
running install
running install_lib
creating build/bdist.linux-x86_64
creating build/bdist.linux-x86_64/wheel
creating build/bdist.linux-x86_64/wheel/xhl_example_pkg
copying build/lib.linux-x86_64-2.7/xhl_example_pkg/__init__.py -> build/bdist.linux-x86_64/wheel/xhl_example_pkg
running install_egg_info
Copying xhl_example_pkg.egg-info to build/bdist.linux-x86_64/wheel/xhl_example_pkg-0.0.1-py2.7.egg-info
running install_scripts
creating build/bdist.linux-x86_64/wheel/xhl_example_pkg-0.0.1.dist-info/WHEEL
```

现在目录情况：

```
hlxiong@hlxiong-VirtualBox:~/work/test/pypi/xhl_example_pkg$ tree
.
├── build
│   ├── bdist.linux-x86_64
│   └── lib.linux-x86_64-2.7
│       └── xhl_example_pkg
│           └── __init__.py
├── dist
│   ├── xhl_example_pkg-0.0.1-py2-none-any.whl
│   └── xhl_example_pkg-0.0.1.tar.gz
├── LICENSE
├── README.md
├── setup.py
├── xhl_example_pkg
│   └── __init__.py
└── xhl_example_pkg.egg-info
    ├── dependency_links.txt
    ├── PKG-INFO
    ├── SOURCES.txt
    └── top_level.txt
```



接下来是需要上传。

先安装twine。

```
sudo   pip install --user --upgrade twine
```

然后使用twine进行上传。

```
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

我这个上传出错了。

```
hlxiong@hlxiong-VirtualBox:~/work/test/pypi/xhl_example_pkg$ twine upload --repository-url https://test.pypi.org/legacy/ dist/*
Enter your username: teddyxiong53
Enter your password: 
Uploading distributions to https://test.pypi.org/legacy/
Uploading xhl_example_pkg-0.0.1-py2-none-any.whl
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 5.45k/5.45k [00:01<00:00, 5.20kB/s]
NOTE: Try --verbose to see response content.
HTTPError: 403 Client Error: Invalid or non-existent authentication information. for url: https://test.pypi.org/legacy/
```

网上搜索了一下，说是需要定义一个.pypirc文件。

```
[distutils]
index-servers =
  pypi
  test

[pypi]
username:username
password:som3passw0rd

[test]
repository:https://test.pypi.org/legacy/
username:username
password:som3passw0rd
```

名字和密码改一下。

需要在https://test.pypi.org这个网站也注册一个账号，我跟pypi上的名字保持一致。

再用twine上传一次就成功了。



下载安装。

```
sudo pip install --index-url https://test.pypi.org/simple/ xhl_example_pkg
```



```
hlxiong@hlxiong-VirtualBox:~/work/test$ sudo pip install --index-url https://test.pypi.org/simple/ xhl_example_pkg
The directory '/home/hlxiong/.cache/pip/http' or its parent directory is not owned by the current user and the cache has been disabled. Please check the permissions and owner of that directory. If executing pip with sudo, you may want sudo's -H flag.
The directory '/home/hlxiong/.cache/pip' or its parent directory is not owned by the current user and caching wheels has been disabled. check the permissions and owner of that directory. If executing pip with sudo, you may want sudo's -H flag.
Looking in indexes: https://test.pypi.org/simple/
Collecting xhl_example_pkg
  Downloading https://test-files.pythonhosted.org/packages/f8/6c/c7bd40feed904adf45e68795cb47b3c2ef04d212df4b6baaf620f2577fb8/xhl_example_pkg-0.0.1-py2-none-any.whl
Installing collected packages: xhl-example-pkg
Successfully installed xhl-example-pkg-0.0.1
You are using pip version 10.0.1, however version 18.1 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.
```



使用：

```

In [66]: import xhl_example_pkg

In [67]: help(xhl_example_pkg)
Help on package xhl_example_pkg:

NAME
    xhl_example_pkg

FILE
    /usr/local/lib/python2.7/dist-packages/xhl_example_pkg/__init__.py

PACKAGE CONTENTS
```



# 升级和加入系统脚本

我看ssr的，会生成sslocal脚本在usr/bin目录下。

是在setup.py里加上这个做到的。我也试一下。然后上传顺便看看怎样升级自己的软件包。

```
entry_points="""
    [console_scripts]
    sslocal = shadowsocks.local:main
    ssserver = shadowsocks.server:main
    """,
```

我这样写

```

```

生成，然后上传

报错了。

```
HTTPError: 400 Client Error: File already exists. See https://test.pypi.org/help/#file-name-reuse for url: https://test.pypi.org/legacy/
hlxiong@hlxiong-VirtualBox:~/work/test/pypi/xhl_example_pkg$ 
```



网上找了一下，

```
python setup.py sdist upload
```

试一下这个。不行。

加上选项。可以了。

```
twine upload --repository-url https://test.pypi.org/legacy/ dist/* --skip-existing
```

```
sudo pip install --index-url https://test.pypi.org/simple/ xhl_example_pkg
```

可以在这里看到我的包的情况。

https://test.pypi.org/manage/project/xhl-example-pkg/release/0.0.2/

我选择先卸载，再安装的方式，可以安装到0.0.2版本的。

执行我的脚本。

```
hlxiong@hlxiong-VirtualBox:~/work/test/pypi/xhl_example_pkg$ xhl_example_pkg_main 
Traceback (most recent call last):
  File "/usr/local/bin/xhl_example_pkg_main", line 7, in <module>
    from shadowsocks.main import main
ImportError: No module named main
```

虽然出错了。但是安装到系统目录下了。

```
hlxiong@hlxiong-VirtualBox:~/work/test/pypi/xhl_example_pkg$ which xhl_example_pkg_main 
/usr/local/bin/xhl_example_pkg_main
```

是我写错了，报名里写了shadowsocks。

改一下。

```

```



总结一下步骤：

```
修改代码，修改版本号。

#生成dist文件。
python setup.py sdist bdist_wheel
#上传，覆盖。
twine upload --repository-url https://test.pypi.org/legacy/ dist/* --skip-existing
#卸载本地
sudo pip uninstall xhl_example_pkg 
#安装
sudo pip install --index-url https://test.pypi.org/simple/ xhl_example_pkg
```

现在可以了。

```
hlxiong@hlxiong-VirtualBox:~/work/test$ xhl_example_pkg_main 
xhl example pkg main.py execute
```



# 参考资料

1、Packaging Python Projects

https://packaging.python.org/tutorials/packaging-projects/

2、

https://github.com/pypiserver/pypiserver/issues/212