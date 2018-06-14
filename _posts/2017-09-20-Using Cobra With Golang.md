---
layout:     post
title:      "Golang之使用Cobra"
subtitle:   "Using Cobra With Golang"
date:       Wed, Sep 20 2017 23:19:10 GMT+8
author:     "ChenJian"
header-img: "img/in-post/Using-Cobra-With-Golang/head_blog.jpg"
catalog:    true
tags: [工作, Golang]
---


### Cobra介绍

Cobra是一个库，其提供简单的接口来创建强大现代的CLI接口，类似于git或者go工具。同时，它也是一个应用，用来生成个人应用框架，从而开发以Cobra为基础的应用。Docker源码中使用了Cobra。

##### 概念

Cobra基于三个基本概念`commands`,`arguments`和`flags`。其中commands代表行为，arguments代表数值，flags代表对行为的改变。

基本模型如下：

`APPNAME VERB NOUN --ADJECTIVE`或者`APPNAME COMMAND ARG --FLAG`

例如：

``` sh
# server是commands，port是flag
hugo server --port=1313

# clone是commands，URL是arguments，brae是flags
git clone URL --bare
```

- Commands

Commands是应用的中心点，同样commands可以有子命令(children commands)，其分别包含不同的行为。

Commands的结构体如下：

``` go
type Command struct {
    Use string // The one-line usage message.
    Short string // The short description shown in the 'help' output.
    Long string // The long message shown in the 'help <this-command>' output.
    Run func(cmd *Command, args []string) // Run runs the command.
}
```

- Flags

Flags用来改变commands的行为。其完全支持POSIX命令行模式和Go的flag包。这里的flag使用的是[spf13/pflag](https://github.com/spf13/pflag)包，具体可以参考[Golang之使用Flag和Pflag](https://o-my-chenjian.com/2017/09/20/Using-Flag-And-Pflag-With-Golang/).

##### 安装与导入

- 安装

``` sh
go get -u github.com/spf13/cobra/cobra
```

- 导入

``` go
import "github.com/spf13/cobra"
```

### Cobra文件结构

##### cjapp的基本结构

``` sh
  ▾ cjapp/
    ▾ cmd/
        add.go
        your.go
        commands.go
        here.go
      main.go
```

##### main.go

其目的很简单，就是初始化Cobra。其内容基本如下：

``` go
package main

import (
  "fmt"
  "os"

  "{pathToYourApp}/cmd"
)

func main() {
  if err := cmd.RootCmd.Execute(); err != nil {
    fmt.Println(err)
    os.Exit(1)
  }
}
```

### 使用cobra生成器

windows系统下使用：

``` sh
go get github.com/spf13/cobra/cobra
```

或者在文件夹`github.com/spf13/cobra/cobra`下使用`go install`在`$GOPATH/bin`路径下生成`cobra.exe`可执行命令。

##### cobra init

命令`cobra init [yourApp]`将会创建初始化应用，同时提供正确的文件结构。同时，其非常智能，你只需给它一个绝对路径，或者一个简单的路径。

``` sh
cobra.exe init cjapp

<<'COMMENT'
Your Cobra application is ready at
/home/chenjian/gofile/src/cjapp.

Give it a try by going there and running `go run main.go`.
Add commands to it by running `cobra add [cmdname]`.
COMMENT
ls -Ra /home/chenjian/gofile/src/cjapp

<<'COMMENT'
/home/chenjian/gofile/src/cjapp:
.  ..  cmd  LICENSE  main.go

/home/chenjian/gofile/src/cjapp/cmd:
.  ..  root.go
COMMENT
```

##### cobra add

在路径`C:\Users\chenjian\GoglandProjects\src\cjapp`下分别执行:

``` sh
cobra add serve
<<'COMMENT'
serve created at /home/chenjian/gofile/src/cjapp/cmd/serve.go
COMMENT

cobra add config
<<'COMMENT'
config created at /home/chenjian/gofile/src/cjapp/cmd/config.go
COMMENT

cobra add create -p 'configCmd'
<<'COMMENT'
create created at /home/chenjian/gofile/src/cjapp/cmd/create.go
COMMENT

ls -Ra /home/chenjian/gofile/src/cjapp

<<'COMMENT'
/home/chenjian/gofile/src/cjapp:
.  ..  cmd  LICENSE  main.go

/home/chenjian/gofile/src/cjapp/cmd:
.  ..  config.go  create.go  root.go  serve.go
COMMENT
```

此时你可以使用:

``` sh
go run main.go

<<'COMMENT'
A longer description that spans multiple lines and likely contains
examples and usage of using your application. For example:

Cobra is a CLI library for Go that empowers applications.
This application is a tool to generate the needed files
to quickly create a Cobra application.

Usage:
  cjapp [command]

Available Commands:
  config      A brief description of your command
  help        Help about any command
  serve       A brief description of your command

Flags:
      --config string   config file (default is $HOME/.cjapp.yaml)
  -h, --help            help for cjapp
  -t, --toggle          Help message for toggle

Use "cjapp [command] --help" for more information about a command.
COMMENT

go run main.go config
<<'COMMENT'
config called
COMMENT

go run main.go serve
<<'COMMENT'
serve called
COMMENT

go run main.go config create
<<'COMMENT'
create called
COMMENT
```

##### cobra生成器配置

Cobra生成器通过`~/.cjapp.yaml`(Linux下)或者`$HOME/.cjapp.yaml`(windows)来生成LICENSE。

一个`.cjapp.yaml`格式例子如下：

``` yaml
author: Chen Jian <chenjian158978@gmail.com>
license: MIT
```

或者可以自定义LICENSE:

``` yaml
{% raw %}license:
  header: This file is part of {{ .appName }}.
  text: |
    {{ .copyright }}

    This is my license. There are many like it, but this one is mine.
    My license is my best friend. It is my life. I must master it as I must
    master my life.{% endraw %}
```

### 人工构建Cobra应用

人工构建需要自己创建`main.go`文件和`RootCmd`文件。例如创建一个Cobra应用`cjappmanu`

##### RootCmd文件

路径为`cjappmanu/cmd/root.go`

代码下载： [cjappmanu\_cmd\_root.go](/download/Using-Cobra-With-Golang/cjappmanu_cmd_root.go)

``` go
package cmd

import (
	"fmt"
	"os"

	"github.com/mitchellh/go-homedir"
	"github.com/spf13/cobra"
	"github.com/spf13/viper"
)

var RootCmd = &cobra.Command{
	Use:     "chenjian",
	Aliases: []string{"cj", "ccccjjjj"},
	Short:   "call me jack",
	Long: `A Fast and Flexible Static Site Generator built with
                love by spf13 and friends in Go.
                Complete documentation is available at https://o-my-chenjian.com`,
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Printf("OK")
	},
}

