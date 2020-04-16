---
title: Linux下动态库的使用
date: 2017-04-25 23:15:34
tags:
	 - 动态库
---
以一个简单的例子来入手，分析动态库的编译和使用。
# 准备
新建一个目录c-test。
目录下新建一个main.c和一个f1.c。
main.c

```
extern void func1();

int main()
{   
    func1();
    return 0;
}
```
f1.c
```
#include <stdio.h>
void func1()
{   
    printf("func1 \n");
}          
```
编译f1.c
```
gcc -c -fPIC -o f1.o f1.c
```
把f1.o链接为动态库libf1.so
```
gcc -shared f1.o -o libf1.so
```
编译main.c并链接libf1.so。
```
gcc main.c -L./ -lf1
```
运行看看：
```
teddy@teddy-ubuntu:~/test/c-test$ ./a.out 
./a.out: error while loading shared libraries: libf1.so: cannot open shared object file: No such file or directory
```
出错了，并不能找到libf1.so文件。
因为Linux只会从指定路径下去找so文件。我现在也不想对系统进行改动。所以这样做：

```
teddy@teddy-ubuntu:~/test/c-test$ export LD_LIBRARY_PATH=./:$LD_LIBRARY_PATH             
teddy@teddy-ubuntu:~/test/c-test$ ./a.out 
func1 
```
就可以了。

上面我们就实现了动态库的编译和使用。

# 分析
ldd命令：查看elf文件所链接到的动态库的情况。
```
teddy@teddy-ubuntu:~/test/c-test$ ldd ./a.out 
        linux-gate.so.1 =>  (0xb77fb000)
        libf1.so => ./libf1.so (0xb77f3000)
        libc.so.6 => /lib/i386-linux-gnu/libc.so.6 (0xb7620000)
        /lib/ld-linux.so.2 (0x800cf000)
```
nm命令：查看所有的符号。
```
teddy@teddy-ubuntu:~/test/c-test$ nm ./a.out 
0804a020 B __bss_start
0804a020 b completed.7181
0804a018 D __data_start
0804a018 W data_start
08048480 t deregister_tm_clones
080484f0 t __do_global_dtors_aux
08049f04 t __do_global_dtors_aux_fini_array_entry
0804a01c D __dso_handle
08049f0c d _DYNAMIC
0804a020 D _edata
0804a024 B _end
080485c4 T _fini
080485d8 R _fp_hw
08048510 t frame_dummy
08049f00 t __frame_dummy_init_array_entry
080486d4 r __FRAME_END__
         U func1
0804a000 d _GLOBAL_OFFSET_TABLE_
         w __gmon_start__
080483d4 T _init
08049f04 t __init_array_end
08049f00 t __init_array_start
080485dc R _IO_stdin_used
         w _ITM_deregisterTMCloneTable
         w _ITM_registerTMCloneTable
08049f08 d __JCR_END__
08049f08 d __JCR_LIST__
         w _Jv_RegisterClasses
080485c0 T __libc_csu_fini
08048560 T __libc_csu_init
         U __libc_start_main@@GLIBC_2.0
0804853b T main
080484b0 t register_tm_clones
08048440 T _start
0804a020 D __TMC_END__
08048470 T __x86.get_pc_thunk.bx
```
strings命令：看elf文件里的字符串信息。
```
teddy@teddy-ubuntu:~/test/c-test$ strings ./a.out 
/lib/ld-linux.so.2
libf1.so
_ITM_deregisterTMCloneTable
__gmon_start__
_Jv_RegisterClasses
_ITM_registerTMCloneTable
func1
_init
_fini
libc.so.6
_IO_stdin_used
__libc_start_main
_edata
__bss_start
_end
GLIBC_2.0
PTRh
QVh;
t$,U
[^_]
;*2$"(
GCC: (Ubuntu 5.2.1-22ubuntu2) 5.2.1 20151010
GCC: (Ubuntu 4.9.2-10ubuntu11) 4.9.2
.symtab
.strtab
.shstrtab
.interp
.note.ABI-tag
.note.gnu.build-id
.gnu.hash
.dynsym
.dynstr
.gnu.version
.gnu.version_r
.rel.dyn
.rel.plt
.init
.text
.fini
.rodata
.eh_frame_hdr
.eh_frame
.init_array
.fini_array
.jcr
.dynamic
.got
.got.plt
.data
.bss
.comment
crtstuff.c
__JCR_LIST__
deregister_tm_clones
register_tm_clones
__do_global_dtors_aux
completed.7181
__do_global_dtors_aux_fini_array_entry
frame_dummy
__frame_dummy_init_array_entry
main.c
__FRAME_END__
__JCR_END__
__init_array_end
_DYNAMIC
__init_array_start
_GLOBAL_OFFSET_TABLE_
__libc_csu_fini
func1
_ITM_deregisterTMCloneTable
__x86.get_pc_thunk.bx
data_start
_edata
_fini
__data_start
__gmon_start__
__dso_handle
_IO_stdin_used
__libc_start_main@@GLIBC_2.0
__libc_csu_init
_end
_start
_fp_hw
__bss_start
main
_Jv_RegisterClasses
__TMC_END__
_ITM_registerTMCloneTable
_init
```

# 链接和装载的原理


