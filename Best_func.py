from sqlalchemy import create_engine,Column,MetaData,Table,Float
from sqlalchemy import types
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import pandas as pd
from unittest import TestCase
import os

class Sql:


    def __init__(self,db_name) : 
       self.engine=create_engine('sqlite:///%s.db'% db_name,echo=False)
       
    
      
         
    def savedata(self,datasave,dataname):
        row_b=None
        try:
             row_b=datasave.to_sql(con=self.engine, name=dataname, if_exists='replace', index=False)
             return dataname+' dataframes replaced in db'
        except:
             if row_b==None  :
               print(dataname+' dataframes did not replace in db')
               return dataname+' dataframes did not replace in db'
            
      
    def readdata(self,tablename):
        result=None
        try:
             result=pd.read_sql('SELECT * FROM %s' % tablename,con=self.engine)

             return result

        except:

            if result==None  :
               print(tablename+' dataframes did not read from db')

               return tablename+' dataframes did not read from db'
    



class Regression(Sql):

    def __init__(self,db_name,train,test,ideal) -> None:
        self.train=train
        self.test=test
        self.ideal=ideal
        self.db_name=db_name
        Sql.__init__(self,db_name)
        
        

    def regression(self):
        

        tr=self.train.drop('x',axis=1)
        id=self.ideal.drop('x',axis=1)
        min_result={}

        for i in tr.items():
            r={}
            for j in id.items():
                
                mse= mean_squared_error(i[1],j[1])
                
                r[j[0]]=mse
        
        
            min_result[i[0]]=(min(r, key=r.get),min(r.values())) 
        id_list=['x']+[i[0] for i in list(min_result.values())]
        self.ideal= self.ideal[id_list]
        
        
        testdev= pd.merge(self.test, self.train, on='x', how='inner')
        
        
        # deviation between y1 train and equivalent y from ideal
        maxdev=[]
        temp=0
        for col in range(1,5):
            for row in range(0,len(self.train)):
                if abs(self.train.iloc[row,col]- self.ideal.iloc[row,col]) > temp:
                    temp=abs(self.train.iloc[row,col]- self.ideal.iloc[row,col])
                    
            maxdev.append(temp)
        
        
        lists=[]
        dev=0
        for col in range(2,6):
            for row in range(0,len(testdev)):
                if all(abs(testdev.iloc[row,1]- testdev.iloc[row,col])<maxdev):
                    dev= abs(testdev.iloc[row,1]- testdev.iloc[row,col])
                    lists.append((self.test.iloc[row]['x'],self.test.iloc[row]['y'],dev,maxdev)) #save the row to list
                    
                    
            
        savedtest= pd.DataFrame(data=lists, columns=['X','Y','dev','maxdev'])

        #save data to database
        Sql.savedata(self,self.train,self.db_name)
        Sql.savedata(self,self.ideal,self.db_name)
        savedtest=savedtest.applymap(str)
        s1=Sql.savedata(self,savedtest,self.db_name)

        return s1
        
        
        
        


    def visualize(self):

        train=Sql.readdata(self,'train')
        ideal=Sql.readdata(self,'ideal')
        
        for i in range(1,5):
            
            plt.plot(train['x'],train.iloc[:,i],label=' %s_train'%train.iloc[:,i].name)
            plt.plot(ideal['x'],ideal.iloc[:,i],label='%s_ideal'%ideal.iloc[:,i].name)

            plt.legend()
            plt.xlabel('x')
            plt.ylabel('y2')
            plt.show()


    def datavis(self):

        
        ideal=Sql.readdata(self,'train')
        
        for i in range(1,5):
            
            
            plt.plot(ideal['x'],ideal.iloc[:,i],label='%s_train'%ideal.iloc[:,i].name)

            plt.legend()
            plt.show()
        



        








    