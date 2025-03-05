---
title: Docker下Jellyfin中文乱码
categories:
  - area
tags:
  - NAS
publish: true
date: 2025-01-21 11:41:32
lastmod: 2025-03-05 09:53:13
---
# 1. 问题

容器化使用jellyfin对中文支持不那么友好，比如

封面图里的中文字变方块
![](/images/image-20250304161139407.png)

字幕乱码
![](/images/image-20250304161139436.png)

# 2. 解决方案

## 2.1. 封面乱码

创建一个新的挂载路径`fonts/dejavu` 指向容器内路径 `/usr/share/fonts/truetype/dejavu`

```dockerfile
    volumes:
      - /vol1/1000/data/docker/jellyfin/config:/config
      - /vol1/1000/data/docker/jellyfin/cache:/cache
      - /vol1/1000/data/docker/jellyfin/fonts/dejavu:/usr/share/fonts/truetype/dejavu
```

容器内有以下字体文件，这些字体是不支持中文显示的，我们要把这些字体替换掉

```bash
DejaVuSans-Bold.ttf 
DejaVuSans.ttf 
DejaVuSansMono-Bold.ttf 
DejaVuSansMono.ttf 
DejaVuSerif-Bold.ttf 
DejaVuSerif.ttf 
```

替换为支持中文简体的字体，这里借一下[老E的博客](https://appscross.com/blog/jellyfin-cover-and-subtitles-garbled.html)做好的下载链接，[https://appscross.com/as-tools/pub%20Tools/Jellyfinfonts/target-fonts.7z](https://appscross.com/as-tools/pub%20Tools/Jellyfinfonts/target-fonts.7z)

重启jellyfin容器，删除封面，重新扫描媒体库即可。 

## 2.2. 字幕乱码

1. 挂载路径下的config中创建fonts文件夹 
2. 下载字体包 [Noto Sans SC woff2](https://raw.githubusercontent.com/CodePlayer/webfont-noto/master/release/NotoSansCJKsc-hinted-standard.zip "Noto Sans SC woff2") 
3. 解压包，将 `NotoSansCJKsc-Medium.woff2` 放入`fonts`目录 
4. 切换到控制台-->播放-->转码，勾选启用备用字体，填入路径/config/fonts路径，保存即可。 ![](/images/image-20250304161139460.png)



> 参考：
>
> 1. [Jellyfin封面与字幕乱码的解决方法 - 老E的博客](https://appscross.com/blog/jellyfin-cover-and-subtitles-garbled.html)
> 2. [解决 Docker 安装 Jellyfin 封面图和部分中文字幕变方块 - 川叶 :: 不舍昼夜](https://blog.lishun.me/docker-jellyfin-chinese-fonts)
