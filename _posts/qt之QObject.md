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



# 代码分析

我是看buildroot里的集成的qt的代码。

```
qmetaobject.h里
QMetaMethod
	有这些常用方法：
	methodSignature

	
QMetaMethodPrivate

	
qobjectdefs.h

QMetaObject

	className
	superClass 返回d.superdata;
	inherits
	cast
	tr
	
	methodOffset
	enumeratorOffset
	propertyOffset
	classInfoOffset
	
	constructorCount
	methodCount
	enumeratorCount
	propertyCount
	classInfoCount
	
	indexOfConstructor
	indexOfMethod
	...
	
	connect
	disconnect
	disconnectOne
	connectSlotsByName
	
	activate
	invokeMethod
	
	newInstance
	
	struct {
	}d; //private data

	
QMetaObject::Connection
```

# 元对象meta object

在Qt框架中，元对象（Meta-Object）是一种特殊的概念，它包含了关于类的元信息，使得在运行时能够进行一些高级的操作，如信号与槽连接、动态属性访问和对象间的通信。以下是有关Qt元对象的详细信息：

1. **元对象系统：** Qt中的元对象系统是一种机制，**它允许在运行时获取有关类的信息**，而不仅仅是类的结构和函数签名。元对象系统包括类的名称、父类的名称、信号和槽的信息、动态属性以及其他类的元信息。

2. **`Q_OBJECT` 宏：** 在Qt中，如果一个类需要使用元对象系统，必须在类的声明中包含 `Q_OBJECT` 宏。这告诉Qt的元对象编译器（MOC，Meta-Object Compiler）对这个类进行处理，以生成元对象的信息。

   ```cpp
   class MyObject : public QObject {
       Q_OBJECT
   public:
       // ...
   };
   ```

3. **信号与槽：** 一个类可以定义信号和槽，**它们允许对象之间进行异步通信。**信号是类似于事件的通知，而槽是响应这些通知的函数。元对象系统允许在运行时建立信号与槽的连接，以便对象之间的通信。

   ```cpp
   class MyObject : public QObject {
       Q_OBJECT
   signals:
       void dataChanged();
   public slots:
       void updateData();
   };
   ```

4. **属性系统：** Qt的元对象系统还支持动态属性，允许在运行时添加、查询和修改对象的属性。这对于创建可扩展的、高度定制的对象非常有用。

5. **运行时类型信息（RTTI）：** 元对象系统还提供了一种跨库边界的运行时类型信息（RTTI）机制，允许在不同库中安全地进行对象类型的查询和转换。

6. **国际化和本地化：** Qt的元对象系统也用于国际化和本地化，允许应用程序支持多种语言和区域设置。

总之，Qt的元对象系统是该框架的一个关键部分，它提供了一种强大的方式来处理对象的元信息和通信。它使Qt成为一个非常灵活、可扩展和易于维护的开发框架，特别适用于创建跨平台应用程序和用户界面。通过信号与槽、属性系统和运行时类型信息，Qt的元对象系统使开发者能够编写高效的、模块化的代码。



除了提供对象间通信的信号和槽机制（引入该系统的主要原因）之外，元对象代码还提供以下附加功能：

QObject::metaObject() 返回该类的关联元对象。
QMetaObject::className() 在运行时以字符串形式返回类名，无需通过 C++ 编译器提供本机运行时类型信息 (RTTI) 支持。
QObject::inherits() 函数返回一个对象是否是继承 QObject 继承树中指定类的类的实例。
QObject::tr() 翻译字符串以实现国际化。
QObject::setProperty() 和 QObject::property() 按名称动态设置和获取属性。
QMetaObject::newInstance() 构造该类的一个新实例。



还可以在 QObject 类上使用 qobject_cast() 执行动态转换。 qobject_cast() 函数的行为与标准 C++dynamic_cast() 类似，其优点是不需要 RTTI 支持并且可以跨动态库边界工作。它尝试将其参数转换为尖括号中指定的指针类型，如果对象类型正确（在运行时确定），则返回非零指针；如果对象类型不兼容，则返回 nullptr。



# moc 元对象编译器

Qt MOC（元对象编译器）是 Qt 框架中的一个工具，用于处理与 Qt 的元对象系统相关的任务。以下是关于 Qt MOC 的一些关键信息：

