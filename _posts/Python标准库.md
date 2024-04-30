---
title: Python标准库
date: 2022-10-29 20:44:33
tags:
	- python

---

--

把python的常见api梳理一遍，便于记忆。

以3.11.0的为学习对象。

https://docs.python.org/zh-cn/3/library/functions.html

# 标准库的分类

Python标准库是Python编程语言的一部分，它提供了丰富的功能和工具，可以用于各种任务和应用程序开发。Python标准库按照功能和用途可以分为以下几个主要分类：

1. 常用数据类型和数据结构：
   - `collections`：提供了各种数据结构，如字典、列表、命名元组等。
   - `json`：用于处理JSON数据格式。
   - `pickle`：用于序列化和反序列化Python对象。

2. 文件和目录操作：
   - `os`：提供了与操作系统交互的功能，如文件和目录操作、进程管理等。
   - `io`：用于进行输入和输出操作，如文件读写、流操作等。
   - `pathlib`：提供了对文件和目录路径的面向对象的操作接口。

3. 网络和通信：
   - `socket`：用于网络编程，提供了套接字接口。
   - `http`：提供了HTTP协议相关的功能，如HTTP请求和响应处理。
   - `email`：用于处理电子邮件相关的功能，如发送和接收邮件。

4. 并发和异步编程：
   - `threading`：用于多线程编程。
   - `multiprocessing`：用于多进程编程。
   - `asyncio`：用于异步编程，提供了事件循环和协程等功能。

5. 数据库和持久化：
   - `sqlite3`：提供了对SQLite数据库的支持。
   - `pickle`：用于对象的序列化和反序列化。
   - `shelve`：提供了简单的对象持久化功能。

6. 测试和调试：
   - `unittest`：用于编写和运行单元测试。
   - `doctest`：用于编写和运行文档字符串中的测试。
   - `pdb`：用于调试Python程序。

除了上述分类之外，Python标准库还包含了许多其他功能模块，如日期和时间处理、数学计算、图形界面开发、加密和哈希算法等。每个模块都提供了详细的文档，可以在Python官方网站上查阅。通过利用Python标准库，开发人员可以更高效地编写Python程序，提高开发效率和质量。



```
内置函数
	既然内置了，那么必然是高频使用的方法。
	a：6个。abs、aiter、all、any、anext、ascii。
		all和any的判断。
		aiter和anext是async的。
		abs和ascii是基础函数。
	b：5个。
		bin：返回二进制字符串。
		bool：返回布尔值。
		breakpoint：断点，不用。
		bytearray：是一个class。
		bytes。
		主要是二进制和bool相关的。
	c：5个。
		c的主要语义包括：调用、字符、类、编译，复数。
		5个函数，就分属于上面5个语义。
		callable
		chr
		classmethod
		compile
		complex
	d：4个。
		d的主要语义是：删除、字典、目录、除。
		4个函数分属于这4个语义。
		delattr
		dict
		dir
		divmod
	e：3个。e的语义有：枚举，计算、执行。
		enumerate
		eval
		exec
	f：4个。f的语义有：过滤、浮点、格式化、冻结。
		filter
		float
		format
		frozenset
	g：
		2个。g的语义有get、全局。
		getattr
		gloabals
	h：4个。h的语义有has、哈希、帮助、hex
		hasattr
		hash
		help
		hex
	i：6个。i的语义有：id、输入、int、is、iter
		id
		input
		int
		isinstance
		issubclass
		iter
	j：没有。
	l：3个。l的语义有：长度、list、locals
		len
		list
		locals
	m：4个。m的语义有：map、max、memory、min
		max/min
		map
		memoryview
	n：1个。就是next。
	o：4个。o的语义有：对象、八进制、打开、ord
		object
		oct
		open
		ord：把字符转成int。
	p：3个。p的语义有pow、打印、属性。
		pow
		print
		property
	q：没有。
	r：4个。r的语义有：范围、repr、反转、取整。
		range
		repr
		reversed
		round
	s：8个。这个是最多的。s的语义有：set、slice、static、sort、字符串、sum、super
		set
		setattr
		sorted
		staticmethod
		str
		sum
		super
	t：2个。语义是tuple和type。
	u：没有。
	v：1个。vars。返回属性。
	w：没有。
	x：没有。
	z：1个。zip。
	
	其中表示数据类型的：从简单到复杂依次是：
		数字类型：int、float、complex
		迭代类型：list、tuple、range
		文本序列：str
		二进制序列类型：bytes、bytearray
		集合类型：set、frozenset。
		映射类型：dict。
	总共70个。
	
```

