---
title: pipewire之spa_dict和pw_map比较
date: 2025-03-11 14:32:37
tags:
	- 音频
---

--

分析一下pw_array、pw_properties、pw_map、spa_list

# 容器类型比较

| Feature 特征                    | pw_array                           | pw_map                                 | pw_properties                  | spa_list                     |
| ------------------------------- | ---------------------------------- | -------------------------------------- | ------------------------------ | ---------------------------- |
| Memory layout 内存布局          | Contiguous 连续的                  | Contiguous with gaps 有间隙的连续      | Array-based 基于数组的         | Non-contiguous 非连续的      |
| Access pattern 访问模式         | Sequential/Index 顺序/入           | ID-based 基于 ID 的                    | Key-based 基于的               | Sequential 顺序              |
| Growth strategy 发展策略        | Extends by fixed amount 通过固定 a | Reuses free slots first 先重用空闲槽位 | Extends as needed 按需扩展     | No reallocation 不重新分配   |
| Primary use case 主要用例       | Simple collections 简单集合        | Object registries 对象注册表           | Configuration 配置             | Dynamic collections 动态集合 |
| Element constraints 元素约束    | Same size 相同大小                 | Same size 相同大小                     | String key-values 字符串键值对 | Any size 任何                |
| Insertion complexity 插入复杂度 | O(1) amortized O(1) 平均时间复杂度 | O(1)                                   | O(n) (lookup) O(n) (查找)      | O(1)                         |
| Lookup complexity 查找复杂度    | O(1) by index O(1)按索引           | O(1) by ID O(1)按 I                    | O(n) by key O(n) 按键          | O(n)                         |
| Removal complexity 删除复杂度   | O(n)                               | O(1)                                   | O(n)                           | O(1)                         |
