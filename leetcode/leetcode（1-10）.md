---
title: leetcode（1-10）
date: 2017-12-20 20:12:22
tags:
	- leetcode

---



现在我要快速把leetcode刷一遍。每10题总结一篇文章。就按顺序来。如果暂时觉得不需要做的，先把位置空着。

# 1. Two Sum

两数之和。这个已经有一篇文章总结了。不难。

我自己写的第一个版本。最自然简单的解决方法。

```
int * twoSum(int *sums, int numSize, int target)
{
    int *a = sums;
    int i,j;
    for(i=0; i<numSize-1; i++) {
        for(j=i+1; j<numSize; j++) {
            if(a[i]+a[j] == target) {
                //printf("[%d,%d]\n", i,j );
                return NULL;
            }
        }
    }
    return NULL;
}
int main(int argc, char const *argv[])
{
    int sums[5] = {2,3,8,7,9};
    twoSum(sums, 5, 16);
    return 0;

}
```

复杂度高了。



# 2. 两个列表内容相加

这个没有一个好的答案。不管。

我自己写了一个，还不能正常工作。

```
#include <stdio.h>
#include <unistd.h>

struct ListNode {
    int val;
    struct ListNode *next;
};

int list_len(struct ListNode *list) {
    int i = 0;
    while(list) {
        i++;
        list = list->next;
    }
    return i;
}
struct ListNode *add(struct ListNode *l1, struct ListNode* l2) {
    int len1 = list_len(l1);
    int len2 = list_len(l2);
    int len = len1>len2? len1 : len2;
    struct ListNode *p = malloc(len*sizeof(struct ListNode));
    memset(p, 0, len*sizeof(struct ListNode));
    struct ListNode *p1, *p2;
    p1 = l1;
    p2 = l2;
    int over = 0;
    while(p1 && p2) {
        p->val = (p1->val + p2->val)%10 + over ;
        if(p1->val + p2->val > 10) {
            over = 1;
        } else {
            over = 0;
        }

        p->next = (struct ListNode *)((unsigned char *) p + sizeof(struct ListNode));
        p = p->next;
        p1 = p1->next;
        p2 = p2->next;
    }
    return p;
}


int main(int argc, char const *argv[])
{
    struct ListNode l1_0, l1_1, l1_2;
    printf("input 3 number :\n");
    scanf("%d %d %d", &l1_0.val, &l1_1.val, &l1_2.val);
    l1_0.next = &l1_1;
    l1_1.next = &l1_2;
    l1_2.next = NULL;
    struct ListNode *l1 = &l1_0;

    printf("input other 3 number: \n");
    struct ListNode l2_0, l2_1, l2_2;
    scanf("%d %d %d", &l2_0.val, &l2_1.val, &l2_2.val);
    l2_0.next = &l2_1;
    l2_1.next = &l2_2;
    l2_2.next = NULL;
    struct ListNode *l2 = &l2_0;

    struct ListNode *sum = add(l1, l2);
    while(sum) {
        printf("%d", sum->val);
        sum = sum->next;
    }
    printf("\n");
    free(sum);
    return 0;
}


```



# 3. 从一个字符串里取最长的没有重复字符的子串

我自己写了一个，是错的。

```
int lengthOfLongestSubstring(char *str) {
    int i,j;
    int len = 0;
    int max_len = 0;
    for(i=0; i<strlen(str)-1; i++) {
        char cur_char = str[i];
        for(j=i+1; str[j]!='\0'; j++) {
            if(cur_char == str[j]) {
                printf("cur_char:%c, j:%d\n", cur_char, j);
                break;
            }
        }
        len = j-i;
        if(len > max_len) {
            printf("len:%d\n", len);
            max_len = len;
        }

    }
    return max_len;
}

int main(int argc, char const *argv[])
{
    char *str1 = "abcabcbb";
    printf("max len:%d\n", lengthOfLongestSubstring(str1));
    return 0;
}

```



