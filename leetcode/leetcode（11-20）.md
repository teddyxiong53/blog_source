---
title: leetcode（1-10）
date: 2017-12-20 20:12:22
tags:
	- leetcode
---

# 11. 装最多水的容器



# 12. 把整数转换为罗马数字



# 13. 把罗马数字转成整数



# 14. 最长的公共前缀

判断是否前缀的java方法有：indexOf，startsWith。

##思路一：水平扫描法

LCP(S1...Sn)=LCP(LCP(LCP(S1,S2),S3),...Sn)

就是这样先找出2个字符串的公共前缀，再把公共前缀跟第三个字符串相比。

代码如下：

```
public class Test {
	public String longestCommonPrefix(String[] strs) {
		if(strs.length == 0) {
			return "";
		}
		String prefix = strs[0];
		for(int i=0; i<strs.length; i++) {
			while(strs[i].indexOf(prefix) != 0) {
				prefix = prefix.substring(0, prefix.length()-1);
				if(prefix.isEmpty()) {
					return "";
				}
			}
		}
		return prefix;
		
	}
	
	public static void main(String[] args) {
		Test test = new Test();
		String[] strs = {"leetcode", "leets"};
		String prefix = test.longestCommonPrefix(strs);
		System.out.println("longest common prefix is: " + prefix);
	}
}
```

时间复杂度是O(S)，S代表的是strs所有字符的长度之和。

空间复杂度是O(1)，是常数。

## 思路二：垂直扫描法

这个就是把各个字符串的同一索引位置的字符进行逐个比较。

```
public String longestCommonPrefix(String[] strs) {
		if(strs.length == 0) {
			return "";
		}
		for(int i=0; i<strs[0].length(); i++) {
			char c = strs[0].charAt(i);
			for(int j=1; j<strs.length; j++) {
				if((strs[j].length() == i) || (strs[j].charAt(i) != c)) {
					return strs[0].substring(0, i);
				}
			}
		}
		return strs[0];
	}
```

复杂度跟思路一的一样。

## 思路三：分治法

从中间把字符串分为两部分。分别取得两部分的公共前缀，然后再取左边和右边的公共前缀就好。

```
public String longestCommonPrefix(String[] strs) {
		if(strs.length == 0) {
			return "";
		}
		return longestCommonPrefix(strs, 0, strs.length-1);
	}
	
	
	private String longestCommonPrefix(String[] strs, int l, int r) {
		// TODO Auto-generated method stub
		if(l == r) {
			return strs[l];
		}
		int mid = (l+r)/2;
		String lcpLeft = longestCommonPrefix(strs, l, mid);
		String lcpRight = longestCommonPrefix(strs, mid+1, r);
		return commonPrefix(lcpLeft, lcpRight);
		
	}


	private String commonPrefix(String left, String right) {
		// TODO Auto-generated method stub
		int min = Math.min(left.length(), right.length());
		for(int i=0; i<min; i++) {
			if(left.charAt(i) != right.charAt(i)) {
				return left.substring(0, i);
			}
		}
		return left.substring(0, min);
	}
```

## 思路四：二分查找法

思路是这样的：

1、先从所有字符串里找到最短的字符串，最大公共前缀不会超过最短字符串的长度的。

2、把最短字符串从中间切分开，把前半部分依次判断是否所有字符串的前缀。然后安装二分法的思路，对前半部分进行加长或者截断操作，找到最大的长度。

```
public String longestCommonPrefix(String[] strs) {
		if(strs.length == 0) {
			return "";
		}
		int minLen = Integer.MAX_VALUE;
		for(String str: strs) {
			minLen = Math.min(minLen, str.length());
		}
		int low = 1;
		int high = minLen;
		while(low <= high) {
			int mid = (low+high)/2;
			if(isPrefix(strs, mid)) {
				low = mid + 1;
			} else {
				high = mid -1;
			}
		}
		return strs[0].substring(0, (low+high)/2);
	}
	
	private boolean isPrefix(String[] strs, int len) {
		// TODO Auto-generated method stub
		for(int i=0; i<strs.length; i++) {
			if(!strs[i].startsWith(strs[0].substring(0, len))) {
				return false;
			}
		}
		return true;
	}
```

## 思路五：Trie法

这个更加高级了。先不看了。



