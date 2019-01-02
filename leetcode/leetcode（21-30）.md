---
title: leetcode（21-30）
date: 2017-12-28 14:58:55
tags:
	- leetcode

---



# 21. 合并两个排序好的list

## 思路一：递归法

基本思路是：

1、list1[0] + merge(list[1:],list2) 如果list1[0] < list2[0]

2、list2[0] + merge(list2[1:], list1) 否则

代码实现如下：

```
class ListNode {
	int val;
	ListNode next;
	ListNode head;
	public ListNode(int value) {
		this.val = value;
		
	}
	@Override
	public String toString() {
		// TODO Auto-generated method stub
		//return super.toString();
		StringBuffer res = new StringBuffer();
		ListNode l = this;
		while(l != null) {
			res.append(l.val);
			l = l.next;
		}
		return res.toString();
	}
}
public class Test {
	public ListNode merge(ListNode list1, ListNode list2) {
		
		if(list1 == null) {
			return list2;
		}
		if(list2 == null) {
			return list1;
		}
		if(list1.val < list2.val) {
			list1.next = merge(list1.next, list2);
			return list1;
		} else {
			list2.next = merge(list2.next, list1);
			return list2;
		}
		
	}
	//@SuppressWarnings("unused")
	public static void main(String[] args) {
		Test test = new Test();
		ListNode list1 = new ListNode(1);
		list1.next = new ListNode(3);
		list1.next.next = new ListNode(5);
		
		ListNode list2 = new ListNode(2);
		list2.next = new ListNode(4);
		list2.next.next = new ListNode(6);
		
		ListNode listMerge = test.merge(list1, list2);
		System.out.println("listMerge:" + listMerge);
		
	}
	
}
```

我实现了ListNode的toString方法。

## 思路二：遍历法。

我们可以假定list1的每个元素都比list2的小，然后把list2的元素逐个插入到list1里面去。

我们还是需要设定一个辅助节点prehead，用来很容易地返回list_merge的head。

另外，再提供一个辅助节点prev。

（我觉得辅助节点这种提法特别好，这样我就把算法跟之前学习数学里的辅助线的思路对接起来了。）

```
	public ListNode merge(ListNode list1, ListNode list2) {
		ListNode prehead = new ListNode(-1);
		ListNode prev = prehead;
		
		while(list1 != null && list2 != null) {
			if(list1.val <= list2.val) {
				prev.next = list1;
				list1 = list1.next;
			} else {
				prev.next = list2;
				list2 = list2.next;
			}
			prev = prev.next;
		}
		if(list1 == null) {
			prev.next = list2;
		} else {
			prev.next = list1;
		}
		return prehead.next;
	}
```

# 22. 产生配对的括号

例如给n=2，那么可以产生的正确结果有：

```
()()
(())
```

## 思路一：暴力法

当n为2的时候，总共有4个位置，每个位置有2种可能（左括号或者右括号）。所以总共是2^4=16种可能。

当n为3的时候，是2^6种可能。

所以规律是2^(2*n)中可能。

把所有的结果得到后，然后判断里面合法的结果，就得到最终结果。

需要用递归法。收敛条件是所有空都填满了。

所有的递归都可以用循环来替代。

```
public class Test {
	public List<String> generateParenthesis(int n) {
		List<String> res = new ArrayList<>();
		
		generateAll(new char[2*n], 0, res);
		
		return res;
	}
	private void generateAll(char[] current, int pos, List<String> res) {
		// TODO Auto-generated method stub
		if(pos == current.length) {
			if(isValid(current)) {
				res.add(new String(current));
			} 
		} else {
			current[pos] = '(';
			generateAll(current, pos+1, res);
			current[pos] = ')';
			generateAll(current, pos+1, res);
			
		}
	}
	private boolean isValid(char[] current) {
		// TODO Auto-generated method stub
		
		return true;
	}
	public static void main(String[] args) {
		Test test = new Test();
		List<String> res = test.generateParenthesis(2);
		for(int i=0; i<res.size(); i++ ) {
			System.out.println("res[" + i + "]" + res.get(i));
		}
	}
}
```

上面的isValid直接返回了true。这样是把所有可能都打印出来了。我们现在把isValid改一下，就可以把有效的打印出来了。

```
private boolean isValid(char[] current) {
		// TODO Auto-generated method stub
		int balance = 0;
		for(char c: current) {
			if(c == '(') {
				balance ++;
			} else {
				balance --;
			}
			if(balance < 0) {
				return false;
			}
			
		}
		return (balance == 0);
	}
```

另外还有两种思路。先不看。

# 23. 合并k个排序好的list

这个跟前面的合并2个排序好的list是类似的，只是list的个数现在是不固定的。



# 28. jump game

一个非负整数数组，从第一个元素开始，往后跳所在位置的数字的格数，看是否可以跳到最后一个元素上去。

调到超出也算是好的。就那种碰到0的就卡住了那种不行。

## 分析

如果从某个位置往后跳，可以调到最后一个元素，那么我们把这个位置叫做good index。否则叫bad  index。

然后这个问题就变成了一个判断index 0是good还是bad的问题了。



这个问题是一个动态编程的问题。

一般来说，解决一个动态编程的问题需要4个步骤：

1、先用递归回溯的方法。

2、使用一个标记表来优化。

3、去掉递归。

4、进一步优化时间和空间占用。



## 思路一

这个是一个最直观的解决方法。

```
public class Solution {
	boolean canJumpFromPositon(int pos, int[] nums) {
		if(pos == nums.length -1 ) {
			return true;
		}
		int furthestJump = Math.min(pos+nums[pos] , num.length-1);
		for(int i=pos+1; i<=furthestJump; i++) {
			if(canJumpFromPositon(i, nums)) {
				return true;
			}
		}
	}
	boolean canJump(int[] nums) {
		return canJumpFromPositon(0, nums);
	}
}
```

一个简单的优化就是，从右往左进行检查，而不是从左往右。

理论上最坏的情况从左往右和从右往左是一样的，但是实际情况，从右往左效率要高些。

## 思路二

top-down动态编程可以看做是回溯法的优化。



我现在的观点是：系统底层开发虽然难度较大，但是并不是这个时代最需要的，这个时代最需要的还是AI开发相关的。





