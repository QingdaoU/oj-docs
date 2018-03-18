Jugder 是怎么工作的？

## 限制系统调用

目前常用的有 `ptrace` 和 `seccomp`。

### ptrace 很惨

听说 `ptrace` 存在效率问题，可能会让你的代码运行时间增加很多，这个是可以[简单测试](https://github.com/virusdefender/UndergraduateThesis)看出来的。

而加载 `seccomp` 需要主动的在自己的代码中加载策略，也就是说需要修改已有的代码，但是去修改用户提交的代码是不大可能的。然后就想到了下面几个方法：

### LD_PRELOAD hook

`LD_PRELOAD`加载动态链接库，然后在 so 中 hook `__libc_start_main`，然后就可以在用户的 `main` 函数前执行自己的代码了。但是如果在用户的代码中再定义`__lbc_start_main`函数就可以绕过，虽然网上有人说需要 `-nostdlib` 的编译参数，但是我实际测试并不需要。下面是沙箱的实现代码

```clike
#define _BSD_SOURCE // readlink
#include <dlfcn.h>
#include <stdlib.h> // exit
#include <string.h> // strstr, memset
#include <link.h>   // ElfW
#include <errno.h>  // EPERM
#include <unistd.h> // readlink
#include <seccomp.h>
#include <stdio.h>
int syscalls_whitelist[] = {SCMP_SYS(read), SCMP_SYS(write), 
                            SCMP_SYS(fstat), SCMP_SYS(mmap), 
                            SCMP_SYS(mprotect), SCMP_SYS(munmap), 
                            SCMP_SYS(brk), SCMP_SYS(access), 
                            SCMP_SYS(exit_group)};
typedef int (*main_t)(int, char **, char **);

#ifndef __unbounded
# define __unbounded
#endif

int __libc_start_main(main_t main, int argc, 
    char *__unbounded *__unbounded ubp_av,
    ElfW(auxv_t) *__unbounded auxvec,
    __typeof (main) init,
    void (*fini) (void),
    void (*rtld_fini) (void), void *__unbounded
    stack_end)
{

    int i;
    ssize_t len;
    void *libc;
    int whitelist_length = sizeof(syscalls_whitelist) / sizeof(int);
    scmp_filter_ctx ctx = NULL;
    int (*libc_start_main)(main_t main,
        int,
        char *__unbounded *__unbounded,
        ElfW(auxv_t) *,
        __typeof (main),
        void (*fini) (void),
        void (*rtld_fini) (void),
        void *__unbounded stack_end);

    // Get __libc_start_main entry point
    libc = dlopen("libc.so.6", RTLD_LOCAL  | RTLD_LAZY);
    if (!libc) {
        exit(1);
    }

    libc_start_main = dlsym(libc, "__libc_start_main");
    if (!libc_start_main) {
        exit(2);
    }
    
    ctx = seccomp_init(SCMP_ACT_KILL);
    if (!ctx) {
        exit(3);
    }
    for(i = 0; i < whitelist_length; i++) {
        if (seccomp_rule_add(ctx, SCMP_ACT_ALLOW, 
                             syscalls_whitelist[i], 0)) {
            exit(4);
        }
    }
    if (seccomp_load(ctx)) {
        exit(5);
    }
    seccomp_release(ctx);
    return ((*libc_start_main)(main, argc, ubp_av, auxvec,
                 init, fini, rtld_fini, stack_end));
}
```

参考  http://stackoverflow.com/a/27735456/2737403 和 https://github.com/daveho/EasySandbox

### 代码级别 hook

编译的时候将两个文件编译在一起，`gcc sandbox.c user_code.c -ldl -lseccomp -o user_code`，虽然说直接定义`__libc_start_main`函数会提示重复定义，但是部分库函数还是可以通过定义同名函数覆盖绕过，比如 `seccomp` 里面的函数、`dlopen`函数。

### execve 前面加载策略

`exceve` 之前加载策略，就需要将 `exceve` 系统调用加白名单，有点不安全，但是可以在 `seccomp` 参数中指定 `exceve` 的执行参数，第一个参数就是文件路径，必须得匹配才行，否则就会 kill 掉。可以将指定的文件名加白名单。

```clike
#include <stdio.h>
#include <unistd.h>
#include <seccomp.h>

int main() {
  char file_name[30] = "/bin/ls";
  char file_name1[30] = "xxxxxx";
  char *argv[] = {"/", NULL};
  char *env[] = {NULL};
  printf("unrestricted\n");

  // Init the filter
  scmp_filter_ctx ctx;
  ctx = seccomp_init(SCMP_ACT_ALLOW);

  seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(execve), 1,
                        SCMP_A0(SCMP_CMP_NE, file_name));

  seccomp_load(ctx);
  execve(file_name, argv, env);
  return 0;
}
```

如果改成`execve(file_name1, argv, env);`，就没法执行了。

## seccomp 应该怎么用

文档看 http://man7.org/linux/man-pages/man3/seccomp_rule_add.3.html 就够了，可以看到 seccomp 是支持某个参数的原始数据大小比较和掩码后数据一致比较的。

对于 C/C++ 等，我们可以开放[白名单](https://github.com/QingdaoU/Judger/blob/newnew/src/rules/c_cpp.c#L10)，类似 execve 这种需要特殊处理，然后就是 `open` 了，
我们不期望这些程序可以写任何文件。这种想法的直觉是限制 `write` 的第一个参数 fd 不能大于 stderr，但是实际是可绕过的，那就是 `mmap`。 http://man7.org/linux/man-pages/man2/mmap.2.html
最下面的例子修改下然后 strace 运行就会发现只需要 open 然后 mmap 也可以写文件的。

根本还是限制 `open`，不能带写权限。[open 的 man page](http://man7.org/linux/man-pages/man2/open.2.html) 中说

> The argument flags must include one of the following access modes: O_RDONLY, O_WRONLY, or O_RDWR

所以这里就需要之前的掩码后比较了，其实掩码操作就是使用掩码和原数据进行与操作，`SCMP_CMP(1, SCMP_CMP_MASKED_EQ, O_WRONLY | O_RDWR, 0)` 就是说这两位上都是0才可以通过。

对于非 C/C++，白名单不太现实，可能会涉及到各种奇奇怪怪的系统调用，所以可以尝试使用黑名单，毕竟在 docker 中如果做好了权限的话，基本上没什么问题的，当然这方面我没法保证，因为我也在探索。

## 资源占用的限制

### CPU 时间限制，是 setrlimit 还是 setitimer

主要是的区别是子进程能否继承限制，进程能否捕获超时错误。

当 `setitimer` 定时器计时结束时,系统就会给进程发送一个信号。
需要关心的两个计数器分别是 ITIMER_REAL,进程实际运行时间计数器,结束的时候发 送 SIGALRM 信号;ITIMER_VIRTUAL,进程 CPU 时间计数器,结束的时候发送 SIGVTALRM 信 号。我们设置好定时器之后,如果捕获到了对应的信号,说明当前进程运行超时。
具体实现代码如下

```clike
int set_timer(int sec, int ms, int is_cpu_time) {
    struct itimerval time_val;
    time_val.it_interval.tv_sec = time_val.it_interval.tv_usec = 0;
    time_val.it_value.tv_sec = sec;
    time_val.it_value.tv_usec = ms * 1000;
    if (setitimer(is_cpu_time?ITIMER_VIRTUAL:ITIMER_REAL, &time_val, NULL)) {
        LOG_FATAL("setitimer failed, errno %d", errno);
        return SETITIMER_FAILED;
    }
    return SUCCESS;
}
```

但是有一点是需要注意的，[setitimer 不能限制子进程的 CPU 和实际运行时间](http://man7.org/linux/man-pages/man2/setitimer.2.html)。
在部分只限制资源占用而不启用沙箱的场景下,这可能导致资源限制失效。

Linux 中 `setrlimit` 函数可以用来限制进程的资源占用, 其中支持 `RLIMIT_CPU`、`RLIMIT_AS` 等参数, 同时子进程会继承父进程的设置。RLIMIT_CPU 也可以控制进程 CPU 时间, 所以要设置为 CPU 时间向上取整的值，然后和最后获取的时间再比较。

### 限制内存和最大输出大小

`RLIMIT_AS` 是限制进程最大内存地址空间,超过这个地址空间的将不能 分配成功,影响 `brk`、`mmap`、`mremap` 等系统调用。
`RLIMIT_FSIZE` 是限制进程最大输出或者写文件的大小，估计是限制了 `write` 等。

### 实际运行时间

这个也很重要，如果一个进程啥都不做只 `sleep` 的话，CPU 时间几乎不会超，这里我的方案是新开一个线程一直监视某个 PID，超时就 kill 掉。

### RLIMIT_NPROC 有点坑

很多人都知道 `while(1) fork()` 可以卡死机器，怎么防？尤其是 go 这类这种天生就要开线程的语言。

> The maximum number of processes (or, more precisely on Linux, threads) that can be created for the real user ID of the calling process. Upon encountering this limit, fork(2) fails with the error EAGAIN

如果简单的使用 `nproc` 限制是不可以的，原因是 `real user ID` 这个其实不仅仅是进程的，和用户也有关。一个用户已经有10个进程了，那你给进程设置 `nproc=10` 是没用的，因为已经满了，而设置更低的数字可能导致进程无法启动。

也许给每个进程都设置一个单独的用户可破？没有试

## 资源占用的获取

### 内存是一个大坑

参考 http://marklux.cn/blog/73

另外一个方法就是写一个内核模块，然后将制定进程的 `maxrss` 重置为0，https://gist.github.com/virusdefender/f494feb00f039bf6b97b49acbd29f564 是一个 demo。

## 还有哪里容易出现问题

### 编译器安全

这是一个容易被忽视的方面,目前已知的主要有以下几种。

 - 引用某些可以无限输出的文件，比如 `#include</dev/random>`，编译器会一直读取, 导致卡死
 - 让编译器产生大量的错误信息，比如下面一段代码，可以让 g++ 编译器产生数 G 的错误日志
 
```clike
int main() {
    struct x struct z<x(x(x(x(x(x(x(x(x(x(x(x(x(x(x(y,x(y><y*,x(y*w>v<y*,w,x{}
    return 0; 
}
```
处理方法就是编译器运行的时候也要控制 CPU 时间和实际运行时间还有最大输出，同时使用编译器参数 `-fmax-errors=N` 来控制最大错误数量

 - C++ 的模板元编程，部分代码是编译期执行的，可以构造出让编译器产生大量计算的代码。类似的有 Python 的编译器常量优化等等。
 - 引用一些敏感文件可能导致信息泄露，比如 `#include</etc/shadow/>` 或者测试用例等，会在编译错误的信息中泄露文件开头的内容。需要给编译器和运行代码设置单独的用户。

### 上面说的基础环境其实都在 docker 里面

docker 默认会[屏蔽一些系统调用和 capability](https://docs.docker.com/engine/security/security/)，所以上面的很多方案都是基于这个前提的，否则需要自己处理 docker 默认屏蔽的系统调用调用黑名单和降权。

参考 

 - http://manpages.ubuntu.com/manpages/saucy/man3/seccomp_rule_add.3.html
 - https://filippo.io/linux-syscall-table/
 - https://www.zhihu.com/question/23067497
