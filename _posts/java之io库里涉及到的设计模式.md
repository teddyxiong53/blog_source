---
title: java之io库里涉及到的设计模式
date: 2019-04-04 11:27:30
tags:
	- java

---



java的io库的设计，用到了2个设计模式：装饰模式和适配器模式。

java io库的2个对称性：

```
1、输入输出的对称。
2、字节和字符的对称。
```

看看InputStream相关的装饰器模式。

首先看层次关系

```
InputStream
	ByteArrayInputStream
	FileInputStream
	FilterInputStream
		BufferedInputStream
		DataInputStream
		LineNumberInputStream
		PushbackInputStream
	ObjectInputStream
	SequenceInputStream
	StringBufferInputStream
```

分析

```
抽象组件（Component）是InputStream类。
具体组件（ConcreteComponent）就是ByteArrayInputStream这些第二层的类。
抽象装饰（Decorator）是FilterInputStream
具体装饰（ConcreteDecorator）是BufferedInputStream这些第三层的类。
```



看具体代码：

```
public class FilterInputStream extends InputStream {
    protected volatile InputStream in;//持有InputStream对象。
```





参考资料

1、设计模式在Java I/O中的应用(装饰模式和适配器模式)

https://blog.csdn.net/puma_dong/article/details/23018555