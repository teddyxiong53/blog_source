---
title: gcc编译过程详细分析
date: 2018-02-02 20:12:47
tags:
	- gcc

---



下面的实验，我是要在树莓派上进行。先查看一下gcc的信息。

```
pi@raspberrypi:~$ gcc -v
Using built-in specs.
COLLECT_GCC=gcc
COLLECT_LTO_WRAPPER=/usr/lib/gcc/arm-linux-gnueabihf/4.8/lto-wrapper
Target: arm-linux-gnueabihf
Configured with: ../src/configure -v --with-pkgversion='Raspbian 4.8.4-1' --with-bugurl=file:///usr/share/doc/gcc-4.8/README.Bugs --enable-languages=c,c++,java,go,d,fortran,objc,obj-c++ --prefix=/usr --program-suffix=-4.8 --enable-shared --enable-linker-build-id --libexecdir=/usr/lib --without-included-gettext --enable-threads=posix --with-gxx-include-dir=/usr/include/c++/4.8 --libdir=/usr/lib --enable-nls --with-sysroot=/ --enable-clocale=gnu --enable-libstdcxx-debug --enable-libstdcxx-time=yes --enable-gnu-unique-object --disable-libmudflap --disable-libitm --disable-libquadmath --enable-plugin --with-system-zlib --disable-browser-plugin --enable-java-awt=gtk --enable-gtk-cairo --with-java-home=/usr/lib/jvm/java-1.5.0-gcj-4.8-armhf/jre --enable-java-home --with-jvm-root-dir=/usr/lib/jvm/java-1.5.0-gcj-4.8-armhf --with-jvm-jar-dir=/usr/lib/jvm-exports/java-1.5.0-gcj-4.8-armhf --with-arch-directory=arm --with-ecj-jar=/usr/share/java/eclipse-ecj.jar --enable-objc-gc --enable-multiarch --disable-sjlj-exceptions --with-arch=armv6 --with-fpu=vfp --with-float=hard --enable-checking=release --build=arm-linux-gnueabihf --host=arm-linux-gnueabihf --target=arm-linux-gnueabihf
Thread model: posix
gcc version 4.8.4 (Raspbian 4.8.4-1) 
```

先把上面的信息逐条分析。

1、lto是Link Time Optimize。链接时优化。

当你用gcc编译的时候，会对各个独立的c文件进行优化。

正常来说，gcc还管不到整个程序的优化，这个只有ld才能看到整个程序。

lto选项，就是让gcc可以对整个程序进行优化的。

2、gcc的目录在/usr/lib/gcc/arm-linux-gnueabihf/4.8。

这个目录的情况：

```
pi@raspberrypi:/usr/lib/gcc/arm-linux-gnueabihf/4.8$ tree
.
├── cc1
├── cc1plus
├── collect2
├── crtbegin.o
├── crtbeginS.o
├── crtbeginT.o
├── crtend.o
├── crtendS.o
├── include
│   ├── arm_neon.h
│   ├── backtrace.h
│   ├── backtrace-supported.h
│   ├── float.h
│   ├── iso646.h
│   ├── mmintrin.h
│   ├── omp.h
│   ├── stdalign.h
│   ├── stdarg.h
│   ├── stdbool.h
│   ├── stddef.h
│   ├── stdfix.h
│   ├── stdint-gcc.h
│   ├── stdint.h
│   ├── stdnoreturn.h
│   ├── unwind-arm-common.h
│   ├── unwind.h
│   └── varargs.h
├── include-fixed
│   ├── limits.h
│   ├── README
│   └── syslimits.h
├── libasan.a
├── libasan_preinit.o
├── libasan.so -> ../../../arm-linux-gnueabihf/libasan.so.0
├── libatomic.a
├── libatomic.so -> ../../../arm-linux-gnueabihf/libatomic.so.1
├── libbacktrace.a
├── libgcc.a
├── libgcc_eh.a
├── libgcc_s.so
├── libgcc_s.so.1 -> /lib/arm-linux-gnueabihf/libgcc_s.so.1
├── libgcov.a
├── libgomp.a
├── libgomp.so -> ../../../arm-linux-gnueabihf/libgomp.so.1
├── libgomp.spec
├── liblto_plugin.so -> liblto_plugin.so.0.0.0
├── liblto_plugin.so.0 -> liblto_plugin.so.0.0.0
├── liblto_plugin.so.0.0.0
├── libssp_nonshared.a
├── libstdc++.a
├── libstdc++.so -> ../../../arm-linux-gnueabihf/libstdc++.so.6
├── libsupc++.a
├── lto1
└── lto-wrapper
```

