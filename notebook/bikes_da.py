def bike_da():
    import streamlit as st
    import os
    import streamlit.components.v1 as components
    import folium
    import seaborn as sns
    import matplotlib.pyplot as plt

    os.chdir("C:/Users/USER/.cursor-tutor/ms-ai-school/notebook")

    @st.cache_data
    def data_prerocessing() :
        import pandas as pd
        import seaborn as sns
        import matplotlib.pyplot as plt

        plt.rc('font', family='Malgun Gothic')

        bikes = pd.DataFrame()

        for i in range(1,4):
            temp = pd.read_csv(f"https://media.githubusercontent.com/media/IDKNWHORU/ms-ai-school-codespace/0626/data/%EC%84%9C%EC%9A%B8%ED%8A%B9%EB%B3%84%EC%8B%9C%20%EA%B3%B5%EA%B3%B5%EC%9E%90%EC%A0%84%EA%B1%B0%20%EB%8C%80%EC%97%AC%EC%A0%95%EB%B3%B4_201906_{i}.csv", encoding="cp949")
            bikes = pd.concat([bikes, temp])
            
        bikes.isnull().sum()
        bikes['대여일시']=bikes['대여일시'].astype('datetime64[ms]') 

        # 파생변수, '요일', '일자', '대여시간대', '주말구분'
        요일 = ['월', '화', '수', '목', '금', '토', '일']
        bikes['요일'] = bikes['대여일시'].dt.dayofweek.apply(lambda x : 요일[x])
        bikes['일자'] = bikes['대여일시'].dt.day
        bikes['대여시간대']=bikes['대여일시'].dt.hour
        bikes['주말구분']=bikes['대여일시'].dt.dayofweek.apply(lambda x: '평일' if x < 5 else '주말')

        # 위도, 경도 파일 merge
        bike_shop = pd.read_csv(f'../data/공공자전거 대여소 정보_23._06.csv', encoding='cp949')
        bike_gu = bike_shop[['자치구', '대여소\r\n번호', '보관소(대여소)명', '위도', '경도']]
        bike_gu = bike_gu.rename(columns={'대여소\r\n번호': '대여소번호', '보관소(대여소)명': '대여소명'})
        bikes = pd.merge(bikes, bike_gu, left_on='대여 대여소번호', right_on='대여소번호')
        bikes = bikes.drop(['대여소번호', '대여소명'], axis=1)
        bikes = bikes.rename(columns={'자치구':"대여구", '위도': '대여점 위도', '경도': '대여점 경도'})
        
        return bikes

    bikes = data_prerocessing()

    tab1, tab2, tab3 = st.tabs(['데이터 보기', '시간적 분석', '인기 대여소'])

    with tab1:
        st.dataframe(bikes.head(30))
    with tab2:
        chart_name = ['요일','일자','대여시간대']
        for i in chart_name:
            # 요일별
            fig, ax = plt.subplots(figsize=(15,4))
            ax = sns.countplot(data=bikes, x=i)
            ax.set_title(f'{i}별 이용건수')
            st.pyplot(fig)

        st.markdown('''
                    1. 요일별 분석
                    * 평일보다 주말에 따릉이 이용건수가 많고
                    * 주말에 인기 있는 대여소 근처에 

                    2. 일자별 분석
                    * 6일
                    * 일회원

                    3. 시간대별 분석
                    * 출퇴근
                    * 출퇴근
                    ''')
        hourly_dayofweek_ride = bikes.pivot_table(index='대여시간대',columns='요일',values='자전거번호',aggfunc='count')
        fig, ax = plt.subplots(figsize=(15,8))
        ax = sns.heatmap(hourly_dayofweek_ride, annot=True, fmt='d')
    with tab3:
        rent_bike = bikes.pivot_table(index=['대여 대여소명','대여점 위도', '대여점 경도'],
                                columns=['주말구분'],
                                values='자전거번호',
                                aggfunc='count')
        
        weekend_house50 = rent_bike.nlargest(50,'주말')[['주말']].reset_index()


        # 지도의 중심위치를 정한다.
        lat = bikes['대여점 위도'].mean()
        lon = bikes['대여점 경도'].mean()
        center = [lat, lon]
        map1 = folium.Map(location = center, zoom_start = 11)

        for i in weekend_house50.index:
            sub_lat = weekend_house50.loc[i,'대여점 위도']
            sub_lon = weekend_house50.loc[i,'대여점 경도']
            name = weekend_house50.loc[i,'대여 대여소명']
            
            folium.Marker(location=[sub_lat,sub_lon],
                        popup=name).add_to(map1)
        
        st.subheader("주말 인기 대여소 Top 50")
        st.caption("주말에 인기 있는 대여소 Top 50을 표시한 것으로 주로 한경변, 호수나 공원 근처이다.")
        
        #지도 시각화 , stremalit
        components.html(map1._repr_html_(),height=400)