# EasyToDo
EasyToDo is a to-do list type application running on Windows, which follows the principles of ease of use and simple functions.

## Install
1. Install using `Pyinstaller`
```
python -m PyInstaller -w -i EasyToDo.ico -F EasyToDo.py
```
2. After the installation is completed, the `dist` directory will be automatically generated. There is `EasyToDo.exe` in the `dist` directory. Move `EasyToDo.exe` to the project directory to use it normally. If they are not moved, some icons will not work properly.
```
cd dist
cp EasyToDo.exe ../
```

## demo
![GIF](images/demo.gif)

## Features
Current software support functions:
- Enter unfinished tasks
- Show unfinished list
- Show completed list
- Modify software transparency
- The interface is fixed on the desktop


## Items to be optimized and related issues
**Items to be optimized**
- The interface needs to be optimized
- Pinned to desktop no need to move desktop

**Related questions**
- When set to be fixed on the desktop, the interface will disappear. You need to switch the desktop or move the desktop before the interface will appear.
