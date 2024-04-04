# Judger for OnlineJudge 

## build

```
sudo apt-get install libseccomp-dev
mkdir build && cd build && cmake .. && make && sudo make install
```

`libjudger.so` is built in both executable and library format.

## Command Line

`./libjudger.so --help` shows the usage

## C API

`#include <runner.h>` then call `run` function with `struct config` and `struct result` pointer.

## `struct config` members

 - `max_cpu_time` (ms):  max cpu time this process can cost, -1 for unlimited
 - `max_real_time` (ms):  max time this process can run, -1 for unlimited
 - `max_memory` (byte):  max size of the process' virtual memory (address space), -1 for unlimited
 - `max_stack` (byte):  max size of the process' stack size
 - `max_process_number`:  max number of processes that can be created for the real user id of the calling process, -1 for unlimited
 - `max_output_size` (byte):  max size of data this process can output to stdout, stderr and file, -1 for unlimited
 - `memory_limit_check_only`: if this value equals `0`, we will only check memory usage number, because setrlimit(maxrss) will cause some crash issues
 - `exe_path`:  path of file to run
 - `input_file`:  redirect content of this file to process's stdin
 - `output_file`:  redirect process's stdout to this file
 - `error_file`:  redirect process's stderr to this file
 - `args` (string array terminated by NULL):  arguments to run this process
 - `env` (string array terminated by NULL):  environment variables this process can get
 - `log_path`:  judger log path
 - `seccomp_rule_name`(string or NULL): seccomp rules used to limit process system calls. Name is used to call corresponding functions.
 - `uid`:  user to run this process
 - `gid`:  user group this process belongs to
 
## `struct result` members

 - `cpu_time`:  cpu time the process has used
 - `real_time`:  actual running time of the process
 - `memory`:  max vaule of memory used by the process
 - `signal`:  signal number
 - `exit_code`:  process's exit code
 - `result`:  judger result, details in `runner.h`
 - `error`:  args validation error or judger internal error, error code in `runner.h`

### `result` return value
  - WRONG_ANSWER (judger module will never return this value, it's used for awswer checker)
  - SUCCESS = 0 (this only means the process exited normally)
  - CPU_TIME_LIMIT_EXCEEDED = 1 
  - REAL_TIME_LIMIT_EXCEEDED = 2
  - MEMORY_LIMIT_EXCEEDED = 3
  - RUNTIME_ERROR = 4
  - SYSTEM_ERROR = 5

### `error` return value
  - SUCCESS = 0
  - INVALID_CONFIG = -1
  - FORK_FAILED = -2
  - PTHREAD_FAILED = -3
  - WAIT_FAILED = -4
  - ROOT_REQUIRED = -5
  - LOAD_SECCOMP_FAILED = -6
  - SETRLIMIT_FAILED = -7
  - DUP2_FAILED = -8
  - SETUID_FAILED = -9
  - EXECVE_FAILED = -10
  - SPJ_ERROR = -11 (judger module will never return this value, it's used for awswer checker)
 
## Python binding (Python 2.7 and 3.5+)

```
sudo python setup.py install
```

### Python demo


Args with string must be Python `str` type

```
>>> import _judger
>>> _judger.VERSION

[2, 0, 1]

>>> _judger.run(max_cpu_time=1000,
...             max_real_time=2000,
...             max_memory=128 * 1024 * 1024,
...             max_process_number=200,
...             max_output_size=10000,
...             max_stack=32 * 1024 * 1024,
...             # five args above can be _judger.UNLIMITED
...             exe_path="/bin/echo",
...             input_path="/dev/null",
...             output_path="echo.out",
...             error_path="echo.out",
...             # can be empty list
...             args=["HelloWorld"],
...             # can be empty list
...             env=["foo=bar"],
...             log_path="judger.log",
...             # can be None
...             seccomp_rule_name="c_cpp",
...             uid=0,
...             gid=0)

{'cpu_time': 0, 'signal': 0, 'memory': 4554752, 'exit_code': 0, 'result': 0, 'error': 0, 'real_time': 2}
```

There are six constants in the module you can use

 - RESULT_SUCCESS
 - RESULT_CPU_TIME_LIMIT_EXCEEDED
 - RESULT_REAL_TIME_LIMIT_EXCEEDED
 - RESULT_MEMORY_LIMIT_EXCEEDED
 - RESULT_RUNTIME_ERROR
 - RESULT_SYSTEM_ERROR


## Run tests

```
cd tests &&  sudo python test.py
```

## Note

 - Linux x64 and kernel version > 3.17 required
 - Judger security relies on Docker with default security config [More](https://github.com/QingdaoU/JudgeServer/blob/master/docker-compose.example.yml)
 - Tested under Ubuntu docker container. System calls may vary due to different system and kernel versions
 - Root user required to change uid / gid
 - Why use seccomp instead of ptrace? Ptrace can decrease process's performance significantly, for each system call, twice 
 context switch between child process and parent process is needed.
 - How to custom seccomp rule? [Example here](https://github.com/QingdaoU/Judger/blob/newnew/src/rules/c_cpp.c).
 
## Known issues

 - Parent process' memory usage will affect child process' memory usage data [ref1](http://marklux.cn/blog/73) [ref2](https://github.com/QingdaoU/Judger/blob/newnew/bindings/Python/_judger/__init__.py)
 
## License

  The Star And Thank Author License (SATA)


