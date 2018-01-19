# db.py
# Handle MySQL database connection and queries
# Author: Adam Mitchell
# Email:  adamstuartmitchell@gmail.com
#
#
# mysql> SHOW columns FROM mfcc_training_data;
# +----------------------+-------------+------+-----+---------+-------+
# | Field                | Type        | Null | Key | Default | Extra |
# +----------------------+-------------+------+-----+---------+-------+
# | idmfcc_training_data | int(5)      | NO   | PRI | NULL    |       |
# | filename             | mediumtext  | YES  |     | NULL    |       |
# | filepath             | mediumtext  | YES  |     | NULL    |       |
# | num_value            | varchar(45) | YES  |     | NULL    |       |
# | word_value           | varchar(45) | YES  |     | NULL    |       |
# | vector               | longtext    | YES  |     | NULL    |       |
# | sex                  | text(2)     | YES  |     | NULL    |       |
# +----------------------+-------------+------+-----+---------+-------+

import numpy, os
import MySQLdb as mysql


class DbHandler(object):
    def __init__(self, pw, user='root', host='localhost', db='mfcc_training_data'):
        self.cnxn = mysql.connect(host=host, user=user, passwd=pw, db=db)
        self.curs = self.cnxn.cursor()

    def construct_write_query(self, table, id, filename, filepath, num_value, word_value, vector, sex):
        self.query = """INSERT INTO {0}(id,filename,filepath,""" \
                     """num_value,word_value,vector,sex) VALUES""" \
                     """("{0}","{1}","{2}","{3}","{4}","{5}","{6}")""".format(table, id,
                                                                              filename, filepath,
                                                                              num_value, word_value,
                                                                              vector, sex
                                                                             )

    def execute_query(self, query):
        try:
            self.curs.execute(query)
            self.cnxn.commit()
        except:
            self.cnxn.rollback()

    def destroy_cnxn(self):
        self.cnxn.close()
