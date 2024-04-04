### 什么是Special Judge

Special Judge是指OJ将使用一个特定的程序来判断提交的程序的输出是不是正确的，而不是单纯地看提交的程序的输出是否和标准输出一模一样。

### 使用场景

一般使用Special Judge都是因为题目的答案不唯一，更具体一点说的话一般是两种情况：

 - 题目最终要求输出一个解决方案，而且这个解决方案可能不唯一。

 - 题目最终要求输出一个浮点数，而且会告诉只要答案和标准答案相差不超过某个较小的数就可以，比如0.01。这种情况保留3位小数、4位小数等等都是可以的，而且多保留几位小数也没什么坏处。

### Special Judge判题程序示例

```c
#include <stdio.h>

#define AC 0
#define WA 1
#define ERROR -1

int spj(FILE *input, FILE *user_output);

void close_file(FILE *f){
    if(f != NULL){
        fclose(f);
    }
}

int main(int argc, char *args[]){
    FILE *input = NULL, *user_output = NULL;
    int result;
    if(argc != 3){
        printf("Usage: spj x.in x.out\n");
        return ERROR;
    }
    input = fopen(args[1], "r");
    user_output = fopen(args[2], "r");
    if(input == NULL || user_output == NULL){
        printf("Failed to open output file\n");
        close_file(input);
        close_file(user_output);
        return ERROR;
    }

    result = spj(input, user_output);
    printf("result: %d\n", result);
    
    close_file(input);
    close_file(user_output);
    return result;
}

int spj(FILE *input, FILE *user_output){
    /*
      parameter: 
        - input，标程输入的文件指针
        - user_output，用户输出文件的指针
      return: 
        - 如果用户答案正确，返回AC
        - 如果用户答案错误返回WA
        - 如果主动捕获到自己的错误，如内存分配失败，返回ERROR
      请用户完成此函数.
      demo:
      int a, b;
      while(fscanf(f, "%d %d", &a, &b) != EOF){
          if(a -b != 3){
              return WA;
          }
      }
      return AC;
     */
}
```

### 使用方法

在本地测试的时候，先编译，然后`./spj your_in_file_path user_output_path`。

在OJ上运行的时候，判题结果来自于`main`函数的返回值。要注意的时候OJ上判题程序也是在沙箱中运行的，时间限制为题目时间限制的3倍，内存限制为1G。
