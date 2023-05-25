---
title: Python之魔法方法
date: 2017-09-29 20:43:46
tags:
	- Python

---

--

# 有多少个魔法方法

在Python中，魔法方法的数量是不固定的，因为它们的数量会随着Python版本的更新和扩展库的引入而变化。但是，对于较新的Python版本（如Python 3.9），大约有80多个魔法方法可用。

请注意，这个数字是近似的，并且可能会因为Python版本和库的变化而有所不同。此外，并非所有的魔法方法都需要在每个类中实现，而是根据需要选择性地实现。

# 1. 什么是魔法方法

魔法方法就是可用给你的类增加魔力的特殊方法，注意是针对类的。名字上的特点是前后都有两个下划线。如`__init__`这种。

```
构造相关
	__init__
	__new__
	__del__
操作相关
	比较操作符
        __cmp__
            实现这个就够了。
            类似的还有：__le__/__ge__/...
    数值操作符
    	一元操作符：就是只有一个参数的。
    		__pos__：取正。
    		__neg__：取负。
    		__abs__
    		__invert__
    		__round__
    		__floor__
    		__ceil__
    		__trunc__
    	常见算术操作符：
    		__add__(self, other)
    			这个是为实现a+b，相当于重载+运算符。
    		__sub__
    		__mul__
    		__floordiv__
    		__div__
    		__mod__
    		__divmod__
    		__pow__
    		__rshift__
    	反射算术运算符：在上面的基础上加上一个r前缀。
    		__radd__(self, other)
    			r表示右边的意思。
    		...
    	增强赋值运算符：就是+=的实现。
    		__iadd__
    		__isub__
    		...
    	类型转换操作符
    		__int__(self)
    		__float__(self)
    		__bool__()
    			这个是为了实现bool(x)这种操作。
    		...
类的表示
	就是用字符串来打印类。
	__str__
	__repr__
	__unicode__
	__format__
	__hash__
	__nonzero__
	__dir__
		对应dir(XX)的行为。
访问控制
	很多人抱怨python无法实现真正意义的封装，就是定义私有变量，然后用setter、getter进行访问。
	魔法方法其实可以做到。
	__getattr__
	__setattr__
	__delattr__
	__getattribute__
		这个跟前面的不同，这个只能用于新式类。
		尽量别用这个。
自定义序列
	__len__
	__getitem__ ：这个是通过[]来访问的。
	__setitem__
	__iter__
	__reversed__
	__contains__
	__missing__
反射
	__instancecheck__
	__subclasscheck__
可调用对象
	__call__
	
上下文管理
	__enter__
	__exit__
描述符对象
	 __get__
	 __set__
	 __delete__
拷贝
	__copy__
	__deepcopy__
pickle
	__getinitargs__
	__getnewargs__
	__getstate__
	__setstate__
	__reduce__
	__reduce_ex__
	
```



什么时候使用呢？

自己定义继承了dict、list等基础类的工具类的时候，需要自己实现一些魔法方法。



# 2. 创建相关的

有3个：

`__init__, __new__, __del__`。



`__new__`的特点：

1、是一个对象实例化时调用的第一个方法。

2、`__new__`决定是是否要调用`__init__`方法。

3、主要用途是用来继承一个不可变的类型，比如tuple、string。

4、返回的是一个构建的实例。

举例，用`__new__`来实现一个单例模式。**注意new的的第一个参数是cls，而不是self。**

```
class Person(object):
	def __init__(self, name, age):
		self.name = name
		self.age = age
		
	def __new__(cls, *args, **kwargs):
		if not hasattr(cls, 'instance'):
			cls.instance = super(Person, cls).__new__(cls)
		return cls.instance
		
p1 = Person(20, 'a')
p2 = Person(21, 'b')
print p1 == p2

```

可以看到结果的True。

`__del__`在对象被销毁时调用。被垃圾回收器调用。

del xx的时候，不是调用`__del__`。

# 3. 成员相关的

也有3个。`__call__, __getitem__, __setitem__`。

`__call__`允许一个类的实例像函数一样被调用。看下面的例子。

```
class Person(object):
	def __init__(self, name, age):
		self.name = name
		self.age = age
		self.instance = add
		
	def __call__(self, *args):
		return self.instance(*args)
		
def add(args):
	return args[0] + args[1]
	
p = Person(20, 'a')
print p([1,2])

```

`__getitem__`定义获取容器中指定元素的行为。相当于self[key]。

```
class Person(object):
	def __init__(self, name, age):
		self.name = name
		self.age = age
		self._resgitry = {
			'name': name,
			'age': age
		}
		
	def __call__(self, *args):
		return self.instance(*args)
		
	def __getitem__(self, key):
		if key not in self._resgitry.keys():
			raise Exception('please register key :%s ' % (key, ))	
		return self._resgitry[key]
	
p = Person('a', 20)
print p.age

```



# 4. 属性相关的

`__getattr__, __setattr__, __delattr__, __get__, __set__ , __delete__, __getattribute__`。





我自己新建一个类，空的。看看有哪些属性。

