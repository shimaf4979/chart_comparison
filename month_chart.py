import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import custom_styles_html
import json

def extract_url_part(url, substring):
    index = url.find(substring)
    if index != -1:
        # 見つかった場合、substringを含むその部分までを返す
        return url[:index + len(substring)]
    else:
        # substringが見つからない場合、元のURLをそのまま返すか、エラーを返す
        return

def home(df):
    html_content=custom_styles_html.custom_font_html()
    st.markdown(html_content,unsafe_allow_html=True)
    st.write("")
    st.markdown(f'<div class="stylish-text"><span style="font-size:14px">左上の>ボタンでメニュー選択できます！</span></div>', unsafe_allow_html=True)
    
    st.write("")
    st.write("")
    selected_alpha='すべてで検索する'
    
    if 'selected_artist' not in st.session_state:
        st.session_state['selected_artist'] = None
    if 'selected_song' not in st.session_state:
        st.session_state['selected_song'] = None 
        
        
            
    #検索条件
    alphabet = ['すべてで検索する'] + list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    selected_alpha = st.selectbox('アルファベットで絞り込む', alphabet)
    
  
    filter_type = st.radio(f"フィルタリングタイプを選択してください", ('アルファベットを含む', 'アルファベットで開始する'))
    if selected_alpha != "すべてで検索する":
        if filter_type == 'アルファベットを含む':
            filtered_df = df[df['artist'].str.contains(selected_alpha, na=False)]['artist'].unique()
        elif filter_type == 'アルファベットで開始する':
            filtered_df = df[df['artist'].str.startswith(selected_alpha)]['artist'].unique()
    else:
        filtered_df = df['artist'].unique()

    selected_artist = st.selectbox('アーティストを選択してください', sorted(filtered_df))
    artist_songs = df[df['artist'].apply(lambda x: selected_artist in x)]
    selected_song = st.selectbox('曲を選択してください', artist_songs['song'].unique())
    song_data = artist_songs[artist_songs['song'] == selected_song]   
    song_data_sorted = song_data.sort_values(by=['year', 'month'])   
    plt.figure(figsize=(10, 6))
    
    #サイズ、フォントの指定
    plot_points_count = len(song_data_sorted)
    font_size = max(15 - (plot_points_count // 8), 6)  
    marker_size = max(20 - (plot_points_count // 20), 2)  
    font_path = 'ipaexg.ttf'
    font_prop = FontProperties(fname=font_path)

    plt.figure(figsize=(10, 6))
    plt.plot(song_data_sorted['year'].astype(str) + '/' + song_data_sorted['month'].astype(str), song_data_sorted['rank'], marker='', linestyle='-', linewidth=2, color='skyblue')

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


    unique_months = song_data_sorted['year_month'].unique()
    month_labels = [f'{month}' for month in unique_months]

    plt.xticks(unique_months, labels=month_labels, fontsize=font_size,rotation=45)
    plt.yticks([1,10,20,30,40,50,60,70,80,90,100],fontsize=15)
    plt.ylim(-3,103)
    plt.gca().invert_yaxis()  # 1位を上に表示
    plt.xlabel('', fontproperties=font_prop)
    plt.ylabel('', fontproperties=font_prop)
    plt.title('月別順位推移', fontproperties=font_prop,fontsize=20)
    plt.legend()
    plt.grid(True, which='both', linestyle='--', linewidth=3, alpha=0.5)


    original_url = song_data['image'].iloc[0]
    processed_url = extract_url_part(original_url, "melon/")
    col10, col1 = st.columns(2)
    selected_song_info = song_data_sorted[song_data_sorted['song'] == selected_song].iloc[0]
    song_name = selected_song_info['song']
    artist_name = selected_song_info['artist']
    album_name = selected_song_info['album']
    # 順位推移の情報を整理
    rank_transitions = song_data_sorted[song_data_sorted['song'] == selected_song]
    rank_list = rank_transitions.apply(lambda x: f"{x['year']}/{x['month']} {x['rank']}位", axis=1).tolist()

    col1.markdown(f'<div class="stylish-text"> <span class="black">{song_name}<span> <span class="highlight">#{ranks.min()} (Highest)<span></div>', unsafe_allow_html=True)
    col1.markdown(f'<div class="stylish-text">Artist: <span class="black">{artist_name}<span></div>', unsafe_allow_html=True)
    col1.markdown(f'<div class="stylish-text">Album: <span class="black">{album_name}<span></div>', unsafe_allow_html=True)    
    if col1.button("アーティストの詳細を確認"):
        st.session_state['selected_artist'] = selected_artist
        st.session_state.page_switched = "artist"
        st.experimental_rerun()

    with col1.expander("順位推移を見る"):
        for rank in rank_list:
            st.write(f"- {rank}")
    # 2つ目のカラムに画像を配置
    col10.image(processed_url, caption=f'{selected_song}', width=300)   
    st.pyplot(plt) 
       
    with st.expander("他の作品を見る"):
        # 選択されたアーティストの他の曲を抽出（選択された曲を除外）
        other_songs = df[(df['artist'].apply(lambda x: selected_artist in x)) & (df['song'] != selected_song)]
        # 表示された曲を追跡するためのリスト
        displayed_songs = [selected_song]
        # 他の曲の情報を表示する
        for _, row in other_songs.iterrows():
            songname = row['song']
            song_image_url = row['image']
            # すでに表示された曲を除外
            if songname not in displayed_songs:
                processed_url = extract_url_part(song_image_url, "melon/")
                col1, col2 = st.columns([1,1]) 
                if col1.button(songname):
                    st.session_state['selected_artist'] = selected_artist
                    st.session_state['selected_song'] = songname
                    st.session_state.page_switched = "home_next"
                    st.experimental_rerun()
                col2.image(processed_url, caption=songname, width=300) 
                # 表示された曲リストに追加
                displayed_songs.append(songname)
                

def home_next(df): 
    html_content=custom_styles_html.custom_font_html()
    st.markdown(html_content,unsafe_allow_html=True)
    st.write("")
    st.write("") 
    if 'selected_artist' not in st.session_state:
        st.session_state['selected_artist'] = None
    if 'selected_song' not in st.session_state:
        st.session_state['selected_song'] = None 
        
    
    if st.button("もう一度検索し直す"):
        st.session_state.page_switched="home"
        st.experimental_rerun() 
        
        

    selected_artist = st.session_state['selected_artist']
    artist_songs = df[df['artist'].apply(lambda x: selected_artist in x)]
    selected_song = st.session_state['selected_song']
    song_data = artist_songs[artist_songs['song'] == selected_song]   
    song_data_sorted = song_data.sort_values(by=['year', 'month'])
    plt.figure(figsize=(10, 6))
    
    #サイズ、フォントの指定
    plot_points_count = len(song_data_sorted)
    font_size = max(15 - (plot_points_count // 8), 6)  
    marker_size = max(20 - (plot_points_count // 20), 2)  
    font_path = 'ipaexg.ttf'
    font_prop = FontProperties(fname=font_path)

    plt.figure(figsize=(10, 6))
    plt.plot(song_data_sorted['year'].astype(str) + '/' + song_data_sorted['month'].astype(str), song_data_sorted['rank'], marker='', linestyle='-', linewidth=2, color='skyblue')

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


    unique_months = song_data_sorted['year_month'].unique()
    month_labels = [f'{month}' for month in unique_months]

    plt.xticks(unique_months, labels=month_labels, fontsize=font_size,rotation=45)
    plt.yticks([1,10,20,30,40,50,60,70,80,90,100],fontsize=15)
    plt.ylim(-3,103)
    plt.gca().invert_yaxis()  # 1位を上に表示
    plt.xlabel('', fontproperties=font_prop)
    plt.ylabel('', fontproperties=font_prop)
    plt.title('月別順位推移', fontproperties=font_prop,fontsize=20)
    plt.legend()
    plt.grid(True, which='both', linestyle='--', linewidth=3, alpha=0.5)


    original_url = song_data['image'].iloc[0]
    processed_url = extract_url_part(original_url, "melon/")
    col10, col1 = st.columns(2)
    selected_song_info = song_data_sorted[song_data_sorted['song'] == selected_song].iloc[0]
    song_name = selected_song_info['song']
    artist_name = ''.join(selected_song_info['artist'])
    album_name = selected_song_info['album']
    # 順位推移の情報を整理
    rank_transitions = song_data_sorted[song_data_sorted['song'] == selected_song]
    rank_list = rank_transitions.apply(lambda x: f"{x['year']}/{x['month']} {x['rank']}位", axis=1).tolist()

    col1.markdown(f'<div class="stylish-text"> <span class="black">{song_name}<span> <span class="highlight">#{ranks.min()} (Highest)<span></div>', unsafe_allow_html=True)
    col1.markdown(f'<div class="stylish-text">Artist: <span class="black">{artist_name}<span></div>', unsafe_allow_html=True)
    col1.markdown(f'<div class="stylish-text">Album: <span class="black">{album_name}<span></div>', unsafe_allow_html=True)
    if col1.button("アーティストの詳細を確認"):
        st.session_state['selected_artist'] = selected_artist
        st.session_state.page_switched = "artist"
        st.experimental_rerun()

    
    with col1.expander("順位推移を見る"):
        for rank in rank_list:
            st.write(f"- {rank}")
    col10.image(processed_url, caption=f'{selected_song}', width=300)
    #ここでグラフを表示
    st.pyplot(plt)

        
    with st.expander("他の作品を見る"):
        # 選択されたアーティストの他の曲を抽出（選択された曲を除外）
        other_songs = df[(df['artist'].apply(lambda x: selected_artist in x)) & (df['song'] != selected_song)]
        # 表示された曲を追跡するためのリスト
        displayed_songs = [selected_song]
        # 他の曲の情報を表示する
        for _, row in other_songs.iterrows():
            songname = row['song']
            song_image_url = row['image']
            # すでに表示された曲を除外
            if songname not in displayed_songs:
                processed_url = extract_url_part(song_image_url, "melon/")
                col1, col2 = st.columns([1,1]) 
                if col1.button(songname):
                    st.session_state['selected_artist'] = selected_artist
                    st.session_state['selected_song'] = songname
                    st.session_state.page_switched = "home_next"
                    st.experimental_rerun()
                col2.image(processed_url, caption=songname, width=300) 
                # 表示された曲リストに追加
                displayed_songs.append(songname)
                
                

def artist_next(df): 
    html_content=custom_styles_html.custom_font_html()
    st.markdown(html_content,unsafe_allow_html=True)
    st.write("")
    st.write("") 
    if 'selected_artist' not in st.session_state:
        st.session_state['selected_artist'] = None
    if 'selected_song' not in st.session_state:
        st.session_state['selected_song'] = None 
        
    
    if st.button("もう一度検索し直す"):
        st.session_state.page_switched_artist="home"
        st.experimental_rerun() 
        
        

    selected_artist = st.session_state['selected_artist']
    artist_songs = df[df['artist'].apply(lambda x: selected_artist in x)]
    selected_song = st.session_state['selected_song']
    song_data = artist_songs[artist_songs['song'] == selected_song]   
    song_data_sorted = song_data.sort_values(by=['year', 'month'])
    plt.figure(figsize=(10, 6))
    
    #サイズ、フォントの指定
    plot_points_count = len(song_data_sorted)
    font_size = max(15 - (plot_points_count // 8), 6)  
    marker_size = max(20 - (plot_points_count // 20), 2)  
    font_path = 'ipaexg.ttf'
    font_prop = FontProperties(fname=font_path)

    plt.figure(figsize=(10, 6))
    plt.plot(song_data_sorted['year'].astype(str) + '/' + song_data_sorted['month'].astype(str), song_data_sorted['rank'], marker='', linestyle='-', linewidth=2, color='skyblue')

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


    unique_months = song_data_sorted['year_month'].unique()
    month_labels = [f'{month}' for month in unique_months]

    plt.xticks(unique_months, labels=month_labels, fontsize=font_size,rotation=45)
    plt.yticks([1,10,20,30,40,50,60,70,80,90,100],fontsize=15)
    plt.ylim(-3,103)
    plt.gca().invert_yaxis()  # 1位を上に表示
    plt.xlabel('', fontproperties=font_prop)
    plt.ylabel('', fontproperties=font_prop)
    plt.title('月別順位推移', fontproperties=font_prop,fontsize=20)
    plt.legend()
    plt.grid(True, which='both', linestyle='--', linewidth=3, alpha=0.5)


    original_url = song_data['image'].iloc[0]
    processed_url = extract_url_part(original_url, "melon/")
    col10, col1 = st.columns(2)
    selected_song_info = song_data_sorted[song_data_sorted['song'] == selected_song].iloc[0]
    song_name = selected_song_info['song']
    artist_name = ''.join(selected_song_info['artist'])
    album_name = selected_song_info['album']
    # 順位推移の情報を整理
    rank_transitions = song_data_sorted[song_data_sorted['song'] == selected_song]
    rank_list = rank_transitions.apply(lambda x: f"{x['year']}/{x['month']} {x['rank']}位", axis=1).tolist()

    col1.markdown(f'<div class="stylish-text"> <span class="black">{song_name}<span> <span class="highlight">#{ranks.min()} (Highest)<span></div>', unsafe_allow_html=True)
    col1.markdown(f'<div class="stylish-text">Artist: <span class="black">{artist_name}<span></div>', unsafe_allow_html=True)
    col1.markdown(f'<div class="stylish-text">Album: <span class="black">{album_name}<span></div>', unsafe_allow_html=True)

    st.pyplot(plt)
    with col1.expander("順位推移を見る"):
        for rank in rank_list:
            st.write(f"- {rank}")
    col10.image(processed_url, caption=f'{selected_song}', width=300)
    #ここでグラフを表示
 

        
    with st.expander("他の作品を見る"):
        # 選択されたアーティストの他の曲を抽出（選択された曲を除外）
        other_songs = df[(df['artist'].apply(lambda x: selected_artist in x)) & (df['song'] != selected_song)]
        # 表示された曲を追跡するためのリスト
        displayed_songs = [selected_song]
        # 他の曲の情報を表示する
        for _, row in other_songs.iterrows():
            songname = row['song']
            song_image_url = row['image']
            # すでに表示された曲を除外
            if songname not in displayed_songs:
                processed_url = extract_url_part(song_image_url, "melon/")
                col1, col2 = st.columns([1,1]) 
                if col1.button(songname):
                    st.session_state['selected_artist'] = selected_artist
                    st.session_state['selected_song'] = songname
                    st.session_state.page_switched_artist = "home_next"
                    st.experimental_rerun()
                col2.image(processed_url, caption=songname, width=300) 
                # 表示された曲リストに追加
                displayed_songs.append(songname)
    
    