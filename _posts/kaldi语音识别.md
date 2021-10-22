---
title: kaldi语音识别
date: 2021-10-18 17:07:33
tags:
	- 语音

---

--

深入对我来说没有必要。

我把基本环境搭建了解一下即可。

下载代码：

```
git clone https://github.com/kaldi-asr/kaldi.git kaldi-trunk --origin golden
```

看看依赖是否都安装了：

```
cd kaldi-trunk/tools/extras/
./check_dependencies.sh
```

根据提示把缺失的软件安装上。

这个做得还是很好的。



在进行编译之前，首先提醒以下，如果是在虚拟机里运行，应该给虚拟机分配足够大的硬盘空间以及内存，一般分配内存为8g，硬盘为55g或者更高为好，因为在后期的使用中，内存太小，就会出现莫名其妙的错误，而kaldi在编译完之后，占用的磁盘空间也比较大，因此硬盘需要分配足够大小。



采用cmake来组织编译的。

使用了c++14的标准。

里面各种bash、perl脚本比较多。



参考资料

1、

https://blog.csdn.net/qq_34049877/article/details/108809651