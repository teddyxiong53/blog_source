---
title: gui之ge2d
date: 2021-06-25 13:31:33
tags:
	- gui

---

--

2D图形引擎（GE2D）专门用于提高图形性能处理。

它可以加速单个GUI功能的操作，

如BitBLT和Bresenham线绘制在所有像素深度上运行，包括每像素8/16/32位。



像素是MicrosoftWindows中定义的最小可寻址屏幕元素，以及线和图片由各种像素组成。 

GE2D用于加快像素中的图形性能数据移动和线条绘制，

以及加速几乎所有的计算机图形布尔值通过消除CPU开销进行操作。

同时，旋转和缩小的功能实现了一些特殊应用。

在图像缩小功能中，均可编程水平和垂直N / M缩放因子用于调整图像大小。

对于2D旋转时，可以向左或向右旋转45度，90度或180度，并且还支持弹动/翻牌，镜像或上下相反的图片。



在AXG A113D S400板子上，测试GE2D

先跑一下ge2d_chip_check

需要/dev/ion设备。ion设备的驱动是有的。

但是设备树里没有配置。

从其他的配置里找一份拷贝过来。

```
/ {
	//...
	ion_dev {
		compatible = "amlogic, ion_dev";
		memory-region = <&ion_reserved>;
	};
	reserved-memory {
		//...
		ion_reserved:linux,ion-dev {
			compatible = "shared-dma-pool";
			reusable;
			size = <0x0 0x2000000>;
			alignment = <0x0 0x400000>;
		};
	}
}
```

烧录设备树，运行，可以看到设备节点有了。

运行ge2d_chip_check，提示内存不够。

```
# ./ge2d_chip_check 
[   62.655295@1]- not enough mem for ION size 1228800, ret=-10001
```

那就先运行iontest。

iontest的选项：

```
static struct option opts[] = {
            {"ion_mem_alloc", no_argument, 0, 'c'},
            {"alloc", no_argument, 0, 'a'},
            {"alloc_flags", required_argument, 0, 'f'},
            {"heap_mask", required_argument, 0, 'h'},
            {"map", no_argument, 0, 'm'},
            {"share", no_argument, 0, 's'},
            {"len", required_argument, 0, 'l'},
            {"align", required_argument, 0, 'g'},
            {"map_flags", required_argument, 0, 'z'},
            {"prot", required_argument, 0, 'p'},
        };
```

主要看这4个选项：

```
case 'a':
            test = ALLOC_TEST;
            break;
        case 'm':
            test = MAP_TEST;
            break;
        case 's':
            test = SHARE_TEST;
            break;
        case 'c':
            test = IONMEM_TEST;
            break;
        }
```



跑ge2d_feature_test也是内存分配失败。

我把文件里的宽高从1920x1080改成720x720

至少内存不会分配失败了。

但是打开文件失败。这个文件不存在。

```
read source file:./fb1.rgb32 open error
```

需要我自己来生成这样的文件。

找脚本来把bmp图片转成fb可以直接显示的东西。

可以简单一点。先显示一下colorbar的测试。

然后：

```
dd if=/dev/fb0 of=/data/cbr
```

得到的cbr文件大小是24M。

但是cbr文件内容再写入到/dev/fb0，全是黑的。

不管。先保证有个文件可以用。

```
# cd /data/
# cp cbr fb1.rgb32
# cp cbr fb2.rgb32
# ./ge2d_
ge2d_chip_check    ge2d_feature_test
# ./ge2d_feature_test 
ThreadIdx -- 0, run time -- 0
plane_number=1,format=1
plane_number=1,format=1
plane_number=1,format=6
dma buffer alloc, index=0
dma buffer export, fd=5
do_strechblit test case:
separate_step=0 time=8 ms
ge2d feature_test exit!!!
# cat /proc/interrupts |grep ge2d
 37:          3          0          0          0     GIC-0 182 Edge      ge2d
```

这样可以运行不报错。

那现在可以找文件来做了。



```
R:16,G:8,B:0 
720x720, 32bpp
screensize=2073600 byte
```

用ffmpeg来进行转换。

```
ffmpeg -i 1.jpg -vcodec rawvideo -pix_fmt rgba raw1.rgb
```

这样得到的图片，至少是可以显示出来的。

虽然颜色不对。

现在测试ge2d_feature_test有效果。

说明ge2d没有问题。

以`./ge2d_feature_test --fillrect ff0000ff_0_0_500_500`为例进行分析。

看看是怎么实现的。

然后和directfb的fd_dok --fillrect进行对比。

看看有哪里不同。

```
typedef enum {
    AML_GE2D_FILLRECTANGLE,
    AML_GE2D_BLEND,
    AML_GE2D_STRETCHBLIT,
    AML_GE2D_BLIT,
    AML_GE2D_NONE,
} GE2DOP;
```

先看一下ge2d的驱动。

ge2d的内存类型：

```
enum ge2d_memtype_s {
	AML_GE2D_MEM_ION,
	AML_GE2D_MEM_DMABUF,
	AML_GE2D_MEM_INVALID,
};
```

当前我在directfb的时候，是没有使用ion的。那就是默认用dma？

dma方式可行吗？

是怎么决定使用哪种内存方式？

上面这个枚举，在kernel里没有看到哪里有用到。

ge2d_monitor_thread 这个内核线程。

有一个这样的ioctl。

GE2D_ATTACH_DMA_FD



```
enum ge2d_src_dst_e {
	OSD0_OSD0 = 0, 我们应该都是这个情况。
	OSD0_OSD1,
	OSD1_OSD1,
	OSD1_OSD0,
	ALLOC_OSD0,
	ALLOC_OSD1,
	ALLOC_ALLOC,
	TYPE_INVALID,
};
```

在驱动里，有：

```
ge2d_manager.buffer = ge2d_dma_buffer_create();
```

还有这个buf请求，是从dma请求的。

```
case GE2D_REQUEST_BUFF:
		ret = ge2d_buffer_alloc(&ge2d_req_buf);
```

在libge2d的代码里有：

```
ge2d_alloc_dma_buffer函数，用到了
ioctl(ge2d_fd, GE2D_REQUEST_BUFF, &buf_cfg);
```

libge2d的 aml_ge2d_mem_alloc函数，就区分了dma和ion内存的申请。

在directfb的对接代码里，怎么没有看到ge2d的内存申请？

搜索一下ge2d_fd，看看有哪些ioctl。

```
GE2D_SRCCOLORKEY
GE2D_SET_BLIT_PALETTE
GE2D_CONFIG_EX
GE2D_FILLRECTANGLE
GE2D_BLEND
GE2D_STRETCHBLIT_NOALPHA
GE2D_STRETCHBLIT

GE2D_BLIT_NOALPHA
GE2D_BLIT
```

当前的确是没有看到内存的申请的。

还是以fillrect为例，看directfb里的。

```
funcs->FillRectangle = amlFillRectangle;
```

上层是surface的函数。

在src/core/gfxcard.c里，

```
 card->funcs.FillRectangle( card->driver_data,
                                                    card->device_data, &rect );
```

再上层就是df_dok这样的程序里调用FillRectangle函数了。

分配的内存被怎样使用了？

拿到dma的fd。GE2D_EXP_BUFF

赋值给了

```
pge2d->ge2dinfo.src_info[0].shared_fd[i] = dma_fd;

//这个函数的作用是什么？
ret = ioctl(fd, GE2D_ATTACH_DMA_FD, &attach);

//最后画框是这里。
ioctl(fd, GE2D_FILLRECTANGLE, &op_ge2d_info);
```

directfb里的确是没有看到内存分配。搜索这个结构体ge2d_dmabuf_req_s也找不到。

如果没有分配内存，在驱动里处理，怎么判断的？

现在先停止这个方向。directfb的应该是需要修改才能跟现在的kernel匹配上。



# qt

```
看内核里有这个配置。
[*] Amlogic GE2D Module                  
[ ]   Amlogic GE2D not use physical addr  这个配置对qt那个有影响吗？
```

对应配置项是AMLOGIC_MEDIA_GE2D_MORE_SECURITY

作用是什么？

代码里，只有一个地方用到了。

```
#ifdef CONFIG_AMLOGIC_MEDIA_GE2D_MORE_SECURITY
	switch (cmd) {
	case GE2D_CONFIG:
	case GE2D_CONFIG32:
	case GE2D_CONFIG_EX:
	case GE2D_CONFIG_EX32:
		pr_err("ioctl not support.\n");
		return -EINVAL;
	}
#endif
```

就是不支持几个配置。

那这个配置项没有用。

把当前qt的改法理解清楚。

从原理上是否讲得通。

当前只在src/gui/painting/qpaintengine_raster.cp里的

```
void QSpanData::adjustSpanMethods()
函数的这个分支才起作用。
case Texture:
        unclipped_blend = qBlendTexture;
```

当前的问题在于，这个唯一的分支，还因为内部条件不满足要求而进不去。



qInitDrawhelperFunctions



把QFbScreen流程看一下。

mScreenImage这个成员变量的作用是什么？

我比较倾向于认为是绘制控制的层。事实是这样吗？

```
class Q_GUI_EXPORT QImage : public QPaintDevice
```



这个会在哪里被调用？如果有被调用，是不是这里导致QImage构造变了？

```
void QFbScreen::setGeometry(const QRect &rect)
{
    delete mPainter;
    mPainter = nullptr;
    mGeometry = rect;
    mScreenImage = QImage(mGeometry.size(), mFormat);
    QWindowSystemInterface::handleScreenGeometryChange(QPlatformScreen::screen(), geometry(), availableGeometry());
    resizeMaximizedWindows();
}
```



这个这么写：

```
    mScreenImage = QImage((uchar*)(mem + mGeometry.height()* mBytesPerLine), mGeometry.width(), mGeometry.height(), mBytesPerLine, mFormat);
```

mem为什么要加上后面这个值？

是指定到末尾？

qlinuxfbscreen.cpp里有一个

```
mFbScreenImage = QImage(mMmap.data, geometry.width(), geometry.height(), mBytesPerLine, mFormat);
```

qfbscreen.cpp里有一个：

```
    mScreenImage = QImage((uchar*)(mem + mGeometry.height()* mBytesPerLine), mGeometry.width(), mGeometry.height(), mBytesPerLine, mFormat);
```

这2个是什么关系？

qlinuxfbscreen.cpp调用了qfbscreen.cpp

qfbscreen.cpp应该提供了一些底层接口适配。

而qlinuxfbscreen.cpp是向上提供接口的。

QLinuxFbScreen.cpp有一个这样的doRedraw函数

