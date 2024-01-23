### 데이터 정리 및 수집

[save_weather.py](save_weather.py)

output > ```../output/cache_weather```/```../output/cache_kma```

- ```load_weather```: 김태곤 교수님 기상 API > 입력 기간을 한 파일로 저장

- ```load_kma```: 공공데이터포털 기상청 API > 입력 기간을 연도별로 저장

---

[organize_cropmodel.py](organize_cropmodel.py)

input > ```../input/apsim_results``` & ```../input/dssat_results```

output > ```../output/작물모델결과.csv```

맥류작황보고서의 지역의 기상 데이터를 사용해 APSIM, DSSAT을 돌린 결과 정리

---

[organize_kosis.py](organize_kosis.py)

input > ```../input/kosis_wheat```

output > ```../output/kosis```

통계청의 밀 생산량 데이터 같은 형식으로 정리

---

[report_all.py](report_all.py)

input > ```Z:\Projects\2302_2306_wheat_report\origin```

output > ```Z:\Projects\2302_2306_wheat_report\report```

맥류작황보고서 파일명에 검색 연도 추가

---

[report_organize.py](report_organize.py)

input > ```Z:\Projects\2302_2306_wheat_report\report```

output > ```../output/report/origin_concated, origin_datas ```

검색년도 기준으로 맥류작황보고서 하나의 파일로 정리 & 재배조건별/지역별/품종별 생산량 파일 생성

---
[report_reorganize.py](report_reorganize.py)

input > ```Z:\Projects\2302_2306_wheat_report\report```

output > ```../output/report/re_concated, re_datas ```

생육시기 기준으로 맥류작황보고서 하나의 파일로 정리 & 재배조건별/지역별/품종별 생산량 파일 생성
