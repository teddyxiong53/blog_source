---
title: java之序列化
date: 2017-12-28 11:43:16
tags:
	- java

---



看java的代码里，有serialVersionUID这个东西。下面梳理一下相关内容。



java序列化是用来保存内存中各种对象的状态的。当然你可以自己用各种方法来保存Object States，但是java已经给你提供了一套现成的。

# 序列化的基本含义

是指把结构化的对象变成无结构的字节流，方便传输和存储。

一个类只要实现了Serializable接口，这个类的对象就可以被序列化。



# 什么时候需要序列化？

1、当你想把内存中的对象保存到文件或者数据库的时候。

2、当你想用socket在网络上传送对象时。

3、当你想通过RMI传输对象的时候。

# 当你对一个对象实现序列化的时候，发生了什么？

在没有序列化前，每个保存在Heap里的对象都有相应的state。例如：

```
Foo myFoo = new Foo();
myFoo.setH(10);
myFoo.setW(20);
```

现在我们用下面的代码进行序列化：

```
FileOutpuStream fs = new FileOutputStream("foo.ser");
ObjectOutputStream os = new ObjectOutputStream(fs);
os.writeObject(myFoo);
```

当上面的代码执行完之后，myFoo这对象的相关属性都被保存起来了。你再次从文件中把它读取出来后，所有属性都恢复到保存时的样子。

# serialVersionUID跟序列化的关系是什么？

1、一个类要实现序列化和反序列化，不生命serialVersionUID也可以的。

2、serialVersionUID是用来辅助序列化的。

3、在进行序列化和反序列化的时候，只有serialVersionUID一样，反序列化才能成功。

例如我们在这台电脑上进行了序列化，传输给另外一台电脑，另外一台电脑上相关类的版本不一致（这个是通过比较serialVersionUID得到的），则肯定无法正确进行反序列化的。



