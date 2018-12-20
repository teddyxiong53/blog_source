---
title: shell的使用艺术
date: 2018-12-20 17:52:17
tags:
	- shell

---



在github上闲逛，看到这个文档，觉得特别好：

https://github.com/jlevy/the-art-of-command-line/blob/master/README-zh.md

把我还不知道的学习一下。

# 日常使用

shell输入时的删除：

```
ctrl+w：删除光标前面的一个单词。
ctrl+u：从光标处到最前面都删掉。
ctrl+k：从光标到行尾的都删掉。
ctrl+l：相当于clear。但是这个方便多了。
```

man readline，可以看到很多快捷键。



如果你输入了一条很长的命令，但是现在不想执行，有个窍门可以保存。

就是在前面加上#号执行一下，后面就可以在history里找到了。

pstree -p。可以用树形结构来展示进程的关系。



