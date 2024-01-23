### 밀 작황 기상요인 분석

[01_preprocess_data.py](./01_preprocess_data.py)

want > re = 재정리, origin = 원본 (line 11)

input > ```../input/맥류작황보고서.xlsx```, ```../output/report/{want}_datas맥류작황보고서.csv```

output > ```../output/report_weather/{want}/*.csv```

작황데이터 + 기상요인과 이 데이터에서 재배조건별/지역별/품종별 생산량과 기초통계량 생성

- winter_temp: 파종~월동 전 온도 > 10월 ~ 2월 중순 => season_year를 기준으로
- vegetative_temp: 월동 후 영양생장기 온도 > 2월 하순 ~ 3월 중순
- spring_temp: 수잉기 온도 > 4월 상순 ~ 중순
- flowering_temp/rain: 출수기 및 개화기 온도와 강수량 > 4월 하순 ~ 5월 상순
- summer_temp/hrad: 등숙기 온도와 일조시간 > 5월


[02_analysis.py](./02_analysis.py)

input > ```../output/report_weather/맥류작황보고서_기상요인분석.csv```

![그림2](https://github.com/SmartDigitalAg/Wheat-Yield-Estimation/assets/93760723/5d8268f3-f532-43de-a8c7-61f2c365f68e)


[03_app.py](./03_app.py)

input > 

-------


<details>
<summary>용어 정리</summary>

- 수량구성요소(이삭수, 이삭당립수, 천립중)으로부터 수량(완전종실중) 추정
- 수량구성요소에 영향을 미치는 기상 요인 추정

   (1) 이삭수 : 파종~월동 전 온도, 월동 후 영양생장기 온도(2월 하순~3월 중순)

   (2) 이삭당립수 : 수잉기 온도(4월 상순~중순), 출수기 및 개화기 온도와 강수량(4월 하순~5월 상순)

   (3) 천립중 : 등숙기 온도와 일조시간(5월)

데이터의 날짜: 생육재생기(3월) 최고분얼기(4월) 출수기(5월) 성숙기(6월) 출현기(10월)

파종 > 출현 > 생육재생기 > 최고분얼기 > 출수기 > 성숙기

'출현기', '파종기', '출수시', '출수기', '출수전', '최고분얼기', '생육재생기', '성숙기'

월동: 분얼기

수잉기: 유수형성기 이후부터 이삭이 나오기 전

출수 개화기: 이삭이 지엽의 엽설 밖으로 나옴/이삭이 나온 후 약 3~7일에 꽃이 핌

등숙기: 개화, 수정한 뒤부터 종실이 완전히 익을 때까지의 과정
</details>