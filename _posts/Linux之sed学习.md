---
title: Linux之sed学习
date: 2018-09-22 14:58:17
tags:
	- Linux

---

--

之前大略看过sed的语法。

现在要逐渐把工作中碰到的用法都总结下来。

```
sed -n 's@^//applet:@@p'
```

这个是在busybox的gen_build_files.sh里的。具体是什么效果呢？

这里的@是做分隔符用的。



sed 是一种单行编辑器，它一次处理一行内容。

处理时，把当前处理的行存储在临时缓冲区中，称为“模式空间”（pattern space），

接着用sed命令处理缓冲区中的内容，处理完成后，把缓冲区的内容送往屏幕。

接着处理下一行，这样不断重复，直到文件末尾。



文件内容并没有 改变，除非你使用重定向存储输出。



Sed主要用来自动编辑一个或多个文件；

简化对文件的反复操作；

编写转换程序等。



# 替换常用命令

基本的：

```
sed 's/old/new/'
```

构成分析：

1、s。表示替换。

2、/。有3根。也可以用?等其他的符号，都保持一样就好了。

3、单引号。可以换成双引号的。

把old替换为new。

全部替换：

```
sed 's/old/new/g'
```

在最后增加了一个g，如果没有，只替换匹配的第一个。

加上行数指定：

```
sed '2s/old/new/' 替换第二行的
sed '2,5s/old/new/'替换第2到第5行的。
```

执行多个规则：

```
sed 's/old/new/; s/old2/new2/'
```



# 常用选项

```
-n：
	安静模式，加上这个选项，则只有经过处理的行才显示出来。
-e：
	直接在命令列模式上进行sed动作编辑（？怎么理解？）
-f
	把所有的操作写在一个文件里，这个在规则比较复杂的时候用。
	
-i：
默认都是 直接输出到屏幕的，用i选项，就会直接插入到文件里去。
```

```
sed [opt] 'n1,n2function'  1.txt
```

function叫动作。

动作有：

```
a：增加
c：取代。
d：删除
i：插入
p：打印
s：取代
```



# 例子

`sed`（Stream Editor）是一个用于文本处理的流编辑器，它在Linux和Unix系统中非常常见。`sed`主要用于对文本进行搜索、替换、删除、插入等操作，可以通过脚本或者命令行参数来执行这些操作。

以下是一些常用的`sed`命令及其功能：

1. **替换文本：**
   ```
   sed 's/old_text/new_text/g' filename
   ```
   这个命令将文件中所有的`old_text`替换为`new_text`。

2. **删除行：**
   ```
   sed '/pattern/d' filename
   ```
   这个命令将删除包含指定`pattern`的所有行。

3. **插入行：**
   ```
   sed '3i\new_line' filename
   ```
   这个命令将在第3行之前插入新的行。

4. **追加行：**
   ```
   sed '$a\new_line' filename
   ```
   这个命令将在文件的最后一行追加新的行。

5. **打印行：**
   ```
   sed -n '5p' filename
   ```
   这个命令将打印文件中的第5行。

6. **替换指定范围内的文本：**
   ```
   sed '2,5s/old_text/new_text/g' filename
   ```
   这个命令将在第2行到第5行之间替换指定文本。

7. **使用正则表达式：**
   ```
   sed 's/[0-9]/X/g' filename
   ```
   这个命令将文件中的所有数字替换为字母X。

8. **从文件读取`sed`脚本：**
   
   ```
   sed -f script.sed filename
   ```
   这个命令从名为`script.sed`的文件中读取`sed`脚本并应用于指定的文件。

这只是一些`sed`命令的基本示例，`sed`提供了丰富的功能和选项，可以根据具体需求进行更复杂的文本处理操作。请查阅`sed`的官方文档以获取更多详细信息。

# 思维导图

https://yemaosheng.com/wp-content/uploads/2009/05/sed.jpg

# 使用脚本的例子

**使用文件中的`sed`脚本进行多个操作：**
假设有一个名为`myscript.sed`的文件包含以下内容：

```
s/apple/orange/g
2i\
New line
/xyz/d
```

然后可以使用以下命令应用该脚本：
```bash
sed -f myscript.sed 1.txt
```

当前1.txt的内容是：

```
apple
xyz
123
```

执行时，输出：

```
sed -f ./script.sed 1.txt
orange
New line
123
```

使用用-i选项（inplace的意思，直接修改目标文件的意思）

```
sed -i -f ./script.sed 1.txt
```

则1.txt的内容直接被修改。





# 参考资料

1、sed命令

http://man.linuxde.net/sed

2、sed 字符串替换

https://www.cnblogs.com/linux-wangkun/p/5745584.html

3、

https://www.itdaan.com/blog/2017/09/08/1fbfa9a146319f526fc611999ada80b2.html