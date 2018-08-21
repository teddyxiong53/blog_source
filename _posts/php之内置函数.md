---
title: php之内置函数
date: 2018-08-21 22:10:46
tags:
	- php

---



#empty函数

别用。

# explode函数

把字符串打散为数组。

```
<?php

$str = "hello world";
print_r(explode(" ", $str));
```

结果：

```
Array ( [0] => hello [1] => world ) 
```

# count函数

```
<?php

$e = array("php"=>array("A", "B", "C"),
    "asp"=>array("asp", "java")
);
echo "常规计数：".count($e);
echo "递归计数：".count($e, COUNT_RECURSIVE);
```

结果：

```
常规计数：2递归计数：7
```

# list函数

作用是在一次操作中给多个遍历赋值。

与array类似，list其实并不是函数。而是语言的一部分。

```
$cars = array("audi","bmw", "byd");
list($a,,$c) = $cars;
```



# htmlspecialchars

把一些特殊字符进行转换。

```
<?php

$str = "this is some <b>bold</b> text";
echo htmlspecialchars($str);
```



# isset函数



# implode函数

这个和explode相反，是把数组内容组成字符串。



# exit函数



# is_dir



