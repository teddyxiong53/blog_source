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



参考资料

1、Micropython开发（1）: 认识Micro Python

https://abcamus.github.io/2017/01/04/Micropython%E5%BC%80%E5%8F%9101/

