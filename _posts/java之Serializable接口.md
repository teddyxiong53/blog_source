---
title: java之Serializable接口
date: 2019-04-03 11:19:04
tags:
	- java

---





先需要了解序列号的概念。

一个对象的生命随着所在的进程退出而结束。

但是有时候，你需要把内存里的各种对象及当时的状态保存到磁盘上。

然后可以在需要的时候再恢复出来。

怎么来实现呢？就是靠序列化。

一个类需要序列号，需要实现Serializable接口。

例如，一个Person类。

```
class Person implements Serializable {
    private static final long serialVersionUID = 1;
    String name;
    int age;
    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }
    public String toString() {
        return "name:" + name + " age: " + age;
    }
}
```

用ObjectOutputStream来写出。

用ObjectInputStream来读取。

serialVersionUID 这个成员变量，只要你实现了Serializable接口，IDE就会提示你加上的。

这个就是版本号。是为了多台机器上的版本一致性。避免出错。



参考资料

1、我对java中Serializable接口的理解

http://blademastercoder.github.io/2015/01/29/java-Serializable.html