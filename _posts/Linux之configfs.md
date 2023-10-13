---
title: Linux之configfs
date: 2020-03-25 13:31:11
tags:
	- Linux

---

--

# 简介

看rk3308的启动脚本，S50usbdevice。里面的内容：

```
mount -t configfs none /sys/kernel/config
```

configfs的作用是：在用户空间配置内核对象。

## configfs vs ioctl

configfs可以直接查看。适用于内核对象很复杂的配置。

## configfs vs sysfs

**configfs可以在用户态创建和删除内核对象。**



## 什么时候可以使用configfs？

1、配置项很多的时候。

2、**需要动态创建内核对象。**

3、不想写ioctl，直接用脚本就可以配置。



configfs默认挂载在/sys/kernel/config目录。

# gpt回复

`configfs` 是 Linux 内核中的一个文件系统，

用于动态配置内核对象和子系统。

它允许用户空间应用程序和内核模块通过文件系统接口进行配置，

创建、管理和删除内核对象，

从而改变内核行为，

而无需重新编译内核或重新启动系统。

==`configfs` 的主要用途是支持内核中的配置管理，==

==如配置 USB 设备、网络设备、块设备等。==

以下是一些关于 `configfs` 的关键特点和信息：

1. **动态配置**：`configfs` 允许用户动态配置内核对象，而无需修改内核源代码或重新编译内核。这对于实现模块化、可配置的内核非常有用。

2. **对象层次结构**：`configfs` 中的配置对象是一个层次结构，可以有父对象和子对象。这些对象以文件和目录的形式在 `/config` 目录中表示。

3. **用户空间接口**：`configfs` 提供了用户空间与内核之间的接口，用户可以使用标准文件操作（例如读取和写入文件）来配置和管理内核对象。

4. **系统目录**：`configfs` 的主目录是 `/config`，内核对象和子系统都在这个目录下组织。用户可以在这个目录中创建、删除和管理对象。

5. **应用领域**：`configfs` 在多个领域中得到应用，包括 USB 子系统、网络子系统、块设备子系统等。例如，在 USB 子系统中，`configfs` 允许用户动态配置 USB 设备和驱动程序的关系，而不需要手动修改配置文件。

6. **内核模块**：`configfs` 需要内核模块的支持，因此你需要确保内核已启用 `CONFIG_CONFIGFS_FS` 选项。

虽然 `configfs` 是一个功能强大的工具，

==但它相对复杂，通常用于高级配置和系统管理任务。==

在一些情况下，更简单的工具和方法（如 sysfs）可能更适合处理配置需求。

如果你要使用 `configfs`，建议查阅相关文档和资源，以更好地理解如何配置内核对象。

# configfs使用举例

以下是一个简单的示例，演示如何使用 `configfs` 创建和配置一个内核对象。

在这个示例中，我们将创建一个名为 "myconfig" 的内核对象，然后配置它的属性。

请注意，`configfs` 通常用于更复杂的配置任务，

这里提供的示例是为了说明基本用法。

1. 加载 `configfs` 内核模块（如果尚未加载）：

   ```bash
   sudo modprobe configfs
   ```

2. 创建 `configfs` 根目录，通常会在 `/sys/kernel/config` 下创建一个子目录：

   ```bash
   sudo mkdir /sys/kernel/config/myconfig
   ```

3. 在 `myconfig` 目录中创建一个属性文件，例如 `my_property`：

   ```bash
   sudo touch /sys/kernel/config/myconfig/my_property
   ```

4. 使用文本编辑器或 `echo` 命令来设置属性的值，例如：

   ```bash
   echo "Hello, configfs!" | sudo tee /sys/kernel/config/myconfig/my_property
   ```

5. 检查配置的属性值：

   ```bash
   cat /sys/kernel/config/myconfig/my_property
   ```

   这将输出 "Hello, configfs!"。
   
   

这个示例中，我们创建了一个 `myconfig` 内核对象，

并在其内部创建了一个属性文件 `my_property`。

然后，我们将属性设置为 "Hello, configfs!"，并最后查看属性的值。





# 参考资料

1、linux之configfs简介和编程入门

https://blog.csdn.net/u014135607/article/details/79949571

2、

https://blog.csdn.net/t1506376703/article/details/109381212