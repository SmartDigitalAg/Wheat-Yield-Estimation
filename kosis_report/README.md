### 통계청 & 국립식량과학원 맥류작황 수확량 예측

<details>
<summary>통계청 밀 생산량 데이터 수집 방법</summary>
<a href = "https://kosis.kr/statHtml/statHtml.do?orgId=101&tblId=DT_1ET0232&vw_cd=MT_ZTITLE&list_id=K1_19&seqNo=&lang_mode=ko&language=kor&obj_var_id=&itm_id=&conn_path=MT_ZTITLE">KOSIS</a> 링크에 접속

1. 검색창에 "지자체 기본통계"를 입력한다.
<img src="https://user-images.githubusercontent.com/93754504/180153807-2bdcce2e-6391-4ebe-a113-92f432d7d4d9.png"  width="100%" height="100%"/>

2. "지자체 기본통계" 폴더를 클릭하고 원하는 지역/세부지역/농림수산업 폴더를 클릭한다.
<img src="https://user-images.githubusercontent.com/93754504/180153946-1f39be56-ce00-4219-9419-efe4e2643c3c.png"  width="20%" height="20%"/>

3. "맥류 생산량" 혹은 "맥류" 파일을 클릭한 뒤 원하는 년도를 설정한다.
<img src="https://user-images.githubusercontent.com/93754504/180154222-b9e64ce2-733f-47a0-bb52-07ba4045a390.png" width="100%" height="100%"/>

4. 파일을 통일시키기 위해 행렬전환을 해준다. (행렬전환은 2타입으로 "강릉타입"과 "동해타입"이 있다.)
<img src="https://user-images.githubusercontent.com/93754504/180154222-b9e64ce2-733f-47a0-bb52-07ba4045a390.png" width="100%" height="100%"/>

4-1. 강릉타입
<figure class="half">
    <img src="https://user-images.githubusercontent.com/93754504/180154551-09fb85ae-20c3-4f77-94eb-9ccd7ce559e5.png" width="30%" height="30%"/>
    <img src="https://user-images.githubusercontent.com/93754504/180155266-a8b556a9-36ef-4462-b0aa-8339c8ca22db.png" width="60%" height="60%"/>
</figure>


4-2. 동해타입
<figure class="third">
  <img src="https://user-images.githubusercontent.com/93754504/180154726-31e9253c-a5c8-4847-8d95-202a63747985.png" width="30%" height="30%"/>
  <img src="https://user-images.githubusercontent.com/93754504/180154965-ab7ad691-59fd-466a-a12c-5c35b3fb463c.png" width="30%" height="30%"/>
  <img src="https://user-images.githubusercontent.com/93754504/180155277-1f8bcbe5-4042-45ad-8676-4f895e4f7130.png" width="60%" height="60%"/>
</figure>
</details>




---

[eda/app_kosis.py](./eda/app_kosis.py)

input > ```../../output/kosis_report/model_input/통계청_전국_기상.csv```

실행 > ```streamlit run kosis_report/eda/app_kosis.py```

---

[eda/app_report.py](./eda/app_report.py)

input > ```../../output/kosis_report/model_input/맥류작황보고서.csv```

실행 > ```streamlit run kosis_report/eda/app_report.py```


---

[models/models_kosis.py](./models/models_kosis.py)

input > ```../../output/kosis_report/model_input/통계청_전국_기상.csv```

output > ```../../output/kosis_report/model_result/model_results_kosis.xlsx```

---

[models/models_report.py](./models/models_report.py)

input > ```../../output/kosis_report/model_input/통계청_전국_기상.csv```

output > ```../../output/kosis_report/model_result/model_results_report.xlsx```