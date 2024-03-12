import month_chart
import artist
import streamlit as st
from time import sleep
import pandas as pd
import json
# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.font_manager import FontProperties

file_path = 'melon_2024_3_top100.json'
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

#とりあえず全部数字型に変えとく     
# df = pd.DataFrame(data)
# df['year'] = pd.to_numeric(df['year'])
# df['month'] = pd.to_numeric(df['month'])
# df['rank'] = pd.to_numeric(df['rank'])
# df['year_month'] = df['year'].astype(str) + '/' + df['month'].astype(str)
# df['artist'] = df['artist'].apply(lambda x: ''.join(x) if isinstance(x, list) else x)
# df['artist'] = df['artist'].str.replace('방탄소년단', 'BTS(방탄소년단)')
# df["artist"] = df["artist"].str.replace("세븐틴","SEVENTEEN(세븐틴)")


@st.cache_data
def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    df = pd.DataFrame(data)
    df['month'] = pd.to_numeric(df['month'])
    df['rank'] = pd.to_numeric(df['rank'])
    df['year_month'] = df['year'].astype(str) + '/' + df['month'].astype(str)
    df['artist'] = df['artist'].apply(lambda x: ''.join(x) if isinstance(x, list) else x)
    df['artist'] = df['artist'].str.replace('방탄소년단', 'BTS(방탄소년단)')
    df["artist"] = df["artist"].str.replace("세븐틴","SEVENTEEN(세븐틴)")
    return df

file_path = 'melon_2024_3_top100.json'
df = load_data(file_path)


menu_selection = st.sidebar.selectbox(
    "メニュー",
    [ "MelonチャートTOP100 月間推移","アーティスト詳細", "年別ランキング","ソースコードと利用規約"]
)



if 'page_switched' not in st.session_state:
    st.session_state.page_switched = "home"
if "page_switched_artist" not in st.session_state:
    st.session_state.page_switched_artist="home"
if "pagego" not in st.session_state:
    st.session_state.pagego = "home"
 
if menu_selection == "アーティスト詳細" :
    if st.session_state.page_switched_artist == "home":
        artist.artist_home(df)
    elif st.session_state.page_switched_artist =="home_next":
        month_chart.artist_next(df)
    
    
    
elif menu_selection == "MelonチャートTOP100 月間推移" :
    if st.session_state.page_switched == "home":
        month_chart.home(df)
    elif st.session_state.page_switched =="home_next" :
        month_chart.home_next(df)
    elif st.session_state.page_switched == "artist":
        artist.artist_about(df)

elif menu_selection == "年別ランキング":
    artist.ranking(df)

# ユーザーによる選択がある場合、その選択をセッションステートに保存
elif menu_selection == "ソースコードと利用規約":
    st.title("ソースコード")
    st.write("[github](https://github.com/shimaf4979/chart_comparison)にて公開しております。")
    st.write("")
    st.header("利用規約")
    st.header("第1条（権利について）")
    st.write("1. 当ウェブサイトにて公開されるチャート情報に関わる全ての知的財産権は、音楽配信プラットフォーム[Melon](https://www.melon.com/index.htm)が保有しています。")
    st.write("2. 本サイトに掲載される各楽曲及びアルバムに係る知的財産権は、該当するアーティストの所属事務所、及び所属アーティストが保有しています")
    st.write("3. 本ウェブサイトは非営利目的で運営されており、いかなる形での収益化を目指しておらず、提供される情報やサービスは利用者の便宜を図るためのものです。")

    st.header("第2条（利用目的について）")
    st.write("当サイトの利用目的は、チャート情報をわかりやすく可視化し、利用者が情報を容易に理解できるようにすることにあります。当サイトは、利用者による情報の利用を支援することを目的としていますが、情報の正確性や完全性を保証するものではありません。")


    st.header("第3条（利用規約の変更）")
    st.write("当サイトは、必要に応じて利用規約を変更することがあります。利用規約が変更された場合、変更後の利用規約が当サイト上で公開されることにより、効力を発生します。利用者は定期的に利用規約を確認し、変更内容を把握する責任を負います。")
    




