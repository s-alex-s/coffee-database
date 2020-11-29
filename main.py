import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.pushButton.clicked.connect(self.show_coffee)

    def show_coffee(self):
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        coffee_list = cur.execute('''SELECT * FROM type_of_coffee''')
        for i in coffee_list:
            self.textEdit.setText('Эспрессо\n')
            self.textEdit.setText(self.textEdit.toPlainText() + '---------------------------------\n')
            self.textEdit.setText(self.textEdit.toPlainText() + 'Сорт: ' + i[1] + '\n')
            self.textEdit.setText(self.textEdit.toPlainText() + 'Степень обжарки: ' + i[2] + '\n')
            self.textEdit.setText(self.textEdit.toPlainText() + 'Молотый/в зернах: ' + i[3] + '\n')
            self.textEdit.setText(self.textEdit.toPlainText() + 'Описание вкуса: ' + i[4] + '\n')
            self.textEdit.setText(self.textEdit.toPlainText() + 'Цена: ' + i[5] + '\n')
            self.textEdit.setText(self.textEdit.toPlainText() + 'Объем упаковки: ' + i[6] + '\n')
            self.textEdit.setText(self.textEdit.toPlainText() + '---------------------------------\n')
        con.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())
