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

上面这些都是简单的用法，而看flask 的代码里，用得比较复杂，分析一下。

看看make  test做了什么。

```
test: clean-pyc install-dev
	pytest
```

```
pip install -q -e .[dev]
```

这句该怎么理解？

我随便建立一个空的目录，执行这句。

```
pip install -q -e .[dev]
Directory '.' is not installable. File 'setup.py' not found.
```

可见是依赖了setup.py文件。





flask的源代码里，就已经给测试做了打桩的。

在Flask类里，有一个test_client函数。

还有一个专门的testing.py文件。

#HelloWorld

```
import pytest

def func(x):
    return x+1
def test_answer():
    assert func(3)==5
```

执行：py.test test.py

就可以完成测试。

# 写一个测试类

```
class TestClass:
    def test_one(self):
        x = "this"
        assert 'h' in x
    def test_two(self):
        x = "hello"
        assert hasattr(x, 'check')
```

# pytest常用命令选项

```
-x 
	遇到错误马上停止。
--maxfail=num
	当错误数达到num时，停止测试。
-s
	打印用例的信息。
-q
	只显示结果，不显示过程。
```

```
pytest dir/
pytest xx.py
pytest -k "MyClass and not method" #匹配某种规则
pytest -m slow
	这个表示测试mark了slow的测试用例。
	@pytest.mark.slow
	def test_xx():
		assert 1==1
	
```

# 在pycharm里运行pytest

# setup和teardown

setup和teardown是在测试之前和测试之后执行的，每个用例都会执行一次。

在pytest里，有4个运行级别：

```
1、模块级。
	setup_module
	teardown_module
2、函数级。
	setup_function
	teardown_function
3、类级。
	setup_class
	teardown_class
4、方法级。
	setup_method
	teardown_method
5、类里面的。运行在调用方法的前后。
	setup
	teardown
这里setup_method和teardown_method的功能和setup/teardown功能是一样的，一般二者用其中一个即可	
```

例子

```
def setup_function():
    print("setup_function:每个方法执行前都会执行")
def teardown_function():
    print("teardown_function:每个方法执行后都会执行")

def test_one():
    print("执行test_one")
    x =  'this'
    assert 'h' in x

def test_two():
    print("执行test_two")
    x = 'hello'
    assert hasattr(x, 'check')
```

```
class TestClass:
    def setup(self):
        print("setup：每个用例开始前执行")

    def teardown(self):
        print("teardown：每个用例结束后执行")

    def setup_class(self):
        print("setup_class：所有用例执行之前")
    def teardown_class(self):
        print("teardown_class：所有用例执行之后")

    def setup_method(self):
        print("setup_method：每个用例开始前执行")

    def teardown_method(self):
        print("teardown_method：每个用例结束后执行")

    def test_one(self):
        print("执行test_one")
        x = 'this'
        assert  'h' in x

    def test_two(self):
        print("执行test_two")
        x = 'hello'
        assert hasattr(x, 'check')
```



输出：

```
test_1.py setup_class：所有用例执行之前        
setup_method：每个用例开始前执行                
setup：每个用例开始前执行                       
执行test_one                            
.teardown：每个用例结束后执行                   
teardown_method：每个用例结束后执行             
setup_method：每个用例开始前执行                
setup：每个用例开始前执行                       
执行test_two                            
Fteardown：每个用例结束后执行                   
teardown_method：每个用例结束后执行             
teardown_class：所有用例执行之后               
```



# fixture

前面讲的setup和teardown是全局生效的。

但是有时候有这种测试场景：

用例1需要先登陆。

用例2不需要登陆。

用例3又需要登陆。

这种场景就不能全局来做。

所以就需要引入fixture。fixture的字面含义是固定设施。

在这里表示预置条件。



fixture相当于setup和teardown，有这些优势：

```
1、命名方式灵活，不像setup必须要包含setup在名字里。
2、conftest.py配置里，可以实现数据共享。不需要import，就可以自动找到一些配置。
3、scope="module"，可以实现多个py跨文件共享前置条件。每个py文件调用一次。
4、scope="session"，实现多个py文件使用一个session来完成多个用例。
```



fixture有5个参数：

```
scope
	默认值是function。可以取的值有：function、class、module、session。
params：
	可选参数列表。
autouse：
	bool类型。默认为False。
ids：
name：
```



参考资料

1、python单元测试框架pytest简介

https://blog.csdn.net/liuchunming033/article/details/46501653

2、pytest文档5-fixture之conftest.py

https://www.cnblogs.com/yoyoketang/p/9390073.html

3、pytest框架之fixture详细使用

https://www.cnblogs.com/huizaia/p/10331469.html

4、pytest文档1-环境准备与入门

这个系列文章有28篇，很不错。

https://www.cnblogs.com/yoyoketang/p/9356693.html