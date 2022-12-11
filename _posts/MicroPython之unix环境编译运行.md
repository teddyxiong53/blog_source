---
title: MicroPython之unix环境编译运行
date: 2018-11-28 21:54:23
tags:
	- MicroPython

---



```
cd ports/unix
make
```

会报错。

网上找了下，说要安装这个。

```
sudo apt-get install python-cffi
```

安装了，还是报错。

在安装这个。

```
sudo apt-get install libffi-dev
```

还是不行，看readme的，是需要用git命令操作一下，我还是git clone下来处理吧。

执行：

```
git submodule update --init
```

这个是会下载其他的几个开源项目的代码。

然后在ports/unix下面编译就可以了。

我现在比较关注的upip的使用。

```
./micropython -m upip install micropython-pystone
```

```
teddy@teddy-ubuntu:~/work/micropython/micropython/ports/unix$ ./micropython -m upip install micropython-pystone
Installing to: /home/teddy/.micropython/lib/
Warning: pypi.org SSL certificate is not validated
Installing micropython-pystone 3.4.2-2 from https://files.pythonhosted.org/packages/13/00/8f7c7ab316e8850ea3273956e1370d008cfd36697dec2492388d3b000335/micropython-pystone-3.4.2-2.tar.gz
```

测试模块：

```
teddy@teddy-ubuntu:~/work/micropython/micropython/ports/unix$ ./micropython -m pystone
Pystone(1.2) time for 50000 passes = 0.357
This machine benchmarks at 140056 pystones/second
```



下载的文件放在~/.micropython/lib目录下，就是一个pystone.py。

```
>>> import pystone
>>> dir(pystone)
['__class__', '__file__', '__name__', 'clock', 'main', 'LOOPS', '__version__', 'Ident1', 'Ident2', 'Ident3', 'Ident4', 'Ident5', 'Record', 'TRUE', 'FALSE', 'pystones', 'Proc0', 'IntGlob', 'BoolGlob', 'Char1Glob', 'Char2Glob', 'Array1Glob', 'Array2Glob', 'PtrGlb', 'PtrGlbNext', 'Proc5', 'Proc4', 'Func2', 'Proc7', 'Proc8', 'Proc1', 'Func1', 'Proc6', 'Proc2', 'Proc3', 'Func3']
>>> print pystone.__file__
Traceback (most recent call last):
  File "<stdin>", line 1
SyntaxError: invalid syntax
>>> print(pystone.__file__)
/home/hlxiong/.micropython/lib/pystone.py
>>> 
```



upip的代码在这里，我们看一下。

https://github.com/micropython/micropython-lib/tree/master/upip



查看帮助信息。

```
hlxiong@hlxiong-VirtualBox:~/work/study/micropython-github/micropython/ports/unix$ ./micropython -m upip -h
upip - Simple PyPI package manager for MicroPython
Usage: micropython -m upip install [-p <path>] <package>... | -r <requirements.txt>
import upip; upip.install(package_or_list, [<path>])

If <path> is not given, packages will be installed into sys.path[1]
(can be set from MICROPYPATH environment variable, if current system
supports that).
Current value of sys.path[1]: /home/hlxiong/.micropython/lib

Note: only MicroPython packages (usually, named micropython-*) are supported
for installation, upip does not support arbitrary code in setup.py.
```



我现在有个疑问，upip，是micropython默认带了吗？不然怎么直接就看以用呢？

搜索一下。在这里。

```
./ports/unix/modules/upip.py
```

而且这个目录下，就只有upip的。这个就算是随mp一起的基本工具。

就如此pip对于python一样。

另外，还有库是用C语言的写，例如usocket的。

```
./ports/unix/modusocket.c
```

用C语言写的模块还有：一共9个。

```
modffi.c  
modjni.c  
modmachine.c 
modos.c 
modtermios.c
modtime.c 
moduos_vfs.c 
moduselect.c
modusocket.c
```

还有一些库是在extmod目录下。例如ssl的。

```
./micropython/extmod/modussl_mbedtls.c
```



pypi是python package index的缩写。

