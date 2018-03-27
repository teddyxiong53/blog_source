---
title: uboot之启动过程分析（二）
date: 2018-03-27 10:08:08
tags:
	- uboot

---



我现在搭建了一个基于mini2440的qemu环境。基于这个环境再进行一次分析。

从Makefile里看，这个uboot版本是1.3.2的。属于比较老的。

现在是编译好的。我们先看看System.map文件的内容。

mini2440的sdram范围是0x3000 0000到0x3400 0000，一共64M。

System.map文件的最前面是这样的。链接的指定位置是sdram的最后512K的位置。这样就不容易跟kernel位置重叠了。

```
33f80000 T _start
33f80020 t _undefined_instruction
33f80024 t _software_interrupt
33f80028 t _prefetch_abort
33f8002c t _data_abort
33f80030 t _not_used
33f80034 t _irq
33f80038 t _fiq
33f80040 T preboot_override
33f80044 T booted_from_nand
33f80048 t _booted_from_nand
33f8004c T booted_from_nor
33f80050 t _booted_from_nor
33f80054 t _end_if_0
33f80058 t _TEXT_BASE
33f8005c T _armboot_start
33f80060 T _bss_start
33f80064 T _bss_end
```



uboot代码的目录结构在这么些年里，也有不小的调整。

启动文件在cpu/arm920t/start.S里。

生成的配置文件是include/autoconf.mk。

看看里面有什么内容。

```
系统时钟配置为12M
CONFIG_RTC_S3C24X0=y
CONFIG_STACKSIZE="(128*1024)"
CONFIG_ETHADDR="08:08:11:18:12:27"
CONFIG_S3C2410_NAND_BBT=y
CONFIG_NAND_DYNPART=y
CONFIG_BOOTARGS="root=/dev/mtdblock3 rootfstype=jffs2 console=ttySAC0,115200"
CONFIG_DM9000_BASE="0x20000300"
CONFIG_JFFS2_NAND=y
CONFIG_DM9000_BASE="0x20000300"
CONFIG_S3C2410_NAND_BOOT=y  #这个是使能的。这个从System.map里也可以看出。
CONFIG_DRIVER_DM9000_NO_EEPROM=y
```

对应的配置头文件。include/configs/mini2440.h。

```
#define CONFIG_S3C2410_NAND_BOOT	1
#define CONFIG_S3C2410_NAND_SKIP_BAD	1
#define CFG_UBOOT_SIZE		0x40000 /* size of u-boot, for NAND loading */
#define CONFIG_ARM920T		1	/* This is an ARM920T Core	*/
#define	CONFIG_S3C2440		1	/* in a SAMSUNG S3C2440 SoC     */
#define CONFIG_MINI2440		1	/* on a MIN2440 Board  */
//允许超频。
#define CONFIG_MINI2440_OVERCLOCK 1	/* allow use of frequencies over 405Mhz */
#define CONFIG_SYS_CLK_FREQ	12000000
#define USE_920T_MMU		1
#define CFG_MALLOC_LEN		(CFG_ENV_SIZE + 2048*1024)//malloc长度是环境变量加2M。
#define CFG_GBL_DATA_SIZE	128	/* size in bytes reserved for initial data */

#define CONFIG_SERIAL1          1	/* we use SERIAL 1 on MINI2440 */
#define	CFG_PROMPT		"MINI2440 # "	

#define CFG_MEMTEST_START	0x30000000	/* memtest works on	*/
#define CFG_MEMTEST_END		0x33F00000	/* 63 MB in DRAM	*/

#define	CFG_LOAD_ADDR		0x32000000	/* default load address	*/

#define CONFIG_STACKSIZE	(128*1024)	/* regular stack */

```



继续回到start.S里。

开始执行的地方是start_code。

