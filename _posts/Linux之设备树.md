---
title: Linux之设备树
date: 2018-01-19 15:47:07
tags:
	- Linux 

---



# 设备树之由来

1、linux的设备树是从Open FirmWare的设备树移植过来的。

2、使用dts源文件和dtsi头文件来表示设备树。都会被编译为dtb二进制文件。

linux3.x开始引入。

在设备树出现之前，所有关于设备的具体信息都写在驱动里。一旦外围设备发生变化。那么驱动代码就要重写。

一个soc对应多个machine。如果每个machine都写一个完全独立的dts，那么就有很多的重复部分。

于是就把公共部分提取为dtsi。



#设备树的意义

##对于soc厂家

减少arch/arm/mach-*这种目录的存在。把精力放在驱动的开发上。

## 对于主板设计者

1、努力减少所需要的端口。

2、不需要为每种板子申请一个机器ID了。用设备树的命名空间来替代。

## 对于嵌入式linux生态系统

1、需要合入的bsp代码更少了。

# 设备树语法

我们先以dm9000的驱动的为例，来进行分析。

对应的文档在Documentation/devicetree/bindings/net/davicom-dm9000.txt。

一个设备树的基本框架是这样的。一般`/`表示的就是板子。

```
/{
	node1{
		key=value;
		...
		node2{
			key=value;
		}
	}
	node3{
		key=value;
	}
}
```

1、每个设备都有一个根节点。每个设备都是一个节点。节点名长度不超过31个字符。

2、节点可以嵌套，形成父子关系。

3、每个设备属性都用一组键值对来描述。

4、属性用分号结尾。

5、`#`不是注释。

##节点

节点名一般写出这个格式：

```
name@0xaaaabbbb
```

另外，还有几个特殊的节点，并不对应真正的设备。而是一些传递给os的参数。例如：

```
chosen {
  bootargs="console=ttySAC2,115200";
  
}
```

##引用

当我们找一个节点的时候，我们必须书写完整的节点路径，这样当一个节点嵌套比较深的时候，就不方便了。所以设备树运行我们给节点起别名。可以实现类似函数调用的效果。

在编译设备树的时候，相同节点的不同属性信息会被合并，相同属性会被覆盖。

有了引用，我们就不用到处去找节点了。直接在板级的dts里写就行了。

```
/ {
  ...
}
&uart0 { 这里就是一个引用，注意位置，在根节点外。
  status = "okay";
}
```



# key

节点的属性是键值对。

我们看key有哪些可用的。

linux定义了这些规范属性：

1、compatible。

2、address。

3、interrupt。

###先看compatible。

dts里是这样的写：

```
	ethernet@18000000 {
		compatible = "davicom,dm9000";
		reg = <0xA8000000 0x2 0xA8000002 0x2>;
		interrupt-parent = <&gph1>;
		interrupts = <1 4>;
		local-mac-address = [00 00 de ad be ef];
		davicom,no-eeprom;
	};
```

而在drivers/net/ethernet/davicom/dm9000.c里是这样的：

```
#ifdef CONFIG_OF
static const struct of_device_id dm9000_of_matches[] = {
	{ .compatible = "davicom,dm9000", },
	{ /* sentinel */ }
};
MODULE_DEVICE_TABLE(of, dm9000_of_matches);
#endif
```

OF代表的就是OpenFirmware。就是设备树了。

###再看address的。

没有太明白，先空着。

### interrupts

计算机系统里的大量设备都是通过中断来请求CPU服务的，所以设备节点中就要指定中断号。

常用的属性有：

1、interrupt-controller。这属性没有value。声明性质的。

2、`#interrupt-cells`。表示这中断控制器需要几个单位做中断描述符。