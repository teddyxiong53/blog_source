---
title: 哈希之uthash.h头文件分析
date: 2024-08-15 14:42:33
tags:
	- 数据结构

---

--

# 简介

`uthash.h` 是一个用于 C 语言的开源哈希表库，提供了简单易用的哈希表实现。以下是对 `uthash.h` 的一些主要特性和使用方法的介绍：

### 主要特性

1. **轻量级**：
   - 只需包含一个头文件 `uthash.h`，无需额外的库文件。

2. **易于使用**：
   - 提供简单的宏和数据结构定义，方便快速创建哈希表。

3. **支持多种数据类型**：
   - 可以存储任意类型的数据，只需定义相应的结构体。

4. **动态调整**：
   - 支持动态扩展和缩减，自动处理内存管理。

5. **线程安全**：
   - 在多线程环境下使用时，可以通过适当的锁机制实现线程安全。

### 基本用法

#### 1. 定义结构体

首先定义一个包含哈希表字段的结构体：

```c
#include "uthash.h"

typedef struct {
    int id;            // 键
    char name[10];    // 值
    UT_hash_handle hh; // 使结构体可用于哈希表
} User;
```

#### 2. 添加元素

使用 `HASH_ADD_INT` 函数添加元素：

```c
User *users = NULL;
User *user = malloc(sizeof(User));
user->id = 1;
strcpy(user->name, "Alice");
HASH_ADD_INT(users, id, user);
```

#### 3. 查找元素

使用 `HASH_FIND_INT` 函数查找元素：

```c
User *found_user;
HASH_FIND_INT(users, &id, found_user);
if (found_user) {
    printf("Found user: %s\n", found_user->name);
}
```

#### 4. 删除元素

使用 `HASH_DEL` 函数删除元素：

```c
HASH_DEL(users, user);
free(user);
```

#### 5. 遍历哈希表

可以使用 `HASH_ITER` 宏遍历哈希表：

```c
User *current_user, *tmp;
HASH_ITER(hh, users, current_user, tmp) {
    printf("User ID: %d, Name: %s\n", current_user->id, current_user->name);
}
```

### 总结

`uthash.h` 是一个强大而灵活的哈希表库，适合用于 C 语言项目中，提供了简洁的 API 和高效的性能。通过简单的宏和结构体定义，可以快速实现哈希表的操作。

# 完整例子

代码：

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "uthash.h"

// 定义用户结构体
typedef struct {
    int id;            // 键
    char name[10];    // 值
    UT_hash_handle hh; // 使结构体可用于哈希表
} User;

int main() {
    User *users = NULL; // 哈希表初始化
    User *user, *found_user;

    // 添加用户
    for (int i = 0; i < 5; i++) {
        user = malloc(sizeof(User));
        user->id = i;
        snprintf(user->name, sizeof(user->name), "User%d", i);
        HASH_ADD_INT(users, id, user); // 添加用户到哈希表，注意这里的第二个参数是成员变量的名字。
    }

    // 查找用户
    int id_to_find = 3;
    HASH_FIND_INT(users, &id_to_find, found_user);
    if (found_user) {
        printf("Found user: ID = %d, Name = %s\n", found_user->id, found_user->name);
    } else {
        printf("User with ID = %d not found.\n", id_to_find);
    }

    // 删除用户
    HASH_FIND_INT(users, &id_to_find, found_user);
    if (found_user) {
        HASH_DEL(users, found_user); // 从哈希表中删除
        free(found_user);            // 释放内存
        printf("User with ID = %d deleted.\n", id_to_find);
    }

    // 遍历哈希表
    printf("Current users in the hash table:\n");
    User *current_user, *tmp;
    HASH_ITER(hh, users, current_user, tmp) {
        printf("User ID: %d, Name: %s\n", current_user->id, current_user->name);
    }

    // 释放所有用户内存
    HASH_ITER(hh, users, current_user, tmp) {
        HASH_DEL(users, current_user); // 从哈希表中删除
        free(current_user);             // 释放内存
    }

    return 0;
}
```



```
./a.out 
Found user: ID = 3, Name = User3
User with ID = 3 deleted.
Current users in the hash table:
User ID: 0, Name: User0
User ID: 1, Name: User1
User ID: 2, Name: User2
User ID: 4, Name: User4
```



