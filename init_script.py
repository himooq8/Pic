import os
import sys
import pyodbc as dbb

PATH = '/path/to/source/'
DEST_PATH = 'static/images/'
ALLOWED = ('jpg', 'png', 'jpeg', 'JPG', 'PNG', 'JPEG')
count = {}


DRIVER = 'SQL Server'
SERVER_NAME = 'HiMoO'
DATABASE_NAME = 'dima'
Uid = 'python'
Pwd = 'Himoo@123'

Connection = f"""
    Driver={DRIVER};
    Server={SERVER_NAME};
    Database={DATABASE_NAME};
    Trust_Connection=yes;
    Uid={Uid};
    Pwd={Pwd};
"""

conn = ''
cursor = ''


def init_db():
    global conn, cursor
    try:
        conn = dbb.connect(Connection)
    except Exception as e:
        print(str(e))
        sys.exit()
    else:
        cursor = conn.cursor()


def is_picture(file):
    return file.split('.')[-1] in ALLOWED


def copy_file(source, dest):
    with open(source, 'rb') as fr:
        with open(dest, 'wb') as fw:
            fw.write(fr.read())


def write_to_db(number, path, pic_num):
    query = f'INSERT INTO dima.dbo.picture (number, picture, pic_num) values (?, ?, ?)'
    try:
        cursor.execute(query, (number, path, pic_num))
        conn.commit()
    except Exception as e:
        print(str(e))


def main():
    global PATH
    PATH = sys.argv[1]
    for root, _, files in os.walk(PATH):
        for file in files:
            if is_picture(file):
                number = root.split(os.path.sep)[-1]
                source = os.path.join(root, file)
                ext = file.split('.')[-1]
                dest = os.path.join(DEST_PATH, 'img{}-{}.{}'.format(number, count.get(number, 0)+1, ext))
                count[number] = count.get(number, 0)+1
                copy_file(source, dest)
                write_to_db(number, dest, count[number])


if __name__ == '__main__':
    init_db()
    main()
