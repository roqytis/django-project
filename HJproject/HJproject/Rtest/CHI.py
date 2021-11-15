import MySQLdb
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

plt.rc('font', family = 'malgun gothic')

config = {

    'host':'127.0.0.1',
    'user':'root',
    'password':'123',
    'database':'elder',
    'port':3306,
    'charset':'utf8',
    'use_unicode':True

}

try:
    conn = MySQLdb.connect(**config)
    print(conn)
    
    cursor = conn.cursor()
  
    sql = " select * from godok "
    cursor.execute(sql)
    
    godok_df = pd.read_sql(sql, conn)
    godok_df.columns = ['번호', '년도', '사망자수']
    
    
    
    sql = "select * from seoul_elder"
    elder_df = pd.read_sql(sql,conn)
    elder_df.columns = ['번호', 'year', 'gu', 'a', 'b', 'c']
    
    sql = "select * from seoul_people"
    people_df = pd.read_sql(sql,conn)
    people_df.columns = ['번호', 'year', 'gu', 'all', 'elder']

# 귀무 : 전체인구가 증가함에따라 독거노인수가 증가하지않는다.
# 대립 : 전체인구가 증가함에따라 독거노인수가 증가한다.

# 전체인구를 비율로 만들어주는 함수 찾아야함.


    elder_df['sum'] = elder_df.iloc[:, 3:].sum(axis=1)       
    print(elder_df)
    
    
    #edg = pd.DataFrame(elder_df.groupby(['year','gu'])['sum'].sum()).reset_index()
    #pdg = pd.DataFrame(people_df.groupby(['year','gu'])['all'].sum()).reset_index()
    
    #print(edg)
    #print(pdg)

    #frame = pd.merge(edg,pdg)
    #print(frame.info())
    
    #print(frame.iloc[:, [2,3]].pct_change())

except Exception as e:
    print('오류는 : ' , e) 
    conn.rollback()
finally:
    cursor.close()
    conn.close()      
    