var cfgFile, projectBase, userLicense string

func init() {
	cobra.OnInitialize(initConfig)

	// 在此可以定义自己的flag或者config设置，Cobra支持持久标签(persistent flag)，它对于整个应用为全局
	// 在StringVarP中需要填写`shorthand`，详细见pflag文档
	RootCmd.PersistentFlags().StringVar(&cfgFile, "config", "", "config file (defalut in $HOME/.cobra.yaml)")
	RootCmd.PersistentFlags().StringVarP(&projectBase, "projectbase", "b", "", "base project directory eg. github.com/spf13/")
	RootCmd.PersistentFlags().StringP("author", "a", "YOUR NAME", "Author name for copyright attribution")
	RootCmd.PersistentFlags().StringVarP(&userLicense, "license", "l", "", "Name of license for the project (can provide `licensetext` in config)")
	RootCmd.PersistentFlags().Bool("viper", true, "Use Viper for configuration")

	// Cobra同样支持局部标签(local flag)，并只在直接调用它时运行
	RootCmd.Flags().BoolP("toggle", "t", false, "Help message for toggle")

	// 使用viper可以绑定flag
	viper.BindPFlag("author", RootCmd.PersistentFlags().Lookup("author"))
	viper.BindPFlag("projectbase", RootCmd.PersistentFlags().Lookup("projectbase"))
	viper.BindPFlag("useViper", RootCmd.PersistentFlags().Lookup("viper"))
	viper.SetDefault("author", "NAME HERE <EMAIL ADDRESS>")
	viper.SetDefault("license", "apache")
}

func Execute()  {
	RootCmd.Execute()
}

func initConfig() {
	// 勿忘读取config文件，无论是从cfgFile还是从home文件
	if cfgFile != "" {
		viper.SetConfigName(cfgFile)
	} else {
		// 找到home文件
		home, err := homedir.Dir()
		if err != nil {
			fmt.Println(err)
			os.Exit(1)
		}

		// 在home文件夹中搜索以“.cobra”为名称的config
		viper.AddConfigPath(home)
		viper.SetConfigName(".cobra")
	}
	// 读取符合的环境变量
	viper.AutomaticEnv()

	if err := viper.ReadInConfig(); err != nil {
		fmt.Println("Can not read config:", viper.ConfigFileUsed())
	}
}

```

##### main.go

`main.go`的目的就是初始化Cobra

代码下载： [cjappmanu\_cmd\_main.go](/download/Using-Cobra-With-Golang/cjappmanu_cmd_main.go)

``` go
package main

import (
	"fmt"
	"os"

	"cjappmanu/cmd"
)

