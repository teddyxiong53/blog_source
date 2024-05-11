---
title: Linux之lighttpd
date: 2019-09-21 10:40:48
tags:
	- Linux

---

--

# 简介

Lighttpd（也称为“轻量级HTTP服务器”）是一个开源的、轻量级的Web服务器，

旨在提供快速、灵活、安全的服务。

它最初由Jan Kneschke开发，并于2004年发布。

Lighttpd的设计目标是尽可能减少资源消耗，同时保持高性能和可扩展性。

Lighttpd的主要特点包括：

1. **轻量级和高性能**：Lighttpd的设计旨在最小化内存和CPU占用，使其能够高效地处理高并发请求。

2. **事件驱动架构**：Lighttpd使用事件驱动的架构，可以处理大量并发连接而不会消耗太多系统资源。

3. **模块化设计**：Lighttpd的功能可以通过加载模块进行扩展，这使得用户可以根据需要自定义和配置服务器。

4. **快速CGI支持**：Lighttpd支持快速CGI（FastCGI）和SCGI（Simple Common Gateway Interface），可以与各种编程语言和应用程序框架集成。

5. **支持虚拟主机和URL重写**：Lighttpd支持虚拟主机配置和灵活的URL重写规则，使其适用于各种Web应用场景。

6. **安全性**：Lighttpd具有许多安全功能，包括访问控制、SSL/TLS支持和基于IP的访问限制，以确保服务器和数据的安全性。

总的来说，Lighttpd是一个可靠、高效的Web服务器，特别适用于处理高流量和高并发请求的场景，同时也非常适合用于构建轻量级的Web应用和服务。

# 发展历史

Lighttpd的发展历史可以追溯到2003年，它最初是由德国的开发者Jan Kneschke创建的。以下是Lighttpd的主要发展里程碑：

1. **2003年**：Lighttpd的开发始于2003年，最初是作为一种响应速度更快、资源消耗更低的Web服务器解决方案而创建的。其设计初衷是提供比传统的Web服务器（如Apache）更高的性能和更少的资源消耗。

2. **2004年**：Lighttpd的第一个公开版本（版本1.0.0）于2004年发布。这个版本包含了基本的功能，并且已经展示了Lighttpd的性能优势。

3. **2005年**：随着越来越多的人开始注意到Lighttpd的性能和灵活性，它逐渐成为了一个备受关注的项目。在这一年，Lighttpd的用户和社区开始迅速增长。

4. **2006年**：Lighttpd的开发团队发布了版本1.4.11，这个版本引入了一些新的特性和改进，包括对SSL加速的支持。

5. **2007年**：Lighttpd继续发展壮大，发布了更多的版本，不断改进性能和功能。在这一年，Lighttpd已经成为了一个备受欢迎的替代Apache的选择，特别是在需要处理大量并发连接的场景下。

6. **2010年至今**：Lighttpd持续发展，并逐渐成为了许多Web开发者和系统管理员的首选之一。在过去的几年里，Lighttpd的开发团队不断推出新的版本，改进其性能、安全性和功能，以适应不断变化的Web服务需求。

虽然Lighttpd的市场份额可能不如Apache或Nginx那么大，但它在特定的使用场景下仍然是一个非常有价值的选择，尤其是对于那些追求高性能和低资源消耗的应用程序。

# 使用经验

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