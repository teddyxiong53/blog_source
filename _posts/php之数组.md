---
title: php之数组
date: 2018-08-21 22:27:11
tags:
	- php

---





php里，有3种数组类型。

1、索引数组。带有数字索引的数组。

2、关联数组。带有指定键的数组。

3、多维数组。



#索引数组

```
$cars = arrary("bwm", "audi");
```

也可以这样。

```
$cars[1] = "bwm";
$cars[2] = "audi";
```



获得数组的长度。

```
echo count($cars);
```

遍历的方法：

```
$cars = array("bwm", "audi");
$arr_len = count($cars);
for($x=0; $x< $arr_len; $x++) {
  echo $cars[$x];
}
```



# 关联数组

```
$ages = array("allen"=>"10", "bob"=>"11");
```

或者：

```
$ages["allen"] = "10";
$ages["bob"] = "11";
```

遍历的方法：

```
$ages = array("allen"=>"10", "bob"=>"11");
foreach($ages as $x=>$x_value) {
  echo "key=".$x.","."value=".$x_value;
}
```

