---
title: js之jerryscript
date: 2018-12-27 11:52:27
tags:
	- js
---



直接从这里下载。

https://github.com/jerryscript-project/jerryscript

看readme就够了。

编译：

```
python ./tools/build.py
```

编译很快。

运行：

```
./build/bin/jerryr ./test.js
```

下面的doc目录下，有markdown的文档。

tests目录下，有测试脚本。

基本的是这样的。

```
print("hello jerry");
```



简单看了一下，这个对我来说没有什么吸引力，暂时不关注了。

这样编译，方便用gdb进行调试跟踪代码的运行。

```
python2 tools/build.py --debug  --all-in-one ON --logging ON   --line-info ON --jerry-debugger ON  --jerry-cmdline ON  --jerry-port-default ON 
```