upip下载，是解析一个json文件。url是这么拼出来的。

以下载包pystone为例。

```
https://pypi.org/pypi/micropyton-pystone/json
```

这个url上就是一个json文件。

这个只有2个版本，一个是3.4.2-1，一个是3.4.2-2 。默认是下载3.4.2-2的。

对应的地址是：

```
"url": "https://files.pythonhosted.org/packages/13/00/8f7c7ab316e8850ea3273956e1370d008cfd36697dec2492388d3b000335/micropython-pystone-3.4.2-2.tar.gz"
```



# 在我的LAC项目里集成micropython并测试

使用minimal的配置。然后把需要的文件提取出来。

用autotols组织编译。

mpconfig.h

```
1、定义版本号。
2、包含mpconfigport.h
3、
```

mpconfigport.h

```
#include "mpconfigvariant.h"
	这个只有几十行，是一些开关，目前是合理的。
	
然后是一些配置项，uint8等数据类型定义。
```



目前出错，看起来是这个宏定义没有。

MICROPY_PLATFORM_COMPILER

moduplatform.h 这个里面有定义。看看谁包含了这个头文件。

pyexec这个文件不用。还是要严格按照minimal的编译打印的文件名进行添加。

多了的文件会有错误，而且没有必要。

mp_type_bytearray 现在是这个找不到定义。

这个是blockdev文件里的。去掉这个就好了。