```
QRegion QLinuxFbScreen::doRedraw()
{
    QRegion touched = QFbScreen::doRedraw();

    if (touched.isEmpty())
        return touched;

    if (!mBlitter)
        mBlitter = new QPainter(&mFbScreenImage);

    mBlitter->setCompositionMode(QPainter::CompositionMode_Source);
    for (const QRect &rect : touched)
        mBlitter->drawImage(rect, mScreenImage, rect);

    return touched;
}
```

在qfbscreen.cpp里，也有一个doRedraw。

```
if (!mPainter)
        mPainter = new QPainter(&mScreenImage);
```

绘制，应该靠的都是Painter。

QLinuxFbScreen调用了QFbScreen::doRedraw

```
QRegion QLinuxFbScreen::doRedraw()
{
    QRegion touched = QFbScreen::doRedraw();
```

QLinuxFbScreen::doRedraw谁调用了呢？

没有找到调用的地方。

QFbScreen::doRedraw在事件处理的里面有调用。

```
bool QFbScreen::event(QEvent *event)
{
    if (event->type() == QEvent::UpdateRequest) {
        doRedraw();
        mUpdatePending = false;
        return true;
    }
    return QObject::event(event);
}
```

event是继承自QObject的函数。

linuxfb的初始化是在这里调用的：

```
void QGuiApplicationPrivate::eventDispatcherReady()
{
    if (platform_integration == 0)
        createPlatformIntegration();

    platform_integration->initialize();
```

把初始化流程走一遍：

首先是QApplication的构造函数。这个调用是明确的，就是main里我们手动写的。

```
QApplication::QApplication(int &argc, char **argv, int _internal)
    : QGuiApplication(*new QApplicationPrivate(argc, argv, _internal))
{
    Q_D(QApplication);
    d->init();//这里就是调用QApplicationPrivate::init()
}
```

QApplicationPrivate::init()

```
调用QGuiApplicationPrivate::init();
后面的其他调用都不是重点。
```

QGuiApplicationPrivate::init()

```
调用QCoreApplicationPrivate::init();
```

QCoreApplicationPrivate::init()

```
调用eventDispatcherReady();

```

但是QGuiApplicationPrivate的这个函数才有内容。

```
void QGuiApplicationPrivate::eventDispatcherReady()
{
    if (platform_integration == 0)
        createPlatformIntegration();

    platform_integration->initialize();

    // All platforms should have added screens at this point. Finish
    // QHighDpiScaling initialization if it has not been done so already.
    if (!QGuiApplicationPrivate::highDpiScalingUpdated)
        QHighDpiScaling::updateHighDpiScaling();
}
```



```
class QLinuxFbScreen : public QFbScreen
```

因为Fb除了linux的，还有bsd的。

调用初始化，是从QLinuxFbScreen调用的。

那么改动，尽量是应该改动QLinuxFbScreen才对，不要改动父类QFbScreen才是合理的改法。

QLinuxFbIntegration应该是调用到QLinuxFbScreen的getfbinfo函数。然后我实现，在QLinuxFbScreen里进行相关的判断返回。

但是现在实际确实调用到了QFbScreen的函数了。怎么做到的？

```
unsigned long QLinuxFbIntegration::get_phy_info(unsigned long mem)
{
    return m_primaryScreen->getfbinfo(mem);
}
```

因为修改代码的人，对C++没有理解，是乱改的。

实际上应该调用子类的，但是因为Qt是采用面向接口编程的。

是一个父类指针，函数没有用virtual进行修饰，所以调用了父类的实现。

这个倒不会直接导致问题，只是代码混乱而已。

现在看这个函数：

```
void qBlendTexture(int count, const QSpan *spans, void *userData)
```

userData这个应该就是绘制元素的指针。

如果只是malloc的东西，那么地址在靠近0x10000开始的位置，可以理解。

因为arm架构的用户态程序的虚拟地址就是从这里开始的。

但是mmap映射得到的内存地址，传递给QImage。这个有什么作用呢？

按照我的理解，那么就是应该在这个内存上进行绘制操作。



QImage是一种绘图device。

```
enum PaintDeviceFlags {
        UnknownDevice = 0x00,
        Widget        = 0x01,
        Pixmap        = 0x02,
        Image         = 0x03,
        Printer       = 0x04,
        Picture       = 0x05,
        Pbuffer       = 0x06,    // GL pbuffer
        FramebufferObject = 0x07, // GL framebuffer object
        CustomRaster  = 0x08,
        MacQuartz     = 0x09,
        PaintBuffer   = 0x0a,
        OpenGL        = 0x0b
    };
```



```
adjustSpanMethods
这个函数被5个地方调用了。
都是在qpaintengine_raster.cpp里。
QRasterPaintEnginePrivate::updateMatrixData
qrasterpaintengine_dirty_clip
	被QRasterPaintEngine::clip调用。
QRasterPaintEngine::fillRect
QRasterPaintEngine::drawImage
QSpanData::setup
先给这些都加上打印。
绝大部分是setup调用的。有一些是fillRect调用的。
对应的QSpanData是QRasterPaintEnginePrivate里的solid_color_filler结构体。
那么这个对应的内存就是随机malloc处理的。没有什么明确特点。

QImage那个data，具体被怎么使用了？
赋值给了QImageData 的data指针。

```

QImage 构造函数，主要就是得到QImageData指针。



raster engine怎么操作QImage这个绘图设备的？

构造的时候，传递进来的：

```
QRasterPaintEngine::QRasterPaintEngine(QPaintDevice *device)
    : QPaintEngineEx(*(new QRasterPaintEnginePrivate))
{
    d_func()->device = device;
    init();
}
```

初始化的时候：

```
case QInternal::Image:
        format = d->rasterBuffer->prepare(static_cast<QImage *>(d->device));
```

这个prepare：

```
QImage::Format QRasterBuffer::prepare(QImage *image)
	m_buffer = (uchar *)image->bits();//这个就是把data赋值给了buffer。
```

m_buffer 又被哪些地方用到了呢？

```
uchar *buffer() const { return m_buffer; }
```

在qBlendTexture函数里

```
dst_addr = (unsigned long)(data->rasterBuffer->buffer());
```

就是这里用了。

按道理dst_addr应该符合地址大小的条件。

prepare为什么被调用了3次？为什么每次的地址不一样了？

```
	Line 32502: QImage::Format QRasterBuffer::prepare(QImage*) 3851, m_buffer:0xf1c05008
	Line 32539: QImage::Format QRasterBuffer::prepare(QImage*) 3851, m_buffer:0xf2944400
	Line 32554: QImage::Format QRasterBuffer::prepare(QImage*) 3851, m_buffer:0xf274a000
```

最后一次这个地址，是mmap的地址值。

那前面2个地址值是从哪里来的？

会有dst addr满足的情况

```
long unsigned int QFbScreen::getfbinfo(long unsigned int) 290, compare addr: mem:0x30918, vir_mem_base:0xf274a000
virtual long unsigned int QLinuxFbIntegration::get_phy_info(long unsigned int) 222,
long unsigned int QFbScreen::getfbinfo(long unsigned int) 290, compare addr: mem:0xf2944400, vir_mem_base:0xf274a000
void qBlendTexture(int, const QSpan*, void*) 5316, src_addr is continue:0, dst_addr is continue:1
```

但是src addr是铁定不满足的。

找一下src addr的赋值情况。

只有initTexture函数里进行了赋值。

QRasterPaintEngineState 这个类里，有2个QSpanData。

```
QSpanData penData;
QSpanData brushData;
```

QRasterPaintEngine::begin 这个函数什么时候调用？



```
void QSpanData::initTexture(
{
texture.imageData = d->data;//这个也有可能是来自于mmap的那个地址。
}
```

但是调用的地方都是这样：

```
if (!tempImage)
            tempImage = new QImage();
        *tempImage = rasterBuffer->colorizeBitmap(qt_imageForBrush(brushStyle, true), brush.color());
        initTexture(tempImage, alpha, QTextureData::Tiled);
```

QImage这样构造，data就是malloc的数据。

那就要看tempImage是不是有值了。

QSpanData的函数，应该只在qpainterengine_raster.cpp内部调用。

```
QRasterPaintEngine::updatePen
QRasterPaintEngine::updateBrush
QRasterPaintEngine::begin
```

QRasterPaintEngine的begin函数在哪里被调用？

应该是用父类指针来调用的。

这样构造的话，m_buffer就是0 

```
d->rasterBuffer.reset(new QRasterBuffer());
```

为什么是在mmap地址靠前一点的地址呢？

我觉得这里就是src addr不满足要求的关键。



# libge2d

先把这个库和kernel的看懂。

这个kernel里是使能的。

```
#ifdef CONFIG_AMLOGIC_ION
	if (!ge2d_ion_client)
		ge2d_ion_client = meson_ion_client_create(-1, "meson-ge2d");
#endif
```

对应这个ioctl的处理GE2D_CONFIG_EX_ION

config_para_s和config_para_ex_s分别处理什么内容？

dma是怎么用的？

dma是通过ioctl申请到的，是ge2d功能的一部分。
往外进行fillrect操作，是调用这个。
ret = ioctl(fd, GE2D_CONFIG_EX_MEM, &ge2d_config_para_ex);
这个在directfb里是找不到的。
那之前fillrect这种操作是怎么做的。
是执行这个。
ioctl(amldrv->ge2d_fd, GE2D_FILLRECTANGLE, &amldev->op_ge2d_info);
这个宏定义在kernel里还有。

GE2D_CONFIG_EX_MEM 和GE2D_FILLRECTANGLE什么关系？
没有明确关系，实现不一样。

GE2D_CONFIG_EX_MEM在ge2d.h里。
GE2D_FILLRECTANGLE在ge2d_cmd.h里。
都混在ioctl里一起处理。
代码有点乱。



驱动没有什么可看的。就是操作寄存器。

