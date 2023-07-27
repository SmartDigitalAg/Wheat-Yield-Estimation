### [Input](input)
- [통계청 밀 생산량 데이터](input/kosis_wheat)
- [한국행정구역분류.xlsx](input/한국행정구역분류.xlsx): 행정구역 영문표기
- [지점코드.xlsx](input/지점코드.xlsx): 기상데이터 불러오기 위한 측구소 정보
- [맥류작황보고서_정보.xlsx](input/맥류작황보고서_정보.xlsx)
- [NDVI_EVI_KOREA.csv](input/NVI_EVI_KOREA.csv): Google Earth Engine에서 얻은 맥류작황보고서 지역의 NDVI, EVI 값

### [prepare](prepare)
데이터 수집 전 필요한 처리
- [prepare/report_all.py](prepare/report_filename/report_all.py)
  - ```공유드라이브```에서 처리 
  - 맥류작황보고서 파일명에 연도 추가

- [prepare/cache_weather.py](prepare/cache_weather.py)
  - ```output/cache_weather```
  - 기상 데이터 수집
  - 교수님API 또는 공공데이터포털API 사용

### [preprocess](preprocess)
수집한 데이터를 한 파일로 정리
- [preprocess/preprocess_kosis.py](preprocess/preprocess_kosis.py)
  - ```output/kosis ```
  - 통계청에서 수집한 밀 생산량 xlsx 파일의 형식을 통일
- [preprocess/preprocess_weather.py](preprocess/preprocess_weather.py)
  - ```output/weather```
  - 기상데이터 재배기간 고려해 정리 및 요약
- [preprocess/preprocess_report.py](preprocess/preprocess_report.py)
  - ```output/report```
  - 맥류작황보고서 한 파일로 정리
  - 재배조건별/지역별/품종별 생산량 파일 생성
- [preprocess/preprocess_cropmodel.py](preprocess/preprocess_cropmodel.py)
  - ```output/cropmodel```
  - 작물모델(DSSAT, AquaCrop) 결과를 한 파일로 정리

### [generate_input](generate_input)
[작물모델에 들어갈 기상 파일](https://github.com/EthanSeok/Crop_model_preprocessing/tree/main)/머신러닝에 들어갈 파일 생성
- [generate_input/input_kosis.py](generate_input/input_kosis.py)
  - ```output/input_kosis```
  - target: kosis 생산량
- [generate_input/input_report.py](generate_input/input_report.py)
  - ```output/input_report```
  - target: 맥류작황보고서 생산량

### [models](models)
수집한 데이터로 밀 생산량을 예측하기 위한 모델

모든 모델의 결과는 ```output/model_result```에서 csv 형식으로 score와 png 형식으로 산점도 확인

- [models/app.py](models/app.py)
  - ```streamlit run models/app.py```
  - 변수간 상관관계 확인을 위한  streamlit 앱
- [models/linear_model.py](models/linear_model.py)
  - sklearn의 LinearRegression을 사용한 모델
- [models/randomforest_model.py](models/randomforest_model.py)
  - sklearn의 RandomForestRegressor을 사용한 모델
- [models/xgb_model.py](models/xgb_model.py)
  - xgboost의 XGBRegressor을 사용한 모델
- [models/all.py](models/models_kosis.py)
  - LinearRegression, RandomForestRegressor, XGBRegressor 한 번에 돌리는 코드