```

teddy@teddy-VirtualBox:~/work/test/micropython/ports/unix$ make
Use make V=1 or set BUILD_VERBOSE in your environment to increase build verbosity.
mkdir -p build-minimal/genhdr
GEN build-minimal/genhdr/mpversion.h
GEN build-minimal/genhdr/qstr.i.last
GEN build-minimal/genhdr/qstr.split
GEN build-minimal/genhdr/qstrdefs.collected.h
QSTR updated
GEN build-minimal/genhdr/qstrdefs.generated.h
GEN build-minimal/genhdr/moduledefs.split
GEN build-minimal/genhdr/moduledefs.collected
Module registrations updated
GEN build-minimal/genhdr/moduledefs.h
GEN build-minimal/genhdr/root_pointers.split
GEN build-minimal/genhdr/root_pointers.collected
Root pointer registrations updated
GEN build-minimal/genhdr/root_pointers.h
GEN build-minimal/genhdr/compressed.split
GEN build-minimal/genhdr/compressed.collected
Compressed data updated
GEN build-minimal/genhdr/compressed.data.h
mkdir -p build-minimal/extmod/
mkdir -p build-minimal/py/
mkdir -p build-minimal/shared/libc/
mkdir -p build-minimal/shared/runtime/
mkdir -p build-minimal/shared/timeutils/
CC ../../py/mpstate.c
CC ../../py/nlr.c
CC ../../py/nlrx86.c
CC ../../py/nlrx64.c
CC ../../py/nlrthumb.c
CC ../../py/nlraarch64.c
CC ../../py/nlrpowerpc.c
CC ../../py/nlrxtensa.c
CC ../../py/nlrsetjmp.c
CC ../../py/malloc.c
CC ../../py/gc.c
CC ../../py/pystack.c
CC ../../py/qstr.c
CC ../../py/vstr.c
CC ../../py/mpprint.c
CC ../../py/unicode.c
CC ../../py/mpz.c
CC ../../py/reader.c
CC ../../py/lexer.c
CC ../../py/parse.c
CC ../../py/scope.c
CC ../../py/compile.c
CC ../../py/emitcommon.c
CC ../../py/emitbc.c
CC ../../py/asmbase.c
CC ../../py/asmx64.c
CC ../../py/emitnx64.c
CC ../../py/asmx86.c
CC ../../py/emitnx86.c
CC ../../py/asmthumb.c
CC ../../py/emitnthumb.c
CC ../../py/emitinlinethumb.c
CC ../../py/asmarm.c
CC ../../py/emitnarm.c
CC ../../py/asmxtensa.c
CC ../../py/emitnxtensa.c
CC ../../py/emitinlinextensa.c
CC ../../py/emitnxtensawin.c
CC ../../py/formatfloat.c
CC ../../py/parsenumbase.c
CC ../../py/parsenum.c
CC ../../py/emitglue.c
CC ../../py/persistentcode.c
CC ../../py/runtime.c
CC ../../py/runtime_utils.c
CC ../../py/scheduler.c
CC ../../py/nativeglue.c
CC ../../py/pairheap.c
CC ../../py/ringbuf.c
CC ../../py/stackctrl.c
CC ../../py/argcheck.c
CC ../../py/warning.c
CC ../../py/profile.c
CC ../../py/map.c
CC ../../py/obj.c
CC ../../py/objarray.c
CC ../../py/objattrtuple.c
CC ../../py/objbool.c
CC ../../py/objboundmeth.c
CC ../../py/objcell.c
CC ../../py/objclosure.c
CC ../../py/objcomplex.c
CC ../../py/objdeque.c
CC ../../py/objdict.c
CC ../../py/objenumerate.c
CC ../../py/objexcept.c
CC ../../py/objfilter.c
CC ../../py/objfloat.c
CC ../../py/objfun.c
CC ../../py/objgenerator.c
CC ../../py/objgetitemiter.c
CC ../../py/objint.c
CC ../../py/objint_longlong.c
CC ../../py/objint_mpz.c
CC ../../py/objlist.c
CC ../../py/objmap.c
CC ../../py/objmodule.c
CC ../../py/objobject.c
CC ../../py/objpolyiter.c
CC ../../py/objproperty.c
CC ../../py/objnone.c
CC ../../py/objnamedtuple.c
CC ../../py/objrange.c
CC ../../py/objreversed.c
CC ../../py/objset.c
CC ../../py/objsingleton.c
CC ../../py/objslice.c
CC ../../py/objstr.c
CC ../../py/objstrunicode.c
CC ../../py/objstringio.c
CC ../../py/objtuple.c
CC ../../py/objtype.c
CC ../../py/objzip.c
CC ../../py/opmethods.c
CC ../../py/sequence.c
CC ../../py/stream.c
CC ../../py/binary.c
CC ../../py/builtinimport.c
CC ../../py/builtinevex.c
CC ../../py/builtinhelp.c
CC ../../py/modarray.c
CC ../../py/modbuiltins.c
CC ../../py/modcollections.c
CC ../../py/modgc.c
CC ../../py/modio.c
CC ../../py/modmath.c
CC ../../py/modcmath.c
CC ../../py/modmicropython.c
CC ../../py/modstruct.c
CC ../../py/modsys.c
CC ../../py/moduerrno.c
CC ../../py/modthread.c
CC ../../py/vm.c
CC ../../py/bc.c
CC ../../py/showbc.c
CC ../../py/repl.c
CC ../../py/smallint.c
CC ../../py/frozenmod.c
CC ../../extmod/machine_bitstream.c
CC ../../extmod/machine_i2c.c
CC ../../extmod/machine_mem.c
CC ../../extmod/machine_pinbase.c
CC ../../extmod/machine_pulse.c
CC ../../extmod/machine_pwm.c
CC ../../extmod/machine_signal.c
CC ../../extmod/machine_spi.c
CC ../../extmod/modbluetooth.c
CC ../../extmod/modbtree.c
CC ../../extmod/modframebuf.c
CC ../../extmod/modlwip.c
CC ../../extmod/modnetwork.c
CC ../../extmod/modonewire.c
CC ../../extmod/moduasyncio.c
CC ../../extmod/modubinascii.c
CC ../../extmod/moducryptolib.c
CC ../../extmod/moductypes.c
CC ../../extmod/moduhashlib.c
CC ../../extmod/moduheapq.c
CC ../../extmod/modujson.c
CC ../../extmod/moduos.c
CC ../../extmod/moduplatform.c
CC ../../extmod/modurandom.c
CC ../../extmod/modure.c
CC ../../extmod/moduselect.c
CC ../../extmod/modusocket.c
CC ../../extmod/modussl_axtls.c
CC ../../extmod/modussl_mbedtls.c
CC ../../extmod/modutimeq.c
CC ../../extmod/moduwebsocket.c
CC ../../extmod/moduzlib.c
CC ../../extmod/modwebrepl.c
CC ../../extmod/network_cyw43.c
CC ../../extmod/network_ninaw10.c
CC ../../extmod/network_wiznet5k.c
CC ../../extmod/uos_dupterm.c
CC ../../extmod/utime_mphal.c
CC ../../extmod/vfs.c
CC ../../extmod/vfs_blockdev.c
CC ../../extmod/vfs_fat.c
CC ../../extmod/vfs_fat_diskio.c
CC ../../extmod/vfs_fat_file.c
CC ../../extmod/vfs_lfs.c
CC ../../extmod/vfs_posix.c
CC ../../extmod/vfs_posix_file.c
CC ../../extmod/vfs_reader.c
CC ../../extmod/virtpin.c
CC ../../shared/libc/abort_.c
CC ../../shared/libc/printf.c
CC main.c
CC gccollect.c
CC unix_mphal.c
CC mpthreadport.c
CC input.c
CC modmachine.c
CC modtime.c
CC moduselect.c
CC alloc.c
CC fatfs_port.c
CC mpbthciport.c
CC mpbtstackport_common.c
CC mpbtstackport_h4.c
CC mpbtstackport_usb.c
CC mpnimbleport.c
CC modtermios.c
CC modusocket.c
CC modffi.c
CC modjni.c
CC ../../shared/runtime/gchelper_generic.c
CC ../../shared/timeutils/timeutils.c
LINK build-minimal/micropython
   text    data     bss     dec     hex filename
 176848   14984    5328  197160   30228 build-minimal/micropython
teddy@teddy-VirtualBox:~/work/test/micropython/ports/unix$ 
```

