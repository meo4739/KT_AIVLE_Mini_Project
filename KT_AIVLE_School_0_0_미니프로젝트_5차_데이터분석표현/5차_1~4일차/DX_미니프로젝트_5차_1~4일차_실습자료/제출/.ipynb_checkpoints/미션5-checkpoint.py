
import pandas as pd
import streamlit as st
import numpy as np
import datetime
import plotly.express as px


# -------------------- ▼ 필요 변수 생성 코딩 Start ▼ --------------------

data = pd.read_csv('./119_emergency_dispatch.csv', encoding="cp949")

## 오늘 날짜
now_date = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=9)
now_date2 = datetime.datetime.strptime(now_date.strftime("%Y-%m-%d"), "%Y-%m-%d")

## 2023년 최소 날짜, 최대 날짜
first_date = pd.to_datetime("2023-01-01")
last_date = pd.to_datetime("2023-12-31")

## 출동 이력의 최소 날짜, 최대 날짜
min_date = datetime.datetime.strptime(data['출동일시'].min(), "%Y-%m-%d")
max_date = datetime.datetime.strptime(data['출동일시'].max(), "%Y-%m-%d")


# -------------------- ▲ 필요 변수 생성 코딩 End ▲ --------------------


# -------------------- ▼ Streamlit 웹 화면 구성 START ▼ --------------------

# 레이아웃 구성하기 
st.set_page_config(layout = 'wide')

# tabs 만들기 
tab1, tab2 = st.tabs(['출동일지', '대시보드'])


with tab1:
    st.write('도전과제')

with tab2:
    ## -------------------- ▼ 2-0그룹 금일 출동 이력 출력 ▼ --------------------
    today_date = now_date.strftime("%Y-%m-%d")
    # today_count = len(data[******************************])
#     if today_count > 0 :
#         st.dataframe(**********)
#     else:
#         st.markdown("금일 출동내역이 없습니다.")
    ## -------------------------------------------------------------------
#     ## -------------------- ▼ 2-1그룹 통계 조회 기간 선택하기 ▼ --------------------
    col210, col211, col212 = st.columns([0.3, 0.2, 0.1])
    
    with col210:
        slider_date = st.slider("날짜 :", min_value = min_date, max_value = max_date,
                                                value = (min_date, now_date2))
    with col211:
        slider_week = st.slider('주간', min_value = min_date,  max_value = max_date,
                                step = datetime.timedelta(weeks = 1), value = (min_date, now_date2), format = 'YYYY-MM')
    
    with col212:
        slider_month = st.slider('월간', min_value = min_date, max_value = max_date,
                                 step = datetime.timedelta(weeks = 1), value = (min_date, now_date2), format = 'YYYY-MM')

    st.info('금일 출동 내역')
    ## 선택된 일자의 data 추출
    data['datetime'] = pd.to_datetime(data['출동일시'])
    data = data[ (slider_date[0] <= data['datetime']) & (data['datetime'] <= slider_date[1] )]
    st.write(data)
    st.dataframe(data[ (slider_date[0] <= data['datetime']) & (data['datetime'] <= slider_date[1] )][['datetime','이송 시간']].sort_values( by = 'datetime', ascending = True))
    
    # 선택된 주간의 data 추출
    st.info('금주 출동 내역')
    data['주별'] = data['datetime'].dt.strftime("%W").astype(int) + 1
    min_week = int(slider_week[0].strftime("%W"))
    max_week = int(slider_week[1].strftime("%W"))
    week_list_df = data[(data['주별'] >= min_week) & (data['주별'] <= max_week)]
    st.write(week_list_df)
    st.write(week_list_df[['datetime','주별','이송 시간']].sort_values(by='주별', ascending=True))
        
    ## 선택된 월의 data 추출
    st.info('당월 출동 내역')
    data['월별'] = data['datetime'].dt.month.astype(int)
    min_month = slider_month[0].month
    max_month = slider_month[1].month
    month_list_df = data[(data['월별'] >= min_month) & (data['월별'] <= max_month)]
    st.write(month_list_df)
    st.write(month_list_df[['datetime','월별','이송 시간']].sort_values(by='월별', ascending=True))

#     ## -------------------------------------------------------------------------------------------
#      ## -------------------- ▼ 2-2그룹 일간/주간/월간 평균 이송시간 통계 그래프 ▼ --------------------
    st.success("평균 이송시간 통계")
    col230, col231, col232 = st.columns([0.3, 0.2, 0.1])
    with col230:
        st.write('일별')
        group_day_time = data.groupby(by = 'datetime', as_index = False)['이송 시간'].mean()
        # group_day_time = **********
        st.write(group_day_time)
        st.line_chart(data = group_day_time, x = 'datetime', y = '이송 시간')

    with col231:
        st.write('주별')
        group_week_time = week_list_df.groupby(by = '주별', as_index = False)['이송 시간'].mean()
        # group_week_time = **********
        st.write(group_week_time)
        st.line_chart(data=group_week_time, x ='주별', y = '이송 시간')

    with col232:
        st.write('월별')
        group_month_time = month_list_df.groupby(by = '월별', as_index = False)['이송 시간'].mean()
        # group_month_time = **********
        st.write(group_month_time)
        st.line_chart(data=group_month_time, x = '월별', y = '이송 시간')
        
    
