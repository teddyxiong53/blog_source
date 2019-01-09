---
title: python之six模块
date: 2019-01-09 15:39:22
tags:		
	- python

---



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



参考资料

1、Six: Python 2 and 3 Compatibility Library

https://pythonhosted.org/six/