1. **元对象系统：** Qt 中的元对象系统是一种用于处理 C++ 类的元信息的机制。**元信息包括类的名称、父类的名称、信号和槽的信息等。**元对象系统使得在运行时能够动态地访问和操作类的属性、方法以及信号与槽。

2. **为什么需要 MOC：** C++ 本身不提供元信息的运行时访问，但 Qt 通过 MOC 工具实现了这一功能。MOC 会处理带有 Qt 特殊宏（如 `Q_OBJECT`）的类，将它们的元信息提取出来，以便在运行时能够执行信号与槽连接、动态属性访问等操作。

3. **MOC 的工作流程：** MOC 的工作流程如下：
   - 首先，MOC 会扫描包含特殊宏（如 `Q_OBJECT`）的 C++ 源文件。
   - 然后，**MOC 会生成一个额外的 C++ 源文件（通常以 `.moc` 扩展名结尾），其中包含了类的元信息和与信号槽相关的代码。**
   - 这个生成的源文件会被编译并链接到应用程序中，以提供元对象系统的功能。

4. **示例：** 假设有一个名为 `MyWidget` 的类，它使用了 `Q_OBJECT` 宏，而且具有信号和槽。在编译时，MOC 将生成一个 `moc_mywidget.cpp` 文件，其中包含 `MyWidget` 类的元信息和信号槽的实现。

   ```cpp
   // 在 MyWidget 类中使用 Q_OBJECT 宏
   class MyWidget : public QWidget {
       Q_OBJECT

   public:
       MyWidget(QWidget* parent = nullptr);

   signals:
       void mySignal();

   public slots:
       void mySlot();
   };
   ```

5. **MOC 的使用：** MOC 是在 Qt 的构建系统中自动运行的，无需手动调用。只需在需要使用信号和槽的类中添加 `Q_OBJECT` 宏，MOC 就会自动处理并生成必要的代码。

总之，Qt MOC 是 Qt 框架的重要组成部分，它使 Qt 具有了元对象系统的功能，允许在运行时进行对象的动态访问和通信，尤其是信号与槽的机制。这是 Qt 中许多强大特性的基础，使 Qt 成为一个非常强大和灵活的开发框架。

# 属性系统

Qt 提供了一个复杂的属性系统，类似于某些编译器供应商提供的系统。

然而，作为一个独立于编译器和平台的库，Qt 不依赖于 __property 或 [property] 等非标准编译器功能。 

Qt 解决方案可与 Qt 支持的每个平台上的任何标准 C++ 编译器配合使用。

它基于元对象系统，还通过信号和槽提供对象间通信。



Qt 的属性系统是一种用于在运行时为对象添加、查询和管理属性的机制。

它提供了一种方便的方式来动态地扩展对象的功能，使其更加灵活和可定制。

以下是有关 Qt 属性系统的详细信息：

1. **属性是什么：** 在 Qt 中，属性是与对象关联的值，可以用于描述对象的状态、特性或配置。属性可以是基本数据类型（如整数、字符串、布尔值等），也可以是自定义的复杂数据类型。

2. **`QObject` 基类：** Qt 的属性系统主要建立在 `QObject` 类之上。如果一个类继承自 `QObject`，它就具备了属性系统的基本能力。为了使用属性系统，需要在类声明中包含 `Q_OBJECT` 宏。

   ```cpp
   class MyObject : public QObject {
       Q_OBJECT
   public:
       // ...
   };
   ```

3. **声明属性：** 在类中，您可以使用 `Q_PROPERTY` 宏来声明属性。这个宏通常用于类的声明部分，并指定了属性的名称、类型以及访问函数。

   ```cpp
   class MyObject : public QObject {
       Q_OBJECT
       Q_PROPERTY(int myProperty READ getMyProperty WRITE setMyProperty)
   public:
       // ...
   };
   ```

4. **访问属性：** 每个属性通常都有一个读取（`READ`）和一个写入（`WRITE`）函数，以便在运行时查询和设置属性的值。这些函数的命名通常遵循一定的约定，例如 `getPropertyName` 和 `setPropertyName`。

   ```cpp
   class MyObject : public QObject {
       Q_OBJECT
       Q_PROPERTY(int myProperty READ getMyProperty WRITE setMyProperty)
   public:
       int getMyProperty() const;
       void setMyProperty(int value);
   };
   ```

