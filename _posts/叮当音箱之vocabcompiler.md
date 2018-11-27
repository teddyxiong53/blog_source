---
title: 叮当音箱之vocabcompiler
date: 2018-11-27 20:57:51
tags:
	- 智能音箱

---



vocabcompiler这个具体是起什么作用呢？

对应的vocabcompiler.py文件， 有500行。

从文件头的注释看，是用来遍历所有的WORD变量（在各个plugin里写的），根据这个创建一个字典。

主要对外的方法有：

get_all_phrases

这个就是把所有plugin里的WORD变量都遍历出来。

get_keyword_phrases

这个对应内容是写在static/keyword_phrases文件里的。不多。就这些。18个。

```
BE
BEING
BUT
DID
FIRST
IN
IS
IT
JASPER
NOW
OF
ON
RIGHT
SAY
WHAT
WHICH
WITH
WORK
```

