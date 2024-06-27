import requests as rq
from bs4 import BeautifulSoup

def get_weather_daum(location) : 
    search_query = location + '날씨'
    base_url = "https://search.daum.net/search?nil_suggest=btn&w=tot&DA=SBC&q="

    url = base_url + search_query

    rs_weather = rq.get(url).text
    soup_weather = BeautifulSoup(rs_weather, 'lxml')

    txt_temp = soup_weather.select_one('strong.txt_temp').text
    txt_weather = soup_weather.select_one('span.txt_weather').text

    dl_weather = soup_weather.select('dl.dl_weather>dd')
    [wind_speed, humidity, pm10] = [x.text for x in dl_weather]
    
    return txt_temp, txt_weather, wind_speed, humidity, pm10

location = input('조회할 동입력 >> ')
txt_temp, txt_weather, wind_speed, humidity, pm10 = get_weather_daum(location)

print(f'지역: {location}, 온도: {txt_temp}, 날씨: {txt_weather}, 현재 풍속: {wind_speed}, 현재 습도: {humidity}, 미세먼지: {pm10}')