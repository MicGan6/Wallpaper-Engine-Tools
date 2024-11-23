# Wallpaper Engine:壁纸引擎 第三方工具
将Wallpaper Engine: 壁纸引擎的壁纸进行导出
## 使用方法
### 方法1(推荐普通用户使用)
1. 打开Release
2. 下载对应软件包，解压后运行main.exe即可
### 方法2(推荐开发用户使用)
1. 通过Git Clone的方式将本程序克隆至您的电脑
2. 运行Main.py
## 运行环境
开发时使用Python 3.12.4， 最低标准Python 3.7.3
## 关于源代码
**如果你想修改本程序源代码，请务必看完本部分**
- 本程序支持自动安装第三方库
- 本程序使用的库如下:
   1. UI: tkinter, tkinter.messagebox
   2. 目录&文件相关: os, json, shutil
   3. 终端: subprocess
   4. 退出程序:sys
   5. 多线程: threading
   6. 获取路径: winreg
   7. 日志: loguru 
   8. 图片: PIL
- 为了方便国际化 ~~(其实是因为Vs Code的中文显示有问题)~~ ，本程序注释采用英文，后续版本将创建新分支以存储含有中文版注释的程序
- 本程序使用面向对象编程的格式(不是标准的tkinter式)
- PR: 本程序欢迎PR，但对PR有一定要求
   
   1. 请尽量使用Python标准库
   2. 请确保你的程序有注释(中英均可), 我们会翻译
   3. 请尽量使用面向对象编程的格式
   4. 欢迎各位的PR
## 目前程序问题&发展规划
- [ ] 程序只能在Windows上使用(关于移植其他平台暂不考虑，因为WPE不支持其他平台)
- [ ] 增加批量导出功能
- [ ] 筛选限制内容(基于json文件实现,)
## 声明
1. RePKG.exe不是本仓库所有者开发的,  它的仓库 *[在这](https://github.com/notscuffed/repkg)*,记得给它个Star
2. 导出的壁纸版权归壁纸创作者所有，本程序仅供学习交流使用。
3. 本程序采用GPL-V3开源，请遵守该开源协议
4. 本项目的workflow与issue模板均参考[gyc-123456-1的pynotepad项目](https://github.com/gyc123456-1/pynotepad)