 # 분산분석(ANOVA) : 종속변수의 변화폭이(분산)이 독립변수에 의해 기인 하는지를 파악하는 것
# 집단 간 분산이 집단 내 분산보다 충분히 큰 것인가를 파악,
#분산이 큰집단 / 분산이 작은집단, between variance/ within variance => f


# 세 개 이상의 모집단에 대한 가설검정 – 분산분석
# ‘분산분석’이라는 용어는 분산이 발생한 과정을 분석하여 요인에 의한 분산과 요인을 통해 나누어진 각 집단 내의 분산으로 나누고 
# 요인에 의한 분산이 의미 있는 크기를 크기를 가지는지를 검정하는 것을 의미한다.
# 세 집단 이상의 평균비교에서는 독립인 두 집단의 평균 비교를 반복하여 실시할 경우에 제1종 오류가 증가하게 되어 문제가 발생한다.
# 이를 해결하기 위해 Fisher가 개발한 분산분석(ANOVA, ANalysis Of Variance)을 이용하게 된다.

# 분산 분석 ANOVA는 전체 그룹 간의 평균값 차이가 의미가 있는지만 판단해 줌.
# 그룹 간의 평균의 차이를 구체적으로 알고 싶은 경우에는 사후분석(POST HOC TEST)을 함

# 귀무 : 2011~2020년 각 연도마다 자치구별로 독거노인의 수의 평균에 대한 차이가 없다.
# 대립 : 2011~2020년 각 연도마다 자치구별로 독거노인의 수의 평균에 대한 차이가 있다.