# 15. 三数之和为0

给一个数组，把里面三个元素相加之和为0的组合找出来。

```
public class Test {
	public List<List<Integer>> threeSum(int[] nums) {
	    List<List<Integer>> res = new ArrayList<>();
	    Arrays.sort(nums);
	    for (int i = 0; i + 2 < nums.length; i++) {
	        if (i > 0 && nums[i] == nums[i - 1]) {              // skip same result
	            continue;
	        }
	        int j = i + 1, k = nums.length - 1;  
	        int target = -nums[i];
	        while (j < k) {
	            if (nums[j] + nums[k] == target) {
	                res.add(Arrays.asList(nums[i], nums[j], nums[k]));
	                j++;
	                k--;
	                while (j < k && nums[j] == nums[j - 1]) j++;  // skip same result
	                while (j < k && nums[k] == nums[k + 1]) k--;  // skip same result
	            } else if (nums[j] + nums[k] > target) {
	                k--;
	            } else {
	                j++;
	            }
	        }
	    }
	    return res;
	}

	public static void main(String[] args) {
		Test test = new Test();
		int[] nums = {1, -1, 0, 2, -2, 1};
		List<List<Integer>> res = new ArrayList<>();
		res = test.threeSum(nums);
		for(int i=0; i<res.size(); i++) {
			List<Integer> l = res.get(i);
			System.out.println("");
			System.out.println("list[" + i + "]");
			for(int j=0; j<l.size(); j++) {
				System.out.print(" " + l.get(j));
			}
		}
	}
}
```

# 16. 三数之和最接近给定值

跟第15题的区别在于和的值是通过参数传递进来的，不是0。

先不细看。

# 17. 九宫格键盘数字可能的字母组合

就是我们平时九宫格进行英文输入的那个判断。这个还是一个很实际的问题。

但是问题描述不是很清楚，所以答案各有区别。

这个还没有正式的答案，讨论里的最高票答案是这样的。

```
public class Test {
	public List<String> letterCombinations(String digits) {
		LinkedList<String> ans = new LinkedList<String>();
		String[] mapping = new String[] { "0", "1", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz" };
		ans.add("");
		for (int i = 0; i < digits.length(); i++) {
			int x = Character.getNumericValue(digits.charAt(i));
			while (ans.peek().length() == i) {
				String t = ans.remove();
				for (char s : mapping[x].toCharArray())
					ans.add(t + s);
			}
		}
		return ans;
	}

	public static void main(String[] args) {
		Test test = new Test();
		List<String> list = test.letterCombinations("23");
		for (int i = 0; i < list.size(); i++) {
			System.out.println("list[" + i + "]" + list.get(i));
		}
	}
}
```

# 18. 四个数之和为0

跟前面的三个数之和为0的类似。

不看了。

# 19. 把linkedlist的从最后数起的第n个元素删除

有个要求：要用one pass来完成（one pass的具体含义是什么？）

one pass是指遍历一次list。

##思路一：先看two pass的方法

倒着数的，还是可以被化归为正着数的。倒数第n个，就是正数第L+1-n个。

L代表的是链表的长度。

我们先添加一个辅助的dummy节点。这个dummy节点指向list head。

dummy 节点是用来简化一些边界情况的。例如：list只有一个node，或者从list head上移除node。

现在我们的先遍历一次，得到长度L。

再遍历第二次。把L+1-n这个节点移除。

# 20. 判断字符串里的括号是否合法

判断大中小括号配对是否合法。不是我们一般理解的那种，还是很简单的那种。就是给连续的括号：

```
()[]{}
```

所以问题其实是比较简单的。

正式答案还没有。看最高票的答案。

用的是stack来解答的。

```
public class Test {
	public boolean isValid(String str) {
		Stack<Character> stack = new Stack<Character>();
		for(char c: str.toCharArray()) {
			if (c == '(') {
				stack.push(')');
			} else if(c == '[') {
				stack.push(']');
			} else if(c == '{') {
				stack.push('}');
			} else if(stack.isEmpty() || stack.pop() != c) {
				return false;
			}
		}
		return stack.isEmpty();
	}
	//@SuppressWarnings("unused")
	public static void main(String[] args) {
		Test test = new Test();
		boolean res = test.isValid("()");
		System.out.println("res:" + res);
	}
}
```









