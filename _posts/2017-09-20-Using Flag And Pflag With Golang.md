---
layout:     post
title:      "Golang之使用Flag和Pflag"
subtitle:   "Using Flag And Pflag With Golang"
date:       Wed, Sep 20 2017 23:35:12 GMT+8
author:     "ChenJian"
header-img: "img/in-post/Using-Flag-And-Pflag-With-Golang/head_blog.jpg"
catalog:    true
tags: [工作, Golang]
---

### Flag

##### 导入flag

`import "flag"`

- 定义flags

``` go
import "flag"

// 返回的是 指针
var ip = flag.Int("flagname", 1234, "help message for flagname")
```

- 将flag绑定到一个变量

``` go
import "flag"

var flagvar int

func init() {
	flag.IntVar(&flagvar, "flagname", 1234, "help message for flagname")
}
```

- 绑定自定义的类型

``` go
import "flag"

// 自定义类型需要实现value接口
flag.Var(&flagVal, "name", "help message for flagname")
```

### flag解析

``` go
// 解析函数将会在碰到第一个非flag命令行参数时停止
flag.Parse()
```

##### 命令行参数的格式

``` sh
-flag xxx （使用空格，一个 - 符号） 
–flag xxx （使用空格，两个 - 符号） 
-flag=xxx （使用等号，一个 - 符号） 
–flag=xxx （使用等号，两个 - 符号）
```

### 使用flag的实例

##### example_flag.go

代码下载： [example\_flag.go](/download/Using-Cobra-With-Golang/example_flag.go)

``` go
package main

import (
	"flag"
	"fmt"
)

var inputName = flag.String("name", "CHENJIAN", "Input Your Name.")
var inputAge = flag.Int("age", 27, "Input Your Age")
var inputGender = flag.String("gender", "female", "Input Your Gender")
var inputFlagvar int

func Init() {
	flag.IntVar(&inputFlagvar, "flagname", 1234, "Help")
}
func main() {
	Init()
	flag.Parse()
	// func Args() []string
	// Args returns the non-flag command-line arguments.
	// func NArg() int
	// NArg is the number of arguments remaining after flags have been processed.
	fmt.Printf("args=%s, num=%d\n", flag.Args(), flag.NArg())
	for i := 0; i != flag.NArg(); i++ {
		fmt.Printf("arg[%d]=%s\n", i, flag.Arg(i))
	}
	fmt.Println("name=", *inputName)
	fmt.Println("age=", *inputAge)
	fmt.Println("gender=", *inputGender)
	fmt.Println("flagname=", inputFlagvar)
}
```

操作:

``` sh
go build example_flag.go

./example_flag -h

<<'COMMENT'
Usage of ./exampleFlag:
  -age int
        Input Your Age (default 27)
  -flagname int
        Help (default 1234)
  -gender string
        Input Your Gender (default "female")
  -name string
        Input Your Name. (default "CHENJIAN")
COMMENT

 ./example_flag chenjian
 
 <<'COMMENT'
args=[chenjian], num=1
arg[0]=chenjian
name= CHENJIAN
age= 27
gender= female
flagname= 1234
COMMENT

./example_flag -name balbalba -age 1111 -flagname=12333 dfdf xccccc eette

 <<'COMMENT'
args=[dfdf xccccc eette], num=3
arg[0]=dfdf
arg[1]=xccccc
arg[2]=eette
name= balbalba
age= 1111
gender= female
flagname= 12333
COMMENT
```

##### 官方实例 offical_flag.go

代码下载： [offical\_flag.go](/download/Using-Cobra-With-Golang/offical_flag.go)

``` go
// 这个实例展示了关于flag包的更复杂的使用
package main

import (
	"errors"
	"flag"
	"fmt"
	"strings"
	"time"
)

// 实例1：一个单独的字符串flag，叫“species”，其默认值为“goher”
var species = flag.String("species", "gopher", "the species we are studying")

// 实例2： 两个flag分享一个变量，所以我们可以一起写
// 初始化顺序没有定义，所以可以同时使用两个默认值。这必须在初始化函数中定义。
var gopherType string

func init() {
	const (
		defaultGopher = "pocket"
		usage         = "the variety of gopher"
	)
	flag.StringVar(&gopherType, "gopher_type", defaultGopher, usage)
	flag.StringVar(&gopherType, "g", defaultGopher, usage+" (shorthand)")
}

// 实例3：用户定义flag类型，一个时间段的切片
type interval []time.Duration

// String是一个用来格式化flag值(flag.Value接口的一部分)的方法
// String方法的输出将被用于调试
func (i *interval) String() string {
	return fmt.Sprint(*i)
}

// Set是一个用来设置flag值(flag.Value接口的一部分)的方法
// Set的参数是String类型，用于设置为flag
// 这是一个以逗号为分隔符的数组，我们需要分离它
func (i *interval) Set(value string) error {
	// 如果flag能被设置为多时间，加速度值，如果有如此声明，我们将会删除这些
	// 这些将会允许很多组合，例如"-deltaT 10s -deltaT 15s"
	if len(*i) > 0 {
		return errors.New("interval flag already set")
	}
	for _, dt := range strings.Split(value, ",") {
		duration, err := time.ParseDuration(dt)
		if err != nil {
			return err
		}
		*i = append(*i, duration)
	}
	return nil
}

// 将一个flag定义为堆积期间。因为它还有个特殊类型，我们需要使用Var函数，从而在初始化中创建flag
var intervalFlag interval

func init() {
	// 将命令行flag与intervalFlag绑定，并设置使用信息
	flag.Var(&intervalFlag, "deltaT", "comma-separated list of intervals to use between events")
}

func main() {
	// 所有有趣的信息都在上面了，但是如果想要使用flag包
	// 最好的方法就是去执行，特别是在main函数（而不是init函数）前执行 flag.Parse()
	// 我们这里并不运行，因为它不是个main函数，而且测试单元会详细设计flag内容
}
```

