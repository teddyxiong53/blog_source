---
title: qt之Q_GADGET
date: 2021-06-10 14:20:11
tags:
	- qt

---

--

对于那些没有继承自QObject但却想拥有反射能力的类型，Q_GADGET是Q_OBJECT的轻量化版本。

和Q_OBJECT一样，Q_GADGET也必须出现在类定义的私有区域。

有Q_GADGET时，可以有Q_ENUM, Q_PROPERTY 和Q_INVOKABLE，但不能有signals和slots。

Q_GADGET使类成员staticMetaObject可用。



`Q_GADGET` 宏是 Qt 框架中用于声明纯数据类型的一种宏。它通常用于定义没有信号槽、继承关系和 QObject 特性的类，这些类只包含数据成员和相关的方法。`Q_GADGET` 宏允许这些类在 Qt 的元对象系统中注册为可识别的类型。

以下是关于 `Q_GADGET` 宏的详细信息：

1. **用途：** `Q_GADGET` 宏用于声明一个纯数据类型，这个类型不需要 QObject 的功能，如信号槽和动态属性。通常，这些类型用于表示纯粹的数据结构，如配置信息、消息结构等。

2. **元对象系统：** 尽管 `Q_GADGET` 类不继承自 QObject，但它们仍然可以在 Qt 的元对象系统中注册，以便在运行时能够通过字符串名称访问它们的成员。

3. **成员变量：** `Q_GADGET` 类可以包含成员变量，这些变量可以是基本数据类型、自定义数据类型或 Qt 类的实例。这些变量通常用于存储数据，而不涉及行为。

4. **成员函数：** `Q_GADGET` 类可以包含成员函数，这些函数可以用于操作成员变量或提供一些辅助功能，但它们通常不包含信号和槽。

以下是一个简单的示例，演示如何使用 `Q_GADGET` 宏声明一个纯数据类型：

```cpp
#include <QMetaEnum>

// 使用 Q_GADGET 宏声明 MyData 类
class MyData {
    Q_GADGET
public:
    enum DataType {
        Integer,
        String
    };
    Q_ENUM(DataType) // 声明枚举类型
    int intValue;
    QString stringValue;
};

int main() {
    // 通过 Qt 的元对象系统访问枚举类型
    QMetaEnum metaEnum = QMetaEnum::fromType<MyData::DataType>();
    qDebug() << "Enum Integer value:" << metaEnum.valueToKey(MyData::Integer);

    return 0;
}
```

在这个示例中，`MyData` 类使用 `Q_GADGET` 宏声明为一个纯数据类型，它包含了一个枚举类型和一些成员变量。通过 `Q_ENUM` 宏，枚举类型也可以在运行时通过字符串名称访问。

总之，`Q_GADGET` 宏用于声明纯数据类型，这些类型可以在 Qt 中的元对象系统中注册为可识别的类型，但它们不具备 QObject 的功能。这在处理纯粹的数据结构时非常有用，例如配置、枚举、消息等。

# 参考资料

1、

https://blog.csdn.net/qq_43248127/article/details/101635247