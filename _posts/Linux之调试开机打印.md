---
title: Linux之调试开机打印
date: 2018-03-04 22:25:36
tags:
	- Linux

---



# 内核启动时挂死

用printascii函数。

这个函数是在linux/arch/arm/kernel/debug.S里。汇编写的。

```
ENTRY(printascii)
		addruart_current r3, r1, r2
		b	2f
1:		waituart r2, r3
		senduart r1, r3
		busyuart r2, r3
		teq	r1, #'\n'
		moveq	r1, #'\r'
		beq	1b
2:		teq	r0, #0
		ldrneb	r1, [r0], #1
		teqne	r1, #0
		bne	1b
		ret	lr
ENDPROC(printascii)
```

用printascii函数跟踪start_kernel有没有执行。

还有一种方法，把printascii加到printk里去。

```
extern void printascii(const char *);//add
static char printk_buf[1024];//add
printk()
{
  //...
  va_end(args);
  printascii(printk_buf);/add
  return r;
}
```



# 在mylinuxlab里实验

```
static inline void prepare_page_table(void)
{
	unsigned long addr;
	phys_addr_t end;
	pr_notice("xhl -- pr_notice");
	printascii("xhl -- pmd size 111");
	printk("xhl -- pmd size:%d \n", PMD_SIZE);
```

我在这里加了3行打印，只有pr_notice打印出来了。

我当前的配置。

```
#define CONFIG_MESSAGE_LOGLEVEL_DEFAULT 7
```

