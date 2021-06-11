---
title: qt之QObject
date: 2021-06-08 19:42:11
tags:
	- qt

---

--

QObject 是所有Qt对象的基类。

QObject 是Qt模块的核心。

它的最主要特征是关于**对象间无缝通信的机制**：信号与槽。

使用connect()建立信号到槽的连接，使用disconnect()销毁连接，

使用blockSignals()暂时阻塞信号以**避免无限通知循环**，

使用connectNotify()和disconnectNotify()追踪连接。



QObject 以对象树的形式组织起来。

当为一个对象创建子对象时，子对象会自动地添加到父对象的children()列表中。

父对象拥有子对象的所有权，

**比如父对象可以在自己的析构函数中删除它的孩子对象。**

使用findChild()或findChildren()通过名字和类型查询孩子对象。

**每个对象都有objectName()，也可以通过metaObject()获得它的类名。可以使用inherits()检测对象的类是否在某个类的继承层次结构中。**

对象被删除时，发射destroyed()信号，捕捉这个信号以免悬挂对这个对象的引用。

QObject 通过event()接收事件，

通过installEventFilter()和enventFilter()过滤来自其他对象的事件。

childEvent()可以捕捉来自子对象的事件。



**宏Q_OBJECT是任何实现信号、槽或属性的强制性要求。**

不管是否需要实现这些机制，都要求使用这个宏。

否则会引发一些函数的奇怪行为。

所有的Qt部件都继承自QObject 。

函数isWidgetType()检测对象是否一个部件。

它比以下这些语句要运行得更快:qobject_cast(obj) 或者obj->inherits("QWidget")。

children()返回QObjectList，它是QList的typedef。



没有复制构造函数和赋值操作符

**QObject 既没有复制构造函数也没有赋值操作符**。

实际上它们使用宏Q_DISABLE_COPY()声明在私有部份。

**所有派生自QObject 的对象都使用这个宏声明复制构造函数和赋值操作符为私有**。

这样的**主要结果是，在使用QObject子对象作为值的地方要使用QObject类型的指针**。

**因为没有构造函数，你不能把QObject 的子对象作为值存储在容器类中，必须存储它的指针。**



自动连接

Qt的元对象系统**自动地为**QObject 的子类和他们的**对象建立信号和槽的连接**。

只要有名字的对象被定义，槽就会自动拥有简单的约定命名，

连接在运行时间通过函数QMetaObject::connectSlotsByName()执行。



国际化

所有的 QObject 支持Qt的转换特性。

能够使用户界面在不同语言间进行转换。

为了将用户可见的文本得到转换，必须将它们包裹到函数tr()中。



我们知道，**在C++中，几乎每一个类(class)中都需要有一些类的成员变量(class member variable)**，在通常情况下的做法如下：

```
class Person
{
private:
    string mszName; // 姓名
    bool mbSex;    // 性别
    int mnAge;     // 年龄
};
```

**在QT中，却几乎都不是这样做的，那么，QT是怎么做的呢？**

几乎每一个C++的类中都会保存许多的数据，要想读懂别人写的C++代码，就一定需要知道每一个类的的数据是如何存储的，是什么含义，否则，我们不可能读懂别人的C++代码。

在这里也就是说，要想读懂QT的代码，第一步就必须先搞清楚QT的类成员数据是如何保存的。

为了更容易理解QT是如何定义类成员变量的，

我们先说一下QT 2.x 版本中的类成员变量定义方法，

因为在 2.x 中的方法非常容易理解。

然后在介绍 QT 4.4 中的类成员变量定义方法。



**QT 2.x 中的方法**

在定义class的时候(在.h文件中)，只包含有一个，只是定义一个成员数据指针，

然后由这个指针指向一个数据成员对象，

这个数据成员对象包含所有这个class的成员数据，

然后在class的实现文件(.cpp文件)中，定义这个私有数据成员对象。

示例代码如下：

```
// File name:  person.h
 struct PersonalDataPrivate; // 声明私有数据成员类型
 class Person
{
public:
 Person ();   // constructor
virtual ~Person ();  // destructor
void setAge(const int);
int getAge();
 private:
 PersonalDataPrivate* d;
};
 //---------------------------------------------------------------------
// File name:  person.cpp
 struct PersonalDataPrivate  // 定义私有数据成员类型
{
string mszName; // 姓名
bool mbSex;    // 性别
int mnAge;     // 年龄
};
 
// constructor
Person::Person ()
{
d = new PersonalDataPrivate;
};
 
// destructor
Person::~Person ()
{
delete d;
};
 
void Person::setAge(const int age)
{
if (age != d->mnAge)
d->mnAge = age;
}
 
int Person::getAge()
{
return d->mnAge;
}
```

在最初学习QT的时候，我也觉得这种方法很麻烦，但是随着使用的增多，我开始很喜欢这个方法了，而且，现在我写的代码，基本上都会用这种方法。

具体说来，它有如下优点：

\* **减少头文件的依赖性**
把具体的数据成员都放到cpp文件中去，这样，在需要修改数据成员的时候，只需要改cpp文件而不需要头文件，这样就可以避免一次因为头文件的修改而导致所有包含了这个文件的文件全部重新编译一次，尤其是当这个头文件是非常底层的头文件和项目非常庞大的时候，优势明显。
同时，也减少了这个头文件对其它头文件的依赖性。

可以把只在数据成员中需要用到的在cpp文件中include一次就可以，在头文件中就可以尽可能的减少include语句

\* **增强类的封装性**
这种方法增强了类的封装性，**无法再直接存取类成员变量，**而必须写相应的 get/set 成员函数来做这些事情。
关于这个问题，仁者见仁，智者见智，每个人都有不同的观点。

有些人就是喜欢把类成员变量都定义成public的，在使用的时候方便。

只是我个人不喜欢这种方法，当项目变得很大的时候，有非常多的人一起在做这个项目的时候，自己所写的代码处于底层有非常多的人需要使用(#include)的时候，这个方法的弊端就充分的体现出来了。

还有，我不喜欢 QT 2.x 中把数据成员的变量名都定义成只有一个字母d，看起来很不直观，尤其是在search的时候，很不方便。但是，QT kernel 中的确就是这么干的。



**QT 4.4.x 中的方法**

在 QT 4.4 中，**类成员变量定义方法的出发点没有变化**，只是在具体的实现手段上发生了非常大的变化，在 QT 4.4 中，**使用了非常多的宏来做事，这凭空的增加了理解 QT source code 的难度**，不知道他们是不是从MFC学来的。就连在定义类成员数据变量这件事情上，也大量的使用了宏。

在这个版本中，类成员变量不再是给每一个class都定义一个私有的成员，而是把这一项common的工作放到了最基础的基类 QObject 中，然后定义了一些相关的方法来存取，好了，让我们进入具体的代码吧。





参考资料

1、QT:QObject 简单介绍

https://blog.csdn.net/aidem_brown/article/details/80236188