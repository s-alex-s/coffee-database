import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QInputDialog, QMessageBox


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
        check_id = QInputDialog.getInt(self, 'id', 'Введите id кофе', 1, 1, 10000, 1)
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        while not list(cur.execute(f'SELECT * FROM type_of_coffee WHERE id = {check_id[0]}')) and check_id[1]:
            QMessageBox.information(self, 'id', 'Кофе с таким id не существует')
            check_id = QInputDialog.getInt(self, 'id', 'Введите id кофе', 1, 1, 10000, 1)
        if check_id[1]:
            con.close()
            ex2.show()
            ex2.edit_coffee(check_id[0])
        con.close()

    def add_window(self):
        global ex2
        ex2 = SecondWindow()
        ex2.show()
        ex2.add_coffee()


class SecondWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.pushButton.clicked.connect(self.save_coffee_add)
        self.pushButton_2.clicked.connect(self.save_coffee_edit)

    def add_coffee(self):
        self.pushButton_2.hide()
        self.setWindowTitle('Добавить кофе')

    def edit_coffee(self, id):
        self.current_id = id
        self.pushButton.hide()
        self.setWindowTitle(f'Редактировать кофе | id: {self.current_id}')
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        info = list(cur.execute(f'SELECT * FROM type_of_coffee WHERE id = {self.current_id}'))[0]
        self.lineEdit.setText(info[1])
        self.lineEdit_2.setText(info[2])
        if info[3] == 'Молотый':
            self.comboBox.setCurrentIndex(0)
        else:
            self.comboBox.setCurrentIndex(1)
        self.lineEdit_3.setText(info[4])
        self.spinBox.setValue(info[5])
        self.spinBox_2.setValue(info[6])
        con.close()

    def save_coffee_add(self):
        self.statusBar().clearMessage()
        if self.lineEdit.text() and self.lineEdit_2.text() and self.lineEdit_3.text():
            if self.lineEdit.text().isalpha() and self.lineEdit_2.text().isalpha() and self.lineEdit.text().isalpha():
                con = sqlite3.connect('coffee.sqlite')
                cur = con.cursor()
                cur.execute('''INSERT INTO type_of_coffee(variety, roasting, type, taste, price, size) 
                               VALUES(?, ?, ?, ?, ?, ?)''', (self.lineEdit.text(), self.lineEdit_2.text(),
                                                             self.comboBox.currentText(), self.lineEdit_3.text(),
                                                             self.spinBox.value(), self.spinBox_2.value()))
                con.commit()
                con.close()
                ex.show_coffee()
                ex2.close()
            else:
                self.statusBar().showMessage('Введите корректные данные')
        else:
            self.statusBar().showMessage('Заполните все поля')

    def save_coffee_edit(self):
        self.statusBar().clearMessage()
        if self.lineEdit.text() and self.lineEdit_2.text() and self.lineEdit_3.text():
            if self.lineEdit.text().isalpha() and self.lineEdit_2.text().isalpha() and self.lineEdit.text().isalpha():
                con = sqlite3.connect('coffee.sqlite')
                cur = con.cursor()
                cur.execute('''UPDATE type_of_coffee
                               SET variety = ?, roasting = ?, type = ?, taste = ?, price = ?, size = ?
                               WHERE id = ?''', (self.lineEdit.text(), self.lineEdit_2.text(),
                                                 self.comboBox.currentText(), self.lineEdit_3.text(),
                                                 self.spinBox.value(), self.spinBox_2.value(),
                                                 self.current_id))
                con.commit()
                con.close()
                ex.show_coffee()
                ex2.close()
            else:
                self.statusBar().showMessage('Введите корректные данные')
        else:
            self.statusBar().showMessage('Введите корректные данные')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())
