from transformers import TFAutoModel, pipeline
import pandas as pd

model_name = "final_model_3"
tf_model = TFAutoModel.from_pretrained(model_name, from_pt=True)
classifier = pipeline(task= 'sentiment-analysis', model= "final_model_3")

df = pd.read_csv('place_info_final_1217.csv')
file_list = df.loc[:,'file_name_1'].to_list()

i = int(input('請輸入開始編號:'))
j = int(input('請輸入結束編號:'))
file_list = df.loc[i:j,'file_name_1'].to_list()
print(f'開始運行，將從第{str(i)}筆資料繼續')
for file in file_list:
    df_review = pd.read_csv(f'review_clean_res_att/{file}.csv')
    review_result = classifier(df_review['review_text'].to_list())
    ans = []
    for d in review_result:
        answer = int(d['label'][5])
        ans.append(answer)
    model_rating = round(sum(ans)/len(ans),1)
    df_subset = df.loc[df['file_name_1'] == file]
    df_subset.loc[:,'model_rating'] = model_rating
    df_subset.to_csv('model_rating.csv', index=False, header=False, mode='a')
    print(f'第{i}筆完成，下次請從編號{i+1}開始輸入')
    i += 1
print('設定的範圍已執行完成')