---
title: micropython之module
date: 2018-11-29 15:57:28
tags:
	- micropython

---



内置的module有这些。

```
extern const mp_obj_module_t mp_module___main__;
extern const mp_obj_module_t mp_module_builtins;
extern const mp_obj_module_t mp_module_array;
extern const mp_obj_module_t mp_module_collections;
extern const mp_obj_module_t mp_module_io;
extern const mp_obj_module_t mp_module_math;
extern const mp_obj_module_t mp_module_cmath;
extern const mp_obj_module_t mp_module_micropython;
extern const mp_obj_module_t mp_module_ustruct;
extern const mp_obj_module_t mp_module_sys;
extern const mp_obj_module_t mp_module_gc;
extern const mp_obj_module_t mp_module_thread;

extern const mp_obj_dict_t mp_module_builtins_globals;

// extmod modules
extern const mp_obj_module_t mp_module_uerrno;
extern const mp_obj_module_t mp_module_uctypes;
extern const mp_obj_module_t mp_module_uzlib;
extern const mp_obj_module_t mp_module_ujson;
extern const mp_obj_module_t mp_module_ure;
extern const mp_obj_module_t mp_module_uheapq;
extern const mp_obj_module_t mp_module_uhashlib;
extern const mp_obj_module_t mp_module_ubinascii;
extern const mp_obj_module_t mp_module_urandom;
extern const mp_obj_module_t mp_module_uselect;
extern const mp_obj_module_t mp_module_ussl;
extern const mp_obj_module_t mp_module_utimeq;
extern const mp_obj_module_t mp_module_machine;
extern const mp_obj_module_t mp_module_lwip;
extern const mp_obj_module_t mp_module_websocket;
extern const mp_obj_module_t mp_module_webrepl;
extern const mp_obj_module_t mp_module_framebuf;
extern const mp_obj_module_t mp_module_btree;
```

一个个看。

#`__main__`

在runtime.c里。

```
const mp_obj_module_t mp_module___main__ = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t*)&MP_STATE_VM(dict_main),
};
```

