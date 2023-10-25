---
title: php之heredoc
date: 2018-08-15 21:28:32
tags:
	- php

---



php里的heredoc是用来引用字符串的一种方式。



语法是：

1、使用操作符`<<<`。

2、操作符后面紧跟标识符，之后重新起一行，输入要引用的字符串，可以包含变量。

3、新的一行，顶格写结束符。用分号结束。



举例：

```
<?php
$str = <<<ET
heredoc test

ET;
echo $str
?>
```

效果是输出：`heredoc test`这一行字符串。

ET是一个标签的名字。

这个是一般的命名。你可以改成其他的任意字符串。

# shell的heredoc

Here documents（heredocs）是一种在shell脚本中用于处理多行文本块的技术。Heretags，或heredocs，是在shell脚本中以特殊方式处理多行文本块的一种技术。这在脚本中非常有用，因为它允许您将大段文本嵌入到脚本中，而不必将其存储在外部文件中。

Heredocs的语法通常如下：

```bash
command <<DELIMITER
...多行文本...
DELIMITER
```

在这里，`command` 是接收文本块的命令，`DELIMITER` 是定界符，它可以是您选择的任何字符串。DELIMITER 用于指定文本块的开始和结束，而这两个定界符之间的文本将作为输入传递给 `command`。

以下是一个简单的示例，演示了如何在shell脚本中使用heredoc：

```bash
#!/bin/bash

cat <<EOF
This is a heredoc example.
It allows you to write multiple lines of text.
EOF
```

在此示例中，`cat` 命令接受 heredoc 中的文本块并将其输出到标准输出。DELIMITER（在此示例中是EOF）标记了文本块的开始和结束。

注意以下要点：

- 定界符可以是任何字符串，但在开始和结束定界符时必须一致。通常使用 `EOF`、`<<END`、`<<HTML` 等。

- ==定界符不区分大小写。例如，`<<EOF` 和 `<<eof` 是等效的。==

- 在heredoc中，变量会被展开，这意味着您可以在文本块中使用变量，它们将被正确替换为其值。

- 除了 `cat`，您还可以在heredoc中使用其他命令，如 `echo`、`sed`、`awk` 等，以便处理文本块。

Heretags 是shell脚本中非常有用的技术，因为它允许您在脚本中包含大段文本而不必维护额外的文件。





# 参考资料

1、PHP heredoc 用法

https://www.cnblogs.com/igoogleyou/p/heredoc.html