3、线程模型用的是posix。

# 编译过程用到的工具和生成的文件

test.c里面就是答应了一行“hello gcc“。

1、`gcc -E test.c`。这一步用到的是gcc。输出的是宏展开之后的样子，直接打印出来。

2、`gcc -S test.c -o test.s`。这一步用到的是内部命令cc1 。

文件内容：

```
	.arch armv6
	.eabi_attribute 27, 3
	.eabi_attribute 28, 1
	.fpu vfp
	.eabi_attribute 20, 1
	.eabi_attribute 21, 1
	.eabi_attribute 23, 3
	.eabi_attribute 24, 1
	.eabi_attribute 25, 1
	.eabi_attribute 26, 2
	.eabi_attribute 30, 6
	.eabi_attribute 34, 1
	.eabi_attribute 18, 4
	.file	"test.c"
	.section	.rodata
	.align	2
.LC0:
	.ascii	"hello gcc\000"
	.text
	.align	2
	.global	main
	.type	main, %function
main:
	@ args = 0, pretend = 0, frame = 0
	@ frame_needed = 1, uses_anonymous_args = 0
	stmfd	sp!, {fp, lr}
	add	fp, sp, #4
	ldr	r0, .L2
	bl	puts
	ldmfd	sp!, {fp, pc}
.L3:
	.align	2
.L2:
	.word	.LC0
	.size	main, .-main
	.ident	"GCC: (Raspbian 4.8.4-1) 4.8.4"
	.section	.note.GNU-stack,"",%progbits

```

3、`gcc -c test.c -o test.o `。这样得到的是o文件。实际上用到了as命令。

4、`gcc  test.c `。这样得到的就是可执行文件。实际上用到ld命令。

# elf文件

这个我另外有一篇文章《elf文件分析》，具体看这里。



# 链接

o文件和a文件都是可重定位文件。链接过程就是给他们重新定位的过程。

```
pi@raspberrypi:~/work/test/gcc$ gcc -v test.o -o test
...省略部分内容
/usr/lib/gcc/arm-linux-gnueabihf/4.8/collect2 --sysroot=/ --build-id --eh-frame-hdr -dynamic-linker /lib/ld-linux-armhf.so.3 -X --hash-style=gnu -m armelf_linux_eabi -o test /usr/lib/gcc/arm-linux-gnueabihf/4.8/../../../arm-linux-gnueabihf/crt1.o /usr/lib/gcc/arm-linux-gnueabihf/4.8/../../../arm-linux-gnueabihf/crti.o /usr/lib/gcc/arm-linux-gnueabihf/4.8/crtbegin.o -L/usr/lib/gcc/arm-linux-gnueabihf/4.8 -L/usr/lib/gcc/arm-linux-gnueabihf/4.8/../../../arm-linux-gnueabihf -L/usr/lib/gcc/arm-linux-gnueabihf/4.8/../../.. -L/lib/arm-linux-gnueabihf -L/usr/lib/arm-linux-gnueabihf test.o -lgcc --as-needed -lgcc_s --no-as-needed -lc -lgcc --as-needed -lgcc_s --no-as-needed /usr/lib/gcc/arm-linux-gnueabihf/4.8/crtend.o /usr/lib/gcc/arm-linux-gnueabihf/4.8/../../../arm-linux-gnueabihf/crtn.o
```

从这里看出，参与链接的，除了test.o，还有crti.o、crtbegin.o、crtend.o、crtn.o。还有c库，gcc的库。

crt是C Runtime的意思。

crtbegin和crtend是给c++用的。

crti和crto是进入和退出清理用的。