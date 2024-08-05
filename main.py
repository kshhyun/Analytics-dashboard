import streamlit as st
import pandas as pd
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")

font_path = 'C:\\Windows\\Fonts\\malgun.ttf'
font_prop = fm.FontProperties(fname=font_path, size=14)
plt.rc('font', family='Malgun Gothic')

# 사이드바 설정
st.sidebar.title("Big-data Project")
sidebar_option = st.sidebar.selectbox('강수', ['강수량'])
sidebar_option2 = st.sidebar.selectbox('지하철', ['지하철 유동인구', '지하철 지연'])

# CSV 파일 경로
rain_csv_file_path = 'D:\\kDigital_workspace\\2차 프로젝트\\dashboard\\Analytics-dashboard\\csv\\rain2.csv'
subway_csv_file_path = 'D:\\kDigital_workspace\\2차 프로젝트\\dashboard\\Analytics-dashboard\\csv\\subway.csv'
subway_delay_csv_file_path = 'D:\\kDigital_workspace\\2차 프로젝트\\dashboard\\Analytics-dashboard\\csv\\delay.csv'

rain_data = pd.read_csv(rain_csv_file_path)
subway_data = pd.read_csv(subway_csv_file_path)
subway_delay_data = pd.read_csv(subway_delay_csv_file_path)



# 날짜 열을 datetime 형식으로 변환
rain_data['날짜'] = pd.to_datetime(rain_data['날짜'])
subway_data['날짜'] = pd.to_datetime(subway_data['날짜'])
subway_delay_data['날짜'] = pd.to_datetime(subway_delay_data['날짜'])

# 강수량 평균 계산
average_rainfall = rain_data['강수량(mm)'].mean()

# 날짜를 기준으로 데이터프레임
merged_data = pd.merge(rain_data, subway_data, on='날짜')
merged_delay_data = pd.merge(rain_data, subway_delay_data, on='날짜')

# 월별로 그룹화하기 위해 '년-월' 형식의 새로운 열 추가
merged_data['연-월'] = merged_data['날짜'].dt.to_period('M').astype(str)
merged_delay_data['연-월'] = merged_delay_data['날짜'].dt.to_period('M').astype(str)



# 역 이름 리스트 생성
stations = subway_data['역명'].unique()

def subway_graph(station):
    st.subheader(f"{station} 역 유동인구")

    # 선택한 역
    station_data = merged_data[merged_data['역명'] == station]

    # 평균 강수량 이상
    above_average_rain = station_data[station_data['강수량(mm)'] > average_rainfall]
    below_average_rain = station_data[station_data['강수량(mm)'] <= average_rainfall]

    # 월별 평균 유동인구
    monthly_avg_traffic_above = above_average_rain.groupby('연-월')['총승하차인원'].mean().reset_index()
    monthly_avg_traffic_below = below_average_rain.groupby('연-월')['총승하차인원'].mean().reset_index()

    # 그래프
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=monthly_avg_traffic_above['연-월'], y=monthly_avg_traffic_above['총승하차인원'],
                             mode='markers+lines', name='평균 이상', line=dict(color='blue')))

    fig.add_trace(go.Scatter(x=monthly_avg_traffic_below['연-월'], y=monthly_avg_traffic_below['총승하차인원'],
                             mode='markers+lines', name='평균 이하', line=dict(color='orange')))

    # 범례
    fig.update_layout(xaxis_title='연-월', yaxis_title='유동인구 평균', legend_title_text='강수량')

    st.plotly_chart(fig)

def rain_graph():
    st.subheader("강수량 별 유동인구")
    
    # 강수량 유동인구 상관관계
    correlation = merged_data['강수량(mm)'].corr(merged_data['총승하차인원'])
    st.write(f"강수량과 유동인구의 상관관계: {correlation:.2f}")

    # 경향선 그래프
    fig = px.scatter(merged_data, x='강수량(mm)', y='총승하차인원', 
                     trendline='ols',
                     labels={'강수량(mm)': '강수량(mm)', '총승하차인원': '유동인구'},
                     trendline_color_override='red')
    
    st.plotly_chart(fig)

