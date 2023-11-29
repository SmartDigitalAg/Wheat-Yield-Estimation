#### 5차(드론데이터 + 생육조사데이터)
* 10반복만 사용(생체중/건조중 엑셀에서 오른쪽의 데이터 사용X)
* 생육조사 엑셀 시트에서 23.06.01(수확) 데이터는 input데이터에 포함되지 않음
* 드론데이터의 가장 마지막 열에 있는 yield(kg/10a)-drone_yield을 예측
* 총 80개의 데이터 사용
* iksan_10data.csv

1.1 RandomForest-drone 포함

* 변수중요도

![fig_RFimportance](https://github.com/SmartDigitalAg/Wheat-Yield-Estimation/assets/93760723/7b214652-acd8-4a55-ac38-0fead6b4d35d)

* 예측 결과(드론데이터 포함 top10)

CVI_개화기, NDRE_분얼후기, NDRE_개화후2주, GNDVI_분얼후기, 엽록소함량(µmol/m2)_개화기, GNDVI_개화후2주, 군집(LAI)_개화기, CVI_개화후2주, 초장(cm)_분얼전기, CVI_분얼전기, 시비, 관개, 파종

MAE: 45.46, R2score: 0.52, RMSE: 54.24

![RF_predict](https://github.com/SmartDigitalAg/Wheat-Yield-Estimation/assets/93760723/1c3075a1-405f-46cf-8474-fa46a2f19f11)

1.2 RandomForest-생육조사결과만
* 변수중요도

![fig_RFplantimportance](https://github.com/SmartDigitalAg/Wheat-Yield-Estimation/assets/93760723/9dca217f-da28-4062-ad3e-750afaebdfe0)

* 예측 결과(생육조사결과 top10 만)

엽록소함량(µmol/m2)_개화기, 간장(cm)_개화후4주, 군집(LAI)_개화후4주, 군집(LAI)_개화후2주, 군집(LAI)_개화기, LAI_분얼전기, 관개, 1수영화수_개화기, 엽록소함량(µmol/m2)_개화후2주, 수장(cm)_개화후2주, 시비, 관개, 파종

MAE: 52.15, R2score: 0.04, RMSE: 65.56

![image](https://github.com/SmartDigitalAg/Wheat-Yield-Estimation/assets/93760723/003f5cb5-2952-4919-b49d-3150a01fd929)

2.1 XGB-drone 포함

* 변수중요도

![fig_XGBimportance](https://github.com/SmartDigitalAg/Wheat-Yield-Estimation/assets/93760723/16472644-f3b3-487e-b17c-8593100057fb)

* 예측 결과(top10)

NDRE_분얼후기, 파종, CVI_개화기, CVI_분얼전기, 엽록소함량(µmol/m2)_개화기, GNDVI_분얼후기, CVI_개화후4주, RVI_분얼전기, NDVI_분얼전기, NDVI_개화기, 시비, 관개

MAE: 58.53, R2score: 0.52, RMSE: 72.2

![XGB_predict](https://github.com/SmartDigitalAg/Wheat-Yield-Estimation/assets/93760723/32ad4a34-3c14-4584-9415-92f159fe1b07)

* 예측결과(top10, max_depth=2, n_estimators=50, learning_rate=0.1, early_stopping_rounds=200)

NDRE_분얼후기, 파종, CVI_개화기, CVI_분얼전기, 엽록소함량(µmol/m2)_개화기, GNDVI_분얼후기, CVI_개화후4주, RVI_분얼전기, NDVI_분얼전기, NDVI_개화기, 시비, 관개

MAE: 46.24, R2score: 0.44, RMSE: 55.86

![XGB_predict](https://github.com/SmartDigitalAg/Wheat-Yield-Estimation/assets/93760723/1ca9890e-a50e-4974-b383-7cfdd933cdcd)

2.2 XGB-생육조사결과만

*  변수중요도

![fig_XGBplantimportance](https://github.com/SmartDigitalAg/Wheat-Yield-Estimation/assets/93760723/60323cc7-d0e8-4861-88ff-cbe6cf1d84c7)


* 예측결과(생육조사결과 top10, max_depth=2, n_estimators=50, learning_rate=0.1, early_stopping_rounds=200)

엽록소함량(µmol/m2)_개화기, 군집(LAI)_개화기, 군집(LAI)_개화후2주, 간장(cm)_개화후4주, 수장(cm)_개화후4주, 초장(cm)_분얼전기, SPAD_분얼후기, LAI_분얼후기, 엽록소함량(µmol/m2)_개화후2주, 군집(LAI)_개화후4주, 시비, 관개, 파종

MAE: 57.22, R2score: 0.11, RMSE: 67.85


![XGBplant_predict](https://github.com/SmartDigitalAg/Wheat-Yield-Estimation/assets/93760723/ba292f63-e39e-4359-9a17-57dc48f4ac47)


#### 4차(드론 데이터 생체중/건조중 반복에 대해  LAI 등 조사결과 10반복 병합)

* RandomForest

![fig_RFimportance](https://github.com/SmartDigitalAg/Wheat-Yield-Estimation/assets/93760723/db1fa326-04bf-42e0-a42c-bb03e25e8495)

* RandomForest-1(top10)

'간장(cm)_개화후2주', '군집(LAI)_개화후2주', 'SPAD_분얼전기', 'CVI_개화후2주', '엽록소함량(µmol/m2)_개화후4주', 'NDRE_개화기', '초장(cm)_분얼후기', '군집(LAI)_개화기', 'LAI_분얼전기', 'GNDVI_개화후2주'+관개/시비/파종

MAE: 95.32, R2score: 0.42, RMSE: 121.21

![RF_predict](https://github.com/SmartDigitalAg/Wheat-Yield-Estimation/assets/93760723/f98b67b6-c731-47de-9c27-5736816e407a)

* RandomForest-2(top3)

'간장(cm)_개화후2주', '군집(LAI)_개화후2주', 'SPAD_분얼전기' + 관개/시비/파종

4번부터 중요도가 확 낮아져서 top3만 넣어서 돌려봄

MAE: 88.14, R2score: 0.51, RMSE: 116.15

![RF_predict](https://github.com/SmartDigitalAg/Wheat-Yield-Estimation/assets/93760723/c9e4766d-2ff3-4697-9958-1ca342999732)


* XGB

![fig_XGBimportance](https://github.com/SmartDigitalAg/Wheat-Yield-Estimation/assets/93760723/b4d7caab-edfe-415f-b0ab-20495a98f442)

* XGB-1(top10)

'군집(LAI)_개화기', '엽록소함량(µmol/m2)_개화후4주', '유수길이(mm)_분얼전기', '엽록소함량(µmol/m2)_개화후2주', 'LAI_분얼후기', '간장(cm)_개화후2주', '초장(cm)_분얼전기', 'SPAD_분얼전기', '초장(cm)_분얼후기', '군집(LAI)_개화후2주'+ 관개/시비/파종

MAE: 86.75, R2score: 0.59 , RMSE: 114.41

![XGB_predict](https://github.com/SmartDigitalAg/Wheat-Yield-Estimation/assets/93760723/ddc8aba7-7fc2-40b2-adaa-cc42718e61c2)


* XGB-2(top4)

4번째 이후부터 중요도 확 낮아져서 4개만 사용해봄

'군집(LAI)_개화후2주', '초장(cm)_분얼후기', 'SPAD_분얼전기', '초장(cm)_분얼전기' + 관개/시비/파종

MAE: 86.31, R2score: 0.59, RMSE: 114.31

![XGB_predict](https://github.com/SmartDigitalAg/Wheat-Yield-Estimation/assets/93760723/b9857ffb-c8e6-43f1-91c0-04f772d05d87)


#### 3차(드론 데이터 X 생체중/건조중 반복에 대해  LAI 등 조사결과 10반복 병합)
변수 중요도에 따라 top 4 사용

데이터 전처리에서 실수로 드론 데이터 사용 X

XGB 4개만 중요하게 나타남

RF 처음에 10개 다 쓰고 XGB 4개만 써서 똑같이 해봤는데 4개만 사용했을 때 더 좋은 성능

* RandomForest

'간장(cm)_개화후2주', '군집(LAI)_개화후2주', 'SPAD_분얼전기', '엽록소함량(µmol/m2)_개화후4주' + 관개/시비/파종

MAE: 88.93m, R2score: 0.50, RMSE: 117.07

![RF importance](https://github.com/SmartDigitalAg/Wheat-Yield-Estimation/assets/93760723/08ff53b3-de89-46dd-a34d-70c6bdfa03bb)

![RF predict](https://github.com/SmartDigitalAg/Wheat-Yield-Estimation/assets/93760723/e0e66e84-11db-4835-acf6-77d5f55ebdb3)


* XGB

'군집(LAI)_개화후2주', '초장(cm)_분얼후기', 'SPAD_분얼전기', '초장(cm)_분얼전기' + 관개/시비/파종

MAE: 86.31, R2score: 0.59, RMSE: 114.31

![XGB importance](https://github.com/SmartDigitalAg/Wheat-Yield-Estimation/assets/93760723/8339cf68-d805-4799-9f22-117fa9f0508e)

![XGB predict](https://github.com/SmartDigitalAg/Wheat-Yield-Estimation/assets/93760723/9f25df1d-d73a-4fdd-9c1d-dec893cb092e)




#### 2차(드론 데이터 사용 O)
* RandomForest
![image](https://github.com/SmartDigitalAg/Wheat-Yield-Estimation/assets/93760723/6c9f868f-9889-478b-bb79-51c7f98d3648)

'간장(cm)_개화후2주', '군집(LAI)_개화후2주', 'NDVI_개화후4주',  'CVI_개화후4주', '엽록소함량(µmol/m2)_개화후2주', 'SPAD_분얼전기', 'NDRE_개화기' + 조사지

MAE: 90.49, R2score: 0.14, RMSE: 110.22

![image](https://github.com/SmartDigitalAg/Wheat-Yield-Estimation/assets/93760723/3a86dd66-ca87-43f4-b6ec-dca7c2e38190)

* XGB

![image](https://github.com/SmartDigitalAg/Wheat-Yield-Estimation/assets/93760723/f3a40937-8340-4941-97b4-acdff61e3671)

변수 중요도에 따라 드론 데이터 변수를 몇 개 추가하여 실행했고, 성능이 향상됨.

'간장(cm)_개화후2주', '군집(LAI)_개화후2주', 'NDVI_개화후4주',  'CVI_개화후4주', '엽록소함량(µmol/m2)_개화후2주' + 조사지

MAE: 95.69 , R2score: 0.74 , RMSE: 107.62

![XGB2차](https://github.com/SmartDigitalAg/Wheat-Yield-Estimation/assets/93760723/c466a68b-c7e4-4e86-93e6-fc1f727fa595)


#### 1차(드론 데이터 사용 X)
* RandomForest

![RF변수중요도](https://github.com/SmartDigitalAg/Wheat-Yield-Estimation/assets/93760723/433b9bd8-9a98-48c4-9658-b48e14aa6a0f)

```python
data_filename = '../output/iksan_data_all.csv'
df = pd.read_csv(data_filename)
df = df[df['반복'] != '평균']
df['종자_생체중_수확'] = df['종자_생체중_수확'] * 25
df = pd.get_dummies(df, columns=['조사지'], prefix='조사지')
df = df.dropna(axis=1)
```
MAE: 84.02, R2score: 0.47, RMSE: 98.29

 'SPAD_분얼전기', '간장(cm)_개화후2주', '군집(LAI)_개화후2주', '엽록소함량(µmol/m2)_개화후4주', '군집(LAI)_개화기' + 조사지

![RF예측](https://github.com/SmartDigitalAg/Wheat-Yield-Estimation/assets/93760723/6286bb0f-8e1d-41d2-8aff-8a06867d46b8)

* XGBoost

![XGB변수중요도](https://github.com/SmartDigitalAg/Wheat-Yield-Estimation/assets/93760723/be202115-5a3a-42a2-b73e-4520892892b0)

```python
    data_filename = '../output/iksan_data_all.csv'
df = pd.read_csv(data_filename)
df = df[df['반복'] != '평균']
df['종자_생체중_수확'] = df['종자_생체중_수확'] * 25
df = pd.get_dummies(df, columns=['조사지'], prefix='조사지')
```

MAE: 98.02 , R2score: 0.68, RMSE: 120.09

'엽록소함량(µmol/m2)_개화후4주', '간장(cm)_개화후2주', 'SPAD_분얼전기',  '군집(LAI)_개화기', '엽록소함량(µmol/m2)_개화후2주' + 조사지

![XGB예측](https://github.com/SmartDigitalAg/Wheat-Yield-Estimation/assets/93760723/9152075e-7413-4193-9233-54c54633b436)

