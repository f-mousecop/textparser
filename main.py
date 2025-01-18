import sys
import re

from PyQt6.QtWidgets import (
    QApplication, QLabel, QWidget, QLineEdit, 
    QPushButton, QVBoxLayout, QMainWindow, QHBoxLayout,
     QGridLayout, QFormLayout, QDialog, QMessageBox, 
     QInputDialog, QFileDialog, QMenu, QPlainTextEdit,
     QGraphicsDropShadowEffect, QToolBar, QStatusBar, QCheckBox
)
from PyQt6.QtCore import QObject, pyqtSignal, Qt
from PyQt6.QtGui import QIcon, QColor, QAction
from PyQt6 import QtGui, QtCore, QtWidgets


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.setWindowTitle("Text File Reader")
        self.setWindowIcon(QIcon('favicon.ico'))
        self.resize(350, 250)
        self.setWindowFlags(Qt.WindowType.Window)
        

        """ button_action = QAction("Button", self)
        button_action.setStatusTip("This is the button")
        button_action.triggered.connect(self.onMyToolBarButtonClick)
        button_action.setCheckable(True)

        button_action2 = QAction("&Button 2", self)
        button_action2.setStatusTip("Button 2")
        button_action2.triggered.connect(self.onMyToolBarButtonClick)
        button_action2.setCheckable(True)
        
        close_button = QAction("&X", self)
        close_button.setStatusTip("Close")
        close_button.triggered.connect(self.onCloseButtonClick)

        self.setStatusBar(QStatusBar(self))

        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        file_menu.addAction(button_action)
        file_menu.addSeparator()
        file_menu.addAction(button_action2)
        close = menu.addAction(close_button) """
        


        # Create QLabel
        label = QLabel("Enter file name:")
        self.fileInput = QLineEdit(self)
        self.fileInput.setStyleSheet("background-color: #eee")

        # Create push button
        submitButton = QPushButton("Submit", self)
        submitButton.clicked.connect(self.onButtonClick)

        openFileButton = QPushButton("Open File", self)
        openFileButton.clicked.connect(self.onOpenFileClicked)

        clearButton = QPushButton("Clear", self)
        clearButton.clicked.connect(self.onClearButtonClick)

        closeButton = QPushButton("Close")
        closeButton.clicked.connect(self.onCloseButtonClick)

        # self.output = QPlainTextEdit(self)
        # self.output.setStyleSheet("background-color: #eee")
        # self.output.setHidden(True)


        # Create vertical layout
        layout = QFormLayout()
        layout.setContentsMargins(20, 60, 20, 20)
        layout.setSpacing(10)
        layout.addRow(label, self.fileInput)
        
        
        hLayout = QHBoxLayout()
        hLayout.addWidget(submitButton)
        hLayout.addWidget(openFileButton)
        hLayout.addWidget(clearButton)
        hLayout.addWidget(closeButton)
        layout.addRow(hLayout)
        # layout.addRow(self.output)
       
        # Create central widget and set layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
        central_widget.setStyleSheet('''
                QWidget {
                    background-color: #a0a4b8;
                    font-size: 15px; 
                }
                QPushButton {
                    background-color: #d8ddef
                }
        ''')
        
        # self.setMinimumSize(400, 200)
    
    def onMyToolBarButtonClick(self, s):
        print("click", s)

    def onOpenFileClicked(self):
        self.user_input = self.fileInput.text().strip('"')
        file_handler = FileHandler(self.user_input)

        if file_handler.read_file():
            self.file_window = FileWindow(file_handler)
            self.file_window.show()
        else:
            return



    def onButtonClick(self):
        print("Clicked")
        self.user_txt = self.fileInput.text().strip('"')
        data_handler = DataHandler(self.user_txt)
        # self.validateFileName()

        if data_handler.read_file():
            self.data_window = DataWindow(data_handler)
            self.data_window.show()
        else:
            return
    
    def validateFileName(self):
        if not re.match(r'^[a-zA-Z0-9_\-]+\.txt$', self.user_txt):
            raise ValueError("Invalid file name")

    def onClearButtonClick(self):
        self.fileInput.clear()

    def onCloseButtonClick(self):
        QApplication.exit()


    def get_input(self):
        text, ok = QInputDialog.getText(self, "Input Dialog", "Enter name: ")
        if ok:
            print("Your name is: ", text)


class DataHandler:
    def __init__(self, file_name):
        self.file_name = file_name
        self.numbers = []
        
    def read_file(self):
        try:
            with open(self.file_name, 'r') as file:
                content = file.read()

            self.numbers = [
                            int(num) for num in content.split()
                            if num.replace('.', '', 1).isdigit()
                            ]

            if not self.numbers:
                raise ValueError("No valid numbers found.")

            return self.file_name

        except FileNotFoundError:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setText(f"File '{self.file_name}' not found.")
            msg_box.setWindowTitle("Error")
            msg_box.exec()

        except ValueError as ve:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setText(str(ve))
            msg_box.setWindowTitle("Error")
            msg_box.exec()
        
        except Exception as oe:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setText(str(oe))
            msg_box.setWindowTitle("Error")
            msg_box.exec()
        
        return False

    def calc_sum(self):
        return sum(self.numbers)

    def get_strings(self):
        return ", ".join(map(str, self.numbers)), " + ".join(map(str,self.numbers))


