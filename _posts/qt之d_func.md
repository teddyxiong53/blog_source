---
title: qt之d_func
date: 2021-07-09 10:15:33
tags:
	- qt

---

--

从这个代码：

```
void QWizardPage::setTitle(const QString &title)
{
    Q_D(QWizardPage);
    d->title = title;
    if (d->wizard && d->wizard->currentPage() == this)
        d->wizard->d_func()->updateLayout();
}
```

Q_D是这样一个宏：

```
#define Q_D(Class) Class##Private * const d = d_func()
```

那么上面的语句展开就是：QWizardPagePrivate *const d = d_func()

d_func() 这个函数又在哪里定义？代表了什么含义呢？

就在Q_D这个宏上面几行，都是在qglobal.h里。

```
#define Q_DECLARE_PRIVATE(Class) \
    inline Class##Private* d_func() \
    { Q_CAST_IGNORE_ALIGN(return reinterpret_cast<Class##Private *>(qGetPtrHelper(d_ptr));) } \
    inline const Class##Private* d_func() const \
    { Q_CAST_IGNORE_ALIGN(return reinterpret_cast<const Class##Private *>(qGetPtrHelper(d_ptr));) } \
    friend class Class##Private;
```

d_func本质上是把d_ptr这个指针进行一个cast操作。

d_ptr又是在哪里呢？

它可以把一个类库的实施细节对使用的用户隐藏， 而且对实施的更改不会打破二进制兼容。

在设计像 Qt 这样的类库的时候，

理想的行为应该是动态连接到 Qt 的应用程序，

甚至在 Qt 类库升级或者替换到另外一个版本的时候，

不需要重新编译就可以继续运行。

例如，你的应用程序 CuteApp 是基于 Qt 4.5 的，你应该可以把你的 Qt 由4.5升级到 Qt 4.6 （在 Windows 下用安装程序，在 Linux 下通常有包管理器自动完成），而你用 Qt 4.5 构建的 CuteApp 应该还可以运行。



这里不全都是和二进制兼容有关。d-pointer 还有其它的好处： **隐藏了实现细节 - 我们可以只发布带有头文件和二进制文件的 WidgetLib。源文件可以是闭源代码的。**

- 头文件很干净，不包含实现细节，可以直接作为 API 参考。
- 由于实施需要的包含的头文件从头文件里已到了实施（源文件）里面，编译速更快。（译：降低了编译依赖）

事实上，上边的好处是微乎其微的。Qt 使用 d-pointer 的真正原因是为了二进制兼容和 Qt 最初是封闭源代码的.（译：Qt 好像没有封闭源代码）



到目前为止，我们仅仅看到的是作为 C 风格的数据机构的 d-pointer。

实际上，它可以包含私有的方法（辅助函数）。

例如，`LabelPrivate` 可以有一个`getLinkTargetFromPoint()` 辅助函数，当鼠标点击的时候找到目标链接。

在很多情况下，这些辅助函数需要访问公有类，也就是 Label 或者它的父类 Widget 的一些函数。

比如，一个辅助函数 `setTextAndUpdateWidget()` 想要调用一个安排重画Widget的公有方法 `Widget::update()`。

所以，`WidgetPrivate` 存储了一个指向公有类的指针，称为q-pointer。

修改上边的代码引入q-pointer，我们得到下面代码：



在 Qt 中，几乎所有的公有类都使用了 d-pointer。

唯一不用的情况是如果事先知道某个类永远不会添加额外的成员变量。

例如，像 `QPoint`, `QRect` 这些类，我们不期望有新的成员添加，

因此它们的数据成员直接保存在类里而没用 d-pointer。



```
QObjectData
QObjectPrivate
```







参考资料

1、c++ - 为什么Qt使用d_func()实例化指向私有(private)数据的指针？

https://www.coder.work/article/575112

2、

https://wiki.qt.io/D-Pointer/zh