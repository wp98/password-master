import psycopg2


class Database:
    def __init__(self):
        self.database = psycopg2.connect(
            host='localhost',
            database='password_master',
            user='postgres',
            password='123'
        )
        self.cur = self.database.cursor()

    def send_query(self, query):
        try:
            self.cur.execute(query)
            requested_query = self.cur.fetchall()
            return requested_query
        except Exception as query_error:
            return query_error

    def add_user(self, user_name, password):
        add_query = """ INSERT INTO users (user_name, password) VALUES ('{}', '{}')""".format(user_name, password)
        user_pass_holder = """CREATE TABLE {}(pass_id SERIAL NOT NULL, 
                                pass_name VARCHAR(64) NOT NULL UNIQUE,
                                pass VARCHAR(64) NOT NULL
        )""".format(user_name)
        try:
            self.cur.execute(add_query)
            self.cur.execute(user_pass_holder)
            self.database.commit()
            return True
        except psycopg2.Error as register_error:
            self.database.rollback()
            return register_error

    def insert_pass(self, user_name, pass_name, password):
        insert_query = """INSERT INTO {}(pass_name, pass) VALUES('{}', '{}')""".format(user_name, pass_name, password)
        try:
            self.cur.execute(insert_query)
            self.database.commit()
            return True
        except psycopg2.Error:
            return False

    def delete_pass(self, user_name, pass_id):
        max_id = self.send_query("""SELECT MAX(pass_id) FROM {}""".format(user_name))
        if max_id[0][0] is not None:
            if int(pass_id) <= 0 or int(pass_id) > max_id[0][0]:
                return False
        elif max_id[0][0] is None:
            return False
        delete_query = """DELETE FROM {} WHERE pass_id={}""".format(user_name, pass_id)
        self.cur.execute(delete_query)
        self.database.commit()
        return True
