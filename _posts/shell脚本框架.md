---
title: shell脚本框架
date: 2021-11-04 11:27:25
tags:
	- shell

---

--

https://github.com/CecilWesterhof/BashLibrary



# bashlib.sh

当然，下面是一个简单的示例，演示如何使用`bashlib`库编写一个Bash脚本，用于执行一些简单的任务：

首先，您需要安装`bashlib`库。

假设您已经将`bashlib`库保存为`bashlib.sh`文件。

```bash
#!/bin/bash

# 引入 bashlib.sh 库
source bashlib.sh

# 在函数库中定义的一些常见函数会在这里可用

# 例如，使用 bl.log 函数记录日志
bl.log.info "这是一条信息日志"
bl.log.warn "这是一条警告日志"
bl.log.error "这是一条错误日志"

# 使用 bl.args.parse 函数解析命令行参数
bl.args.parse "--option1=value1 --option2=value2" "h/help,option1:,option2:"

# 使用 bl.args.get 函数获取解析后的参数值
option1_value=$(bl.args.get option1)
option2_value=$(bl.args.get option2)

# 执行您的脚本逻辑
echo "选项1的值：$option1_value"
echo "选项2的值：$option2_value"
```

在上面的示例中，我们首先导入了`bashlib.sh`库。然后，我们使用`bl.log`函数记录了一些日志信息。接下来，我们使用`bl.args.parse`函数解析命令行参数，该函数的第一个参数是要解析的参数字符串，第二个参数是定义的选项。最后，我们使用`bl.args.get`函数获取解析后的参数值，并执行脚本逻辑。

这只是一个简单的示例，您可以根据您的需求扩展和修改它。`bashlib`提供了许多其他有用的功能，您可以在需要时使用它们来简化脚本编写过程。

# amlogic的代码

看amlogic的编译bootloader的脚本，觉得这个框架不错，可以扒出来做shell脚本框架用。

总的入口：

```
function main() {
	if [ -z $1 ]
	then
		usage
		return
	fi

	MAIN_FOLDER=`pwd`
	parser $@
	build $@
}

main $@ # parse all paras to function
```

还是从main来入口，参数传递给main函数。

main函数分两大步：解析参数、执行。

parse函数

首先把所有参数都放入到argv这个数组里。注意数组的定义方法。局部变量统一都用local来声明。

全局变量都用declare来声明。这样就看起来比较像正式的语言。

```
	local i=0
	local argv=()
	for arg in "$@" ; do
		argv[$i]="$arg"
		i=$((i + 1))
	done
```

这样来循环解析参数

```
	i=0
	while [ $i -lt $# ]; do
		arg="${argv[$i]}"
		i=$((i + 1)) # must place here
		case "$arg" in
			-h|--help|help)
				usage
				exit ;;
			--config)
				print_config
				return ;;
			# SCRIPT_ARG_CHIPSET_VARIANT is used in source variable
			# soc, so should add first
			--chip-varient)
				SCRIPT_ARG_CHIPSET_VARIANT="${argv[$i]}"
				export SCRIPT_ARG_CHIPSET_VARIANT
				continue ;;
			--check-compile)
				check_compile "${argv[@]:$((i))}"
				exit ;;
			clean|distclean|-distclean|--distclean)
				clean
				exit ;;
			*)
		esac
	done
```

打印帮助信息：这样可以很方便地保留格式。

```
function usage() {
  cat << EOF
  Usage:
    $(basename $0) --help
EOF
}
```

