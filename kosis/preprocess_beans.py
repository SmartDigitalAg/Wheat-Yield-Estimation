import os
import pandas as pd
import warnings
import re
warnings.filterwarnings("ignore")


def main():
    bean_dir = '두류생산량_원본'
    files = os.listdir(bean_dir)

    output_dir = './두류생산량_전처리'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 1.'경기도', '강원특별자치도', ... 등의 데이터는 제외하고 수행
    files = [file_name for file_name in files if len(file_name.split('_')) >= 3 and not re.match(r'^\d', file_name.split('_')[2])]

    for file in files:
        file_path = os.path.join(bean_dir, file)
        df = pd.read_excel(file_path)

        # 2. 데이터열을 제외하고 nan 값이 있으면 이전 행의 값을 읽어와서 채우기
        nan_cols = [col for col in df.columns if col != '데이터']
        df[nan_cols] = df[nan_cols].fillna(method='ffill')


        # 3. 읍면동열 or 행정구역열이 있으면 합계 행만 사용 -> 열이름에서 '읍면' or '행정구역'을 포함하는 열이 있는지 확인
        eup_hang = [col for col in df.columns if '읍면' in col or '행정' in col or '동별' in col]

        if eup_hang:
            eup_hang_col = eup_hang[0]
            df = df[(df[eup_hang_col] == '합계') | (df[eup_hang_col] == '합 계') | (df[eup_hang_col] == '전체')]
            df = df.drop(columns=[eup_hang_col])

        # 4. 항목: 면적, 생산량 등을 포함하는 열이 있는지 확인하고 'itm'으로 통일
        #         면적, 생산량 등이 없다면 그 데이터는 생산량만 있는 데이터이기 때문에 '항목'열을 만들고 그 열의 값을 모두 '생산량'으로 채움
        itm_col = [col for col in df.columns if any('면적' in s for s in df[col].astype(str).unique())]
        if itm_col:
            df = df.rename(columns={itm_col[0]:'itm'})
        else:
            df['itm'] = '생산량'

        # 5. 두류별: 콩, 팥 등을 포함하는 열이 있는지 확인하고 'crop'로 통일
        crop_col = [col for col in df.columns if any('콩' in s for s in df[col].astype(str).unique())]

        if crop_col:
            df = df.rename(columns={crop_col[0]:'crop'})

        df = df[['시점', 'crop', 'itm', '데이터']]
        df['시점'] = df['시점'].astype(int)
        df = df.rename(columns={'시점':'year', '데이터':'value'})

        df.to_csv(os.path.join(output_dir, file.replace('xlsx', 'csv')), index=False, encoding='utf-8-sig')

    print(len(os.listdir(output_dir)))
    print(len(files))



if __name__ == '__main__':
    main()