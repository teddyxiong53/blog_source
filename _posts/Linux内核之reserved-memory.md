---
title: Linux内核之reserved-memory
date: 2021-06-21 10:42:33
tags:
	- Linux内核

---

--

一个设备树示例是这样：

```
reserved-memory {
		#address-cells = <2>;
		#size-cells = <2>;
		ranges;
		/* global autoconfigured region for contiguous allocations */
		ramoops@0x07400000 {
			compatible = "ramoops";
			reg = <0x0 0x07400000 0x0 0x00100000>;
			record-size = <0x20000>;
			console-size = <0x40000>;
			ftrace-size = <0x80000>;
			pmsg-size = <0x20000>;
		};
```

在内核里是怎么做的？

对应的数据结构

include/linux/of_reserved_mem.h

```
struct reserved_mem {
	const char			*name;
	unsigned long			fdt_node;
	unsigned long			phandle;
	const struct reserved_mem_ops	*ops;
	phys_addr_t			base;
	phys_addr_t			size;
	void				*priv;
};

struct reserved_mem_ops {
	int	(*device_init)(struct reserved_mem *rmem,
			       struct device *dev);
	void	(*device_release)(struct reserved_mem *rmem,
				  struct device *dev);
};
```



参考资料

1、amlogic相关资料