#     ## -------------------------------------------------------------------------------------------
#     ## -------------------- ▼ 2-3 그룹 일간/주간/월간 총 출동 건수 통계 그래프 ▼ --------------------
    st.error("출동 건수")
    select_bins = st.radio("주기", ('일별', '주별', '월별'), horizontal=True)
    if select_bins == '일별':
        select_df = data.groupby(by = 'datetime', as_index = False)['ID'].count()
        select_df = select_df.rename(columns = {'ID':'출동건수', 'datetime':'일별'})
        st.write(select_df)
        st.bar_chart(data=select_df, x= '일별', y = '출동건수')
        
    elif select_bins=='주별':
        select_df = data.groupby(by = '주별', as_index = False)['ID'].count()
        select_df = select_df.rename(columns = {'ID':'출동건수'})
        st.write(select_df)
        st.bar_chart(data=select_df, x= '주별', y = '출동건수')
    else:
        select_df = data.groupby(by = '월별', as_index = False)['ID'].count()
        select_df = select_df.rename(columns = {'ID':'출동건수'})
        st.write(select_df)
        st.bar_chart(data=select_df, x= '월별', y = '출동건수')
        
#     re_select_df = select_df.rename(columns={"출동일시": '일별'})    
#     dispatch_count = re_select_df.groupby(***************************)['ID'].count()
#     dispatch_count = dispatch_count.rename(*******************************)
#     dispatch_count = dispatch_count.sort_values(*************************)

#     st.bar_chart(*****************************************)


#     ## -------------------------------------------------------------------------------------------
#     ## -------------------- ▼ 2-4 성별/중증질환/나이대 별 비율 그래프 ▼ --------------------
    st.warning("성별/중증질환/나이대 별 통계")
    st.write(data)
    data['성별'] = data['성별'].replace('남성','남자')
    col240, col241, col242 = st.columns(3)
    with col240: # 성별 통계
        st.write('성별 통계') 
        group_by_gender = data.groupby(by= ['datetime','성별'], as_index=False)['ID'].count()
        group_by_gender = group_by_gender.rename(columns={'ID':'숫자'})
        st.write(group_by_gender)

        fig = px.pie(group_by_gender, values= '숫자', names='성별', title='성별 통계', hole=0.3)
#         fig.update_traces(textposition=*******, textinfo=********)
#         fig.update_layout(font=dict(size=16))
        st.plotly_chart(fig)

    with col241: # 중증질환별 통계
        st.write('중증질환별 통계')
        group_by_disease =data.groupby(by=['datetime','중증질환'], as_index=False)['ID'].count()
        st.write(group_by_disease)
        # group_day_disease = ***********************************
        group_by_disease = group_by_disease.rename(columns={'ID':'숫자'})
        
        fig = px.pie(group_by_disease, values= '숫자', names='중증질환', title='중증질환별 통계', hole=0.3)
#         fig = px.pie(***********************************************************)
#         fig.update_traces(*****************************************************)
#         fig.update_layout(*********************************)
        st.plotly_chart(fig)

    with col242:  # 나이대별 통계
        st.write('나이대별 통계')
        group_by_age =data.groupby(by=['datetime','나이'], as_index=False)['ID'].count()
        group_by_age = group_by_age.rename(columns={'ID':'숫자'})
        st.write(group_by_age)
        group_by_age['나이대'] = (group_by_age['나이']//10)*10
        fig = px.pie(group_by_age, values= '숫자', names='나이대', title='나이대별 통계', hole=0.3)
#         group_day_disease = **************************************************************
#         group_day_disease = ***************************************************************

#         fig = *****************************************************************
#         fig.update_traces(***************************************************)
#         fig.update_layout(*********************)
        st.plotly_chart(fig)

    
    ## -------------------------------------------------------------------------------------------

    ## -------------------- ▼ 2-4그룹 그외 필요하다고 생각되는 정보 추가 ▼ --------------------


    st.error("증상별 출동")
    st.write(data.columns)
    select_bins = st.radio("증상", ('간헐성 경련', '설사', '기침', '호흡 곤란', '출혈' ,'통증', '만지면 아프다'), horizontal=True)
    if select_bins == '간헐성 경련':
        select_df = data.groupby(by = '간헐성 경련', as_index = False)['ID'].count()
        select_df = select_df.rename(columns = {'ID':'출동건수'})
        st.write(select_df)
        st.bar_chart(data=select_df, x= '간헐성 경련', y = '출동건수')
        
    elif select_bins=='설사':
        select_df = data.groupby(by = '설사', as_index = False)['ID'].count()
        select_df = select_df.rename(columns = {'ID':'출동건수'})
        st.write(select_df)
        st.bar_chart(data=select_df, x= '설사', y = '출동건수')
    elif select_bins== '기침':
        select_df = data.groupby(by = '기침', as_index = False)['ID'].count()
        select_df = select_df.rename(columns = {'ID':'출동건수'})
        st.write(select_df)
        st.bar_chart(data=select_df, x= '기침', y = '출동건수')
        
    elif select_bins=='호흡 곤란':
        select_df = data.groupby(by = '호흡 곤란', as_index = False)['ID'].count()
        select_df = select_df.rename(columns = {'ID':'출동건수'})
        st.write(select_df)
        st.bar_chart(data=select_df, x= '호흡 곤란', y = '출동건수')
        
    elif select_bins== '출혈':
        select_df = data.groupby(by = '출혈', as_index = False)['ID'].count()
        select_df = select_df.rename(columns = {'ID':'출동건수'})
        st.write(select_df)
        st.bar_chart(data=select_df, x= '출혈', y = '출동건수')
        
    elif select_bins=='통증':
        select_df = data.groupby(by = '통증', as_index = False)['ID'].count()
        select_df = select_df.rename(columns = {'ID':'출동건수'})
        st.write(select_df)
        st.bar_chart(data=select_df, x= '통증', y = '출동건수')
        
    elif select_bins== '만지면 아프다':
        select_df = data.groupby(by = '만지면 아프다', as_index = False)['ID'].count()
        select_df = select_df.rename(columns = {'ID':'출동건수'})
        st.write(select_df)
        st.bar_chart(data=select_df, x= '만지면 아프다', y = '출동건수')