---
title: shell（1）
date: 2021-05-30 09:24:11
tags:
	- shell

---

--

打算重新梳理一下shell的知识。

# 主要使用的shell

我主要使用bash。所以下面的内容都只针对bash。

# bash简介

Bash（Bourne Again SHell）是一种Unix shell和命令语言，

是Bourne shell（sh）的增强版本。

它是一个命令解释器，用户可以通过Bash在Unix系统（如Linux和macOS）中执行命令、编写脚本以及进行系统管理。

以下是Bash的一些关键特点和功能：

1. **命令解释器：** Bash是一个交互式的命令解释器，用户可以直接在命令行中输入命令，并且Bash会解释并执行这些命令。

2. **脚本语言：** Bash是一种脚本语言，用户可以编写Bash脚本来自动化执行任务、处理文本数据、管理系统等。

3. **功能丰富：** Bash提供了丰富的内置命令和功能，包括文件操作、文本处理、条件判断、循环、函数定义等，使得用户可以方便地进行各种操作。

4. **通配符扩展：** Bash支持通配符扩展（例如`*`和`?`），使得用户可以更加灵活地匹配文件和路径。

5. **命令历史：** Bash会记录用户执行过的命令历史，并且提供了一系列的命令来查看和管理命令历史。

6. **作业控制：** Bash允许用户在后台运行命令，并且提供了一系列的命令来管理这些作业，如`bg`、`fg`和`jobs`等。

7. **环境变量：** Bash允许用户定义和管理环境变量，这些变量可以在Shell会话和脚本中使用，用来传递参数和配置环境。

8. **扩展性：** Bash是一个开源的项目，用户可以根据自己的需要编写自定义的函数和脚本，并且可以利用Bash的扩展机制来扩展其功能。

由于其强大的功能和灵活性，Bash在Unix和类Unix系统中得到了广泛的应用，成为了一个非常受欢迎的命令解释器和脚本语言。

# bash发展历史

Bash（Bourne Again SHell）是一种Unix shell和命令语言，它是Bourne shell（sh）的增强版本。Bash的发展历史可以追溯到1987年，以下是其主要里程碑：

1. **1987年：** Bash由Brian Fox创建，作为GNU计划的一部分发布。它是为了在GNU系统中提供一个免费的、功能强大的shell而开发的。

2. **1989年：** Bash 1.0发布。这个版本是Bash的首个公开发布版本，提供了基本的Bourne shell兼容功能，并增加了一些扩展特性。

3. **1993年：** Bash 1.0的稳定版本发布。这个版本引入了一些重要的功能，如命令历史、程序化执行、shell函数等。

4. **1996年：** Bash 2.0发布。这个版本引入了更多的功能和改进，包括shell选项、数组、更丰富的扩展语法等。

5. **2000年：** Bash 2.05发布。这个版本是2.x系列的最后一个版本。

6. **2001年：** Bash 2.05b发布。这个版本是2.05系列的最后一个版本。

7. **2005年：** Bash 3.0发布。这个版本引入了新的特性和改进，如shell数组初始化、关联数组、更丰富的扩展语法等。

8. **2006年：** Bash 3.2发布。这个版本是3.x系列的最后一个版本。

9. **2009年：** Bash 4.0发布。这个版本引入了一系列的新特性，如增强的通配符、新的扩展语法、改进的作业控制等。

10. **2011年：** Bash 4.2发布。这个版本是4.x系列的最后一个版本。

11. **2014年：** Bash 4.3发布。这个版本引入了一些新特性和改进，包括新的内置命令、更好的作业控制等。

12. **2019年：** Bash 5.0发布。这个版本是目前最新版本，它引入了一些新特性和改进，如内置的`wait`命令、`coproc`命令等。

Bash在Unix和类Unix系统中被广泛使用，它是许多Linux发行版的默认shell，也是macOS的默认shell。它的强大和灵活性使得它成为了一个非常受欢迎的命令解释器和脚本语言。

