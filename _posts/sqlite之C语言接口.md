---
title: sqlite之C语言接口
date: 2018-11-01 14:11:19
tags:
	- 数据库

---



分析一下sqlite3.h内容。

```
typedef int (*sqlite3_callback)(void*,int,char**, char**);
```

```
int SQLITE_STDCALL sqlite3_exec(
  sqlite3*,                                  /* An open database */
  const char *sql,                           /* SQL to be evaluated */
  int (*callback)(void*,int,char**,char**),  /* Callback function */
  void *,                                    /* 1st argument to callback */
  char **errmsg                              /* Error msg written here */
);
```

错误码

```
#define SQLITE_OK           0   /* Successful result */
/* beginning-of-error-codes */
#define SQLITE_ERROR        1   /* SQL error or missing database */
#define SQLITE_INTERNAL     2   /* Internal logic error in SQLite */
#define SQLITE_PERM         3   /* Access permission denied */
#define SQLITE_ABORT        4   /* Callback routine requested an abort */
```

```
SQLITE_API int SQLITE_STDCALL sqlite3_initialize(void);
SQLITE_API int SQLITE_STDCALL sqlite3_shutdown(void);
SQLITE_API int SQLITE_STDCALL sqlite3_os_init(void);
SQLITE_API int SQLITE_STDCALL sqlite3_os_end(void);
```



