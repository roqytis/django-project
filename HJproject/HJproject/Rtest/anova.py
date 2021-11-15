
import MySQLdb
import pandas as pd 
import scipy.stats as stats
from pingouin import welch_anova
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm


import scipy.
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
 
    sql = "select * from seoul_elder"
    elder_df = pd.read_sql(sql,conn)
    elder_df.columns = ['번호', '기간', '자치구명', '기초생활수급', '저소득', '일반']
    
    sql = "select * from seoul_people"
    people_df = pd.read_sql(sql,conn)
    people_df.columns = ['번호', '기간', '자치구명', '전체인구', '65세이상 노인']
    
    elder_df['합'] = elder_df.iloc[:, 3:].sum(axis=1)
    #edg = pd.DataFrame(elder_df.groupby(['기간','자치구명'])['합'].sum()).reset_index()
    edg = pd.DataFrame(elder_df)
    print(edg)
    
    year = edg['기간']
    elder = edg['합']
    
    print(year)
    print(elder)
    
    gr1 = edg[edg['기간'] == 2011]['합']
    gr2 = edg[edg['기간'] == 2012]['합']
    gr3 = edg[edg['기간'] == 2013]['합']
    gr4 = edg[edg['기간'] == 2014]['합']
    gr5 = edg[edg['기간'] == 2015]['합']
    gr6 = edg[edg['기간'] == 2016]['합']
    gr7 = edg[edg['기간'] == 2017]['합']
    gr8 = edg[edg['기간'] == 2018]['합']
    gr9 = edg[edg['기간'] == 2019]['합']
    gr10 = edg[edg['기간'] == 2020]['합']
    
    print(np.mean(gr1), ' ', np.mean(gr2), ' ',np.mean(gr3), ' ',np.mean(gr4), ' ',
        np.mean(gr5), ' ',np.mean(gr6), ' ',np.mean(gr7), ' ',np.mean(gr8), ' ',
        np.mean(gr9), ' ',np.mean(gr10))
        
    # 시각화
    
    plt.boxplot([gr1, gr2, gr3, gr4, gr5,gr6,gr7,gr8,gr9,gr10])
    plt.show()
    
    f_sta, pv = stats.f_oneway(gr1, gr2, gr3, gr4,gr5,gr6,gr7,gr8,gr9,gr10)
    print('f_sta, pv : ', f_sta, pv)

    lmodel = ols('합 ~ C(기간)', data = edg).fit()
    result = anova_lm(lmodel, typ = 2)
    print(result)

    from statsmodels.stats.multicomp import pairwise_tukeyhsd
    tk = pairwise_tukeyhsd(edg.합, edg.기간, alpha = 0.05)
    print(tk)

    tk.plot_simultaneous()
    plt.show()

        
    #pdg1 = pd.DataFrame(people_df.groupby('기간')['전체인구'].sum()).reset_index()
    #pdg2 = pd.DataFrame(people_df.groupby('기간')['65세이상 노인'].sum()).reset_index()

    # print(pdg1)
    # print(pdg2)
    #
    # print(pdg1.describe()) # pdg1에 outlier(이상치) 발견
    # print(pdg2.describe())
    # print(edg.describe())
    #
    # print(stats.shapiro(pdg1['전체인구'])) # pvalue=0.81577 > 0.05 이므로 만족
    # print(stats.shapiro(pdg2['65세이상 노인'])) # pvalue=0.98256 > 0.05 이므로 만족
    # print(stats.shapiro(edg['합'])) # pvalue=0.9808 > 0.05 이므로 만족
    #
    # y1 = pdg1['전체인구']
    # y2 = pdg2['65세이상 노인']
    # y3 = edg['합']
    # print('등분산성 확인 : ', stats.levene(y1, y2, y3).pvalue) # 0.0020 < 0.05 이므로 만족x
    #
    #
    # dfmarge = pd.merge(pdg1,pdg2)
    # sdg = pd.merge(dfmarge,edg)
    # print(sdg)
    #
    # #print(sdg.columns)
    # #print(sdg.type())
    #
    # print(welch_anova(dv ='', between = '65세 이상 노인', data = sdg))
    # # 결론 :
    #
    #


   
    
    
except Exception as e:
    print('오류는 : ' , e) 
    conn.rollback()
finally:
    cursor.close()
    conn.close()    