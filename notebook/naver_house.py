import pandas as pd
import matplotlib.pyplot as plt

plt.rc('font', family='Malgun Gothic')

def fetch_data():
    df = pd.DataFrame()
    for page_num in range(1, 11):
        base_url = f"https://land.naver.com/news/trendReport.naver?page={page_num}"
        temp = pd.read_html(base_url)
        df = pd.concat([df, temp[0]])
    return df

def clean_data(df):
    temp = df['제목'].str.replace('%', '')
    regions = ['전국', '서울', '수도권']
    for region in regions:
        temp = temp.str.replace(region, '')
    temp = temp.str.split(']', expand=True)[1]
    temp = temp.str.split(',', expand=True)
    temp = temp.astype(float)
    df[regions] = temp
    return df

def prepare_data(df):
    df_rate = df[['등록일'] + ['전국', '서울', '수도권'] + ['번호']]
    df_rate = df_rate[::-1]
    df_rate['월'] = df_rate['등록일'].str.replace('.', '').astype('datetime64[ns]').dt.month
    df_rate['년도'] = df_rate['등록일'].str.replace('.', '').astype('datetime64[ns]').dt.year
    return df_rate

def plot_data(df_rate):
    df_rate.groupby('월')[['전국','서울','수도권']].mean().plot(title="월별 추이 분석")
    plt.show()
    df_rate.groupby('년도')[['전국', '서울','수도권']].mean().plot(title="년도별 추이 분석")
    plt.show()

# 메인 실행 부분
df = fetch_data()
df = clean_data(df)
df_rate = prepare_data(df)
plot_data(df_rate)