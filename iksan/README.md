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

