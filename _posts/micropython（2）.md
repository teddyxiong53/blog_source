---
title: micropython（2）
date: 2018-11-28 09:14:28
tags:
	- micropython

---



现在开始看代码细节。

从builtin的东西开始看。

```
typedef mp_obj_t (*mp_fun_0_t)(void);
typedef mp_obj_t (*mp_fun_1_t)(mp_obj_t);
typedef mp_obj_t (*mp_fun_2_t)(mp_obj_t, mp_obj_t);
typedef mp_obj_t (*mp_fun_3_t)(mp_obj_t, mp_obj_t, mp_obj_t);
typedef mp_obj_t (*mp_fun_var_t)(size_t n, const mp_obj_t *);
```



objtype.c是一切的基础。

