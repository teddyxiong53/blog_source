---
title: gcc编译过程分析
date: 2016-12-30 22:14:15
tags:
	- gcc
---
现在我们就以helloworld程序为例，来分析gcc的编译过程。
main.c
```
#include <stdio.h>
int main()
{
	printf("helloworld\n");
	return 0;
}
```
最简单的编译方式是：`gcc main.c`。这样会默认生成可执行文件a.out。
其实gcc默认帮我们封装了好几个步骤的工作，第一步是



用`-v`选项来看连接过程的详细信息。
```
teddy@teddy-ubuntu:~/test/c-test$ gcc -v -o test test.o myprintf.o
Using built-in specs.
COLLECT_GCC=gcc
COLLECT_LTO_WRAPPER=/usr/lib/gcc/i686-linux-gnu/5/lto-wrapper
Target: i686-linux-gnu
Configured with: ../src/configure -v --with-pkgversion='Ubuntu 5.2.1-22ubuntu2' --with-bugurl=file:///usr/share/doc/gcc-5/README.Bugs --enable-languages=c,ada,c++,java,go,d,fortran,objc,obj-c++ --prefix=/usr --program-suffix=-5 --enable-shared --enable-linker-build-id --libexecdir=/usr/lib --without-included-gettext --enable-threads=posix --libdir=/usr/lib --enable-nls --with-sysroot=/ --enable-clocale=gnu --enable-libstdcxx-debug --enable-libstdcxx-time=yes --with-default-libstdcxx-abi=new --enable-gnu-unique-object --disable-vtable-verify --enable-libmpx --enable-plugin --with-system-zlib --disable-browser-plugin --enable-java-awt=gtk --enable-gtk-cairo --with-java-home=/usr/lib/jvm/java-1.5.0-gcj-5-i386/jre --enable-java-home --with-jvm-root-dir=/usr/lib/jvm/java-1.5.0-gcj-5-i386 --with-jvm-jar-dir=/usr/lib/jvm-exports/java-1.5.0-gcj-5-i386 --with-arch-directory=i386 --with-ecj-jar=/usr/share/java/eclipse-ecj.jar --enable-objc-gc --enable-targets=all --enable-multiarch --disable-werror --with-arch-32=i686 --with-multilib-list=m32,m64,mx32 --enable-multilib --with-tune=generic --enable-checking=release --build=i686-linux-gnu --host=i686-linux-gnu --target=i686-linux-gnu
Thread model: posix
gcc version 5.2.1 20151010 (Ubuntu 5.2.1-22ubuntu2) 
COMPILER_PATH=/usr/lib/gcc/i686-linux-gnu/5/:/usr/lib/gcc/i686-linux-gnu/5/:/usr/lib/gcc/i686-linux-gnu/:/usr/lib/gcc/i686-linux-gnu/5/:/usr/lib/gcc/i686-linux-gnu/
LIBRARY_PATH=/usr/lib/gcc/i686-linux-gnu/5/:/usr/lib/gcc/i686-linux-gnu/5/../../../i386-linux-gnu/:/usr/lib/gcc/i686-linux-gnu/5/../../../../lib/:/lib/i386-linux-gnu/:/lib/../lib/:/usr/lib/i386-linux-gnu/:/usr/lib/../lib/:/usr/lib/gcc/i686-linux-gnu/5/../../../:/lib/:/usr/lib/
COLLECT_GCC_OPTIONS='-v' '-o' 'test' '-mtune=generic' '-march=i686'
 /usr/lib/gcc/i686-linux-gnu/5/collect2 -plugin /usr/lib/gcc/i686-linux-gnu/5/liblto_plugin.so -plugin-opt=/usr/lib/gcc/i686-linux-gnu/5/lto-wrapper -plugin-opt=-fresolution=/tmp/cc2Wk1iT.res -plugin-opt=-pass-through=-lgcc -plugin-opt=-pass-through=-lgcc_s -plugin-opt=-pass-through=-lc -plugin-opt=-pass-through=-lgcc -plugin-opt=-pass-through=-lgcc_s --sysroot=/ --build-id --eh-frame-hdr -m elf_i386 --hash-style=gnu --as-needed -dynamic-linker /lib/ld-linux.so.2 -z relro -o test /usr/lib/gcc/i686-linux-gnu/5/../../../i386-linux-gnu/crt1.o /usr/lib/gcc/i686-linux-gnu/5/../../../i386-linux-gnu/crti.o /usr/lib/gcc/i686-linux-gnu/5/crtbegin.o -L/usr/lib/gcc/i686-linux-gnu/5 -L/usr/lib/gcc/i686-linux-gnu/5/../../../i386-linux-gnu -L/usr/lib/gcc/i686-linux-gnu/5/../../../../lib -L/lib/i386-linux-gnu -L/lib/../lib -L/usr/lib/i386-linux-gnu -L/usr/lib/../lib -L/usr/lib/gcc/i686-linux-gnu/5/../../.. test.o myprintf.o -lgcc --as-needed -lgcc_s --no-as-needed -lc -lgcc --as-needed -lgcc_s --no-as-needed /usr/lib/gcc/i686-linux-gnu/5/crtend.o /usr/lib/gcc/i686-linux-gnu/5/../../../i386-linux-gnu/crtn.o
```
我们把上面这些信息抽取有用部分整理如下：
```
ld --eh-frame-hdr -m elf_i386 -dynamic-linker /lib/ld-linux.so.2  -o test test.o myprintf.o -L/usr/lib/gcc/i686-linux-gnu/5 -L/usr/lib/i386-linux-gnu     -L/lib/i386-linux-gnu -L/lib -L/usr/lib /usr/lib/i386-linux-gnu/crt1.o /usr/lib/i386-linux-gnu/crti.o /usr/lib/gcc/i686-linux-gnu/5/crtbegin.o /usr/lib/gcc/i686-linux-gnu/5/crtend.o  /usr/lib/i386-linux-gnu/crtn.o -lc -lgcc_s
```
这样我们就可以用ld链接得到可执行文件了。