```
aml_ge2d_process_ion  这个没有用。
aml_ge2d_process 这个用了。
说明什么？
说明ion的并没有用。

aml_ge2d_t 这个是最全局的结构体。
下面包含了aml_ge2d_info_t
还有一些指针。

aml_ge2d_info_t内容多一些
除了fd。
还有buffer_info_t的src和dst。

buffer_info_t内容
	mem_alloc_type
	memtype
		这2个是什么区别？
		memtype就是canvastype。
		对于fillrect，src的memtype是invalid。dst的可以是alloc或者osd0
		对于blit，src和dst的memtype是alloc。也可以是osd0
		alloc_type默认都是dma的。
		我理解一下，fillrect，就是没有src，直接往屏幕上操作。
		blit，是从屏幕的一个区域拷贝到另外一个区域。
		根据alloc_type不同，会进行不同的内存分配：
		ion_mem_alloc
		dmabuf_alloc
		
	vaddr
		代表了什么？
		是映射的连续物理内存的对应的虚拟地址。
		可以不设置，是用来调试用的。
	shared_fd
		？
		
dmabuf_alloc的逻辑：
使用ioctl来申请ioctl(ge2d_fd, GE2D_REQUEST_BUFF, &buf_cfg);
kernel里这样处理这个ioctl。
ge2d_buffer_alloc(&ge2d_req_buf);
aml_dma_alloc
dma_alloc_from_contiguous
我看之前设备树里有给ion保留一段内存。
但是当前不是ion方式，dma方式的连续内存又是从哪里来的呢？
那应该就是从默认的来的，默认的又有多少呢？够用吗？
static inline struct cma *dev_get_cma_area(struct device *dev)
{
	if (dev && dev->cma_area)
		return dev->cma_area;
	return dma_contiguous_default_area;
}
搜索dma_contiguous_default_area
找到shared-dma-pool
在设备树里有shared-dma-pool的是：
linux,meson-fb 
linux,ion-dev
那起作用的具体又是哪一个呢？
CONFIG_DMA_CMA=y 这个是使能的。

看看kernel的这个文档reserved-memory.txt
需要reserved-memeory子节点有这个属性的，才会被当成默认的dma连续内存来用。
linux,cma-default
当前没有一个节点有这个属性。
但是还有一个默认
dma_contiguous_reserve(arm64_dma_phys_limit);
加打印看看这个是多少。

echo 2 > /sys/class/ge2d/log_level
这样打开ge2d的日志级别。
```

现在运行怎么又不行了。

```
do_fill_rectangle test case:
ge2d config ex dma failed.
```

fb的打印：

```
fb: malloc_osd_memory, cma:ffffff800a910528
```

代码是这样的：

```
#ifdef CONFIG_CMA
	if (fb_rmem.base) {
		base = fb_rmem.base;
		size = fb_rmem.size;
	} else {
		cma = dev_get_cma_area(info->device);
		if (cma) {
			base = cma_get_base(cma);
			size = cma_get_size(cma);
			pr_info("%s, cma:%p\n", __func__, cma);
		}
	}
#else
```

今天运行ge2d_feature_test一定报错了。

```
# ./ge2d_feature_test 
ThreadIdx -- 0, run time -- 0
plane_number=1,format=1
plane_number=1,format=1
plane_number=1,format=6
dma buffer alloc, index=0
dma buffer export, fd=5
do_strechblit test case:
ge2d config ex dma failed. 
ge2d config ex dma failed. 
ge2d config ex dma failed. 
separate_step=0 time=0 ms
ge2d feature_test exit!!!
# 
```

没有什么变化啊。

ge2d config ex dma failed.  这个错误是GE2D_CONFIG_EX_MEM出错了。

看libge2d的readme.txt

有这样的描述：

````
if dma buffer is allocated by ge2d, please add content blow in DTS:

/ {
    /* ...... */
    reserved-memory {
        /* ...... */
            ge2d_cma_reserved:linux,ge2d_cma {
                compatible = "shared-dma-pool";
                reusable;
                status = "okay";
                size = <0x0 0x1800000>;
                alignment = <0x0 0x400000>;
            };
    }
    /* ...... */
    ge2d {
        /* ...... */
        memory-region = <&ge2d_cma_reserved>;
    };
}
````

我加上这个配置看看。

还是不行。

即使我指定使用ion，也还是报dma的错误。

先把kernel里的打印打开。

```
ge2d_process = ge2d_config + ge2d_execute
```

libge2d.so文件。

```
xhl -- before fill rect config 
ge2d_fillrectangle_config_ex,memtype=3,src_format=1200300,s_canvas_w=720,s_canvas_h=720,rotation=0
ge2d_fillrectangle_config_ex,memtype=0,dst_format=1020007,d_canvas_w=736,d_canvas_h=720,rotation=0
ge2d config ex dma failed.
xhl -- after fill rect config,ret:-1 
```

看这些参数值。应该不对吧。

d_canvas_w=736 这个是怎么来的？

是因为要32对齐。

```
static void ge2d_set_canvas(int bpp, int w,int h, int *canvas_w, int *canvas_h)
{
   *canvas_w = (CANVAS_ALIGNED(w * bpp >> 3))/(bpp >> 3);
   *canvas_h = h;
}
```



```
0000@0]d       07400000 - 07500000,     1024 KB, ramoops@0x07400000
[    0.000000@0]d fdt_init_reserved_mem, start:0x0000000005000000, end:0x0000000005400000, len:4 MiB
[    0.000000@0]d       05000000 - 05400000,     4096 KB, linux,secmon
[    0.000000@0]d fdt_init_reserved_mem, start:0x000000003e000000, end:0x0000000040000000, len:32 MiB
[    0.000000@0]d       3e000000 - 40000000,    32768 KB, linux,meson-fb
[    0.000000@0]d       3bc00000 - 3dc00000,    32768 KB, linux,ion-dev
[    0.000000@0]d       3a400000 - 3bc00000,    24576 KB, linux,ge2d_cma
```

pr_debug的内容一致没有打印出来。

我都改成printk的。

也还是没有打印出来。

还是有打印出来的。要dmesg才看得到。

现在的问题是，获取的osd的宽高信息和bpp信息都不对。

```
[   61.290917] osd0 
[   61.292871] xhl -- setup_display_property,841, data32:0x408410
[   61.298928] xhl -- setup_display_property,844, data32:0x408410
[   61.304973] xhl -- setup_display_property,862, w:0, h:0
[   61.310386] 16 bpp
```

osd_get_info

```
void osd_get_info(u32 index, u32 *addr, u32 *width, u32 *height)
{
	*addr = osd_hw.fb_gem[index].addr;
	*width = osd_hw.fb_gem[index].width;
	*height = osd_hw.fb_gem[index].yres;
}
```

这又是为什么？

看看osd_hw.fb_gem哪里被赋值。

osd_setup_hw

fb初始化的时候，是32bpp的。

```
[   11.142137@0]- fb: reserved memory base:0x000000003e000000, size:2000000
[   11.149107@0]- fb: init fbdev bpp is:32
[   11.153319@3]- fb: set osd0 reverse as NONE
[   11.168652@3]- fb: osd probe OK
```

fb和osd是什么关系？

osd就是fb。

axg的只有一个osd。这个结构体是给vpu match的时候用 的。vpu在osdfb之前初始化。

```
static struct osd_device_data_s osd_axg = {
	.cpu_id = __MESON_CPU_MAJOR_ID_AXG,
	.osd_ver = OSD_SIMPLE,
	.afbc_type = NO_AFBC,
	.osd_count = 1,
	.has_deband = 1,
	.has_lut = 1,
	.has_rdma = 0,
	.has_dolby_vision = 0,
	 /* use iomap its self, no rdma, no canvas, no freescale */
	.osd_fifo_len = 64, /* fifo len 64*8 = 512 */
	.vpp_fifo_len = 0x400,
	.dummy_data = 0x00808000,
	.has_viu2 = 0,
};
```

osd这里width和xres是什么关系？

我用fb_basic_info获取到的信息里，width也是0 。

现在再执行ge2d_feature_test，dmesg又变了。

```
[ 1374.951638] osd0 
[ 1374.953507] xhl -- setup_display_property,841, data32:0x408504
[ 1374.959566] xhl -- setup_display_property,844, data32:0x408504
[ 1374.965604] xhl -- setup_display_property,862, w:2880, h:720
[ 1374.971456] 32 bpp
[ 1374.973676] ge2d: dst-->type: osd0, format: 0x1100300 !!
[ 1374.979219] ge2d error: dst: osd0, out of range
```

width又变成了2880了。

fbset默认读取到的配置信息是这样：

```
# fbset

mode "720x720"
    geometry 720 720 720 1440 32
    timings 0 [ 1475.020164@1]- fb: osd_release now.index=0,open_count=1
0 0 0 0 0 0
    rgba 8/16,8/8,8/0,8/24
endmode
```

fbset的代码在这里

https://github.com/Distrotech/fbset/blob/master/fbset.c

还是读取的fb var信息。

从这里看，宽高信息是对的。

至少没有2880 。

2880从哪里来的？

osd_setup_hw

被2处调用：

osddev_setup

osd_init_hw

```
osd_set_par //这个分支应该没有调用吧。
	osddev_setup
```

```
static struct fb_ops osd_ops = {
	.owner          = THIS_MODULE,
	.fb_check_var   = osd_check_var,
	.fb_set_par     = osd_set_par,//这里
```

看osd_init_hw

```
err_num = request_irq(int_viu_vsync, &vsync_isr,
					IRQF_SHARED, "osd-vsync", osd_setup_hw);
```

request_irq的最后一个参数，可以给函数？而且vsync_isr也没有使用这个参数啊。



```
# fbset
[   78.885594@1]- fb: malloc_osd_memory, cma:ffffff800a910528
[   78.885649@1]- fb: malloc_osd_memory, 1208, base:0x000000003e000000, size:33554432
[   78.893055@1]- fb: malloc_osd_memory, 1240, fb_index=0,fb_rmem_size=25165824
[   78.901219@1]- fb: malloc_osd_memory, cma mem
[   78.904313@1]- fb: Frame buffer memory assigned at[   78.908871@1]- fb:  0, phy: 0x000000003e300000, vir:0xffffffc03e000000, size=24576K
[   78.908871@1]- 
[   78.918180@1]- fb: logo_index=0,fb_index=0
[   78.922235@1]- fb: ---------------clear fb0 memory ffffffc03e000000
[   78.945907@1]- fb: osd[0] canvas.idx =0x40
[   78.945933@1]- fb: osd[0] canvas.addr=0x3e300000
[   78.948942@1]- fb: osd[0] canvas.width=2880
[   78.953110@1]- fb: osd[0] canvas.height=1440
[   78.957329@1]- fb: osd[0] frame.width=720
[   78.961277@1]- fb: osd[0] frame.height=720
[   78.965354@1]- fb: osd[0] out_addr_id =0x0

mode "720x720"
    geometry 720 720[   78.972718@0]- fb: osd_release now.index=0,open_count=1
 720 1440 32
    timings 0 0 0 0 0 0 0
    rgba 8/16,8/8,8/0,8/24
endmode
```

canvas.width=2880 这个为什么是这么多呢？

刚上电后，第一次执行ge2d_feature_test，打印的w和h都是0

然后执行一次fbset查看信息，然后再执行ge2d_feature_test就看到w是2880，h是1440了。

malloc_osd_memory是在osd_open的时候执行。

那变化就是一次osd_open导致的。

是的。

执行ge2d的测试，不会进行fb的打开操作？

那是怎么显示到lcd的呢？

ge2d要正常运行，是不是需要有一个gui程序在后台一直运行？

不是。

还是看canvas的width为什么变成了2880 。

