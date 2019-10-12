---
title: python之update_wrapper用途
date: 2019-10-10 11:17:22
tags:		
	- python

---

1

update_wrapper，主要是用来修改被修饰函数的某些属性的。如果不用，则这些属性不对。

```
from functools import update_wrapper
def wrapper(f):
    def wrapper_function(*args, **kwargs):
        '''
        这个是修饰函数
        :param args:
        :param kwargs:
        :return:
        '''
        return f(*args, **kwargs)
    update_wrapper(wrapper_function, f)
    return wrapper_function

@wrapper
def wrapped():
    '''
    这个是被修饰函数。
    :return:
    '''
    pass

print(wrapped.__doc__)
print(wrapped.__name__)
```

wraps的作用是类似的。

```
from functools import wraps

def wrapper(f):
    @wraps(f) # 注释掉这一行，则最后得到的打印信息不同。
    def wrapper_function(*args, **kwargs):
        '''
        这个是修饰函数
        :param args:
        :param kwargs:
        :return:
        '''
        return f(*args, **kwargs)
    return wrapper_function

@wrapper
def wrapped():
    '''
    这个是被修饰函数。
    :return:
    '''
    pass

print(wrapped.__doc__)
print(wrapped.__name__)
```



参考资料

1、装饰器partial、update_wrapper、wraps作用以及如何使用

https://blog.csdn.net/qq_21178933/article/details/78539470