# 详细说明bash的作业控制，以及它可以给我们日常操作带来哪些便利

Bash提供了作业控制（Job Control）功能，允许用户在后台运行命令，并且可以轻松地管理这些作业。作业控制功能包括以下几个方面：

1. **前台作业和后台作业：** 在Bash中，命令默认是在前台执行的，也就是说命令执行期间会占用控制台。但是，通过在命令末尾添加`&`符号，可以将命令置于后台执行，这样就可以立即返回到控制台而不必等待命令执行完成。

   ```bash
   command &  # 将命令放入后台执行
   ```

2. **作业状态查看：** 用户可以使用`jobs`命令查看当前正在执行的作业以及它们的状态。

   ```bash
   jobs
   ```

3. **切换前台作业：** 使用`fg`命令可以将后台作业切换到前台执行，并将其置于当前控制终端。

   ```bash
   fg %job_number  # 将后台作业切换到前台执行
   ```

4. **后台作业运行：** 使用`bg`命令可以将一个停止状态的作业从后台切换为继续执行。

   ```bash
   bg %job_number  # 将停止的后台作业切换为继续执行
   ```

5. **作业控制信号：** 用户可以使用`Ctrl + Z`将当前正在前台执行的作业暂停，并将其置于后台。同时，可以使用`kill`命令发送信号给作业，如`SIGSTOP`、`SIGCONT`等，控制作业的运行状态。

   ```bash
   kill -SIGSTOP %job_number  # 暂停指定作业
   kill -SIGCONT %job_number  # 继续指定作业
   ```

作业控制给我们日常操作带来了许多便利：

- **后台任务管理：** 当需要执行长时间运行的任务时，可以将其放入后台执行，这样就可以继续使用控制台执行其他任务而无需等待任务完成。
- **多任务处理：** 在同时进行多个任务时，可以使用作业控制轻松地切换和管理不同的任务。
- **错误恢复：** 如果一个作业出现了问题，可以轻松地停止或者重新启动它，而不影响其他作业的执行。
- **任务调度：** 可以使用作业控制在后台执行一系列任务，比如备份、编译、清理等，而不影响前台的交互操作。

# bash的通配符用法举例

Bash的通配符是用来匹配文件名的模式，常用的通配符包括星号（`*`）、问号（`?`）、方括号（`[]`）等。下面是一些通配符的用法示例：

1. **星号（`*`）：匹配零个或多个字符。**

   ```bash
   ls *.txt  # 匹配所有以 .txt 结尾的文件
   ls file*  # 匹配以 "file" 开头的文件
   ls *.jpg  # 匹配所有以 .jpg 结尾的文件
   ```

2. **问号（`?`）：匹配单个字符。**

   ```bash
   ls file?.txt  # 匹配文件名为 "file" 后跟一个字符，再以 .txt 结尾的文件
   ```

3. **方括号（`[]`）：匹配方括号内的任意一个字符。**

   ```bash
   ls [aeiou]*  # 匹配以元音字母开头的文件名
   ls [0-9]*    # 匹配以数字开头的文件名
   ```

4. **花括号（`{}`）：用于生成字符串序列，用逗号分隔不同的选择。**

   ```bash
   cp file{1,2,3}.txt dest/  # 复制 file1.txt、file2.txt 和 file3.txt 到 dest 目录
   ```

5. **递归匹配（`**`）：匹配任意子目录中的文件。**

   ```bash
   ls /path/to/dir/**/*.txt  # 在 /path/to/dir 及其子目录中匹配所有 .txt 文件
   ```

这些通配符使得在Bash中进行文件名匹配变得非常方便。您可以根据需要组合和使用这些通配符来匹配文件名。

# shell的语言规范

https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html

## The Open Group Base Specifications

The Open Group Base Specifications（开放集团基础规范）通常简称为Base Specifications或Base Specs，是由The Open Group维护的一组技术标准和规范。The Open Group是一个全球性的联盟，致力于制定供应商中立的技术标准和认证，旨在实现IT系统在各种平台上的互操作性和可移植性。

