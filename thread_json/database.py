import pymysql
from datetime import datetime


class MysqlHelple():
    def __init__(self, host, user, password, db):
        self.host = host
        self.user = user
        self.password = password
        self.db = db

    def connect(self):
        conn = pymysql.connect(self.host, self.user, self.password, self.db)
        cursor = conn.cursor()
        return conn, cursor

    def insert_into_t_news(self, conn, cursor, param):
        sql = 'INSERT INTO t_news VALUES(%s,%s,%s,%s,%s,%s,%s)'
        try:
            print(param)
            cursor.execute(sql, param)
            conn.commit()
            print("插入t_news成功:", param)
        except Exception as e:
            conn.rollback()
            print("exception:", e)
        # finally:
        #     conn.close()

    def insert_into_t_label(self, conn, cursor, param):
        sql = "INSERT INTO t_label VALUES(%s, %s)"
        try:
            cursor.execute(sql, param)
            conn.commit()
            print("插入t_lable成功:", param)
        except Exception as e:
            conn.rollback()
            print("exception:", e)
        # finally:
        #     conn.close()

    def insert_into_t_news_label(self, conn, cursor, param):
        sql = "INSERT INTO t_news_label VALUES(%s, %s)"
        try:
            cursor.execute(sql, param)
            conn.commit()
            print("插入t_news_lable成功:", param)
        except Exception as e:
            conn.rollback()
            print("exception:", e)
        # finally:
        #     conn.close()

    def select_label_id(self, conn, cursor, label):
        sql = 'SELECT Id FROM t_label WHERE Name = %s'
        id = None
        try:
            print("数据库参数lable：", label)
            cursor.execute(sql, label)
            result = cursor.fetchone()
            print("数据库打印result：", result)
            if result is None:
                param = []
                print("返回结果为空打印result:", result)
                id = str(datetime.now().timestamp())
                param.append(id)
                param.append(label)
                params = tuple(param)
                print("要插入t_label表的数据：", params)
                self.insert_into_t_label(conn, cursor, params)
            else:
                id = result[0]
        except Exception as e:
            cursor.rollback()
            print("execption:", e)
        finally:
            return id
            # conn.close()




