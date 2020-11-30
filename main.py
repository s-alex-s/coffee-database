import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.textEdit.setReadOnly(True)
        self.pushButton.clicked.connect(self.show_coffee)

    def show_coffee(self):
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        coffee_list = cur.execute('''SELECT * FROM type_of_coffee''')
        self.textEdit.clear()
        self.textEdit.setText(self.textEdit.toPlainText() + '---------------------------------\n')
        for i in coffee_list:
            self.textEdit.setText(self.textEdit.toPlainText() + 'Сорт: ' + i[1] + '\n')
            self.textEdit.setText(self.textEdit.toPlainText() + 'Степень обжарки: ' + i[2] + '\n')
            self.textEdit.setText(self.textEdit.toPlainText() + 'Молотый/в зернах: ' + i[3] + '\n')
            self.textEdit.setText(self.textEdit.toPlainText() + 'Описание вкуса: ' + i[4] + '\n')
            self.textEdit.setText(self.textEdit.toPlainText() + 'Цена: ' + str(i[5]) + ' тг.\n')
            self.textEdit.setText(self.textEdit.toPlainText() + 'Объем упаковки: ' + str(i[6]) + ' г.\n')
            self.textEdit.setText(self.textEdit.toPlainText() + '---------------------------------\n')
        con.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())
