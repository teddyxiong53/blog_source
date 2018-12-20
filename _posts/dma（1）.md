---
title: dma（1）
date: 2018-02-28 10:56:38
tags:
	- dma

---



# dma分类

目前有2种dma方式：

1、分散聚合dma。scatter gather。

要传输的数据可以不连续。用链表组织起来。这个效率更高。

整个链表传输完再产生一次中断。

2、块dma。block dma。

数据是连续的一整块内存。



# linux的dma框架

Linux实现的dma框架叫dma engine。驱动开发者要按照固定的流程来编码，才能正确使用dma功能。

使用流程是：

1、分配一个dma slave channel。

2、设置slave和controller的参数。

3、为本次传输拿到一个描述符。

4、提交传输请求给dma engine。

5、开始传输。

6、等待完成。

一个驱动的例子如下。

```
struct completion finished;
struct dma_chan *dmachn;

struct dma_async_tx_descriptor *tx = NULL;

#define DEST_ADDR 0x73800000
#define SRC_ADDR 0x10400000

static int mydma_mmap(struct file *file, struct vm_area_struct *vma)
{
    int size;
    size = vma->vm_end - vma->vm_start;
    remap_pfn_range(vma, vma->vm_start ,DEST_ADDR>>PAGE_SHIFT, 0x800000, vma->vm_page_prot);
    return 0;
}

static void dma_complete_func(void *completion)
{
    complete(completion);
}
static int mydma_ioctl(struct inode *inode, struct file* file, int num, int param)
{
    struct dma_device *dmadev;
    enum dma_ctrl_flags flags;
    dmadev = dmachn->device;
    flags = DMA_CTRL_ACK | DMA_COMPL_SKIP_DEST_UNMAP | DMA_COMPL_SKIP_SRC_UNMAP;
    tx = dmadev->device_prep_dma_memcpy(dmachn, DEST_ADDR, SRC_ADDR*param*0x40000, 0x40000, flags);
    if(!tx)
    {
        printk("failed to prepare dma memcpy\n");
        return -1;
    }
    init_completion(&finished);
    tx->callback = dma_complete_func;
    tx->callback_param = &finished;

    dma_cookie_t cookie;
    cookie = tx->tx_submit(tx);
    if(dma_submit_error(cookie)) {
        printk("failed to do dma tx submit \n");
        return -1;
    }
    dma_async_issue_pending(dmachn);
    wait_for_completion(&finished);
    return 0;
}
static struct file_operations fpga_fops = {
    .owner = THIS_MODULE,
    .mmap = mydma_mmap,
    .ioctl = mydma_ioctl,
};
static init mydma_init(void)
{
    dev_t fpga_dev;
    struct cdev *fpga_cdev;
    dma_addr_t addr;
    dma_cap_mask_t mask;
    dma_cap_zero(mask);
    dma_cap_set(DMA_MEMCPY, mask);
    dmachn = dma_request_channel(mask, 0, NULL);

    if(register_chrdev_region(MKDEV(200,0), 1, "fpga"))
    {
        printk(KERN_ERR "alloc chrdev failed\n");
        return -1;
    }
    fpga_cdev = cdev_alloc();
    fpga_cdev->ops = &fpga_fops;
    fpga_cdev->owner = THIS_MODULE;
    if(cdev_add(fpga_cdev, MKDEV(200, 0), 1))
    {
        printk(KERN_ERR "cdev add failed \n");
        return -1;
    }
    printk("fpga driver loaded \n");
    return 0;
}
```

