from django.shortcuts import render
from HJ_app.models import Godok, SeoulCenter, SeoulElder, SeoulPeople, SeoulHospital
import pandas as pd
import folium
import json
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView

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


# 병원 등록
class CreateHospitalView(CreateView): 
    template_name = 'signup.html' 
    form_class =  UserCreationForm 
    success_url = reverse_lazy('create_hospital_done') 
    
class RegisteredView(TemplateView): 
    template_name = 'create_hospital_done.html'
    def post(self, request, **kwargs):
        print(request.POST)
        h_name = request.POST.get('t_name', '')
        h_open = request.POST.get('t_address','')
        h_addr = request.POST.get('t_phone', '')
        h_tel = request.POST.get('t_webaddress', '')
        h_kind = request.POST.get('t_info', '')
        h_wi = request.POST.get('t_adult', '')
        h_kung = request.POST.get('t_kid', '')
        h_url = request.POST.get('t_kid', '')
        tmp = SeoulHospital()(
            h_name=h_name,
            h_open = h_open,
            h_addr = h_addr,
            h_tel = h_tel,
            h_kind = h_kind,
            h_wi = h_wi,
            h_kung = h_kung,
            h_url = h_url,
        )
        tmp.save()
        return render(request, 'create_hospital_done.html')