```
内置常量
	False
	True
	None
	NotImplemented
	Ellipsis
	__debug__
	一共6个。常用是前面3个。
	
由site添加的常量。在repl中比较有用。脚本里不要用。
    quit()
    exit()
    copyright
    credits
    license
```

```
内置异常
	不一一看了。
	
```

```
文本处理
	string
	re
	这2个算是最常用的。掌握这2个就好了。
```

```
二进制处理
	struct
	掌握这一个就好了。
```

```
数据类型
	datetime
	collections
	collections.abc
	array
	weakref
	enum
```

```
函数式编程模块
	itertools
	functools
	
```

```
文件和目录访问
	os.path
	fileinput
	tempfile
	glob
	shutil
```

```
数据持久化
	pickle：对象序列化。
	sqlite3
	
```

```
文件格式
	csv
	
```

```
通用os服务
	os
	io
	time
	argparse
	logging
	getpass
	platform
	errno
	ctypes
```

```
并发执行
	threading
	multiprocessing
	subprocess
	queue
	
```

```
网络和进程通信
	asyncio
	socket
	ssl
	mmap
	signal
```

```
互联网数据处理
	json
	base64
```

```
html处理
	html
	html.parser
	html.entities
	
```

```
互联网协议处理
	urllib
	http
	http.server
	http.client
	uuid
	
```

```
多媒体
	wav
```

```
开发工具
	typing：类型注解支持
	unittest
```

```
unix特有服务
	posix
	pwd
	grp
	tty
	fcntl
```

# 常用库分析

## sys模块有哪些接口

`sys` 模块提供了许多接口，用于与 Python 解释器、系统环境以及运行时相关的交互。以下是 `sys` 模块中一些常用的接口：

1. **`sys.argv`**: 包含命令行参数的列表，其中第一个参数是脚本的名称。

2. **`sys.executable`**: 返回 Python 解释器的路径。

3. **`sys.exit([arg])`**: 退出 Python 解释器，可选参数 `arg` 用于指定退出时的返回值。

4. **`sys.version`**: 返回 Python 解释器的版本信息。

5. **`sys.platform`**: 返回运行 Python 解释器的平台信息。

6. **`sys.stdin`**: 标准输入流的文件对象。

7. **`sys.stdout`**: 标准输出流的文件对象。

8. **`sys.stderr`**: 标准错误流的文件对象。

9. **`sys.modules`**: 一个字典，包含当前载入的所有模块。

10. **`sys.path`**: 包含用于查找模块的路径的列表。

11. **`sys.byteorder`**: 返回本地字节顺序的指示符，可能是 'big' 或 'little'。

12. **`sys.getsizeof(object[, default])`**: 返回对象的大小（以字节为单位），默认情况下包括间接开销。

13. **`sys.getfilesystemencoding()`**: 返回默认的文件系统编码名称。

14. **`sys.getdefaultencoding()`**: 返回 Unicode 字符串的默认编码。

15. **`sys.getrefcount(object)`**: 返回对象的引用计数。

这只是 `sys` 模块提供的一小部分接口。您可以通过查看官方文档或者在 Python 中使用 `help(sys)` 查看完整的接口列表和详细说明。

## os模块有哪些接口

`os` 模块是 Python 的标准库之一，用于与操作系统进行交互。它提供了许多接口来执行各种操作，包括文件和目录操作、进程管理、环境变量访问等。以下是 `os` 模块中一些常用的接口：

1. **文件和目录操作**：
   - `os.getcwd()`: 获取当前工作目录。
   - `os.chdir(path)`: 改变当前工作目录为指定路径。
   - `os.listdir(path='.')`: 返回指定目录下的文件和目录列表。
   - `os.mkdir(path[, mode=0o777])`: 创建一个新目录。
   - `os.makedirs(path[, mode=0o777])`: 递归创建多级目录。

