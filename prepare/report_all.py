import os
import re
import tqdm
import warnings
import pandas as pd

warnings.simplefilter("ignore")

class ReportInfo:
    # skip_row = 2
    #
    # def __str__(self):
    #     return f"ReportInfo: skip_row = {self.skip_row}"
    pass


def preprocess(folders_path, report):
    folder_name = os.path.join(folders_path, rf"origin\{report.dir_name}")

    output_dir = os.path.join(folders_path, rf"report\{report.dir_name}")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filenames = [x for x in os.listdir(folder_name) if x.endswith(".xlsx")]

    empty_list = []
    for filename in filenames:
        df = pd.read_excel(os.path.join(folder_name, filename))
        year = df.loc[0].to_list()[0].split(",")[0]
        year = re.sub(r'[^0-9]', '', year)
        if report.columns is None:
            df = df.rename(columns=df.loc[1])
        else:
            df.columns = report.columns
        df = df.drop(df.index[0:report.skip_row])
        df['year'] = year
        if df.empty:
            empty_list.append(year)
        else:
            df.to_csv(os.path.join(output_dir, f"맥류작황보고서_{report.item_name}_{year}.csv"), encoding='cp949', index=False)

    print(report.item_name, empty_list)


def check_year_output_dir(output_dir):
    dir_list = [name for name in os.listdir(output_dir) if os.path.isdir(os.path.join(output_dir, name))]

    full_year_list = set(range(1968, 2023 + 1))
    found_years = []
    for each_dir in dir_list:
        file_list = [x for x in os.listdir(os.path.join(output_dir, each_dir)) if x.endswith(".csv")]
        for filename in file_list:
            found_years.append(int(filename[-8:-4]))

        print(each_dir, full_year_list - set(found_years))

def main():
    folders_path = r"Z:\Projects\2302_2306_wheat_report"


    print("*******empty_list*******")
    # 수당립수,간중
    report = ReportInfo()
    report.columns = None
    report.dir_name = "count"
    report.item_name = "수당립수,간중"
    report.skip_row = 2
    preprocess(folders_path, report)

    # 경수,유효경비율,수수
    report = ReportInfo()
    report.columns = ['맥종', '지역', '재배조건', '품종', '년도', '경수(cm)_12월10일', '경수(cm)_2월20일', '경수(cm)_3월20일', '경수(cm)_4월10일',
                      '경수(cm)_5월1일', '유효경비율(%)', '수수(개/m2)']
    report.dir_name = "fruitful"
    report.item_name = "경수,유효경비율,수수"
    report.skip_row = 3
    preprocess(folders_path, report)

    # 출수기 생장량
    report = ReportInfo()
    report.columns = None
    report.dir_name = "growth"
    report.item_name = "출수기_생장량"
    report.skip_row = 2
    preprocess(folders_path, report)

    # 초장간장
    report = ReportInfo()
    report.columns = ['맥종', '지역', '재배조건', '품종', '년도', '초장(cm)_12월10일', '초장(cm)_2월20일', '초장(cm)_3월20일', '초장(cm)_4월10일',
                      '초장(cm)_5월1일', '간장(cm)']
    report.dir_name = "length"
    report.item_name = "초장간장"
    report.skip_row = 3
    preprocess(folders_path, report)

    # 재배법
    report = ReportInfo()
    report.columns = ['시험년도', '지역', '맥종', '품종', '재배조건', '파폭', '시비량_기비_N', '시비량_기비_K20', '시비량_기비_P205',
                      '시비량_추비_N', '파종기', '파종량', '휴폭(cm)']
    report.dir_name = "method"
    report.item_name = "재배법"
    report.skip_row = 4
    preprocess(folders_path, report)

    # 1회차
    report = ReportInfo()
    report.columns = None
    report.dir_name = "method_1"
    report.item_name = "1회차(12_10 조사,제1회 보고)"
    report.skip_row = 2
    preprocess(folders_path, report)

    # 2회차
    report = ReportInfo()
    report.columns = None
    report.dir_name = "method_2"
    report.item_name = "2회차(2_20 조사,제2회 보고)"
    report.skip_row = 2
    preprocess(folders_path, report)

    # 3회차
    report = ReportInfo()
    report.columns = None
    report.dir_name = "method_3"
    report.item_name = "3회차(3_20 조사,제3회 보고)"
    report.skip_row = 2
    preprocess(folders_path, report)

    # 4회차
    report = ReportInfo()
    report.columns = None
    report.dir_name = "method_4"
    report.item_name = "4회차(4_10 조사,중간생육점검)"
    report.skip_row = 2
    preprocess(folders_path, report)

    # 5회차
    report = ReportInfo()
    report.columns = None
    report.dir_name = "method_5"
    report.item_name = "5회차(4_30 조사,제4회 보고)"
    report.skip_row = 2
    preprocess(folders_path, report)

    # 6회차
    report = ReportInfo()
    report.columns = None
    report.dir_name = "method_6"
    report.item_name = "6회차(5_20 조사,제5회 보고)"
    report.skip_row = 2
    preprocess(folders_path, report)

    # 7회차
    report = ReportInfo()
    report.columns = None
    report.dir_name = "method_7"
    report.item_name = "7회차(6_20 조사,제6회 보고)"
    report.skip_row = 2
    preprocess(folders_path, report)

    # 생육시기
    report = ReportInfo()
    report.columns = None
    report.dir_name = "stage"
    report.item_name = "생육시기"
    report.skip_row = 2
    preprocess(folders_path, report)

    # 생육시기
    report = ReportInfo()
    report.columns = None
    report.dir_name = "yield"
    report.item_name = "수량"
    report.skip_row = 2
    preprocess(folders_path, report)

    print("\n*******found_years*******")
    check_year_output_dir(os.path.join(folders_path, "report"))

    origin_list = [name for name in os.listdir(os.path.join(folders_path, "origin")) if os.path.isdir(os.path.join(os.path.join(folders_path, "report"), name))]
    report_list = [name for name in os.listdir(os.path.join(folders_path, "report")) if os.path.isdir(os.path.join(os.path.join(folders_path, "report"), name))]

    print("\n*******check_success*******")
    print(len(origin_list))
    print(len(report_list))


if __name__ == '__main__':
    main()