```
osd_log_info("osd[%d] canvas.width=%d\n",
			index, osd_hw.fb_gem[index].width);
```

那可能是dts里要改一下？

mem_alloc 这个设备树属性是做什么的？当前默认是1 。如果是0，表示用mmap。

```
prop = of_get_property(pdev->dev.of_node, "mem_alloc", NULL);
	if (prop)
		b_alloc_mem = of_read_ulong(prop, 1);
```

我把dts的宽高值都改成720的。

再试一下，看看osd_open的时候，现在值是多少。

```
[   27.425253@1]- fb: osd[0] canvas.idx =0x40
[   27.425283@1]- fb: osd[0] canvas.addr=0x3e300000
[   27.428314@1]- fb: osd[0] canvas.width=2880
[   27.432463@1]- fb: osd[0] canvas.height=720
[   27.436596@1]- fb: osd[0] frame.width=720
[   27.440559@1]- fb: osd[0] frame.height=720
[   27.444616@1]- fb: osd[0] out_addr_id =0x0
```

现在canvas height变成720了。

但是canvas width还是2880 。

那就要看2880怎么计算得到的。

```
u32 w = (color->bpp * xres_virtual + 7) >> 3;
```

这个为什么要这样算？

这样算了之后，的确就w等于2880 了。

这个计算倒是没有问题。

找到问题了，是我在ge2d_feature_test里，dst format忘了改了。

默认是YV12的，所以导致720被对齐到736（32对齐）

改成ARGB8888就好了。

现在可以确认ge2d正常。

现在看directfb的fillrect。

对比一下打印。

ge2d_feature_test有一行这样的打印：

```
ge2d_canv_config:index=0,addr=3e300000,stride=2880
```

而df_dok的，是这样：

```
ge2d_canv_config:index=0,addr=0,stride=0
```

那这个应该是不合理的。

这个是怎么配置下来的？

在./media/common/ge2d/ge2d_hw.c

```
void ge2d_canv_config(u32 index, u32 addr, u32 stride)
{
	ge2d_log_dbg("ge2d_canv_config:index=%d,addr=%x,stride=%d\n",
		index, addr, stride);
	if (index <= 2) {
		ge2d_reg_write(GE2D_DST1_BADDR_CTRL + index * 2,
			((addr + 7) >> 3));
		ge2d_reg_write(GE2D_DST1_STRIDE_CTRL + index * 2,
			((stride + 7) >> 3));
	}
}
```



```
fillrect的调用流程
先GE2D_CONFIG_EX_MEM 
再GE2D_FILLRECTANGLE
到了驱动的ge2d_ioctl里。
是增加一个cmd任务到workqueue。
ge2d_wq_add_work
ge2d_monitor_thread 这个内核线程
处理ge2d_process_work_queue
然后是ge2d_set_src1_data
然后 ge2d_canv_config
那么问题就在于 cfg->dst_phyaddr 
directfb这个地址一直是0 。
```



分析ge2d_feature_test fill-rect的过程

```
ioctl :0x470b  获取能力，在aml_ge2d_init函数里调用。
ioctl :0x42184707 这个是GE2D_CONFIG_EX_MEM，配置内存信息。
ioctl :0x46fd 是GE2D_FILLRECTANGLE
add new work @@ge2d_wq_add_work:614 添加任务到wq里。
secure mode:0 不是secure模式。
ge2d_canv_config:index=0,addr=3e300000,stride=2880
	这个是最关键的。
	
```

dfb_dok的过程

```
ioctl :0x46fd 一上来就是fill-rect。没有配置内存信息的过程。
ioctl :0x4700 这个是GE2D_BLEND 为什么会有blend？
```



```
typedef enum {
	GE2D_DRAW_TYPE_NONE,
	GE2D_DRAW_TYPE_BLEND,//fill-rect，可能是这种情况。
	GE2D_DRAW_NOT_SUPPORT
} AMLDrawSubFunction;
```

这个draw type的none和blend有什么区别？

取决于amlSetState设置的值。

还是要加打印，把dfb_dok的过程再明确一下。



```
--fill-rect对应函数fill_rect
--fill-rect-blend对应函数fill_rect_blend
```



GetAccelerationMask的流程

```
最上层的调用是，是从surface指针来调用。
是dest这个surface。
DFBRectangle rect = { 0, 0, SW, SH };
primary->GetSubSurface (primary, &rect, &dest);
```



```
当前内核里：
#define GE2D_CONFIG_EX_MEM	 \
	_IOW(GE2D_IOC_MAGIC, 0x07,  struct config_ge2d_para_ex_s)
之前的directfb里：
#define GE2D_CONFIG_EX	     _IOW(GE2D_IOC_MAGIC, 0x01,  config_para_ex_t)
ioctl(amldrv->ge2d_fd, GE2D_CONFIG_EX, &amldev->ge2d_config_ex);
```

config_ge2d_para_ex_s结构体内容：

```
struct config_ge2d_para_ex_s {
	union {
		struct config_para_ex_ion_s para_config_ion;
		struct config_para_ex_memtype_s para_config_memtype;
	};
};

```

config_para_ex_t结构体：

```
typedef    struct {
	src_dst_para_ex_t src_para;
	src_dst_para_ex_t src2_para;
	src_dst_para_ex_t dst_para;

	//key mask
	src_key_ctrl_t  src_key;
	src_key_ctrl_t  src2_key;

	int alu_const_color;
	unsigned src1_gb_alpha;
#ifdef CONFIG_GE2D_SRC2
	unsigned int src2_gb_alpha;
#endif
	unsigned op_mode;
	unsigned char bitmask_en;
	unsigned char bytemask_only;
	unsigned int  bitmask;
	unsigned char dst_xy_swap;

	// scaler and phase releated
	unsigned hf_init_phase;
	int hf_rpt_num;
	unsigned hsc_start_phase_step;
	int hsc_phase_slope;
	unsigned vf_init_phase;
	int vf_rpt_num;
	unsigned vsc_start_phase_step;
	int vsc_phase_slope;
	unsigned char src1_vsc_phase0_always_en;
	unsigned char src1_hsc_phase0_always_en;
	unsigned char src1_hsc_rpt_ctrl;  //1bit, 0: using minus, 1: using repeat data
	unsigned char src1_vsc_rpt_ctrl;  //1bit, 0: using minus  1: using repeat data

	//unsigned char    src1_cmult_asel;
	//unsigned char    src2_cmult_asel;
	//canvas info
	config_planes_t src_planes[4];
	config_planes_t src2_planes[4];
	config_planes_t dst_planes[4];
}config_para_ex_t;
```

内核里还是有config_para_ex_s 这个结构体，GE2D_CONFIG_EX也还有。

就是结构体成员在最后多了一个int mem_sec;



GE2D_CONFIG_EX_MEM 对应config_ge2d_para_ex_s，作用是：

GE2D_CONFIG_EX对应config_para_ex_s ，作用是：

GE2D_CONFIG_EX_MEM 是新版本的GE2D_CONFIG_EX。为了兼容保留了GE2D_CONFIG_EX。



当前ion和dma方式，是以一个union的形式存在，kernel导致用一个呢？哪里进行了设置呢？

代码真的有点乱。

```
struct config_para_ex_memtype_s {
	int ge2d_magic;
	struct config_para_ex_ion_s _ge2d_config_ex;
```

config_para_ex_memtype_s里完整包含了config_para_ex_ion_s

库接口使用方法可以参考vendor/amlogic/ipc/ipc_plugins/common/imgproc.c里的imgproc_transform()

最关键的还是那个dma fd。

DFBSurfaceDrawingFlags

```
DFBSurfaceDrawingFlags
这样用：
primary->SetDrawingFlags( primary, DSDRAW_BLEND );   
blend这表示：使用颜色里的alpha值。
/* uses alpha from color */
```

只处理着两种情况：

```
switch(flags){
		case DSDRAW_NOFX:
		amldev->function_type = GE2D_DRAW_TYPE_NONE;
		break;
		case DSDRAW_BLEND:
		amldev->function_type = GE2D_DRAW_TYPE_BLEND;
		break;			
		default:
		amldev->function_type = GE2D_DRAW_NOT_SUPPORT;
		break;
	}
```



看看gst_dmabuf_memory_get_fd怎么实现的。

imgproc_transform里就是填充aml_ge2d_info_t结构体，然后调用aml_ge2d_process

我当前要简单处理，不能做这么大的改动。

要拿到dma fd。还是自己用ioctl的方式来做。

在哪里获取dma fd？

是否全局性地获取一次就够了？是的，所以在初始化的时候，做一次就好了。

怎么释放dma fd？

不用释放。不用管就行了。

这个dma数据的同步，在什么时候需要做？

```
if (pge2dinfo->src_info[0].mem_alloc_type == AML_GE2D_MEM_DMABUF)
        aml_ge2d_sync_for_device(pge2dinfo, 0);
if (pge2dinfo->dst_info.mem_alloc_type == AML_GE2D_MEM_DMABUF)
        aml_ge2d_sync_for_cpu(pge2dinfo);
```

本质上也是一个ge2d的ioctl ：GE2D_SYNC_DEVICE



blend是指对多个src的数据进行融合。不过我们一般只有一个src。

```
case AML_GE2D_FILLRECTANGLE:
            attach_flag = ATTACH_DST;
            break;
        case AML_GE2D_BLEND:
            attach_flag = ATTACH_SRC | ATTACH_SRC2 | ATTACH_DST;
```



应用是32位的，kernel是64位的。

ioctl的的时候，是使用compat的接口？



fillrect的时候，从libge2d的例子看，src mem的type是invalid。为什么是invalid？而不是malloc？

应该是因为fillrect，只需要指定范围和颜色，由ge2d来完成填写。

而不是先赋值一块内存，然后拷贝内存内容。



现在有个问题。

```
./ge2d_feature_test --fillrect ff000000_0_0_720_720 我所有格式都是设置ARGB的，但是实际效果为什么是RGBA？前面这个名字，预期应该是全黑的，但是实际上是红色的。
```

看到代码里有这样的：

```
case PIXEL_FORMAT_ARGB_8888:
        *pge2d_format = GE2D_FORMAT_S32_BGRA;
        *p_bpp = GE2D_BPP_32;
        is_one_plane = 1;
        break;
```

顺序完全是反的？

但是反的也不符合实际效果。

如果颜色写成ff 00 00 00 ，显示是红色，如果是上面代码写的，那么应该显示蓝色。

这颜色为什么搞得这么纠结呢？直观一点不好吗？



amlFillRectangle_ConfigEx和amlFillRectangle_blend_ConfigEx区别是什么？

blend还是多屏融合，src2也是有效的。



