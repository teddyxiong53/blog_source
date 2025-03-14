---
title: pipewire之spa_dict和pw_map比较
date: 2025-03-11 14:32:37
tags:
	- 音频
---

--

在 PipeWire 中，`spa_dict` 和 `pw_map` 是两种不同的数据结构，用于存储键值对或映射关系，尽管它们在某些场景下功能看似相似，但设计目标、实现方式和使用场景有显著区别。以下是对 `spa_dict` 和 `pw_map` 的详细对比分析，结合源码（如 `spa/utils/dict.h` 和 `pipewire/map.h`）进行说明。

---

### 1. `spa_dict` 概述
- **定义文件**: `spa/include/spa/utils/dict.h`
- **全称**: Simple Plugin API Dictionary
- **作用**: 一个轻量级的键值对存储结构，用于表示属性集合。
- **结构**:
  ```c
  struct spa_dict_item {
      const char *key;   // 键（字符串）
      const char *value; // 值（字符串）
  };
  
  struct spa_dict {
      uint32_t n_items;          // 键值对数量
      const struct spa_dict_item *items; // 键值对数组
  };
  ```
- **特点**:
  - 静态或只读设计，`items` 是指向常量数组的指针。
  - 键和值均为字符串（`const char *`）。
  - 不支持动态插入或删除，通常用于初始化或传递固定配置。

#### 使用场景
- **属性传递**: 用于模块、工厂或对象的属性（如 `module_props` 在 `module-metadata.c`）。
- **示例**:
  ```c
  static const struct spa_dict_item module_props[] = {
      { PW_KEY_MODULE_AUTHOR, "Wim Taymans" },
      { PW_KEY_MODULE_DESCRIPTION, "Metadata module" },
  };
  struct spa_dict props = { .n_items = 2, .items = module_props };
  ```

---

### 2. `pw_map` 概述
- **定义文件**: `pipewire/map.h`
- **全称**: PipeWire Map
- **作用**: 一个动态的 ID 到对象的映射表，用于管理 PipeWire 中的资源（如代理对象、内存块）。
- **结构**:
  ```c
  struct pw_map {
      void **items;      // 对象指针数组
      size_t n_items;    // 当前项数
      size_t allocated;  // 已分配空间大小
      size_t extend;     // 每次扩展的项数
      uint32_t free_list;// 空闲项链表头
      bool simple;       // 是否为简单模式（仅存储整数）
  };
  ```
- **特点**:
  - 动态分配，支持插入（`pw_map_insert_new`）、移除（`pw_map_remove`）和查找（`pw_map_lookup`）。
  - 值可以是任意指针（`void *`），键是整数（`uint32_t`）。
  - 使用数组和空闲链表优化内存管理。

#### 使用场景
- **资源管理**: 用于跟踪全局 ID 和对象的映射（如 `pw_core->objects`）。
- **示例**:
  ```c
  struct pw_map objects;
  pw_map_init(&objects, 64, 64); // 初始化 64 个槽
  uint32_t id = pw_map_insert_new(&objects, proxy); // 插入代理对象
  void *obj = pw_map_lookup(&objects, id); // 查找对象
  ```

---

### 3. 区别对比

| **特性**         | **`spa_dict`**              | **`pw_map`**                 |
| ---------------- | --------------------------- | ---------------------------- |
| **定义位置**     | SPA（`spa/utils/dict.h`）   | PipeWire（`pipewire/map.h`） |
| **数据类型**     | 键值对（字符串-字符串）     | ID-对象映射（整数-指针）     |
| **动态性**       | 静态，只读                  | 动态，支持插入、移除         |
| **键类型**       | `const char *`              | `uint32_t`                   |
| **值类型**       | `const char *`              | `void *`（任意指针）         |
| **存储方式**     | 连续的 `spa_dict_item` 数组 | 动态数组 + 空闲链表          |
| **主要功能**     | 属性存储和传递              | 资源 ID 管理                 |
| **典型使用场景** | 配置参数、模块属性          | 代理对象、内存块映射         |
| **内存管理**     | 无动态分配，依赖外部数组    | 内部管理内存，自动扩展       |
| **查找复杂度**   | O(n)（线性遍历）            | O(1)（数组索引）             |

---

### 4. 源码中的体现

#### (1) `spa_dict` 在 `module-metadata.c`
- **模块属性**:
  ```c
  static const struct spa_dict_item module_props[] = {
      { PW_KEY_MODULE_AUTHOR, "Wim Taymans" },
      { PW_KEY_MODULE_DESCRIPTION, "Allow clients to create metadata store" },
  };
  pw_impl_module_update_properties(module, &SPA_DICT_INIT_ARRAY(module_props));
  ```
- **作用**: 定义模块的静态属性，传递给 `pw_impl_module`。

#### (2) `pw_map` 在 `core.c`
- **代理对象管理**:
  ```c
  struct pw_core {
      struct pw_proxy proxy;
      struct pw_map objects; // 映射全局 ID 到代理对象
      // ...
  };
  pw_map_init(&core->objects, 64, 64);
  uint32_t id = pw_map_insert_new(&core->objects, proxy);
  ```
- **作用**: 在 `pw_core` 中管理客户端的代理对象（如节点、端口）。

---

### 5. 使用场景与协作

#### (1) `spa_dict`
- **场景**: 
  - 定义模块或对象的静态属性（如 `module-rt.c` 中的 `module_props`）。
  - 在协议中传递配置（如 `pw_properties` 转为 `spa_dict`）。
- **与 `pw_map` 的关系**:
  - 无直接交互，`spa_dict` 通常用于初始化阶段，而 `pw_map` 用于运行时管理。

#### (2) `pw_map`
- **场景**: 
  - 管理动态资源（如 `pw_core->objects` 映射全局 ID 到 `pw_proxy`）。
  - 在内存池（`pw_mempool`）中映射 ID 到 `pw_memblock`。
- **与 `spa_dict` 的关系**:
  - 可存储 `spa_dict` 指针（如 `pw_map_insert_new(&map, &dict)`），但不常见。

---

### 6. 设计特点与选择依据
- **`spa_dict`**:
  - **优点**: 轻量、简单，适合静态数据。
  - **局限**: 不支持动态修改，查找效率低。
  - **选择**: 需要传递固定属性时使用。
- **`pw_map`**:
  - **优点**: 动态管理，查找高效，灵活性强。
  - **局限**: 内存开销稍大，复杂度高。
  - **选择**: 需要运行时管理资源时使用。

#### 示例选择
- 定义模块描述：用 `spa_dict`（`module_props`）。
- 管理客户端代理：用 `pw_map`（`core->objects`）。

---

### 7. 总结
- **`spa_dict`**: SPA 提供的静态键值对结构，适合存储只读属性，键值均为字符串。
- **`pw_map`**: PipeWire 的动态映射表，适合管理运行时资源，键为整数，值为指针。
二者在 PipeWire 中分工明确：`spa_dict` 用于配置和初始化，`pw_map` 用于动态资源管理，共同支持系统的模块化和高效性。如果需要更具体的代码示例或使用分析，请告诉我！
