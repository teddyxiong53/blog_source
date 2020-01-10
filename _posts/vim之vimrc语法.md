---
title: vim之vimrc语法
date: 2020-01-010 09:00:08
tags:
	- vim

---

1

.vimrc是配置自己的vim的主要文件。

了解一下基本的语法。

```
注释
	注释是用一个双引号开头的。
变量
	变量分为两种。
	1、标量变量。2、特殊变量。
	标量变量
		命名方式为  作用域:变量名。
		b:xx 只对当前buffer有效的变量。
		w:xx 只对当前window有效的变量。
		g:xx 全局变量
		v:xx vim预设变量
		a:xx 函数的参变量。
		引用的时候，也要把作用域加上。
	特殊变量
		有3种：
			$NAME 环境变量
			&name 选项。
			@r  寄存器
	变量赋值
		let var=name
	释放变量
		unlet! var
控制结构
	条件：
        if 
        elseif
        else
        endif
	循环：
		while xx
			xx
			break/continue
		endwhile
函数
	function xx(aa)
		xx
	endfunc
	函数的调用：
		call xx(aa)
执行命令
	1、执行命令
        在vimrc里执行命令是：
            exec "ls ./ -lh"
        在命令行模式
            :!ls -lh
	2、键盘映射
		map：所有模式都映射
		nmap：normal模式下映射。
		vmap：visual模式下映射
		imap：insert模式下映射。
	3、自动命令：
		autocmd。简写au。
		
```



参考资料

1、vimrc语法

https://www.cnblogs.com/biglucky/p/4511537.html