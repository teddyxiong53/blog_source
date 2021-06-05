---
title: shell（1）
date: 2021-05-30 09:24:11
tags:
	- shell

---

--

打算重新梳理一下shell的知识。

# 数值运算

包括：

1、基本预算，加减乘除、求模、求幂。

2、产生指定范围的随机数。

3、产生指定范围的数列。

shell本身可以做整数运算，复杂一些的运算要通过外部命令来实现。

例如bc、expr、awk。

RANDOM这个环境变量可以产生一个0到32767 的随机数。

外部命令，例如awk，有rand函数来产生随机数。

seq命令用来产生一个数列。

## 整数运算

对一个数加1

```
i=0
#方法1
((i++)) 
#方法2
let i++
#方法3，这里$i这些空格是必须要有的。
expr $i + 1
#方法4
echo $i 1 | awk '{printf $1+$2}'
#方法5
i=$(echo $i+1|bc)
```

从1加到某个数

```
i=0
while [ $i -lt 10 ]; do
	((i++))
done
```

上面这些方法的效率，shell内置的是最高的。

也就是(())效率最高。其次是let。其余的都比较慢。

shell本身不能完成浮点运算，这个就需要借助外部工具。

## 求模

let、expr、bc都可以求模。符号都是%

```
expr 5 % 2

let i=5%/2

echo 5%/2 | bc

((i=5%2))
```

## 求幂

(())、bc、let都可以求幂。bc的符号不同，是^

```
let i=5**2
((i=5**2))

echo "5^2"|bc
```

## 进制转换

(())和bc都可以。

(())比bc更加简洁。

下面是把8进制转成十进制的。

```
echo "obase=10;ibase=8;11"| bc -l

echo $((8#11))
```

不过bc适用范围更广。可以用于任意进制的转换。

## 浮点运算

bc和awk可以。

```
#1除以13，保留3位小数。
echo "scale=3; 1/13" | bc
```

## 产生数列

```
seq 5
seq 1 5
seq 1 2 5
seq -w 1 2 14
seq -s: -w 1 2 14
seq -f "0x%g" 1 5
```

## 综合示例

统计一篇文章里的每个单词出现的次数。

```
wget -c http://tinylab.org
cat index.html | sed -e "s/[^a-zA-Z]/\n/g" \
| grep -V ^$ | sort | uniq -c 
```

# 布尔运算

shell里有2个命令，true和false。

与或非：&& || ！

# 字符串运算

对字符串的操作包括：

1、判断字符的类型，是字母还是数字，是否可打印。

2、求子串、插入字符、删除字符、替换字符、比较。

3、复杂操作。

## 字符串的属性

### 类型

字符可能是数字、字母，空格、特殊字符。

字符串则是字符串的任意组合。

组合后，可能构成特殊意义的字符串。例如邮箱地址、url。

判断字符的组合类型

```
#判断是否都是字母。
echo $aa | grep -q "^[a-zA-Z]\+$"
#判断是否是字母和数字的组合
$echo $aa |grep -q "^[0-9a-zA-Z]\+$"
```

判断是不是空白字符

```
echo $aa | grep "[[:space:]]"
```

匹配邮件地址

```
echo "1073167306@qq.com" | grep "[0-9a-zA-Z\.]*@[0-9a-zA-Z\.]"
```

判断字符是否可以打印

```
echo "\t\n" |grep "[[:print:]]"
```

## 求字符串长度

有好几种，看着用吧。

```
var="get the length of me"
echo ${#var}
expr length "$var"
echo -n $var | wc -c
```



## 字符串颜色

```
red='\e[0;41m' # 红色  反显的效果。
RED='\e[1;31m'
NC='\e[0m' # 没有颜色
echo -e "${red}显示红色0 ${NC}"
echo -e "${RED}显示红色1 ${NC}"   
```



https://blog.csdn.net/taotaost/article/details/41927547



## 把字符串拆分成数组

```
var="get the length of me"
var_arr=($var) #这样就完成了拆分了。
echo ${var_arr[@]} #@可以用*替换。
echo ${#var_arr[@]} #数组元素个数。
```

对于字符串数字，可以用for in进行遍历。

```
for item in var_arr; do
	echo $item
done
```

## 字符串常规操作

### 求取子串

按位置来取

```
var="get the length of me"
echo ${var:0:3}
#得到的是get这个单词。
```

也可以用expr来求取

```
echo `expr substr "$var" 0 3`
```

awk也可以。

### 子串替换

把所有空格替换为_

```
echo ${var// /_}
```

awk也可以。

sed也可以。而且是sed的专长。

tr也可以替换单个字符。



# 参考资料

1、

https://www.w3cschool.cn/shellbook/et3s9ozt.html