# JudgeServer API

所有的请求，请在HTTP头中放入`X-Judge-Server-Token`字段，值为token的sha256结果。

所有的响应都是两个字段，`err`和`data`，正常情况下`err`为`null`，`data`为响应的数据。出现错误的情况下，`err`是错误代码，`data`为错误详情。下面所有的响应都是`data`的内容。

# 获取系统状态

-  URL `/ping`
-  Method `POST`

## 参数

 - 无参数

## 响应

```js
{
    "judger_version": "2.0.1",
    "hostname": "d3765528134e",
    // cpu核数，这个数字也确定了可以并发运行的判题任务数量
    "cpu_core": 1,
    // cpu和内存使用率，百分比
    "cpu": 4.1,
    "memory": 24.5
}
```

# 判题（非Special Judge)

 - URL `/judge`
 - Method `POST`

## 参数
 
  - src，源码
  - language_config，参考`languages.py`中，一般不需要修改
  - submission_id，这个提交唯一的id，请不要出现重复，比如使用时间戳也是不推荐的
  - max_cpu_time，单位毫秒
  - max_memory，最大内存，单位字节
  - test_case_id，用于找到存放有测试用例的文件夹

## 响应
  
```js
[
    // 每组都是一个测试用例，通过test_case字段区分
    {
        // cpu时间，毫秒
        "cpu_time": 1,
        // 见本文档最后部分
        "result": 0,
        // 内存，字节
        "memory": 12836864,
        // 实际时间，毫秒
        "real_time": 2,
        "signal": 0,
        "error": 0,
        "exit_code": 0,
        "output_md5": "eccbc87e4b5ce2fe28308fd9f2a7baf3",
        // 测试用例id
        "test_case": 1
    },
    {
        "cpu_time": 1,
        "result": 0,
        "memory": 12849152,
        "real_time": 1,
        "signal": 0,
        "error": 0,
        "exit_code": 0,
        "output_md5": "eccbc87e4b5ce2fe28308fd9f2a7baf3",
        "test_case": 2
    }
]
```

在编译错误的时候，返回

```js
{
	"err": "CompileError", 
	"data": "编译器的错误输出"
}
```

# 编译Special Judge

- URL `/compile_spj`
- Method `POST`

## 参数
 
  - src，源码
  - spj_version，Special Judge的版本，用于决定是否要重新编译二进制
  - spj_compile_config，参考`languages.py`，一般不需要修改
  - test_case_id

## 响应
  
```js
"success"
```

在编译错误的时候，返回

```js
{
	"err": "SPJCompileError", 
	"data": "编译器的错误输出"
}
```

# 判题（Special Judge)

注意，必须提前编译Special Judge，见上一个API

 - URL `/judge`
 - Method `POST`

## 参数
 
  - src
  - language_config
  - submission_id
  - max_cpu_time
  - max_memory
  - test_case_id
  - spj_version
  - spj_config，参考`languages.py`，一般不需要修改

## 响应
  
```js
[
    // 每组都是一个测试用例，通过test_case字段区分
    {
        // cpu时间，毫秒
        "cpu_time": 1,
        // 见本文档最后部分
        "result": 0,
        // 内存，字节
        "memory": 12836864,
        // 实际时间，毫秒
        "real_time": 2,
        "signal": 0,
        "error": 0,
        "exit_code": 0,
        "output_md5": null,
        // 测试用例id
        "test_case": 1
    },
    {
        "cpu_time": 1,
        "result": 0,
        "memory": 12849152,
        "real_time": 1,
        "signal": 0,
        "error": 0,
        "exit_code": 0,
        "output_md5": null,
        "test_case": 2
    }
]
```

在编译错误的时候，返回

```js
{
	"err": "CompileError", 
	"data": "编译器的错误输出"
}
```

# result 字段含义

 - WRONG_ANSWER = -1
 - AEECPTED = 0
 - CPU_TIME_LIMITED = 1
 - REAL_TIME_LIMIT_EXCEEDED = 2
 - MEMORY_LIMIT_EXCEEDED = 3
 - RUNTIME_ERROR = 4
 - SYSTEM_ERROR = 5


 