```
我还是自己写一个简单的测试例子。
来绘制长方形。就嵌套3个，
红：720x720
绿：480x480
蓝：320x320
就在primary这个surface上做。
先用fb来做。保证用例可以正常运行。
为了避免颜色重叠，还是红绿蓝依次对角线排列。
每个大小都用100x100的。

在我自己的demo里加directfb的，编译头文件问题还得解决。
直接在dfb_dok目录下找到程序来改吧。

自己写的例子跑起来了，使用fb可以正常显示。
xhl -- get pixel format:4295684
xhl -- get size, w:139728,h:139724
为什么宽高值是这么大的？
这个是primary的大小。
注释里这么写的。那就不管。
struct {
         /* 'wanted' is passed to GetSubSurface(), it doesn't matter if it's
            too large or has negative starting coordinates as long as it
            intersects with the 'granted' rectangle of the parent.
            'wanted' should be seen as the origin for operations on that
            surface. Non sub surfaces have a 'wanted' rectangle
            of '{ 0, 0, width, height }'. 'wanted' is calculated just once
            during surface creation. */
         DFBRectangle       wanted;
```



先把编译的so放到板端运行一下。

```
(!) Direct/Modules: Unable to dlopen `/usr/lib/directfb-1.7-7/gfxdrivers/libdirectfb_amlgfx.so'!
    --> /usr/lib/directfb-1.7-7/gfxdrivers/libdirectfb_amlgfx.so: undefined symbol: aml_ge2d_mem_free
```

这就涉及到automake工具添加动态库链接的问题了。

当前可执行程序ldd查看，是链接了这些东西。

```
libstdc++.so.6 => /lib/libstdc++.so.6 (0xf744e000)
        libz.so.1 => /usr/lib/libz.so.1 (0xf742b000)
        libdirectfb-1.7.so.7 => /usr/lib/libdirectfb-1.7.so.7 (0xf71ea000)
        libfusion-1.7.so.7 => /usr/lib/libfusion-1.7.so.7 (0xf71bf000)
        libdirect-1.7.so.7 => /usr/lib/libdirect-1.7.so.7 (0xf7173000)
        libpthread.so.0 => /lib/libpthread.so.0 (0xf714d000)
        libc.so.6 => /lib/libc.so.6 (0xf7061000)
        libm.so.6 => /lib/libm.so.6 (0xf6fe7000)
        /lib/ld-linux-armhf.so.3 (0xf7558000)
        libgcc_s.so.1 => /lib/libgcc_s.so.1 (0xf6fbd000)
        libdl.so.2 => /lib/libdl.so.2 (0xf6fa8000)
        librt.so.1 => /lib/librt.so.1 (0xf6f90000)
```

看看directfb-examples的配置。

有一条这样的：

```
LIBADDS = \
	@DIRECTFB_LIBS@
```

这个从哪里来呢？

在directfb的编译目录下搜索，找到这个：

```
./ChangeLog:20644:    spooky: Add $(DIRECTFB_LIBS) to linker command line.
```

怎么加的？

应该是从directfb-1.7.7/directfb.pc里输出的。

directfb-1.7.7/directfb.pc也不是手写的，而是通过in文件生成的。

那in文件里又是怎么写的？

我在directfb.pc.in文件里加上-lge2d。

make directfb-reconfigure，执行后，directfb.pc里有了-lge2d。

但是编译打印里还是没有：

```
  LIBS                      -ldl -lrt -lpthread 
  DYNLIB                    -ldl
  RTLIB                     -lrt
  THREADFLAGS               -D_REENTRANT
  THREADLIB                 -lpthread
```

简单起见，我先把libge2d的c文件直接放进来编译吧。

好像这里可以加动态库

```
libdirectfb_amlgfx_la_LDFLAGS = \
	-module			\
	-avoid-version		\
	$(DFB_LDFLAGS)
```

加上试一下。可以。

```
ldd ./libdirectfb_amlgfx.so
ldd: $warning: you do not have execution permission for `./libdirectfb_amlgfx.so'
        libge2d.so => /usr/lib/libge2d.so (0xf7439000)
        libdirect-1.7.so.7 => /usr/lib/libdirect-1.7.so.7 (0xf73ed000)
```

运行也可以正常调用到ge2d的函数。

但是运行宽高怎么不对？所以没有效果。

```
[ge2d_process 3007] xhl -- before fill rect config 
[ge2d_fillrectangle_config_ex 1351] ge2d_fillrectangle_config_ex,memtype=3,src_format=1300300,s_canvas_w=720,s_canvas_h=720,rotation=0
[ge2d_fillrectangle_config_ex 1354] ge2d_fillrectangle_config_ex,memtype=0,dst_format=1300300,d_canvas_w=720,d_canvas_h=720,rotation=0
[ge2d_process 3009] xhl -- after fill rect config,ret:0 
[ge2d_fillrectangle 2422] ge2d_fillrectangle:rect x is 0, y is 0, w is 0, h is 0
```

当前是从（100,100）画一个w和h都是100的矩形。

在上层是对的：

```
-> [ 0]  100, 100- 100x 100
```

传递到下面不对，应该是数据填充不对。

```
[13148.975216@0]- xhl -- setup_display_property,862, w:2880, h:720
[13148.981078@0]- 32 bpp
[13148.983292@0]- xhl -- setup_display_property,871, bpp:32, xres:720 
[13148.989520@0]- ge2d: dst-->type: osd0, format: 0x1100300 !!
[13148.995068@0]- xhl -- ge2d_context_config_ex_mem,2252, top:0, left:0, width:104, height:100, res:720, yres:720
[13149.004962@0]- ge2d osd phy_addr:0x3e300000,stride=0xb40,format:0x1100300
x[13149.011796@0]- xhl -- ioctl :0x46fd 
[13149.015285@0]- fill rect...,x=0,y=0,w=0,h=0,color=0x0
[13149.020331@0]- add new work @@ge2d_wq_add_work:614
[13149.025054@0]- add new work ok
```

的确填充不对。

imgproc里是这样。

```
pge2dinfo->src_info[0].canvas_w = in_pos.canvas_w;
  pge2dinfo->src_info[0].canvas_h = in_pos.canvas_h;
  pge2dinfo->src_info[0].rect.x = in_pos.x;
  pge2dinfo->src_info[0].rect.y = in_pos.y;
  pge2dinfo->src_info[0].rect.w = in_pos.w;
  pge2dinfo->src_info[0].rect.h = in_pos.h;
```

安装这个改一下。

现在尺寸对了。但是颜色还是不对。

```
[ge2d_fillrectangle 2423] color is 0
```

在这里手动写上颜色：

```
	pge2dinfo->color = 0x00ff00;
	pge2dinfo->gl_alpha = 0;
	pge2dinfo->const_color = 0;
```

运行，现在至少可以看到运行效果了。

当前色块尺寸不对。

占满了屏幕，而不是100x100.

不是尺寸不对，是因为我当前把颜色写死的，导致clear也是全部是颜色。

而且跟后面画框是一个颜色。

我这样处理一下，就可以看到正常画框了。

```
static int first = 1;
	if(first) {
		pge2dinfo->color = 0xff000000;
		first = 0;
	} else {
		pge2dinfo->color = 0x0000ff00;
	}
```

像素格式是RGBA的。

像素格式先不管。最后看实际效果再统一考虑。

当前我全部都写ARGB。

先看颜色值的传递。

应用层是通过surface的SetColor来设置颜色。

这个值放到哪里去了？怎么传递给ge2d？

给了IDirectFBSurface_data里。

后面又怎么取用呢？

看之前的ge2d写法，虽然没有效果的，但是应该也是有一定道理的。

之前是这样：

```
amldev->op_ge2d_info.color = amldev->color;

	int ret = ioctl(amldrv->ge2d_fd, GE2D_FILLRECTANGLE, &amldev->op_ge2d_info);
```

颜色值的传递，这个问题必须解决，不然没法做。

之前的颜色是放在amldev->color;里。
aml_set_color 这个函数进行的设置。
被amlSetState函数调用。这个是SetState指针调用。
可以正常进行显示。
而且颜色的对的。

跑df_dok --fill-rect可以正常了。

现在需要分析一下当前的代码，有些点要搞清楚再继续。

amldev->function_type的赋值，两种可能，一个是none，一个是blend。

当前fill-rect是none的情况。

什么情况下会使用blend？

是靠CardState的drawingflags来控制的。

```
DFBSurfaceDrawingFlags flags = state->drawingflags;
```

CardState的值又是怎么确定的呢？

amlSetState被框架调用。

dfb_gfxcard_state_check_acquire和dfb_gfxcard_state_acquire区别是什么？

```
还有一个dfb_gfxcard_state_check函数
我估计dfb_gfxcard_state_check_acquire是这2个函数合体的效果。
```

df_dok有一个fill_rect_blend的测试。

我跑一下看看。

代码逻辑：

```
SET_DRAWING_FLAGS( DSDRAW_BLEND );
先给dest这个surface设置drawing flag为blend。
if (!showAccelerated( DFXL_FILLRECTANGLE, NULL ))
          return 0;
然后查询是否支持fill rect的加速。
然后就是SetColor和FillRectangle函数调用。
```

写到这里，我发现我前面自己写的简单例子。

没有进行drawing flag的设置和加速能力的检查。

没有设置drawing flag，所以默认就是非blend的情况。

gfx的加速能力在哪里设置的？按道理应该是在gfx代码里。

就是这个：

```
funcs->CheckState    = amlCheckState;
```

当前ge2d支持的加速操作有：

```
1、只支持ARGB这一种格式。
2、只支持fill-rect、blit、stretch-blit这三种操作。
```

把我写的简单测试代码完善一下。

fill-rect-blend跟fill-rect有什么不一样？

对比一下之前的代码的这2个函数。

也就是src2的不是invalid，而是有效值。

其他的没有什么特别的。

我实现一下，测试看看是否正常。

但是现在的实现，本来src1就都是mem_type是invalid的。

这个先留空吧。

看看qt实际例子，会不会调用到这个函数。

就用只全屏显示一个按钮的例子。

blend是没有调用。但是有很多blit调用。

stretch blit没有看到调用。估计这个是给手动缩放这种场景用的。

先把blit实现。

directfb里有QDirectFbBlitter类。

代码这样调用：

```
result = m_surface->FillRectangle(m_surface.data(), x, y, w, h);
```

可以靠这个环境变量来打开调试打印

QT_DIRECTFB_BLITTER_DEBUGPAINT

还是有很多的amlFillRectangle_blend_ConfigEx调用。

那么blend应该怎么写呢？

可以先看一下libge2d的代码。

还是要先把blend的例子跑一下，仔细分析。

先把directfb的看懂。代码不多，就看qdirectfbblitter.cpp就好了。

m_premult 这个表示预乘。

在构造函数里，这样来决定它的值。

