---
title: Linux之lighttpd
date: 2019-09-21 10:40:48
tags:
	- Linux

---

1

现在是在嵌入式板端使用lighttpd，做测试通道。

碰到一个问题，执行cgi脚本。浏览器总是弹出下载窗口。

```
lighttpd is working correctly. Your browser is prompting you to save a file since the response from the python code did not contain a Content-Type response header indicating the content type (e.g. text/html or text/plain)
```

index.sh的最前面加上这句就好了。

```
echo  "Content-type:text/html\r\n\r\n"
```

这个其实还是不正常，下面这样才是正常的。

```
echo  "Content-type:text/html"
echo ""
```



执行脚本进行录音是不行的，那么就只好曲线救国了。

touch一个文件作为标志。这个文件只能在cgi-bin目录下，其他目录都不行。

最后录音完成后，要把这个标志文件删除掉。



shell获取参数。

```
username=`param username`
```

这个可以拿到。

```
echo $QUERY_STRING
```

解析这个字符串的方法，这篇文章讲得好。

https://stackoverflow.com/questions/3919755/how-to-parse-query-string-from-a-bash-cgi-script

这篇文章更加完整。

http://biancheng.dnbcw.net/linux/420142.html

下面这个代码是可行的。

```
LINE=`echo $QUERY_STRING | sed 's/&/ /g'`
for LOOP in $LINE
do
    NAME=`echo $LOOP | sed 's/=/ /g' | awk '{print $1}'`
    TYPE=`echo $LOOP | sed 's/=/ /g' | awk '{print $2}' | sed -e 's/%\(\)/\\\x/g' | sed 's/+/ /g'`
    printf "${NAME}=${TYPE}\n"
    VARS=`printf "${NAME}=${TYPE}\n"`
    #echo $VARS
    eval `printf $VARS`
done

```



# 配置语法

```
name = value #直接赋值
name += value #追加赋值
name := value #替换赋值
name的命名风格：modulename.key，可以用点号来表示层次。
value的可能取值："text" | 1 | "enable" 。
还可以是数组。
数组是这样定义的：
arr1 = ("key1"=>"val1", "key2"=>"val2")
arr2 = ("val3", "val4")
include "cgi.conf"
include_shell "ls /xx"
```



lighttpd是一个单线程的server。

它的主要资源限制就是max fd。默认是1024 。



代码入口文件是server.c。



当前我使用cgi方式，非常简单。看看正式的使用是怎么用的。

modules.conf里

```
"mod_access", //基础模块
"mod_alias", //路径绑定 用来指定CGI路径
这里不能打开mod_cgi。（事实上也没有写出了）。
如果这里加了mod_cgi，会跟后面的include cgi.conf冲突的。
```



参考资料

1、配置语法

https://redmine.lighttpd.net/projects/lighttpd/wiki/Docs_Configuration

2、Lighttpd1.4.20源码分析 笔记 网络服务主模型

https://blog.csdn.net/jiange_zh/article/details/50483099

3、

https://blog.csdn.net/iGrey_/article/details/88265572