2. **路径操作**：
   - `os.path.join(path1[, path2[, ...]])`: 将各部分路径组合成一个完整路径。
   - `os.path.exists(path)`: 判断路径是否存在。
   - `os.path.isfile(path)`: 判断路径是否为文件。
   - `os.path.isdir(path)`: 判断路径是否为目录。

3. **进程管理**：
   - `os.system(command)`: 在子 shell 中执行命令。
   - `os.spawnv(mode, path, args)`: 在新进程中执行程序。
   - `os.fork()`: 创建一个子进程（Unix/Linux 系统）。

4. **环境变量**：
   - `os.getenv(varname[, value])`: 获取指定环境变量的值。
   - `os.putenv(varname, value)`: 设置指定环境变量的值。

5. **文件操作**：
   - `os.remove(path)`: 删除指定路径的文件。
   - `os.rename(src, dst)`: 将文件或目录从 src 重命名为 dst。

6. **权限操作**：
   - `os.chmod(path, mode)`: 更改文件或目录的权限模式。

7. **其他**：
   - `os.getpid()`: 获取当前进程的 ID。
   - `os.kill(pid, signal)`: 向指定进程发送信号。

这些只是 `os` 模块提供的一小部分接口。您可以通过查看官方文档或者在 Python 中使用 `help(os)` 查看完整的接口列表和详细说明。

## itertools模块

`itertools` 模块是 Python 标准库中的一个模块，提供了许多用于迭代操作的函数。这些函数能够处理迭代器和可迭代对象，帮助我们更方便地进行迭代操作和组合。

以下是 `itertools` 模块中一些常用的函数：

1. **`itertools.count(start=0, step=1)`**：
   从指定的起始值开始生成无限迭代器，步长为指定值。

   ```python
   import itertools

   for i in itertools.count(1, 2):
       if i > 10:
           break
       print(i)  # 输出: 1, 3, 5, 7, 9
   ```

2. **`itertools.cycle(iterable)`**：
   创建一个无限循环的迭代器，不断重复指定的可迭代对象。

   ```python
   import itertools

   for i, item in enumerate(itertools.cycle(['a', 'b', 'c'])):
       if i >= 5:
           break
       print(item)  # 输出: a, b, c, a, b
   ```

3. **`itertools.repeat(elem, times=None)`**：
   将指定的元素重复生成指定次数的迭代器，如果 `times` 为 `None`，则生成无限次。

   ```python
   import itertools

   for i in itertools.repeat('hello', 3):
       print(i)  # 输出: hello, hello, hello
   ```

4. **`itertools.chain(*iterables)`**：
   将多个可迭代对象连接成一个迭代器。

   ```python
   import itertools

   iter1 = [1, 2, 3]
   iter2 = ['a', 'b', 'c']
   combined_iter = itertools.chain(iter1, iter2)
   for item in combined_iter:
       print(item)  # 输出: 1, 2, 3, a, b, c
   ```

5. **`itertools.combinations(iterable, r)`** 和 **`itertools.permutations(iterable, r=None)`**：
   分别生成指定长度的组合和排列。

   ```python
   import itertools

   items = ['a', 'b', 'c']
   for combination in itertools.combinations(items, 2):
       print(combination)  # 输出: ('a', 'b'), ('a', 'c'), ('b', 'c')

   for permutation in itertools.permutations(items, 2):
       print(permutation)  # 输出: ('a', 'b'), ('a', 'c'), ('b', 'a'), ('b', 'c'), ('c', 'a'), ('c', 'b')
   ```

这些只是 `itertools` 模块提供的一小部分功能。它还包含其他函数，例如用于组合、排列、分组和过滤的函数等。这些函数可以帮助我们简化迭代操作，提高代码的可读性和效率。

## concurrent

`concurrent` 模块实际上指的是 `concurrent.futures` 模块，它提供了高级别的接口来异步执行可调用对象（函数或其他可调用对象）的任务。这个模块使得并发编程变得更加容易，尤其是在处理 I/O 密集型任务时。以下是 `concurrent.futures` 模块中一些常用的接口：