```
>>> class MyClass():
...     pass
... 
>>> dir(MyClass)
['__doc__', '__module__']
>>> print MyClass.__doc__
None
>>> print MyClass.__module__
__main__
>>> help(MyClass)
Help on class MyClass in module __main__:

class MyClass
```

新建一个继承了object的class。

```
>>> class MyClass2(object):
...     pass
... 
>>> dir(MyClass2)
['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__']
>>> help(MyClass2)
Help on class MyClass2 in module __main__:

class MyClass2(__builtin__.object)
 |  Data descriptors defined here:
 |  
 |  __dict__
 |      dictionary for instance variables (if defined)
 |  
 |  __weakref__
 |      list of weak references to the object (if defined)
```

# 重新整理

主要参考这个

https://www.cnblogs.com/nmb-musen/p/10861536.html

照着这个实现一个测试例子。

```
class Test:
  def __new__(cls, *args, **kwargs):
    print('call __new__')
    if not hasattr(cls, 'instacne'):
      cls.instance = super(Test, cls).__new__(cls)
    return cls.instance
  def __init__(self, v):
    print('call __init__')
    self.v = v
  def __del__(self):
    print('call __del__')
  def __call__(self, *args, **kwargs):
    print('call __call__', *args, **kwargs)
  def __len__(self):
    print('call __len__')
    return 0 # 必须返回数字，不然有error
  def __repr__(self):
    print('call __repr__')
    return f'Test {self.v}'
  def __str__(self):
    print('call __str__')
    return f'str Test {self.v}'
  def __bytes__(self):
    print('call __bytes__')
    return bytes('Test'.encode('utf-8'))
  def __hash__(self):
    print('call __hash__')
    return 1
  def __bool__(self):
    print('call __bool__')
    return self.v >= 0
  def __format__(self, format_spec):
    print('call __format__')
    return 'format 123'
  def __getattr__(self, key): # 这个是专门给访问不存在的属性时使用的
    print('call __getattr__')
    print(key)
    return 'has no such a attr'
  '''
  # 下面这个加上后，会导致其他的方法出错。
  def __getattribute__(self, name):
    # print('call __getattribute__')
    # 默认是返回getattr(self, name)
    # return getattr(self, name)
    # return self.name
    pass
  '''
  def __lt__(self, other):
    return self.v < other.v
  def __add__(self, other):
    return self.v + other.v
t1 = Test(1.0)# 这个都会依次调用__new__ __init__ __del__
t2 = Test(2.0)
t1(1) # 这个会调用__call__
len(t1)
print(repr(t1))
print(str(t1))
print(bytes(t1))
print(hash(t1))
print(bool(t1))
print('test format {}'.format(t1))
print(f'use f to format :{t1}')
# print('use % to format %s' % t1) # 这个不行的
print(t1.abc)
print(t1.v)
print('t1 < t2 :{}'.format(t1<t2))
print('t1+t2 {}'.format(t1+t2))
```



# 一些疑问

## `__getattr__` 和 `__getattribute__`的区别以及为什么要这么设计

`__getattr__` 和 `__getattribute__` 都是用于处理属性访问的特殊方法，但它们之间有几个重要的区别：

1. 触发时机：
   - `__getattr__`：在访问不存在的属性时触发。
   - `__getattribute__`：在访问任何属性时都会触发，包括已存在的属性。
2. 默认行为：
   - `__getattr__`：如果属性不存在，`__getattr__` 方法会被调用，可以返回一个默认值或引发 `AttributeError` 异常。
   - `__getattribute__`：无论属性是否存在，`__getattribute__` 方法都会被调用，它是属性访问的第一站。
3. 安全性和递归：
   - `__getattr__`：由于在属性不存在时才触发，因此可以用于提供默认值或处理动态属性，但可能导致递归调用。
   - `__getattribute__`：在每次属性访问时都会触发，需要小心处理，以避免无限递归调用。

看示例代码：

```
class MyClass:
    def __init__(self):
        self.x = 10
    def __getattr__(self, name):
        print(f"__getattr__ called for attribute: {name}")
        return 42

    def __getattribute__(self, name):
        print(f"__getattribute__ called for attribute: {name}")
        return object.__getattribute__(self, name)

obj = MyClass()

print(obj.x)  # 访问不存在的属性
print(obj.y)  # 访问存在的属性


```

打印：

```
__getattribute__ called for attribute: x
10
__getattribute__ called for attribute: y
__getattr__ called for attribute: y
42
```



设计 `__getattr__` 和 `__getattribute__` 这样的特殊方法是为了提供对属性访问的**灵活性和自定义能力**。

它们允许开发者在属性访问过程中插入自定义逻辑，从而实现更高级的属性访问行为。

下面是一些原因解释为什么要这样设计：

