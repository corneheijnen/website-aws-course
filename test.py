from sqlalchemy import create_engine, inspect
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

from sqlalchemy.sql import text

engine = create_engine("mysql+pymysql://admin:j3eCawR71!@database-1.c7vm4wmhspek.eu-central-1.rds.amazonaws.com/blogpost?charset=utf8mb4")
connection = engine.connect()

data = ({"username": "corne", "password": "test"}, {"username": "miguel", "password": "test"})

for line in data:
    connection.execute(text("INSERT INTO user(username, password) VALUES (:username, :password)"), parameters= line)

result = connection.execute(text("SELECT * FROM user"))
for line in result:
    print(line)

# for line in data:
#     connection.execute(text("INSERT INTO test(name) VALUES (:name)"), parameters={'name': line['username']})
#
# connection.execute(text("SELECT * FROM user"))
#
#
# metadata = MetaData()
# books = Table('test', metadata,
#   Column('id', Integer, primary_key=True, autoincrement=True),
#   Column('name', String(16)),
# )
# metadata.create_all(engine)
