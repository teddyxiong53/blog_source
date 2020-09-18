---
title: snapcast之snapdroid代码分析
date: 2020-09-15 16:18:32
tags:
	- java

---

1

snapdroid还比较适合做java和Android的学习材料。

业务逻辑不复杂，各种组件都用到了。又是一个有实用价值的程序。所以值得学习。

# 定义一个枚举

```
    public enum RPCEvent {
        response,
        notification
    }
```

# Snackbar

这个跟toast类似，但是表现更强烈。

用来表示一些警告信息。

![img](../images/random_name/828721-476620e85b863aa6.webp)

# ServiceConnection

先new一个ServiceConnection。

```
private ServiceConnection mConnection = new ServiceConnection() {

        @Override
        public void onServiceConnected(ComponentName className,
                                       IBinder service) {

        }

        @Override
        public void onServiceDisconnected(ComponentName arg0) {
            bound = false;
        }
    };
```

然后在onStart的地方。绑定service和activity。

```
Intent intent = new Intent(this, SnapclientService.class);
bindService(intent, mConnection, Context.BIND_AUTO_CREATE);
```

# 修改ui元素

这样来提交给ui线程来做。

```
MainActivity.this.runOnUiThread(new Runnable() {
            @Override
            public void run() {
                ActionBar actionBar = getSupportActionBar();
                if (actionBar != null)
                    actionBar.setSubtitle(subtitle);
            }
        });
```

# checkFirstRun

检测第一次运行的方法。

读取package信息。和当前的进行对比。

# 选项菜单处理

onCreateOptionsMenu

onOptionsItemSelected

# 保持屏幕常亮

这样开启保持常亮。

```
PowerManager powerManager = (PowerManager) getSystemService(POWER_SERVICE);
            wakeLock = powerManager.newWakeLock(PARTIAL_WAKE_LOCK, "snapcast:SnapcastPartialWakeLock");
            wakeLock.acquire();

```



这个是停止保持常亮。

```
getWindow().clearFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
```

# 保持wifi网络活跃

这个跟保持屏幕常亮是类似的，都是为了业务需要，保持wifi不要休眠。

```
WifiManager wm = (WifiManager) getApplicationContext().getSystemService(WIFI_SERVICE);
            wifiWakeLock = wm.createWifiLock(WifiManager.WIFI_MODE_FULL_HIGH_PERF, "snapcast:SnapcastWifiWakeLock");
            wifiWakeLock.acquire();
```

释放：

```
wifiWakeLock.release();
```



# 启动一个进程

```
ProcessBuilder pb = new ProcessBuilder()
                .command(this.getApplicationInfo().nativeLibraryDir + "/libsnapclient.so", "-h", host, "-p", Integer.toString(port), "--hostID", getUniqueId(this.getApplicationContext()), "--player", player, "--sampleformat", sampleformat)
                .redirectErrorStream(true);
                
process = pb.start();
```



# TaskStackBuilder

# 前台服务

这个可以提供优先级。保活。



# json处理





参考资料

1、

