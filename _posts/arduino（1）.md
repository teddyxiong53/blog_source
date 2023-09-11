---
title: arduino（1）
date: 2023-02-03 16:13:17
tags:
	- arduino

---



# 架构分析

以x-track的ArduinoAPI目录为切入点进行分析。

D:\study\X-TRACK\Software\X-Track\ArduinoAPI

这个是为了使用arduino的相关的开源库而封装的适配层。





arduino ide 1.x版本是java写的。

2.x版本就改成electron的方案了。基于vscode了。

# c++代码分析

## 重载new操作符

```
void *operator new (size_t size)
{
  return malloc(size);
}

void *operator new[](size_t size)
{
  return malloc(size);
}
```

这是C++中的内存分配运算符重载函数，用于在动态内存分配时调用。

当使用`new`关键字分配内存时，会自动调用`operator new`函数进行内存分配，

在这里，`operator new`函数被重载为调用`malloc`函数来分配内存。

同样地，当使用`new[]`关键字分配数组内存时，会自动调用`operator new[]`函数进行内存分配，

在这里，`operator new[]`函数也被重载为调用`malloc`函数来分配内存。

`size`参数表示需要分配的内存大小，函数返回值为指向分配的内存块的指针。

由于`malloc`函数返回的是一个`void*`类型的指针，因此这里`operator new`和`operator new[]`的返回值也是`void*`类型的指针。

这种重载运算符的方式使得内存分配操作可以自定义，从而可以在程序中实现更加灵活、高效的内存管理。

**同时，这种运算符重载也使得C++中的内存分配操作与C语言中的内存分配操作（如`malloc`和`free`）兼容，方便与C语言代码的交互。**

## 虚函数处理

```
extern "C" void __cxa_pure_virtual(void) __attribute__((__noreturn__));
extern "C" void __cxa_deleted_virtual(void) __attribute__((__noreturn__));

void __cxa_pure_virtual(void)
{
  // We might want to write some diagnostics to uart in this case
  //std::terminate();
  while (1)
    ;
}

void __cxa_deleted_virtual(void)
{
  // We might want to write some diagnostics to uart in this case
  //std::terminate();
  while (1)
    ;
}
```

这段代码定义了两个函数`__cxa_pure_virtual`和`__cxa_deleted_virtual`，这两个函数都是C++中的异常处理函数，用于在发生虚函数调用错误时进行处理。

`__cxa_pure_virtual`函数用于处理纯虚函数调用错误，**即在没有实现虚函数的情况下调用该函数。**

该函数的实现是一个死循环，它会一直等待程序中止。

在这个死循环中可以添加一些诊断信息或者其他处理方式，例如向串口打印错误信息，以便在调试时进行分析。

`__cxa_deleted_virtual`函数用于处理已删除的虚函数调用错误，即在已删除的虚函数上调用该函数。

该函数的实现与`__cxa_pure_virtual`函数类似，也是一个死循环，它会一直等待程序中止。

**这两个函数都被声明为`extern "C"`，这是为了告诉编译器这是一个C语言函数，而不是C++语言函数。**

**这是因为C++中的函数名会经过名称重整（name mangling）处理，导致在链接时无法正确地找到函数的符号。**

通过使用`extern "C"`声明，可以避免这个问题，并使得这两个函数可以被其他编程语言（例如C语言）调用。同时，这两个函数也使用了`__attribute__((__noreturn__))`属性，表示它们不会返回任何结果，而是永远阻塞在循环中，以确保程序中止。

这些函数通常由编译器自动生成，用于处理一些C++异常和错误的情况。

**如果用户在程序中显式地声明了一个纯虚函数，但没有对其进行实现，或者将一个已删除的虚函数进行调用，那么就会触发这些异常处理函数的调用。**

在这些处理函数中，可以添加一些额外的处理逻辑，以便在发生异常时进行诊断和调试。

## main函数

```
int main(void)
{
  initVariant();

  setup();

  for (;;) {
#if defined(CORE_CALLBACK)
    CoreCallback();
#endif
    loop();
    serialEventRun();
  }

  return 0;
}
```

# arduino库标志



https://arduino.github.io/arduino-cli/0.34/library-specification/

# 参考资料

1、
https://www.phodal.com/blog/arduino-modular/

2、
http://arduiniana.org/

3、
https://www.arduino.cc/reference/en/