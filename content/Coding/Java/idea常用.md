---
title: idea常用
slug: idea-chang-yong
date: 2026-03-25 18:12:12
lastmod: 2026-04-20 14:18:32
publish: true
tags:
  - Coding
---



# 1. 下载

[idea官网](https://www.jetbrains.com/idea/download/#section=windows)下载Ultimate版本的安装包

或直接使用`scoop`安装

```
scoop install idea-ultimate
```

# 2. 激活

采用`ja-netfilter`，可至下面地址获取激活码和安装包

[https://jetbra.in/5d84466e31722979266057664941a71893322460](https://jetbra.in/5d84466e31722979266057664941a71893322460)

在`idea64.vmoptions`中，添加如下配置，注意修改路径

```
--add-opens=java.base/jdk.internal.org.objectweb.asm=ALL-UNNAMED
--add-opens=java.base/jdk.internal.org.objectweb.asm.tree=ALL-UNNAMED
-javaagent:C:\Users\sunyin\jetbra\ja-netfilter.jar=jetbrains
```

# 3. 常用配置

## 3.1. 隐藏.idea,.iml文件

![](/images/image-5c4a5c9e-036e-4a69-95ff-8e3620214c0f.png)

## 3.2. 文件修改显示* 号

![](/images/image-2188cdad-f64a-4b2c-8cd1-e109941cacea.png)

## 3.3. eclipse风格的import

![](/images/image-6d3ee6a7-7414-49e8-8b58-6e5ad895f01e.png)

![](/images/image-f1b333a6-37dd-495e-802f-97e307fc57fd.png)

## 3.4. 优先使用Module源码编译

运行配置中需要勾选解析工作区工件

![](/images/image-ca3f94d1-9824-42bc-a9a0-26dd17b29cfb.png)

# 4. 高频使用的快捷键

|   |   |
|---|---|
|**快捷键**|作用|
|Ctrl + Shift + Enter|代码补全后，自动在代码末尾添加分号结束符|
|Ctrl + Alt + B|跳转到实现类|
|Ctrl + U|跳转到接口|
|Ctrl + P|在某个方法中，调用该按键后，会展示出这个方法的调用参数列表信息|
|Ctrl + Q|展示某个类或者方法的 API 说明文档|
|Ctrl + F12|展示所有structure，类似eclipse的outline|
|Ctrl + O|展示该类中所有覆盖或者实现的方法列表|
|Ctrl + Alt + T|自动生成具有环绕性质的代码，比如：if..else,try..catch, for, synchronized 等等，使用前要先选择好需要环绕的代码块|
|Ctrl + W|选中当前光标所在的代码块，多次触发，代码块会逐级变大。（常用）|
|Alt + Q|展示包含当前光标所在代码的父节点信息，比如在 java 方法中调用，就会展示方法签名信息。|
|Alt + Enter|展示当前当前光标所在代码，可以变化的扩展操作|
|Ctrl + Alt + L|格式化代码|
|Ctrl + Alt + O|去除未使用的包|
|Ctrl + Shift + V|从之前的剪切或拷贝的代码历史记录中，选择现在需要粘贴的内容。|
|Ctrl + Alt + V|自动补全方法的返回值|
|Ctrl + Y|删除行|
|Ctrl + D|复制行|
|Ctrl + Shift + U|转换大小写|
|Alt + Shift + Insert|多行编辑模式|
|Ctrl + Shift + ]/[|从当前光标所在位置开始，一直选择到当前光标所在代码段起始或者结束位置。|
|Ctrl + Delete|删除从当前光标所在位置开始，直到这个单词的结尾的内容。|
|Ctrl + Shift + Space|智能补全|
|Shift + F6|重命名|
|Ctrl + (+/-)|展开/收起代码|
|Ctrl + Shift + (+/-)|展开/收起所有代码|
|Ctrl + E|最近文件|
|Ctrl + Shift + A|操作|
|Ctrl + Shift + N|搜索文件|
|Ctrl + N|搜索java文件|
|Ctrl + R|替换文本|
|Ctrl + Alt + F7|打开使用情况列表。|
|Alt + Number|切换面板|
|Shift + Esc|关闭当前面板|
|Ctrl + K|代码Commit|
|Ctrl + T|代码Update|
|Ctrl + Shift + K|代码Push(Git)|
|Ctrl + H|查看类或接口的继承关系|
|Ctrl + Alt + B|查找接口的实现类|

# 5. 常用插件

## 5.1. Rainbow Brackets Lite

彩虹色括号，方便代码阅读，

## 5.2. CodeGlance Pro

类似VSCode右侧的缩略图，方便代码滚动，可使用快捷键`Ctrl+Shift+G`开启/关闭

## 5.3. JRebel

热部署插件

### 5.3.1. 激活

#### 5.3.1.1. 本地反代理

用[本地反代理工具](https://github.com/ilanyu/ReverseProxy)启动

```
./ReverseProxy_windows_amd64.exe -l "0.0.0.0:8888"
```

然后server激活GUID通过在线GUID随机生成即可

![](/images/image-59c8951b-efc6-4b3c-a37d-510d548891d2.png)

#### 5.3.1.2. GitHub开源项目
clone [JrebelLicenseServerforJava](https://github.com/Byron4j/JrebelLicenseServerforJava)
idea启动运行即可

## 5.4. Maven Helper

用于分析jar包依赖

打开pom文件，点击下方的`Dependency Analyzer`即可唤出

## 5.5. Patcher

用于导出增量更新文件

![](/images/image-73e7e817-8ed3-4d26-8f2f-293e58a03d1e.png)

## 5.6. GitToolBox

增强Git

![](/images/image-0ce0a0c0-8e47-444f-a582-270742c34207.png)

## 5.7. .ignore

用于快速创建`.gitignore`的插件

![](/images/image-6b5d2444-e113-4ff5-af52-74916b68c26a.png)
