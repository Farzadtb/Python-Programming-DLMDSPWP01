import Best_func
import pandas as pd



train=pd.read_csv('train.csv')
test=pd.read_csv('test.csv')
ideal=pd.read_csv('ideal.csv')

reg_obj=Best_func.Regression('test',train,test,ideal)


result= reg_obj.regression()

#reg_obj.visualize()

reg_obj.datavis()



