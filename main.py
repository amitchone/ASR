# main.py
# Interaction between separate elements
# Author: Adam Mitchell
# Email:  adamstuartmitchell@gmail.com

import getpass, numpy, os, sys, traceback, time
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


def read_vectors():
    sql = db.DbHandler(getpass.getpass())

    global start
    start = time.time()

    vectors = sql.execute_query("""SELECT vector, vector_shape, num_value FROM mfcc_training_data;""")

    for vector in vectors:
        shape = vector[1]
        num_value = vector[2]

        for char in [ '(', ')' ]:
            shape = shape.replace(char, '')

        shape = shape.split(',')

        yield numpy.fromstring(vector[0][1:-1], dtype=numpy.float64).reshape(int(shape[0]), int(shape[1])), num_value

    sql.destroy_cnxn()


if __name__ == '__main__':
    #write_training_data_to_db()

    train = mfcc.get_feature_vector('wavs/training/zero-test.wav')

    results = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: []}

    for template in read_vectors():
        results[int(template[1])].append(round(sum(mfcc.get_dtw(template[0], train)) / 12, 2))

    for key, val in results.iteritems():
        print key, sum(val) / 12

    print time.time() - start