```
DFBSurfaceCapabilities surfaceCaps;
    m_surface->GetCapabilities(m_surface.data(), &surfaceCaps);
    m_premult = (surfaceCaps & DSCAPS_PREMULTIPLIED);
```

取决于surface的cap属性。而cap属性是人为设置的。

例如在df_dok里，有这样的：

```
     dsc.flags |= DSDESC_CAPS;
     dsc.caps   = DSCAPS_PREMULTIPLIED;

     DFBCHECK(dfb->CreateSurface( dfb, &dsc, &rose_pre ));
```

首先会调用QDirectFbWindow::createDirectFBWindow

```
window()->type() == Qt::Desktop
这个条件不满足。
```

```
description.options = DFBWindowOptions(DWOP_ALPHACHANNEL);
        description.caps = DFBWindowCapabilities(DWCAPS_DOUBLEBUFFER|DWCAPS_ALPHACHANNEL);
 默认是双buffer的。
```



从打印看，blitfunction_type这个是一个较大的知识点。

当前是在amldev里的属性。看看之前是怎么把这个属性传递给驱动的。

这个就导致了amlBlit函数有很多的分支。

```
switch (amldev->blitfunction_type){
			case GE2D_BLEND_PRE_ALPHACHANNEL:
			amlBlend_Config_Ex(drv, dev, rect, rect, &amldev->src_info, &amldev->dst_info, &amldev->dst_info, PREMULT_NONE);
			amlBlend_Start(drv, dev, rect, rect, dx, dy);
			break;
			case GE2D_BLEND_ALPHACHANNEL:
```

各个分支的区别是什么？

有这些分支：

```
typedef enum {
	GE2D_BLEND_NOFX,
	GE2D_BLEND_PRE_ALPHACHANNEL,
	GE2D_BLEND_ALPHACHANNEL,
	GE2D_BLEND_SRC_COLORKEY,
	GE2D_BLEND_COLORIZE,
	GE2D_BLEND_COLORIZE_ALPHA,
	GE2D_BLEND_SRC_COLORKEY_COLORIZE,
	GE2D_ROTATION,
	GE2D_BLEND_COLORALPHA,
	GE2D_NOT_SUPPORT
} AMLBlendSubFunction;
```



```
GE2D_BLEND_PRE_ALPHACHANNEL
GE2D_BLEND_ALPHACHANNEL
GE2D_BLEND_COLORIZE_ALPHA
这个3个带alpha的，处理都是一样的。
都是：
amlBlend_Config_Ex
amlBlend_Start
函数参数的src_rect和dst_rect是一个。
应该是对自己进行处理。
```

没有单独的blend调用，只有blit调用blend的情况。

也不是，fill-rect-blend有调用。

而且调用次数还不少。

dst_info phys这个的值是怎么确定的？从哪里来？

```
amlgfx amlBlit_ConfigEx 393> src_info phys is 0x3e300000
amlgfx amlBlit_ConfigEx 394> dst_info phys is 0x3e4fa400
```

靠应用层的SetState传递下来。

```
static inline void 
aml_set_dst( AMLGFX_DriverData *amldrv,
		AMLGFX_DeviceData *amldev,
		CardState *state )
{
	if (amldev->aml_smf.smf_destination){
		return;
	}

	amldev->dst_info.addr = (unsigned long)state->dst.addr;
	amldev->dst_info.phys = state->dst.phys;
	amldev->dst_info.pitch = state->dst.pitch;
```

所以SetState函数需要再仔细看一遍。

之所以颜色对得上，是因为这里又转了一次。

```
case DSPF_ARGB:
			amldev->color = PIXEL_ARGB( state->color.r,
					state->color.g,
					state->color.b,
					state->color.a );
```

物理地址怎么获取到的？

我估计是这里。

```
lock->phys = dfb_fbdev->shared->fix.smem_start + lock->offset;
```

SurfacePoolFuncs的Lock是做什么的？感觉不像是加锁。

CardState的不少属性，都是通过amldev的属性来在各个函数之间传递。

例如这些：

````
config_info src_info;
	config_info dst_info;

	DFBDimension src_size;
	DFBDimension dst_size;
````

aml_state.c里的函数，就是用来把CardState的属性传递给amldev的。

fillrect和blit的区别就在于：fillrect没有进行set-src的操作。

set-dst是所有情况都要做的。

set-src和set-dst就是给这几个属性赋值：

```
typedef struct {
	unsigned long addr;
	unsigned long phys;
	unsigned long pitch;
	unsigned long format;
	int mem_type;
	int rotation;
}config_info;
```

DSBLIT_SRC_COLORKEY 这个color key属性是什么含义？

用来叠层显示过滤生成的指定颜色的。

当前应该都没有用上。

也是通过amldev的属性进行传递。

```
amldev->dst_colorkey = ColorKey;
```

aml_state.c里都设置好了amldev的参数。

然后最后执行操作，还修改了哪些内容？

看aml_accel.c

以amlFillRectangle为例。

传递过来的参数，就是除了amldev和amldrv，就是一个rect。

aml_updatePalette 这个什么时候调用？作用是什么？

在amldev里有这2个属性：

```
	CorePalette   *palette;
	bool           	bNeedCLUTReload;
```

bNeedCLUTReload只有在DSPF_LUT8的时候才满足。

所以这个函数条件满足不了。忽略就行。

amlgfx的代码看了个大概。

现在看libge2d的代码。

aml_ge2d_info 跟directfb里的amldev的作用类似。

也有color和gl_alpha的属性。

buffer_info_t 这个类型：

```

```



blend，应该是对osd上的两个内容进行操作。

所以src、src2、dst都应该是GE2D_CANVAS_OSD0类型。



我写directfb的例子，应该怎么写呢？

先看df_dok的例子怎么调用到下面的。



我看一下gfxdrivers/gp2d这个的实现。



我想到一个调试方法，就是分步来调。

通过修改CheckState，每次只使能一种能力。

例如，现在我的fill-rect是好的，那么就把其他的都设置为不支持。

看看这样能不能把界面显示出来。

我的最简单的qt例子是可以显示出来的。但是按钮的文字颜色是绿色。

正常应该是黑色的。

而且跑qt官方例子，直接卡住了。界面没有显示出来。

卡住是卡在vt了。directfbrc里加上no-vt就不会卡住了。

然后有的问题是：图片素材显示不出来。文字也没有显示出来。文字颜色不对。

我把fill-rect的能力也关闭。使用directfb看看跟直接使用fb有没有区别。

按道理应该没有区别了。

还是不支持。

我改成no-hardware的配置，还是不正常。

板端重启就正常了。

blend的暂时搞不清楚，就先不管吧。

先做blit的。

GE2D_SRCCOLORKEY

这个在libge2d里没有用。

我先忽略这个吧。

运行demo_qt，blit只有这3种情况。

```
DSBLIT_NOFX                   = 0x00000000,
DSBLIT_BLEND_ALPHACHANNEL     = 0x00000001,
                                           
DSBLIT_BLEND_COLORALPHA       = 0x00000002,
```

AML_SUPPORTED_BLITTINGFLAGS 这个里面支持的是上面的1和2 ，0没有写。

配置card的能力，是在driver_init的时候，给这个结构体赋值。

```
typedef struct {
     CardCapabilitiesFlags   flags;

     DFBAccelerationMask     accel;
     DFBSurfaceBlittingFlags blitting;
     DFBSurfaceDrawingFlags  drawing;
     DFBAccelerationMask     clip;
} CardCapabilities;
```



传递给canvas的是amldev->src_size，这是从state传递过来的。

canvas是固定的吗？不是的，这个应该就是绘制的元素的尺寸。

aml为什么要对canvas的width进行8对齐？

不对齐会怎么样？

先保证对齐。

之前我没有留意amldev->dst_size.w 这个应该怎么用呢？



需要搞清楚，ge2d，从应用层往下传递的尺寸和颜色信息，有哪几个。

怎么传递。

```
qt这一层
	完全不用关注，qt自己处理了。
	绘制控件，
```



还是看一下自己写的directfb的fill-rect的例子。

这里有个疑问，ge2d_context_config_ex_mem配置的是720，后面fill rect的为什么是100的？

```
[ 9680.284640@1]- xhl -- ge2d_context_config_ex_mem,2252, top:0, left:0, width:720, height:720, res:720, yres:720
[ 9680.294548@1]- ge2d osd phy_addr:0x3e300000,stride=0xb40,format:0x1100300
-[ 9680.301359@1]- xhl -- ioctl :0x46fd 
[ 9680.304901@1]- fill rect...,x=0,y=0,w=100,h=100,color=0xff0000ff
```

看kernel的ge2d_context_config_ex_mem函数打印这个几个参数怎么打印的。

是这4个值。

config_para_ex_ion_s这个结构体里的。

```
top = ge2d_config->dst_para.top;
left = ge2d_config->dst_para.left;
width = ge2d_config->dst_para.width;
height = ge2d_config->dst_para.height;
```

上层是怎么把这4个值传递下来的？

没有找到哪里传递了这4个值。

有的，就是在ge2d_process里设置的。

在ge2d_process里，有进行一次对齐。对齐数据的来源是output_buffer_info

```
ge2d_set_canvas(bpp,output_buffer_info->canvas_w,output_buffer_info->canvas_h,&d_canvas_w,&d_canvas_h);
```

```
buffer_info_t* output_buffer_info = &(pge2dinfo->dst_info);
```

所以要看上层对dst_info的填充。

dst_info是一个buffer_info。主要包含的内容有：

```
mem_alloc_type 
mem_type
canvas_w
canvas_h
rect ： rect的宽高和canvas的宽高是什么关系？
format
rotation
shared_fd 这个是dma的fd
plane_alpha：这个是平面的透明度？有用上没？也只是src_info用到了。
layer_mode：这个只看到src_info用到了。取值是枚举，invalid、non、premulti、coverage
fill_color_en：bool。只有src_info用到了。
def_color：也只有src_info用到。
```

还是需要把ge2d_feature_test的所有情况都测试一遍。理解了每个变量的含义，才方便做。

aml_ge2d_info结构体包含的内容：

```
ge2d_fd
ion_fd 这2个没什么可说的。就是fd。
offset：不知道干啥的。
blend_mode：跟buffer_info里的layer_mode取值一样，也是invalid、non、premulti、coverage。
	默认被赋值为premulti的。
ge2d_op：枚举，就是fill-rect、blit这几种。
src_info[2]
dst_info 
	就是buffer_info。
color：这个颜色值怎么用？
gl_alpha：gl表示什么？在libge2d里完全没有用上。
const_color：也没有被明确赋值。
dst_op_cnt：基本都是1，只有PIXEL_FORMAT_YV12格式是3 。
cap_attr：通过GE2D_GET_CAP这个ioctl来读取。
	能力包括9个bit。我看没有值得注意的。
b_src_swap：后面看代码，发现是src和src2的能力不同，有些情况src2能力不足，需要交换src和src2来处理。

```

