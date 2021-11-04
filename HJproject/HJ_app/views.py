from django.shortcuts import render
from HJ_app.models import Godok, SeoulCenter, SeoulElder, SeoulPeople
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import json

# Create your views here.
# def mainFunc(request):
#     godok = Godok.objects.all().values()
#     center = SeoulCenter.objects.all().values()
#     elder = SeoulElder.objects.all().values()
#     people = SeoulPeople.objects.all().values()
#
#     """
#     DB 데이터 print 확인
#     print(godok)
#     print(center)
#     print(elder)
#     print(people)
#     """
#
#     godok_df = pd.DataFrame.from_records(godok)
#     godok_df.columns = ['번호', '년도', '사망자수']
#     print(godok_df)
#
#     center_df = pd.DataFrame.from_records(center)
#     center_df.columns = ['번호', '년도', '자치구명', '노인복지관', '경로당', '노인교실']
#     print(center_df)
#
#     elder_df = pd.DataFrame.from_records(elder)
#     elder_df.columns = ['번호', '기간', '자치구명', '기초생활수급', '저소득', '일반']
#     print(elder_df)
#
#     people_df = pd.DataFrame.from_records(people)
#     people_df.columns = ['번호', '기간', '자치구명', '전체인구', '65세이상 노인']
#     print(people_df)
#
#     return render(request, 'main.html')


def mainFunc(request):
    map = folium.Map(location=[37.541, 126.986], zoom_start=11, 
                 tiles='Stamen Toner')
    
    
    elder = SeoulElder.objects.all().values()
    elder_df = pd.DataFrame.from_records(elder)
    elder_df.columns = ['번호', '기간', '자치구명', '기초생활수급', '저소득', '일반']
    elder_df = elder_df[elder_df.기간 == 2020]
    elder_df = elder_df[['자치구명', '기초생활수급', '저소득', '일반']]
    elder_df['합'] = elder_df.sum(axis=1)
    print(elder_df)
    
    # skorea-municipalities-geo.json 파일을 열어서 geo에 저장
    with open('C:\work\psou\HJproject\geo.json', mode='rt', encoding='utf-8') as f:
        geo = json.loads(f.read()) # json 파일 로드
        f.close()
    
    folium.Choropleth(
        geo_data = geo,
        data = elder_df, 
        columns=('자치구명', '합'), 
        key_on='feature.properties.name',
        fill_color='YlGn', # 여기가 바뀌었습니다.
        legend_name='독거노인 인구수',
    ).add_to(map)

    # geo를 seoul에 추가
    folium.GeoJson(geo, name='seoul_municipalities').add_to(map)
    maps = map._repr_html_()

    
    return render(request, 'main.html', {'m' : maps})
    