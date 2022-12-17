---
title: lua之cfadmin web框架学习
date: 2022-12-14 18:29:17
tags:
	- lua

---

--

代码在这里

https://github.com/cfadmin-cn/cfadmin

编译：

```
# 先编译依赖，依赖了libev、libeio、lua
./build.sh
# 然后编译cfamdin
make build
```

运行：

```
./cfadmin 
```

现在会报一个mysql数据库连不上的问题。

所以我先通过docker安装一个mysql。

算了。直接通过docker启动吧。

```
docker-compose -f docker-compose-with-cfadmin.yaml up
```

启动时打印的日志：

```
Creating network "docker_Web_Net" with driver "bridge"
Pulling WebDB (mysql:5.6)...
5.6: Pulling from library/mysql
35b2232c987e: Pull complete
fc55c00e48f2: Pull complete
0030405130e3: Pull complete
e1fef7f6a8d1: Pull complete
1c76272398bb: Pull complete
f57e698171b6: Pull complete
f5b825b269c0: Pull complete
dcb0af686073: Pull complete
27bbfeb886d1: Pull complete
6f70cc868145: Pull complete
1f6637f4600d: Pull complete
Digest: sha256:20575ecebe6216036d25dab5903808211f1e9ba63dc7825ac20cb975e34cfcae
Status: Downloaded newer image for mysql:5.6
Pulling WebApp (candymi/cfweb:)...
latest: Pulling from candymi/cfweb
2d473b07cdd5: Pull complete
d64fb057524e: Pull complete
a3ed95caeb02: Pull complete
Digest: sha256:ac574572d4c40bd684844291f270a687beb530eb4a635a9ea86182836eb64a3f
Status: Downloaded newer image for candymi/cfweb:latest
Creating docker_WebDB_1 ... done
Creating docker_WebApp_1 ... done
Attaching to docker_WebDB_1, docker_WebApp_1
WebDB_1   | 2022-12-14 10:45:34+00:00 [Note] [Entrypoint]: Entrypoint script for MySQL Server 5.6.51-1debian9 started.
WebDB_1   | 2022-12-14 10:45:34+00:00 [Note] [Entrypoint]: Switching to dedicated user 'mysql'
WebDB_1   | 2022-12-14 10:45:34+00:00 [Note] [Entrypoint]: Entrypoint script for MySQL Server 5.6.51-1debian9 started.
WebDB_1   | 2022-12-14 10:45:34+00:00 [Note] [Entrypoint]: Initializing database files
WebDB_1   | 2022-12-14 10:45:35 0 [Warning] TIMESTAMP with implicit DEFAULT value is deprecated. Please use --explicit_defaults_for_timestamp server option (see documentation for more details).
WebDB_1   | 2022-12-14 10:45:35 0 [Note] Ignoring --secure-file-priv value as server is running with --bootstrap.
WebDB_1   | 2022-12-14 10:45:35 0 [Note] /usr/sbin/mysqld (mysqld 5.6.51) starting as process 47 ...
WebDB_1   | 2022-12-14 10:45:35 47 [Note] InnoDB: Using atomics to ref count buffer pool pages
WebDB_1   | 2022-12-14 10:45:35 47 [Note] InnoDB: The InnoDB memory heap is disabled
WebDB_1   | 2022-12-14 10:45:35 47 [Note] InnoDB: Mutexes and rw_locks use GCC atomic builtins
WebDB_1   | 2022-12-14 10:45:35 47 [Note] InnoDB: Memory barrier is not used
WebDB_1   | 2022-12-14 10:45:35 47 [Note] InnoDB: Compressed tables use zlib 1.2.11
WebDB_1   | 2022-12-14 10:45:35 47 [Note] InnoDB: Using Linux native AIO
WebDB_1   | 2022-12-14 10:45:35 47 [Note] InnoDB: Using CPU crc32 instructions
WebDB_1   | 2022-12-14 10:45:35 47 [Note] InnoDB: Initializing buffer pool, size = 128.0M
WebDB_1   | 2022-12-14 10:45:35 47 [Note] InnoDB: Completed initialization of buffer pool
WebDB_1   | 2022-12-14 10:45:35 47 [Note] InnoDB: The first specified data file ./ibdata1 did not exist: a new database to be created!
WebDB_1   | 2022-12-14 10:45:35 47 [Note] InnoDB: Setting file ./ibdata1 size to 12 MB
WebDB_1   | 2022-12-14 10:45:35 47 [Note] InnoDB: Database physically writes the file full: wait...
WebDB_1   | 2022-12-14 10:45:35 47 [Note] InnoDB: Setting log file ./ib_logfile101 size to 48 MB
WebApp_1  | [2022-12-14 10:45:34,921] [@lualib/DB/mysql.lua:42] [WARN] : "The connection failed. The reasons are: [MySQL Server Connect failed.], Try to reconnect after 3 seconds" 
WebDB_1   | 2022-12-14 10:45:35 47 [Note] InnoDB: Setting log file ./ib_logfile1 size to 48 MB
WebDB_1   | 2022-12-14 10:45:35 47 [Note] InnoDB: Renaming log file ./ib_logfile101 to ./ib_logfile0
WebDB_1   | 2022-12-14 10:45:35 47 [Warning] InnoDB: New log files created, LSN=45781
WebDB_1   | 2022-12-14 10:45:35 47 [Note] InnoDB: Doublewrite buffer not found: creating new
WebDB_1   | 2022-12-14 10:45:35 47 [Note] InnoDB: Doublewrite buffer created
WebDB_1   | 2022-12-14 10:45:35 47 [Note] InnoDB: 128 rollback segment(s) are active.
WebDB_1   | 2022-12-14 10:45:35 47 [Warning] InnoDB: Creating foreign key constraint system tables.
WebDB_1   | 2022-12-14 10:45:35 47 [Note] InnoDB: Foreign key constraint system tables created
WebDB_1   | 2022-12-14 10:45:35 47 [Note] InnoDB: Creating tablespace and datafile system tables.
WebDB_1   | 2022-12-14 10:45:35 47 [Note] InnoDB: Tablespace and datafile system tables created.
WebDB_1   | 2022-12-14 10:45:35 47 [Note] InnoDB: Waiting for purge to start
WebDB_1   | 2022-12-14 10:45:36 47 [Note] InnoDB: 5.6.51 started; log sequence number 0
WebDB_1   | 2022-12-14 10:45:36 47 [Note] RSA private key file not found: /var/lib/mysql//private_key.pem. Some authentication plugins will not work.
WebDB_1   | 2022-12-14 10:45:36 47 [Note] RSA public key file not found: /var/lib/mysql//public_key.pem. Some authentication plugins will not work.
WebDB_1   | 2022-12-14 10:45:36 47 [Note] Binlog end
WebDB_1   | 2022-12-14 10:45:36 47 [Note] InnoDB: FTS optimize thread exiting.
WebDB_1   | 2022-12-14 10:45:36 47 [Note] InnoDB: Starting shutdown...
WebDB_1   | 2022-12-14 10:45:37 47 [Note] InnoDB: Shutdown completed; log sequence number 1625977
WebDB_1   | 
WebDB_1   | 
WebDB_1   | 2022-12-14 10:45:37 0 [Warning] TIMESTAMP with implicit DEFAULT value is deprecated. Please use --explicit_defaults_for_timestamp server option (see documentation for more details).
WebDB_1   | 2022-12-14 10:45:37 0 [Note] Ignoring --secure-file-priv value as server is running with --bootstrap.
WebDB_1   | 2022-12-14 10:45:37 0 [Note] /usr/sbin/mysqld (mysqld 5.6.51) starting as process 70 ...
WebDB_1   | 2022-12-14 10:45:37 70 [Note] InnoDB: Using atomics to ref count buffer pool pages
WebDB_1   | 2022-12-14 10:45:37 70 [Note] InnoDB: The InnoDB memory heap is disabled
WebDB_1   | 2022-12-14 10:45:37 70 [Note] InnoDB: Mutexes and rw_locks use GCC atomic builtins
WebDB_1   | 2022-12-14 10:45:37 70 [Note] InnoDB: Memory barrier is not used
WebDB_1   | 2022-12-14 10:45:37 70 [Note] InnoDB: Compressed tables use zlib 1.2.11
WebDB_1   | 2022-12-14 10:45:37 70 [Note] InnoDB: Using Linux native AIO
WebDB_1   | 2022-12-14 10:45:37 70 [Note] InnoDB: Using CPU crc32 instructions
WebDB_1   | 2022-12-14 10:45:37 70 [Note] InnoDB: Initializing buffer pool, size = 128.0M
WebDB_1   | 2022-12-14 10:45:37 70 [Note] InnoDB: Completed initialization of buffer pool
WebDB_1   | 2022-12-14 10:45:37 70 [Note] InnoDB: Highest supported file format is Barracuda.
WebDB_1   | 2022-12-14 10:45:37 70 [Note] InnoDB: 128 rollback segment(s) are active.
WebDB_1   | 2022-12-14 10:45:37 70 [Note] InnoDB: Waiting for purge to start
WebDB_1   | 2022-12-14 10:45:37 70 [Note] InnoDB: 5.6.51 started; log sequence number 1625977
WebDB_1   | 2022-12-14 10:45:37 70 [Note] RSA private key file not found: /var/lib/mysql//private_key.pem. Some authentication plugins will not work.
WebDB_1   | 2022-12-14 10:45:37 70 [Note] RSA public key file not found: /var/lib/mysql//public_key.pem. Some authentication plugins will not work.
WebDB_1   | 2022-12-14 10:45:38 70 [Note] Binlog end
WebDB_1   | 2022-12-14 10:45:38 70 [Note] InnoDB: FTS optimize thread exiting.
WebDB_1   | 2022-12-14 10:45:38 70 [Note] InnoDB: Starting shutdown...
WebApp_1  | [2022-12-14 10:45:37,922] [@lualib/DB/mysql.lua:42] [WARN] : "The connection failed. The reasons are: [MySQL Server Connect failed.], Try to reconnect after 3 seconds" 
WebDB_1   | 2022-12-14 10:45:39 70 [Note] InnoDB: Shutdown completed; log sequence number 1625987
WebDB_1   | 
WebDB_1   | 
WebDB_1   | 
WebDB_1   | 
WebDB_1   | PLEASE REMEMBER TO SET A PASSWORD FOR THE MySQL root USER !
WebDB_1   | To do so, start the server, then issue the following commands:
WebDB_1   | 
WebDB_1   |   /usr/bin/mysqladmin -u root password 'new-password'
WebDB_1   |   /usr/bin/mysqladmin -u root -h 5be047e70eb6 password 'new-password'
WebDB_1   | 
WebDB_1   | Alternatively you can run:
WebDB_1   | 
WebDB_1   |   /usr/bin/mysql_secure_installation
WebDB_1   | 
WebDB_1   | which will also give you the option of removing the test
WebDB_1   | databases and anonymous user created by default.  This is
WebDB_1   | strongly recommended for production servers.
WebDB_1   | 
WebDB_1   | See the manual for more instructions.
WebDB_1   | 
WebDB_1   | Please report any problems at http://bugs.mysql.com/
WebDB_1   | 
WebDB_1   | The latest information about MySQL is available on the web at
WebDB_1   | 
WebDB_1   |   http://www.mysql.com
WebDB_1   | 
WebDB_1   | Support MySQL by buying support/licenses at http://shop.mysql.com
WebDB_1   | 
WebDB_1   | Note: new default config file not created.
WebDB_1   | Please make sure your config file is current
WebDB_1   | 
WebDB_1   | WARNING: Default config file /etc/mysql/my.cnf exists on the system
WebDB_1   | This file will be read by default by the MySQL server
WebDB_1   | If you do not want to use this, either remove it, or use the
WebDB_1   | --defaults-file argument to mysqld_safe when starting the server
WebDB_1   | 
WebDB_1   | 2022-12-14 10:45:39+00:00 [Note] [Entrypoint]: Database files initialized
WebDB_1   | 2022-12-14 10:45:39+00:00 [Note] [Entrypoint]: Starting temporary server
WebDB_1   | 2022-12-14 10:45:39+00:00 [Note] [Entrypoint]: Waiting for server startup
WebDB_1   | 2022-12-14 10:45:40 0 [Warning] TIMESTAMP with implicit DEFAULT value is deprecated. Please use --explicit_defaults_for_timestamp server option (see documentation for more details).
WebDB_1   | 2022-12-14 10:45:40 0 [Note] mysqld (mysqld 5.6.51) starting as process 95 ...
WebDB_1   | 2022-12-14 10:45:40 95 [Note] Plugin 'FEDERATED' is disabled.
WebDB_1   | 2022-12-14 10:45:40 95 [Note] InnoDB: Using atomics to ref count buffer pool pages
WebDB_1   | 2022-12-14 10:45:40 95 [Note] InnoDB: The InnoDB memory heap is disabled
WebDB_1   | 2022-12-14 10:45:40 95 [Note] InnoDB: Mutexes and rw_locks use GCC atomic builtins
WebDB_1   | 2022-12-14 10:45:40 95 [Note] InnoDB: Memory barrier is not used
WebDB_1   | 2022-12-14 10:45:40 95 [Note] InnoDB: Compressed tables use zlib 1.2.11
WebDB_1   | 2022-12-14 10:45:40 95 [Note] InnoDB: Using Linux native AIO
WebDB_1   | 2022-12-14 10:45:40 95 [Note] InnoDB: Using CPU crc32 instructions
WebDB_1   | 2022-12-14 10:45:40 95 [Note] InnoDB: Initializing buffer pool, size = 128.0M
WebDB_1   | 2022-12-14 10:45:40 95 [Note] InnoDB: Completed initialization of buffer pool
WebDB_1   | 2022-12-14 10:45:40 95 [Note] InnoDB: Highest supported file format is Barracuda.
WebDB_1   | 2022-12-14 10:45:40 95 [Note] InnoDB: 128 rollback segment(s) are active.
WebDB_1   | 2022-12-14 10:45:40 95 [Note] InnoDB: Waiting for purge to start
WebDB_1   | 2022-12-14 10:45:40 95 [Note] InnoDB: 5.6.51 started; log sequence number 1625987
WebDB_1   | 2022-12-14 10:45:40 95 [Warning] No existing UUID has been found, so we assume that this is the first time that this server has been started. Generating a new UUID: 73a6a974-7b9c-11ed-9e3c-0242ac150002.
WebDB_1   | 2022-12-14 10:45:40 95 [Note] RSA private key file not found: /var/lib/mysql//private_key.pem. Some authentication plugins will not work.
WebDB_1   | 2022-12-14 10:45:40 95 [Note] RSA public key file not found: /var/lib/mysql//public_key.pem. Some authentication plugins will not work.
WebDB_1   | 2022-12-14 10:45:40 95 [Warning] Insecure configuration for --pid-file: Location '/var/run/mysqld' in the path is accessible to all OS users. Consider choosing a different directory.
WebDB_1   | 2022-12-14 10:45:40 95 [Warning] 'user' entry 'root@5be047e70eb6' ignored in --skip-name-resolve mode.
WebDB_1   | 2022-12-14 10:45:40 95 [Warning] 'user' entry '@5be047e70eb6' ignored in --skip-name-resolve mode.
WebDB_1   | 2022-12-14 10:45:40 95 [Warning] 'proxies_priv' entry '@ root@5be047e70eb6' ignored in --skip-name-resolve mode.
WebDB_1   | 2022-12-14 10:45:40 95 [Note] Event Scheduler: Loaded 0 events
WebDB_1   | 2022-12-14 10:45:40 95 [Note] mysqld: ready for connections.
WebDB_1   | Version: '5.6.51'  socket: '/var/run/mysqld/mysqld.sock'  port: 0  MySQL Community Server (GPL)
WebDB_1   | 2022-12-14 10:45:41+00:00 [Note] [Entrypoint]: Temporary server started.
WebApp_1  | [2022-12-14 10:45:40,924] [@lualib/DB/mysql.lua:42] [WARN] : "The connection failed. The reasons are: [MySQL Server Connect failed.], Try to reconnect after 3 seconds" 
WebDB_1   | Warning: Unable to load '/usr/share/zoneinfo/iso3166.tab' as time zone. Skipping it.
WebDB_1   | Warning: Unable to load '/usr/share/zoneinfo/leap-seconds.list' as time zone. Skipping it.
WebDB_1   | Warning: Unable to load '/usr/share/zoneinfo/zone.tab' as time zone. Skipping it.
WebDB_1   | Warning: Unable to load '/usr/share/zoneinfo/zone1970.tab' as time zone. Skipping it.
WebDB_1   | 2022-12-14 10:45:42 95 [Warning] 'proxies_priv' entry '@ root@5be047e70eb6' ignored in --skip-name-resolve mode.
WebDB_1   | 2022-12-14 10:45:42+00:00 [Note] [Entrypoint]: Creating database cfadmin
WebDB_1   | 
WebDB_1   | 2022-12-14 10:45:42+00:00 [Note] [Entrypoint]: /usr/local/bin/docker-entrypoint.sh: running /docker-entrypoint-initdb.d/database.sql
WebDB_1   | 
WebDB_1   | 
WebDB_1   | 2022-12-14 10:45:42+00:00 [Note] [Entrypoint]: Stopping temporary server
WebDB_1   | 2022-12-14 10:45:42 95 [Note] mysqld: Normal shutdown
WebDB_1   | 
WebDB_1   | 2022-12-14 10:45:42 95 [Note] Giving 0 client threads a chance to die gracefully
WebDB_1   | 2022-12-14 10:45:42 95 [Note] Event Scheduler: Purging the queue. 0 events
WebDB_1   | 2022-12-14 10:45:42 95 [Note] Shutting down slave threads
WebDB_1   | 2022-12-14 10:45:42 95 [Note] Forcefully disconnecting 0 remaining clients
WebDB_1   | 2022-12-14 10:45:42 95 [Note] Binlog end
WebDB_1   | 2022-12-14 10:45:42 95 [Note] Shutting down plugin 'partition'
WebDB_1   | 2022-12-14 10:45:42 95 [Note] Shutting down plugin 'PERFORMANCE_SCHEMA'
WebDB_1   | 2022-12-14 10:45:42 95 [Note] Shutting down plugin 'INNODB_SYS_DATAFILES'
WebDB_1   | 2022-12-14 10:45:42 95 [Note] Shutting down plugin 'INNODB_SYS_TABLESPACES'
WebDB_1   | 2022-12-14 10:45:42 95 [Note] Shutting down plugin 'INNODB_SYS_FOREIGN_COLS'
WebDB_1   | 2022-12-14 10:45:42 95 [Note] Shutting down plugin 'INNODB_SYS_FOREIGN'
WebDB_1   | 2022-12-14 10:45:42 95 [Note] Shutting down plugin 'INNODB_SYS_FIELDS'
WebDB_1   | 2022-12-14 10:45:42 95 [Note] Shutting down plugin 'INNODB_SYS_COLUMNS'
WebDB_1   | 2022-12-14 10:45:42 95 [Note] Shutting down plugin 'INNODB_SYS_INDEXES'
WebDB_1   | 2022-12-14 10:45:42 95 [Note] Shutting down plugin 'INNODB_SYS_TABLESTATS'
WebDB_1   | 2022-12-14 10:45:42 95 [Note] Shutting down plugin 'INNODB_SYS_TABLES'
WebDB_1   | 2022-12-14 10:45:42 95 [Note] Shutting down plugin 'INNODB_FT_INDEX_TABLE'
WebDB_1   | 2022-12-14 10:45:42 95 [Note] Shutting down plugin 'INNODB_FT_INDEX_CACHE'
WebDB_1   | 2022-12-14 10:45:42 95 [Note] Shutting down plugin 'INNODB_FT_CONFIG'
WebDB_1   | 2022-12-14 10:45:42 95 [Note] Shutting down plugin 'INNODB_FT_BEING_DELETED'
WebDB_1   | 2022-12-14 10:45:42 95 [Note] Shutting down plugin 'INNODB_FT_DELETED'
WebDB_1   | 2022-12-14 10:45:42 95 [Note] Shutting down plugin 'INNODB_FT_DEFAULT_STOPWORD'
WebDB_1   | 2022-12-14 10:45:42 95 [Note] Shutting down plugin 'INNODB_METRICS'
WebDB_1   | 2022-12-14 10:45:42 95 [Note] Shutting down plugin 'INNODB_BUFFER_POOL_STATS'
WebDB_1   | 2022-12-14 10:45:42 95 [Note] Shutting down plugin 'INNODB_BUFFER_PAGE_LRU'
WebDB_1   | 2022-12-14 10:45:42 95 [Note] Shutting down plugin 'INNODB_BUFFER_PAGE'
WebDB_1   | 2022-12-14 10:45:42 95 [Note] Shutting down plugin 'INNODB_CMP_PER_INDEX_RESET'
WebDB_1   | 2022-12-14 10:45:42 95 [Note] Shutting down plugin 'INNODB_CMP_PER_INDEX'
WebDB_1   | 2022-12-14 10:45:42 95 [Note] Shutting down plugin 'INNODB_CMPMEM_RESET'
WebDB_1   | 2022-12-14 10:45:42 95 [Note] Shutting down plugin 'INNODB_CMPMEM'
WebDB_1   | 2022-12-14 10:45:42 95 [Note] Shutting down plugin 'INNODB_CMP_RESET'
WebDB_1   | 2022-12-14 10:45:42 95 [Note] Shutting down plugin 'INNODB_CMP'
WebDB_1   | 2022-12-14 10:45:42 95 [Note] Shutting down plugin 'INNODB_LOCK_WAITS'
WebDB_1   | 2022-12-14 10:45:42 95 [Note] Shutting down plugin 'INNODB_LOCKS'
WebDB_1   | 2022-12-14 10:45:42 95 [Note] Shutting down plugin 'INNODB_TRX'
WebDB_1   | 2022-12-14 10:45:42 95 [Note] Shutting down plugin 'InnoDB'
WebDB_1   | 2022-12-14 10:45:42 95 [Note] InnoDB: FTS optimize thread exiting.
WebDB_1   | 2022-12-14 10:45:42 95 [Note] InnoDB: Starting shutdown...
WebApp_1  | [2022-12-14 10:45:43,924] [@lualib/DB/mysql.lua:42] [WARN] : "The connection failed. The reasons are: [MySQL Server Connect failed.], Try to reconnect after 3 seconds" 
WebDB_1   | 2022-12-14 10:45:44 95 [Note] InnoDB: Shutdown completed; log sequence number 1663905
WebDB_1   | 2022-12-14 10:45:44 95 [Note] Shutting down plugin 'BLACKHOLE'
WebDB_1   | 2022-12-14 10:45:44 95 [Note] Shutting down plugin 'ARCHIVE'
WebDB_1   | 2022-12-14 10:45:44 95 [Note] Shutting down plugin 'MRG_MYISAM'
WebDB_1   | 2022-12-14 10:45:44 95 [Note] Shutting down plugin 'MyISAM'
WebDB_1   | 2022-12-14 10:45:44 95 [Note] Shutting down plugin 'MEMORY'
WebDB_1   | 2022-12-14 10:45:44 95 [Note] Shutting down plugin 'CSV'
WebDB_1   | 2022-12-14 10:45:44 95 [Note] Shutting down plugin 'sha256_password'
WebDB_1   | 2022-12-14 10:45:44 95 [Note] Shutting down plugin 'mysql_old_password'
WebDB_1   | 2022-12-14 10:45:44 95 [Note] Shutting down plugin 'mysql_native_password'
WebDB_1   | 2022-12-14 10:45:44 95 [Note] Shutting down plugin 'binlog'
WebDB_1   | 2022-12-14 10:45:44 95 [Note] mysqld: Shutdown complete
WebDB_1   | 
WebDB_1   | 2022-12-14 10:45:44+00:00 [Note] [Entrypoint]: Temporary server stopped
WebDB_1   | 
WebDB_1   | 2022-12-14 10:45:44+00:00 [Note] [Entrypoint]: MySQL init process done. Ready for start up.
WebDB_1   | 
WebDB_1   | 2022-12-14 10:45:44 0 [Warning] TIMESTAMP with implicit DEFAULT value is deprecated. Please use --explicit_defaults_for_timestamp server option (see documentation for more details).
WebDB_1   | 2022-12-14 10:45:44 0 [Note] mysqld (mysqld 5.6.51) starting as process 1 ...
WebDB_1   | 2022-12-14 10:45:44 1 [Note] Plugin 'FEDERATED' is disabled.
WebDB_1   | 2022-12-14 10:45:44 1 [Note] InnoDB: Using atomics to ref count buffer pool pages
WebDB_1   | 2022-12-14 10:45:44 1 [Note] InnoDB: The InnoDB memory heap is disabled
WebDB_1   | 2022-12-14 10:45:44 1 [Note] InnoDB: Mutexes and rw_locks use GCC atomic builtins
WebDB_1   | 2022-12-14 10:45:44 1 [Note] InnoDB: Memory barrier is not used
WebDB_1   | 2022-12-14 10:45:44 1 [Note] InnoDB: Compressed tables use zlib 1.2.11
WebDB_1   | 2022-12-14 10:45:44 1 [Note] InnoDB: Using Linux native AIO
WebDB_1   | 2022-12-14 10:45:44 1 [Note] InnoDB: Using CPU crc32 instructions
WebDB_1   | 2022-12-14 10:45:44 1 [Note] InnoDB: Initializing buffer pool, size = 128.0M
WebDB_1   | 2022-12-14 10:45:44 1 [Note] InnoDB: Completed initialization of buffer pool
WebDB_1   | 2022-12-14 10:45:44 1 [Note] InnoDB: Highest supported file format is Barracuda.
WebDB_1   | 2022-12-14 10:45:44 1 [Note] InnoDB: 128 rollback segment(s) are active.
WebDB_1   | 2022-12-14 10:45:44 1 [Note] InnoDB: Waiting for purge to start
WebDB_1   | 2022-12-14 10:45:44 1 [Note] InnoDB: 5.6.51 started; log sequence number 1663905
WebDB_1   | 2022-12-14 10:45:44 1 [Note] RSA private key file not found: /var/lib/mysql//private_key.pem. Some authentication plugins will not work.
WebDB_1   | 2022-12-14 10:45:44 1 [Note] RSA public key file not found: /var/lib/mysql//public_key.pem. Some authentication plugins will not work.
WebDB_1   | 2022-12-14 10:45:44 1 [Note] Server hostname (bind-address): '*'; port: 3306
WebDB_1   | 2022-12-14 10:45:44 1 [Note] IPv6 is available.
WebDB_1   | 2022-12-14 10:45:44 1 [Note]   - '::' resolves to '::';
WebDB_1   | 2022-12-14 10:45:44 1 [Note] Server socket created on IP: '::'.
WebDB_1   | 2022-12-14 10:45:44 1 [Warning] Insecure configuration for --pid-file: Location '/var/run/mysqld' in the path is accessible to all OS users. Consider choosing a different directory.
WebDB_1   | 2022-12-14 10:45:44 1 [Warning] 'proxies_priv' entry '@ root@5be047e70eb6' ignored in --skip-name-resolve mode.
WebDB_1   | 2022-12-14 10:45:44 1 [Note] Event Scheduler: Loaded 0 events
WebDB_1   | 2022-12-14 10:45:44 1 [Note] mysqld: ready for connections.
WebDB_1   | Version: '5.6.51'  socket: '/var/run/mysqld/mysqld.sock'  port: 3306  MySQL Community Server (GPL)
WebApp_1  | [2022/12/14 10:45:46] [INFO] httpd listen: 0.0.0.0:8080 
WebApp_1  | [2022/12/14 10:45:46] [INFO] httpd Web Server Running...

```

然后通过http://192.168.56.101:8080/index.html 这个地址访问。

这个地址进入到后台：

http://192.168.56.101:8080/admin

登陆的用户名和密码是：

```
admin
admin
```

# master进程和worker进程

默认不带任何参数运行时，是单进程，也就是只有一个worker进程。worker进程就是跑业务的进程。

master进程的作用就是根据需要去fork多个work进程。



# 参考资料

