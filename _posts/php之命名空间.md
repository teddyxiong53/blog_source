---
title: php之命名空间
date: 2018-08-18 19:02:21
tags:
	- php

---



命名空间是从php5.3版本开始引入的。

主要是为了解决这2类问题：

1、名字冲突。

2、创建简短的别名，方便引用。



# 定义命名空间

使用关键字namespace。

```
namespace MyProject;
const CONNECT_OK = 1;
//...
```

不过，一般推荐用大括号括起来。

```
namespace MyProject {
  const CONNECT_OK = 1;
  
}
```

全局的内容，就把namespace后面不跟内容就好了。

```
namespace {
  //这是全局的。
}
```

# 子命名空间

就是层级关系。用反斜杠。

```
namespace MyProject\Sub\Level;
```



# 别名

这个是为了写代码的时候方便。

```
use My\Full\Name as full;
```



# 参考资料

1、

http://www.runoob.com/php/php-namespace.html