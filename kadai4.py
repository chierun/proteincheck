import streamlit as st
import pandas as pd
import openpyxl
import random


st.header("タンパク質の目標量と目安を知ろう")
#1．目標量を知ろう
st.subheader("１．まずは目標摂取量を出してみよう！")
st.text("←←身体活動レベルとは日常の活動を、強度に応じて3段階に区分したもの")
st.text("←←[1 運動はしない(低い) 2 軽く運動(ふつう) 3 活発に活動(高い)]を選択して[実行]‼")

# input
age = st.sidebar.number_input("年齢を入力👶",min_value=0,max_value=120,value=40,step=1)
level = st.sidebar.selectbox("身体活動レベルを選択💪",[1,2,3])
gender = st.sidebar.selectbox("性別を選択👧",["女性","男性"])

# タンパク質摂取量のリスト（年齢 x レベル x 性別）
l = {#75歳以上
    (75, 2, "男性"): "79~105ｇ",
    (75, 3, "男性"): "規定なし",
    (75, 1, "女性"): "53~70ｇ",
    (75, 2, "女性"): "62~83ｇ",
    (75, 3, "女性"): "規定なし",
}
l1 = {#65-74years
    (65, 1, "男性"): "77~103ｇ",
    (65, 2, "男性"): "90~120ｇ",
    (65, 3, "男性"): "103~138ｇ",
    (65, 1, "女性"): "58~78ｇ",
    (65, 2, "女性"): "69~93ｇ",
    (65, 3, "女性"): "79~105ｇ",
}
l2 = {#50-64years
    (50, 1, "男性"): "77~110ｇ",
    (50, 2, "男性"): "91~130ｇ",
    (50, 3, "男性"): "103~148ｇ",
    (50, 1, "女性"): "58~83ｇ",
    (50, 2, "女性"): "68~98ｇ",
    (50, 3, "女性"): "79~113ｇ",
}
l3 = {#30-49years
    (30, 1, "男性"): "75~115ｇ",
    (30, 2, "男性"): "88~135ｇ",
    (30, 3, "男性"): "99~153ｇ",
    (30, 1, "女性"): "57~88ｇ",
    (30, 2, "女性"): "67~103ｇ",
    (30, 3, "女性"): "76~118ｇ",
}
l4 = {#18-29years
    (20, 1, "男性"): "75~115ｇ",
    (20, 2, "男性"): "86~133ｇ",
    (20, 3, "男性"): "99~153ｇ",
    (20, 1, "女性"): "57~88ｇ",
    (20, 2, "女性"): "65~100ｇ",
    (20, 3, "女性"): "75~115ｇ",
}

# process
if st.sidebar.button('実行',type='primary'):
    a = "目標量は‥　対応年齢外です  ごめんなさい"  # エラー対応
    if age > 74:
        key = (75, level, gender)  # 75歳以上の場合のキー
        if key in l:
            a = l[key]
    elif 75 > age > 64:
        key = (65, level, gender) 
        if key in l1:
            a = l1[key]
    elif 65 > age > 49:
        key = (50, level, gender) 
        if key in l2:
            a = l2[key]
    elif 50 > age > 29:
        key = (30, level, gender) 
        if key in l3:
            a = l3[key]
    elif 30 > age > 17:
        key = (20, level, gender) 
        if key in l4:
            a = l4[key]
    
    # output
    st.image("tanpaku.png", caption="↓↓↓あなたのタンパク質目標摂取量は？↓↓↓", use_column_width=False)
    st.markdown(f"### １日あたり{a}")
    st.text("「日本人の食事摂取基準（2020年）厚生労働省」準拠  （妊娠中・授乳中の方には対応していません）")
    st.text(" ※疾患によりタンパク質摂取制限が必要な場合もあります。治療中の疾患がある方は、主治医にご確認ください。")
    
#2.目安チェック
st.text("")
st.subheader("２．目標量がわかったら、次に今日の朝食チェック！")
st.text("どのくらいタンパク質を摂っているか確認しましょう")

#excel data　Pandasのread_excel関数、ファイルからデータを読み込みDataFrameオブジェクトとしてdfに格納
excel_file = 'tanpaku.xlsx'
df = pd.read_excel(excel_file)
values = df['品名'].tolist()
selected_keys = st.multiselect('今朝食べたものをすべて選択',values)
#↑df['品名']はDataFrame df内の特定の列（ここでは'品名'列）を取得
#.tolistはその列内に含まれる全ての品名を取得

total_value = df[df['品名'].isin(selected_keys)]['グラム数'].sum()
#df['品名'].isin(selected_keys)は、'品名'列の値がselected_keysの中に含まれる行をフィルタリング
#['グラム数']は、フィルタリングされた行から'グラム数'列を取得
#.sum()は、'グラム数'列の合計値を計算。つまり、ユーザーが選択した品名に対応するすべての'グラム数'の合計を計算

#output
with st.expander("あなたの摂ったタンパク質量をクリックして確認"):
  st.markdown(f"### 合計　約{total_value}g　🍴")
  st.text("「日本食品標準成分表2020年版」参照")
  st.text("※一般的には、このほか穀類や調味料等からも約20g/日摂取していると言われています")

#選んでいない品名からひとつをランダムにおススメする
  remaining_keys = [value for value in values if value not in selected_keys]
  recommend_keys = random.choice(remaining_keys)
  st.text(f"目標量めざして、まずは一品追加してみよう！今日は{recommend_keys}がおススメ✨")