1. **ThreadPoolExecutor 和 ProcessPoolExecutor**：
   这两个类分别用于创建线程池和进程池，它们提供了 `submit()` 方法来提交任务，并返回一个 `Future` 对象，可以用于获取任务的执行结果。

   ```python
   from concurrent.futures import ThreadPoolExecutor

   def some_function(x):
       return x * x

   with ThreadPoolExecutor() as executor:
       future = executor.submit(some_function, 10)
       result = future.result()
       print(result)  # 输出: 100
   ```

2. **map() 方法**：
   `ThreadPoolExecutor` 和 `ProcessPoolExecutor` 类都提供了 `map()` 方法，可以将可调用对象应用于可迭代对象的每个元素，并返回结果。

   ```python
   from concurrent.futures import ThreadPoolExecutor

   def square(x):
       return x * x

   with ThreadPoolExecutor() as executor:
       results = executor.map(square, [1, 2, 3, 4, 5])
       print(list(results))  # 输出: [1, 4, 9, 16, 25]
   ```

3. **shutdown() 方法**：
   用于关闭线程池或进程池，以释放资源。

   ```python
   from concurrent.futures import ThreadPoolExecutor

   with ThreadPoolExecutor() as executor:
       # 执行任务...
   # 在退出 with 块后，线程池将会被关闭
   ```

4. **Future 对象**：
   `submit()` 方法返回的对象，用于跟踪任务的状态并获取其结果。可以使用 `result()` 方法来获取任务的执行结果。

   ```python
   from concurrent.futures import ThreadPoolExecutor

   def some_function(x):
       return x * x

   with ThreadPoolExecutor() as executor:
       future = executor.submit(some_function, 10)
       # 等待任务完成并获取结果
       result = future.result()
       print(result)  # 输出: 100
   ```

这些是 `concurrent.futures` 模块中一些常用的接口，它们使得并发编程变得更加容易和直观。



### ThreadPoolExecutor 更加贴合实际的用法

当涉及到执行大量 I/O 密集型任务时，`ThreadPoolExecutor` 是一个非常有用的工具。它允许你在一个线程池中并发执行多个任务，而不会阻塞主线程，从而提高了程序的性能和响应性。

以下是 `ThreadPoolExecutor` 在实际用法中的一些常见场景：

1. **网络请求**：
   在进行网络请求时，往往会发生 I/O 阻塞，因为等待网络响应需要一定的时间。使用 `ThreadPoolExecutor` 可以让你并发地发起多个网络请求，从而加快整体的处理速度。

   ```python
   import requests
   from concurrent.futures import ThreadPoolExecutor

   def fetch_url(url):
       response = requests.get(url)
       return response.text

   urls = ['https://example.com', 'https://example.org', 'https://example.net']

   with ThreadPoolExecutor() as executor:
       results = executor.map(fetch_url, urls)

   for result in results:
       print(result)
   ```

2. **文件 I/O**：
   在读取或写入大量文件时，文件 I/O 操作也会成为性能瓶颈。使用 `ThreadPoolExecutor` 可以并发地读取或写入多个文件，以提高处理效率。

   ```python
   from concurrent.futures import ThreadPoolExecutor

   def read_file(filename):
       with open(filename, 'r') as file:
           return file.read()

   filenames = ['file1.txt', 'file2.txt', 'file3.txt']

   with ThreadPoolExecutor() as executor:
       results = executor.map(read_file, filenames)

   for result in results:
       print(result)
   ```

3. **数据库操作**：
   数据库查询和写入通常也是 I/O 密集型的任务。通过使用 `ThreadPoolExecutor`，可以并发地执行多个数据库操作，从而提高整体的数据库性能。

   ```python
   import sqlite3
   from concurrent.futures import ThreadPoolExecutor

   def fetch_data_from_database(query):
       connection = sqlite3.connect('example.db')
       cursor = connection.cursor()
       cursor.execute(query)
       result = cursor.fetchall()
       connection.close()
       return result

   queries = ['SELECT * FROM table1', 'SELECT * FROM table2', 'SELECT * FROM table3']

   with ThreadPoolExecutor() as executor:
       results = executor.map(fetch_data_from_database, queries)

   for result in results:
       print(result)
   ```