def max_delay_time():
    st.subheader("강수량 별 지하철 지연 빈도수")
    
    rain_csv_file_path = 'D:\\kDigital_workspace\\2차 프로젝트\\dashboard\\Analytics-dashboard\\csv\\rain2.csv'
    delay_csv_file_path = 'D:\\kDigital_workspace\\2차 프로젝트\\dashboard\\Analytics-dashboard\\csv\\delay.csv'

    df1 = pd.read_csv(rain_csv_file_path)
    df2 = pd.read_csv(delay_csv_file_path)

    # 데이터 전처리
    df2['날짜'] = pd.to_datetime(df2['날짜'])
    df2['최대지연시간'] = df2['최대지연시간'].str.replace('분', '').astype(int)
    df1['날짜'] = pd.to_datetime(df1['날짜'])

    # 데이터 병합
    merged_df = pd.merge(df2, df1, left_on='날짜', right_on='날짜', how='inner')

    # 강수량 최대 지연 시간 평균
    average_delay_rain = merged_df.groupby('날짜').agg({'최대지연시간': 'mean', '강수량(mm)': 'mean'}).reset_index()


    fig1 = px.scatter(average_delay_rain, x='강수량(mm)', y='최대지연시간',
                      labels={'강수량(mm)': '강수량 (mm)', '최대지연시간': '평균 최대 지연 시간 (분)'})

    st.plotly_chart(fig1)

def delay_analysis():
    st.subheader("강수량 별 평균 및 최대 지연시간")
    
    rain_csv_file_path = 'D:\\kDigital_workspace\\2차 프로젝트\\dashboard\\Analytics-dashboard\\csv\\rain2.csv'
    delay_csv_file_path = 'D:\\kDigital_workspace\\2차 프로젝트\\dashboard\\Analytics-dashboard\\csv\\delay.csv'

    df1 = pd.read_csv(rain_csv_file_path)
    df2 = pd.read_csv(delay_csv_file_path)

    # 데이터 전처리
    df2['날짜'] = pd.to_datetime(df2['날짜'])
    df2['최대지연시간'] = df2['최대지연시간'].str.replace('분', '').astype(int)
    df1['날짜'] = pd.to_datetime(df1['날짜'])

    # 데이터 병합
    merged_df = pd.merge(df2, df1, left_on='날짜', right_on='날짜', how='inner')

    # 강수량별 평균 및 최대 지연 시간
    average_delay = merged_df.groupby('강수량(mm)')['최대지연시간'].mean().reset_index()
    average_delay.columns = ['강수량(mm)', '평균 지연 시간 (분)']

    max_delay = merged_df.groupby('강수량(mm)')['최대지연시간'].max().reset_index()
    max_delay.columns = ['강수량(mm)', '최대 지연 시간 (분)']

    fig2 = go.Figure()

    # 평균 지연 시간 시각화
    fig2.add_trace(go.Bar(x=average_delay['강수량(mm)'], y=average_delay['평균 지연 시간 (분)'],
                          name='평균 지연 시간 (분)', marker_color='blue'))

    # 최댓값 지연 시간 시각화
    fig2.add_trace(go.Bar(x=max_delay['강수량(mm)'], y=max_delay['최대 지연 시간 (분)'],
                          name='최대 지연 시간 (분)', marker_color='orange'))

    # 그래프
    fig2.update_layout(
        xaxis_title='강수량 (mm)',
        yaxis_title='지연 시간 (분)',
        barmode='group'
    )

    st.plotly_chart(fig2)



def main():
    st.header("강수량에 따른 서울 지하철 유동인구 및 지연 분석")
    
    if sidebar_option2 == '지하철 유동인구':
        tab1, tab2 = st.tabs(["유동인구", "역별"])

        with tab1:
            rain_graph()

        with tab2:
            # 역 선택
            station = st.selectbox('역 선택:', stations)
            if station:
                subway_graph(station)
                
    elif sidebar_option2 == '지하철 지연':
        tab1, tab2 = st.tabs(["지연 시간", "지연 빈도수"])

        with tab1:
            delay_analysis()

        with tab2:
            max_delay_time()

if __name__ == '__main__':
    main()
