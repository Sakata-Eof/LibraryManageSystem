import sys
import database
import datetime
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, QPushButton,
                             QTableWidget, QTableWidgetItem, QMessageBox, QTabWidget)

class BookManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("图书管理系统")
        self.resize(1000,800)
        self.db = database.DatabaseManager()
        self.initUI()

    def initUI(self):
        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.create_book_tab(), "图书管理")
        self.tab_widget.addTab(self.create_borrower_tab(), "借阅人管理")
        self.tab_widget.addTab(self.create_borrow_record_tab(), "借阅记录管理")

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tab_widget)
        self.setLayout(main_layout)

    def create_book_tab(self):
        """创建图书管理标签页"""
        self.book_table = QTableWidget()
        self.book_table.setColumnCount(5)
        self.book_table.setHorizontalHeaderLabels(["ID", "书名", "作者", "类型", "年份"])
        self.book_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.book_table.cellClicked.connect(self.fill_book_form)

        form_layout = QFormLayout()
        self.book_title_input = QLineEdit()
        self.book_author_input = QLineEdit()
        self.book_genre_input = QLineEdit()
        self.book_year_input = QLineEdit()
        form_layout.addRow("书名:", self.book_title_input)
        form_layout.addRow("作者:", self.book_author_input)
        form_layout.addRow("类型:", self.book_genre_input)
        form_layout.addRow("年份:", self.book_year_input)

        button_layout = QHBoxLayout()
        add_button = QPushButton("添加")
        update_button = QPushButton("更新")
        delete_button = QPushButton("删除")
        search_button = QPushButton("查询")
        button_layout.addWidget(add_button)
        button_layout.addWidget(update_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(search_button)

        add_button.clicked.connect(self.add_book)
        update_button.clicked.connect(self.update_book)
        delete_button.clicked.connect(self.delete_book)
        search_button.clicked.connect(self.search_books)

        layout = QVBoxLayout()
        layout.addWidget(self.book_table)
        layout.addLayout(form_layout)
        layout.addLayout(button_layout)

        self.load_books()

        book_tab = QWidget()
        book_tab.setLayout(layout)
        return book_tab

    def create_borrower_tab(self):
        """创建借阅人管理标签页"""
        self.borrower_table = QTableWidget()
        self.borrower_table.setColumnCount(3)
        self.borrower_table.setHorizontalHeaderLabels(["ID", "姓名", "邮箱"])
        self.borrower_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.borrower_table.cellClicked.connect(self.fill_borrower_form)

        form_layout = QFormLayout()
        self.borrower_name_input = QLineEdit()
        self.borrower_email_input = QLineEdit()
        form_layout.addRow("姓名:", self.borrower_name_input)
        form_layout.addRow("邮箱:", self.borrower_email_input)

        button_layout = QHBoxLayout()
        add_button = QPushButton("添加")
        update_button = QPushButton("更新")
        search_button = QPushButton("查询")
        delete_button = QPushButton("删除")
        button_layout.addWidget(add_button)
        button_layout.addWidget(update_button)
        button_layout.addWidget(search_button)
        button_layout.addWidget(delete_button)

        add_button.clicked.connect(self.add_borrower)
        update_button.clicked.connect(self.update_borrower)
        search_button.clicked.connect(self.search_borrower)
        delete_button.clicked.connect(self.delete_borrower)

        layout = QVBoxLayout()
        layout.addWidget(self.borrower_table)
        layout.addLayout(form_layout)
        layout.addLayout(button_layout)

        self.load_borrowers()

        borrower_tab = QWidget()
        borrower_tab.setLayout(layout)
        return borrower_tab

    def create_borrow_record_tab(self):
        """创建借阅记录管理标签页"""
        self.record_table = QTableWidget()
        self.record_table.setColumnCount(5)
        self.record_table.setHorizontalHeaderLabels(["ID", "书名", "借阅人", "借阅日期", "归还日期"])
        self.record_table.setSelectionBehavior(QTableWidget.SelectRows)
        #self.record_table.cellClicked.connect(self.fill_record_form)

        form_layout = QFormLayout()
        self.record_book_id_input = QLineEdit()
        self.record_borrower_id_input = QLineEdit()
        self.record_borrow_date_input = QLineEdit()
        self.record_return_date_input = QLineEdit()
        form_layout.addRow("书籍:", self.record_book_id_input)
        form_layout.addRow("借阅人:", self.record_borrower_id_input)
        form_layout.addRow("借阅日期:", self.record_borrow_date_input)
        form_layout.addRow("归还日期:", self.record_return_date_input)

        button_layout = QHBoxLayout()
        add_button = QPushButton("添加")
        delete_button = QPushButton("删除")
        button_layout.addWidget(add_button)
        button_layout.addWidget(delete_button)

        add_button.clicked.connect(self.add_borrow_record)
        delete_button.clicked.connect(self.delete_borrow_record)

        layout = QVBoxLayout()
        layout.addWidget(self.record_table)
        layout.addLayout(form_layout)
        layout.addLayout(button_layout)

        self.load_borrow_records()

        record_tab = QWidget()
        record_tab.setLayout(layout)
        return record_tab

    def add_book(self):
        """添加图书"""
        title = self.book_title_input.text().strip()
        author = self.book_author_input.text().strip()
        genre = self.book_genre_input.text().strip()
        year = self.book_year_input.text().strip()

        if not title or not author or not genre or not year:
            QMessageBox.warning(self, '错误', '所有字段均为必填项。')
            return

        try:
            year = int(year)
        except ValueError:
            QMessageBox.warning(self, '错误', '年份必须为整数。')
            return

        try:
            self.db.add_book(title, author, genre, year)
            QMessageBox.information(self, '成功', '图书添加成功！')
            self.clear_book_form()
            self.load_books()
        except Exception as e:
            QMessageBox.critical(self, '错误', f'添加图书失败: {e}')

    def update_book(self):
        """更新图书"""
        selected_row = self.book_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, '错误', '请选择要更新的图书。')
            return

        book_id = self.book_table.item(selected_row, 0).text()
        title = self.book_title_input.text().strip()
        author = self.book_author_input.text().strip()
        genre = self.book_genre_input.text().strip()
        year = self.book_year_input.text().strip()

        if not title or not author or not genre or not year:
            QMessageBox.warning(self, '错误', '所有字段均为必填项。')
            return

        try:
            year = int(year)
        except ValueError:
            QMessageBox.warning(self, '错误', '年份必须为整数。')
            return

        try:
            self.db.update_book(book_id, title, author, genre, year)
            QMessageBox.information(self, '成功', '图书更新成功！')
            self.clear_book_form()
            self.load_books()
        except Exception as e:
            QMessageBox.critical(self, '错误', f'更新图书失败: {e}')

    def delete_book(self):
        """删除图书"""
        selected_row = self.book_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, '错误', '请选择要删除的图书。')
            return

        book_id = self.book_table.item(selected_row, 0).text()

        try:
            self.db.delete_book(book_id)
            QMessageBox.information(self, '成功', '图书删除成功！')
            self.clear_book_form()
            self.load_books()
        except Exception as e:
            QMessageBox.critical(self, '错误', f'删除图书失败: {e}')

    def search_books(self):
        """根据书名或作者查询图书"""
        title = self.book_title_input.text().strip()
        author = self.book_author_input.text().strip()
        genre = self.book_genre_input.text().strip()
        year = self.book_year_input.text().strip()
        try:
            books = self.db.search_book(title, author, genre, year)
            self.book_table.setRowCount(len(books))
            for row_idx, book in enumerate(books):
                self.book_table.setItem(row_idx, 0, QTableWidgetItem(str(book[0])))
                self.book_table.setItem(row_idx, 1, QTableWidgetItem(book[1]))
                self.book_table.setItem(row_idx, 2, QTableWidgetItem(book[2]))
                self.book_table.setItem(row_idx, 3, QTableWidgetItem(book[3]))
                self.book_table.setItem(row_idx, 4, QTableWidgetItem(str(book[4])))
        except Exception as e:
            QMessageBox.critical(self, '错误', f'查询图书失败: {e}')

    def clear_book_form(self):
        """清空图书表单"""
        self.book_title_input.clear()
        self.book_author_input.clear()
        self.book_genre_input.clear()
        self.book_year_input.clear()

    def fill_book_form(self):
        """填充图书表单"""
        selected_row = self.book_table.currentRow()
        if selected_row < 0:
            return

        book_id = self.book_table.item(selected_row, 0).text()
        title = self.book_table.item(selected_row, 1).text()
        author = self.book_table.item(selected_row, 2).text()
        genre = self.book_table.item(selected_row, 3).text()
        year = self.book_table.item(selected_row, 4).text()

        self.book_title_input.setText(title)
        self.book_author_input.setText(author)
        self.book_genre_input.setText(genre)
        self.book_year_input.setText(year)

    def load_books(self):
        """加载所有图书"""
        try:
            books = self.db.get_books()
            self.book_table.setRowCount(len(books))
            for row_idx, book in enumerate(books):
                self.book_table.setItem(row_idx, 0, QTableWidgetItem(str(book[0])))
                self.book_table.setItem(row_idx, 1, QTableWidgetItem(book[1]))
                self.book_table.setItem(row_idx, 2, QTableWidgetItem(book[2]))
                self.book_table.setItem(row_idx, 3, QTableWidgetItem(book[3]))
                self.book_table.setItem(row_idx, 4, QTableWidgetItem(str(book[4])))
        except Exception as e:
            QMessageBox.critical(self, '错误', f'加载图书失败: {e}')

    def add_borrower(self):
        """添加借阅人"""
        name = self.borrower_name_input.text().strip()
        email = self.borrower_email_input.text().strip()

        if not name or not email:
            QMessageBox.warning(self, '错误', '所有字段均为必填项。')
            return

        try:
            self.db.add_borrower(name, email)
            QMessageBox.information(self, '成功', '借阅人添加成功！')
            self.clear_borrower_form()
            self.load_borrowers()
        except Exception as e:
            QMessageBox.critical(self, '错误', f'添加借阅人失败: {e}')

    def update_borrower(self):
        """更新借阅人"""
        selected_row = self.borrower_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, '错误', '请选择要更新的借阅人。')
            return

        borrower_id = self.borrower_table.item(selected_row, 0).text()
        name = self.borrower_name_input.text().strip()
        email = self.borrower_email_input.text().strip()

        if not name or not email:
            QMessageBox.warning(self, '错误', '所有字段均为必填项。')
            return

        try:
            self.db.update_borrower(borrower_id, name, email)
            QMessageBox.information(self, '成功', '借阅人更新成功！')
            self.clear_borrower_form()
            self.load_borrowers()
        except Exception as e:
            QMessageBox.critical(self, '错误', f'更新借阅人失败: {e}')

    def search_borrower(self):
        """查询借阅人信息"""
        name = self.borrower_name_input.text().strip()
        email = self.borrower_email_input.text().strip()
        try:
            borrowers = self.db.search_borrower(name, email)
            self.borrower_table.setRowCount(len(borrowers))
            for row_idx, borrower in enumerate(borrowers):
                self.borrower_table.setItem(row_idx, 0, QTableWidgetItem(str(borrower[0])))
                self.borrower_table.setItem(row_idx, 1, QTableWidgetItem(borrower[1]))
                self.borrower_table.setItem(row_idx, 2, QTableWidgetItem(borrower[2]))
        except Exception as e:
            QMessageBox.critical(self, '错误', f'查询借阅人失败: {e}')
    def delete_borrower(self):
        """删除借阅人"""
        selected_row = self.borrower_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, '错误', '请选择要删除的借阅人。')
            return

        borrower_id = self.borrower_table.item(selected_row, 0).text()

        try:
            self.db.delete_borrower(borrower_id)
            QMessageBox.information(self, '成功', '借阅人删除成功！')
            self.clear_borrower_form()
            self.load_borrowers()
        except Exception as e:
            QMessageBox.critical(self, '错误', f'删除借阅人失败: {e}')

    def clear_borrower_form(self):
        """清空借阅人表单"""
        self.borrower_name_input.clear()
        self.borrower_email_input.clear()

    def fill_borrower_form(self):
        """填充借阅人表单"""
        selected_row = self.borrower_table.currentRow()
        if selected_row < 0:
            return

        borrower_id = self.borrower_table.item(selected_row, 0).text()
        name = self.borrower_table.item(selected_row, 1).text()
        email = self.borrower_table.item(selected_row, 2).text()

        self.borrower_name_input.setText(name)
        self.borrower_email_input.setText(email)

    def load_borrowers(self):
        """加载所有借阅人"""
        try:
            borrowers = self.db.get_borrowers()
            self.borrower_table.setRowCount(len(borrowers))
            for row_idx, borrower in enumerate(borrowers):
                self.borrower_table.setItem(row_idx, 0, QTableWidgetItem(str(borrower[0])))
                self.borrower_table.setItem(row_idx, 1, QTableWidgetItem(borrower[1]))
                self.borrower_table.setItem(row_idx, 2, QTableWidgetItem(borrower[2]))
        except Exception as e:
            QMessageBox.critical(self, '错误', f'加载借阅人失败: {e}')

    def add_borrow_record(self):
        """添加借阅记录"""
        book_id = self.record_book_id_input.text().strip()
        borrower_id = self.record_borrower_id_input.text().strip()
        borrow_date = self.record_borrow_date_input.text().strip()
        return_date = self.record_return_date_input.text().strip()

        if not book_id or not borrower_id or not borrow_date:
            QMessageBox.warning(self, '错误', '书籍ID、借阅人ID和借阅日期为必填项。')
            return

        if not book_id.isdigit() or not borrower_id.isdigit():
            QMessageBox.warning(self, '错误', '书籍ID、借阅人ID应为纯数字。')
            return
        try:
            borrow_date = datetime.strptime(borrow_date, '%Y-%m-%d').date()
            return_date = datetime.strptime(return_date, '%Y-%m-%d').date() if return_date else None
        except ValueError:
            QMessageBox.warning(self, '错误', '日期格式应为 YYYY-MM-DD。')
            return

        try:
            self.db.add_borrow_record(book_id, borrower_id, borrow_date, return_date)
            QMessageBox.information(self, '成功', '借阅记录添加成功！')
            self.clear_record_form()
            self.load_borrow_records()
        except Exception as e:
            QMessageBox.critical(self, '错误', f'添加借阅记录失败: {e}')


    def update_borrow_record(self):
        #更新借阅记录
        selected_row = self.record_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, '错误', '请选择要更新的借阅记录。')
            return

        record_id = self.record_table.item(selected_row, 0).text()
        book_id = self.record_book_id_input.text().strip()  # 获取书籍ID输入框的文本
        borrower_id = self.record_borrower_id_input.text().strip()  # 获取借阅人ID输入框的文本
        borrow_date = self.record_borrow_date_input.text().strip()
        return_date = self.record_return_date_input.text().strip()

        if not book_id or not borrower_id or not borrow_date:
            QMessageBox.warning(self, '错误', '书籍ID、借阅人ID和借阅日期为必填项。')
            return

        try:
            borrow_date = datetime.strptime(borrow_date, '%Y-%m-%d').date()
            return_date = datetime.strptime(return_date, '%Y-%m-%d').date() if return_date else None
        except ValueError:
            QMessageBox.warning(self, '错误', '日期格式应为 YYYY-MM-DD。')
            return

        try:
            self.db.update_borrow_record(record_id, book_id, borrower_id, borrow_date, return_date)
            QMessageBox.information(self, '成功', '借阅记录更新成功！')
            self.clear_record_form()
            self.load_borrow_records()
        except Exception as e:
            QMessageBox.critical(self, '错误', f'更新借阅记录失败: {e}')

    def delete_borrow_record(self):
        """删除借阅记录"""
        selected_row = self.record_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, '错误', '请选择要删除的借阅记录。')
            return

        record_id = self.record_table.item(selected_row, 0).text()

        try:
            self.db.delete_borrow_record(record_id)
            QMessageBox.information(self, '成功', '借阅记录删除成功！')
            self.clear_record_form()
            self.load_borrow_records()
        except Exception as e:
            QMessageBox.critical(self, '错误', f'删除借阅记录失败: {e}')

    def clear_record_form(self):
        """清空借阅记录表单"""
        self.record_book_id_input.clear()
        self.record_borrower_id_input.clear()
        self.record_borrow_date_input.clear()
        self.record_return_date_input.clear()

    def fill_record_form(self):
        """填充借阅记录表单"""
        selected_row = self.record_table.currentRow()
        if selected_row < 0:
            return

        record_id = self.record_table.item(selected_row, 0).text()
        book_id = self.record_table.item(selected_row, 1).text()  # 使用书籍ID而不是书名
        borrower_id = self.record_table.item(selected_row, 2).text()  # 使用借阅人ID而不是姓名
        borrow_date = self.record_table.item(selected_row, 3).text()
        return_date = self.record_table.item(selected_row, 4).text()

        self.record_book_id_input.setText(book_id)
        self.record_borrower_id_input.setText(borrower_id)
        self.record_borrow_date_input.setText(borrow_date)
        self.record_return_date_input.setText(return_date)

    def load_borrow_records(self):
        """加载所有借阅记录"""
        try:
            records = self.db.get_borrow_records()
            self.record_table.setRowCount(len(records))
            for row_idx, record in enumerate(records):
                self.record_table.setItem(row_idx, 0, QTableWidgetItem(str(record[0])))
                self.record_table.setItem(row_idx, 1, QTableWidgetItem(record[1]))
                self.record_table.setItem(row_idx, 2, QTableWidgetItem(record[2]))
                self.record_table.setItem(row_idx, 3, QTableWidgetItem(str(record[3])))
                self.record_table.setItem(row_idx, 4, QTableWidgetItem(str(record[4]) if record[4] else ""))
        except Exception as e:
            QMessageBox.critical(self, '错误', f'加载借阅记录失败: {e}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    manager = BookManager()
    manager.show()
    sys.exit(app.exec_())