1. 动态属性和默认值：通过 `__getattr__` 方法，可以在访问不存在的属性时动态地提供默认值，而不是引发 `AttributeError` 异常。这对于动态地计算属性值或提供默认设置非常有用。
2. 惰性计算和资源延迟加载：**通过 `__getattr__` 方法，可以在属性被访问时才进行计算或加载资源**，而不是在对象初始化阶段就提前执行。这可以提高性能和节省资源，尤其对于大型对象或资源密集型应用程序而言。
3. 属性访问的拦截和控制：`__getattribute__` 方法在每次属性访问时都会被调用，它允许开发者完全控制属性的访问行为。这样可以实现各种拦截、验证、日志记录、安全性检查等操作，以实现更细粒度的属性访问控制。
4. 动态类和属性代理：使用 `__getattribute__` 和 `__getattr__` 方法，可以在类级别上实现动态生成属性或属性代理的功能。这对于元编程、动态类构建和属性委派等场景非常有用。

## `__setattr__` 和 `__setitem__`区别

简单说，setattr是点号的方式。setitem是索引的方式（也就是中括号的方式）。

总结：

- `__setattr__` 方法用于设置对象的属性值，在赋值操作中调用，适用于普通对象的属性赋值。
- `__setitem__` 方法用于设置对象的元素值，在索引赋值操作中调用，适用于可索引对象的元素赋值。



需要注意的是，在实现这两个方法时，如果直接使用 `self.name = value` 或 `self[key] = value` 的形式进行赋值，会导致递归调用自身，从而引发无限循环。为了避免这种情况，通常需要使用 `super()` 来调用基类的相应方法来完成实际的赋值操作。

```
class MyClass:
    def __setattr__(self, name, value):
        print("Setting attribute:", name)
        # 执行实际的属性赋值操作
        super().__setattr__(name, value) #这句是为了避免递归。

obj = MyClass()
obj.foo = 42  # 调用 __setattr__ 方法

```








## `__call__ `方法用途

`__call__` 方法是 Python 类中的特殊方法之一，用于使对象可调用。当使用函数调用运算符 `()` 调用一个对象时，Python 会检查该对象是否实现了 `__call__` 方法，如果实现了，则会调用该方法。

`__call__` 方法的主要作用是让对象具备像函数一样的行为，可以像调用函数一样使用该对象。通过实现 `__call__` 方法，我们可以将一个类实例化的对象变得可调用，就像调用函数一样。

下面是一个简单的示例，演示了 `__call__` 方法的用法：

```python
class CallableClass:
    def __init__(self, name):
        self.name = name

    def __call__(self, *args, **kwargs):
        print(f"Hello, {self.name}!")
        print("Arguments:", args)
        print("Keyword arguments:", kwargs)

# 实例化一个对象
obj = CallableClass("Alice")

# 调用对象，就像调用函数一样
obj(1, 2, 3, foo="bar")
```

运行上述代码，会输出以下结果：

```
Hello, Alice!
Arguments: (1, 2, 3)
Keyword arguments: {'foo': 'bar'}
```

在上述示例中，我们定义了一个 `CallableClass` 类，该类实现了 `__call__` 方法。当我们实例化 `CallableClass` 类的对象 `obj` 后，我们可以像调用函数一样使用 `obj`，并且会调用 `__call__` 方法。在 `__call__` 方法中，我们可以执行一些操作，处理传入的参数，并进行相应的逻辑。

总而言之，通过实现 `__call__` 方法，我们可以让一个类的实例对象具备函数的行为，可以直接调用对象并执行相应的逻辑。这种方式可以使代码更具灵活性和可读性，使对象更像一个可调用的函数。



## int、str等内置函数也是通过`__call__`实现的吗

不完全正确。内置函数（如 `int`、`str` 等）不是通过 `__call__` 方法实现的，而是通过特殊的 C 代码实现的。这些内置函数在 Python 解释器的内部是以 C 语言实现的，而不是通过 Python 代码。

Python 中的内置函数是直接提供给开发者使用的一些常用函数，它们在语言层面上具有特殊的功能和行为，如类型转换、字符串处理、数学计算等。这些内置函数在解释器启动时就已经加载进来，可以直接使用，无需定义类或实例化对象。

虽然内置函数不是通过 `__call__` 方法实现的，但是它们仍然可以像函数一样被调用。这是因为内置函数对象在内部实现了 `__call__` 方法，使其具备可调用的行为。这种实现方式是由解释器内部处理的，对于开发者来说，可以将内置函数看作普通的函数一样使用。

例如，我们可以直接调用 `int` 函数将一个字符串转换为整数：

```python
num = int("10")
print(num)  # 输出：10
```

在上述示例中，我们直接调用了 `int` 函数，将字符串 `"10"` 转换为整数。尽管我们没有使用 `()` 运算符显式调用 `__call__` 方法，但是解释器内部会自动调用该方法来执行相应的逻辑。

因此，虽然内置函数的实现方式与普通类中的 `__call__` 方法不同，但它们都具备可调用的行为，可以通过直接调用函数名的方式使用。

# 参考资料

1、

https://pyzh.readthedocs.io/en/latest/python-magic-methods-guide.html

2、Python 魔术方法指南

https://pycoders-weekly-chinese.readthedocs.io/en/latest/issue6/a-guide-to-pythons-magic-methods.html

3、`python __add__和__radd`__

https://blog.csdn.net/u011019726/article/details/77834602

