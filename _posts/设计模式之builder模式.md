---
title: 设计模式之builder模式
date: 2019-04-08 13:16:30
tags:
	- 设计模式

---



builder模式，中文翻译为建造者模式。

什么是builder模式？为什么需要builder模式？builder模式解决了什么问题？

builder模式的构成部分有哪些？



builder模式要解决的是构造复杂对象的问题。



问题的由来

当我们需要创建一个复杂的对象的时候，使用静态工厂或者构造器的方式，就显得非常笨拙。

因为他们有一个共同的局限性，就是不能很好地扩展大量可选参数。

我们举个例子，以Person来看。

除了姓名、年龄、性别、生日这些必要的属性之外，还有许多可选的属性，例如身高、学历、体重等。

对于这样的对象，我们应该怎样来创建呢？

无论是重叠构造器、还是JavaBean模式，都不能很好地解决这个问题。

而builder模式就是为了这种情况而出现的。

为了更好地体现builder模式的优势，我们先用重叠构造器和JavaBean来看看怎么解决这个问题。



#重叠构造器

```
这种解决办法就是：
1、定义一个构造函数，只包含所有必选参数。
2、定义一个构造函数，出来包含必选参数，包含一个可选参数。
3、包含2个可选参数。
4、依次类推，直到定义了一个包含了所有参数的构造函数。
```

这个非常不优雅。



#JavaBean方式

这种就是定义先new一个空的Person，然后一步步setXxx来设置。

代码也很丑陋。各种set还在多线程并发时比较麻烦。



#builder模式

我们直接看代码。

```
public class Person {
    private final String name;//必选
    private final String gender;//必选

    private final int weight;//可选
    private final int height;//可选

    //私有构造函数，Person对象的创建必选使用builder。
    private Person(Builder builder) {
        this.name = builder.name;
        this.gender = builder.gender;
        this.weight = builder.weight;
        this.height = builder.height;
    }

    public static class Builder {
        private final String name;//必选
        private final String gender;//必选

        private  int weight;//可选，不用final
        private  int height;//可选

        public Builder (String name, String gender){
            this.name = name;
            this.gender  = gender;
        }

        public Builder weight(int weight) {
            this.weight = weight;
            return this;
        }
        public Builder height(int height) {
            this.height = height;
            return this;
        }

        public Person build() {
            return new Person(this);//每次都创建一个新的Person对象。
        }
    }

}
```

使用是这么用：

```
Person.Builder builder = new Person.Builder("xx", 10);
builder.weight(100).height(100);
```



builder模式的优点：

```
1、可读性好，采用了链式调用。

```





参考资料

1、优雅地创建复杂对象 —— Builder 模式

https://blog.csdn.net/justloveyou_/article/details/78298420