Base Specifications为操作系统和其他计算环境的开发提供了基础，定义了接口、协议和行为，以确保在不同的实现之间实现兼容性和一致性。这些规范涵盖了广泛的领域，包括：

1. **系统接口**：定义了应用程序与操作系统交互的系统调用、库和其他系统级功能的接口。

2. **网络**：指定了用于在各种网络架构上系统之间进行通信的协议、API和其他与网络相关的标准。

3. **文件格式和API**：定义了标准文件格式、文件系统接口和用于文件操作和管理的API。

4. **命令和实用程序**：指定了标准命令行实用程序及其行为，确保在不同的类Unix操作系统上的一致性。

5. **安全**：定义了与计算环境的安全相关的标准和机制，包括身份验证、访问控制、加密等安全方面。

6. **国际化和本地化**：规定了软件国际化（i18n）和本地化（l10n）处理的标准，包括字符编码、语言支持和文化惯例。

7. **Shell和实用程序**：定义了用于shell脚本语言（例如POSIX shell）和命令行环境中常用的实用程序的标准。

8. **实时和嵌入式系统**：提供了针对实时和嵌入式系统的规范，解决了它们的独特需求和约束。

Base Specifications定期由The Open Group进行更新和维护，由行业专家和成员组织贡献。符合这些规范可以确保软件实现符合广泛接受的标准，促进IT系统的互操作性、可移植性和可维护性。

开发人员、供应商和组织可以将Base Specifications作为构建和集成软件组件的参考，以确保与现有系统的兼容性，并促进更加开放和协作的计算生态系统。此外，基于这些规范的认证计划允许供应商展示其产品和服务符合行业标准，增强对其产品和服务的信任和信心。



# 脚本内部的函数也可以进行重定向

```
test_echo()
{
	echo "111"
}
test_echo >> ./1.txt
```



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

# 命令的返回值

## 非0返回值的取值范围

在Unix/Linux系统中，非0返回值通常表示命令执行失败或出现了某种错误。具体来说，一般情况下，返回值的范围可以分为以下几种情况：

1. **1至125**：这个范围内的值通常由命令自身定义，用于表示不同的错误类型或状态。不同的命令可能会定义不同的非0返回值。你可以查阅相应命令的文档或手册来了解其具体含义。

2. **126**：这个返回值通常表示命令无法执行，可能是因为找不到命令文件、权限不足等原因导致的执行失败。

3. **127**：这个返回值通常表示命令不存在，即Shell无法找到要执行的命令文件。

4. **128及以上**：这个范围内的值通常用于表示命令被信号中断终止的情况。具体来说，如果命令被信号`SIGINT`、`SIGQUIT`、`SIGILL`、`SIGABRT`、`SIGFPE`、`SIGSEGV`、`SIGPIPE`、`SIGALRM`、`SIGTERM`等中断，则返回值为`128 + 信号值`。

总的来说，虽然非0返回值的具体含义可能因命令而异，但通常情况下，非0返回值表示命令执行失败或出现了某种错误。

## C语言的main函数return -1 在命令行上得到的返回值是多少

在C语言的`main`函数中，`return -1;`语句会将返回值设为-1。当在命令行上执行这个程序时，其返回值会被映射到一个合法的范围内。

根据POSIX标准，程序的返回值必须在0到255之间。如果`main`函数的返回值为负数，POSIX标准要求取其最低字节的8位来作为程序的返回值。因此，-1会被映射为255。

所以，当在命令行上执行`main`函数返回-1的C程序时，其返回值将会是255。



## 检查返回值

最简单常见的方式。

```
echo abcdef | grep abcd
if [ $? -ne 0 ]; then
	echo "not found"
else
	echo "found"
fi
```

再简洁一点的。我觉得这个不好，不直观，只是一个冷门的技巧而已。

```
if echo abcdef | grep -q abcd; then
	echo "found"
else
	echo "not found"
fi
```

