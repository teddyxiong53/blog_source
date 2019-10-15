---
title: python之setup
date: 2019-10-14 16:50:54
tags:
	- Python

---

1

有些模块没有办法通过pip install来安装，因为没有上传到pypi上去。

但是这些模块会提供一个setup.py文件来给我们安装用。

怎么使用呢？执行2个步骤就可以：

```
python setup.py build
python setup.py install
```

setup.py的本质是：把指定模块路径调节到PYTHONPATH环境变量里。

distutils和setuptools的区别：

distutils是python自带的，但是功能不够好。

setuptools是disutils的增强版本。



看看setup.py应该怎么写。

```
from setuptools import setup, find_packages

setup(
    name="test",
    version="1.0.0",
    keywords=("test", "xx"),
    description="test desc",
    long_description="test long desc",
    license="MIT License",
    url="http://xx.com",
    author="test",
    author_email="test@xx.com",

    packages=find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = [],
    scripts = [],
    entry_points = {
        'console_scripts': [
            'test = test.help:main'
        ]
    }
)
```



# setup.cfg

setup.cfg是给setup.py里的setup函数提供配置项的。

https://setuptools.readthedocs.io/en/latest/setuptools.html#configuring-setup-using-setup-cfg-files

这里是说明文档。



参考资料

1、python安装模块如何通过setup.py安装

https://blog.csdn.net/qq_34104395/article/details/80209574

2、python的构建工具setup.py

https://blog.csdn.net/whatday/article/details/90767387

3、

http://blog.konghy.cn/2018/04/29/setup-dot-py/