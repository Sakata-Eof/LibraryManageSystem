import random
from faker import Faker
import database
# 向表中随机填入数据
# 初始化Faker实例，并设置为中文
fake = Faker('zh_CN')

# 定义一些类别
genres = ['科幻', '小说', '历史', '传记', '童话', '悬疑', '浪漫', '技术', '哲学', '诗歌']

cur = database.DatabaseManager()


for i in range(1000):
    title = fake.sentence(nb_words=random.randint(1, 5))
    author = fake.name()
    genre = random.choice(genres)
    year = random.randint(1, 2024)
    cur.add_book(title, author, genre, year)

    name = fake.name()
    email = fake.company_email()
    cur.add_borrower(name, email)

    print(i)


