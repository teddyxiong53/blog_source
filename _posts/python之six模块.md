---
title: python之six模块
date: 2019-01-09 15:39:22
tags:		
	- python

---

1

常用内容：

```
get_unbound_function
get_method_function
get_method_self
get_function_closure
get_function_code
get_function_defaults
get_function_globals

advance_iterator
	获取迭代器的下一个，py2是it.next()，py3是next(it)
callable
	
```



six是6，6是2和3的最小公倍数。

six这个模块就是为了兼容python2和python3而存在的。

基于six写的代码，可以不需要修改就可以在python2和python3上跑。

具体是怎么做到的呢？

就另外弄了一套名字，在内部兼容2和3 。

在python2里。

```
In [102]: six.string_types
Out[102]: (basestring,)

In [103]: six.class_types
Out[103]: (type, classobj)


In [104]: six.integer_types
Out[104]: (int, long)

In [105]: six.text_type
Out[105]: unicode

In [106]: six.binary_type
Out[106]: str

In [107]: six.MAXSIZE
Out[107]: 9223372036854775807
```

在python3里。

```

In [5]: six.string_types                                                                                                                                                                     
Out[5]: (str,)

In [6]: six.class_types                                                                                                                                                                      
Out[6]: (type,)

In [7]: six.integer_types                                                                                                                                                                    
Out[7]: (int,)

In [8]: six.text_type                                                                                                                                                                        
Out[8]: str

In [9]: six.binary_type                                                                                                                                                                      
Out[9]: bytes

In [10]: six.MAXSIZE                                                                                                                                                                         
Out[10]: 9223372036854775807
```

可以看出python2和python3的不同。

six.py代码里是这么写的。

```
if PY3:
    string_types = str,
    integer_types = int,
    class_types = type,
    text_type = str
    binary_type = bytes

    MAXSIZE = sys.maxsize
else:
    string_types = basestring,
    integer_types = (int, long)
    class_types = (type, types.ClassType)
    text_type = unicode
    binary_type = str
```

这个文件只有800行。



# 对象模型兼容



# 语法兼容



class_types的不同，在于python2里有2种类，type对应新式类，types.ClassType对应经典类。

python2和python3为什么在整数长度上有差异？



```
get_unbound_function
	这个的作用是什么？
	这个是因为py2和py3的对象模型不同导致的，在py3里面，不存在unbound function。而在py2里是存在的。
	所谓unbound函数，技术ClassName.member_function这种方式访问的普通成员函数。
	这个特性有什么意义吗？
```

```
get_member_function
	
```



参考资料

1、Six: Python 2 and 3 Compatibility Library

https://pythonhosted.org/six/

2、官网文档

https://six.readthedocs.io/

3、python之six用法

https://blog.csdn.net/xc_zhou/article/details/80921509