新建一个java文件Test.java。写入下面的内容：

```
import java.util.Set;
import java.util.HashSet;
public class Test {
	public int lengthOfLongestSubstring(String s) {
		int n = s.length();
		int ans = 0;
		for (int i=0; i<n;i++) {
			for (int j=i+1; j<=n; j++) {
				if(allUnique(s, i, j)) {
					if (ans < j-i) {
						ans = j - i;
					}
				}
			}
		}
		return ans;
	}
	public boolean allUnique(String s, int start, int end) {
		Set<Character> set = new HashSet<>();
		for(int i=start; i< end; i++) {
			Character ch = s.charAt(i);
			if(set.contains(ch)) {
				return false;
			}
			set.add(ch);
		}
		return true;
	}
	
	public static void main(String[] args) {
		String str = new String("ifthisagoodthing");
		Test Test = new Test();
		int len = Test.lengthOfLongestSubstring(str);
		System.out.println("len: " + len);
	}
}
```

这个是一个最简单直接的实现。采用了3层循环。所以时间复杂度是O(n^3)。

这个是不可接受的。我们要在这个基础上进行改进。

在上面的算法中，我们反复检查了子串里是否有重复的字符，这个是没有必要的，如果s[i,j]中，s[i,j-1]已经确认没有重复的字符了。那么只需要看s[j]是否在s[i,j-1]里就可以了。

有个方法，叫做滑动窗口。滑动窗口是一个抽象的概念，经常用来处理字符串问题。

```
	public int lengthOfLongestSubstring(String s) {
		int n = s.length();
		Set<Character> set = new HashSet<>();
		int ans=0, i=0, j=0;
		while(i<n && j <n) {
			if(!set.contains(s.charAt(j))) {
				set.add(s.charAt(j++));
				if( ans < j-i) {
					ans = j-i;
				}
			} else {
				set.remove(s.charAt(i++));
			}
			
		}
		return ans;
	}
```

现在已经被优化到O(n)了。只有一层循环。

但是实际上还是可以进一步优化的。用HashMap来做。上面实际上是O(2n)，我们可以继续优化到O(n)。

暂时不深入看。

另外还有一个巧妙的方法来做。也先不细看。

# 4. 求两个排序好的数组的中间值

这个题目有点看不懂。对排序的时间复杂度有要求。

# 5. 最长回文子串

##思路一

一个很直接的思路是，把字符串反过来，找反序字符串和原字符串的相同部分。这种方法不能对所有情况都管用。

我们现在用这种思路来做。每次找到一个最初的子串候选，我们检查子串的索引是不是跟原来的索引一样。如果是的，我们就更新当前的最长的回文子串，如果不是，我们就跳过，然后看下一个候选者。

这种方式的时间复杂度是O(n^2)，空间复杂度也是O(n^2)。

## 思路二

暴力方法。

字符串的长度是n。

这个的时间复杂度是O(n^3)，空间复杂度是O(1)。

## 思路三

要改进暴力法，我们首先要看如何避免在验证回文时的不必要的重复计算。

显然回文串是对称的。长度为奇数的回文串以最中间字符为对称轴，长度为偶数的回文串以中间空隙为对称轴。

这种对称性可以用来提高效率。

可以成为对称轴的，在一个长度为n的字符串里，有n+(n-1)个。（n个字符，n-1个空隙）。

从这些位置向左边和右边去遍历，直到左边和右边不同或者到达边界。

这个改进算法的时间复杂度是O(n^2)。

##思路四

这个就是当前的最优方案，叫做Manacher算法。

O(n^2)，对字符串很长时，难以接受这种效率。

先看思路三的缺点：

1、长度为奇偶性不确定导致需要分情况处理。

2、很多子串被重复多次访问。

针对第一个奇偶性的问题，可以采用在字符插入特定符号的方式来保证长度变成奇数。

我们下面的讨论就基于两个例子：aba和abba。

我们采用插入#号的方式：

```
aba变成：#a#b#a#
abba变成：#a#b#b#a#
```

