---
title: micropython（1）
date: 2018-11-28 13:52:28
tags:
	- Python

---

--

# 资源

novaspirit的视频，用micropython在树莓派pico上运行ssd1306的显示。

IDE的方式进行编程和下载代码。

https://www.youtube.com/watch?v=YR9v04qzJ5E



这个系列文章看起来不错。但是是付费专栏。

https://blog.csdn.net/zhangzhechun/category_12622842.html

这个专栏不收费，看起来也不错。

https://blog.csdn.net/superatom01/category_12386277.html





## IDE使用

- [Mu Editor](https://randomnerdtutorials.com/micropython-ides-esp32-esp8266/#mu-editor)
- [uPyCraft IDE](https://randomnerdtutorials.com/micropython-ides-esp32-esp8266/#upycraft-ide)
- [Thonny IDE](https://randomnerdtutorials.com/micropython-ides-esp32-esp8266/#thonny-ide)
- [VS Code + Pymakr extension](https://randomnerdtutorials.com/micropython-ides-esp32-esp8266/#VS-Code)
- [PyCharm](https://randomnerdtutorials.com/micropython-ides-esp32-esp8266/#pycharm)
- [microIDE](https://randomnerdtutorials.com/micropython-ides-esp32-esp8266/#microide)



现在从头开始学习micropython，看看是如何实现的。

我从buildroot里拷贝下载的代码，micropython-1.8.7这个版本。

解压代码，进入到minimals目录，输入：

```
make
```

报错了。

```
/usr/include/features.h:367:25: fatal error: sys/cdefs.h: 没有那个文件或目录
```

解决办法：

```
sudo apt install libc6-dev-i386
```

然后编译通过。

运行：输入make run就可以了。

```
hlxiong@hlxiong-VirtualBox:~/work/study/micropython-1.8.7/minimal$ make run
Use make V=1 or set BUILD_VERBOSE in your environment to increase build verbosity.
stty raw opost -echo
build/firmware.elf
MicroPython v1.8.7 on 2018-11-28; minimal with unknown-cpu
Type "help()" for more information.
>>> 
```

内置模块定义在这里：在py/objmodule.c里。

```
STATIC const mp_rom_map_elem_t mp_builtin_module_table[] = {
    { MP_ROM_QSTR(MP_QSTR___main__), MP_ROM_PTR(&mp_module___main__) },
    { MP_ROM_QSTR(MP_QSTR_builtins), MP_ROM_PTR(&mp_module_builtins) },
    { MP_ROM_QSTR(MP_QSTR_micropython), MP_ROM_PTR(&mp_module_micropython) },

#if MICROPY_PY_ARRAY
    { MP_ROM_QSTR(MP_QSTR_array), MP_ROM_PTR(&mp_module_array) },
#endif
#if MICROPY_PY_IO
    { MP_ROM_QSTR(MP_QSTR_uio), MP_ROM_PTR(&mp_module_io) },
#endif
#if MICROPY_PY_COLLECTIONS
    { MP_ROM_QSTR(MP_QSTR_ucollections), MP_ROM_PTR(&mp_module_collections) },
#endif
#if MICROPY_PY_STRUCT
    { MP_ROM_QSTR(MP_QSTR_ustruct), MP_ROM_PTR(&mp_module_ustruct) },
#endif

#if MICROPY_PY_BUILTINS_FLOAT
#if MICROPY_PY_MATH
    { MP_ROM_QSTR(MP_QSTR_math), MP_ROM_PTR(&mp_module_math) },
#endif
#if MICROPY_PY_BUILTINS_COMPLEX && MICROPY_PY_CMATH
    { MP_ROM_QSTR(MP_QSTR_cmath), MP_ROM_PTR(&mp_module_cmath) },
#endif
#endif
#if MICROPY_PY_SYS
    { MP_ROM_QSTR(MP_QSTR_sys), MP_ROM_PTR(&mp_module_sys) },
#endif
#if MICROPY_PY_GC && MICROPY_ENABLE_GC
    { MP_ROM_QSTR(MP_QSTR_gc), MP_ROM_PTR(&mp_module_gc) },
#endif
#if MICROPY_PY_THREAD
    { MP_ROM_QSTR(MP_QSTR__thread), MP_ROM_PTR(&mp_module_thread) },
#endif

    // extmod modules

#if MICROPY_PY_UERRNO
    { MP_ROM_QSTR(MP_QSTR_uerrno), MP_ROM_PTR(&mp_module_uerrno) },
#endif
#if MICROPY_PY_UCTYPES
    { MP_ROM_QSTR(MP_QSTR_uctypes), MP_ROM_PTR(&mp_module_uctypes) },
#endif
#if MICROPY_PY_UZLIB
    { MP_ROM_QSTR(MP_QSTR_uzlib), MP_ROM_PTR(&mp_module_uzlib) },
#endif
#if MICROPY_PY_UJSON
    { MP_ROM_QSTR(MP_QSTR_ujson), MP_ROM_PTR(&mp_module_ujson) },
#endif
#if MICROPY_PY_URE
    { MP_ROM_QSTR(MP_QSTR_ure), MP_ROM_PTR(&mp_module_ure) },
#endif
#if MICROPY_PY_UHEAPQ
    { MP_ROM_QSTR(MP_QSTR_uheapq), MP_ROM_PTR(&mp_module_uheapq) },
#endif
#if MICROPY_PY_UTIMEQ
    { MP_ROM_QSTR(MP_QSTR_utimeq), MP_ROM_PTR(&mp_module_utimeq) },
#endif
#if MICROPY_PY_UHASHLIB
    { MP_ROM_QSTR(MP_QSTR_uhashlib), MP_ROM_PTR(&mp_module_uhashlib) },
#endif
#if MICROPY_PY_UBINASCII
    { MP_ROM_QSTR(MP_QSTR_ubinascii), MP_ROM_PTR(&mp_module_ubinascii) },
#endif
#if MICROPY_PY_URANDOM
    { MP_ROM_QSTR(MP_QSTR_urandom), MP_ROM_PTR(&mp_module_urandom) },
#endif
#if MICROPY_PY_USELECT
    { MP_ROM_QSTR(MP_QSTR_uselect), MP_ROM_PTR(&mp_module_uselect) },
#endif
#if MICROPY_PY_USSL
    { MP_ROM_QSTR(MP_QSTR_ussl), MP_ROM_PTR(&mp_module_ussl) },
#endif
#if MICROPY_PY_LWIP
    { MP_ROM_QSTR(MP_QSTR_lwip), MP_ROM_PTR(&mp_module_lwip) },
#endif
#if MICROPY_PY_WEBSOCKET
    { MP_ROM_QSTR(MP_QSTR_websocket), MP_ROM_PTR(&mp_module_websocket) },
#endif
#if MICROPY_PY_WEBREPL
    { MP_ROM_QSTR(MP_QSTR__webrepl), MP_ROM_PTR(&mp_module_webrepl) },
#endif
#if MICROPY_PY_FRAMEBUF
    { MP_ROM_QSTR(MP_QSTR_framebuf), MP_ROM_PTR(&mp_module_framebuf) },
#endif
#if MICROPY_PY_BTREE
    { MP_ROM_QSTR(MP_QSTR_btree), MP_ROM_PTR(&mp_module_btree) },
#endif

    // extra builtin modules as defined by a port
    MICROPY_PORT_BUILTIN_MODULES
};
```



我们看看sys这个内置模块。

```
STATIC MP_DEFINE_CONST_DICT(mp_module_sys_globals, mp_module_sys_globals_table);

const mp_obj_module_t mp_module_sys = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t*)&mp_module_sys_globals,
};
```

我们就先看version_info这个属性的。

```
STATIC const MP_DEFINE_STR_OBJ(version_obj, "3.4.0");
```

mp_execute_bytecode这个函数是最主要的解析函数。



# 在rt-thread里进行实验

我搭建的rt-thread环境，适合用来调试micropython的代码。

改了配置后，需要在bsp/qemu-vexpress-a9里执行，pkgs --update命令。才会把包下载下来并解压放好。

先把目录结构看一下。

```
hlxiong@hlxiong-VirtualBox:~/work/study/rtt/rt-thread/bsp/qemu-vexpress-a9/packages/micropython-latest$ tree -L 1
.
├── docs：都是markdown写的文档，值得看一下。
├── drivers
├── extmod：不管。
├── lib
├── LICENSE
├── port：这个是重点要看的。
├── py：重点。
├── README.md
└── SConscript
```

还是从入口函数mpy_main开始看，这个是注册的一个msh命令。

```
static void python(uint8_t argc, char **argv) {
    if (argc > 1) {
        mpy_main(argv[1]);
    } else {
        mpy_main(NULL);
    }
}
MSH_CMD_EXPORT(python, MicroPython: `python [file.py]` execute python script);
```



首先需要弄清楚qstr这个概念。

qstr是什么？起什么作用？

还是需要看一下编译过程。

当前rt-thread的移植版本，qstr没有生成过程。

是已经生成好的了。

最核心的结构体。

```
typedef struct _mp_state_ctx_t {
    mp_state_thread_t thread;
    mp_state_vm_t vm;
    mp_state_mem_t mem;
} mp_state_ctx_t;
```



基础类型

list：objlist.h和objlist.c。

map：

dict：



配置文件

mpconfigport.h

mpconfig.h



各种类型的特征：

```
// A MicroPython object is a machine word having the following form:
//  - xxxx...xxx1 : a small int, bits 1 and above are the value
//  - xxxx...xx10 : a qstr, bits 2 and above are the value
//  - xxxx...xx00 : a pointer to an mp_obj_base_t (unless a fake object)
#define MICROPY_OBJ_REPR_A (0)
```

默认用的就是A这种类型。

一个对象就是一个void *指针。

```
typedef void *mp_obj_t;
typedef const void *mp_const_obj_t;
```



带不同个数参数的函数定义。

```
typedef mp_obj_t (*mp_fun_0_t)(void);
typedef mp_obj_t (*mp_fun_1_t)(mp_obj_t);
typedef mp_obj_t (*mp_fun_2_t)(mp_obj_t, mp_obj_t);
typedef mp_obj_t (*mp_fun_3_t)(mp_obj_t, mp_obj_t, mp_obj_t);
typedef mp_obj_t (*mp_fun_var_t)(size_t n, const mp_obj_t *);
```

把debug宏打开，在mpconfigport.h里修改。

有些地方，还编译不过。注释掉这些打印。

现在进入python环境。多了很多的打印。

```
msh />python
Initializing GC heap: 6010eae4..60110ae0 = 8188 bytes
GC layout:
  alloc table at 6010eae4, length 125 bytes, 500 blocks
  finaliser table at 6010eb61, length 63 bytes, 504 blocks
  pool at 6010eba0, length 8000 bytes, 500 blocks
gc_alloc(24 bytes -> 2 blocks)
gc_alloc(6010eba0)
malloc 24 : 6010eba0
gc_alloc(8 bytes -> 1 blocks)
gc_alloc(6010ebc0)
malloc 8 : 6010ebc0
gc_alloc(16 bytes -> 1 blocks)
gc_alloc(6010ebd0)
malloc 16 : 6010ebd0
gc_alloc(16 bytes -> 1 blocks)
gc_alloc(6010ebe0)
malloc 16 : 6010ebe0
gc_alloc(11 bytes -> 1 blocks)
gc_alloc(6010ebf0)
malloc 11 : 6010ebf0
gc_alloc(16 bytes -> 1 blocks)
gc_alloc(6010ec00)
malloc 16 : 6010ec00

gc_alloc(32 bytes -> 2 blocks)
gc_alloc(6010ec10)
malloc 32 : 6010ec10
MicroPython v1.9.3-477-g7b0a020-dirty on 2018-03-21; Universal python platform with RT-Thread
Type "help()" for more information.
```



定义的各种异常：

```
extern const mp_obj_type_t mp_type_BaseException;
extern const mp_obj_type_t mp_type_ArithmeticError;
extern const mp_obj_type_t mp_type_AssertionError;
extern const mp_obj_type_t mp_type_AttributeError;
extern const mp_obj_type_t mp_type_EOFError;
extern const mp_obj_type_t mp_type_Exception;
extern const mp_obj_type_t mp_type_GeneratorExit;
extern const mp_obj_type_t mp_type_ImportError;
extern const mp_obj_type_t mp_type_IndentationError;
extern const mp_obj_type_t mp_type_IndexError;
extern const mp_obj_type_t mp_type_KeyboardInterrupt;
extern const mp_obj_type_t mp_type_KeyError;
extern const mp_obj_type_t mp_type_LookupError;
extern const mp_obj_type_t mp_type_MemoryError;
extern const mp_obj_type_t mp_type_NameError;
extern const mp_obj_type_t mp_type_NotImplementedError;
extern const mp_obj_type_t mp_type_OSError;
extern const mp_obj_type_t mp_type_TimeoutError;
extern const mp_obj_type_t mp_type_OverflowError;
extern const mp_obj_type_t mp_type_RuntimeError;
extern const mp_obj_type_t mp_type_StopAsyncIteration;
extern const mp_obj_type_t mp_type_StopIteration;
extern const mp_obj_type_t mp_type_SyntaxError;
extern const mp_obj_type_t mp_type_SystemExit;
extern const mp_obj_type_t mp_type_TypeError;
extern const mp_obj_type_t mp_type_UnicodeError;
extern const mp_obj_type_t mp_type_ValueError;
extern const mp_obj_type_t mp_type_ViperTypeError;
extern const mp_obj_type_t mp_type_ZeroDivisionError;
```

使能了垃圾收集之后，把malloc这些都改了。

```
#undef malloc
#undef free
#undef realloc
#define malloc(b) gc_alloc((b), false)
#define malloc_with_finaliser(b) gc_alloc((b), true)
#define free gc_free
#define realloc(ptr, n) gc_realloc(ptr, n, true)
#define realloc_ext(ptr, n, mv) gc_realloc(ptr, n, mv)
```

执行了import sys的打印。

```
>>> import sys
gc_alloc(11 bytes -> 1 blocks)
gc_alloc(6010ec30)
malloc 11 : 6010ec30
gc_alloc(16 bytes -> 1 blocks)
gc_alloc(6010ec40)
malloc 16 : 6010ec40
gc_alloc(84 bytes -> 6 blocks)
gc_alloc(6010ec50)
malloc 84 : 6010ec50
gc_alloc(20 bytes -> 2 blocks)
gc_alloc(6010ecb0)
malloc 20 : 6010ecb0
gc_alloc(32 bytes -> 2 blocks)
gc_alloc(6010ecd0)
malloc 32 : 6010ecd0
gc_alloc(512 bytes -> 32 blocks)
gc_alloc(6010ecf0)
malloc 512 : 6010ecf0
gc_alloc(128 bytes -> 8 blocks)
gc_alloc(6010eef0)
malloc 128 : 6010eef0
gc_alloc(24 bytes -> 2 blocks)
gc_alloc(6010ef70)
malloc 24 : 6010ef70
realloc 6010ef70, 20, 1611722608 : 6010e8e0
gc_free(6010ecf0)
free 6010ecf0
gc_free(6010eef0)
free 6010eef0
gc_free(6010ec40)
free 6010ec40
gc_free(6010ecd0)
free 6010ecd0
gc_free(6010ecb0)
free 6010ecb0
gc_free(6010ec50)
free 6010ec50
gc_alloc(48 bytes -> 3 blocks)
gc_alloc(6010ec40)
malloc 48 : 6010ec40
gc_alloc(16 bytes -> 1 blocks)
gc_alloc(6010ec70)
malloc 16 : 6010ec70
gc_alloc(32 bytes -> 2 blocks)
gc_alloc(6010ec80)
malloc 32 : 6010ec80
gc_alloc(64 bytes -> 4 blocks)
gc_alloc(6010eca0)
malloc 64 : 6010eca0
gc_alloc(0 bytes -> 0 blocks)
malloc 0 : 00000000
gc_alloc(24 bytes -> 2 blocks)
gc_alloc(6010ece0)
malloc 24 : 6010ece0
gc_alloc(0 bytes -> 0 blocks)
malloc 0 : 00000000
assign byte code: code=6010ece0 len=24 flags=0
gc_free(00000000)
free 00000000
gc_free(6010eca0)
free 6010eca0
gc_free(6010ef70)
free 6010ef70
gc_free(6010ec80)
free 6010ec80
gc_free(6010ec40)
free 6010ec40
make_function_from_raw_code 6010ec70
gc_alloc(16 bytes -> 1 blocks)
gc_alloc(6010ec40)
malloc 16 : 6010ec40
calling function 6010ec40(n_args=0, n_kw=0, args=00000000)
Input n_args: 0, n_kw: 0
Input pos args: 00000000: 
Input kw args: 00000000: 
Calling: n_pos_args=0, n_kwonly_args=0
6010e8f4: 
6010e8ec: 00000000 00000000 
import name 'sys' level=0
__import__:
  'sys'
  None
  None
  None
  0
Module already loaded
store name sys <- 600eeff4
mp_map_rehash(6010b5a8): 1 -> 2
gc_alloc(16 bytes -> 1 blocks)
gc_alloc(6010ec50)
malloc 16 : 6010ec50
gc_free(6010ebc0)
free 6010ebc0
```

dir(sys.version)的过程

```
>>> dir(sys.version)
gc_alloc(17 bytes -> 2 blocks)
gc_alloc(6010ec80)
malloc 17 : 6010ec80
gc_alloc(16 bytes -> 1 blocks)
gc_alloc(6010ebc0)
malloc 16 : 6010ebc0
gc_alloc(84 bytes -> 6 blocks)
gc_alloc(6010ed00)
malloc 84 : 6010ed00
gc_alloc(20 bytes -> 2 blocks)
gc_alloc(6010eca0)
malloc 20 : 6010eca0
gc_alloc(32 bytes -> 2 blocks)
gc_alloc(6010ecc0)
malloc 32 : 6010ecc0
gc_alloc(512 bytes -> 32 blocks)
gc_alloc(6010ed60)
malloc 512 : 6010ed60
gc_alloc(128 bytes -> 8 blocks)
gc_alloc(6010ef60)
malloc 128 : 6010ef60
gc_alloc(24 bytes -> 2 blocks)
gc_alloc(6010efe0)
malloc 24 : 6010efe0
realloc 6010efe0, 40, 1611722720 : 6010efe0
realloc 6010efe0, 52, 1611722720 : 6010efe0
realloc 6010efe0, 68, 1611722720 : 6010efe0
realloc 6010efe0, 84, 1611722720 : 6010efe0
realloc 6010efe0, 80, 1611722720 : 6010e8e0
gc_free(6010ed60)
free 6010ed60
gc_free(6010ef60)
free 6010ef60
gc_free(6010ebc0)
free 6010ebc0
gc_free(6010ecc0)
free 6010ecc0
gc_free(6010eca0)
free 6010eca0
gc_free(6010ed00)
free 6010ed00
gc_alloc(48 bytes -> 3 blocks)
gc_alloc(6010eca0)
malloc 48 : 6010eca0
gc_alloc(16 bytes -> 1 blocks)
gc_alloc(6010ebc0)
malloc 16 : 6010ebc0
gc_alloc(32 bytes -> 2 blocks)
gc_alloc(6010ed00)
malloc 32 : 6010ed00
gc_alloc(64 bytes -> 4 blocks)
gc_alloc(6010ed20)
malloc 64 : 6010ed20
gc_alloc(0 bytes -> 0 blocks)
malloc 0 : 00000000
gc_alloc(33 bytes -> 3 blocks)
gc_alloc(6010ed60)
malloc 33 : 6010ed60
gc_alloc(0 bytes -> 0 blocks)
malloc 0 : 00000000
assign byte code: code=6010ed60 len=33 flags=0
gc_free(00000000)
free 00000000
gc_free(6010ed20)
free 6010ed20
gc_free(6010efe0)
free 6010efe0
gc_free(6010ed00)
free 6010ed00
gc_free(6010eca0)
free 6010eca0
make_function_from_raw_code 6010ebc0
gc_alloc(16 bytes -> 1 blocks)
gc_alloc(6010ec60)
malloc 16 : 6010ec60
calling function 6010ec60(n_args=0, n_kw=0, args=00000000)
Input n_args: 0, n_kw: 0
Input pos args: 00000000: 
Input kw args: 00000000: 
Calling: n_pos_args=0, n_kwonly_args=0
6010e8f8: 
6010e8ec: 00000000 00000000 00000000 
load name __repl_print__
load global __repl_print__
load name dir
load global dir
load name sys
load global sys
load attr 600eeff4.version
load method 600eeff4.version
calling function 600ee560(n_args=1, n_kw=0, args=6010e8f4)
gc_alloc(16 bytes -> 1 blocks)
gc_alloc(6010eca0)
malloc 16 : 6010eca0
gc_alloc(16 bytes -> 1 blocks)
gc_alloc(6010ecb0)
malloc 16 : 6010ecb0
realloc 6010ecb0, 32 : 6010ecb0
gc_alloc(64 bytes -> 4 blocks)
gc_alloc(6010ed00)
gc_realloc(6010ecb0 -> 6010ed00)
gc_free(6010ecb0)
realloc 6010ecb0, 64 : 6010ed00
gc_alloc(128 bytes -> 8 blocks)
gc_alloc(6010ed90)
gc_realloc(6010ed00 -> 6010ed90)
gc_free(6010ed00)
realloc 6010ed00, 128 : 6010ed90
calling function 600ee61c(n_args=1, n_kw=0, args=6010e8f0)
['__class__', 'center', 'count', 'endswith', 'find', 'format', 'index', 'isalpha', 'isdigit', 'islower', 'isspace', 'isupper', 'join', 'lower', 'lstrip', 'partition', 'replace', 'rfind', 'rindex', 'rpartition', 'rsplit', 'rstrip', 'split', 'splitlines', 'startswith', 'strip', 'upper', 'encode']
gc_alloc(16 bytes -> 1 blocks)
gc_alloc(6010ecb0)
malloc 16 : 6010ecb0
gc_alloc(8 bytes -> 1 blocks)
gc_alloc(6010ecc0)
malloc 8 : 6010ecc0
```

定义一个变量a=1

```
>>> a=1
gc_alloc(4 bytes -> 1 blocks)
gc_alloc(6010ecd0)
malloc 4 : 6010ecd0
gc_alloc(16 bytes -> 1 blocks)
gc_alloc(6010ed00)
malloc 16 : 6010ed00
gc_alloc(84 bytes -> 6 blocks)
gc_alloc(6010ee10)
malloc 84 : 6010ee10
gc_alloc(20 bytes -> 2 blocks)
gc_alloc(6010ed10)
malloc 20 : 6010ed10
gc_alloc(32 bytes -> 2 blocks)
gc_alloc(6010ed30)
malloc 32 : 6010ed30
gc_alloc(512 bytes -> 32 blocks)
gc_alloc(6010ee70)
malloc 512 : 6010ee70
gc_alloc(128 bytes -> 8 blocks)
gc_alloc(6010f070)
malloc 128 : 6010f070
gc_alloc(128 bytes -> 8 blocks)
gc_alloc(6010f0f0)
malloc 128 : 6010f0f0
QSTR: add hash=196 len=1 data=a
gc_alloc(40 bytes -> 3 blocks)
gc_alloc(6010f170)
malloc 40 : 6010f170
QSTR: allocate new pool of size 6
gc_alloc(24 bytes -> 2 blocks)
gc_alloc(6010f1a0)
malloc 24 : 6010f1a0
realloc 6010f1a0, 24, 1611723168 : 6010e8e0
gc_free(6010ee70)
free 6010ee70
gc_free(6010f070)
free 6010f070
gc_free(6010ed00)
free 6010ed00
gc_free(6010ed30)
free 6010ed30
gc_free(6010ed10)
free 6010ed10
gc_free(6010ee10)
free 6010ee10
gc_alloc(48 bytes -> 3 blocks)
gc_alloc(6010ed00)
malloc 48 : 6010ed00
gc_alloc(16 bytes -> 1 blocks)
gc_alloc(6010ed30)
malloc 16 : 6010ed30
gc_alloc(32 bytes -> 2 blocks)
gc_alloc(6010ed40)
malloc 32 : 6010ed40
gc_alloc(64 bytes -> 4 blocks)
gc_alloc(6010ee10)
malloc 64 : 6010ee10
gc_alloc(0 bytes -> 0 blocks)
malloc 0 : 00000000
gc_alloc(20 bytes -> 2 blocks)
gc_alloc(6010ee50)
malloc 20 : 6010ee50
gc_alloc(0 bytes -> 0 blocks)
malloc 0 : 00000000
assign byte code: code=6010ee50 len=20 flags=0
gc_free(00000000)
free 00000000
gc_free(6010ee10)
free 6010ee10
gc_free(6010f1a0)
free 6010f1a0
gc_free(6010ed40)
free 6010ed40
gc_free(6010ed00)
free 6010ed00
make_function_from_raw_code 6010ed30
gc_alloc(16 bytes -> 1 blocks)
gc_alloc(6010ed00)
malloc 16 : 6010ed00
calling function 6010ed00(n_args=0, n_kw=0, args=00000000)
Input n_args: 0, n_kw: 0
Input pos args: 00000000: 
Input kw args: 00000000: 
Calling: n_pos_args=0, n_kwonly_args=0
6010e8f8: 
6010e8f4: 00000000 
store name a <- 00000003
mp_map_rehash(6010b5a8): 2 -> 4
gc_alloc(32 bytes -> 2 blocks)
gc_alloc(6010ed10)
malloc 32 : 6010ed10
gc_free(6010ec50)
free 6010ec50
```

定义一个元组。

```
>>> a=(1,2)
gc_alloc(8 bytes -> 1 blocks)
gc_alloc(6010ec50)
malloc 8 : 6010ec50
gc_alloc(16 bytes -> 1 blocks)
gc_alloc(6010ed40)
malloc 16 : 6010ed40
gc_alloc(84 bytes -> 6 blocks)
gc_alloc(6010ee70)
malloc 84 : 6010ee70
gc_alloc(20 bytes -> 2 blocks)
gc_alloc(6010ee10)
malloc 20 : 6010ee10
gc_alloc(32 bytes -> 2 blocks)
gc_alloc(6010ee30)
malloc 32 : 6010ee30
gc_alloc(512 bytes -> 32 blocks)
gc_alloc(6010eed0)
malloc 512 : 6010eed0
gc_alloc(128 bytes -> 8 blocks)
gc_alloc(6010f1a0)
malloc 128 : 6010f1a0
gc_alloc(24 bytes -> 2 blocks)
gc_alloc(6010f0d0)
malloc 24 : 6010f0d0
realloc 6010f0d0, 36, 0 : 6010f0d0
realloc 6010f0d0, 24, 1611722960 : 6010f0d0
gc_alloc(24 bytes -> 2 blocks)
gc_alloc(6010f220)
malloc 24 : 6010f220
realloc 6010f220, 40, 1611723296 : 6010f220
realloc 6010f220, 36, 1611723296 : 6010e8e0
gc_free(6010eed0)
free 6010eed0
gc_free(6010f1a0)
free 6010f1a0
gc_free(6010ed40)
free 6010ed40
gc_free(6010ee30)
free 6010ee30
gc_free(6010ee10)
free 6010ee10
gc_free(6010ee70)
free 6010ee70
gc_alloc(48 bytes -> 3 blocks)
gc_alloc(6010ee10)
malloc 48 : 6010ee10
gc_alloc(16 bytes -> 1 blocks)
gc_alloc(6010ed40)
malloc 16 : 6010ed40
gc_alloc(32 bytes -> 2 blocks)
gc_alloc(6010ee70)
malloc 32 : 6010ee70
gc_alloc(64 bytes -> 4 blocks)
gc_alloc(6010ee90)
malloc 64 : 6010ee90
gc_alloc(0 bytes -> 0 blocks)
malloc 0 : 00000000
gc_alloc(23 bytes -> 2 blocks)
gc_alloc(6010eed0)
malloc 23 : 6010eed0
gc_alloc(0 bytes -> 0 blocks)
malloc 0 : 00000000
assign byte code: code=6010eed0 len=23 flags=0
gc_free(00000000)
free 00000000
gc_free(6010ee90)
free 6010ee90
gc_free(6010f220)
free 6010f220
gc_free(6010f0d0)
free 6010f0d0
gc_free(6010ee70)
free 6010ee70
gc_free(6010ee10)
free 6010ee10
make_function_from_raw_code 6010ed40
gc_alloc(16 bytes -> 1 blocks)
gc_alloc(6010ed50)
malloc 16 : 6010ed50
calling function 6010ed50(n_args=0, n_kw=0, args=00000000)
Input n_args: 0, n_kw: 0
Input pos args: 00000000: 
Input kw args: 00000000: 
Calling: n_pos_args=0, n_kwonly_args=0
6010e8f4: 
6010e8ec: 00000000 00000000 
gc_alloc(16 bytes -> 1 blocks)
gc_alloc(6010ee10)
malloc 16 : 6010ee10
store name a <- 6010ee10
```

定义一个list。

```
>>> a=[1,2]
gc_alloc(8 bytes -> 1 blocks)
gc_alloc(6010ee20)
malloc 8 : 6010ee20
gc_alloc(16 bytes -> 1 blocks)
gc_alloc(6010ee30)
malloc 16 : 6010ee30
gc_alloc(84 bytes -> 6 blocks)
gc_alloc(6010ee70)
malloc 84 : 6010ee70
gc_alloc(20 bytes -> 2 blocks)
gc_alloc(6010eef0)
malloc 20 : 6010eef0
gc_alloc(32 bytes -> 2 blocks)
gc_alloc(6010ef10)
malloc 32 : 6010ef10
gc_alloc(512 bytes -> 32 blocks)
gc_alloc(6010f1a0)
malloc 512 : 6010f1a0
gc_alloc(128 bytes -> 8 blocks)
gc_alloc(6010ef30)
malloc 128 : 6010ef30
gc_alloc(24 bytes -> 2 blocks)
gc_alloc(6010efb0)
malloc 24 : 6010efb0
realloc 6010efb0, 36, 1611722672 : 6010efb0
realloc 6010efb0, 52, 1611722672 : 6010efb0
realloc 6010efb0, 52, 1611722672 : 6010e8e0
gc_free(6010f1a0)
free 6010f1a0
gc_free(6010ef30)
free 6010ef30
gc_free(6010ee30)
free 6010ee30
gc_free(6010ef10)
free 6010ef10
gc_free(6010eef0)
free 6010eef0
gc_free(6010ee70)
free 6010ee70
gc_alloc(48 bytes -> 3 blocks)
gc_alloc(6010ee70)
malloc 48 : 6010ee70
gc_alloc(16 bytes -> 1 blocks)
gc_alloc(6010ee30)
malloc 16 : 6010ee30
gc_alloc(32 bytes -> 2 blocks)
gc_alloc(6010eea0)
malloc 32 : 6010eea0
gc_alloc(64 bytes -> 4 blocks)
gc_alloc(6010eef0)
malloc 64 : 6010eef0
gc_alloc(0 bytes -> 0 blocks)
malloc 0 : 00000000
gc_alloc(23 bytes -> 2 blocks)
gc_alloc(6010ef30)
malloc 23 : 6010ef30
gc_alloc(0 bytes -> 0 blocks)
malloc 0 : 00000000
assign byte code: code=6010ef30 len=23 flags=0
gc_free(00000000)
free 00000000
gc_free(6010eef0)
free 6010eef0
gc_free(6010efb0)
free 6010efb0
gc_free(6010eea0)
free 6010eea0
gc_free(6010ee70)
free 6010ee70
make_function_from_raw_code 6010ee30
gc_alloc(16 bytes -> 1 blocks)
gc_alloc(6010ee40)
malloc 16 : 6010ee40
calling function 6010ee40(n_args=0, n_kw=0, args=00000000)
Input n_args: 0, n_kw: 0
Input pos args: 00000000: 
Input kw args: 00000000: 
Calling: n_pos_args=0, n_kwonly_args=0
6010e8f4: 
6010e8ec: 00000000 00000000 
gc_alloc(16 bytes -> 1 blocks)
gc_alloc(6010ee70)
malloc 16 : 6010ee70
gc_alloc(16 bytes -> 1 blocks)
gc_alloc(6010ee80)
malloc 16 : 6010ee80
store name a <- 6010ee70
```

定义一个dict。

```
>>> d = {"a":1,"b":2}
gc_alloc(18 bytes -> 2 blocks)
gc_alloc(6010ee90)
malloc 18 : 6010ee90
gc_alloc(16 bytes -> 1 blocks)
gc_alloc(6010eeb0)
malloc 16 : 6010eeb0
gc_alloc(84 bytes -> 6 blocks)
gc_alloc(6010ef50)
malloc 84 : 6010ef50
gc_alloc(20 bytes -> 2 blocks)
gc_alloc(6010eef0)
malloc 20 : 6010eef0
gc_alloc(32 bytes -> 2 blocks)
gc_alloc(6010ef10)
malloc 32 : 6010ef10
gc_alloc(512 bytes -> 32 blocks)
gc_alloc(6010f1a0)
malloc 512 : 6010f1a0
gc_alloc(128 bytes -> 8 blocks)
gc_alloc(6010efb0)
malloc 128 : 6010efb0
QSTR: add hash=193 len=1 data=d
gc_alloc(24 bytes -> 2 blocks)
gc_alloc(6010f030)
malloc 24 : 6010f030
QSTR: add hash=199 len=1 data=b
realloc 6010f030, 40, 1611722800 : 6010d81c
realloc 6010f030, 52, 1611722800 : 6010d81c
realloc 6010f030, 68, 1611722800 : 6010d81c
realloc 6010f030, 80, 1611722800 : 6010d81c
realloc 6010f030, 96, 1611722800 : 6010d81c
realloc 6010f030, 96, 1611722800 : 6010e8e0
gc_free(6010f1a0)
free 6010f1a0
gc_free(6010efb0)
free 6010efb0
gc_free(6010eeb0)
free 6010eeb0
gc_free(6010ef10)
free 6010ef10
gc_free(6010eef0)
free 6010eef0
gc_free(6010ef50)
free 6010ef50
gc_alloc(48 bytes -> 3 blocks)
gc_alloc(6010eef0)
malloc 48 : 6010eef0
gc_alloc(16 bytes -> 1 blocks)
gc_alloc(6010eeb0)
malloc 16 : 6010eeb0
gc_alloc(32 bytes -> 2 blocks)
gc_alloc(6010ef50)
malloc 32 : 6010ef50
gc_alloc(64 bytes -> 4 blocks)
gc_alloc(6010ef70)
malloc 64 : 6010ef70
gc_alloc(0 bytes -> 0 blocks)
malloc 0 : 00000000
gc_alloc(31 bytes -> 2 blocks)
gc_alloc(6010efb0)
malloc 31 : 6010efb0
gc_alloc(0 bytes -> 0 blocks)
malloc 0 : 00000000
assign byte code: code=6010efb0 len=31 flags=0
gc_free(00000000)
free 00000000
gc_free(6010ef70)
free 6010ef70
gc_free(6010f030)
free 6010f030
gc_free(6010ef50)
free 6010ef50
gc_free(6010eef0)
free 6010eef0
make_function_from_raw_code 6010eeb0
gc_alloc(16 bytes -> 1 blocks)
gc_alloc(6010eec0)
malloc 16 : 6010eec0
calling function 6010eec0(n_args=0, n_kw=0, args=00000000)
Input n_args: 0, n_kw: 0
Input pos args: 00000000: 
Input kw args: 00000000: 
Calling: n_pos_args=0, n_kwonly_args=0
6010e8f8: 
6010e8ec: 00000000 00000000 00000000 
gc_alloc(16 bytes -> 1 blocks)
gc_alloc(6010eef0)
malloc 16 : 6010eef0
gc_alloc(16 bytes -> 1 blocks)
gc_alloc(6010ef00)
malloc 16 : 6010ef00
store name d <- 6010eef0
```

定义一个字符串。

```
>>> a = "123"
gc_alloc(10 bytes -> 1 blocks)
gc_alloc(6010ef10)
malloc 10 : 6010ef10
gc_alloc(16 bytes -> 1 blocks)
gc_alloc(6010ef20)
malloc 16 : 6010ef20
gc_alloc(84 bytes -> 6 blocks)
gc_alloc(6010ef50)
malloc 84 : 6010ef50
gc_alloc(20 bytes -> 2 blocks)
gc_alloc(6010efd0)
malloc 20 : 6010efd0
gc_alloc(32 bytes -> 2 blocks)
gc_alloc(6010eff0)
malloc 32 : 6010eff0
gc_alloc(512 bytes -> 32 blocks)
gc_alloc(6010f1a0)
malloc 512 : 6010f1a0
gc_alloc(128 bytes -> 8 blocks)
gc_alloc(6010f010)
malloc 128 : 6010f010
QSTR: add hash=213 len=3 data=123
gc_alloc(24 bytes -> 2 blocks)
gc_alloc(6010f090)
malloc 24 : 6010f090
realloc 6010f090, 24, 1611722896 : 6010e8e0
gc_free(6010f1a0)
free 6010f1a0
gc_free(6010f010)
free 6010f010
gc_free(6010ef20)
free 6010ef20
gc_free(6010eff0)
free 6010eff0
gc_free(6010efd0)
free 6010efd0
gc_free(6010ef50)
free 6010ef50
gc_alloc(48 bytes -> 3 blocks)
gc_alloc(6010ef50)
malloc 48 : 6010ef50
gc_alloc(16 bytes -> 1 blocks)
gc_alloc(6010ef20)
malloc 16 : 6010ef20
gc_alloc(32 bytes -> 2 blocks)
gc_alloc(6010ef80)
malloc 32 : 6010ef80
gc_alloc(64 bytes -> 4 blocks)
gc_alloc(6010efd0)
malloc 64 : 6010efd0
gc_alloc(0 bytes -> 0 blocks)
malloc 0 : 00000000
gc_alloc(22 bytes -> 2 blocks)
gc_alloc(6010f010)
malloc 22 : 6010f010
gc_alloc(0 bytes -> 0 blocks)
malloc 0 : 00000000
assign byte code: code=6010f010 len=22 flags=0
gc_free(00000000)
free 00000000
gc_free(6010efd0)
free 6010efd0
gc_free(6010f090)
free 6010f090
gc_free(6010ef80)
free 6010ef80
gc_free(6010ef50)
free 6010ef50
make_function_from_raw_code 6010ef20
gc_alloc(16 bytes -> 1 blocks)
gc_alloc(6010ef50)
malloc 16 : 6010ef50
calling function 6010ef50(n_args=0, n_kw=0, args=00000000)
Input n_args: 0, n_kw: 0
Input pos args: 00000000: 
Input kw args: 00000000: 
Calling: n_pos_args=0, n_kwonly_args=0
6010e8f8: 
6010e8f4: 00000000 
store name a <- 00000a86
```

看看gc.c这个文件。

一个block是4个word，也就是16个字节。

mp_print_kind_t这个用到的地方多，但是幅值的地方不多，就这里。

```
            mp_print_kind_t print_kind;
            if (conversion == 's') {
                print_kind = PRINT_STR;
            } else {
                assert(conversion == 'r');
                print_kind = PRINT_REPR;
            }
```

上面的调试打印太多了。大多数是malloc和free的。都注释掉。

```
>>> import sys
assign byte code: code=6010ebc0 len=24 flags=0
make_function_from_raw_code 6010eb50
calling function 6010eb20(n_args=0, n_kw=0, args=00000000)
Input n_args: 0, n_kw: 0
Input pos args: 00000000: 
Input kw args: 00000000: 
Calling: n_pos_args=0, n_kwonly_args=0
6010e7d4: 
6010e7cc: 00000000 00000000 
import name 'sys' level=0
__import__:
  'sys'
  None
  None
  None
  0
Module already loaded
store name sys <- 600eeed0
mp_map_rehash(6010b488): 1 -> 2
```



这个bc是bytecode的缩写。当前就是这种方式。

```
mp_obj_new_fun_bc
```

靠的是这里来执行。

```
mp_obj_t mp_call_function_n_kw(mp_obj_t fun_in, size_t n_args, size_t n_kw, const mp_obj_t *args) {
    // TODO improve this: fun object can specify its type and we parse here the arguments,
    // passing to the function arrays of fixed and keyword arguments

    DEBUG_OP_printf("calling function %p(n_args=" UINT_FMT ", n_kw=" UINT_FMT ", args=%p)\n", fun_in, n_args, n_kw, args);

    // get the type
    mp_obj_type_t *type = mp_obj_get_type(fun_in);

    // do the call
    if (type->call != NULL) {
        return type->call(fun_in, n_args, n_kw, args);
    }
```

是调用到这里：

```
STATIC mp_obj_t fun_bc_call(mp_obj_t self_in, size_t n_args, size_t n_kw, const mp_obj_t *args) {
    MP_STACK_CHECK();
```

```
xhl -- func:mp_execute_bytecode, line:204, case:80
xhl -- func:mp_execute_bytecode, line:204, case:11
xhl -- func:mp_execute_bytecode, line:204, case:68
import name 'sys' level=0
__import__:
  'sys'
  None
  None
  None
  0
Module already loaded
xhl -- func:mp_execute_bytecode, line:204, case:24
store name sys <- 600ef038
mp_map_rehash(6010b668): 1 -> 2
xhl -- func:mp_execute_bytecode, line:204, case:11
xhl -- func:mp_execute_bytecode, line:204, case:5b
```



执行了这个分支。

```
ENTRY(MP_BC_IMPORT_NAME): {
                    MARK_EXC_IP_SELECTIVE();
                    DECODE_QSTR;
                    mp_obj_t obj = POP();
                    SET_TOP(mp_import_name(qst, obj, TOP()));
                    DISPATCH();
                }
```

```
>>> dir(sys)
xhl -- parse_input_kind:0
xhl -- exec flag is vstr
assign byte code: code=6010ee80 len=30 flags=0
xhl -- in mp compile
make_function_from_raw_code 6010edf0
xhl -- func:mp_make_function_from_raw_code, line:131, rc->kind:2
xhl -- func:mp_make_function_from_raw_code, line:149,  rc->data.u_byte.bytecode:
calling function 6010edc0(n_args=0, n_kw=0, args=00000000)
Input n_args: 0, n_kw: 0
Input pos args: 00000000: 
Input kw args: 00000000: 
Calling: n_pos_args=0, n_kwonly_args=0
6010e9b8: 
6010e9ac: 00000000 00000000 00000000 
xhl -- func:mp_execute_bytecode, line:204, case:1b
load name __repl_print__
load global __repl_print__
xhl -- func:mp_execute_bytecode, line:204, case:1b
load name dir
load global dir
xhl -- func:mp_execute_bytecode, line:204, case:1b
load name sys
load global sys
xhl -- func:mp_execute_bytecode, line:204, case:64
calling function 600ee5a4(n_args=1, n_kw=0, args=6010e9b4)
xhl -- func:fun_builtin_var_call, line:115, 
gc_realloc(6010ede0 -> 6010ee20)
xhl -- func:mp_execute_bytecode, line:204, case:64
calling function 600ee660(n_args=1, n_kw=0, args=6010e9b0)
xhl -- func:fun_builtin_1_call, line:69, 
['__class__', '__name__', 'modules', 'exit', 'byteorder', 'version_info', 'path', 'argv', 'version', 'implementation', 'print_exception', 'platform']
xhl -- func:mp_execute_bytecode, line:204, case:32
xhl -- func:mp_execute_bytecode, line:204, case:11
xhl -- func:mp_execute_bytecode, line:204, case:5b
```

# mpy-cross 

mpy-cross 是 MicroPython 提供的一个交叉编译工具，

用于将 Python 源文件（.py 文件）预编译成适合目标设备运行的 .mpy 文件。

以下是使用 mpy-cross 的详细步骤和方法：

编译生成mpy-cross文件

```
git clone --recursive https://github.com/micropython/micropython.git 
make -C micropython/mpy-cross
```

也可以用pip安装：

```
pip install mpy-cross
```

把python文件编译生成mpy文件：

```
./mpy-cross sample.py 
```

在 Thonny 中可以直接安装 mpy-cross 并使用它来生成 .mpy 文件，从而加速运行和加密代码

https://github.com/thonny/thonny

thonny这个工具是用途tkinter编写的IDE，也是挺厉害的。可以看出tkinter的能力也不小。



也可以添加到环境变量

另外 如果是自定义固件，调试稳定的py文件，最好放到固件里面。详情查看本站其他文章。

**经过测试，同名的模块执行优先级依次为：**

**flash的.py => flash的.mpy => rom的.py => rom的.c**

python 的代码几乎无法完全加密，基本上不可能加密。

核心敏感内容，建议用c来写，micropython不适合做这个事情。 或者 c模块+ mpy的方式也凑合可以。

无论从代码执行效率和mcu资源的利用率，还是代码的保护上 micropython 都是不是好选择。

但是在初期产品阶段micropython 还是非常不错的，上线前 根据情况用c写一部分模块，或者干脆重写就好了。



## 参考资料

Thonny MicroPython 使用mpy-cross 生成MPY文件加速运行与加密

https://www.cnblogs.com/timseng/p/17112300.html

micropython代码压缩和简单加密 mpy-cross

https://dev.leiyanhui.com/mcu/mpy-cross/

mpy-cross文档

https://github.com/RT-Thread-packages/micropython/blob/master/docs/tools-mpy-cross.md

# mpy默认的文件系统

MicroPython默认使用LittleFS作为其文件系统，而旧版本则使用FAT格式。

MicroPython使用LittleFS文件系统具有以下几个优势：

1. **写入负载均衡**：LittleFS通过写入负载均衡技术，可以显著提高存储闪存的寿命。这意味着在频繁写入数据的应用中，LittleFS能够更有效地管理存储设备的使用，从而延长其使用寿命。
2. **更好的对电源故障的抵抗能力**：与传统的FAT文件系统相比，LittleFS具有更好的抗电源故障能力。这使得它在需要高可靠性的嵌入式应用中更为适用。
3. **支持修改时间戳**：LittleFS v2版本允许为文件添加和更新修改时间戳，这对于需要记录文件变更历史的应用非常有用。当启用`mtime`参数时，即使文件没有时间戳，`os.stat ()`也会返回0作为时间戳。
4. **透明地处理现有文件**：对于已经存在的文件，一旦它们被打开进行写入操作，LittleFS会自动添加或更新时间戳，无需重新格式化整个文件系统。
5. **易于挂载和使用**：创建一个使用LittleFS的文件系统对象后，可以通过`mount()`方法将其挂载到微Python环境中，这样可以方便地进行文件系统的管理和操作。



在MicroPython中，FAT格式的文件系统与LittleFS相比有以下不同：

1. **访问方式**：FAT文件系统的主要优点是可以在支持的板卡（例如STM32）上通过USB MSC访问，无需主机PC上的额外驱动程序。这意味着如果需要通过USB设备访问文件系统，FAT可能更方便。
2. **对写操作期间停电的容忍度**：FAT文件系统不耐受写操作期间的停电，这可能会导致文件系统损坏。而LittleFS设计有强大的复制写保证，如果发生随机电源故障，文件系统将回退到上一次已知的正确状态。
3. **性能和稳定性**：长期使用后，FAT文件系统的碎片化问题可能导致存储速度下降。LittleFS则具有磨损均衡功能和掉电保护能力，适用于RAM和ROM有限的场景。
4. **资源占用**：LittleFS高度集成，使用比FAT少的ROM空间（约13K）和RAM空间（少于4K），适合资源受限的MCU。

因此，**对于不需要USB MSC的应用程序，或者对存储性能和稳定性要求较高的应用，建议使用LittleFS。**



根据最新的MicroPython官方文档，关于文件系统选择的最新指导或更新主要集中在以下几个方面：

1. **执行.mpy文件**：新版本支持直接<u>从文件系统执行.mpy文件，无需先将其复制到RAM中</u>。这显著提高了代码部署速度并减少了内存开销和碎片化。
2. **更灵活的配置方式**：引入了对分区、文件系统类型以及USB大容量存储等选项的更灵活配置方式。
3. **自动创建默认配置和检测主文件系统**：MicroPython会自动创建默认配置并自动检测主文件系统，因此用户主要适用于希望修改这些设置的场景。
4. **兼容性和扩展性**：通过将MicroPython扩展从CPython API中移除，实现了与CPython更好的兼容性，使开发人员能够更容易地编写可在两个平台上运行的代码。

https://wiki.sipeed.com/soft/maixpy/zh/get_started/mpfshell-lite/mpfshell-lite.html

# littlefs



## 参考资料

littlefs原理分析--存储结构（一）

https://www.51cto.com/article/721451.html

小型文件系统FatFS和LittleFS对比和区别

https://blog.csdn.net/ybhuangfugui/article/details/105780880

# qstr

在MicroPython中，QSTR（uni独特的字符串）是一种用于字符串驻留（ intern）的机制。

其主要目的是为了节省内存和存储空间，

通过将重复出现的字符串存储在一个共享池中来避免重复存储

QSTR表是一个全局性的数据结构，

它将.mpy文件内部的qstr编号映射到运行时环境中该字符串对应的qstr编号。

这种机制使得所有需要使用字符串的地方都可以通过一个唯一的编号来引用，

从而提高了代码的执行效率和内存利用率。



在编译过程中，MicroPython会生成QSTR头部文件，

这些文件包含了所有需要驻留的字符串及其相关信息，

如长度、哈希值等。

这些信息被存储在ROM或闪存中，

具体取决于模块是否被冻结为字节码。

例如，在某些情况下，如果模块没有完全调试但可以导入并运行，则可以将其源代码树复制到PC上，并使用工具链构建固件。



使用Incremental Update工具来更新代码中的QSTR数据表是一个有效的最佳实践。这个过程包括五个步骤：

- 使用Incremental Update工具对现有文件进行修改，并生成新的文件`qstr.i.last `。
- 创建一个空文件`qstr.splitIs `用于跟踪增量更新的运行情况。
- 将所有匹配的QSTR文件组合到一起，形成`qstrdefs.collected.h `文件，其中包含每个MP_QSTR_Foo的完整列表。
- 生成一个枚举，将每个MP_QSTR_Foo映射到其对应的索引。然后将`qstrdefs.collected.h `和`qstrdefs*.h`组合在一起，并转换每个Q(Foo)为"Q(Foo)"，以便在预处理器中处理条件编译。
- 使用`make qstrdata.py `生成`qstrdefs.generated.h `文件，其中包含每个MP_QSTR_Foo的哈希值和相应的索引。

https://metaso.cn/search/8514435144619732992?q=micropython+qstr



# mpy原理

https://www.limfx.pro/ReadArticle/1115/micropython-yun-hang-yuan-li-yi-ji-ru-he-tong-guocyu-yan-kuo-zhan-micropython-module



移植micropython到jz2440开发板(samsung s3c2440 soc)记录

https://blog.csdn.net/CallMe_Xu/article/details/107090569



https://blog.csdn.net/superatom01/article/details/135956214



# micropython esp8266 编译

https://metaso.cn/search/8514531143766327296?q=micropython+esp8266+%E7%BC%96%E8%AF%91

Python+ESP嵌入式开发快速上手 ，这个有不少的例子。

https://www.cnblogs.com/holychan/p/18262227



https://docs.01studio.cc/esp8266/quickref.html

这个手册不错。

http://micropython.circuitpython.com.cn/en/latet/esp8266/tutorial/intro.html



# micropython gc算法

MicroPython使用的是标记和清除（Mark-Sweep）算法来管理内存。该算法分为两个主要阶段：

1. **标记阶段**：此阶段遍历堆，标记所有活动对象，即那些仍然被引用的对象。
2. **清扫阶段**：随后的清扫阶段则遍历堆，回收所有未被标记的对象。

这种算法的优点在于其简单性和快速性，通常运行周期少于4毫秒。此外，MicroPython还提供了手动触发垃圾回收的功能，可以通过调用`gc.collect ()`来实现。

https://metaso.cn/search/8514561448295223296?q=micropython+gc%E7%AE%97%E6%B3%95

# 编译过程分析

```
make VARIANT=minimal
```



首先是生成一些头文件。靠python脚本处理。

```
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
```

编译文件的顺序：

```
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
CC ../../py/nlrmips.c
CC ../../py/nlrpowerpc.c
CC ../../py/nlrxtensa.c
CC ../../py/nlrrv32.c
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
CC ../../py/asmrv32.c
CC ../../py/emitnrv32.c
CC ../../py/emitndebug.c
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
CC ../../py/cstack.c
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
CC ../../py/moderrno.c
CC ../../py/modthread.c
CC ../../py/vm.c
CC ../../py/bc.c
CC ../../py/showbc.c
CC ../../py/repl.c
CC ../../py/smallint.c
CC ../../py/frozenmod.c
CC ../../extmod/machine_adc.c
CC ../../extmod/machine_adc_block.c
CC ../../extmod/machine_bitstream.c
CC ../../extmod/machine_i2c.c
CC ../../extmod/machine_i2s.c
CC ../../extmod/machine_mem.c
CC ../../extmod/machine_pinbase.c
CC ../../extmod/machine_pulse.c
CC ../../extmod/machine_pwm.c
CC ../../extmod/machine_signal.c
CC ../../extmod/machine_spi.c
CC ../../extmod/machine_timer.c
CC ../../extmod/machine_uart.c
CC ../../extmod/machine_usb_device.c
CC ../../extmod/machine_wdt.c
CC ../../extmod/modasyncio.c
CC ../../extmod/modbinascii.c
CC ../../extmod/modbluetooth.c
CC ../../extmod/modbtree.c
CC ../../extmod/modcryptolib.c
CC ../../extmod/moddeflate.c
CC ../../extmod/modframebuf.c
CC ../../extmod/modhashlib.c
CC ../../extmod/modheapq.c
CC ../../extmod/modjson.c
CC ../../extmod/modlwip.c
CC ../../extmod/modmachine.c
CC ../../extmod/modnetwork.c
CC ../../extmod/modonewire.c
CC ../../extmod/modopenamp.c
CC ../../extmod/modopenamp_remoteproc.c
CC ../../extmod/modopenamp_remoteproc_store.c
CC ../../extmod/modos.c
CC ../../extmod/modplatform.c
CC ../../extmod/modrandom.c
CC ../../extmod/modre.c
CC ../../extmod/modselect.c
CC ../../extmod/modsocket.c
CC ../../extmod/modtls_axtls.c
CC ../../extmod/modtls_mbedtls.c
CC ../../extmod/modtime.c
CC ../../extmod/moductypes.c
CC ../../extmod/modvfs.c
CC ../../extmod/modwebrepl.c
CC ../../extmod/modwebsocket.c
CC ../../extmod/network_cyw43.c
CC ../../extmod/network_esp_hosted.c
CC ../../extmod/network_lwip.c
CC ../../extmod/network_ninaw10.c
CC ../../extmod/network_wiznet5k.c
CC ../../extmod/os_dupterm.c
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
CC alloc.c
CC fatfs_port.c
CC mpbthciport.c
CC mpbtstackport_common.c
CC mpbtstackport_h4.c
CC mpbtstackport_usb.c
CC mpnimbleport.c
CC modtermios.c
CC modsocket.c
CC modffi.c
CC modjni.c
CC ../../shared/runtime/gchelper_generic.c
CC ../../shared/timeutils/timeutils.c
LINK build-minimal/micropython
   text    data     bss     dec     hex filename
 173993   14704    5320  194017   2f5e1 build-minimal/micropython
```

查看更加详细的编译输出

```
make VARIANT=minimal V=1
```

主要看看脚本的调用。

```
python3 ../../py/makeversionhdr.py build-minimal/genhdr/mpversion.h
```



```
python3 ../../py/makeqstrdefs.py pp gcc -E output build-minimal/genhdr/qstr.i.last cflags  -DFFCONF_H=\"lib/oofatfs/ffconf.h\" -I. -I../.. -Ibuild-minimal -Wall -Werror -Wextra -Wno-unused-parameter -Wpointer-arith -Wdouble-promotion -Wfloat-conversion -std=gnu99 -DUNIX -Os -DNDEBUG -fdata-sections -ffunction-sections -Ivariants/minimal  -g -U _FORTIFY_SOURCE -DMICROPY_ROM_TEXT_COMPRESSION=1 -DNO_QSTR cxxflags -DFFCONF_H=\"lib/oofatfs/ffconf.h\" -I. -I../.. -Ibuild-minimal -Wall -Werror -Wextra -Wno-unused-parameter -Wpointer-arith -Wdouble-promotion -Wfloat-conversion -DUNIX -Os -DNDEBUG -fdata-sections -ffunction-sections -Ivariants/minimal -g -U _FORTIFY_SOURCE -DMICROPY_ROM_TEXT_COMPRESSION=1 -DNO_QSTR sources ../../py/mpstate.c ../../py/malloc.c ../../py/gc.c ../../py/pystack.c ../../py/qstr.c ../../py/vstr.c ../../py/mpprint.c ../../py/unicode.c ../../py/mpz.c ../../py/reader.c 
//   …………中间省掉一大堆的c文件名字
../../shared/libc/printf.c main.c gccollect.c unix_mphal.c mpthreadport.c input.c alloc.c fatfs_port.c mpbthciport.c mpbtstackport_common.c mpbtstackport_h4.c mpbtstackport_usb.c mpnimbleport.c modtermios.c modsocket.c modffi.c modjni.c ../../shared/runtime/gchelper_generic.c ../../shared/timeutils/timeutils.c variants/minimal/mpconfigvariant.h ../../py/mpconfig.h mpconfigport.h

```



```
python3 ../../py/makeqstrdefs.py split qstr build-minimal/genhdr/qstr.i.last build-minimal/genhdr/qstr _
```



```
python3 ../../py/makeqstrdefs.py cat qstr _ build-minimal/genhdr/qstr build-minimal/genhdr/qstrdefs.collected.h
```



```
python3 ../../py/makeqstrdata.py build-minimal/genhdr/qstrdefs.preprocessed.h > build-minimal/genhdr/qstrdefs.generated.h

```



```
python3 ../../py/makeqstrdefs.py split module build-minimal/genhdr/qstr.i.last build-minimal/genhdr/module _

```

```
python3 ../../py/makeqstrdefs.py cat module _ build-minimal/genhdr/module build-minimal/genhdr/moduledefs.collected

```

```
python3 ../../py/makemoduledefs.py build-minimal/genhdr/moduledefs.collected > build-minimal/genhdr/moduledefs.h
```

```
python3 ../../py/makecompresseddata.py build-minimal/genhdr/compressed.collected > build-minimal/genhdr/compressed.data.h

```



makeqstrdefs.py 这个脚本需要5个参数：

```
command 
mode 
input_filename 
output_dir 
output_file
```

command有这几个：‘

```
"pp", // 这个表示预处理。
"output",
"cflags",
"cxxflags",
"sources",
"changed_sources",
"dependencies"
```

mode有这4种：

```
# Extract MP_QSTR_FOO macros.
_MODE_QSTR = "qstr"

# Extract MP_COMPRESSED_ROM_TEXT("") macros.  (Which come from MP_ERROR_TEXT)
_MODE_COMPRESS = "compress"

# Extract MP_REGISTER_(EXTENSIBLE_)MODULE(...) macros.
_MODE_MODULE = "module"

# Extract MP_REGISTER_ROOT_POINTER(...) macros.
_MODE_ROOT_POINTER = "root_pointer"
```

# nlr：no-local return

nlr_* 函数集是针对 MicroPython 所需的功能专门定制的函数，

因此允许从原本昂贵的异常处理操作中挤出每个 CPU 周期。

SetJMP/LongJMP是在“尽力而为”的基础上工作的通用函数。

它们最初是为了允许快速移植到不同的 Unix 架构而添加的。

https://forum.micropython.org/viewtopic.php?t=1909

https://www.cnblogs.com/juwan/p/13079797.html



# 参考资料

1、Micropython开发（1）: 认识Micro Python

https://abcamus.github.io/2017/01/04/Micropython%E5%BC%80%E5%8F%9101/