```
start_code:
	/*
	 * set the cpu to SVC32 mode
	 */
	mrs	r0,cpsr #把cpsr读取到r0里来进行操作。
	bic	r0,r0,#0x1f #最低5位清零。
	orr	r0,r0,#0xd3 #关闭中断，设置为ARM而不是thumb模式，设置为svcmode
	msr	cpsr,r0 #把改后的r0值写回到cpsr里。生效。
	
	ldr     r0, =pWTCON //关闭看门狗。
	mov     r1, #0x0
	str     r1, [r0]
	
	mov	r1, #0xffffffff //关闭所有中断。
	ldr	r0, =INTMSK
	str	r1, [r0]
	
	/* Make sure we get FCLK:HCLK:PCLK */
	ldr	r0, =CAMDIVN //把camera的关闭掉？
	mov	r1, #0
	str	r1, [r0]
	
	/* Clock asynchronous mode */
	mrc	p15, 0, r1, c1, c0, 0
	orr	r1, r1, #0xc0000000
	mcr	p15, 0, r1, c1, c0, 0
	
	/* enable uart */
	ldr	r0, =0x4c00000c		/* clkcon */
	ldr	r1, =0x7fff0		/* all clocks on */
	str	r1, [r0]
	
	/* gpio UART0 init */ //串口gpio复用配置。
	ldr	r0, =0x56000070
	mov	r1, #0xaa
	str	r1, [r0]
	
	/* init uart */  //串口波特率等配置。
	ldr	r0, =0x50000000
	mov	r1, #0x03
	str	r1, [r0]
	ldr	r1, =0x245
	str	r1, [r0, #0x04]
	mov	r1, #0x01
	str	r1, [r0, #0x08]
	mov	r1, #0x00
	str	r1, [r0, #0x0c]
	mov	r1, #0x1a
	str	r1, [r0, #0x28]
	
	bl	cpu_init_crit //
		这里面做了这些事情：
		1、刷cache。
		/*
         * flush v4 I/D caches
         */
        mov	r0, #0
        mcr	p15, 0, r0, c7, c7, 0	/* flush v3/v4 cache */
        mcr	p15, 0, r0, c8, c7, 0	/* flush v4 TLB */
		2、禁止mmu。
		/*
         * disable MMU stuff and caches
         */
        mrc	p15, 0, r0, c1, c0, 0
        bic	r0, r0, #0x00002300	@ clear bits 13, 9:8 (--V- --RS)
        bic	r0, r0, #0x00000087	@ clear bits 7, 2:0 (B--- -CAM)
        orr	r0, r0, #0x00000002	@ set bit 2 (A) Align
        orr	r0, r0, #0x00001000	@ set bit 12 (I) I-Cache
        mcr	p15, 0, r0, c1, c0, 0
		3、建立ram时序。因为ram时序是跟板子相关的。
		mov	ip, lr
		bl	lowlevel_init//这个在board/lowlevel_init.S里。
			做了这些事情：
			{
				就是一个配置寄存器的过程。
			}
		mov	lr, ip
		mov	pc, lr
	adr	r0, _start		/* r0 <- current position of code   */ 把当前pc值存入到r0里。
	#define	BWSCON	0x48000000
	ldr	r1, =BWSCON		/* Z = CPU booted from NAND	    */
	ldr	r1, [r1]
	tst	r1, #6			/* BWSCON[2:1] = OM[1:0]	    */
	teqeq	r0, #0			/* Z &= running at address 0	    */
	beq	nand_load
		{
			做了这些事情。
			bl	may_resume	//这个不管。
			mov	r1, #S3C2440_NAND_BASE
            ldr	r2, =0xfff0		@ initial value tacls=3,rph0=7,rph1=7
            ldr	r3, [r1, #oNFCONF]
            orr	r3, r3, r2
            str	r3, [r1, #oNFCONF]

            ldr	r3, [r1, #oNFCONT]
            orr	r3, r3, #1		@ enable nand controller
            str	r3, [r1, #oNFCONT]
            
            ldr	r0, _TEXT_BASE		/* upper 128 KiB: relocated uboot   */
            sub	r0, r0, #CFG_MALLOC_LEN	/* malloc area                      */
            sub	r0, r0, #CFG_GBL_DATA_SIZE /* bdinfo                        */
            
            	@ copy u-boot to RAM
                ldr	r0, _TEXT_BASE
                mov     r1, #0x0
                mov	r2, #CFG_UBOOT_SIZE
                bl	nand_read_ll //这个代码在cpu/arm920t/s3c24x0/nand_read.c里。

                tst	r0, #0x0
                beq	ok_nand_read
		}
		//到这里，已经从nand里把内容读取到sdram里了。应该可以直接读取到目标位置吧。
	relocate:				/* relocate U-Boot to RAM	    */
      teq	r0, #0			/* running at address 0 ?	    */
      bleq	may_resume		/* yes -> do low-level setup	    */
      adr	r0, _start		/* the above may have clobbered r0  */

      ldr	r1, _TEXT_BASE		/* test if we run from flash or RAM */
      cmp     r0, r1                  /* don't reloc during debug         */
      beq     done_relocate

      ldr	r2, _armboot_start
      ldr	r3, _bss_start
      sub	r2, r3, r2		/* r2 <- size of armboot            */
      add	r2, r0, r2		/* r2 <- source end address         */
   copy_loop: //这里就是重定位的拷贝。
	ldmia	r0!, {r3-r10}		/* copy from source address [r0]    */
	stmia	r1!, {r3-r10}		/* copy to   target address [r1]    */
	cmp	r0, r2			/* until source end address [r2]    */
	ble	copy_loop
	
		mov	r0, #0			/* flush v3/v4 cache */
	mcr	p15, 0, r0, c7, c7, 0
	ldr	pc, _done_relocate	/* jump to relocated code */
_done_relocate:
	.word	done_relocate
	{
		这里做了这些事情。
		1、拷贝向量表。
		mov	r0, #0
      ldr	r1, _TEXT_BASE
      mov	r2, #0x40
  irqvec_cpy_next:
      ldr	r3, [r1], #4
      str	r3, [r0], #4
      subs	r2, r2, #4
      bne	irqvec_cpy_next
      然后建立堆栈。
      清bss
      最后调用到start_armboot
      ldr	pc, _start_armboot
_start_armboot:	.word start_armboot
	}
```

汇编阶段的总体过程就是上面这些了。

我们现在要理一下其中几个关键的地址。

1、重定位是从哪里拷贝到哪里。



```
arm-none-eabi-ld -Bstatic -T /home/teddy/work/mini2440-lab/uboot/uboot/board/mini2440/u-boot.lds  --defsym raise=hang -Ttext 0x33F80000 $UNDEF_SYM cpu/arm920t/start.o
```

