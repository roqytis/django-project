# *서로 대응인 두 집단의 평균 차이 검정 (paired samples t test)
# 처리 이전과 처리 이후를 각각의 모집단으로 판단하여 동일한 관찰 대상으로부터 처리 이전과 처리 이후를 1 1 로 대응시킨 두 집단으로 부터
# 의 표본을 대응표본 (paired sample) 이라고 한다
# 대응인 두 집단의 평균 비교는 동일한 관찰 대상으로부터 처리 이전의 관찰과 이후의 관찰을 비교하여 영향을 미친 정도를 밝히는데 주로 사용
# 하고 있다 집단 간 비교가 아니므로 등분산 검정을 할 필요가 없다

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
  
    # 연도별로 고독자 사망자 수 데이터를 가져온다.
    sql = " select * from godok "
    cursor.execute(sql)
    # godok_df 에다가 pandas의 read_sql을 사용하여 DB연결후 고독자 사망자수 데이터를 가져온다.
    godok_df = pd.read_sql(sql, conn)
    # 고독자 사망자수의 컬럼명을 순서대로 지정해준다.
    godok_df.columns = ['번호', '년도', '사망자수']
    
    sql = "select * from seoul_elder"
    elder_df = pd.read_sql(sql,conn)
    elder_df.columns = ['번호', '기간', '자치구명', '기초생활수급', '저소득', '일반']
    
    sql = "select * from seoul_people"
    people_df = pd.read_sql(sql,conn)
    people_df.columns = ['번호', '기간', '자치구명', '전체인구', '65세이상 노인']

    sql = "select * from seoul_center"
    center_df = pd.read_sql(sql,conn)
    center_df.columns = ['번호', '년도', '자치구명', '노인복지관', '경로당', '노인교실']
       
    
    # T-test
    # 귀무 : 독거노인 수가 증가할수록 고독사하는 노인도 증가하지않는다.
    # 대립 : 독거노인 수가 증가할수록 고독사하는 노인도 증가한다.
    
    print(godok_df)
#        번호    년도  사망자수
#         0   1  2011    98
#         1   2  2012   107
#         2   3  2013   162....
    # 컬럼을 순서대로  0부터 시작하기때문에 0 1 2 3 순으로 숫자가 정해진다.
    # godok_df 의 컬럼을 자르기 위해  iloc [ : 데이터 다가져오고 , 1: 두번쨰 컬럼부터 가져온다]
    godok = godok_df.iloc[:, 1:]
    print(godok)
        #  년도  사망자수
        # 0  2011    98
        # 1  2012   107...
 

    
    # people_df 을 기간을 기준으로 groupby 함수를 통하여 65세이상의 데이터의 합을 구해준다. 
    # 아래와 같이 출력이 되도록!
    pdg = pd.DataFrame(people_df.groupby('기간')['65세이상 노인'].sum()).reset_index()
    #print(pdg)
    # 이런식으로 출력됨.
    #     기간  65세이상 노인
    # 0  2011   1049425
    # 1  2012   1110995
    # 2  2013   1167177
    # 3  2014   1221616
    # 4  2015   1267563
    # 5  2016   1300877
    # 6  2017   1365126
    # 7  2018   1416131
    # 8  2019   1485272
    # 9  2020   1568331
    
    # 정규성 확인
    print(stats.shapiro(godok['사망자수']))  # pvalue=0.190658 > 0.05 정규성 만족
    print(stats.shapiro(pdg['65세이상 노인']))  # pvalue=0.98256 > 0.05 정규성 만족
    
    #등분산성
    print(stats.levene(godok['사망자수'], pdg['65세이상 노인'])) # pvalue=0.00023 < 0.05 등분산성 만족 x
    
    # 등분산성은 만족하지 않지만 일단 검정을 계속 진행하였음.
    result = stats.ttest_ind(godok['사망자수'], pdg['65세이상 노인'], equal_var = False) # 등분산성 만족하지 않기에 equal_var = False 임.
    print(result)
    
    # plt.plot(godok['사망자수'])
    # plt.plot(pdg['65세이상 노인'])
    # plt.show()
    
    ######### 결 론 ###########
    # pvalue=1.3960699906962343e-09 < 0.05 귀무 기각. 대립선택
    
    
except Exception as e:
    print('err : ', e)