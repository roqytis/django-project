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
    godok_df = pd.read_sql(sql, conn)
    godok_df.columns = ['번호', '년도', '사망자수']
 
    sql = "select * from seoul_elder"
    elder_df = pd.read_sql(sql,conn)
    elder_df.columns = ['번호', '년도', '자치구명', '기초생활수급', '저소득', '일반']
    
    sql = "select * from seoul_people"
    people_df = pd.read_sql(sql,conn)
    people_df.columns = ['번호', '년도', '자치구명', '전체인구', '65세이상 노인']
    
    elder_df['합'] = elder_df.iloc[:, 3:].sum(axis=1)
    edg = pd.DataFrame(elder_df.groupby(['년도'])['합'].sum()).reset_index()
    godok_df = godok_df.iloc[:, 1:]
    
    # edg2 = pd.DataFrame(edg.groupby(['년도']).sum()['합'])
    
    print(godok_df)
    print(edg)
    frame = pd.merge(godok_df, edg, how='inner', on=None)
    print(frame)

    # 공분산
    print(frame.cov())
    
    # 상관계수
    print(frame.corr())
    
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
    pred1 = model1.predict()
    print(pred1)
    # 시각화
    plt.scatter(x = frame.년도, y = frame.사망자수)
    plt.plot(frame.년도, pred1, 'r')
    plt.show()
    
    print('---' * 30)
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
    
    pred2 = model2.predict()
    print(pred2)
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