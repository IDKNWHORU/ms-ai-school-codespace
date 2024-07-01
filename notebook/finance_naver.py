# pandas 이용
import pandas as pd
import matplotlib.pyplot as plt
import warnings
import streamlit as st

warnings.filterwarnings("ignore")

def get_exchange_date_date(code, currency_name):
    df = pd.DataFrame()

    for page_num in range(1, 13) :
        base_url = f"https://finance.naver.com/marketindex/exchangeDailyQuote.naver?marketindexCd=FX_{code}KRW&page={page_num}"
        temp = pd.read_html(base_url, encoding="cp949", header=1)
        
        df = pd.concat([df, temp[0]])
    
    total_rate_data_view(df, code, currency_name)

def total_rate_data_view(df, code, currency_name):
    plt.rc("font", family="Malgun Gothic")

    # 원하는 열만 선택    
    df_total = df[["날짜", "매매기준율", "사실 때", "파실 때", "보내실 때", "받으실 때"]]
    st.subheader(f"{currency_name}: {code}")
    st.dataframe(df_total.head(20))
    # 차트 작성
    df_total_chart = df_total.copy()
    df_total_chart = df_total_chart.set_index("날짜")

    # 최신 데이터와 과거 데이터의 순서를 바꿈, 역순으로 표시함
    df_total_chart = df_total_chart[::-1]

    ax = df_total_chart["매매기준율"].plot(figsize=(15,6),title="exchange rate")
    fig = ax.get_figure()
    st.pyplot(fig)
    # plt.show()
#     month_rate_data_view(df_total)

# def month_rate_data_view(df_total):
#     #월별 검색
#     df_total["날짜"] = df_total["날짜"].str.replace(".", "").astype("datetime64[ms]")

#     # 월 파생변수 생성
#     df_total["월"] = df_total["날짜"].dt.month
#     month_in = int(input("검색할 월 입력"))
#     month_df = df_total.loc[(df_total["월"]==month_in), ["날짜", "매매기준율", "사실 때", "파실 때", "보내실 때", "받으실 때"]]
#     month_df = month_df[::-1].reset_index(drop=True)

#     month_df_chart = month_df.copy()
#     month_df_chart = month_df_chart.set_index("날짜")

#     print(f"==={currency_names[code_in-1]}({code})===")
#     print(month_df_chart.head(20))
#     month_df_chart["매매기준율"].plot(figsize=(15,6))
#     plt.show()

def exchange_main():
    currency_symbols_names = {"미국 달러": "USD", "유럽 연합 유로": "EUR", "일본 엔화(100)": "JPY"}
    currency_name = st.selectbox("통화유형 선택", currency_symbols_names.keys())
    code = currency_symbols_names[currency_name]
    
    clicked = st.button("환율 데이터 가져오기")
    if clicked:
        get_exchange_date_date(code, currency_name)

if __name__=="__main__":
    exchange_main()