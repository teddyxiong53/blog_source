---
title: shell之实用命令
date: 2018-02-01 10:53:02
tags:
	- shell

---

### 找出当前目录下最占用空间的子目录

```
du -h --max-depth=1 ./
```

### 同时查找多种文件

```
find -name "Makefile" \
-o -name "*.mk" \
-o -name "*.sh" \
| xargs grep -nwr "generic\-package"
```

### 排除几种文件

```
find -type f ! -name "*.c" \
-type f ! -name "*.h" \
-type f ! -name "*.cmd" \
-type f ! -name "*.java" \
 | xargs grep -nwr "PLATFORM_VERSION_CODENAME"
```

### 查找拷贝

```
find -name "*.so" -exec cp {} ./dst_dir \;
```

## stdout和stderr都重定向

```
xxx > /dev/null 2>&1
```

## 包含其他公共文件

要实现模块化编程，就需要把公共函数放在一起。

common.sh里。

```
#!/bin/sh

function mytest()
{
	echo "mytest func"
}
```

test.sh里。

```
#!/bin/sh

source ./common.sh

mytest
```



## shell里进行数学运算

```
let a="2*3"
echo $a
```

数值比较

```
"1" -lt "2"
```

```
 size_list="00400000
 00200000
 00100000
 00d00000
 00c00000
 05a00000
 17a00000"
 for sz in $size_list; do
 	sz1=`echo $((16#${sz}))`
 	flash_size=`expr $flash_size + $sz1`
 done
```

```
size_list="00400000
00200000
00100000
00d00000
00c00000
05a00000
17a00000"
for sz in $size_list; do
	sz="0x"${sz}
	sz=`printf "%d" $sz`
	flash_size=`expr $flash_size + $sz`
done
echo "FLASH:["$flash_size"],"
```



查看cpu的频率和修改。

https://blog.csdn.net/zhangyongfeiyong/article/details/52923563



## 去掉空格

```
function trim() 
{ 
	echo $1 |  awk 'gsub(/^ *| *$/,"")'
}
```

## 逐行读取文件

有两种方式：

方式一：

```
cat 1.txt | while read line
do
	echo $line
done
```

方式二：

```
while read line
do 
	echo $line
done < 1.txt
```

今天碰到一个坑，就是比较复杂的一个行。

一行数据是这样的，那么上面的方法工作不正常。

```
30 6,8,12,22 * * * node /scripts/jd_immortal.js >> /scripts/logs/jd_immortal.log 2>&1
```

需要在前面加上这样一行：

```
IFS=$'\n'       # make newlines the only separator
```



## 文件名处理

```
fullfile=$1

filename_with_postfix=$(basename "$fullfile")
extension="${filename_with_postfix##*.}"
filename="${filename_with_postfix%.*}"

echo $filename_with_postfix
echo $extension
echo $filename
```

## 定义字符串数组

```
#!/bin/sh

str_arr=("aa" "bb" "cc" \
	"dd"\
	)

str_arr_len=${#str_arr[@]}

i=0
while [[ $i -lt $str_arr_len ]]
do
	let i++
done
echo $i

```

## 命令行查看自己的公网ip

```
curl http://members.3322.org/dyndns/getip
```

## 获取当前音量的数字

```
amixer get Master Playback |grep % |grep Left | awk '{print $5}' | tr -cd "0-9"
```

## 函数返回值

return int部分----shell函数可以有返回值，但只能返回整数不能返回字符串

要得到字符串，一般通过全局变量的方式来得到。



## 用lsof查看端口是否被占用

lsof -i:2335

这样就可以查看2335端口是否被使用。如果没有使用，返回空 的，否则返回有内容。



参考资料

Linux Shell函数定义与调用

<https://www.cnblogs.com/lsdb/p/10148177.html>