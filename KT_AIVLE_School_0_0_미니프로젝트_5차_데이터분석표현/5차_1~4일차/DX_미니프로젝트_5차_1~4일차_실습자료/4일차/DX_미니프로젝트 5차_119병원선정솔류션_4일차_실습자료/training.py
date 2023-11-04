
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

data = pd.read_csv('./119_emergency_dispatch_1.csv', encoding="cp949")

## 오늘 날짜
now_date = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=9)
now_date2 = datetime.datetime.strptime(now_date.strftime("%Y-%m-%d"), "%Y-%m-%d")

## 출동 이력의 최소 날짜, 최대 날짜
min_date = datetime.datetime.strptime("2023-01-01", "%Y-%m-%d")
max_date = datetime.datetime.strptime("2023-12-31", "%Y-%m-%d")
today_date = now_date.strftime("%Y-%m-%d")




## 레이아웃 구성하기 
st.set_page_config(layout="wide")

st.write(


# *********************** ▲ 가이드 코딩 End ▲ ***********************
# *********************** ▼ 연습 코딩 Start ▼ ***********************




























# *********************** ▲ 연습 코딩 End ▲ ***********************

