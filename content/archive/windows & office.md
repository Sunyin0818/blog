---
title: windows & office
category:
  - archive
tags:
  - windows
publish: true
date: 2024-11-04 15:46:17
lastmod: 2024-11-07 09:49:54
---
# 1. windows

## 1.1. 下载

+ [https://hellowindows.cn/](https://hellowindows.cn/)
+ [https://next.itellyou.cn/](https://next.itellyou.cn/)

## 1.2. 激活

直接使用[2.1.2. 激活脚本](#2.1.2.%20激活脚本)

也可以尝试另一个[图形化激活工具](https://cmwtat.cloudmoe.com/cn.html)



# 2. office

## 2.1. 资源包准备

### 2.1.1. office安装包

#### 2.1.1.1. （二选一）一键安装
[Office Tool Plus](https://otp.landian.vip/)

#### 2.1.1.2. （二选一）手动安装

+ [office离线镜像](https://massgrave.dev/office_c2r_links.html)

  我这里选择的是ProPlus的离线包，下载得到`O365ProPlusRetail.img`

  ![](/static/images/image-20250304161140604.png)

+ [office部署工具](https://www.microsoft.com/en-us/download/details.aspx?id=49117)

  微软官方提供的工具，用于自定义安装路径和组件数量

  

### 2.1.2. 激活脚本 

[Microsoft-Activation-Scripts](https://github.com/massgravel/Microsoft-Activation-Scripts)

GitHub开源的百k star神器


## 2.2. 一键安装

使用`Office Tool Plus`很方便，按需选择即可



## 2.3. 手动安装
### 2.3.1. 装载镜像

装载离线镜像`O365ProPlusRetail.img`，如果无需自定义安装组件，可以直接安装

### 2.3.2. 自定义安装组件

部署工具的[使用文档](https://learn.microsoft.com/zh-cn/deployoffice/office-deployment-tool-configuration-options#product-element)

安装office部署工具后，可以得到如下的文件：

```bash
-a---          2023/10/19    23:05           1164 configuration-Office2019Enterprise.xml
-a---          2023/10/19    23:05           1368 configuration-Office2021Enterprise.xml
-a---          2023/10/19    23:05           1014 configuration-Office365-x64.xml
-a---          2023/10/19    23:05           1014 configuration-Office365-x86.xml
-a---          2023/10/19    23:05        7615656 setup.exe
```

我们使用`configuration-Office365-x64.xml`作为模板，复制一个重命名为`configuration-Office365-x64 - custom.xml`

修改后内容如下：

```xml
<Configuration>

  <Add OfficeClientEdition="64" SourcePath="E:\" Channel="Current">
    <Product ID="O365ProPlusRetail">
      <Language ID="zh-cn" />
      <ExcludeApp ID="Access" />
      <ExcludeApp ID="Bing" />
      <ExcludeApp ID="Groove" />
      <ExcludeApp ID="Lync" />
      <ExcludeApp ID="OneDrive" />
      <ExcludeApp ID="OneNote" />
      <ExcludeApp ID="Outlook" />
      <ExcludeApp ID="Publisher" />
      <ExcludeApp ID="Teams" />
    </Product>
  </Add>

  <!--  <Updates Enabled="TRUE" Channel="Current" /> -->

  <!--  <Display Level="None" AcceptEULA="TRUE" />  -->

  <!--  <Property Name="AUTOACTIVATE" Value="1" />  -->

</Configuration>
```

- `SourcePath`：镜像装载的盘符
- `ExcludeApp`：可选如下，可查阅微软文档，这里我只保留了三件套

![](/static/images/image-20250304161140624.png)

执行安装命令

```powershell
./setup.exe /configure '.\configuration-Office365-x64 - custom.xml'
```

效果如下图，只安装了三件套

![](/static/images/image-20250304161140638.png)



## 2.4. 激活

解压下载的安装脚本`Microsoft-Activation-Scripts-master.zip`，直接双击运行`Microsoft-Activation-Scripts-master/MAS/All-In-One-Version/MAS_AIO.cmd`

我们选择[2.6. Ohook](04%20Archive/windows%20&%20office.md#2.6.%20Ohook)的方式激活，按`2`

![](/static/images/image-20250304161140655.png)

然后按`1`，开始激活

![](/static/images/image-20250304161140669.png)

## 2.5. 卸载

如需卸载，上图中按`2`，选择`Uninstall`即可卸载激活信息

## 2.6. Ohook

原理上说，KMS 激活是写信告知了微软：「兄弟，咱们是正规军，有手续的那种」，然后一路拿着许可证通过检测。

而 Ohook 激活，是微软发现你没激活，准备写信告诉 Office：「这哥们没激活」，就在这个时候，把这封信给拦截了，并把信里的内容替换成了：「这哥们激活了，放行」。

简单说，就是通过欺骗 Office 的方式，让本地程序把所有功能全部解禁。

卸载就是选「Uninstall」，把那个用于劫持 Office 的文件一删，刚激活的 Office 就又失效了，没有副作用

不过原理大家也看了，这么激活和 KMS 激活一样，正版的云功能是别想了。那个需要微软的二次验证，但不用 180 天一激活，离线功能也更全。