ge2d_feature_test的separate_step 分步操作有什么不同的？

```
aml_ge2d_attach_dma_fd
	不分步的，好像没有看到这个操作。
	是一个ioctl操作。
aml_ge2d_config
aml_ge2d_execute
```

经过阅读libge2d的代码，我有点觉得不需要用libge2d。而只是ioctl可能就够了。

这样改动也会更小。

还是需要再进一步理解透彻。

amlFillRectangle_Start 这个函数的可以不动。是一样的。

只需要填充x、y、w、h、color这5个值。

就是需要合理填充GE2D_CONFIG_EX_MEM对应的结构体。

可能需要在当前的结构体的基础上增加一些东西就可以。

我不太理解这个，为什么left和top一直是写死的0？

```
ge2d_config_ex->src_para.left = 0;
    ge2d_config_ex->src_para.top = 0;
    ge2d_config_ex->src_para.width = s_canvas_w;
    ge2d_config_ex->src_para.height = s_canvas_h;
```

继续看，觉得用libge2d也可以。

看看之前blend是怎么实现的。

之前是src和src2的mem_type都是alloc的，这样就是blend。

src2是invalid，这样是fill-rect。

而dst一直是alloc。

现在逻辑不是这样。

先看directfb在blend的时候，传递下来的参数是什么。

跟fill-rect还是一样的参数。

我就是很不明白，为什么blend跟fill-rect混为一谈了？



blend包括两个部分，color和alpha。



现在要看qt运行时，为什么有那么多blend操作传递下来？

DSDRAW_BLEND

```
QDirectFbBlitter::fillRect(const QRectF &rect, const QColor &color)
直接调用
alphaFillRect(rect, color, QPainter::CompositionMode_Source);
```

QDirectFbBlitter构造函数有2个，2个都有被调用。

第二个参数为surface的，premult是0，第二个参数是bool的，是表示是alpha的意思，在函数里直接被写成了true了。

```
QDirectFbBlitter::QDirectFbBlitter(const QSize&, IDirectFBSurface*) 74, premult:0
QDirectFbBlitter::QDirectFbBlitter(const QSize&, bool) 88, 
QDirectFbBlitter::QDirectFbBlitter(const QSize&, bool) 88, 
QDirectFbBlitter::QDirectFbBlitter(const QSize&, bool) 88, 
```

注释写的：

```
// force alpha format to get AlphaFillRectCapability and ExtendedPixmapCapability support
    alpha = true;
```

第二个参数是surface的，只被调用了一次，是不是清空屏幕的哪次？不是，是绘制最外层的框的。只有一次。

DSCAPS_PREMULTIPLIED 这个也是强制设置的。

QDirectFbBlitter 看看构造被哪些地方调用了。



qpaintengine_blitter.cpp这个是核心。

```
QBlitterPaintEngine : public QRasterPaintEngine
```

```
QBlitterPaintEngine::fillRect
-> QBlitterPaintEnginePrivate::fillRect
	-> 	pmData->blittable()->alphaFillRect 
```

那么看pmData是怎么回事。

```
QBlitterPaintEnginePrivate的属性：
QBlittablePlatformPixmap *pmData;
构造时，把指针直接赋值。
pmData(QBlittablePlatformPixmap *p)
指针是构造时传递进来。
QBlitterPaintEnginePrivate(QBlittablePlatformPixmap *p)
是这个构造时带来
QBlitterPaintEngine(QBlittablePlatformPixmap *p)
```

也就这里调用了构造函数。

```
QPaintEngine *QBlittablePlatformPixmap::paintEngine() const
{
    if (!m_engine) {
        QBlittablePlatformPixmap *that = const_cast<QBlittablePlatformPixmap *>(this);
        that->m_engine.reset(new QBlitterPaintEngine(that));
    }
    return m_engine.data();
}
```



```c++
QDirectFbBlitterPlatformPixmap *blitPm = static_cast<QDirectFbBlitterPlatformPixmap *>(pixmap.handle());
    QDirectFbBlitter *dfbBlitter = static_cast<QDirectFbBlitter *>(blitPm->blittable());
```

这里创建的吧。

```
QBlittable *QBlittablePlatformPixmap::blittable() const
{
    if (!m_blittable) {
        QBlittablePlatformPixmap *that = const_cast<QBlittablePlatformPixmap *>(this);
        that->m_blittable.reset(this->createBlittable(QSize(w, h), m_alpha));
    }

    return m_blittable.data();
}
```

```
inline QBlittable *QDirectFbBlitterPlatformPixmap::createBlittable(const QSize& size, bool alpha) const
{
    return new QDirectFbBlitter(size, alpha);
}
```

为了方便看动态的变化。

我重新把tslib input打开。现在居然会段错误。

应该是编译的版本问题，重新编译就好了。



wearable例子，fill-rect的操作，没有太多。



我知道之前文字变绿色的问题的原因了，是因为是调试模式。

我设置了这个环境变量导致的。QT_DIRECTFB_BLITTER_DEBUGPAINT

这个可以看出画了哪些rect。



现在可以看看qt是怎么把blend数据传递下去的。

就是设置了一个blend标志，其余的没有什么特别的。

那么就看directfb的处理。

看at128这个显卡怎么处理的。

```
if (state->drawingflags & DSDRAW_BLEND) {
                    ati128_set_blending_function( adrv, adev, state );
                    funcs->FillRectangle = ati128FillBlendRectangle;
                    funcs->DrawRectangle = ati128DrawBlendRectangle;
               }
               else {
                    funcs->FillRectangle = ati128FillRectangle;
                    funcs->DrawRectangle = ati128DrawRectangle;
               }
```

ati128FillBlendRectangle和ati128FillRectangle处理有什么不同。

看不出什么来。

而df_dok在fill-rect和fill-rect-blend的效果上，的确是有明显不同。

看看软件方式是怎么实现的。

gFillRectangle

我自己写代码，单独测试一下blend的行为。

就2个矩形进行操作。

红色：(0,0,200,200)

绿色：(100,100,200,200)

alpha都设置为255 

看看是怎样进行表现。

fill-rect和fill-rect-blend看起来没有区别。

都是绿色叠加在红色上面。

我把绿色的透明度改成0看看。

对于fill-rect，没有变化。

对于fill-rect-blend，则绿色完全不见了。

那么blend的区别就是alpha生效了？

我把绿色的透明度改成100看看。

的确是blend的alpha有作用，而普通的fill-rect的alpha根本就被忽略了。

那就好搞了。

有这么2个参数：

```
unsigned char src1_gb_alpha_en;
unsigned src1_gb_alpha;
```

这个alpha的使能，只在ge2d_blend_config_ex和ge2d_blit_config_ex时候设置了。

但是在libge2d里，blend的具体行为，因为它是分开了2个枚举的。

我感觉这2个不是一回事。

我先只使能src1的alpha的。然后运行一下，看看效果是不是跟当前软件方式的一致。

libge2d的fill-rect的config里，没有从上层取得src1_gb_alpha_en，所以需要改一下。

先这么调通吧。后面可能还是我自己手动ioctl的方式来做。

上层怎么把src1_gb_alpha_en往下传递呢？

那就在buffer_info里增加一个属性？

改好了。测试一下。

没有预期的效果。

看驱动里src1_gb_alpha_en这个怎么用的。

```
ge2d_reg_set_bits(GE2D_GEN_CTRL2,
		cfg->src1_gb_alpha_en, 29, 1);
```



这2个函数多次被调用：

```
xhl -- amlEngineSync 66, 
xhl -- amlEngineReset 73, 
xhl -- amlEngineSync 66, 
xhl -- amlEngineReset 73, 
xhl -- amlEngineSync 66, 
xhl -- amlEngineReset 73, 
xhl -- amlEngineSync 66, 
xhl -- amlEngineReset 73,
```

是起什么作用？都是空函数不管吧。

blend也先不管。只是没有透明效果。

# Blit调试

继续看blit的。

先写blit的测试例子，看看是什么效果。

df_dok里的blit的行为：

```
读取图片，图片是128x128的。
DFBCHECK(dfb->CreateImageProvider( dfb, DATADIR"/melted.png",
                                        &provider ));
     DFBCHECK(provider->GetSurfaceDescription( provider, &dsc ));

     dsc.flags = DSDESC_WIDTH | DSDESC_HEIGHT | DSDESC_PIXELFORMAT;
     dsc.width = SX;
     dsc.height = SY;
     dsc.pixelformat = pixelformat;
创建一个simple 的surface，把图片渲染到surface里。
DFBCHECK(dfb->CreateSurface( dfb, &dsc, &simple ));
     DFBCHECK(provider->RenderTo( provider, simple, NULL ));
     
     
blit的操作
SET_BLITTING_FLAGS( DSBLIT_NOFX );
dest->Blit( dest, simple, NULL,
```

实际效果：就是一张图片的内容在屏幕的不同位置进行显示。

blit函数的参数理解

```
IDirectFBSurface_Blit( IDirectFBSurface   *thiz,
                       IDirectFBSurface   *source,
                       const DFBRectangle *sr,
                       int dx, int dy )
sr为NULL，表示什么含义？
我看基本都是给了NULL
其余参数就没有什么。就是把source这个内容，移动到x/y这个位置上。
```

看一下之前的Blit的实现。

amldev有个clip属性。做什么用途？

```
static inline void
aml_set_clip( AMLGFX_DriverData *amldrv,
		AMLGFX_DeviceData *amldev,
		DFBRegion *clip )
{
	if (amldev->aml_smf.smf_clip)
		return;

	amldev->clip.x1 = clip->x1;
	amldev->clip.y1 = clip->y1;
	amldev->clip.x2 = clip->x2 + 1;
	amldev->clip.y2 = clip->y2 + 1;

	amldev->aml_smf.smf_clip = 1;
}
```

这个函数调用取决于SMF_CLIP

```
if (state->mod_hw & SMF_CLIP){
		aml_set_clip( amldrv, amldev, &state->clip);
	}
```

SMF_CLIP什么时候被设置？

是指显示的范围有变化？

clip应该就是表示当前的surface的范围，移动的时候，就是范围有变动了。

blitfunction_type 包括这些类型：