class DataWindow(MainWindow):
    def __init__(self, data_handler):
        super().__init__()
        self.data_handler = data_handler
        self.initDataUI()

    def initDataUI(self):
        self.setWindowTitle("Calculation Results")
        self.resize(600, 200)

        try:
            name = self.data_handler.read_file()
            result = str(self.data_handler.calc_sum())
            numbers_str, numbers_add = self.data_handler.get_strings()

            layout = QFormLayout()
            label1 = QLabel("Total")
            label2 = QLabel(f"Numbers found in '{name}'")
            label3= QLabel("Addition")
            label4 = QLabel("Sum")
            
            text1 = QLineEdit(result)
            text2 = QLineEdit(numbers_str)
            text3 = QLineEdit(numbers_add)
            text4 = QLineEdit(result)

            text1.setReadOnly(True), text2.setReadOnly(True)
            text3.setReadOnly(True), text4.setReadOnly(True)

            close_button = QPushButton("Close")
            close_button.clicked.connect(self.close)
            layout.addRow(label1, text1)
            layout.addRow(label2, text2)
            layout.addRow(label3, text3)
            layout.addRow(label4, text4)
            box_layout = QVBoxLayout()
            layout.addRow(box_layout)
            box_layout.addWidget(close_button, 4, Qt.AlignmentFlag.AlignCenter)
            close_button.setFixedWidth(200)
            layout.setSpacing(10)
            
            
            central_widget = QWidget()
            central_widget.setLayout(layout)
            self.setCentralWidget(central_widget)
            central_widget.setStyleSheet('''
                    QWidget {
                        background-color: #a0a4b8;
                        font-size: 15px;     
                    }
                    QLineEdit {
                        background-color: #eee
                    }
                    QPushButton {
                        background-color: #d8ddef
                    }

            ''')


        except Exception as e:
            layout = QFormLayout()
            error_label = QLabel(F"Error: {str(e)}")
            layout.addWidget(error_label)

            central_widget = QWidget()
            central_widget.setLayout(layout)
            self.setCentralWidget(central_widget)


class FileHandler:
    def __init__(self, file_name):
        self.file_name = file_name
    
    def read_file(self):
        try:
            with open(self.file_name, 'r') as file:
                content = file.read()

            return content
        
        except FileNotFoundError:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setText(f"File '{self.file_name}' not found.")
            msg_box.setWindowTitle("Error")
            msg_box.exec()

        except Exception as oe:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setText(str(oe))
            msg_box.setWindowTitle("Error")
            msg_box.exec()
            
        return False

    
class FileWindow(MainWindow):
    def __init__(self, file_handler):
        super().__init__()
        self.file_handler = file_handler
        self.initDataUI()
    
    def initDataUI(self):
        self.setWindowTitle("Content")
        self.resize(600, 300)
        self.setMinimumSize(400,300)

        try:
            output = self.file_handler.read_file()

            layout = QVBoxLayout()
            test_area = QPlainTextEdit(self)
            test_area.setPlainText(output)
            test_area.setReadOnly(True)

            close_button = QPushButton("Close Window")
            close_button.clicked.connect(self.close)
            close_button.setFixedWidth(200)

            box_layout = QVBoxLayout()

            layout.addWidget(test_area, Qt.AlignmentFlag.AlignHCenter)
            layout.addLayout(box_layout)
            layout.setSpacing(10)
            box_layout.addWidget(close_button, 4, Qt.AlignmentFlag.AlignCenter)

            central_widget = QWidget()
            central_widget.setLayout(layout)
            self.setCentralWidget(central_widget)

            central_widget.setStyleSheet('''
                        QWidget {
                            background-color: #a0a4b8;
                            font-size: 15px;     
                        }
                        QPlainTextEdit {
                            background-color: #eee
                        }
                        QPushButton {
                            background-color: #d8ddef
                        }

                ''')
        except Exception as e:
            layout = QFormLayout()
            error_label = QLabel(F"Error: {str(e)}")
            layout.addWidget(error_label)

            central_widget = QWidget()
            central_widget.setLayout(layout)
            self.setCentralWidget(central_widget)   


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet('''
        
        QPushButton {
                font-size: 13px;
                background-color: #d8ddef  
        }
        
        QToolBar, QStatusBar {
                background-color: #A0A4B8
        }
        
        QMenuBar {
                      background-color: #d8ddef;
                      }
        window {
                      background-color: #d8ddef;
                      }
''')

    window = MainWindow()
    window.show()

    sys.exit(app.exec())