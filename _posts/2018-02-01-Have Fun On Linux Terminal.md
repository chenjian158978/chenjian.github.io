---
layout:     post
title:      "Linux终端上的乐趣"
subtitle:   "Have Fun On Linux Terminal"
date:       Thu, Feb 01 2018 23:10:37 GMT+8
author:     "ChenJian"
header-img: "img/in-post/Have-Fun-On-Linux-Terminal/head_blog.jpg"
catalog:    true
tags: [工作, Linux]
---

### 包下载网站推荐

1. [https://pkgs.org/](https://pkgs.org/)


### [cmatrix](https://www.asty.org/cmatrix)

经典电影《黑客帝国》（The Matrix），在男主眼中，任何东西都是以计算机字节流的形式流动。我们也可以进化成这样！

#### 安装

``` shell
# ubuntu 16.04
sudo apt-get install cmatrix -y


# centos7
yum -y install gcc make ncurses-devel
sudo wget https://svwh.dl.sourceforge.net/project/cmatrix/cmatrix/1.2a/cmatrix-1.2a.tar.gz
tar -xvf cmatrix-1.2a.tar.gz
cd cmatrix-1.2a
./configure && make && make install
```
#### 运行

``` shell
cmatrix
```

其中参数如下：

-  -a: Asynchronous scroll 异步滚动
-  -b: Bold characters on 字符加粗
-  -B: All bold characters (overrides -b) 所有字符加粗
-  -f: Force the linux $TERM type to be on 强制开启Linux $TERM（Ctrl+c）退出模式 
-  -l: Linux mode (uses matrix console font) Linux模式(使用matrix控制台字体)
-  -o: Use old-style scrolling 使用旧式滚动
-  -h: Print usage and exit 输出使用说明并退出
-  -n: No bold characters (overrides -b and -B, default) 关闭字符加粗(优于-b与-B，默认)
-  -s: "Screensaver" mode, exits on first keystroke 屏保模式，第一次按键退出
-  -x: X window mode, use if your xterm is using mtx.pcf X窗口模式，如果使用mtx.pcf终端
-  -V: Print version information and exit 打印版本信息并退出
-  -u delay (0 - 10, default 4): Screen update delay 屏幕更新延时(0-10秒，默认4秒)
-  -C [color]: Use this color for matrix (default green) 调整matrix颜色(默认绿色)

#### 效果

![cmatrix](/img/in-post/Have-Fun-On-Linux-Terminal/cmatrix.jpg)

### sl

一辆火车缓缓开过....

#### 安装

``` shell
# ubuntu 16.04
sudo apt-get install sl -y

# centos7
yum install sl -y
```

#### 运行

``` shell
sl
```

更多功能：

``` shell
NAME
       sl - cure your bad habit of mistyping 治愈你的输入错误的坏毛病

SYNOPSIS
       sl [ -alFc ]

DESCRIPTION
       sl is a highly advanced animation program for curing your bad habit of mistyping.

       -a     An accident is occurring. People cry for help. 发生事故，人们哭着喊救命

       -l     Little version 小点儿的火车

       -F     It flies like the galaxy express 999. 像星球急速一样飞起来了

       -c     C51 appears instead of D51. 暂时不知
```

#### 效果

``` shell
                            (@@) (  ) (@)  ( )  @@    ()    @     O     @     O      @
                        (   )
                    (@@@@)
                (    )

              (@@@)
          ====        ________                ___________
        _D _|  |_______/        \__I_I_____===__|_________|
        |(_)---  |   H\________/ |   |        =|___ ___|      _________________
        /     |  |   H  |  |     |   |         ||_| |_||     _|                \_____A
       |      |  |   H  |__--------------------| [___] |   =|                        |
       | ________|___H__/__|_____/[][]~\_______|       |   -|                        |
       |/ |   |-----------I_____I [][] []  D   |=======|____|________________________|_
      __/ =| o |=-~~\  /~~\  /~~\  /~~\ ____Y___________|__|__________________________|_
      |/-=|___|=    ||    ||    ||    |_____/~\___/          |_D__D__D_|  |_D__D__D_|
      \_/      \_O=====O=====O=====O/      \_/               \_/   \_/    \_/   \_/
```

### cowsay & fortune/fortune-zh

#### 安装

``` shell
# ubuntu 16.04
sudo apt-get install -y cowsay fortune fortune-zh

# centos7
yum install -y fortune cowsay
```

#### 运行

``` shell
# fortune会输出英文
fortune | cowsay
# fortune会输出中文诗词
fortune-zh | cowsay
```

``` shell
 _______________________________________
/ Silence is the element in which great \
| things fashion themselves.            |
|                                       |
\ -- Thomas Carlyle                     /
 ---------------------------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||

 ___________________________________________________________________
/ 《金陵图》 作者：韦庄                                     \
\ 江雨霏霏江草齐，六朝如梦鸟空啼。 无情最是台城柳，依旧烟笼十里堤。 /
 -------------------------------------------------------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||

```

#### 另类图形

``` shell
cowsay -h

<<'COMMENT'
Cow files in /usr/share/cowsay:
beavis.zen blowfish bong bud-frogs bunny cheese cower default dragon
dragon-and-cow elephant elephant-in-snake eyes flaming-sheep ghostbusters
head-in hellokitty kiss kitty koala kosh luke-koala mech-and-cow meow milk
moofasa moose mutilated ren satanic sheep skeleton small sodomized
stegosaurus stimpy supermilker surgery telebears three-eyes turkey turtle
tux udder vader vader-koala www
COMMENT
```

- `fortune | cowsay -f hellokitty`

``` shell
 ________________________________________
/ Kites rise highest against the wind -- \
| not with it.                           |
|                                        |
\ -- Winston Churchill                   /
 ----------------------------------------
  \
   \
      /\_)o<
     |      \
     | O . O|
      \_____/
```

- `fortune | cowsay -f skeleton`

``` shell
 _________________________________________
/ As a goatherd learns his trade by goat, \
\ so a writer learns his trade by wrote.  /
 -----------------------------------------
          \      (__)      
           \     /oo|  
            \   (_"_)*+++++++++*
                   //I#\\\\\\\\I\
                   I[I|I|||||I I `
                   I`I'///'' I I
                   I I       I I
                   ~ ~       ~ ~
                     Scowleton
```
> 不过作者还做了mutilated（掉头的奶牛），sodomized（兽奸），three-eyes（三只眼睛的奶牛）这些比较恐怖的图形；还有一些比较搞笑的，例如www，是拥有“三个奶头”的奶牛；以及一些很荒谬的，例如head-in，人头在牛屁股里面。

> 这些让我甚是吃惊！

### 观看《星球大战-第四集》

#### 运行

``` shell
telnet towel.blinkenlights.nl
```

#### 效果


``` shell
                  ..........   @@@@@    @@@@@             ...........    
                  .........   @     @  @     @            ..........     
                  ........       @@@   @     @             ........      
                  .......      @@      @     @             ........      
                   ......     @@@@@@@   @@@@@  th         ......         
                  ......    -----------------------        ....          
                  .....       C  E  N  T  U  R  Y          ...           
                  ....      -----------------------        ...           
                  ..        @@@@@ @@@@@ @   @ @@@@@        ..            
                  ==          @   @      @ @    @          ==            
                __||__        @   @@@@    @     @        __||__          
               |      |       @   @      @ @    @       |      |         
      _________|______|_____  @   @@@@@ @   @   @  _____|______|_________

                                                                         
                          8888888888  888    88888                       
                         88     88   88 88   88  88                      
                          8888  88  88   88  88888                       
                             88 88 888888888 88   88                     
                      88888888  88 88     88 88    888888                
                                                                         
                      88  88  88   888    88888    888888                
                      88  88  88  88 88   88  88  88                     
                      88 8888 88 88   88  88888    8888                  
                       888  888 888888888 88   88     88                 
                        88  88  88     88 88    8888888                  
                                                                         

                 |          ___________________          |               
                 |         /__\     /__\      /\         |               
                 |        |<><>|   |<><>|    |<>|        |               
                 |        |_/\_)   (_/\_)    (_/|        |               
                 |        |  *  \ /      \  /   |        |               
                 |        |/***|| ||/=*\||  ||/=|        |               
                 |        |/ *\ | | /  \ |  | / |        |               
                 |        |][][\/ \/][][\/  \/][|        |               
                 |        |\  /|   |\  /|    |\ |        |               
                 |        |_||_|   |_||_|    |_||        |               
                 |        | ][ ]   [ ][ ]    [ ]|        |               
                 |         \_|_|___|_||_|____|_/         |               
                 |                                       |               


                             ,===                                        
                            (@o o@                                       
                             \ -/                                        
                           //~  ~~\          ___                         
                          /  (   ) \        /() \                        
                         /_/\    /\_|     _|_____|_                      
                          \\ \\ /| ||    | | === | |                     
                           @ | | | @     |_|  O  |_|                     
                             | | |        ||  O  ||                      
                             | | |        ||__*__||                      
                            /  |  \      |~ \___/ ~|                     
                            ~~~~~~~      /=\     /=\                     
      ______________________(_)(__\______[_]_____[_]_____________________
```

### aafire

我的爱情就像一把火，燃烧了整个终端。

#### 安装

``` shell
# ubuntu 16.04
sudo apt-get install libaa-bin -y
```

#### 运行

``` shell
aafire
```

#### 效果

![aafire](/img/in-post/Have-Fun-On-Linux-Terminal/aafire.jpg)

### oneko

#### 安装

> 需要桌面版本的

``` shell
# ubuntu 16.04
sudo apt-get install oneko -y

# centos7
yum install oneko -y
```

#### 运行

``` shell
oneko -dog
```

- -speed 奔跑的速度
- -neko 一只纯色小猫
- -tora 一只背部有条纹的小猫
- -dog 一只小狗
- -sakura 一个短裙猫耳的小女孩
- -tomoyo 一个长发爱摄像的小女孩

#### 效果

![oneko](/img/in-post/Have-Fun-On-Linux-Terminal/oneko.jpg)


### [figlet](http://www.figlet.org/)

#### 安装

``` shell
# ubuntu 16.04
sudo apt-get install figlet -y

# centos7
yum install figlet -y
```

#### 运行

``` shell
figlet chenjian
```

可以在官网下载一些字体，例如`bell.flf`。

然后使用参数`-f`：

``` shell
figlet chenjian -f bell.flf
```

#### 效果

``` shell
# default
      _                 _ _             
  ___| |__   ___ _ __  (_|_) __ _ _ __  
 / __| '_ \ / _ \ '_ \ | | |/ _` | '_ \ 
| (__| | | |  __/ | | || | | (_| | | | |
 \___|_| |_|\___|_| |_|/ |_|\__,_|_| |_|
                     |__/              

# bell.flf
        _                                          
   ___  /        ___  , __       .  `   ___  , __  
 .'   ` |,---. .'   ` |'  `.     \  |  /   ` |'  `.
 |      |'   ` |----' |    |     |  | |    | |    |
  `._.' /    | `.___, /    | /`  |  / `.__/| /    |
                             \___/`                
```

### [asciiquarium](http://www.robobunny.com/projects/asciiquarium/html/)

#### 安装

``` shell
# 安装Perl module
# centos7
yum install perl-Curses perl-ExtUtils-MakeMaker perl-Data-Dumper -y
cd /tmp
wget http://search.cpan.org/CPAN/authors/id/K/KB/KBAUCOM/Term-Animation-2.6.tar.gz
tar -zxvf Term-Animation-2.6.tar.gz
cd Term-Animation-2.6/
perl Makefile.PL && make && make test
sudo make install

# ubuntu 16.04
sudo apt-get install libcurses-perl
cd /tmp
wget http://search.cpan.org/CPAN/authors/id/K/KB/KBAUCOM/Term-Animation-2.6.tar.gz
tar -zxvf Term-Animation-2.6.tar.gz
cd Term-Animation-2.6/
perl Makefile.PL && make && make test
sudo make install

# 安装asciiquarium
wget http://www.robobunny.com/projects/asciiquarium/asciiquarium.tar.gz  
tar -zxvf asciiquarium.tar.gz
cd asciiquarium_1.1/
cp asciiquarium /usr/local/bin
chmod 0755 /usr/local/bin/asciiquarium
```

#### 运行

``` shell
asciiquarium
```

#### 效果

![asciiquarium](/img/in-post/Have-Fun-On-Linux-Terminal/asciiquarium.jpg)

### bb

#### 安装

``` shell
# ubuntu 16.04
sudo apt-get install bb -y
```

#### 运行

``` shell
bb
```

#### 效果

![bb](/img/in-post/Have-Fun-On-Linux-Terminal/bb.jpg)


### moo

#### 运行

moo隐藏在`apt-get命令`下:

``` shell
apt-get -h

<<'COMMENT'
...
See apt-get(8) for more information about the available commands.
Configuration options and syntax is detailed in apt.conf(5).
Information about how to configure sources can be found in sources.list(5).
Package and version choices can be expressed via apt_preferences(5).
Security details are available in apt-secure(8).
                                        This APT has Super Cow Powers.
COMMENT

# This APT has Super Cow Powers.
apt-get moo
```

#### 效果

``` shell
                 (__) 
                 (oo) 
           /------\/ 
          / |    ||   
         *  /\---/\ 
            ~~   ~~   
..."Have you mooed today?"...
```

### [xeyes](https://linux.die.net/man/1/xeyes)

#### 安装

> 需要桌面版本的

``` shell
# ubuntu 16.04
sudo apt-get install xeyes -y

# centos7
yum install xeyes -y
```

#### 运行

``` shell
xeyes
```

#### 效果

![xeyes](/img/in-post/Have-Fun-On-Linux-Terminal/xeyes.jpg)

### [toilet](http://caca.zoy.org/wiki/toilet)

源码在: [cacalabs/toilet](https://github.com/cacalabs/toilet)

``` shell
# ubuntu 16.04
sudo apt-get install -y toilet
```

#### 运行

``` shell
toilet -f mono9 -F gay I Love You
```

#### 效果

![toilet](/img/in-post/Have-Fun-On-Linux-Terminal/toilet.jpg)


### 参考博文

1. [Linux下使用cmatrix正确的装逼](http://blog.csdn.net/qq_31573519/article/details/53667871)
2. [动画演示10个有趣但毫无用处的Linux命令](http://www.linuxidc.com/Linux/2013-12/94300.htm)
3. [在centos下用cmatrix做出黑客屏幕数字下雨效果](http://blog.csdn.net/springyh/article/details/79204695)
4. [Linux下好玩的命令](https://www.cnblogs.com/joeyupdo/articles/2768113.html)
5. [Linux 奇技淫巧](https://www.cnblogs.com/Nice-Boy/p/6091307.html)
6. [在 Linux 终端下看《星球大战》](https://linux.cn/article-6827-1.html)
7. [非常有趣linux图形及动画显示-菜鸟提升兴趣必看](http://blog.51cto.com/oldboy/1669526)
8. [macasciiquarium](https://habilis.net/macasciiquarium/)
9. [Linux/UNIX Desktop Fun: Terminal ASCII Aquarium](https://www.cyberciti.biz/tips/linux-unix-apple-osx-terminal-ascii-aquarium.html)
10. [编译git遇到的perl-ExtUtils-MakeMaker错误](http://blog.csdn.net/zj_jim/article/details/55190192)


<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>本作品由<a xmlns:cc="http://creativecommons.org/ns#" href="https://o-my-chenjian.com/2018/02/01/Have-Fun-On-Linux-Terminal/" property="cc:attributionName" rel="cc:attributionURL">陈健</a>采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。