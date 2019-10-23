---
title: Linux之pushd和popd
date: 2019-10-23 11:38:49
tags:
	- Linux

---

1

pushd和popd，在有些脚本里看到用，但是我一直没有用过。了解一下。

是对一个目录栈进行操作。

另外还有一个配套的命令，dirs。

dirs就是查看目录栈的内容。

我创建一个这样的目录结构，供测试使用。

```
hlxiong@hlxiong-VirtualBox:~/work/test/pushd$ mkdir 1 2 3 
hlxiong@hlxiong-VirtualBox:~/work/test/pushd$ ls
1  2  3
```

用pushd进入到目录1

```
hlxiong@hlxiong-VirtualBox:~/work/test/pushd$ pushd ./1
~/work/test/pushd/1 ~/work/test/pushd
```

执行完pushd之后，会自动打印出当前的目录栈的内容。

然后就可以popd进行返回。

如果目录栈里没有内容了，就会打印这个：

```
hlxiong@hlxiong-VirtualBox:~/work/test/pushd/1$ popd
~/work/test/pushd
hlxiong@hlxiong-VirtualBox:~/work/test/pushd$ popd
-bash: popd: 目录栈为空
```

pushd用法：

```
实现cd -类似效果。
pushd /
pushd 
相当于
cd /
cd -
```



参考资料

1、

