# db.py
# Handle MySQL database connection and queries
# Author: Adam Mitchell
# Email:  adamstuartmitchell@gmail.com
#
#
# mysql> SHOW columns from mfcc_training_data;
# +----------------------+-------------+------+-----+---------+-------+
# | Field                | Type        | Null | Key | Default | Extra |
# +----------------------+-------------+------+-----+---------+-------+
# | idmfcc_training_data | int(11)     | NO   | PRI | NULL    |       |
# | filename             | mediumtext  | YES  |     | NULL    |       |
# | filepath             | text        | YES  |     | NULL    |       |
# | num_value            | varchar(45) | YES  |     | NULL    |       |
# | word_value           | varchar(45) | YES  |     | NULL    |       |
# | vector               | longtext    | YES  |     | NULL    |       |
# | time_added           | datetime    | YES  |     | NULL    |       |
# +----------------------+-------------+------+-----+---------+-------+

import time
import MySQLdb as mysql


class DbHandler(object):
    def __init__(self, pw, user='root', host='localhost', db='mfcc_training_data'):
        self.cnxn = mysql.connect(host=host, user=user, passwd=pw, db=db)
        self.curs = self.cnxn.cursor()

        self.curs.execute('SHOW columns FROM mfcc_training_data;')

        for col in self.curs.fetchall():
            print col

        filename = "eleven-11-0-m.wav"
        filepath = "wavs/training"
        num_value = "11"
        word_value = "eleven"
        vector = "[ [1,1,1], [2,2,2], [3,3,3], [4,4,4], [5,5,5] ]"
        time_added = time.time()

        query = """INSERT INTO mfcc_training_data(filename,filepath,num_value,""" \
                """word_value,vector) VALUES ({0},{1},{2},{3},{4});""".format(filename, filepath, num_value, word_value, vector)

        print query
        self.curs.execute(query)


        self.cnxn.close()


pw = raw_input('Password: ')
db = DbHandler(pw)

'''
passwd = raw_input('Database password: ')
database = 'mfcc_training_data'


db = mysql.connect(host='localhost', user='root', passwd=passwd, db=database)
cu = db.cursor()
cu.execute('SHOW columns FROM mfcc_training_data;')
for col in cu.fetchall():
    print col
'''