```
GE2D_BLEND_NOFX,
	blit操作。
GE2D_BLEND_PRE_ALPHACHANNEL,
	amlBlend_Start
GE2D_BLEND_ALPHACHANNEL,
	amlBlend_Start 
GE2D_BLEND_SRC_COLORKEY,
	aml_setColorKey 使能
	amlBlit_Start
	aml_setColorKey 禁止
GE2D_BLEND_COLORIZE,
	另外一种blend。amlBlend_ColorPremultiply_ConstColor
GE2D_BLEND_COLORIZE_ALPHA,
	amlBlend_Start
GE2D_BLEND_SRC_COLORKEY_COLORIZE,
	aml_setColorKey
	amlBlend_ColorPremultiply_ConstColor
	aml_setColorKey
GE2D_ROTATION,
	blit
GE2D_BLEND_COLORALPHA,
	amlBlend_Start
GE2D_NOT_SUPPORT
```

blitfunction_type取值从哪里来？

是SetState调用aml_set_blend_config来设置的。

总的来说，是来自于state->blittingflags

blitfunction_type前提还要是poter_duff_rule是有效值。

poter_duff_rule的设置从哪里来？

还是要来自于SetState

```
if (state->mod_hw & (SMF_SRC_BLEND | SMF_DST_BLEND))
		amldev->poter_duff_rule = aml_ge2d_convert_to_supported_porterduff (state);
```



从这个枚举看，blend的策略有这些：

有的是使用src的颜色和透明度。有的是使用dst的颜色和透明度。



```
typedef enum {
     /*
      * pixel color = sc * cf[sf] + dc * cf[df]
      * pixel alpha = sa * af[sf] + da * af[df]
      * sc = source color
      * sa = source alpha
      * dc = destination color
      * da = destination alpha
      * sf = source blend function
      * df = destination blend function
      * cf[x] = color factor for blend function x
      * af[x] = alpha factor for blend function x
      */
     DSBF_UNKNOWN            = 0,  /*                             */
     DSBF_ZERO               = 1,  /* cf:    0           af:    0 */
     DSBF_ONE                = 2,  /* cf:    1           af:    1 */
     DSBF_SRCCOLOR           = 3,  /* cf:   sc           af:   sa */
     DSBF_INVSRCCOLOR        = 4,  /* cf: 1-sc           af: 1-sa */
     DSBF_SRCALPHA           = 5,  /* cf:   sa           af:   sa */
     DSBF_INVSRCALPHA        = 6,  /* cf: 1-sa           af: 1-sa */
     DSBF_DESTALPHA          = 7,  /* cf:   da           af:   da */
     DSBF_INVDESTALPHA       = 8,  /* cf: 1-da           af: 1-da */
     DSBF_DESTCOLOR          = 9,  /* cf:   dc           af:   da */
     DSBF_INVDESTCOLOR       = 10, /* cf: 1-dc           af: 1-da */
     DSBF_SRCALPHASAT        = 11  /* cf: min(sa, 1-da)  af:    1 */
} DFBSurfaceBlendFunction;
```

在CardState里，包括了src_blend和dst_blend。

这二者的组合，得到porter-duff类型。

```
例如：
src_blend==zero
	如果dst_blend也等于zero，则porter-duff类型是clear。
	如果dst_blend是one，那么是使用dst的颜色和透明度。
	还有dst_in、dst_out这样的porter-duff。
```



当前ge2d的blend策略都是add的策略。

```
amldev->blend_op.color_blending_mode = OPERATION_ADD;
		amldev->blend_op.alpha_blending_mode = OPERATION_ADD;
```

先写一个blit的测试例子。

```
红色矩形：在（0,0），大小100x100
绿色矩形：在（400,400），大小200x200
把红色矩形移动到（400,400）
看颜色是否有融合的效果。
先看软件模拟的方式的。
```

先看df_dok里的blit的逻辑。

```
SET_BLITTING_FLAGS( DSBLIT_NOFX );
dest->Blit( dest, simple, NULL,
```

这个Blit是操作一个surface，而不是一个矩形。移动后，原来的位置图案还是保留的，并没有被清除掉。

要分析改造一下。

我肯定是用矩形色块来做。这样简单纯粹。

那就是先在dest这个surface上画一个绿色的矩形。

然后在simple这个surface上画红色矩形。

```
dest->SetDrawingFlags( dest, DSDRAW_NOFX);
dest->SetColor(dest, 0x00, 0xff,0x00, 100);
dest->FillRectangle(dest, 400,400,200,200);
//create simple surface
DFBRectangle rect = {0,0,100,100};
primary->GetSubSurface (primary, &rect, &simple);
simple->SetDrawingFlags(simple, DSDRAW_NOFX);
simple->SetColor(simple, 0xff, 0,0, 0xff);
simple->FillRectangle(simple, 0,0,100,100);
sleep(2);
//blit
dest->Blit(dest, simple, NULL, 400,400);
```

上面的代码没有涉及blend。

用软件方式，可以看到效果是正常的。

ge2d的，那我只需要先实现这个分支。

```
case GE2D_BLEND_NOFX:
			amlBlit_ConfigEx(drv, dev, rect, amldev->src_info, amldev->dst_info);
			amlBlit_Start(drv, dev, rect, dx, dy, GE2D_BLIT, SRC_TO_DST);
```

先要看懂libge2d的blit config需要传递哪些参数进来。然后就知道应该给info填哪些参数。

```
src_info[0]
dst_info
```

```
src_info传递的参数
memtype
format
rect  这个重点
layer_mode
rotation
plane_alpha

就上面这些，dst_info不要管layer_mode和plane_alpha。

可以看到canvas_w和canvas_h根本没用。所以写什么值都没关系。
```

现在的问题就是，位置和宽高信息从上层哪里获取到？

amldev里有哪些信息？

那要看SetState传递了位置信息没有。

当前只有宽高信息，位置信息没有。

那还是回到最上层，

dest->Blit(dest, simple, NULL, 400,400);

这里只传递了位置信息。400,400 坐标值给了谁？

simple自己就包含了自己的位置和宽高信息。

调用

```
CoreGraphicsStateClient_Blit( &data->state_client, &srect, &p, 1 );
这里就有传递一个rect和一个point信息。
```

然后就调用到显卡的函数了

```
card->funcs.Blit( card->driver_data, card->device_data,
                                                &srect, drect.x, drect.y )
```

在srect就包含了被移动的surface的位置和宽高信息。

就是这里了

```
amlBlit( void *drv, void *dev, DFBRectangle *rect, int dx, int dy )
```

那就从rect里取值就好了。

而目标的xy值，需要给amlBlit_ConfigEx函数增加参数。必须在这里传递过来。

不过libge2d里，dst没有给位置信息。

```
ge2d_config_ex->dst_para.left = 0;
    ge2d_config_ex->dst_para.top = 0;
```

那怎么知道移动到什么位置？

先不加xy的参数。运行一下看看效果。

我现在这样填写的参数

```
pge2dinfo->dst_info.rect.x = 0;
	pge2dinfo->dst_info.rect.y = 200;
	pge2dinfo->dst_info.rect.w = 0;
	pge2dinfo->dst_info.rect.h = 0;
```

红色块被移动到0,200的位置。大小正常。

位置信息还是传递下去了的。但是是在blit这一步传递，而不是config这一步传递。

```
static int ge2d_blit(int fd,aml_ge2d_info_t *pge2dinfo,rectangle_t *rect,unsigned int dx,unsigned int dy)
```

那就解释得通了。

把dx和dy赋值给下面的。就正常了。

```
pge2dinfo->dst_info.rect.x = 0;
	pge2dinfo->dst_info.rect.y = 200;
```

现在普通的blit可以了。

但是df_dok --blit不行。

打印没看到报错。可能是图片的显示问题。



# blit带blend效果

先看df_dok的blit-blend的函数。

```
SET_BLITTING_FLAGS( DSBLIT_BLEND_ALPHACHANNEL );
dest->Blit( dest, image32a, NULL,
```

没有什么特别的。就是先设置了blitting flag。

DSBLIT_BLEND_ALPHACHANNEL 这个表示使用src的透明度。





# 涉及的知识点

## Porter-Duff 操作

Porter-Duff 操作是 1 组 12 项用于描述数字图像合成的基本手法，包括
Clear、Source Only、Destination Only、Source Over、Source In、Source
Out、Source Atop、Destination Over、Destination In、Destination
Out、Destination Atop、XOR。

**通过组合使用 Porter-Duff 操作，可完成任意 2D图像的合成。**

 Thomas Porter 和 Tom Duff 发表于 1984

PorterDuffXfermode类主要用于图形合成时的图像过渡模式计算，

其概念来自于1984年在ACM SIGGRAPH计算机图形学出版物上发表了“Compositing digital images（合成数字图像）”的Tomas Porter和Tom Duff，

**合成图像的概念极大地推动了图形图像学的发展，**

PorterDuffXfermode类名就来源于这俩人的名字组合PorterDuff。

下面是android SDK中PorterDuff的Mode枚举类型定义。



```undefined
Sa：全称为Source alpha，表示源图的Alpha通道；
Sc：全称为Source color，表示源图的颜色；
Da：全称为Destination alpha，表示目标图的Alpha通道；
Dc：全称为Destination color，表示目标图的颜色.
```

当Alpha通道的值为1时，图像完全可见；

当Alpha通道值为0时，图像完全不可见；

当Alpha通道的值介于0和1之间时，图像只有一部分可见。

Alpha通道描述的是图像的形状，而不是透明度。







Porter-Duff 的由来

https://www.douban.com/note/143111853/

各个击破搞明白PorterDuff.Mode

https://www.jianshu.com/p/d11892bbe055

## color key

1.大图像A是1920x1080大小，在上面贴一个小图像300x200（称为图像B，作为OSD），一般这个osd的数据结构可能是：
struct osd_type {
    void *raster;      //图像点阵
    int alpha;        //0到100的透明度
    int colorkey;      //colorkey值
    int flag;         //标记（alpha或colorkey使能）
};（这个数据结构是我想象出来的，不要对号入座，八九不离十吧）

flag 比如设置为 ENABLE_ALPHA | ENABLE_COLORKEY，

colorkey为0xffffff（白色），alpha为50%；

那么实际效果是：osd的0xffffff全部过滤掉，其它地方显示50%亮度。

Colorkey技术是作用在两个图像叠加混合的时候，

对特殊色做特殊过滤，符合条件的区域叫match区，

在match区就全部使用另外一个图层的颜色值，

不符合条件的区域就是非match区，非match区就是走普通的alpha混合。

Alpha值越大就是越不透明。



alpha和color key

https://blog.csdn.net/fantasker/article/details/79508755

# 参考资料

1、2D图形加速引擎（GE2D）_Wayne Woo的专栏-程序员宅基地

http://www.cxyzjd.com/article/Righthek/72853531

2、

http://seenaburns.com/2018/04/04/writing-to-the-framebuffer/

3、

https://stackoverflow.com/questions/6278824/how-a-compat-ioctl-gets-called-from-the-user-space-can-anybody-please-provide-s