### Pflag

github地址：[spf13/pflag](https://github.com/spf13/pflag)

Docker源码中使用了Pflag。

##### 安装spf13/pflag

``` sh
go get github.com/spf13/pflag
```

##### 使用spf13/pflag

基本的使用和“flag包”基本相同

新增:

- 添加shorthand参数

``` go
// func IntP(name, shorthand string, value int, usage string) *int
// IntP is like Int, but accepts a shorthand letter that can be used after a single dash.
var ip= flag.IntP("flagname", "f", 1234, "help message")
```

- 设置非必须选项的默认值

``` go
var ip = flag.IntP("flagname", "f", 1234, "help message")
flag.Lookup("flagname").NoOptDefVal = "4321"
```

结果如下图:

| Parsed Arguments | Resulting Value |
| :-------------:    | :-------------:   |
| --flagname=1357  | ip=1357         |
| --flagname       | ip=4321         |
| [nothing]        | ip=1234         |

- 命令行语法

``` sh
--flag    // 布尔flags, 或者非必须选项默认值
--flag x  // 只对于没有默认值的flags
--flag=x
```

- flag定制化

例如希望使用“-”，“_”或者“.”，像`--my-flag == --my_flag == --my.flag`:

``` go
func wordSepNormalizeFunc(f *pflag.FlagSet, name string) pflag.NormalizedName {
	from := []string{"-", "_"}
	to := "."
	for _, sep := range from {
		name = strings.Replace(name, sep, to, -1)
	}
	return pflag.NormalizedName(name)
}

myFlagSet.SetNormalizeFunc(wordSepNormalizeFunc)
```

例如希望联合两个参数,像`--old-flag-name == --new-flag-name`:

``` go
func aliasNormalizeFunc(f *pflag.FlagSet, name string) pflag.NormalizedName {
	switch name {
	case "old-flag-name":
		name = "new-flag-name"
		break
	}
	return pflag.NormalizedName(name)
}

myFlagSet.SetNormalizeFunc(aliasNormalizeFunc)
```

- 弃用flag或者它的shothand

例如希望弃用名叫`badflag`参数，并告知开发者使用代替参数:

``` go
// deprecate a flag by specifying its name and a usage message
flags.MarkDeprecated("badflag", "please use --good-flag instead")
```

从而当使用`badflag`时，会提示`Flag --badflag has been deprecated, please use --good-flag instead`

例如希望保持使用`noshorthandflag`，但想弃用简称`n`:

``` go
// deprecate a flag shorthand by specifying its flag name and a usage message
flags.MarkShorthandDeprecated("noshorthandflag", "please use --noshorthandflag only")
```

从而当使用`n`时，会提示`Flag shorthand -n has been deprecated, please use --noshorthandflag only`

- 隐藏flag

例如希望保持使用`secretFlag`参数，但在help文档中隐藏这个参数的说明：

``` go
// hide a flag by specifying its name
flags.MarkHidden("secretFlag")
```

- 关闭flags的排序

例如希望关闭对help文档或使用说明的flag排序：

``` go
flags.BoolP("verbose", "v", false, "verbose output")
flags.String("coolflag", "yeaah", "it's really cool flag")
flags.Int("usefulflag", 777, "sometimes it's very useful")
flags.SortFlags = false
flags.PrintDefaults()
```

输出：

``` sh
-v, --verbose           verbose output
    --coolflag string   it's really cool flag (default "yeaah")
    --usefulflag int    sometimes it's very useful (default 777)
```

- 同时使用flag包和pflag包

``` go
import (
	goflag "flag"
	flag "github.com/spf13/pflag"
)

var ip *int = flag.Int("flagname", 1234, "help message for flagname")

func main() {
	flag.CommandLine.AddGoFlagSet(goflag.CommandLine)
	flag.Parse()
}
```

### 参考文献

1. [Go语言学习之flag包The way to go](http://blog.csdn.net/wangshubo1989/article/details/72914384?locationNum=14&fps=1)
2. [package flag](https://godoc.org/flag#pkg-index)
3. [package pflag](https://godoc.org/github.com/spf13/pflag)

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>本作品由<a xmlns:cc="http://creativecommons.org/ns#" href="https://o-my-chenjian.com/2017/09/20/Using-Flag-And-Pflag-With-Golang/" property="cc:attributionName" rel="cc:attributionURL">陈健</a>采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。