func main() {
	if err := cmd.RootCmd.Execute(); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
}

```

##### 附加命令

附加命令可以在`/cmd/`文件夹中写，例如一个版本信息文件，可以创建`/cmd/version.go`

代码下载： [version.go](/download/Using-Cobra-With-Golang/version.go)

``` go
package cmd

import (
	"fmt"

	"github.com/spf13/cobra"
)

func init() {
	RootCmd.AddCommand(versionCmd)
}

var versionCmd = &cobra.Command{
	Use:   "version",
	Short: "Print the version number of ChenJian",
	Long:  `All software has versions. This is Hugo's`,
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("Chen Jian Version: v1.0 -- HEAD")
	},
}

```

同时，可以将命令添加到父项中，这个例子中`RootCmd`便是父项。只需要添加：

``` go
RootCmd.AddCommand(versionCmd)
```

### 处理Flags

##### Persistent Flags

`persistent`意思是说这个flag能任何命令下均可使用，适合全局flag：

``` go
RootCmd.PersistentFlags().BoolVarP(&Verbose, "verbose", "v", false, "verbose output")
```

##### Local Flags

Cobra同样支持局部标签(local flag)，并只在直接调用它时运行

``` go
RootCmd.Flags().StringVarP(&Source, "source", "s", "", "Source directory to read from")
```

##### Bind flag with Config

使用`viper`可以绑定flag

``` go
var author string

func init() {
  RootCmd.PersistentFlags().StringVar(&author, "author", "YOUR NAME", "Author name for copyright attribution")
  viper.BindPFlag("author", RootCmd.PersistentFlags().Lookup("author"))
}
```

### Positional and Custom Arguments

##### Positional Arguments

Leagacy arg validation有以下几类：

- `NoArgs`: 如果包含任何位置参数，命令报错
- `ArbitraryArgs`: 命令接受任何参数
- `OnlyValidArgs`: 如果有位置参数不在`ValidArgs`中，命令报错
- `MinimumArgs(init)`: 如果参数数目少于N个后，命令行报错
- `MaximumArgs(init)`: 如果参数数目多余N个后，命令行报错
- `ExactArgs(init)`: 如果参数数目不是N个话，命令行报错
- `RangeArgs(min, max)`: 如果参数数目不在范围(min, max)中，命令行报错

##### Custom Arguments

``` go
var cmd = &cobra.Command{
  Short: "hello",
  Args: func(cmd *cobra.Command, args []string) error {
    if len(args) < 1 {
      return errors.New("requires at least one arg")
    }
    if myapp.IsValidColor(args[0]) {
      return nil
    }
    return fmt.Errorf("invalid color specified: %s", args[0])
  },
  Run: func(cmd *cobra.Command, args []string) {
    fmt.Println("Hello, World!")
  },
}
```

### 实例

将`root.go`修改为以下：

代码下载： [example\_root.go](/download/Using-Cobra-With-Golang/example_root.go)

``` go
package cmd

import (
	"fmt"
	"os"
	"strings"

	homedir "github.com/mitchellh/go-homedir"
	"github.com/spf13/cobra"
	"github.com/spf13/viper"
)

var cfgFile string
var echoTimes int

var RootCmd = &cobra.Command{
	Use: "app",
}

var cmdPrint = &cobra.Command{
	Use:   "print [string to print]",
	Short: "Print anything to the screen",
	Long: `print is for printing anything back to the screen.
For many years people have printed back to the screen.`,
	Args: cobra.MinimumNArgs(1),
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("Print: " + strings.Join(args, " "))
	},
}

var cmdEcho = &cobra.Command{
	Use:   "echo [string to echo]",
	Short: "Echo anything to the screen",
	Long: `echo is for echoing anything back.
Echo works a lot like print, except it has a child command.`,
	Args: cobra.MinimumNArgs(1),
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("Print: " + strings.Join(args, " "))
	},
}

var cmdTimes = &cobra.Command{
	Use:   "times [# times] [string to echo]",
	Short: "Echo anything to the screen more times",
	Long: `echo things multiple times back to the user by providing
a count and a string.`,
	Args: cobra.MinimumNArgs(1),
	Run: func(cmd *cobra.Command, args []string) {
		for i := 0; i < echoTimes; i++ {
			fmt.Println("Echo: " + strings.Join(args, " "))
		}
	},
}

func init() {
	cobra.OnInitialize(initConfig)

	cmdTimes.Flags().IntVarP(&echoTimes, "times", "t", 1, "times to echo the input")

	// 两个顶层的命令，和一个cmdEcho命令下的子命令cmdTimes
	RootCmd.AddCommand(cmdPrint, cmdEcho)
	cmdEcho.AddCommand(cmdTimes)
}