https://github.com/teddyxiong53/lac/tree/main/micropython

现在编译出来了。

可以import sys。

但是为什么没有os的呢？

难道minimal配置连os模块都没有打开？

先把当前编译进来的文件都统一分析一遍。

我的目录是这样放的：

```
extmod
genhdr
py
shared
unix
```

先从unix目录开始看。

## unix目录

我编译了这些文件。

```
unix/alloc.c                  \
unix/coverage.c               \
unix/gccollect.c              \
unix/input.c                  \
unix/main.c                   \
unix/modffi.c                 \
unix/modjni.c                 \
unix/modmachine.c             \
unix/modtermios.c             \
unix/modtime.c                \
unix/moduos.c                 \
unix/moduselect.c             \
unix/modusocket.c             \
unix/mpthreadport.c           \
unix/unix_mphal.c   \
```

```
alloc.c
	MICROPY_EMIT_NATIVE 这个没有定义。所以这个文件等于空的。
coverage.c  
	等于空的。
gccollect.c 
	有用。
	里面就一个gc_collect函数。
input.c
	MICROPY_USE_READLINE 没有定义。
main.c
	main函数在这里。入口。
modffi.c 
	相当于空的。
modjni.c 
	空的。
modmachine.c   
	空的。
modtermios.c 
	空的。
modtime.c

```

unix/mpconfigport.mk

这个里面还是配置了一些的。但是我应该是相当于都没有用。

我试了官方代码编译的minimal的，os和time也是没有的。

是因为要通过uos这样的名字来引入。

## 进一步完善

但是当前没有json。

我至少要可以用mpy把jsonrpc client实现。

```
// Enable just the sys and os built-in modules.
#define MICROPY_PY_SYS (1)
#define MICROPY_PY_UOS (1)
```

目前在micropython\unix\mpconfigvariant.h里，确实只使能了这2个内置模块。

我要把其他需要的也使能。

看看这个的配置。

./ports/qemu-arm/mpconfigport.h

我直接拷贝一些内容进去，会报这些错误，估计是qstr那些没有包括这个。

```
py/modio.c:206:50: error: ‘MP_QSTR_uio’ undeclared here (not in a function); did you mean ‘MP_QSTR_uos’?
  206 |     { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_uio) },
      |                                                  ^~~~~~~~~~~
```

