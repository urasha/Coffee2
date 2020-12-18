import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect('coffee.sqlite')
        self.cur = self.con.cursor()
        self.load_table()
        self.pushButton.clicked.connect(self.switch)

    def load_table(self):
        lst = self.cur.execute('SELECT * FROM espresso').fetchall()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels('ID, название, описание,'.split(','))
        self.tableWidget.horizontalHeader().setSectionResizeMode(1)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(lst):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, col in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(col)))

    def switch(self):
        self.wind = EditCoffee()
        self.wind.show()
        self.close()


class EditCoffee(QMainWindow):
    def __init__(self):
        super(EditCoffee, self).__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.pushButton.clicked.connect(self.act)

    def act(self):
        self.con = sqlite3.connect('coffee.sqlite')
        self.cur = self.con.cursor()
        lst = self.textEdit.toPlainText().split(', ')
        try:
            self.cur.execute(f'INSERT INTO coffee(id, title, description)'
                             f' VALUES(?, ?, ?)', (*lst,))
        except sqlite3.IntegrityError:
            self.cur.execute("""UPDATE coffee
                                SET name = ?,
                                title = ?,
                                description = ?,
                                WHERE id = ?""", (*lst[1:], lst[0]))
        except Exception:
            return
        self.con.commit()
        self.wind = Window()
        self.wind.show()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wind = Window()
    wind.show()
    sys.exit(app.exec())