func Execute() {
	RootCmd.Execute()
}

func initConfig() {
	// 勿忘读取config文件，无论是从cfgFile还是从home文件
	if cfgFile != "" {
		viper.SetConfigName(cfgFile)
	} else {
		// 找到home文件
		home, err := homedir.Dir()
		if err != nil {
			fmt.Println(err)
			os.Exit(1)
		}

		// 在home文件夹中搜索以“.cobra”为名称的config
		viper.AddConfigPath(home)
		viper.SetConfigName(".cobra")
	}
	// 读取符合的环境变量
	viper.AutomaticEnv()

	if err := viper.ReadInConfig(); err != nil {
		fmt.Println("Can not read config:", viper.ConfigFileUsed())
	}
}

```

操作如下：

``` sh
go run main.go

<<'COMMENT'
Usage:
  app [command]

Available Commands:
  echo        Echo anything to the screen
  help        Help about any command
  print       Print anything to the screen
  version     Print the version number of ChenJian

Flags:
  -h, --help   help for app

Use "app [command] --help" for more information about a command.
COMMENT


go run main.go echo -h

<<'COMMENT'
echo is for echoing anything back.
Echo works a lot like print, except it has a child command.

Usage:
  app echo [string to echo] [flags]
  app echo [command]

Available Commands:
  times       Echo anything to the screen more times

Flags:
  -h, --help   help for echo

Use "app echo [command] --help" for more information about a command.
COMMENT

go run main.go echo times -h

<<'COMMENT'
echo things multiple times back to the user by providing
a count and a string.

Usage:
  app echo times [# times] [string to echo] [flags]

Flags:
  -h, --help        help for times
  -t, --times int   times to echo the input (default 1)
COMMENT

go run main.go print HERE I AM
<<'COMMENT'
Print: HERE I AM
COMMENT

go run main.go version
<<'COMMENT'
Chen Jian Version: v1.0 -- HEAD
COMMENT

go run main.go echo times WOW -t 3
<<'COMMENT'
Echo: WOW
Echo: WOW
Echo: WOW
COMMENT
```

### 自定义help和usage

- help

默认的help命令如下：

``` go
func (c *Command) initHelp() {
  if c.helpCommand == nil {
    c.helpCommand = &Command{
      Use:   "help [command]",
      Short: "Help about any command",
      Long: `Help provides help for any command in the application.
        Simply type ` + c.Name() + ` help [path to command] for full details.`,
      Run: c.HelpFunc(),
    }
  }
  c.AddCommand(c.helpCommand)
}
```

可以通过以下来自定义help:

``` go
command.SetHelpCommand(cmd *Command)
command.SetHelpFunc(f func(*Command, []string))
command.SetHelpTemplate(s string)
```

- usage

默认的help命令如下：

``` go
return func(c *Command) error {
  err := tmpl(c.Out(), c.UsageTemplate(), c)
  return err
}
```

可以通过以下来自定义help:

``` go
command.SetUsageFunc(f func(*Command) error)

command.SetUsageTemplate(s string)
```

### 先执行与后执行

Run功能的执行先后顺序如下：

- PersistentPreRun
- PreRun
- Run
- PostRun
- PersistentPostRun

### 错误处理函数

RunE功能的执行先后顺序如下：

- PersistentPreRunE
- PreRunE
- RunE
- PostRunE
- PersistentPostRunE

### 对不明命令的建议

当遇到不明命令，会有提出一定的建，其采用[最小编辑距离算法(Levenshtein distance)](http://www.cnblogs.com/aga-j/archive/2011/04/16/2017658.html)。例如：

``` sh
hugo srever

<<'COMMENT'
Error: unknown command "srever" for "hugo"

Did you mean this?
        server

Run 'hugo --help' for usage.
COMMENT
```

如果你想关闭智能提示，可以：

``` go
command.DisableSuggestions = true

// 或者

command.SuggestionsMinimumDistance = 1
```

或者使用`SuggestFor`属性来自定义一些建议，例如：

``` sh
kubectl remove
<<'COMMENT'
Error: unknown command "remove" for "kubectl"

Did you mean this?
        delete

Run 'kubectl help' for usage.
COMMENT
```


### 参考文献

1. [Cobra简介](http://time-track.cn/cobra-brief-introduction.html)
2. [golang命令行库cobra的使用](http://www.cnblogs.com/borey/p/5715641.html?hmsr=studygolang.com&utm_medium=studygolang.com&utm_source=studygolang.com)

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>本作品由<a xmlns:cc="http://creativecommons.org/ns#" href="https://o-my-chenjian.com/2017/09/20/Using-Cobra-With-Golang/" property="cc:attributionName" rel="cc:attributionURL">陈健</a>采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。