我需要先生成下standard的配置文件。然后从里面挑选一些配置出来。

还是需要把官方版本的编译配置过程看懂。

不然直接改配置是不行的。

ports\unix\variants 这个下面放了不同配置的mk文件。

例如minimal和standard。



MICROPY_PY_BUILTINS_STR_OP_MODULO

这个宏的作用是什么？

加上这个宏定义为1.

现在至少编译过了。

现在是连接找不到符号。

```
/usr/bin/ld: py/objmodule.o:(.data.rel.ro+0x8): undefined reference to `mp_module_btree'
/usr/bin/ld: py/objmodule.o:(.data.rel.ro+0x28): undefined reference to `mp_module_cmath'
/usr/bin/ld: py/objmodule.o:(.data.rel.ro+0x38): undefined reference to `mp_module_ffi'
```



当前我这个折腾出这个多问题，都是因为我是先在windows下弄的。

导致软件异常了。

变成了普通文件。所以btree依赖的berkeley db编译出现问题。

所以我才去编译minimal版本。才发现功能很少，才又回过头来编译standard版本。

还是要直接在

## 正常的代码编译

```
teddy@teddy-VirtualBox:~/work/test/mpy-code/micropython-1.19/ports/unix$ make
Use make V=1 or set BUILD_VERBOSE in your environment to increase build verbosity.
mkdir -p build-standard/genhdr
GEN build-standard/genhdr/mpversion.h
GEN build-standard/genhdr/qstr.i.last
GEN build-standard/genhdr/qstr.split
GEN build-standard/genhdr/qstrdefs.collected.h
QSTR updated
GEN build-standard/genhdr/qstrdefs.generated.h
GEN build-standard/genhdr/moduledefs.split
GEN build-standard/genhdr/moduledefs.collected
Module registrations updated
GEN build-standard/genhdr/moduledefs.h
mkdir -p build-standard/build-standard/
mkdir -p build-standard/extmod/
mkdir -p build-standard/lib/axtls/crypto/
mkdir -p build-standard/lib/axtls/ssl/
mkdir -p build-standard/lib/berkeley-db-1.xx/btree/
mkdir -p build-standard/lib/berkeley-db-1.xx/mpool/
mkdir -p build-standard/py/
mkdir -p build-standard/shared/libc/
mkdir -p build-standard/shared/readline/
mkdir -p build-standard/shared/runtime/
mkdir -p build-standard/shared/timeutils/
CC ../../py/mpstate.c
CC ../../py/nlr.c
CC ../../py/nlrx86.c
CC ../../py/nlrx64.c
CC ../../py/nlrthumb.c
CC ../../py/nlraarch64.c
CC ../../py/nlrpowerpc.c
CC ../../py/nlrxtensa.c
CC ../../py/nlrsetjmp.c
CC ../../py/malloc.c
CC ../../py/gc.c
CC ../../py/pystack.c
CC ../../py/qstr.c
CC ../../py/vstr.c
CC ../../py/mpprint.c
CC ../../py/unicode.c
CC ../../py/mpz.c
CC ../../py/reader.c
CC ../../py/lexer.c
CC ../../py/parse.c
CC ../../py/scope.c
CC ../../py/compile.c
CC ../../py/emitcommon.c
CC ../../py/emitbc.c
CC ../../py/asmbase.c
CC ../../py/asmx64.c
CC ../../py/emitnx64.c
CC ../../py/asmx86.c
CC ../../py/emitnx86.c
CC ../../py/asmthumb.c
CC ../../py/emitnthumb.c
CC ../../py/emitinlinethumb.c
CC ../../py/asmarm.c
CC ../../py/emitnarm.c
CC ../../py/asmxtensa.c
CC ../../py/emitnxtensa.c
CC ../../py/emitinlinextensa.c
CC ../../py/emitnxtensawin.c
CC ../../py/formatfloat.c
CC ../../py/parsenumbase.c
CC ../../py/parsenum.c
CC ../../py/emitglue.c
CC ../../py/persistentcode.c
CC ../../py/runtime.c
CC ../../py/runtime_utils.c
CC ../../py/scheduler.c
CC ../../py/nativeglue.c
CC ../../py/pairheap.c
CC ../../py/ringbuf.c
CC ../../py/stackctrl.c
CC ../../py/argcheck.c
CC ../../py/warning.c
CC ../../py/profile.c
CC ../../py/map.c
CC ../../py/obj.c
CC ../../py/objarray.c
CC ../../py/objattrtuple.c
CC ../../py/objbool.c
CC ../../py/objboundmeth.c
CC ../../py/objcell.c
CC ../../py/objclosure.c
CC ../../py/objcomplex.c
CC ../../py/objdeque.c
CC ../../py/objdict.c
CC ../../py/objenumerate.c
CC ../../py/objexcept.c
CC ../../py/objfilter.c
CC ../../py/objfloat.c
CC ../../py/objfun.c
CC ../../py/objgenerator.c
CC ../../py/objgetitemiter.c
CC ../../py/objint.c
CC ../../py/objint_longlong.c
CC ../../py/objint_mpz.c
CC ../../py/objlist.c
CC ../../py/objmap.c
CC ../../py/objmodule.c
CC ../../py/objobject.c
CC ../../py/objpolyiter.c
CC ../../py/objproperty.c
CC ../../py/objnone.c
CC ../../py/objnamedtuple.c
CC ../../py/objrange.c
CC ../../py/objreversed.c
CC ../../py/objset.c
CC ../../py/objsingleton.c
CC ../../py/objslice.c
CC ../../py/objstr.c
CC ../../py/objstrunicode.c
CC ../../py/objstringio.c
CC ../../py/objtuple.c
CC ../../py/objtype.c
CC ../../py/objzip.c
CC ../../py/opmethods.c
CC ../../py/sequence.c
CC ../../py/stream.c
CC ../../py/binary.c
CC ../../py/builtinimport.c
CC ../../py/builtinevex.c
CC ../../py/builtinhelp.c
CC ../../py/modarray.c
CC ../../py/modbuiltins.c
CC ../../py/modcollections.c
CC ../../py/modgc.c
CC ../../py/modio.c
CC ../../py/modmath.c
CC ../../py/modcmath.c
CC ../../py/modmicropython.c
CC ../../py/modstruct.c
CC ../../py/modsys.c
CC ../../py/moduerrno.c
CC ../../py/modthread.c
CC ../../py/vm.c
CC ../../py/bc.c
CC ../../py/showbc.c
CC ../../py/repl.c
CC ../../py/smallint.c
CC ../../py/frozenmod.c
CC ../../extmod/moduasyncio.c
CC ../../extmod/moductypes.c
CC ../../extmod/modujson.c
CC ../../extmod/moduos.c
CC ../../extmod/modure.c
CC ../../extmod/moduzlib.c
CC ../../extmod/moduheapq.c
CC ../../extmod/modutimeq.c
CC ../../extmod/moduhashlib.c
CC ../../extmod/moducryptolib.c
CC ../../extmod/modubinascii.c
CC ../../extmod/virtpin.c
CC ../../extmod/machine_bitstream.c
CC ../../extmod/machine_mem.c
CC ../../extmod/machine_pinbase.c
CC ../../extmod/machine_signal.c
CC ../../extmod/machine_pulse.c
CC ../../extmod/machine_pwm.c
CC ../../extmod/machine_i2c.c
CC ../../extmod/machine_spi.c
CC ../../extmod/modbluetooth.c
CC ../../extmod/modussl_axtls.c
CC ../../extmod/modussl_mbedtls.c
CC ../../extmod/moduplatform.c
CC ../../extmod/modurandom.c
CC ../../extmod/moduselect.c
CC ../../extmod/moduwebsocket.c
CC ../../extmod/modwebrepl.c
CC ../../extmod/modframebuf.c
CC ../../extmod/vfs.c
CC ../../extmod/vfs_blockdev.c
CC ../../extmod/vfs_reader.c
CC ../../extmod/vfs_posix.c
CC ../../extmod/vfs_posix_file.c
CC ../../extmod/vfs_fat.c
CC ../../extmod/vfs_fat_diskio.c
CC ../../extmod/vfs_fat_file.c
CC ../../extmod/vfs_lfs.c
CC ../../extmod/utime_mphal.c
CC ../../extmod/uos_dupterm.c
CC ../../shared/libc/abort_.c
CC ../../shared/libc/printf.c
make -C ../../mpy-cross/
make[1]: 进入目录“/home/teddy/work/test/mpy-code/micropython-1.19/mpy-cross”
Use make V=1 or set BUILD_VERBOSE in your environment to increase build verbosity.
mkdir -p build/genhdr
GEN build/genhdr/mpversion.h
GEN build/genhdr/qstr.i.last
GEN build/genhdr/qstr.split
GEN build/genhdr/qstrdefs.collected.h
QSTR updated
GEN build/genhdr/qstrdefs.generated.h
GEN build/genhdr/moduledefs.split
GEN build/genhdr/moduledefs.collected
Module registrations updated
GEN build/genhdr/moduledefs.h
mkdir -p build/py/
mkdir -p build/shared/runtime/
CC ../py/mpstate.c
CC ../py/nlr.c
CC ../py/nlrx86.c
CC ../py/nlrx64.c
CC ../py/nlrthumb.c
CC ../py/nlraarch64.c
CC ../py/nlrpowerpc.c
CC ../py/nlrxtensa.c
CC ../py/nlrsetjmp.c
CC ../py/malloc.c
CC ../py/gc.c
CC ../py/pystack.c
CC ../py/qstr.c
CC ../py/vstr.c
CC ../py/mpprint.c
CC ../py/unicode.c
CC ../py/mpz.c
CC ../py/reader.c
CC ../py/lexer.c
CC ../py/parse.c
CC ../py/scope.c
CC ../py/compile.c
CC ../py/emitcommon.c
CC ../py/emitbc.c
CC ../py/asmbase.c
CC ../py/asmx64.c
CC ../py/emitnx64.c
CC ../py/asmx86.c
CC ../py/emitnx86.c
CC ../py/asmthumb.c
CC ../py/emitnthumb.c
CC ../py/emitinlinethumb.c
CC ../py/asmarm.c
CC ../py/emitnarm.c
CC ../py/asmxtensa.c
CC ../py/emitnxtensa.c
CC ../py/emitinlinextensa.c
CC ../py/emitnxtensawin.c
CC ../py/formatfloat.c
CC ../py/parsenumbase.c
CC ../py/parsenum.c
CC ../py/emitglue.c
CC ../py/persistentcode.c
CC ../py/runtime.c
CC ../py/runtime_utils.c
CC ../py/scheduler.c
CC ../py/nativeglue.c
CC ../py/pairheap.c
CC ../py/ringbuf.c
CC ../py/stackctrl.c
CC ../py/argcheck.c
CC ../py/warning.c
CC ../py/profile.c
CC ../py/map.c
CC ../py/obj.c
CC ../py/objarray.c
CC ../py/objattrtuple.c
CC ../py/objbool.c
CC ../py/objboundmeth.c
CC ../py/objcell.c
CC ../py/objclosure.c
CC ../py/objcomplex.c
CC ../py/objdeque.c
CC ../py/objdict.c
CC ../py/objenumerate.c
CC ../py/objexcept.c
CC ../py/objfilter.c
CC ../py/objfloat.c
CC ../py/objfun.c
CC ../py/objgenerator.c
CC ../py/objgetitemiter.c
CC ../py/objint.c
CC ../py/objint_longlong.c
CC ../py/objint_mpz.c
CC ../py/objlist.c
CC ../py/objmap.c
CC ../py/objmodule.c
CC ../py/objobject.c
CC ../py/objpolyiter.c
CC ../py/objproperty.c
CC ../py/objnone.c
CC ../py/objnamedtuple.c
CC ../py/objrange.c
CC ../py/objreversed.c
CC ../py/objset.c
CC ../py/objsingleton.c
CC ../py/objslice.c
CC ../py/objstr.c
CC ../py/objstrunicode.c
CC ../py/objstringio.c
CC ../py/objtuple.c
CC ../py/objtype.c
CC ../py/objzip.c
CC ../py/opmethods.c
CC ../py/sequence.c
CC ../py/stream.c
CC ../py/binary.c
CC ../py/builtinimport.c
CC ../py/builtinevex.c
CC ../py/builtinhelp.c
CC ../py/modarray.c
CC ../py/modbuiltins.c
CC ../py/modcollections.c
CC ../py/modgc.c
CC ../py/modio.c
CC ../py/modmath.c
CC ../py/modcmath.c
CC ../py/modmicropython.c
CC ../py/modstruct.c
CC ../py/modsys.c
CC ../py/moduerrno.c
CC ../py/modthread.c
CC ../py/vm.c
CC ../py/bc.c
CC ../py/showbc.c
CC ../py/repl.c
CC ../py/smallint.c
CC ../py/frozenmod.c
CC main.c
CC gccollect.c
CC ../shared/runtime/gchelper_generic.c
LINK mpy-cross
   text    data     bss     dec     hex filename
 307907   17184     840  325931   4f92b mpy-cross
