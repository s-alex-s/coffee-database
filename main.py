import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QPushButton
from PyQt5.QtCore import pyqtSignal


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.textEdit.setReadOnly(True)
        self.pushButton.clicked.connect(self.show_coffee)
        self.pushButton_2.clicked.connect(self.edit_window)
        self.pushButton_3.clicked.connect(self.add_window)

    def show_coffee(self):
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        coffee_list = cur.execute('''SELECT * FROM type_of_coffee''')
        self.textEdit.clear()
        self.textEdit.setText(self.textEdit.toPlainText() + '---------------------------------\n')
        for i in coffee_list:
            self.textEdit.setText(self.textEdit.toPlainText() + 'id: ' + str(i[0]) + '\n')
            self.textEdit.setText(self.textEdit.toPlainText() + 'Сорт: ' + i[1] + '\n')
            self.textEdit.setText(self.textEdit.toPlainText() + 'Степень обжарки: ' + i[2] + '\n')
            self.textEdit.setText(self.textEdit.toPlainText() + 'Молотый/в зернах: ' + i[3] + '\n')
            self.textEdit.setText(self.textEdit.toPlainText() + 'Описание вкуса: ' + i[4] + '\n')
            self.textEdit.setText(self.textEdit.toPlainText() + 'Цена: ' + str(i[5]) + ' тг.\n')
            self.textEdit.setText(self.textEdit.toPlainText() + 'Объем упаковки: ' + str(i[6]) + ' г.\n')
            self.textEdit.setText(self.textEdit.toPlainText() + '---------------------------------\n')
        con.close()

    def edit_window(self):
        global ex2
        ex2 = SecondWindow()
        ex2.show()
        ex2.edit_coffee()

    def add_window(self):
        global ex2
        ex2 = SecondWindow()
        ex2.show()
        ex2.add_coffee()


class SecondWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.pushButton.clicked.connect(self.save_coffee)

    def add_coffee(self):
        self.label_7.hide()
        self.spinBox_3.hide()
        self.setWindowTitle('Добавить кофе')

    def edit_coffee(self):
        self.setWindowTitle('Редактировать кофе')

    def save_coffee(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())
