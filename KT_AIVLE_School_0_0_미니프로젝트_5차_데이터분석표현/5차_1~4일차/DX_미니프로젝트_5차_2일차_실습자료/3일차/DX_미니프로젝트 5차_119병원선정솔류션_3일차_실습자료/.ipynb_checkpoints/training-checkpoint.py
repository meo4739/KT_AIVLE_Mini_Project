
# 라이브러리 불러오기 

import pandas as pd
import numpy as np
import datetime
import joblib
from keras.models import load_model
from haversine import haversine
from urllib.parse import quote
import streamlit as st
from streamlit_folium import st_folium
import folium
import branca
from geopy.geocoders import Nominatim
import ssl
from urllib.request import urlopen
import pandas as pd
import plotly.express as px

# *********************** ▼ 가이드 코딩 Start ▼ ***********************

data = pd.read_csv('119_emergency_dispatch.csv', encoding="cp949")

## 오늘 날짜
now_date = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=9)
now_date2 = datetime.datetime.strptime(now_date.strftime("%Y-%m-%d"), "%Y-%m-%d")

## 출동 이력의 최소 날짜, 최대 날짜
min_date = datetime.datetime.strptime("2023-01-01", "%Y-%m-%d")
max_date = datetime.datetime.strptime("2023-12-31", "%Y-%m-%d")
today_date = now_date.strftime("%Y-%m-%d")

## 레이아웃 구성하기 
st.set_page_config(layout="wide")

# *********************** ▲ 가이드 코딩 End ▲ ***********************
# *********************** ▼ 연습 코딩 Start ▼ ***********************

tab1, tab2 = st.tabs(['tab1', 'tab2'])
with tab1:    
    col1, col2, col3 = st.columns([0.1, 0.8, 0.1])
    with col1:
        st.write("**")
    with col2:
        st.title('Pre Prototype')
    with col3:
        st.write("**")
        
    with st.expander("119", expanded = True):
        st.image('119.png')

st.markdown("## 화면에 표시하기")

st.write("텍스트를 출력합니다")

st.info("데이터프레임")

er_df = pd.read_csv('daegu_hospital_list.csv')
st.dataframe(er_df[:10])

today = st.date_input("오늘 날짜", label_visibility = 'collapsed')

now_time = st.time_input("현재 시간")

name = st.text_input("이름")

age = st.number_input("나이", min_value=0, max_value = 120)

st.markdown("## Input widget(2)")

st.info("중증 질환 선택")

select_radio = st.radio("중증 질환 선택", ['뇌출혈', '중증화상','뇌경색','심근경색','심근경색'],
                       horizontal = True, label_visibility = 'collapsed')

cough_check = st.checkbox('기침')

convolusion_check = st.checkbox("간헐적 경련")

emergency = st.selectbox("판단", ("중증 질환 아님","중증 질환"))

col1, col2 = st.columns(2)
with col1:
    lati = st.slider('위도', 35.00, 35.40)
with col2:
    long = st.slider('경도', 128.80, 129.30)
                         
data = pd.read_csv('119_emergency_dispatch.csv', encoding = 'cp949')

st.markdown('Form')

with st.form(key = 'tab1_first'):
    if st.form_submit_button(label = '병원조회'):
        with st.expander("병원 정보", expanded = True):
            st.dataframe(data[:10])

st.markdown("지도 1")

m = folium.Map(location = [35.15, 129.10], zoom_start = 11)

patient_lat = 35.268312
patient_lon = 129.171137

icon = folium.Icon(color = 'red')

folium.Marker(location = [patient_lat, patient_lon],
              popup = '환자', tooltip = '환자위치', icon = icon).add_to(m)

st_folium(m, width = 1000)

# *********************** ▲ 연습 코딩 End ▲ ***********************

hospital_list = pd.read_csv('daegu_hospital_list.csv')

st.write(hospital_list.columns)

st.markdown("지도 2")
for idx, row in hospital_list[:5].iterrows():
    html = """<!DOCTYPE html>
    <html>
    <table style="height: 126px; width: 330px;"> <tbody> <tr>
        <td style="background-color: #2A799C;">
        <div style="color: #ffffff;text-align:center;">dutyName</div></td>
        <td style="width: 230px;background-color: #C5DCE7;">{}</td>""".format(row['dutyName'])+"""</tr> 
        <tr><td style="background-color: #2A799C;">
        <div style="color: #ffffff;text-align:center;">wgs84Lat</div></td>
        <td style="width: 230px;background-color: #C5DCE7;">{}</td>""".format(row['wgs84Lat'])+"""</tr>
        <tr><td style="background-color: #2A799C;">
        <div style="color: #ffffff;text-align:center;">wgs84Lon</div></td>
        <td style="width: 230px;background-color: #C5DCE7;">{}</td>""".format(row['wgs84Lon'])+""" </tr>
        </tbody> </table> </html> """
        
    iframe = branca.element.IFrame(html=html, width=350, height=150)
    popup_text = folium.Popup(iframe,parse_html=True)
    icon = folium.Icon(color="blue")
    folium.Marker(location=[row['wgs84Lat'], row['wgs84Lon']], 
    popup=popup_text, tooltip=row['dutyName'], icon=icon).add_to(m)

st_data = st_folium(m, width=1000)