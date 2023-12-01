import sys
import win32gui
import sqlite3
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import  QWidget, QVBoxLayout, QListWidget, QLineEdit, QComboBox, QHBoxLayout


class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self.setWindowTitle('Settings')
        self.setGeometry(100, 100, 300, 150)
        layout = QtWidgets.QVBoxLayout(self)

        self.stick_to_desktop_checkbox = QtWidgets.QCheckBox("Stick to Desktop", self)
        self.stick_to_desktop_checkbox.setChecked(parent.is_sticking_to_desktop)
        layout.addWidget(self.stick_to_desktop_checkbox)

        layout.addWidget(QtWidgets.QLabel('Opacity:', self))
        self.opacity_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.opacity_slider.setMinimum(0)
        self.opacity_slider.setMaximum(100)
        self.opacity_slider.setValue(int(parent.windowOpacity() * 100))
        layout.addWidget(self.opacity_slider)

        self.save_button = QtWidgets.QPushButton('Save', self)
        self.save_button.clicked.connect(self.accept)
        layout.addWidget(self.save_button)

    def is_sticking_to_desktop(self):
        return self.stick_to_desktop_checkbox.isChecked()

    def get_opacity(self):
        return self.opacity_slider.value() / 100.0

# Database initialization and functions
def init_db():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT,
            description TEXT,
            create_time TEXT,
            finish_time TEXT,
            is_done INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def add_task_to_db(title, description, is_done):
    try:
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        current_time = QtCore.QDateTime.currentDateTime().toString(QtCore.Qt.ISODate)
        c.execute('''
            INSERT INTO tasks (title, description, create_time, is_done)
            VALUES (?, ?, ?, ?)
        ''', (title, description, current_time, is_done))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"An error occurred: {e.args[0]}")
        return False

def get_task(task_id):
    try:
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
        task = c.fetchone()
        conn.close()
        return task
    except sqlite3.Error as e:
        print(f"An error occurred: {e.args[0]}")
        return None

def get_tasks(is_done):
    try:
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        if is_done:
            c.execute('SELECT id, title, finish_time FROM tasks WHERE is_done = ? ORDER BY finish_time DESC', (is_done,))
        else:
            c.execute('SELECT id, title, create_time FROM tasks WHERE is_done = ?', (is_done,))
        tasks = c.fetchall()
        conn.close()
        return [(id, title, QtCore.QDateTime.fromString(time, QtCore.Qt.ISODate).toString("MM/dd")) for id, title, time in tasks]
    except sqlite3.Error as e:
        print(f"An error occurred: {e.args[0]}")
        return [] 

def update_task_status(task_id, is_done):
    try:
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute('''
            UPDATE tasks SET is_done = ?, finish_time = ?
            WHERE id = ?
        ''', (is_done, QtCore.QDateTime.currentDateTime().toString(QtCore.Qt.ISODate) if is_done else None, task_id))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"An error occurred: {e.args[0]}")
        return False

def update_task(task_id, title, description):
    try:
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute('''
            UPDATE tasks SET title = ?, description = ?
            WHERE id = ?
        ''', (title, description, task_id))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"An error occurred: {e.args[0]}")
        return False

def delete_task_from_db(task_id):
    try:
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"An error occurred: {e.args[0]}")
        return False

