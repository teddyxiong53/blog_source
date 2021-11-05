---
title: shell脚本框架
date: 2021-11-04 11:27:25
tags:
	- shell

---

--

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

