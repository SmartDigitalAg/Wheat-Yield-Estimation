import pandas as pd
import os
import tqdm
import time
import json
import requests
from urllib.parse import quote_plus, urlencode

def load_weather(stn_Ids):
    '''
    교수님 API에서 한 파일로 기상데이터 불러옴
    지역마다 하나의 파일에 지정한 모든 연도의 기상데이터 담은 csv 파일 생성
    '''
    cache_dir = "../output/cache_weather"
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    cache_filename = os.path.join(cache_dir, f"all_{stn_Ids}.csv")
    if not os.path.exists(cache_filename):
        sy = 1967
        ey = 2023

        URL = f"https://api.taegon.kr/stations/{stn_Ids}/?sy={sy}&ey={ey}&format=csv"
        df = pd.read_csv(URL, sep='\\s*,\\s*', engine="python")

        df.to_csv(os.path.join(cache_dir, f"all_{stn_Ids}.csv"), index=False, encoding="utf-8-sig")

    else:
        pass

def load(stn_Ids):
    '''
    공공데이터포털 API에서 연도별 기상데이터 불러옴
    지역마다, 연도마다의 csv 파일 생성
    '''
    cache_dir = "../output/cache_weather"
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    url = 'http://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList'
    servicekey = 'HOhrXN4295f2VXKpOJc4gvpLkBPC/i97uWk8PfrUIONlI7vRB9ij088/F5RvIjZSz/PUFjJ4zkMjuBkbtMHqUg=='
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64)'
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132'
                             'Safari/537.36'}

    for y in range(2007, 2023):
        cache_filename = os.path.join(cache_dir, f"{stn_Ids}_{y}.csv")
        if not os.path.exists(cache_filename):
            params = f'?{quote_plus("ServiceKey")}={servicekey}&' + urlencode({
                quote_plus("pageNo"): "1",  # 페이지 번호 // default : 1
                quote_plus("numOfRows"): "720",  # 한 페이지 결과 수 // default : 10
                quote_plus("dataType"): "JSON",  # 응답자료형식 : XML, JSON
                quote_plus("dataCd"): "ASOS",
                quote_plus("dateCd"): "DAY",
                quote_plus("startDt"): f"{y}0101",
                quote_plus("endDt"): f"{y}1231",
                quote_plus("stnIds"): f"{stn_Ids}"
            })
            try:
                result = requests.get(url + params, headers=headers)
            except:
                time.sleep(2)
                result = requests.get(url + params, headers=headers)

            js = json.loads(result.content)
            weather = pd.DataFrame(js['response']['body']['items']['item'])

            weather['year'] = pd.to_datetime(weather['tm']).dt.year
            weather['month'] = pd.to_datetime(weather['tm']).dt.month
            weather['day'] = pd.to_datetime(weather['tm']).dt.day

            weather['d'] = pd.to_datetime(weather[['year', 'month', 'day']])
            weather['doy'] = weather['d'].dt.strftime('%j')

            # sumRn: 일강수량, sumGsr: 합계 일사량, sumSmlEv: 합계 소형증발량, avgTa: 평균기온, minTa: 최저기온, maxTa: 최고기온
            # avgTa: 평균기온, avgRhm: 평균상대습도, avgWs: 평균 풍속, sumSsHr: 합계 일조 시간
            #
            # 평균기온, 평균습도, 일조시간, 북위, 해발고도, 풍속계 높이(10) | 일사량, 최고기온, 최저기온, 강수량, 증발산량

            # li = ['year', 'day', 'sumGsr', 'maxTa', 'minTa', 'sumRn', 'sumSmlEv', 'avgTa', 'avgRhm', 'avgWs', 'avgTca', 'month']
            li = ['year', 'month', 'day', 'doy', 'sumGsr', 'maxTa', 'minTa', 'sumRn', 'sumSmlEv',
                  'avgTa', 'avgRhm', 'avgWs', 'sumSsHr']
            weather = weather.loc[:, li]
            weather = weather.apply(pd.to_numeric)
            weather.to_csv(cache_filename, index=False)
        else:
            pass

def main():
    info_df = pd.read_excel("../input/지점코드.xlsx")

    for idx, row in info_df.iterrows():
        try:
            print(row['지점코드'], row['지점명'])
            stn_Ids = row['지점코드']
            load_weather(stn_Ids)
            load(stn_Ids)
        except:
            print("error:", row['지점코드'], row['지점명'])


if __name__ == '__main__':
    main()
