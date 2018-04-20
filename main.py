# main.py
# Interaction between separate elements
# Author: Adam Mitchell
# Email:  adamstuartmitchell@gmail.com

import getpass, numpy, os, sys, traceback, time
import mfcc, db


class FeatureCompare(object):
    def __init__(self):
        pass


    def write_training_data_to_db(self):
        self.connect_db()

        for idx, f in enumerate(os.listdir('{0}/wavs/training'.format(os.getcwd()))):
            print idx, f

            try:
                info = f.split('-')

                if f != '.DS_Store' and f!= 'in_db_sd_high_spl' and f!= 'in_db_sd_low_spl':
                    filename = f
                    filepath = '{0}/wavs/training'.format(os.getcwd())
                    num_value = info[1]
                    word_value = info[0]
                    vector = mfcc.get_feature_vector('wavs/training/{0}'.format(filename))
                    vector_blob = vector.tostring()
                    sex = info[-1][0]
                    vector_shape = vector.shape

                    query = self.sql.construct_write_query('sd_high_spl',
                                                           int(idx),
                                                           str(filename),
                                                           str(filepath),
                                                           int(num_value),
                                                           str(word_value),
                                                           str(sex),
                                                           str(vector_shape)
                                                          )

                    self.sql.execute_query(query, vector_blob)
            except:
                print f, traceback.format_exc()
                sys.exit(1)

        self.disconnect_db()


    def read_vectors(self):
        #self.connect_db()

        for vector in self.sql.execute_query("""SELECT vector, vector_shape, num_value FROM sd_high_spl;"""):
            shape = vector[1]
            num_value = vector[2]

            for char in [ '(', ')' ]:
                shape = shape.replace(char, '')

            shape = shape.split(',')

            yield numpy.fromstring(vector[0][1:-1], dtype=numpy.float64).reshape(int(shape[0]), int(shape[1])), num_value

        #self.disconnect_db()

    def get_comparison(self, f):
        train = mfcc.get_feature_vector(f)

        results = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: []}

        for template in self.read_vectors():
            results[int(template[1])].append(round(sum(mfcc.get_dtw(template[0], train)) / 12, 2))

        numbers = [ (sum(i) / len(i)) for i in results.itervalues() ] # mean average

        for key, val in results.iteritems():
            print key, sum(val) / len(val)

        for idx, i in enumerate(numbers):
            if min(numbers) == i:
                return idx


    def connect_db(self):
        if not 'sql' in self.__dict__:
            self.sql = db.DbHandler('focusRITE339')


    def disconnect_db(self):
        if 'sql' in self.__dict__:
            self.sql.destroy_cnxn()


if __name__ == '__main__':
    #start = time.time()
    fc = FeatureCompare()
    #fc.write_training_data_to_db()

    fc.connect_db()
    '''
    res = fc.get_comparison('wavs/training/5hspl.wav')
    print 'You said: {0}'.format(res)
    '''
    tally = list()
    for i in range(0, 50):
        #start = time.time()
        res = fc.get_comparison('wavs/training/{0}.wav'.format(i))
        if i < 10:
            if res == i:
                print '{0}: Correct!'.format(i)
                tally.append(i)
            else:
                print '{0}: Incorrect!'.format(i)
        else:
            if str(i)[1] == str(res):
                print '{0}: Correct!'.format(i)
                tally.append(i)
            else:
                print '{0}: Incorrect!'.format(i)
        #print time.time() - start


    print '{0}/50 Correct'.format(len(tally))

    #print 'Took: {0}s'.format(time.time() - start)

    fc.disconnect_db()
    #print 'Took: {0}s'.format(time.time() - start)
