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



参考资料

1、