这些示例展示了在实际应用中如何使用 `ThreadPoolExecutor` 来并发地执行多个 I/O 密集型任务，从而提高程序的性能和效率。

### **ThreadPoolExecutor 和 ProcessPoolExecutor** 对比

`ThreadPoolExecutor` 和 `ProcessPoolExecutor` 

都是 Python 标准库中 `concurrent.futures` 模块提供的类，用于创建线程池和进程池，以便并发执行任务。

它们之间的主要区别在于它们执行任务的方式：

线程池使用线程来执行任务，而进程池使用进程来执行任务。

以下是它们之间的一些比较：

1. **性能**：
   - 线程池通常比进程池更轻量级，因为线程之间的切换开销比进程之间的切换开销要小。在某些情况下，特别是在 I/O 密集型任务中，线程池可能表现更好，因为它可以利用操作系统级别的线程调度来实现并发执行。
   - 进程池在处理 CPU 密集型任务时可能表现更好，因为它可以利用多核 CPU，并且由于 GIL（全局解释器锁）的存在，Python 的线程并不能充分利用多核 CPU。

2. **并发度**：
   - 线程池中的线程共享同一个进程的内存空间，因此它们可以轻松地共享数据。但是，由于 GIL 的存在，Python 中的多线程并不能实现真正的并行执行。
   - 进程池中的进程是独立的，每个进程都有自己独立的内存空间。因此，它们可以实现真正的并行执行，并且不受 GIL 的影响。但是，进程之间的通信和数据共享需要额外的开销。

3. **资源消耗**：
   - 线程池中的线程共享同一个进程的内存空间，因此它们之间的切换开销较小，但是线程之间的数据共享可能会引入线程安全问题。
   - 进程池中的进程是独立的，每个进程都有自己独立的内存空间，因此它们之间的数据共享相对更安全。但是，由于每个进程都需要独立的内存空间和系统资源，因此进程池可能会消耗更多的资源。

4. **适用场景**：
   - 线程池适用于 I/O 密集型任务，例如网络请求、文件 I/O 等，因为它们可以利用线程之间的并发执行来提高性能。
   - 进程池适用于 CPU 密集型任务，例如计算密集型的数值计算、图像处理等，因为它们可以利用多核 CPU 来实现真正的并行执行。

综上所述，选择使用 `ThreadPoolExecutor` 还是 `ProcessPoolExecutor` 取决于任务的特性以及性能和资源消耗的考量。在实际应用中，可以根据任务的类型和需求来选择合适的执行方式。

### ProcessPoolExecutor 实际代码举例

以下是一个使用 `ProcessPoolExecutor` 的简单示例，演示了如何使用多进程并发地计算斐波那契数列的值：

```python
from concurrent.futures import ProcessPoolExecutor

def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

def main():
    numbers = [35, 36, 37, 38, 39]  # 计算斐波那契数列的前五个数值

    with ProcessPoolExecutor() as executor:
        results = executor.map(fibonacci, numbers)

    for number, result in zip(numbers, results):
        print(f"Fibonacci({number}) = {result}")

if __name__ == "__main__":
    main()
```

在这个示例中，我们首先定义了一个 `fibonacci()` 函数，用于计算斐波那契数列的第 `n` 个数值。然后，我们定义了一个 `main()` 函数，在其中创建了一个 `ProcessPoolExecutor` 对象，并使用 `map()` 方法并发地计算了斐波那契数列的多个数值。最后，我们遍历结果并打印出每个数值对应的结果。

通过使用 `ProcessPoolExecutor`，我们可以利用多个进程并行地计算斐波那契数列的多个数值，从而提高了计算效率。在实际应用中，可以将类似的并行计算模式应用于各种 CPU 密集型任务，以提高程序的性能。

## ctypes模块

`ctypes` 模块是 Python 标准库中的一个模块，

用于调用动态链接库（DLL，Windows）、共享库（SO，Unix/Linux）等外部库中的函数。

