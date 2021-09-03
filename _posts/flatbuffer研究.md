---
title: flatbuffer研究
date: 2021-08-30 10:58:33
tags:
	- npu

---

--

tflite-micro用到了flatbuffer。了解一下。

flatbuffer是一个protobuf的替代品。



在内存空间占用这个指标上，FlatBuffers占用的内存空间比protobuf多了两倍。

序列化时二者的cpu计算时间FB比PB快了3000ms左右，

反序列化时二者的cpu计算时间FB比PB快了9000ms左右。

**FB在计算时间上占优势，**

而PB则在内存空间上占优（相比FB，这也正是它计算时间比较慢的原因）。



内存占用多实际上就是代表传输时间较长。

因此FB的编解码比较快，而PB的传输比较快。

从这个角度来说，总数据量小，但结构复杂的数据类型使用FB时应该会比较快；

而总数据量大，结构单一的数据，则PB可能会比较快。



flatbuffer是google发布的一个跨平台序列化框架具有如下特点

1、对序列化的数据不需要打包和拆包

2、内存和效率速度高，扩展灵活

3、代码依赖较少

4、强类型设计，编译期即可完成类型检查

5、使用简单、可跨平台使用



参考资料

1、

https://www.cnblogs.com/frankwt/p/12943924.html