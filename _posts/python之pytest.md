---
title: python之pytest
date: 2019-09-03 17:03:03
tags:
	- python
---

1

pytest是python里的单元测试框架。

python官方有自带一个unittest。

pytest更加好用一些。

安装：

```
sudo pip install pytest
```

查看版本。

```
py.test --version
```

py.test可以带参数，参数是需要被测试的目录或者文件名。

不带参数的话，它会自动查找当前目录下的test_xx.py这种格式的文件进行测试。



基本规则：

```
1、测试文件test_开头。（以_test结尾其实也可以）
2、测试类，以Test开头。而且不能有__init__函数。
3、测试函数以test_开头。
4、断言就用基本的asset。
```



生成测试报告：

需要先安装一个模块：

```
sudo pip install pytest-html
```

然后执行这个，就可以生成报告。格式挺好的。

```
py.test test_func.py --html=report.html
```



测试指定函数，用2个冒号来连接。

```
py.test test_file1::test_func1
```



参考资料

1、python单元测试框架pytest简介

https://blog.csdn.net/liuchunming033/article/details/46501653