它提供了一种简单的方法来与 C 语言编写的外部代码进行交互，

从而实现 Python 与底层系统或其他语言的集成。

以下是 `ctypes` 模块的一些常用功能和用法：

1. **加载动态链接库或共享库**：
   使用 `ctypes.CDLL()` 或 `ctypes.WinDLL()` 函数可以加载动态链接库或共享库。`CDLL()` 用于 Unix/Linux 系统，`WinDLL()` 用于 Windows 系统。

   ```python
   from ctypes import CDLL, WinDLL

   # Unix/Linux
   libc = CDLL("libc.so.6")

   # Windows
   kernel32 = WinDLL("kernel32.dll")
   ```

2. **调用外部函数**：
   使用加载的库对象的属性即可调用其中的函数。需要确保传递正确的参数类型和返回值类型。

   ```python
   # 调用 Unix/Linux 系统的 printf 函数
   libc.printf(b"Hello, %s!\n", b"world")

   # 调用 Windows 系统的 MessageBoxA 函数
   MessageBoxA = kernel32.MessageBoxA
   MessageBoxA(None, b"Hello", b"Message", 0)
   ```

3. **定义函数原型**：
   可以使用 `CFUNCTYPE()` 函数定义函数原型，以指定函数的参数类型和返回值类型。

   ```python
   from ctypes import CFUNCTYPE, c_int

   # 定义函数原型
   add_func = CFUNCTYPE(c_int, c_int, c_int)

   # 调用函数
   add = add_func(lambda x, y: x + y)
   print(add(3, 5))  # 输出: 8
   ```

4. **处理结构体和指针**：
   `ctypes` 还支持处理结构体和指针等数据类型，以便与底层 C 代码进行交互。

   ```python
   from ctypes import Structure, POINTER, c_int

   class Point(Structure):
       _fields_ = [("x", c_int), ("y", c_int)]

   p = Point(1, 2)
   print(p.x, p.y)  # 输出: 1 2

   p_ptr = POINTER(Point)(p)
   print(p_ptr.contents.x, p_ptr.contents.y)  # 输出: 1 2
   ```

通过使用 `ctypes` 模块，Python 可以方便地与底层 C 代码进行交互，调用外部函数、处理结构体和指针等，从而实现更高级别的集成和功能。

## json模块

`json` 库是 Python 标准库中的一个模块，用于处理 JSON（JavaScript Object Notation）格式的数据。JSON 是一种轻量级的数据交换格式，常用于在不同平台之间传递数据。`json` 库提供了一组功能来解析 JSON 数据、将 Python 数据结构转换为 JSON 格式以及将 JSON 数据解析为 Python 数据结构。

以下是 `json` 库的一些常用功能和用法：

1. **解析 JSON 数据**：
   使用 `json.loads()` 函数可以将 JSON 格式的字符串==解析为 Python 数据结构（通常是字典或列表）==。

   ```python
   import json

   json_string = '{"name": "John", "age": 30, "city": "New York"}'
   data = json.loads(json_string)
   print(data)  # 输出: {'name': 'John', 'age': 30, 'city': 'New York'}
   ```

2. **序列化 Python 数据**：
   使用 `json.dumps()` 函数可以将 Python 数据结构（字典、列表等）序列化为 JSON 格式的字符串。

   ```python
   import json

   data = {'name': 'John', 'age': 30, 'city': 'New York'}
   json_string = json.dumps(data)
   print(json_string)  # 输出: {"name": "John", "age": 30, "city": "New York"}
   ```

3. **读取和写入 JSON 文件**：
   使用 `json.load()` 函数可以从 JSON 文件中读取数据，并使用 `json.dump()` 函数可以将数据写入到 JSON 文件中。

   ```python
   import json

   # 读取 JSON 文件
   with open('data.json', 'r') as file:
       data = json.load(file)
       print(data)

   # 写入 JSON 文件
   data = {'name': 'John', 'age': 30, 'city': 'New York'}
   with open('data.json', 'w') as file:
       json.dump(data, file)
   ```

