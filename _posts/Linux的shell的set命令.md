---
title: Linux的shell的set命令
date: 2024-02-02 13:34:17
tags:
	- Linux

---

--

一般用set命令都是很简单的set -x 和set -e。

没有仔细研究过set的完整用法，在buildroot的utils\docker-run 发现这个：

```
set -o errexit -o pipefail
```

才发现这个set的用法还比较复杂。

研究一下。

# 基本用法

==`set` 是一个在 Linux 命令行中用于配置 shell 环境的命令。==

它有多种用途，==可以用来设置和显示各种 shell 参数==。以下是一些常见的用法和说明：

1. **显示所有变量和函数：**
   
   ```
   set

这会显示当前 shell 中==所有已设置的变量和函数。==

2. **设置环境变量：**

   set VAR_NAME=value


用于设置环境变量，将 `VAR_NAME` 设置为指定的值。

3. **取消变量：**

   set +u VAR_NAME


这会将 `VAR_NAME` 取消设置，即删除该变量。

4. **显示特定变量的值：**

   echo $VAR_NAME


   用于显示特定环境变量的值。

5. **设置选项：**

   set -o option


   用于设置 shell 选项，可以使用 `set -o` 来查看所有选项。==例如，`set -o errexit` 将使 shell 在命令返回非零退出状态时立即退出。==

6. **取消选项：**

   set +o option


用于取消先前设置的 shell 选项。

7. **显示当前 shell 中的所有函数：**

   set | grep '()'


通过使用管道和 `grep` 来显示当前 shell 中的所有函数。

8. **显示脚本中执行的命令：**

   set -x


用于显示脚本中每个命令执行的详细信息，便于调试。

9. **关闭命令执行显示：**

   set +x


   用于停止显示脚本中每个命令的详细信息。

这只是 `set` 命令的一些常见用法，它有很多其他选项和功能，你可以通过 `help set` 或者 `man set` 查看更详细的信息。

## 参数符合规则

看起来 ：

-xx：这个是打开某个选项。
+xx：这个是关闭某个选项。

记忆方法就是-xx是所有linux命令的常规的选项用法。

而+xx是set命令这里特意用来跟-xx对着干的。

所以是用来关闭选项。


# set -o查看的所有选项

```
allexport       off
braceexpand     on
emacs           on
errexit         off
errtrace        off
functrace       off
hashall         on
histexpand      on
history         on
ignoreeof       off
interactive-comments    on
keyword         off
monitor         on
noclobber       off
noexec          off
noglob          off
nolog           off
notify          off
nounset         off
onecmd          off
physical        off
pipefail        off
posix           off
privileged      off
verbose         off
vi              off
xtrace          off
```



`set -o` 用于显示或修改 shell 的各种选项。以下是一些常见的选项：

1. **errexit (-e):**

   set -o errexit


   当一个命令返回非零退出状态时，脚本将立即退出。

2. **nounset (-u):**

   set -o nounset


   当尝试使用未设置的变量时，脚本将产生错误并退出。

3. **pipefail:**

   set -o pipefail


   如果管道中的任何一个命令失败，则整个管道的退出状态将是失败的。

4. **noclobber:**

   set -o noclobber


   防止使用 `>` 和 `>>` 重定向操作符时意外地覆盖文件。

5. **xtrace (-x):**

   set -o xtrace


   显示脚本中每个命令的执行详细信息，用于调试脚本。

6. **verbose (-v):**

   set -o verbose


   类似于 `xtrace`，但只显示每个命令的输入行，而不是执行时的详细信息。

7. **monitor (-m):**

   set -o monitor


启用作业控制，将后台作业与前台作业区分开。

8. **nocaseglob:**

   set -o nocaseglob


   在文件名扩展时忽略大小写。

9. **ignoreeof:**

   set -o ignoreeof


   防止通过重复按 `Ctrl-D` 来意外退出 shell。

这只是其中的一些选项，你可以使用 `set -o` 来查看当前 shell 中启用的所有选项，以及使用 `set +o` 来关闭这些选项。例如，`set +o errexit` 将关闭 `errexit` 选项。

## set -o xx等价于其他的set -单字符选项的



# set -nounset

这个就是在碰到没有定义的变量时，直接报错退出。而不是作为空字符处理。

这样可以保证程序的健壮性。