```
#include <stdio.h>
#include <string.h>
#include <sqlite3.h>
 
/***************************
typedef int (*sqlite3_callback)(
void*,    // Data provided in the 4th argument of sqlite3_exec()
int,        // The number of columns in row 
char**,   // An array of strings representing fields in the row 
char**    // An array of strings representing column names 
);
***************************/
 
/* callback函数只有在对数据库进行select, 操作时才会调用 */
static int select_callback(void *data, int argc, char **argv, char **azColName){
   int i;
   printf("%s", (char*)data);
   for(i=0; i < argc; i++){
      printf("%s = %s\n", azColName[i], argv[i] ? argv[i] : "NULL");
   }
   printf("\n");
   return 0;
}
 
int main(int argc, char* argv[])
{
   sqlite3 *db;
   char *zErrMsg = 0;
   int rc;
 
   /* 数据库创建或打开 */
   rc = sqlite3_open("test.db", &db);
 
   if( rc ){
      fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
      exit(0);
   }else{
      fprintf(stderr, "Opened database successfully\n");
   }
 
   char* sql;
   sql = "create table healthinfo (" \
           "sid int primary key not null," \
           "name text not null," \
           "ishealth char(4) not null);";
 
   /* 创建表 */
   rc = sqlite3_exec(db, sql, NULL, NULL, &zErrMsg);
   if( rc != SQLITE_OK ){
      fprintf(stderr, "SQL error: %s\n", zErrMsg);
      sqlite3_free(zErrMsg);
   }else{
      fprintf(stdout, "Table created successfully\n");
   }
 
   sql = "insert into healthinfo (sid, name, ishealth)" \
           "values (201601001, 'xiaowang', 'yes');" \
           "insert into healthinfo (sid, name, ishealth)" \
           "values (201601002, 'xiaoli', 'yes');" \
           "insert into healthinfo (sid, name, ishealth)" \
           "values (201601003, 'xiaozhang', 'no');" \
           "insert into healthinfo (sid, name, ishealth)" \
           "values (201601004, 'xiaozhou', 'yes');" \
           "insert into healthinfo (sid, name, ishealth)" \
           "values (201601005, 'xiaosun', 'yes');";
 
    /* 插入数据 */
   rc = sqlite3_exec(db, sql, NULL, NULL, &zErrMsg);
   if( rc != SQLITE_OK ){
      fprintf(stderr, "SQL error: %s\n", zErrMsg);
      sqlite3_free(zErrMsg);
   }else{
      fprintf(stdout, "Table insert data successfully\n");
   }
 
   char* strname = "xiaoyang";
   //char strname[256] = {'x','i','a','o','y','a','n','g'};
   char sql2[256] = {'0'};
   /* 不推荐使用这种方式 */
   sprintf(sql2, "insert into healthinfo (sid, name, ishealth) values (201601006, '%s', 'yes');", strname);
    /* 插入数据 */
   rc = sqlite3_exec(db, sql2, NULL, NULL, &zErrMsg);
   if( rc != SQLITE_OK ){
      fprintf(stderr, "SQL error: %s\n", zErrMsg);
      sqlite3_free(zErrMsg);
   }else{
      fprintf(stdout, "Table insert data successfully\n");
   }
 
   /***********  存数据和取数据的第二种方法***********/
  
   sql = "insert into healthinfo (sid, name, ishealth)" \
           "values (:sid, :name, :ishealth);";   /* 注: ":sid" 为命名参数 也可以用? 号*/
 
   sqlite3_stmt *stmt;
   /* 准备一个语句对象 */
   sqlite3_prepare_v2(db, sql, strlen(sql), &stmt, NULL); 
   /* 语句对象绑定的参数个数也就是上面sql语句values括号中的参数 */
   printf("max_parameter_count = %d\n", sqlite3_bind_parameter_count(stmt));
   /* 只有上面指定了:sid这个名字才可以用 */
   printf("sid parameter index = %d\n", sqlite3_bind_parameter_index(stmt, ":sid")); 
   printf("name parameter index = %d\n", sqlite3_bind_parameter_index(stmt, ":name"));
   printf("ishealth parameter index = %d\n", sqlite3_bind_parameter_index(stmt, ":ishealth"));
   /* 如果是?号命名的则返回的文本为null */
   printf("index = 1 's parameter's name = %s\n", sqlite3_bind_parameter_name(stmt, 1)); 
   sqlite3_bind_int(stmt, 1, 201601007);
   sqlite3_bind_text(stmt, 2, "xiaoqian", -1, NULL); /* 第四个参数设为负数则自动计算第三个参数的长度 */
   sqlite3_bind_text(stmt, 3, "yes", 3, NULL);
   //sqlite3_bind_blob(stmt, 1, sectionData, 4096, SQLITE_STATIC); /* 将sectonData 绑定到stmt对象 */
   
   /* 执行sql 语句对象并判断其返回值
       发现如果不是select 这样会产生结果集的操作
       返回值为SQLITE_DONE 或者出错，只有执行sql语句会产生
       结果集执行step函数才返回SQLITE_ROW*/
   rc = sqlite3_step(stmt);  
   printf("step() return %s\n", rc == SQLITE_DONE ? "SQLITE_DONE" \
                                          : rc == SQLITE_ROW ? "SQLITE_ROW" : "SQLITE_ERROR");
 
    sqlite3_reset(stmt);  /* 如果要重新绑定其他值要reset一下 */
    sqlite3_bind_int(stmt, 1, 201601008);
    sqlite3_bind_text(stmt, 2, "xiaowu", -1, NULL); /* 重新绑定值 */
    sqlite3_bind_text(stmt, 3, "yes", 3, NULL);
    sqlite3_step(stmt);  /* 再执行 */
   
   /* 销毁prepare 创建的语句对象 */
   sqlite3_finalize(stmt);  
 
   /* 取数据 */
   //sql = "select * from healthinfo;";
   sql = "select * from healthinfo limit 4 offset 2;";  /* 限制返回4行且从第3行开始 */
   sqlite3_prepare_v2(db, sql, strlen(sql), &stmt, NULL);
   printf("total_column = %d\n", sqlite3_column_count(stmt));
   
   /* 遍历执行sql语句后的结果集的每一行数据 */
   while(sqlite3_step(stmt) == SQLITE_ROW){
       /* 获得字节数，第二个参数为select结果集合的列号 */
       /* 由于select 的结果集只有section这一列，因此为0 */
       int len_sid = sqlite3_column_bytes(stmt, 0);
       int len_name = sqlite3_column_bytes(stmt, 1);
       int len_ishealth = sqlite3_column_bytes(stmt, 2);
       
       printf("sid = %d, len = %d\n", sqlite3_column_int(stmt, 0), len_sid);
       printf("name = %s, len = %d\n", sqlite3_column_text(stmt, 1), len_name);
       printf("ishealth = %s, len = %d\n", sqlite3_column_text(stmt, 2), len_ishealth);
       //unsigned char* srcdata = sqlite3_column_blob(stmt, 0);  /* 取得数据库中的blob数据 */
   }
   printf("\n");
   sqlite3_finalize(stmt);
   /******************* end ****************************/
   
 
   const char* data = "select call back function call!\n";
   /* select 使用*/
   sql = "select * from healthinfo where ishealth == 'yes';";
   rc = sqlite3_exec(db, sql, select_callback, data, &zErrMsg);
   if( rc != SQLITE_OK ){
      fprintf(stderr, "SQL error: %s\n", zErrMsg);
      sqlite3_free(zErrMsg);
   }else{
      fprintf(stdout, "Table select successfully\n");
   }
 
   data = "update call back function call!\n";
   /* update 使用*/
   sql = "update healthinfo set ishealth = 'no' where name='xiaoli';" \
            "select * from healthinfo where ishealth == 'yes';";
   rc = sqlite3_exec(db, sql, select_callback, data, &zErrMsg);
   if( rc != SQLITE_OK ){
      fprintf(stderr, "SQL error: %s\n", zErrMsg);
      sqlite3_free(zErrMsg);
   }else{
      fprintf(stdout, "Table update successfully\n");
   }
   
   
   /* 删除表 */
   sql = "drop table healthinfo;";
   rc = sqlite3_exec(db, sql, NULL, NULL, &zErrMsg);
   if( rc != SQLITE_OK ){
      fprintf(stderr, "SQL error: %s\n", zErrMsg);
      sqlite3_free(zErrMsg);
   }else{
      fprintf(stdout, "Table droped successfully\n");
   }
 
 
   char sql5[256];
   char* tname = "abc";
   sprintf(sql5, "create table if not exists %s ("\
                    "id int not null," \
                    "name text not null);", tname);
 
   printf("%s\n", sql5);
 
   /* 创建表 */
   rc = sqlite3_exec(db, sql5, NULL, NULL, &zErrMsg);
   if( rc != SQLITE_OK ){
      fprintf(stderr, "SQL error: %s\n", zErrMsg);
      sqlite3_free(zErrMsg);
   }else{
      fprintf(stdout, "Table created successfully\n");
   }
   
   sqlite3_close(db);
}
```

