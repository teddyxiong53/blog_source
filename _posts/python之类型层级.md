---
title: python之类型层级
date: 2019-01-03 11:43:59
tags:
	- python

---



```
标准类型层级
None

NotImplemented

Ellipsis 这个是省略号。

numbers.Number
	numbers.Integers
		Integers
		Booleans
	numbers.Real
	numbers.Complex
Sequences
	Immutable sequences
		Strings
		Tuples
		Bytes
	Mutable sequences
		Lists
		Byte Arrays
Set types
	Sets
	Frozen sets
	
Mappings
	Dictionaries
	
Callable types
	user defined function
	instance method
	Generator method
	Coroutine functions
	Async generator function
	Built-in function
	built-in method
	Classes
Modules
Custom classes
Class instances
IO objects
Internal types
	code objects
	Frame objects
	Traceback objects
	Slice objects
	static method objects
	class method objects
```



参考资料

1、

https://docs.python.org/3/reference/datamodel.html#types