5. **使用属性：** 一旦属性被声明和访问函数被实现，您可以在运行时使用 `QObject::property()` 方法来查询属性的值，并使用 `QObject::setProperty()` 方法来设置属性的值。

   ```cpp
   MyObject obj;
   obj.setProperty("myProperty", 42);
   int value = obj.property("myProperty").toInt();
   ```

6. **信号与槽：** Qt 的属性系统可以与信号和槽机制集成，以便在属性值发生变化时触发信号，从而通知其他对象。

7. **动态属性：** Qt 的属性系统还允许您在运行时动态地添加、查询和修改对象的属性，而无需在类的声明中显式声明这些属性。这对于实现高度可定制的对象非常有用。

属性系统的使用场景包括创建可视化用户界面、实现国际化和本地化、管理对象的状态以及支持插件式架构等。它是 Qt 框架中的一个非常强大和灵活的特性，有助于使应用程序更加可维护和可扩展。



标准 C++ 对象模型为对象范例提供了非常有效的运行时支持。

但其静态特性在某些问题领域中缺乏灵活性。

图形用户界面编程是一个既需要运行时效率又需要高度灵活性的领域。 

Qt 通过将 C++ 的速度与 Qt 对象模型的灵活性相结合来实现这一点。

Qt 将以下功能添加到 C++ 中：

一种非常强大的无缝对象通信机制，称为信号和槽
可查询和可设计的对象属性
强大的事件和事件过滤器
国际化的上下文字符串翻译
复杂的间隔驱动定时器，可以在事件驱动的 GUI 中优雅地集成许多任务
分层且可查询的对象树，以自然的方式组织对象所有权
受保护的指针 (QPointer)，当引用的对象被销毁时，它们会自动设置为 0，这与普通 C++ 指针不同，普通 C++ 指针在其对象被销毁时会变成悬空指针
跨库边界的动态转换。
支持自定义类型创建。

# 重要的类