再简洁点的。

```
echo abcdef |grep -q abcd && echo "found" || echo "not found"
```



# bash调试方法

## bashdb调试

有个工具叫bashdb。可以用来调试bash脚本。使用方法类似gdb。

## -x选项

1、bash -x test.sh

2、在脚本前面加上#!/bin/sh -x

3、用set -x来启用，用set +x来禁用。



参考资料

1、如何在 Linux 或者 UNIX 下调试 Bash Shell 脚本

<https://linux.cn/article-9302-1.html>

# 重定向

把stdout和stderr重定向到/dev/null。

```
./test.sh 1>/dev/null 2>&1
```

简洁的：

```
./test.sh &> /dev/null
```



# `2>&1`是什么意思

在有些脚本里，会有`which docker > /dev/null 2>&1`这种用法。代表的具体内涵是什么呢？

0/1/2分别代表了stdin、stdout、stderr。这个是知道的。

我们先看看一条命令在命令行上执行时的输出情况。

以普通用户执行：find /etc -name passwd

这条命令会有正确输出和错误信息的。

如下：

```
teddy@teddy-ubuntu:~/work/test$ find /etc -name passwd
find: ‘/etc/polkit-1/localauthority’: Permission denied
find: ‘/etc/vmware-tools/GuestProxyData/trusted’: Permission denied
/etc/passwd
find: ‘/etc/docker’: Permission denied
find: ‘/etc/cups/ssl’: Permission denied
find: ‘/etc/ssl/private’: Permission denied
/etc/pam.d/passwd
/etc/cron.daily/passwd
```

可以看到，默认stdout和stderr都是输出到屏幕上的。我们现在就把stdout和stderr分开看看。

```
find /etc -name passwd > find.out 2>find.err
```

我们看find.out有什么内容：

```
teddy@teddy-ubuntu:~/work/test$ cat find.out
/etc/passwd
/etc/pam.d/passwd
/etc/cron.daily/passwd

```

find.err内容：

```
teddy@teddy-ubuntu:~/work/test$ cat find.err
find: ‘/etc/polkit-1/localauthority’: Permission denied
find: ‘/etc/vmware-tools/GuestProxyData/trusted’: Permission denied
find: ‘/etc/docker’: Permission denied
find: ‘/etc/cups/ssl’: Permission denied
find: ‘/etc/ssl/private’: Permission denied

```

可以用一个`&`来表示1和2。

例如：

```
teddy@teddy-ubuntu:~/work/test$ find /etc/ -name passwd &>find.all
teddy@teddy-ubuntu:~/work/test$ cat find.all
find: ‘/etc/polkit-1/localauthority’: Permission denied
find: ‘/etc/vmware-tools/GuestProxyData/trusted’: Permission denied
/etc/passwd
find: ‘/etc/docker’: Permission denied
find: ‘/etc/cups/ssl’: Permission denied
find: ‘/etc/ssl/private’: Permission denied
/etc/pam.d/passwd
/etc/cron.daily/passwd
teddy@teddy-ubuntu:~/work/test$ 
```

有时候是希望把stderr重定向到跟stdout一样的地方。按照自然的写法是2>1，但是这个实际上会是重定向到一个名字叫`1`的文件里去了。所以需要加一个`&`来表示。就是`2>&1`了。

`which docker > /dev/null 2>&1`这句的完整含义，就是stdout不输出，stderr也不输出。

# `[`的知识

`[`的作用相当于test命令。

有个选项，-a表示与的关系。例如`[ "$xxx=a" -a "$yyy=b" ]`。表示这2个条件同时为真。

```
teddy@teddy-ubuntu:~$ [ "$xxx" = "a" ]
teddy@teddy-ubuntu:~$ echo $?
1
teddy@teddy-ubuntu:~$ xxx=a
teddy@teddy-ubuntu:~$ [ "$xxx" = "a" ]
teddy@teddy-ubuntu:~$ echo $?
0
teddy@teddy-ubuntu:~$ 
```