编译：

```
gcc test.c -l sqlite3
```

运行：

```
hlxiong@hlxiong-VirtualBox:~/work/test/c-test$ ./a.out 
Opened database successfully
Table created successfully
Table insert data successfully
Table insert data successfully
max_parameter_count = 3
sid parameter index = 1
name parameter index = 2
ishealth parameter index = 3
index = 1 's parameter's name = :sid
step() return SQLITE_DONE
total_column = 3
sid = 201601003, len = 9
name = xiaozhang, len = 9
ishealth = no, len = 2
sid = 201601004, len = 9
name = xiaozhou, len = 8
ishealth = yes, len = 3
sid = 201601005, len = 9
name = xiaosun, len = 7
ishealth = yes, len = 3
sid = 201601006, len = 9
name = xiaoyang, len = 8
ishealth = yes, len = 3

select call back function call!
sid = 201601001
name = xiaowang
ishealth = yes

select call back function call!
sid = 201601002
name = xiaoli
ishealth = yes

select call back function call!
sid = 201601004
name = xiaozhou
ishealth = yes

select call back function call!
sid = 201601005
name = xiaosun
ishealth = yes

select call back function call!
sid = 201601006
name = xiaoyang
ishealth = yes

select call back function call!
sid = 201601007
name = xiaoqian
ishealth = yes

select call back function call!
sid = 201601008
name = xiaowu
ishealth = yes

Table select successfully
update call back function call!
sid = 201601001
name = xiaowang
ishealth = yes

update call back function call!
sid = 201601004
name = xiaozhou
ishealth = yes

update call back function call!
sid = 201601005
name = xiaosun
ishealth = yes

update call back function call!
sid = 201601006
name = xiaoyang
ishealth = yes

update call back function call!
sid = 201601007
name = xiaoqian
ishealth = yes

update call back function call!
sid = 201601008
name = xiaowu
ishealth = yes

Table update successfully
Table droped successfully
create table if not exists abc (id int not null,name text not null);
Table created successfully
```



参考资料

1、sqlite3数据库c语言常用接口应用实例

https://blog.csdn.net/u010312436/article/details/51558964

2、C-language Interface Specification for SQLite

https://www.sqlite.org/capi3ref.html