---
title: Linux之提高终端下的工作效率
date: 2018-03-26 17:38:43
tags:
	- Linux

---

--

觉得还是有必要把这一块梳理一下，提高命令行下面的工作效率。



用jobs和fg命令在多任务之间切换。



# 命令行上快速删除字符

```
ctrl + u 从光标位置删除到开头
ctrl + k 从光标位置删除到结尾
alt + f 往前跳一个单词
alt + b 往后跳一个单词
ctrl + w 删除一个单词
```

# 历史命令的快速执行

```
!! 连续2个感叹号，相当于执行一下上一条命令。好像没有什么优势，我直接向上一下箭头符号也可以。
```

使用上一条命令的最后一个参数来执行

```
例如：
ls /proc/interrupt
觉得需要加上-lh
可以这样：
ls -lh !$ 
这样!$就表示上一条命令的最后一个参数。
```

使用上一条命令的所有参数

```
$*
```

感觉对我来说，不是很有用。了解一下就可以了。



# 参考资料

1、提高命令行效率。

这个网站非常好。值得好好研究一下。

https://www.ctolib.com/linux/categories/linux-shell-command-line-productivity.html

2、提高Linux工作效率的十大bash技巧

https://blog.csdn.net/zhaomininternational/article/details/52038101

3、How to Multitask in the Linux Terminal: 3 Ways to Use Multiple Shells at Once

https://www.howtogeek.com/111417/how-to-multitask-in-the-linux-terminal-3-ways-to-use-multiple-shells-at-once/

4、

https://juejin.cn/post/6844903905524989960