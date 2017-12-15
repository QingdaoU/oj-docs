# JudgeServer API

## Preparement

 - `X-Judge-Server-Token` HTTP header is required for all requests, the value of this header is `sha256(token)`.
 - Type of request and response data is JSON.
 - Request method is `POST`.
 - For all responses, `err` and `data` fields will be returned. 

    - If the request is processed successfully, `err` field will be `null`, `data` field will be the data returned. 
    - If error occured while processing request, `err` field will be error code, `data` field will be the reason.

# Get system info

-  URL `/ping`

## Args

 - Do not need args

## Response

```js
{
    "judger_version": "2.0.1",
    "hostname": "d3765528134e",
    // number of cpu cores, this value will determine the number of concurrent tasks
    "cpu_core": 1,
    // usage of cpu and memory
    "cpu": 4.1,
    "memory": 24.5,
    "action": "pong"
}
```

# Judge (not for Special Judge)

 - URL `/judge`

## Args
 
  - `src`: source code
  - `language_config`: refer to `client/Python/languages.py`, do not need to modify generally
  - `max_cpu_time`: unit is ms
  - `max_memory`: unit is byte
  - `test_case_id`: used to get the test_case directory
  - `output`: if this value is `true`, then user's output is returned else `null` is returned. You can use this to debug your solution

## Response
  
```js
[
    // each object/dict is a test case file running result
    {
        "cpu_time": 1,
        // refer to the end of this document
        "result": 0,
        "memory": 12836864,
        "real_time": 2,
        "signal": 0,
        "error": 0,
        // refer to the end of this document
        "exit_code": 0,
        "output_md5": "eccbc87e4b5ce2fe28308fd9f2a7baf3",
        // test case file id
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

When compilation is failed, following data will be returned

```js
{
	"err": "CompileError", 
	"data": "error resson"
}
```

# Compile Special Judge

- URL `/compile_spj`

## Args
 
  - `src`: special judge soure code
  - `spj_version`: version of special judge, used to determine whether to recompile special judge
  - `spj_compile_config`: refer to `client/Python/languages.py`, do not need to modify generally

## Response
  
```js
"success"
```

When compilation is failed, following data will be returned

```js
{
	"err": "SPJCompileError", 
	"data": "error resson"
}
```

# Judge (for Special Judge)

 - URL `/judge`

## Args
 
  - `src`
  - `language_config`
  - `max_cpu_time`
  - `max_memory`
  - `spj_version`
  - `spj_config`, refer to `client/Python/languages.py`, do not need to modify generally
  - `spj_compile_config`: refer to `client/Python/languages.py`, do not need to modify generally
  - `spj_src`
  - `output`

## Response
  
```js
[
    {
        "cpu_time": 1,
        "result": 0,
        "memory": 12836864,
        "real_time": 2,
        "signal": 0,
        "error": 0,
        "exit_code": 0,
        "output_md5": null,
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

When compilation is failed, following data will be returned

```js
{
	"err": "CompileError", 
	"data": "error reason"
}
```

If SPJ process crashed, `result = SYSTEM_ERROR` and `ERROR = SPJ_ERROR` is returned.

# `result` field return value
  - WRONG_ANSWER = -1 (this means the process exited normally, but the answer is wrong)
  - SUCCESS = 0 (this means the answer is accepted)
  - CPU_TIME_LIMIT_EXCEEDED = 1 
  - REAL_TIME_LIMIT_EXCEEDED = 2
  - MEMORY_LIMIT_EXCEEDED = 3
  - RUNTIME_ERROR = 4
  - SYSTEM_ERROR = 5

# `error` field return value
  - SUCCESS = 0
  - INVALID_CONFIG = -1
  - CLONE_FAILED = -2
  - PTHREAD_FAILED = -3
  - WAIT_FAILED = -4
  - ROOT_REQUIRED = -5
  - LOAD_SECCOMP_FAILED = -6
  - SETRLIMIT_FAILED = -7
  - DUP2_FAILED = -8
  - SETUID_FAILED = -9
  - EXECVE_FAILED = -10
  - SPJ_ERROR = -11

 



