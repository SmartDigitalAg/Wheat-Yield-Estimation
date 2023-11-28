#### 3차(드론 데이터 생체중/건조중 반복에 대해  LAI 등 조사결과 10반복 병합)
변수 중요도에 따라 top 4 사용

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

