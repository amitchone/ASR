# main.py
# Interaction between separate elements
# Author: Adam Mitchell
# Email:  adamstuartmitchell@gmail.com

import getpass, os, traceback
import mfcc, db


def write_training_data_to_db():
    sql = db.DbHandler(getpass.getpass())

    for idx, f in enumerate(os.listdir('{0}/wavs/training'.format(os.getcwd()))):
        print idx, f

        try:
            info = f.split('-')

            filename = f
            filepath = '{0}/wavs/training'.format(os.getcwd())
            num_value = info[1]
            word_value = info[0]
            vector = mfcc.get_feature_vector('wavs/training/{0}'.format(filename))
            vector_blob = numpy.getbuffer(mfcc.get_feature_vector('wavs/training/{0}'.format(filename)), dtype=np.float32)
            sex = info[-1][0]
            vector_shape = vector.shape

            query = sql.construct_write_query('mfcc_training_data',
                                              int(idx),
                                              str(filename),
                                              str(filepath),
                                              int(num_value),
                                              str(word_value),
                                              str(vector_blob),
                                              str(sex),
                                              str(vector_shape)
                                             )

            sql.execute_query(query)
        except:
            print f, traceback.format_exc()

    sql.destroy_cnxn()


if __name__ == '__main__':
    write_training_data_to_db()
