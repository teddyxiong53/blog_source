---
title: 如何刷leetcode
date: 2017-11-18 20:55:22
tags:

---



# 1. 什么是leetcode

网址是：https://leetcode.com

1、是一个平台。用来针对技术面试的。

2、有超过450道题。我现在看，是有727道题。

3、支持11种语言：c、Java、Python都支持的。

4、需要注册。

有中文站点。

https://leetcode-cn.com/problemset/all/

我现在按照顺序来刷。

默认用c++来做吧。

# 2.先看一个简单的例子

看第一题，Two Sum。我们通过这个搞懂这个流程。

每个问题页面，包含了5个tag。

分别是：

1、description。描述问题。

2、hint。一般是空的。

3、submissions。也是空的。

4、discuss。这个很重要，是大家给的解决方法。

5、solution。一个基本的解决方法，可能不是很好。

Two Sum这个题目，是给定一个数组，和一个数字。然后找出数组里的两个数，它们的和加起来等于给定的那个数字。要求返回的就是找到的那2个数字的索引值。

我们先看solution里给的3种方法。是Java写的。

第一种：

```
public int[] twoSum(int[] nums, int target) {
	for(int i=0; i<nums.length; i++) {
		for(intj=i+1; j<nums.length; j++) {
			if(nums[i]+nums[j] == target) {
				return new int[]{i,j};
			}
		}
	}
	throw new IllegalArgumentExcetption("No two sum solution");
}
```

这个类似一个冒泡排序，采用的是两层循环。但是很容易理解。

时间复杂度较高。是n2的。

第二种：

因为第一种的时间复杂度很高，所以我们要寻求替代方案。

用来表示索引值和它对应的值的关系，什么数据结构最合适？没错，是HashMap。

我们把查找时间从O(n)减少到O(1)，通过空间换时间，这也是HashMap存在的价值。

简单的实现，是利用2个遍历。

```
public int[] twoSum(int[] nums, int target) {
	Map<Integer, Interger> map = new HashMap<>();
	for(int i=; i<nums.length; i++) {
		map.put(nums[i], i);
	}
	for(int i=0; i<nums.length; i++) {
		int complement = target - nums[i];
		if(map.containKey(complement) && map.get(complement)!=i) {
			return new int[] {i, map.get(complement)};
		}
	}
	throw new IllegalArgumentException("no two sum solution");
}

```

第三种：

第三种是对第二种的优化，我们没有必要做两次遍历。

```
public int[] twoSum(int[] nums, int target) {
	Map<Integer,Integer> map = new HashMap<>();
	for(int i=0; i<nums.length; i++) {
		int complement = target - nums[i];
		if(map.containsKey(complement)) {
			return new int[]{map.get(complement), i};
		}
		map.put(nums[i],i);
	}
	return new IllegalArgumentException("no two sum solutions");
}

```

现在我们到discuss里看看Python版本的。

我看最靠前的那个Python版本，看下面的评论，说跑起来，无法出正确答案。所以这里要注意了，要有自己的思考。但是我测试了一下，是对的。不知道是不是可以修改的，后面作者已经改对了。

```
def twoSum(nums, target):
        if len(nums) <= 1:
            return False
        buff_dict = {}
        for i in range(len(nums)):
            if nums[i] in buff_dict:
                return [buff_dict[nums[i]], i]
            else:
                buff_dict[target - nums[i]] = i
        
numbers=[2,10,3,33333,23,9798,43489,7,5,7]
target = 9
print twoSum(numbers, target)
```

到目前，发现方法就是在于利用可以提高效率的已有数据结构。但是在C语言里，没有这些数据结构。

看到的C语言的方法，都实现地很复杂。都要自己去实现对应的数据结构。

返回值是int指针。分配了sizeof(int)*2。

函数写得比较长。就不贴在这里了。也是用来2个循环，没有嵌套。





这里有代码。

https://github.com/pezy/LeetCode

安装后，在vscode左侧有一个图标，点击进去。

会让你输入用户名和密码进行登陆，然后就可以在vscode里看题目做题目了。



c++版本的，一般都有使用stl的库，就如同java版本，可以使用标准库一样。

只有C语言，没有库可以用，只能用最原始的方式。



参考资料

1、无需打开浏览器！使用VScode刷LeetCode.

https://blog.csdn.net/OCEANtroye/article/details/82811790