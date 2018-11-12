---
title: glib和glibc关系
date: 2018-11-12 13:19:19
tags:
	- C语言

---



准确来说，没有关系。

glib的g表示的GTK的底层。里面定义的都是GObject这些类型的数据类型。

glib加了很多的高级用法。例如队列等。

```
hlxiong@hlxiong-VirtualBox:/usr/include/glib-2.0/glib$ ls
deprecated     gbitlock.h       gdate.h       ghash.h       gkeyfile.h           gmem.h       gprintf.h   gsequence.h  gstringchunk.h  gtrashstack.h  gvarianttype.h
galloca.h      gbookmarkfile.h  gdatetime.h   ghmac.h       glib-autocleanups.h  gmessages.h  gqsort.h    gshell.h     gstring.h       gtree.h        gversion.h
garray.h       gbytes.h         gdir.h        ghook.h       glist.h              gnode.h      gquark.h    gslice.h     gtestutils.h    gtypes.h       gversionmacros.h
gasyncqueue.h  gcharset.h       genviron.h    ghostutils.h  gmacros.h            goption.h    gqueue.h    gslist.h     gthread.h       gunicode.h     gwin32.h
gatomic.h      gchecksum.h      gerror.h      gi18n.h       gmain.h              gpattern.h   grand.h     gspawn.h     gthreadpool.h   gurifuncs.h
gbacktrace.h   gconvert.h       gfileutils.h  gi18n-lib.h   gmappedfile.h        gpoll.h      gregex.h    gstdio.h     gtimer.h        gutils.h
gbase64.h      gdataset.h       ggettext.h    giochannel.h  gmarkup.h            gprimes.h    gscanner.h  gstrfuncs.h  gtimezone.h     gvariant.h
```



gtypes.h

```
typedef char   gchar;
typedef short  gshort;
typedef long   glong;
typedef int    gint;
typedef gint   gboolean;

typedef unsigned char   guchar;
typedef unsigned short  gushort;
typedef unsigned long   gulong;
typedef unsigned int    guint;

typedef float   gfloat;
typedef double  gdouble;
```

这些东西也是自己定义的一套。

```
union _GMutex
{
  /*< private >*/
  gpointer p;
  guint i[2];
};

struct _GRWLock
{
  /*< private >*/
  gpointer p;
  guint i[2];
};

struct _GCond
{
  /*< private >*/
  gpointer p;
  guint i[2];
};

```







