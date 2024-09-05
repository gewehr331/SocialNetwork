import psycopg2
from psycopg2 import sql


class database:
    __dbname = "socialnetwork"
    __user = "postgres"
    __password = "postgres"
    __host = "localhost"
    __port = "5432"

    def connect(self):
        conn = psycopg2.connect(
            dbname=self.__dbname,
            user=self.__user,
            password=self.__password,
            host=self.__host,
            port=self.__port
        )

        # Создание курсора
        cur = conn.cursor()
        return cur, conn

    def add_new_user(self, username, password):
        cur, conn = self.connect()

        # Создание таблицы
        cur.execute("""INSERT INTO users (username, password) VALUES (%s, %s);""", (username, password))

        cur.close()
        conn.commit()
        conn.close()
    def check_user(self, username, password):
        cur, conn = self.connect()

        cur.execute("""select * from users where username=%s and password=%s;""",(username, password))

        rows = cur.fetchall()
        if rows:
            return "success"
        else:
            return "not success"


if __name__ == "__main__":
    test = database()
    res = test.check_user(username='ad1min', password='admin')
    print(res)