`ld --verbose` 可以查看默认的链接脚本。


gcc的常用编译选项。
`-Wl,xxx,yyy`:跟在Wl后面的选项用逗号隔开，这些选项会传递给linker。
例如`-Wl,-Maps,output.map`这个也可以这样写`-Wl,-Maps=output.map`。
这个一般用到linker被gcc间接调用的时候，我们一般很少直接调用linker，大多是通过gcc内部自动去调用linker。
`-Wl`可以多次使用。例如这样：`gcc -Wl,--startgroup foo.o bar.o -Wl,--endgroup`


`--as-needed`这个链接选项的作用：
这个选项允许链接器忽略没有用到的动态库。
打开这个选项的常见问题是，

查看一个so文件的依赖库情况
```
teddy@teddy-ubuntu:/usr/lib$ readelf -d ./i386-linux-gnu/libm.so

Dynamic section at offset 0x4aec0 contains 30 entries:
  标记        类型                         名称/值
 0x00000001 (NEEDED)                     共享库：[libc.so.6]
 0x00000001 (NEEDED)                     共享库：[ld-linux.so.2]
 0x0000000e (SONAME)                     Library soname: [libm.so.6]
```
或者用ldd
```
teddy@teddy-ubuntu:/usr/lib$ ldd  ./i386-linux-gnu/libm.so
        linux-gate.so.1 =>  (0xb7791000)
        libc.so.6 => /lib/i386-linux-gnu/libc.so.6 (0xb756c000)
        /lib/ld-linux.so.2 (0x80071000)
```
load动态库的过程就是符号重定位，然后合并到全局符号表。

gcc链接库的顺序是安装从左到右的顺序来的，符合人的一般习惯。但是链接成动态库会稍为不同。
根据`-L`指定的目录，用最先找到的，后面的同名库被忽略。

如果是链接主程序的o文件和静态库，不能定位地址就报undefined reference to xxx。
如果是链接主程序的o文件和动态库，如果找不到对应的动态库，则报undefined symbol xxx。






