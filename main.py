# main.py
# Interaction between separate elements
# Author: Adam Mitchell
# Email:  adamstuartmitchell@gmail.com

import MySQLdb as mysql
import getpass, numpy, os, sys, traceback
import mfcc, db


def write_training_data_to_db():
    sql = db.DbHandler(getpass.getpass())

    for idx, f in enumerate(os.listdir('{0}/wavs/training'.format(os.getcwd()))):
        print idx, f

        try:
            info = f.split('-')

            if f != '.DS_Store' and f!= 'in_db':
                filename = f
                filepath = '{0}/wavs/training'.format(os.getcwd())
                num_value = info[1]
                word_value = info[0]
                vector = mfcc.get_feature_vector('wavs/training/{0}'.format(filename))
                vector_blob = vector.tostring()
                sex = info[-1][0]
                vector_shape = vector.shape

                query = sql.construct_write_query('mfcc_training_data',
                                                  int(idx),
                                                  str(filename),
                                                  str(filepath),
                                                  int(num_value),
                                                  str(word_value),
                                                  str(sex),
                                                  str(vector_shape)
                                                 )

                sql.execute_query(query, vector_blob)
        except:
            print f, traceback.format_exc()
            sys.exit(1)

    sql.destroy_cnxn()


def read_vector():
    sql = db.DbHandler(getpass.getpass())

    v = mfcc.get_feature_vector('wavs/training/in_db/zero-0-0-m.wav')
    print v.shape

    for b in sql.execute_query("""SELECT vector, vector_shape FROM mfcc_training_data WHERE filename LIKE 'zero-0-0-m.wav'"""):
        shape = b[1]
        for char in [ '(', ')' ]:
            shape = shape.replace(char, '')
        shape = shape.split(',')
        d = numpy.fromstring(b[0][1:-1], dtype=numpy.float64).reshape(int(shape[0]), int(shape[1]))

        print d.shape



if __name__ == '__main__':
    #write_training_data_to_db()
    read_vector()
