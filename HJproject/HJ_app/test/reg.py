"""
선형 회귀란 무엇인가 ( linear regression model)
이때 우리가 찾아낼 수 있는 가장 직관적이고 간단한 모델은 선(line)이다. 그래서 데이터를 놓고 그걸 가장 잘 설명할 수 있는 선을 찾는 분석하는 방법을 
선형 회귀(Linear Regression) 분석이라 부른다.
예를 들어 키와 몸무게 데이터를 펼쳐 놓고 그것들을 가장 잘 설명할 수 있는 선을 하나 잘 그어놓게 되면,
 특정 인의 키를 바탕으로 몸무게를 예측할 수 있다.
 
"""

import MySQLdb
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import statsmodels.formula.api as smf

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
    
    # godok_df에다가 pandas를 통하여 읽어온 godok 테이블의 데이터를 저장한다.
    godok_df = pd.read_sql(sql, conn)
    godok_df.columns = ['번호', '년도', '사망자수']
 
    sql = "select * from seoul_elder"
    # elder_df 에다가 pandas를 통하여 읽어온 seoul_elder 테이블의 데이터를 저장한다.
    elder_df = pd.read_sql(sql,conn)
    elder_df.columns = ['번호', '년도', '자치구명', '기초생활수급', '저소득', '일반']
    
    sql = "select * from seoul_people"
    # people_df 에다가 pandas를 통하여 읽어온 seoul_people 테이블의 데이터를 저장한다.
    people_df = pd.read_sql(sql,conn)
    people_df.columns = ['번호', '년도', '자치구명', '전체인구', '65세이상 노인']
    
    # 합은 elder_df에 있는 독거노인의 기준이 나누어져있는 컬럼인  ('기초생활수급', '저소득', '일반') 의 합을 구한 데이터.
    # elder_df['합'] 이란 컬럼을 추가해준다
    # elder_df iloc[: 모든데이터 , 3: 컬럼의 3번째부터 기초생활수급,저소득,일반] 을 다 더한 값 axis는 1은 행을 나타내므로 행을 다 더한값으로 이해할 수 있다.
    elder_df['합'] = elder_df.iloc[:, 3:].sum(axis=1)
    # edg 에다가 elder_df를 연도별 독거노인의 합을 나타내기 위해 groupby() 함수를 통하여 기간별로 나누어주고 구별로 나누어져있는 부분은 .sum()을 통하여 합한다.
    edg = pd.DataFrame(elder_df.groupby(['년도'])['합'].sum()).reset_index()
    
    # godok_df 의 컬럼을 자르기 위해  iloc [ : 데이터 다가져오고 , 1: 두번쨰 컬럼부터 가져온다]
    godok_df = godok_df.iloc[:, 1:]
    
    # 데이터 확인을 위한 코드임.
    # print(godok_df)
    # print(edg)
    
    # frame 에다가 merge를 통하여 godok__df와 egd의 데이터를 년도를 기준으로 합친다.
    frame = pd.merge(godok_df, edg, how='inner', on=None)
    # print(frame)
    #      년도  사망자수       합
    # 0  2011    98  211226
    # 1  2012   107  238551
    # 2  2013   162  253302
    # 3  2014   188  273190
    # 4  2015   219  281068
    # 5  2016   243  288599
    # 6  2017   287  303824
    # 7  2018   311  332512
    # 8  2019   346  343567
    # 9  2020   579  366134



    # 공분산
    print(frame.cov())
    #               년도          사망자수          합
    # 년도         9.166667  3.926667e+02  1.458204e+05
    # 사망자수     392.666667  1.983756e+04  6.357394e+06
    # 합     145820.388889  6.357394e+06  2.357905e+09
    
    # 상관계수
    print(frame.corr())
    #          년도      사망자수       합
    # 년도    1.000000  0.920819  0.991858
    # 사망자수  0.920819  1.000000  0.929548
    # 합     0.991858  0.929548  1.000000
    
    # linear regression model
    model1 = smf.ols(formula = "사망자수 ~ 년도", data = frame).fit()
    print(model1.summary())
    
    '''
                            OLS Regression Results                            
    ==============================================================================
    Dep. Variable:                   사망자수   R-squared:                       0.848
    Model:                            OLS   Adj. R-squared:                  0.829
    Method:                 Least Squares   F-statistic:                     44.60
    Date:                Fri, 05 Nov 2021   Prob (F-statistic):           0.000156
    Time:                        22:06:24   Log-Likelihood:                -53.723
    No. Observations:                  10   AIC:                             111.4
    Df Residuals:                       8   BIC:                             112.1
    Df Model:                           1                                         
    Covariance Type:            nonrobust                                         
    ==============================================================================
                     coef    std err          t      P>|t|      [0.025      0.975]
    ------------------------------------------------------------------------------
    Intercept  -8.608e+04   1.29e+04     -6.659      0.000   -1.16e+05   -5.63e+04
    년도            42.8364      6.414      6.678      0.000      28.045      57.628
    ==============================================================================
    Omnibus:                        9.685   Durbin-Watson:                   1.423
    Prob(Omnibus):                  0.008   Jarque-Bera (JB):                4.120
    Skew:                           1.398   Prob(JB):                        0.127
    Kurtosis:                       4.439   Cond. No.                     1.41e+06
    ==============================================================================
    '''
    print('결정계수(설명력) :', model1.rsquared) # 0.84790 독립변수가 종속변수의 분산을 84.7..% 정도이다. 
    print('p-value(유의확률) : ', model1.pvalues[1]) #0.0001561 < 0.05
    
    pred1 = model1.predict() 
    print('예측 값 : ' , pred1[:5]) 
    print('실제 값 : ' , frame.사망자수[:5].values)
    
    # 새로운 년도를 입력하여 , 해당 년도의 사망년도를 증가를 기준으로 예측.
    new_year = pd.DataFrame({'년도':[2023]})
    new_pred = model1.predict(new_year)
    print('입력값으로 사망자 예측 : \n', new_pred[0])
    
    # 시각화
    plt.scatter(x = frame.년도, y = frame.사망자수)
    plt.plot(frame.년도, pred1, 'r')
    plt.show()
    
    print('---' * 30)
    
    # 기간별로 독거노인의 증가수를 모델로 만듬.
    model2 = smf.ols(formula = "합 ~ 년도", data = frame).fit()
    print(model2.summary())
    '''
                            OLS Regression Results                            
    ==============================================================================
    Dep. Variable:                      합   R-squared:                       0.984
    Model:                            OLS   Adj. R-squared:                  0.982
    Method:                 Least Squares   F-statistic:                     485.3
    Date:                Fri, 05 Nov 2021   Prob (F-statistic):           1.90e-08
    Time:                        22:09:30   Log-Likelihood:                -100.96
    No. Observations:                  10   AIC:                             205.9
    Df Residuals:                       8   BIC:                             206.5
    Df Model:                           1                                         
    Covariance Type:            nonrobust                                         
    ==============================================================================
                     coef    std err          t      P>|t|      [0.025      0.975]
    ------------------------------------------------------------------------------
    Intercept  -3.177e+07   1.46e+06    -21.830      0.000   -3.51e+07   -2.84e+07
    년도          1.591e+04    722.128     22.029      0.000    1.42e+04    1.76e+04
    ==============================================================================
    Omnibus:                        1.946   Durbin-Watson:                   1.493
    Prob(Omnibus):                  0.378   Jarque-Bera (JB):                0.989
    Skew:                          -0.400   Prob(JB):                        0.610
    Kurtosis:                       1.683   Cond. No.                     1.41e+06
    ==============================================================================
    '''
    
    print('결정계수(설명력) :', model2.rsquared) #  0.983781
    print('p-value(유의확률) : ', model2.pvalues[1]) # 1.904186773288583e-08 > 0.05
    
    pred2 = model2.predict()
    print('예측 값 : ' , pred2[:5])
    print('실제 값 : ' , frame.합[:5].values)
    
    # 새로운 연도를 입력하여 해당 연도의 독거노인의 수를 예측한다.
    new_year2 = pd.DataFrame({'년도':[2023]})
    new_pred2 = model2.predict(new_year2)
    print('입력값으로 n년도 독거노인 수 예측 : \n', new_pred2[0])
 

    plt.scatter(x = frame.년도, y = frame.합)
    plt.plot(frame.년도, pred2, 'r')
    plt.show()
   

    
    # sns.pairplot(frame)    
    # plt.show()
    
    
except Exception as e:
    print('오류는 : ' , e) 
    conn.rollback()
finally:
    cursor.close()
    conn.close()