# 用`.`执行和直接执行脚本的区别

用点来执行是使得脚本内容在当前shell里执行，而不是另外开一个shell来执行。

这个带来的一个好处就是环境变量都可以访问到。

一个典型用途，就是让脚本直接可以进行包含。

新建一个inc.sh和一个test.sh。

inc.sh：

```
#!/bin/sh 

xxx=a
echo "abc"

```

test.sh：

```
#!/bin/sh
. ./inc.sh
echo $xxx

```

在test.sh里可以访问到inc.sh里定义的变量。这就是最大的好处。

用`.`执行时的参数情况和直接执行的也不同。

test.sh内容：

```
#!/bin/sh
echo "0:$0" 
echo "1:$1"
```

直接执行：

```
teddy@teddy-ubuntu:~/work/test/shell$ ./test.sh aa
0:./test.sh
1:aa
```

用`.`执行：

```
teddy@teddy-ubuntu:~/work/test/shell$ . ./test.sh aa
0:-bash
1:aa
```

感觉用点执行的效果就像是把脚本内容一条条扒出来在命令行上敲是一样的效果。



# su和su -的区别

su -会把环境变量也带过去。相当于以root用户登录一样。



# printf和echo区别

1、printf的用法跟c语言中的很类似，可以格式化打印。

2、printf打印后，不会自动换行的。



# 怎么查看所有的环境变量

用export就可以看到。用env也可以看到。二者的区别是，export的排序了，env的没有排序。

# declare用法

declare是一个命令，是bash版本2才开始有的。

用来限定变量的属性。

```
declare -r a #变量a就是只读的了。
declare -i b #变量b就是整数的了。
declare -a c #变量c是数组。
declare -f ddd # ddd是函数
declare -x e #变量e会被export。
```

# exec命令

这个跟直接执行的区别就是，exec是取代了原有进程。

我们在shell上执行：

```
exec ls
```

执行完会退出shell的。

好处是什么？

# cd -- dir

跟直接cd dir没有区别。

# .bash_profile和.bashrc区别

下面是`.bash_profile`和`.bashrc`的主要区别：

| `.bash_profile`                                              | `.bashrc`                                                    |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 主要用于登录shell时执行的配置文件。                          | 主要用于非登录shell时执行的配置文件。                        |
| 在用户登录时执行一次，通常用于设置环境变量、启动应用程序等。 | 在每次启动一个新的非登录shell时执行，通常用于定义别名、设置终端颜色等。 |
| 仅当用户登录时才会执行，例如通过SSH登录或在本地控制台登录。  | 在任何新的shell会话中都会执行，无论是登录shell还是非登录shell。 |
| 一般情况下，该文件只会包含一次执行其他脚本的命令，例如`source ~/.bashrc`。 | 一般情况下，该文件包含用户自定义的配置，如别名、函数等。     |

总的来说，`.bash_profile`用于配置登录时需要执行的内容，而`.bashrc`用于配置每个新的非登录shell会话中需要执行的内容。通常情况下，`.bash_profile`会调用`.bashrc`，以确保登录和非登录shell都能获得正确的配置。

## 什么是非登陆shell

非登录shell是指在用户登录后打开的新的shell会话，而不是用户初始登录时的shell。在非登录shell中，通常不会执行`.bash_profile`，而是执行`.bashrc`。这种情况通常发生在用户已经登录系统后，在图形界面中打开一个终端窗口或者在已经登录的终端会话中打开一个新的子shell。

非登录shell通常用于用户在已登录系统后的交互操作，例如运行命令、编辑文件等。

与登录shell相比，非登录shell不会重新设置用户环境，

因此不会执行`.bash_profile`，而是执行`.bashrc`。

==简单说，就是你在shell，再手动执行一下bash程序，这个时候执行的就是.bashrc了。==



# 参考资料

1、

https://www.w3cschool.cn/shellbook/et3s9ozt.html