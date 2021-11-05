from django.shortcuts import render
from HJ_app.models import SeoulElder, SeoulHospital
import pandas as pd
import folium
import json

def mainFunc(request):
    map = folium.Map(location=[37.541, 126.986], zoom_start=11, tiles='cartodbpositron')
    
    # 독거노인
    elder = SeoulElder.objects.all().values()
    elder_df = pd.DataFrame.from_records(elder)
    elder_df.columns = ['번호', '기간', '자치구명', '기초생활수급', '저소득', '일반']
    elder_df = elder_df[elder_df.기간 == 2020]
    elder_df = elder_df[['자치구명', '기초생활수급', '저소득', '일반']]
    elder_df['합'] = elder_df.sum(axis=1)
    print(elder_df)
    
    # 요양병원
    hp = SeoulHospital.objects.all().values()
    hp_df = pd.DataFrame.from_records(hp)
    #hp_df.columns = ['번호', '여부', '전화', '주소', '이름', '종류', '위도', '경도', 'url']
    hp_df.columns = ['번호', '이름', '여부', '주소', '전화', '종류', '위도', '경도', 'url', '회원가입여부']
    
    # 서울 행정구
    with open('C:\work\psou\HJproject\geo.json', mode='rt', encoding='utf-8') as f:
        geo = json.loads(f.read()) # json 파일 로드
        f.close()
    
    folium.Choropleth(
        geo_data = geo,
        data = elder_df, 
        columns=('자치구명', '합'), 
        key_on='feature.properties.name',
        fill_color='PuBu',
        legend_name='독거노인 인구수',
    ).add_to(map)

    # 구별 테두리
    folium.GeoJson(geo).add_to(map)
    
    # 마커 표시
    for i in range(0, len(hp_df)):
        folium.Marker([hp_df['위도'][i], hp_df['경도'][i]], popup="<i><a href="+hp_df['url'][i]+">"+hp_df['이름'][i]+"</a></i>").add_to(map)
    
    maps = map._repr_html_()
    return render(request, 'main.html', {'m' : maps})


# 병원 회원가입 폼
def CreateHospitalFunc(request): 
    return render(request, 'createHospital.html')
# 회원가입 신청
def RegisteredFunc(request): 
    if request.method == 'POST':
        h_name = request.POST.get('h_name')
        h_open = request.POST.get('h_open')
        h_addr = request.POST.get('h_addr')
        h_tel = request.POST.get('h_tel')
        h_kind = request.POST.get('h_kind')
        h_url = request.POST.get('h_url')
        SeoulHospital(
            h_name=h_name,
            h_open = h_open,
            h_addr = h_addr,
            h_tel = h_tel,
            h_kind = h_kind,
            h_url = h_url,
            is_confirmed = 0
        ).save()
        
        return render(request, 'create_hospital_done.html')
# 로그인 폼
def LoginFormFunc(request):
    pass
# 로그인 
def LoginFunc(request):
    pass



