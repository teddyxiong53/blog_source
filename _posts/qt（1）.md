---
title: qt（1）
date: 2021-05-31 19:17:11
tags:
	- gui

---

--

# qt的容器类

Qt 库提供了一组通用的基于模板的容器类。这些类可用于存储指定类型的项目。例如，如果您需要可调整大小的 QString 数组，请使用 QList QString 。

这些容器类被设计为比 STL 容器更轻、更安全且更易于使用。如果您不熟悉 STL，或者更喜欢以“Qt 方式”做事，您可以使用这些类而不是 STL 类。

容器类是隐式共享的，它们是可重入的，并且针对速度、低内存消耗和最小内联代码扩展进行了优化，从而产生更小的可执行文件。此外，在所有用于访问它们的线程将它们用作只读容器的情况下，它们是线程安全的。



Qt 提供了以下顺序容器：QList、QStack 和 QQueue。对于大多数应用程序，QList 是最好使用的类型。它提供非常快速的附加。如果您确实需要链表，请使用 std::list。 QStack 和 QQueue 是提供 LIFO 和 FIFO 语义的便利类。

Qt 还提供了这些关联容器：QMap、QMultiMap、QHash、QMultiHash 和 QSet。 “Multi”容器方便地支持与单个键关联的多个值。 “哈希”容器通过使用哈希函数而不是对排序集进行二分搜索来提供更快的查找。

作为特殊情况，QCache 和 QContigouslyCache 类在有限的缓存存储中提供有效的对象哈希查找。

# qt的数据隐式共享

Qt 中的数据隐式共享（Implicit Sharing）是一种用于优化内存和性能的机制，它允许多个对象共享相同的数据，而不需要进行显式的复制。

这个机制是通过 Qt 类的深拷贝实现的，

使得在需要修改数据时才会进行实际的复制，从而减少了内存占用和提高了性能。



以下是关于 Qt 数据隐式共享的主要特点和用法：

1. **共享不可变数据：** 数据隐式共享适用于不可变的数据，即一旦创建，数据就不会被修改。这样的数据可以被多个对象安全地共享，因为没有对象会对数据进行更改。

2. **`QSharedData` 类：** Qt 中的数据隐式共享是通过 `QSharedData` 类实现的。这个类用于存储数据的实际内容，而多个对象可以共享对同一 `QSharedData` 实例的指针。

3. **`QSharedDataPointer` 类：** 在 Qt 中，`QSharedDataPointer` 类用于管理对共享数据的指针。多个 `QSharedDataPointer` 可以指向相同的 `QSharedData` 实例，从而实现数据的隐式共享。

4. **深拷贝：** 当需要修改共享的数据时，Qt 会自动进行深拷贝，即复制数据的内容，以确保修改不会影响其他对象。这个过程是隐式的，开发者无需手动复制数据。

以下是一个简单示例，演示了如何使用 `QSharedDataPointer` 来实现数据的隐式共享：

```cpp
#include <QString>
#include <QSharedDataPointer>

class MySharedData : public QSharedData {
public:
    int value;
    QString text;
};

class MyClass {
public:
    MyClass() : d(new MySharedData) {
        d->value = 42;
        d->text = "Hello, Qt!";
    }

    int getValue() const {
        return d->value;
    }

    QString getText() const {
        return d->text;
    }

private:
    QSharedDataPointer<MySharedData> d;
};

int main() {
    MyClass obj1;
    MyClass obj2 = obj1; // 共享数据

    qDebug() << "Value from obj1:" << obj1.getValue();
    qDebug() << "Value from obj2:" << obj2.getValue();

    // 修改其中一个对象的数据，将会进行深拷贝
    obj2.getText() += " (Modified)";

    qDebug() << "Text from obj1:" << obj1.getText();
    qDebug() << "Text from obj2:" << obj2.getText();

    return 0;
}
```

在这个示例中，`MyClass` 类包含一个 `QSharedDataPointer`，它指向 `MySharedData` 对象，这个对象包含整数和字符串。当我们将一个 `MyClass` 对象赋值给另一个时，它们共享相同的数据，直到其中一个对象尝试修改数据时才会进行深拷贝。

总之，Qt 的数据隐式共享机制允许多个对象共享相同的不可变数据，以减少内存占用和提高性能。这对于处理大型数据结构、字符串等常见情况非常有用，因为它允许多个对象同时访问相同的数据，而不需要复制多份相同的数据。

# qt的资源系统

Qt 资源系统是一种独立于平台的机制，用于在应用程序中传送资源文件。

如果您的应用程序始终需要一组特定的文件（如图标、翻译文件、图像），并且您不想使用特定于系统的方法来打包和定位这些资源，请使用它。

最常见的是，资源文件嵌入到应用程序可执行文件中，或者嵌入到应用程序可执行文件加载的库和插件中。

或者，资源文件也可以存储在外部资源文件中。

该资源系统基于 Qt 的 rcc 资源编译器、构建系统和 Qt 运行时 API 之间的紧密合作。



资源编译器 (rcc) 命令行工具读取资源文件并生成 C++ 或 Python 源文件或 .rcc 文件。

文件和相关元数据的列表以 Qt 资源集合文件的形式传递给 rcc。

默认情况下，rcc 将生成 C++ 源代码，然后将其编译为可执行文件或库的一部分。 -g python 选项会生成 Python 源代码。 -binary 选项生成一个二进制存档，按照惯例，该存档保存在 .rcc 文件中，并且可以在运行时加载。