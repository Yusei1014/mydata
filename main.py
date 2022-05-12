import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image

st.title("Streamlit 超入門")
st.write("DataFrame")

df = pd.DataFrame({
    '1列目':[1,2,3,4],
    '2列目':[10,20,30,40]
})

#3種類の記述方法
st.table(df.style.highlight_max(axis=0))
st.dataframe(df.style.highlight_min(axis=0))

#折れ線グラフを作成する
df2 = pd.DataFrame(
    np.random.rand(20,3),
    columns=["a","b","c"]
)

"""
### 折れ線グラフ
"""

st.line_chart(df2)
st.bar_chart(df2)

#マップをプロットする??

df3 = pd.DataFrame(
    np.random.rand(100,2)/[50.50] + [35.69,139.70],
    columns=["lat","lon"] #latは緯度、lonは軽度
)

"""
### 新宿付近のマップをプロットしてみる
"""
st.map(df3)

#画像の表示をしてみる。
#チェックボックスを作成する 👉 チェックボックスはTrue/Folseとして利用することもできるのでif文で表示
if st.checkbox('Show Image'):
    img = Image.open("Sample.JPG")
    st.image(img,caption="urara",use_column_width=True)

option = st.selectbox(
    'あなたが好きな数字を教えて下さい',
    list(range(1,11))
)
'あなたが好きな数字は',option,'です。'

text = st.text_input('あなたの趣味を教えて下さい')

'あなたの趣味は',text,'です。'

#スライダーを用いる
condition = st.slider('あなたの今の調子は？',0,100,50)

'あなたの調子はは',condition,'％です。'


#レイアウトの追加を見ていきます！
#サイドバーニ表示させたいときは、.sidebarをstの後ろにつけるだけでOK！
#2カラム表示をしよう！
left_column , right_column = st.columns(2)
button = left_column.button('右カラムに文字を表示')
if button:
    right_column.write("ここは右カラムです。")

#expanderはアコーディオンブロックみたいな感じ！
expander = st.beta_expander('問い合わせ')
expander.write('問い合わせ内容を書く')

#プログラスバーを見ていくよ！