import MySQLdb
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import numpy as np
from pingouin import welch_anova
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm

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
    
    
    sql = "select * from seoul_center"
    center_df = pd.read_sql(sql,conn)
    center_df.columns = ['번호', '년도', '자치구명', '노인복지관', '경로당', '노인교실']
    
    sql = "select * from seoul_elder"
    elder_df = pd.read_sql(sql,conn)
    elder_df.columns = ['번호', '기간', '자치구명', '기초생활수급', '저소득', '일반']
    
    sql = "select * from seoul_people"
    people_df = pd.read_sql(sql,conn)
    people_df.columns = ['번호', '기간', '자치구명', '전체인구', '65세이상 노인']
    
    
    # T-test
    # 귀무 : 독거노인 수가 증가할수록 고독사하는 노인도 증가하지않는다.
    # 대립 : 독거노인 수가 증가할수록 고독사하는 노인도 증가한다.
    
    godok = godok_df.iloc[:, 1:]
    #print(godok_df)
    
    pdg = pd.DataFrame(people_df.groupby('기간')['65세이상 노인'].sum()).reset_index()
    print(pdg)
    
    print(stats.shapiro(godok['사망자수']))  # pvalue=0.190658 > 0.05 정규성 만족
    print(stats.shapiro(pdg['65세이상 노인']))  # pvalue=0.98256 > 0.05 정규성 만족
    
    #등분산성
    print(stats.levene(godok['사망자수'], pdg['65세이상 노인'])) # pvalue=0.00023 < 0.05 정규성 만족 x
    
    result = stats.ttest_ind(godok['사망자수'], pdg['65세이상 노인'], equal_var = False)
    print(result)
    
    plt.plot(godok['사망자수'])
    plt.plot(pdg['65세이상 노인'])
    plt.show()
    
    # pvalue=1.3960 < 0.05 귀무 기각. 대립선택
    
    
except Exception as e:
    print('err : ', e)