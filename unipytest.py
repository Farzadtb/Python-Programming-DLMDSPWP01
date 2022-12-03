import Best_func
import pandas as pd
import unittest


class Test(unittest.TestCase):


    def test_sql_error(self):
        self.train=pd.read_csv('Test_train.csv')
        self.test=pd.read_csv('Test_test.csv')
        self.ideal=pd.read_csv('Test_ideal.csv')
        self.db_name='unitest'
        Best_func.Regression.__init__(self,self.db_name,self.train,self.test,self.ideal)

        self.result=Best_func.Regression.regression(self)
        # case 1: if the regression process faces an error so the sql will send error for data saving
        message = "Test value is true."
        self.assertTrue(self.result==self.db_name+' dataframes replaced in db',message)
        


if __name__ == '__main__':
    unittest.main()