class TaskDetailsDialog(QtWidgets.QDialog):
    def __init__(self, task_id, parent=None):
        super(TaskDetailsDialog, self).__init__(parent)
        self.task_id = task_id
        self.setWindowTitle('Task Details')
        self.setGeometry(100, 100, 300, 200)
        # 创建顶部布局用于标题和删除按钮
        self.top_layout = QtWidgets.QHBoxLayout()

        # 标题标签
        self.title_label = QtWidgets.QLabel('Title:', self)
        self.top_layout.addWidget(self.title_label)

        # 删除按钮，使用垃圾桶图标
        self.delete_button = QtWidgets.QPushButton(self)
        self.delete_button.setIcon(QIcon('images/trash_icon.png'))  # 设置按钮图标
        self.delete_button.setIconSize(QtCore.QSize(18, 18))  # 设置图标大小
        self.delete_button.clicked.connect(self.delete_task)
        self.top_layout.addWidget(self.delete_button, alignment=Qt.AlignRight)  # 右对齐

        # 创建主布局并添加顶部布局
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addLayout(self.top_layout)

        # Fetch task details
        task = get_task(task_id)
        if task:
            self.title_input = QtWidgets.QLineEdit(task[1], self)
            self.description_input = QtWidgets.QTextEdit(self)
            self.description_input.setPlainText(task[2])
            self.create_time_label = QtWidgets.QLabel("Created: " + task[3], self)
            self.finish_time_label = QtWidgets.QLabel("Finished: " + (task[4] if task[4] else "Not finished"), self)

            # self.layout.addWidget(QtWidgets.QLabel('Title:', self))
            self.layout.addWidget(self.title_input)
            self.layout.addWidget(QtWidgets.QLabel('Description:', self))
            self.layout.addWidget(self.description_input)
            self.layout.addWidget(self.create_time_label)
            self.layout.addWidget(self.finish_time_label)

            # Save button
            self.save_button = QtWidgets.QPushButton('Save', self)
            self.save_button.clicked.connect(self.save_task)
            self.layout.addWidget(self.save_button)
        else:
            self.layout.addWidget(QtWidgets.QLabel('Task not found!', self))

    def save_task(self):
        title = self.title_input.text()
        description = self.description_input.toPlainText() 
        update_task(self.task_id, title, description)
        self.accept()

    def delete_task(self):
        # 调用删除任务的函数
        if delete_task_from_db(self.task_id):
            self.accept()  # 关闭对话框
            # QtWidgets.QMessageBox.information(self, "Deleted", "Task has been deleted.")
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Could not delete the task.")

class TaskWidget(QtWidgets.QWidget):
    taskStatusChanged = QtCore.pyqtSignal(int, bool)

    def __init__(self, task_id, title, date, is_done, parent=None):
        super(TaskWidget, self).__init__(parent)
        self.task_id = task_id
        layout = QtWidgets.QHBoxLayout(self)

        # Checkbox to mark task as done
        self.checkbox = QtWidgets.QCheckBox()
        self.checkbox.setChecked(is_done)
        self.checkbox.stateChanged.connect(self.emit_task_status)
        layout.addWidget(self.checkbox)

        # Task title label
        self.title_label = QtWidgets.QLabel(title)
        layout.addWidget(self.title_label)

        layout.addStretch()  # This will push the following widgets to the right

        # Task date label, aligned to the right
        self.date_label = QtWidgets.QLabel(date)
        self.date_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        layout.addWidget(self.date_label)

    def emit_task_status(self, state):
        self.taskStatusChanged.emit(self.task_id, state == QtCore.Qt.Checked)

class TodoApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        init_db()
        self.currently_showing = 0  # 0 for not done, 1 for done
        self.is_sticking_to_desktop = False
        self.initUI()
        self.setWindowIcon(QIcon('images/EasyToDo.ico'))

    def set_as_desktop_child(self):
        def set_parent():
            hwnd = self.winId()
            progman = win32gui.FindWindow("Progman", None)
            if not progman:
                return
            win32gui.SetParent(hwnd, progman)

        # 延迟执行设置父窗口操作
        QTimer.singleShot(1000, set_parent) 

    def initUI(self):
        self.setWindowTitle('EasyToDo')
        self.setGeometry(100, 100, 600, 400)
        self.setWindowIcon(QIcon('images/EasyToDo.ico'))

        # Apply a style sheet for the overall app for a consistent look
        self.setStyleSheet("""
            QWidget {
                font-size: 15px;
            }
            QComboBox, QPushButton, QLineEdit {
                padding: 7px;
                margin: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #eee;
            }
            QPushButton:hover {
                background-color: #ddd;
            }
            QListWidget {
                border: none;
            }
            QLineEdit {
                border: 1px solid #aaa;
            }
            QCheckBox {
                width: 20px;
                height: 20px;
            }
        """)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Top row layout for settings and task type dropdown
        self.top_row_layout = QHBoxLayout()
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.addLayout(self.top_row_layout)

        # Task type dropdown
        self.task_type_dropdown = QComboBox()
        self.task_type_dropdown.addItem("To-Do")
        self.task_type_dropdown.addItem("Done")
        self.task_type_dropdown.currentIndexChanged.connect(self.change_task_type)
        self.top_row_layout.addWidget(self.task_type_dropdown, alignment=Qt.AlignLeft)

        # Settings button
        self.settings_button = QtWidgets.QPushButton(self)
        self.settings_button.setIcon(QtGui.QIcon('images/settings_icon.png'))  # 设置按钮图标
        self.settings_button.setIconSize(QtCore.QSize(20, 20))  # 设置图标大小
        self.settings_button.clicked.connect(self.open_settings_dialog)
        self.top_row_layout.addWidget(self.settings_button, alignment=QtCore.Qt.AlignRight)

        # Todo list
        self.todo_list = QListWidget()
        self.main_layout.addWidget(self.todo_list)

        # New task input
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText('Enter new task and press Enter')
        self.task_input.returnPressed.connect(self.create_new_task)
        self.main_layout.addWidget(self.task_input)

        self.populate_list(self.currently_showing)
        if self.is_sticking_to_desktop:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnBottomHint)

        self.centerOnScreen()

    def centerOnScreen(self):
        # 获取屏幕尺寸和窗口尺寸
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        size = self.geometry()

        # 计算窗口在屏幕中心的位置
        self.move((screen.width() - size.width()) // 2, 
                  (screen.height() - size.height()) // 2)

        if self.is_sticking_to_desktop:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnBottomHint)
            self.show()  # 重新显示窗口以应用新的窗口标志

    def change_task_type(self, index):
        self.currently_showing = index
        self.populate_list(self.currently_showing)

        # 当选择已完成列表时，隐藏新任务输入框
        if index == 1:  # 假设 "Done" 项的索引为 1
            self.task_input.hide()
        else:
            self.task_input.show()

    def create_new_task(self):
        title = self.task_input.text()
        if title:
            if add_task_to_db(title, "", self.currently_showing):
                self.populate_list(self.currently_showing)  # Update the list
            self.task_input.clear()

    def populate_list(self, is_done):
        try:
            self.todo_list.clear()
            tasks = get_tasks(is_done)
            for task_id, title, time in tasks:
                task_widget = TaskWidget(task_id, title, time, is_done)
                task_widget.taskStatusChanged.connect(self.on_task_status_changed)
                task_widget.title_label.mousePressEvent = lambda event, task_id=task_id: self.show_task_details(task_id)
                item = QtWidgets.QListWidgetItem(self.todo_list)
                item.setSizeHint(task_widget.sizeHint())
                self.todo_list.addItem(item)
                self.todo_list.setItemWidget(item, task_widget)
        except Exception as e:
            print(f"An error occurred when populating the list: {e}")

    def on_task_status_changed(self, task_id, is_done):
        if update_task_status(task_id, is_done):
            self.populate_list(self.currently_showing)
    
    def open_settings_dialog(self):
        try:
            dialog = SettingsDialog(self)

            # 获取主窗口的位置和尺寸
            mainWindowRect = self.geometry()
            dialog.move(mainWindowRect.left(), mainWindowRect.top())

            if dialog.exec_():
                self.is_sticking_to_desktop = dialog.is_sticking_to_desktop()
                opacity_value = dialog.get_opacity()
                self.setWindowOpacity(opacity_value)

                if self.is_sticking_to_desktop:
                    self.set_as_desktop_child()
                else:
                    win32gui.SetParent(self.winId(), None)
        except Exception as e:
            print(f"Error in settings dialog: {e}")

    def show_task_details(self, task_id):
        dialog = TaskDetailsDialog(task_id)
        # 获取主窗口的位置和尺寸
        mainWindowRect = self.geometry()

        # 将任务详情对话框移动到主窗口的位置
        dialog.move(mainWindowRect.left(), mainWindowRect.top())
        if dialog.exec_():
            self.populate_list(self.currently_showing)

if __name__ == '__main__':
    QtWidgets.QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)  # 启用高 DPI 缩放
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QIcon('images/EasyToDo.ico'))
    mainWin = TodoApp()
    mainWin.show()
    sys.exit(app.exec_())