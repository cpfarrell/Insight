import mysql.connector
import sys
from mysql.connector import errorcode

class DbAccess(object):
    """Access database
    """
    def __init__(self, db_name, usr='', pwd=None):
        self.db_name = db_name
        self.db_url = "localhost"
        self.connect(usr, pwd)
        self.cursor = self.cnx.cursor()

    def connect(self, usr, pwd=None):
        """Try to connect to DB
        """
        try:
            self.cnx = mysql.connector.connect(user=usr, password=pwd, 
                database=self.db_name, host=self.db_url)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exists")
            else:
                print(err)
            sys.exit(1)

    def close(self):
        """Disconnect from DB
        """
        self.cursor.close()
        self.cnx.close()

    def commit(self):
        self.cnx.commit()