import MySQLdb
import pandas as pd 
import scipy.stats as stats
from pingouin import welch_anova
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm


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
    # 서울시 자치구별 고독사 사망자수 가져오기.
    sql = " select * from godok "
    cursor.execute(sql)
    
    # 서울시 자치구별 노인 DB 가져오기.
    sql = "select * from seoul_elder"
    # pandas 의 read_sql을 통하여 서울시 자치구별 독거노인 데이터를 가져와 elder_df에 저장을 한다.
    elder_df = pd.read_sql(sql,conn)
    # elder_df의 컬럼명을 순서대로 아래와 같이 저장한다.
    elder_df.columns = ['번호', '기간', '자치구명', '기초생활수급', '저소득', '일반']
    
    # 서울시 자치구별 전체인구 및 65세 이상 노인 DB,
    sql = "select * from seoul_people"
    # 위와 동일하게 서울시 자치구별 전체인구,65세이상노인 데이터를 가져와  people_df 에 저장한다.
    people_df = pd.read_sql(sql,conn)
    # people_df의 컬럼명을 순서대로 아래와 같이 저장한다.
    people_df.columns = ['번호', '기간', '자치구명', '전체인구', '65세이상 노인']
    
    # '독거노인' 이라는 새로운 열(컬럼) 을 만듦. '기초생활수급 + 저소득 + 일반'을 다 더한 데이터임.
    #  elder_df의 전체 행의 , 3: 의 의미는 4번쨰 컬럼 부터 합친다 (행의 값들을 )  컬럼을 기준으로 0부터 시작하기에 값이 3 임. 
    elder_df['독거노인'] = elder_df.iloc[:, 3:].sum(axis=1)
    #edg = pd.DataFrame(elder_df.groupby(['기간','자치구명'])['합'].sum()).reset_index()
    
    # elder_df의 값들을 데이터프레임으로 edg에 저장한다.
    edg = pd.DataFrame(elder_df)
    print(edg) 
    # print 결과
    #      번호    기간 자치구명  기초생활수급   저소득    일반   독거노인
    # 0      1  2011  종로구     911     268    4686   5865
    # 1      2  2011   중구    1002     188    3720   4910
    # 2      3  2011  용산구    1371     352    5992   7715
    # 3      4  2011  성동구    1168     432    5363   6963
    # 4      5  2011  광진구    1178     162    5534   6874
    
    
    # edg에서 '기간' column만 가져와서 year 변수에 저장
    year = edg['기간']
    # edg에서 '독거노인' column만 가져와서 elder 변수에 저장
    elder = edg['독거노인']
    
    print(year)
    # 0      2011
    # 1      2011
    # 2      2011
    # 3      2011
    # 4      2011
    #        ...
 
    print(elder)
    # 0       5865
    # 1       4910
    # 2       7715
    # 3       6963
    # 4       6874
    #        ...  
    
    # 해당 년도에 기간이 일치하는 2011년의 독거노인(기초생활수급자, 저소득, 일반 의 합) 데이터를 가져온다 
    gr1 = edg[edg['기간'] == 2011]['독거노인']
    # print(gr1)  # 기간이 2011년도인 구별로 독거노인 데이터를 가져옴.
    gr2 = edg[edg['기간'] == 2012]['독거노인']   
    gr3 = edg[edg['기간'] == 2013]['독거노인']
    gr4 = edg[edg['기간'] == 2014]['독거노인']
    gr5 = edg[edg['기간'] == 2015]['독거노인']
    gr6 = edg[edg['기간'] == 2016]['독거노인']
    gr7 = edg[edg['기간'] == 2017]['독거노인']
    gr8 = edg[edg['기간'] == 2018]['독거노인']
    gr9 = edg[edg['기간'] == 2019]['독거노인']
    gr10 = edg[edg['기간'] == 2020]['독거노인']
    
    
    # 평균을 구하는 함수. np.mean()을 통하여 2011년도부터 20년도까지의 독거노인의 평균을 구한다.
    print(np.mean(gr1), ' ', np.mean(gr2), ' ',np.mean(gr3), ' ',np.mean(gr4), ' ',
        np.mean(gr5), ' ',np.mean(gr6), ' ',np.mean(gr7), ' ',np.mean(gr8), ' ',
        np.mean(gr9), ' ',np.mean(gr10))
    
    # 시각화
    
    plt.boxplot([gr1, gr2, gr3, gr4, gr5,gr6,gr7,gr8,gr9,gr10]) # boxplot으로 데이터를 보여주겠다..
    # 그래프 보여주기.
    plt.show()
    
    # anova(분산분석) 중 일원분산분석 방법을 사용함.
    f_sta, pv = stats.f_oneway(gr1, gr2, gr3, gr4,gr5,gr6,gr7,gr8,gr9,gr10) # f통계량과, p-value 얻기 위한 코드임.
    print('f_sta, pv : ', f_sta, pv)
    # f통계량은 : 9.829209864267   <- 이 값이 클수록 집단간 평균 차가 존재한다는 것을 알 수 있음.
    # p-value : 8.457752865997506e-13 < 0.05 이므로 귀무가설을 기각하고 대립가설을 받아들임.
    
    # 위 내용이 이해안갈 시 참고 바람. : https://blog.naver.com/hlkim96/220768419177
    
    
    # 모델을 만듦.
    # 독거노인 : 종속변수, 기간 : 독립변수. C <- 범주형일 때 표기를 해줘야 함.
    # 독립변수 : 혼자 있을 수 있는 값 어디에 영향을 받지 않는 값
    # 종속변수 : 독립변수에 의하여 영향을 받는 값
    # ex) 차의 무게가 차의 연비에 영향
    # 독립 : 차의 무게
    # 종속 : 차의 연비
    # 차의 무게가 1t 증가할 때마다 연비가 약 5.3 감소한다.
    # data = edg <- edg는 우리가 만든 DataFrame
    lmodel = ols('독거노인 ~ C(기간)', data = edg).fit()
    
    # 결과출력
    result = anova_lm(lmodel, typ = 2) 
    print(result)
    
    # 사후검정: 그룹간의 평균 차이가 의미가 있는지 확인
    from statsmodels.stats.multicomp import pairwise_tukeyhsd  # 비교 대상 표본 수가 동일한 경우 사용. 우리 데이터는 년도별 자치구 수가 동일함
    tk = pairwise_tukeyhsd(edg.독거노인, edg.기간, alpha = 0.05)  # alpha <- 5%의 유의수준 허용
    print(tk)
    
    # 시각화
    tk.plot_simultaneous()
    plt.show()
    
    ######################################################################################
    # 해당의 아래부분은 전체인구, 고령화 노인 , 독거노인을 비교한다.
    #####################################################################################
 
    # 귀무 : 기간을 기준으로 전체인구, 고령화 노인(65세 이상), 독거노인 의 평균의 차이가 없다 
    # 대립 : 기간을 기준으로 전체인구, 고령화 노인(65세 이상), 독거노인 의 평균의 차이가 있다. 
    
    # people_df를 기간을 기준으로 구별로 나누어져있는 전체인구 의 데이터를 합치고 인덱스로 새롭게주고 데이터프레임화 시킨다음 pdg1 을 저장시킨다.
    pdg1 = pd.DataFrame(people_df.groupby('기간')['전체인구'].sum()).reset_index()
    # people_df를 기간을 기준으로 구별로 나누어져있는 65세이상 노인의 데이터를 합치고 인덱스를 새롭게주어 데이터프레임화 시키고 pdg2에 저장 시킴.
    pdg2 = pd.DataFrame(people_df.groupby('기간')['65세이상 노인'].sum()).reset_index()
    
    #print(pdg1)
    #print(pdg2)
    
    print(pdg1.describe()) 
    #            기간          전체인구
    # count    10.00000  1.000000e+01
    # mean   2015.50000  1.023263e+07
    # std       3.02765  2.047487e+05
    # min    2011.00000  9.911088e+06        # pdg1에 outlier(이상치) 발견
    # 25%    2013.25000  1.006835e+07
    # 50%    2015.50000  1.025060e+07
    # 75%    2017.75000  1.038344e+07
    # max    2020.00000  1.052877e+07
    print(pdg2.describe())
    #             기간      65세이상 노인
    # count    10.00000  1.000000e+01
    # mean   2015.50000  1.295251e+06
    # std       3.02765  1.657237e+05
    # min    2011.00000  1.049425e+06
    # 25%    2013.25000  1.180787e+06
    # 50%    2015.50000  1.284220e+06
    # 75%    2017.75000  1.403380e+06
    # max    2020.00000  1.568331e+06
    print(edg.describe())
    #             번호           기간  ...            일반          독거노인
    # count  250.000000   250.000000  ...    250.000000    250.000000
    # mean   125.500000  2015.500000  ...   8449.460000  11567.892000
    # std     72.312977     2.878043  ...   2542.238603   3557.765512
    # min      1.000000  2011.000000  ...   2030.000000   4910.000000
    # 25%     63.250000  2013.000000  ...   6751.000000   8939.750000
    # 50%    125.500000  2015.500000  ...   8488.500000  11223.500000
    # 75%    187.750000  2018.000000  ...  10133.250000  13867.000000
    # max    250.000000  2020.000000  ...  16345.000000  21899.000000
    
    # 정규성 확인
    print(stats.shapiro(pdg1['전체인구'])) # pvalue=0.81577 > 0.05 이므로 만족
    print(stats.shapiro(pdg2['65세이상 노인'])) # pvalue=0.98256 > 0.05 이므로 만족
    print(stats.shapiro(edg['독거노인'])) # pvalue=0.9808 > 0.05 이므로 만족
    
    # y1 은 pdg1의 전체인구컬럼의 데이터를 넣는다
    y1 = pdg1['전체인구']
    
    # y2 은 pdg2의 65세이상 노인의 데이터를 넣는다
    y2 = pdg2['65세이상 노인']
    # y3 은 edg의 독거노인의 데이터를 넣는다.
    y3 = edg['독거노인']
    # 말그대로 등분산성 확인을 통하여 데이터 확인.
    print('등분산성 확인 : ', stats.levene(y1, y2, y3).pvalue) # 0.0020 < 0.05 이므로 등분산성 만족x
    
    # pd.merge의 명령어를 통해 pdg1, pdg2의 데이터를 합치고 dfmarge의 넣는다. 
    dfmarge = pd.merge(pdg1,pdg2)
    # pd.merge의 경우 3개 동시에 작용이 안되기때문에 한번 더 사용하여 dfmarge와 edg를 합치고 sdg에 넣는다.
    sdg = pd.merge(dfmarge,edg)
    print(sdg)
    
    #print(sdg.columns)
    #print(sdg.type())
    
    # 등분산성을 만족하지 못할 때 welch_anova 검정을 실시함.
    # (data=data, dv=’종속변수’, between='독립변수')
    print(welch_anova(dv ='전체인구', between = '65세이상 노인', data = sdg))
    #     Source  ddof1  ddof2    F  p-unc  np2
    # 0  65세이상 노인      9    inf  0.0    1.0  1.0
    # p-value : 1.0 > 0.05 큼 
    
    # 결론 : 해당 모델의 경우 사용이 부적합하므로 평균의 차이가 있다고 볼수 없다 (귀무가설 채택)


   
    
    
except Exception as e:
    print('오류는 : ' , e) 
    conn.rollback()
finally:
    cursor.close()
    conn.close()    