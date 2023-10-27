---
title: Linux内核之bin_attribute
date: 2018-04-02 16:30:30
tags:
	- Linux内核

---

--

# bin_attribute和attribute有什么不同？

1、bin_attribute比attribute多了一个size变量来描述文件大小。而普通的attribute文件总是4096字节。就是一个page的大小。

2、bin_attribute多了mmap接口的支持。

在Linux内核中，`bin_attribute`和`attribute`是用于创建sysfs文件的两种不同方法，它们在使用上有一些不同之处。这两种方法都用于在/sys文件系统中创建文件以允许用户空间应用程序读取或写入内核的某些参数或状态信息。

1. **`attribute`**：
   - `attribute`是在`struct attribute`的基础上创建的。`struct attribute`通常包含一个名称和一些操作函数，比如`show`和`store`，它们分别用于读取和写入文件的值。
   - `attribute`需要手动创建sysfs目录结构，并将其与内核对象相关联。这通常需要编写一些额外的代码来设置目录和文件，并将`attribute`对象添加到该目录中。

2. **`bin_attribute`**：
   - `bin_attribute`是在`struct bin_attribute`的基础上创建的。`struct bin_attribute`与`attribute`类似，但它具有一个额外的`size`字段，用于指定文件的大小。
   - `bin_attribute`相对于`attribute`更适用于表示二进制数据，如内核缓冲区或二进制文件。它们通常用于大型数据块，而不仅仅是文本值。

主要不同之处在于数据的类型和用途。`attribute`更适合用于表示文本数据，而`bin_attribute`更适合用于表示二进制数据。选择哪种方法取决于您要在sysfs中公开的数据类型。不过，请注意，随着内核版本的变化，sysfs也在不断演进，因此在具体的内核版本中可能会有不同的用法和最佳实践。