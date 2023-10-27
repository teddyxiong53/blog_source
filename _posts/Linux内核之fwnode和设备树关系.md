---
title: Linux内核之fwnode和设备树关系
date: 2021-02-19 15:35:30
tags:
- Linux
---

--

fwnode是相比于设备树更高一层的抽象。

fwnode，包括了设备树、acpi等硬件配置方式。

fwnode就是of_node，所有的fwnode_函数都是二次封装的of_函数。

所以在驱动中，有的人喜欢有fwnode对设备树进行解析，有的人喜欢用of，功能都是一样的，没必要纠结。

# 关系

`fwnode` 和 `of`（Open Firmware）接口是Linux内核中用于处理设备树（Device Tree）的两种不同方法，它们有一定的关联，但又有不同的用途。

1. **`fwnode`**：
   - `fwnode` 是一种抽象的设备节点表示，它用于在内核中表示设备节点（如PCI设备、ACPI设备、DMI设备等）的属性和关系。它可以表示不同的物理设备并提供一致的方式来访问这些设备的属性。
   - ==`fwnode` 是通用的，不仅仅用于设备树，还用于其他设备描述方法，如ACPI、DMI等。==它提供了一种跨设备描述方法的抽象层。

2. **`of`（Open Firmware）**：
   - `of` 是Linux内核中用于处理设备树的子系统。设备树是一种描述硬件平台和设备的数据结构，通常用于嵌入式系统。`of` 子系统处理设备树的解析、访问和与设备的关联。
   - `of` 子系统通常用于处理基于设备树的平台，如ARM架构中的大多数系统。

关系：
- 在Linux内核中，`fwnode` 提供了一个通用的抽象层，可以用于访问不同类型的设备节点和属性，包括设备树节点。
- `of` 子系统通常使用 `fwnode` 抽象来表示设备树节点。这使得Linux内核能够使用通用的方式来访问不同类型的设备树节点，而不必依赖于特定于设备树的接口。

总之，`fwnode` 和 `of` 是Linux内核中用于设备节点和属性管理的两个关联但不同的概念。`fwnode` 提供了通用的抽象，而 `of` 子系统通常使用 `fwnode` 来表示设备树节点。这使得Linux内核能够更灵活地处理不同类型的设备描述方法，而不限于设备树。

# fwnode的常用接口函数

`fwnode` 是Linux内核中的一个抽象层，用于表示设备节点和属性，

以便跨不同的设备描述方法（如设备树、ACPI、DMI等）提供一致的访问接口。

以下是一些常用的`fwnode`接口函数：

1. **`fwnode_handle`**:
   - `struct fwnode_handle *fwnode_handle_get(dev)`：获取给定设备的 `fwnode` 句柄。通常，`dev` 是一个 `struct device` 结构，表示内核中的设备。
   - `void fwnode_handle_put(struct fwnode_handle *fwnode)`：释放 `fwnode` 句柄。

2. **属性读取和写入**:
   - `int fwnode_property_read_u32(struct fwnode_handle *fwnode, const char *propname, u32 *val)`：从 `fwnode` 中读取一个32位整数属性。
   - `int fwnode_property_read_string(struct fwnode_handle *fwnode, const char *propname, const char **str)`：从 `fwnode` 中读取一个字符串属性。
   - `int fwnode_property_write_u32(struct fwnode_handle *fwnode, const char *propname, u32 val)`：将一个32位整数写入 `fwnode` 的属性。
   - `int fwnode_property_write_string(struct fwnode_handle *fwnode, const char *propname, const char *str)`：将一个字符串写入 `fwnode` 的属性。

3. **属性遍历**:
   - `int fwnode_property_count_strings(const struct fwnode_handle *fwnode, const char *propname)`：获取字符串数组属性的元素数量。
   - `int fwnode_property_read_string_index(const struct fwnode_handle *fwnode, const char *propname, int index, const char **str)`：按索引读取字符串数组属性的元素。

4. **`fwnode` 关系**:
   - `struct fwnode_handle *fwnode_get_parent(const struct fwnode_handle *fwnode)`：获取给定 `fwnode` 的父节点。
   - `struct fwnode_handle *fwnode_get_next_child(const struct fwnode_handle *fwnode, struct fwnode_handle *previous)`：获取给定 `fwnode` 的下一个子节点。

5. **其他**:
   - `bool fwnode_property_present(const struct fwnode_handle *fwnode, const char *propname)`：检查指定属性是否存在。
   - `struct fwnode_handle *fwnode_reference(const struct fwnode_handle *fwnode)`：获取 `fwnode` 引用计数。

这些函数允许开发人员在不同的设备描述方法之间以一致的方式操作设备节点和属性。

具体的用法和函数参数可能会因不同的设备描述方法而有所不同，

所以需要查看相关的文档和内核源代码来获取更多细节。

# of常用接口函数

在Linux内核中，设备树（Device Tree）是一种常见的硬件描述方法，Open Firmware（OF）子系统用于解析和处理设备树。以下是一些常用的`of`接口函数：

1. **设备节点查找**：
   - `struct device_node *of_find_node_by_name(struct device_node *from, const char *name)`：根据节点名称在设备树中查找节点。
   - `struct device_node *of_find_node_by_phandle(phandle phandle)`：根据phandle查找节点。
   - `struct device_node *of_find_compatible_node(struct device_node *from, const char *type, const char *compat)`：查找具有给定类型和兼容性字符串的节点。

2. **属性读取**：
   - `int of_property_read_u32(const struct device_node *np, const char *propname, u32 *out_value)`：读取一个32位整数属性。
   - `int of_property_read_string(const struct device_node *np, const char *propname, const char **out_string)`：读取一个字符串属性。
   - `int of_property_read_string_array(const struct device_node *np, const char *propname, const char **out_strings, int array_size)`：读取字符串数组属性。

3. **设备树遍历**：
   - `struct device_node *of_get_next_parent(const struct device_node *node)`：获取给定节点的下一个父节点。
   - `struct device_node *of_get_next_child(const struct device_node *node, struct device_node *previous)`：获取给定节点的下一个子节点。
   - `struct device_node *of_get_next_available_child(const struct device_node *node, struct device_node *previous)`：获取给定节点的下一个可用子节点。
   
4. **属性存在性检查**：
   - `int of_property_read_bool(const struct device_node *np, const char *propname)`：检查指定属性是否存在并返回布尔值。
   
5. **中断控制**：
   - `int of_irq_init(struct device_node *device)`：初始化与设备关联的中断控制器。
   - `int of_irq_to_resource(struct device_node *device, int index, struct resource *rsrc)`：获取中断资源信息。

6. **OF平台总线**：
   - `int of_platform_populate(struct device_node *root, const struct of_device_id *matches, const struct of_dev_auxdata *lookup, struct device *parent)`：注册设备并连接设备到OF平台总线。

这些函数允许开发人员在设备树中查找节点、读取属性、遍历设备树结构以及执行其他与设备树相关的操作。具体的使用取决于您的驱动程序或子系统需求。这些函数的参数和返回值可能因不同的内核版本而有所不同，所以请查看相关的内核文档和源代码以获取更多信息。

# 参考资料

1、Linux fwnode和device_node的区别

https://blog.csdn.net/qq_40937426/article/details/107706460