* RandomForest

![RF변수중요도](https://github.com/SmartDigitalAg/Wheat-Yield-Estimation/assets/93760723/433b9bd8-9a98-48c4-9658-b48e14aa6a0f)

```python
data_filename = '../output/iksan_data.csv'
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
    data_filename = '../output/iksan_data.csv'
    df = pd.read_csv(data_filename)
    df = df[df['반복'] != '평균']
    df['종자_생체중_수확'] = df['종자_생체중_수확'] * 25
    df = pd.get_dummies(df, columns=['조사지'], prefix='조사지')
```

MAE: 98.02 , R2score: 0.68, RMSE: 120.09

'엽록소함량(µmol/m2)_개화후4주', '간장(cm)_개화후2주', 'SPAD_분얼전기',  '군집(LAI)_개화기', '엽록소함량(µmol/m2)_개화후2주' + 조사지

![XGB예측](https://github.com/SmartDigitalAg/Wheat-Yield-Estimation/assets/93760723/9152075e-7413-4193-9233-54c54633b436)