make[1]: 离开目录“/home/teddy/work/test/mpy-code/micropython-1.19/mpy-cross”
MPY upip.py
MPY upip_utarfile.py
GEN build-standard/frozen_content.c
CC build-standard/frozen_content.c
CC main.c
CC gccollect.c
CC unix_mphal.c
CC mpthreadport.c
CC input.c
CC modmachine.c
CC modtime.c
CC moduselect.c
CC alloc.c
CC fatfs_port.c
CC mpbthciport.c
CC mpbtstackport_common.c
CC mpbtstackport_h4.c
CC mpbtstackport_usb.c
CC mpnimbleport.c
CC ../../lib/axtls/ssl/asn1.c
CC ../../lib/axtls/ssl/loader.c
CC ../../lib/axtls/ssl/tls1.c
CC ../../lib/axtls/ssl/tls1_svr.c
CC ../../lib/axtls/ssl/tls1_clnt.c
CC ../../lib/axtls/ssl/x509.c
CC ../../lib/axtls/crypto/aes.c
CC ../../lib/axtls/crypto/bigint.c
CC ../../lib/axtls/crypto/crypto_misc.c
CC ../../lib/axtls/crypto/hmac.c
CC ../../lib/axtls/crypto/md5.c
CC ../../lib/axtls/crypto/rsa.c
CC ../../lib/axtls/crypto/sha1.c
CC ../../extmod/modbtree.c
CC ../../lib/berkeley-db-1.xx/btree/bt_close.c
CC ../../lib/berkeley-db-1.xx/btree/bt_conv.c
CC ../../lib/berkeley-db-1.xx/btree/bt_debug.c
CC ../../lib/berkeley-db-1.xx/btree/bt_delete.c
CC ../../lib/berkeley-db-1.xx/btree/bt_get.c
CC ../../lib/berkeley-db-1.xx/btree/bt_open.c
CC ../../lib/berkeley-db-1.xx/btree/bt_overflow.c
CC ../../lib/berkeley-db-1.xx/btree/bt_page.c
CC ../../lib/berkeley-db-1.xx/btree/bt_put.c
CC ../../lib/berkeley-db-1.xx/btree/bt_search.c
CC ../../lib/berkeley-db-1.xx/btree/bt_seq.c
CC ../../lib/berkeley-db-1.xx/btree/bt_split.c
CC ../../lib/berkeley-db-1.xx/btree/bt_utils.c
CC ../../lib/berkeley-db-1.xx/mpool/mpool.c
CC modtermios.c
CC modusocket.c
CC modffi.c
CC ../../shared/runtime/gchelper_generic.c
CC ../../shared/timeutils/timeutils.c
CC ../../shared/readline/readline.c
LINK micropython
   text    data     bss     dec     hex filename
 472833   53744    2256  528833   811c1 micropython
```

