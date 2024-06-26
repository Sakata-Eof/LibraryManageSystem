import psycopg2





class DatabaseManager:
    def __init__(self):
        self.connection = psycopg2.connect(database="db_tpcc", user="joe", password="Bigdata@123", host="139.9.139.6", port=26000)
        self.create_tables()

    def create_tables(self):
        """创建数据库表"""
        with self.connection.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS books (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    author VARCHAR(255) NOT NULL,
                    genre VARCHAR(100),
                    year INTEGER
                );
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS borrowers (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL
                );
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS borrow_records (
                    id SERIAL PRIMARY KEY,
                    book_id INTEGER NOT NULL REFERENCES books(id),
                    borrower_id INTEGER NOT NULL REFERENCES borrowers(id),
                    borrow_date DATE NOT NULL,
                    return_date DATE
                );
            ''')
            self.connection.commit()

    def add_book(self, title, author, genre, year):
        """添加图书"""
        with self.connection.cursor() as cursor:
            cursor.execute('''
                INSERT INTO books (title, author, genre, year) VALUES (%s, %s, %s, %s);
            ''', (title, author, genre, year))
            self.connection.commit()

    def update_book(self, book_id, title, author, genre, year):
        """更新图书"""
        with self.connection.cursor() as cursor:
            cursor.execute('''
                UPDATE books SET title=%s, author=%s, genre=%s, year=%s WHERE id=%s;
            ''', (title, author, genre, year, book_id))
            self.connection.commit()

    def delete_book(self, book_id):
        """删除图书"""
        with self.connection.cursor() as cursor:
            cursor.execute('''
                DELETE FROM books WHERE id=%s;
            ''', (book_id,))
            self.connection.commit()

    def get_books(self):
        """获取所有图书"""
        with self.connection.cursor() as cursor:
            cursor.execute('SELECT * FROM books;')
            return cursor.fetchall()

    def search_book(self, title=None, author=None, genre=None, year=None):
        """根据书名或作者查询图书"""
        with self.connection.cursor() as cursor:
            query = "SELECT * FROM books WHERE TRUE"
            params = []

            if title:
                query += " AND title ILIKE %s"
                params.append(f"%{title}%")
            if author:
                query += " AND author ILIKE %s"
                params.append(f"%{author}%")
            if genre:
                query += " AND genre ILIKE %s"
                params.append(f"%{genre}%")
            if year:
                query += " AND year = %s"
                params.append(year)

            cursor.execute(query, params)
            return cursor.fetchall()

    def add_borrower(self, name, email):
        """添加借阅人"""
        with self.connection.cursor() as cursor:
            cursor.execute('''
                INSERT INTO borrowers (name, email) VALUES (%s, %s);
            ''', (name, email))
            self.connection.commit()

    def update_borrower(self, borrower_id, name, email):
        """更新借阅人"""
        with self.connection.cursor() as cursor:
            cursor.execute('''
                UPDATE borrowers SET name=%s, email=%s WHERE id=%s;
            ''', (name, email, borrower_id))
            self.connection.commit()

    def delete_borrower(self, borrower_id):
        """删除借阅人"""
        with self.connection.cursor() as cursor:
            cursor.execute('''
                DELETE FROM borrowers WHERE id=%s;
            ''', (borrower_id,))
            self.connection.commit()

    def get_borrowers(self):
        """获取所有借阅人"""
        with self.connection.cursor() as cursor:
            cursor.execute('SELECT * FROM borrowers;')
            return cursor.fetchall()

    def add_borrow_record(self, book_id, borrower_id, borrow_date, return_date):
        """添加借阅记录"""
        with self.connection.cursor() as cursor:
            cursor.execute('''
                INSERT INTO borrow_records (book_id, borrower_id, borrow_date, return_date)
                VALUES (%s, %s, %s, %s);
            ''', (book_id, borrower_id, borrow_date, return_date))
            self.connection.commit()

    def update_borrow_record(self, record_id, book_id, borrower_id, borrow_date, return_date):
        """更新借阅记录"""
        with self.connection.cursor() as cursor:
            cursor.execute('''
                UPDATE borrow_records SET book_id=%s, borrower_id=%s, borrow_date=%s, return_date=%s
                WHERE id=%s;
            ''', (book_id, borrower_id, borrow_date, return_date, record_id))
            self.connection.commit()

    def delete_borrow_record(self, record_id):
        """删除借阅记录"""
        with self.connection.cursor() as cursor:
            cursor.execute('''
                DELETE FROM borrow_records WHERE id=%s;
            ''', (record_id,))
            self.connection.commit()

    def get_borrow_records(self):
        """获取所有借阅记录"""
        with self.connection.cursor() as cursor:
            cursor.execute('''
                SELECT br.id, b.title, bw.name, br.borrow_date, br.return_date
                FROM borrow_records br
                JOIN books b ON br.book_id = b.id
                JOIN borrowers bw ON br.borrower_id = bw.id;
            ''')
            return cursor.fetchall()