| [QMetaClassInfo](https://doc.qt.io/qt-6/qmetaclassinfo.html) | Additional information about a class                     |
| ------------------------------------------------------------ | -------------------------------------------------------- |
| [QMetaEnum](https://doc.qt.io/qt-6/qmetaenum.html)           | Meta-data about an enumerator                            |
| [QMetaMethod](https://doc.qt.io/qt-6/qmetamethod.html)       | Meta-data about a member function                        |
| [QMetaObject](https://doc.qt.io/qt-6/qmetaobject.html)       | Contains meta-information about Qt objects               |
| [QMetaProperty](https://doc.qt.io/qt-6/qmetaproperty.html)   | Meta-data about a property                               |
| [QMetaSequence](https://doc.qt.io/qt-6/qmetasequence.html)   | Allows type erased access to sequential containers       |
| [QMetaType](https://doc.qt.io/qt-6/qmetatype.html)           | Manages named types in the meta-object system            |
| [QObject](https://doc.qt.io/qt-6/qobject.html)               | The base class of all Qt objects                         |
| [QObjectCleanupHandler](https://doc.qt.io/qt-6/qobjectcleanuphandler.html) | Watches the lifetime of multiple QObjects                |
| [QPointer](https://doc.qt.io/qt-6/qpointer.html)             | Template class that provides guarded pointers to QObject |
| [QSignalBlocker](https://doc.qt.io/qt-6/qsignalblocker.html) | Exception-safe wrapper around QObject::blockSignals()    |
| [QSignalMapper](https://doc.qt.io/qt-6/qsignalmapper.html)   | Bundles signals from identifiable senders                |
| [QVariant](https://doc.qt.io/qt-6/qvariant.html)             | Acts like a union for the most common Qt data types      |

## QPointer  类作用

`QPointer` 是 Qt 框架中的一个类，用于管理指向 `QObject` 或其派生类的指针。

它的主要作用是提供一种安全的方式来管理对象指针，以避免悬挂指针问题和内存泄漏。

以下是 `QPointer` 类的主要作用和用法：

1. **避免悬挂指针问题：** 在 C++ 编程中，当一个对象被销毁后，如果其他地方还存在指向该对象的指针，这些指针就会变成悬挂指针，进而导致未定义的行为。`QPointer` 可以安全地管理指向 `QObject` 的指针，一旦对象被销毁，`QPointer` 会自动将指针设置为 `nullptr`，而不会成为悬挂指针。

2. **监视对象的生命周期：** 使用 `QPointer`，您可以监视一个对象的生命周期。如果对象被销毁，`QPointer` 会在检索时自动将其设置为 `nullptr`，从而允许您检测对象是否仍然存在。

3. **与信号槽机制结合使用：** 当您在信号和槽连接中使用 `QPointer` 时，如果连接的对象被销毁，连接会自动断开，避免了悬挂的信号槽连接。

以下是 `QPointer` 的简单示例：

```cpp
#include <QPointer>
#include <QObject>

int main() {
    QObject* obj = new QObject;
    QPointer<QObject> pointer(obj);

    // ...

    delete obj;  // 当对象被删除后，QPointer 会自动将指针置为 nullptr

    if (pointer.isNull()) {
        // 对象已销毁
        // 可以安全地访问 pointer
    }

    // ...
    
    return 0;
}
```

在这个示例中，当 `obj` 对象被删除后，`pointer` 会自动变成 `nullptr`，避免了悬挂指针问题。

总之，`QPointer` 是 Qt 中用于管理 `QObject` 派生类指针的一个非常有用的工具，它确保了指向对象的指针在对象销毁后不会导致未定义的行为，从而提高了程序的稳定性和可维护性。

## QVariant 类作用

我的理解：这个不就是动态语言的通用类型嘛。



`QVariant` 是 Qt 框架中的一个类，用于处理各种数据类型的通用容器。它的主要作用是在不同的数据类型之间进行类型安全的转换和存储。以下是 `QVariant` 类的主要作用：

1. **通用数据容器：** `QVariant` 可以存储各种数据类型的值，包括基本数据类型（如整数、浮点数、布尔值）、自定义数据类型、Qt 的类（如 `QString`、`QDateTime`、`QColor` 等）以及其他标准 C++ 类型。

2. **类型安全的数据转换：** `QVariant` 提供了一组函数，用于将存储的数据类型安全地转换为其他数据类型。这些转换函数在进行类型转换时会检查数据的有效性，避免了潜在的类型错误。

3. **处理不同数据类型的通用接口：** `QVariant` 允许您以统一的方式处理不同的数据类型，而不需要显式地进行类型检查和转换。这对于编写通用的数据处理代码非常有用，尤其是在处理用户界面元素或插件时。

4. **与信号槽机制结合使用：** `QVariant` 可以与 Qt 的信号槽机制结合使用，允许对象之间以一种灵活的方式传递不同类型的数据。这对于实现插件化的应用程序或创建通用的组件非常有用。

5. **支持自定义数据类型：** 您可以使用 `Q_DECLARE_METATYPE` 宏和 `qRegisterMetaType` 函数将自定义数据类型注册到 `QVariant`，从而使其可以被 `QVariant` 存储和转换。

6. **国际化和本地化：** `QVariant` 也用于支持国际化和本地化，因为它可以存储不同语言和区域设置下的文本、日期时间等数据。

以下是一个简单的示例，演示了如何使用 `QVariant` 存储和转换不同的数据类型：

```cpp
#include <QVariant>
#include <QString>
#include <QDebug>

int main() {
    QVariant var;
    int intValue = 42;
    QString strValue = "Hello, Qt!";
    
    // 存储整数和字符串
    var = intValue;
    qDebug() << "Stored integer:" << var.toInt();
    
    var = strValue;
    qDebug() << "Stored string:" << var.toString();
    
    return 0;
}
```

在这个示例中，`QVariant` 用于存储整数和字符串，并且可以通过 `toInt()` 和 `toString()` 方法安全地将其转换为不同的数据类型。

总之，`QVariant` 是 Qt 中用于通用数据类型存储和转换的重要工具，使得处理各种数据类型变得更加灵活和方便。它在 Qt 应用程序的开发中经常用于处理配置数据、用户输入、插件通信等各种场景。

# 参考资料

1、QT:QObject 简单介绍

https://blog.csdn.net/aidem_brown/article/details/80236188

2、

https://doc.qt.io/qt-6/metaobjects.html