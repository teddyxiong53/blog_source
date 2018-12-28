---
title: nodejs之index.d.ts文件分析
date: 2018-12-28 10:06:25
tags:
	- nodejs

---



这个文件适合用来分析nodejs有哪些内容。

总共9000行左右。

```
declare var process: NodeJS.Process;
declare var global: NodeJS.Global;
declare var console: Console;

declare var __filename: string;
declare var __dirname: string;

declare var require: NodeRequire;
declare var exports: any;

type BufferEncoding = "ascii" | "utf8" | "utf16le" | "ucs2" | "base64" | "latin1" | "binary" | "hex";

declare namespace NodeJS {
	class EventEmitter
	interface ReadableStream extends EventEmitter 
	interface Process extends EventEmitter 
}

declare module "events" {
    class internal extends NodeJS.EventEmitter { }
}
```



可以看出各个module里，注册了哪些事件。

所有的模块，以及模块的长度。这里可以看出。

```
	Line 1078: declare module "buffer" {
	Line 1085: declare module "querystring" {
	Line 1103: declare module "events" {
	Line 1133: declare module "http" {
	Line 1381: declare module "cluster" {
	Line 1643: declare module "worker_threads" {
	Line 1768: declare module "zlib" {
	Line 1907: declare module "os" {
	Line 2100: declare module "https" {
	Line 2138: declare module "punycode" {
	Line 2151: declare module "repl" {
	Line 2524: declare module "readline" {
	Line 2660: declare module "vm" {
	Line 2725: declare module "child_process" {
	Line 3084: declare module "url" {
	Line 3189: declare module "dns" {
	Line 3482: declare module "net" {
	Line 3734: declare module "dgram" {
	Line 3832: declare module "fs" {
	Line 6105: declare module "path" {
	Line 6265: declare module "string_decoder" {
	Line 6275: declare module "tls" {
	Line 6647: declare module "crypto" {
	Line 7017: declare module "stream" {
	Line 7312: declare module "util" {
	Line 7486: declare module "assert" {
	Line 7539: declare module "tty" {
	Line 7555: declare module "domain" {
	Line 7572: declare module "constants" {
	Line 7852: declare module "module" {
	Line 7856: declare module "process" {
	Line 7860: declare module "v8" {
	Line 7889: declare module "timers" {
	Line 7906: declare module "console" {
	Line 7913: declare module "async_hooks" {
	Line 8055: declare module "http2" {
	Line 8917: declare module "perf_hooks" {
	Line 9159: declare module "trace_events" {
```