插入字符串中不存在的符号，不会影响原字符串的回文特性。这样就解决了第一个问题。

接下来看重复访问的问题。

引入一个概念：回文半径。

回文半径是指回文子串中最左边或者最右边的字符与它的对称轴的距离。现在定义一个回文半径数组RL。

```
char: # a # b # a #
RL:   1 2 1 4 1 2 1
RL-1: 0 1 0 3 0 1 0
i :   0 1 2 3 4 5 6
```

通过观察上面的内容，可以得出结论：RL-1的值，就是原字符串中，以位置i为对称轴的最长回文串的长度。

所以，只要我们得到了RL数组的内容，就解决了这个问题。

https://segmentfault.com/a/1190000003914228

这里文章有详细描述。

看到这里，我感觉有不少的算法问题，是西方人完的文字游戏的解决。

# 6. ZigZag 转换

这个没有什么意思，看踩的人很多，真的是个无意义的文字游戏。

# 7. 反转整数

就是把整数倒过来写，把得到的数值得到，如果0排到右边最前面了，就没意义。

这个确实是一个简单的问题。我先自己想一想。

最直接的想法是，求出每一位的数值。

Python的话，可以很容易把一个数值变成一个字符串。然后就处理字符串。但是无疑这个是不好的解决方法，已经偏移了考察的核心了。重点考察的是数字运算，而不是字符串处理。

避免反复条件判断的解决办法就是用循环。

```
public class Test {
	public int reverse(int x) {
		int val = 0;
		while(x != 0) {
			val = val*10 + x%10;
			x = x/10;
			if(val > Integer.MAX_VALUE || val < Integer.MIN_VALUE) {
				return 0;
			}
		}
		return val;
	}
	
	public static void main(String[] args) {
		String str = new String("ifthisagoodthing");
		Test test = new Test();
		int val = test.reverse(1234);
		System.out.println("val: " + val);
		val = test.reverse(-1234);
		System.out.println("val: " + val);
		val = test.reverse(12340);
		System.out.println("val: " + val);
	}
}
```

# 8. atoi的实现

这个就不做了。

# 9. 回文数字

判断一个数字是否是回文数字，不要使用多余的空间。

我的思路是：

先把一个数字倒序一下，然后看倒序后的值和倒序前的值是否相等就可以了。

但是，看网上给的说明，说可能倒序后，数字就溢出了。这个的确是可能的。给出的解决方法是把数字的半截进行倒序，跟剩下的半截进行比较判断。这个的确是好的方法。

那怎么取到数字的半截呢？

下面是我自己写的。用了3个函数。我感觉不简洁。

```
public class Test {
	public  int reverse(int x) {
		int val = 0;
		while(x != 0) {
			val = val*10 + x%10;
			x = x/10;
			
		}
		return val;
	}
	public int getDigitLen(int x) {
		int digitLen = 0;
		if(x == 0) {
			return 1;
		}
		while(x != 0) {
			x = x/10;
			digitLen ++;
		}
		return digitLen;
	}
	public boolean isPlalindrome(int x) {
		//get the digit len
		int digitLen = getDigitLen(x);
		int halfLen = digitLen/2;
		int highHalf = x/(int)Math.pow(10, digitLen-halfLen);
		int lowHalf = x%(int)Math.pow(10,digitLen-halfLen);
		int highHalfReversed = this.reverse(highHalf);
		if(highHalfReversed == lowHalf) {
			return true;
		}
		return false;
	}
	
	public static void main(String[] args) {
		String str = new String("ifthisagoodthing");
		Test test = new Test();
		boolean isPlalindrome = test.isPlalindrome(1221);
		System.out.println("isPlalindrome: " + isPlalindrome);
	}
}
```

不过网上也没有给出好的代码。

# 10. 正则表达式匹配

实现正则表达式的”.“和”*“的匹配判断。

官网给了几种思路。

## 思路一

递归法。

暂时不细看。