4. **处理特殊类型**：
   `json` 库支持处理一些特殊类型，如字符串、数字、布尔值、None 值等。

   ```python
   import json

   data = {
       'name': 'John',
       'age': 30,
       'is_student': False,
       'grades': [85, 90, 88],
       'address': None
   }
   json_string = json.dumps(data)
   print(json_string)
   ```

通过使用 `json` 库，Python 可以方便地处理 JSON 格式的数据，从而实现与其他平台和系统的数据交换和通信。

## logging模块

`logging` 模块是 Python 标准库中的一个模块，用于记录程序运行时的日志信息。它提供了一种灵活而强大的日志记录工具，可以帮助开发人员在程序运行过程中收集、存储和分析各种类型的日志信息。

以下是 `logging` 模块的一些常用功能和用法：

1. **创建日志记录器**：
   使用 `logging.getLogger()` 函数可以创建一个日志记录器对象，用于记录程序中的日志信息。

   ```python
   import logging

   logger = logging.getLogger('example_logger')
   ```

2. **配置日志记录器**：
   使用 `logging.basicConfig()` 函数可以配置日志记录器的基本设置，如日志级别、格式、处理程序等。

   ```python
   logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
   ```

3. **记录日志信息**：
   使用日志记录器对象的各种方法（如 `debug()`、`info()`、`warning()`、`error()`、`critical()`）记录不同级别的日志信息。

   ```python
   logger.debug('This is a debug message')
   logger.info('This is an info message')
   logger.warning('This is a warning message')
   logger.error('This is an error message')
   logger.critical('This is a critical message')
   ```

4. **添加处理程序**：
   可以添加不同类型的处理程序（如文件处理程序、控制台处理程序、SMTP 处理程序等）来处理不同级别的日志信息。

   ```python
   file_handler = logging.FileHandler('example.log')
   console_handler = logging.StreamHandler()

   logger.addHandler(file_handler)
   logger.addHandler(console_handler)
   ```

5. **设置日志级别**：
   可以通过设置日志记录器对象的级别来控制记录的日志信息的级别，只有达到或超过该级别的日志消息才会被记录。

   ```python
   logger.setLevel(logging.DEBUG)
   ```

6. **自定义日志格式**：
   可以通过设置日志格式来自定义日志消息的显示格式，包括时间、日志级别、消息内容等。

   ```python
   formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
   file_handler.setFormatter(formatter)
   ```

通过使用 `logging` 模块，Python 可以方便地实现程序运行时的日志记录功能，从而帮助开发人员更好地理解和调试程序，及时发现和解决问题。

## argparse模块

`argparse` 模块是 Python 标准库中的一个模块，用于解析命令行参数。它提供了一种简单而灵活的方式来处理命令行参数，并生成帮助文档，从而使得编写命令行工具和脚本变得更加容易和方便。

以下是 `argparse` 模块的一些常用功能和用法：

1. **创建解析器**：
   使用 `argparse.ArgumentParser()` 函数可以创建一个参数解析器对象，用于解析命令行参数。

   ```python
   import argparse

   parser = argparse.ArgumentParser(description='Description of your program')
   ```

2. **添加参数**：
   使用 `add_argument()` 方法可以向解析器中添加命令行参数，包括位置参数和可选参数。可以指定参数的名称、类型、默认值等属性。

   ```python
   parser.add_argument('filename', help='Name of the file to process')
   parser.add_argument('-o', '--output', help='Name of the output file')
   parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose mode')
   ```

3. **解析命令行参数**：
   使用 `parse_args()` 方法可以解析命令行参数，并返回一个包含参数值的命名空间对象。

   ```python
   args = parser.parse_args()
   ```

4. **访问参数值**：
   可以通过访问命名空间对象的属性来获取命令行参数的值。

   ```python
   print(args.filename)
   print(args.output)
   print(args.verbose)
   ```

5. **生成帮助文档**：
   使用 `print_help()` 方法可以生成参数解析器的帮助文档，并显示在命令行界面上。

   ```python
   parser.print_help()
   ```

通过使用 `argparse` 模块，Python 可以方便地处理命令行参数，使得编写命令行工具和脚本变得更加简单和直观。它提供了丰富的功能和选项，可以满足各种不同的命令行参数处理需求。