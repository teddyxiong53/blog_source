---
title: C语言笔试题解法
date: 2017-02-26 18:45:50
tags:
---
# 1. 组合种类的求解
递归法：
```
#include <stdio.h>
#define MAXN 100
int a[MAXN]={0};
int counts=0;
void  comb(int m,int k)
{     int i,j;
      for (i=m;i>=k;i--)
      { 
          a[k]=i;
          if (k>1)
              comb(i-1,k-1);
          else
          {   
              counts++;              
              for (j=a[0];j>0;j--)
                  printf("%d ",a[j]);
              printf("\n");
              
          }
      }
}
int main()
{   
      int m,r;
      printf("Please input m:");
      scanf("%d",&m);
      printf("Please input n:");
      scanf("%d",&r);
      counts=0;
      a[0]=r;
      comb(m,r);
      printf("All kinds is:%d\n",counts);
      return 0;
}
```
# 2. 读程序段，回答问题  
```
int main(int argc,char *argv[])  
{  
int c=9,d=0;  
c=c++%5;  
d=c;  
printf("d=%d\n",d);  
return 0;  
}  
```
a) 写出程序输出  
b) 在一个可移植的系统中这种表达式是否存在风险？why?  
有的机器会是4（我测试就是这样），有的会是5。取决于编译器的。
这种问题并没有太大的意义。

# 3. 分析这个中断处理函数的错误。
```
__interrupt double compute_area(double radius)  
{  
double area = PI * radius *radius;  
printf("nArea = %f", area);  
return area;  
}  
```
由4个错误：
1. 不能有返回值。
2. 不能有参数。
3. 浮点数一般是不可重入的。
4. printf函数是有性能和重入问题的。


