---
title: python之哈希表
date: 2019-10-15 15:16:54
tags:
	- Python

---

1

python里的dict，就是基于哈希表的原理的。

用来解决leetcode里的twoSum的问题。很方便。

```
class Solution(object):
    def twoSum(self, nums, target):
        """

        :param nums: List[int]
        :param target: int
        :return: List[int]
        """
        map_a = dict()
        k = len(nums)
        for i in range(0, k):
            temp = target - nums[i]
            if temp in map_a:
                return [map_a[temp], i]
            map_a[nums[i]] = i
```



参考资料

1、Python之哈希表

https://blog.csdn.net/wycgi/article/details/85063342