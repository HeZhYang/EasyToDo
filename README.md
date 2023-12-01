# EasyToDo
EasyToDo是一款运行在Windows上的to-do list类型的应用，遵循易用和功能简单的原则。

## 安装
1. 使用`Pyinstaller`安装
```
python -m PyInstaller -w -i EasyToDo.ico -F EasyToDo.py
```
2. 安装完成后会自动生成`dist`目录，在`dist`目录中有`EasyToDo.exe`，将`EasyToDo.exe`移动至项目目录下即可正常是使用。如不移动，部分图标无法正常使用。
```
cd dist
cp EasyToDo.exe ../
```

## demo
![GIF](images/demo.gif)

## 功能介绍
目前软件支持功能：
- 输入未完成任务
- 显示未完成列表
- 显示已完成列表
- 修改软件透明度
- 界面固定在桌面上


## 待优化项和相关问题
**待优化项**
- 界面待优化
- 固定在桌面上不需要移动桌面

**相关问题**
- 设置为固定在桌面上时，界面会消失，需要切换桌面或移动桌面，界面才会出现
