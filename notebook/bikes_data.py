def data_prerocessing() :
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt

    plt.rc('font', family='Malgun Gothic')

    bikes = pd.DataFrame()

    for i in range(1,4):
        temp = pd.read_csv(f"../data/서울특별시 공공자전거 대여정보_201906_{i}.csv", encoding="cp949")
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

if __name__ == "__main__":
    bikes = data_prerocessing()
    print(bikes.head())
