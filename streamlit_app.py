import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import json

def extract_url_part(url, substring):
    # substringの位置を見つける
    index = url.find(substring)
    if index != -1:
        # 見つかった場合、substringを含むその部分までを返す
        return url[:index + len(substring)]
    else:
        # substringが見つからない場合、元のURLをそのまま返すか、エラーを返す
        return url  # または適切なエラーハンドリング
substring = "melon/"

menu_selection = st.sidebar.selectbox(
    "メニュー",
    ["ホーム", "MelonチャートTOP100 月間推移", "その他"]
)

# 選択に基づいてメイン画面の内容を変更
if menu_selection == "ホーム":
    st.write("### ホームページへようこそ！")
    st.write("### 左上の>ボタンをクリックして選択")
elif menu_selection == "MelonチャートTOP100 月間推移":

    file_path = 'melon_2024_3_top100.json'
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        
    df = pd.DataFrame(data)
    df['year'] = pd.to_numeric(df['year'])
    df['month'] = pd.to_numeric(df['month'])
    df['rank'] = pd.to_numeric(df['rank'])
    
    
    alphabet = ['すべてで検索する'] + list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    selected_alpha = st.selectbox('アルファベットで絞り込む', alphabet)
    df['artist'] = df['artist'].apply(lambda x: ''.join(x) if isinstance(x, list) else x)
    
    filter_type = st.radio(f"フィルタリングタイプを選択してください", ('アルファベットを含む', 'アルファベットで開始する'))


    if selected_alpha != "すべてで検索する":
        if filter_type == 'アルファベットを含む':
            filtered_df = df[df['artist'].str.contains(selected_alpha, na=False)]['artist'].unique()
        elif filter_type == 'アルファベットで開始する':
            filtered_df = df[df['artist'].str.startswith(selected_alpha)]['artist'].unique()
    else:
        filtered_df = df['artist'].unique()

    selected_artist = st.selectbox('アーティストを選択してください', sorted(filtered_df))

    # 選択されたアーティストの曲を抽出
    artist_songs = df[df['artist'] == selected_artist]
    selected_song = st.selectbox('曲を選択してください', artist_songs['song'].unique())

    # 選択された曲のデータを抽出
    song_data = artist_songs[artist_songs['song'] == selected_song]


    # 'month'を数値型に変換（既に数値型の場合は不要）
    song_data['month'] = pd.to_numeric(song_data['month'])
    # 'rank'を数値型に変換
 


    plt.style.use('seaborn-darkgrid')
    # グラフの描画
    plt.figure(figsize=(10, 6))


    df['year_month'] = df['year'].astype(str) + '/' + df['month'].astype(str)

    # 選択された曲のデータを抽出し、'year_month'でソート
    song_data = df[df['song'] == selected_song].copy()
    # song_data_sorted = song_data.sort_values('year_month')
    song_data_sorted = song_data.sort_values(by=['year', 'month'])
    
    # プロットするデータの数に基づいてフォントサイズとマーカーサイズを調整
    plot_points_count = len(song_data_sorted)
    font_size = max(15 - (plot_points_count // 8), 6)  # プロット点が多いほどフォントサイズを小さくする
    marker_size = max(20 - (plot_points_count // 20), 2)  # プロット点が多いほどマーカーサイズを小さくする
    font_path = 'ipaexg.ttf'
    font_prop = FontProperties(fname=font_path)

    # 各色ごとにデータを分けてプロットするためのリストを準備
    months = song_data_sorted['month'].values


    plt.figure(figsize=(10, 6))

    plt.plot(song_data_sorted['year'].astype(str) + '/' + song_data_sorted['month'].astype(str), song_data_sorted['rank'], marker='', linestyle='-', linewidth=2, color='skyblue')

    # 'ranks' の定義が必要です。前の説明を基に、ここで定義します。
    ranks = song_data_sorted['rank'].astype(int).values

    # 各順位範囲ごとに色を変えてプロット

    colors = [
        'DarkRed',        # 1. ダークレッド
        'Firebrick',      # 2. 暗いレンガ色の赤
        'Crimson',        # 3. 濃い赤紫色
        'DeepPink',       # 4. 深いピンク
        'PaleVioletRed',  # 5. 薄いバイオレットレッド
        'HotPink',        # 6. 鮮やかなピンク
        'Pink',           # 7. 標準的なピンク
        'LightPink',      # 8. 明るいピンク
        'MistyRose',      # 9. やや薄いピンク
        'LavenderBlush'   # 10. 非常に薄いピンク、ほぼ白に近い
    ]

    bounds = [
        (1, 10), (11, 20), (21, 30), (31, 40), (41, 50),
        (51, 60), (61, 70), (71, 80), (81, 90), (91, 100)
    ]


    for color_index, (lower, upper) in enumerate(bounds):
        condition = (ranks >= lower) & (ranks <= upper)
        filtered_indices = np.where(condition)[0]  # 条件に一致するインデックスを取得
        if len(filtered_indices) > 0:  # データがある場合のみプロット
            plt.plot(song_data_sorted['year_month'].iloc[filtered_indices], song_data_sorted['rank'].astype(int).iloc[filtered_indices], marker='o', linestyle='', markersize=marker_size, color=colors[color_index], label=f'{lower}-{upper}')
    # for lower, upper in bounds:
    #     # 正しい範囲内のデータのみ抽出（'ranks'と'song_data_sorted['month']'を使用）
    #     condition = (ranks >= lower) & (ranks <= upper)
    #     filtered_months = song_data_sorted['month'][condition]
    #     filtered_ranks = ranks[condition]
    #     if len(filtered_months) > 0:  # データがある場合のみプロット
    #         plt.plot(filtered_months, filtered_ranks, marker='o', linestyle='', markersize=20, color=colors[bounds.index((lower, upper))])

    # Y軸の設定
    plt.yticks([1,10,20,30,40,50,60,70,80,90,100],fontsize=15)
    plt.ylim(-3,103)
    plt.gca().invert_yaxis()  # 1位を上に表示

    unique_months = song_data_sorted['year_month'].unique()

    # 「年/月」形式のラベルを生成
    month_labels = [f'{month}' for month in unique_months]

    # X軸の目盛りラベルを設定
    plt.xticks(unique_months, labels=month_labels, fontsize=font_size,rotation=45)


    # 日本語フォントの設定

    plt.xlabel('', fontproperties=font_prop)
    plt.ylabel('', fontproperties=font_prop)
    plt.title('月別順位推移', fontproperties=font_prop,fontsize=20)
    plt.legend()

    plt.grid(True, which='both', linestyle='--', linewidth=3, alpha=0.5)
    # Streamlitにグラフを表示
    st.pyplot(plt)

    # 選択された曲の画像を表示
    # 元のURLをDataFrameから取得
    original_url = song_data['image'].iloc[0]

    # URLを加工する（"melon/" までの部分を抽出）
    processed_url = extract_url_part(original_url, "melon/")

    # 加工後のURLで画像を表示
    col1, col10 = st.columns(2)

    # 1つ目のカラムにテキストを配置
    # 選択された曲の基本情報を取得
    selected_song_info = song_data_sorted[song_data_sorted['song'] == selected_song].iloc[0]

    # 曲名
    song_name = selected_song_info['song']
    # アーティスト（リストから文字列へ変換）
    artist_name = ''.join(selected_song_info['artist'])
    # アルバム名
    album_name = selected_song_info['album']

    # 順位推移の情報を整理
    rank_transitions = song_data_sorted[song_data_sorted['song'] == selected_song]
    rank_list = rank_transitions.apply(lambda x: f"{x['year']}/{x['month']} {x['rank']}位", axis=1).tolist()

    # 順位推移を表示するコードの部分
    col1.write(f"### {song_name}")  # 曲名を表示
    col1.write(f"### Artist:  {artist_name}")
    col1.write(f"### Alubm:  {album_name}")
    
    with col1.expander("順位推移を見る"):
        st.write("### 順位推移:")
        for rank in rank_list:
            st.write(f"- {rank}")

    # 2つ目のカラムに画像を配置
    col10.image(processed_url, caption=f'{selected_song}', width=400)
    
        # "他の作品を見る"ボタンを追加
    # "他の作品を見る"ボタンを追加
    with st.expander("他の作品を見る"):
        # 選択されたアーティストの他の曲を抽出（選択された曲を除外）
        other_songs = df[(df['artist'].apply(lambda x: selected_artist in x)) & (df['song'] != selected_song)]

        # 表示された曲を追跡するためのリスト
        displayed_songs = [selected_song]

        # 他の曲の情報を表示する
        for _, row in other_songs.iterrows():
            song_name = row['song']
            song_image_url = row['image']

            # すでに表示された曲を除外
            if song_name not in displayed_songs:
                processed_url = extract_url_part(song_image_url, "melon/")
                col1, col2 = st.columns([1,1])  # 曲名のためのスペースと画像のためのスペースを調整
                col1.write(song_name)  # 曲名を表示
                col2.image(processed_url, caption=song_name, width=300)  # 画像を表示

                # 表示された曲リストに追加
                displayed_songs.append(song_name)


    
elif menu_selection == "その他":
    st.write("その他のコンテンツです。")

