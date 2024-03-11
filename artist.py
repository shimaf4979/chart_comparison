import streamlit as st
import custom_styles_html 
import pandas as pd
import json
import month_chart

def artist_about(df):
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


    artist_rank_count = df['artist'].value_counts().reset_index()
    artist_rank_count.columns = ['artist', 'rank_count']
    song_rank_count = df['song'].value_counts().reset_index()
    song_rank_count.columns = ['song', 'rank_count']

    # 元のデータフレームにランクイン回数をマージ
    df_merged = pd.merge(df, artist_rank_count, on='artist')
    df_merged = pd.merge(df_merged, song_rank_count, on='song', suffixes=('_artist', '_song'))

    # カスタムランキングロジック関数
    def custom_rank_artist(series):
        unique_counts = series.value_counts().sort_index(ascending=False)
        rank = 1
        ranks = {}
        for count, num_items in unique_counts.items(): # ここを修正
            ranks[count] = rank
            rank += int(num_items/count)
        return series.map(ranks)
    
    def custom_rank_songs(series):
        unique_counts = series.value_counts().sort_index(ascending=False)
        rank = 1
        ranks = {}
        for count, num_items in unique_counts.items(): # ここを修正
            ranks[count] = rank
            rank += num_items/count
        return series.map(ranks)
        

    # アーティストと曲のランキングを設定
    df_merged['rank_of_artist'] = custom_rank_artist(df_merged['rank_count_artist'])
    df_merged['rank_of_song'] = custom_rank_songs(df_merged['rank_count_song'])

    # 結果の表示
        
    st.markdown(f'<div class="stylish-text">Artist: <span class="black">{selected_artist}<span></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="stylish-text">Artist Rank:<span> <span class="black">#{df_merged[df_merged["artist"] == selected_artist]["rank_of_artist"].min()} (of {df_merged["rank_of_artist"].max()})<span></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="stylish-text">Highest ranked:<span> <span class="black">#{int(df_merged[df_merged["artist"] == selected_artist]["rank_of_song"].min())} (of {int(df_merged["rank_of_song"].max())})<span></div>', unsafe_allow_html=True)
    
    
    
    song_rank=df_merged[df_merged["artist"] == selected_artist]["rank_of_song"].min()
    original_url = df_merged[(df_merged["rank_of_song"] == song_rank) & (df_merged["artist"] == selected_artist)]["image"].iloc[0]
    processed_url = month_chart.extract_url_part(original_url, "melon/")    
    st.image(processed_url, caption=f'{df_merged[(df_merged["rank_of_song"] == song_rank) & (df_merged["artist"] == selected_artist)]["song"].iloc[0]}',width=400)   
    
    with st.expander("作品一覧"):
        # 選択されたアーティストの他の曲を抽出（選択された曲を除外）
        other_songs = df[(df['artist'].apply(lambda x: selected_artist in x))]
        # 表示された曲を追跡するためのリスト
        displayed_songs = []
        # 他の曲の情報を表示する
        for _, row in other_songs.iterrows():
            songname = row['song']
            song_image_url = row['image']
            # すでに表示された曲を除外
            if songname not in displayed_songs:
                processed_url = month_chart.extract_url_part(song_image_url, "melon/")
                col1, col2 = st.columns([1,1]) 
                if col1.button(songname):
                    st.session_state['selected_artist'] = selected_artist
                    st.session_state['selected_song'] = songname
                    st.session_state.page_switched = "home_next"
                    st.experimental_rerun()
                col2.image(processed_url, caption=songname, width=300) 
                # 表示された曲リストに追加
                displayed_songs.append(songname)
    
    
    st.header("The List of CSV File")
    st.write(df_merged[df_merged['artist'].apply(lambda x: selected_artist in x)])
    
    
def artist_home(df):
    html_content=custom_styles_html.custom_font_html()
    st.markdown(html_content,unsafe_allow_html=True)
    st.markdown(f'<div class="stylish-text"><span style="font-size:15px">アーティストの検索<span></div>', unsafe_allow_html=True)
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
    
    artist_rank_count = df['artist'].value_counts().reset_index()
    artist_rank_count.columns = ['artist', 'rank_count']
    song_rank_count = df['song'].value_counts().reset_index()
    song_rank_count.columns = ['song', 'rank_count']

    # 元のデータフレームにランクイン回数をマージ
    df_merged = pd.merge(df, artist_rank_count, on='artist')
    df_merged = pd.merge(df_merged, song_rank_count, on='song', suffixes=('_artist', '_song'))

    # カスタムランキングロジック関数
    def custom_rank_artist(series):
        unique_counts = series.value_counts().sort_index(ascending=False)
        rank = 1
        ranks = {}
        for count, num_items in unique_counts.items(): # ここを修正
            ranks[count] = rank
            rank += int(num_items/count)
        return series.map(ranks)
    
    def custom_rank_songs(series):
        unique_counts = series.value_counts().sort_index(ascending=False)
        rank = 1
        ranks = {}
        for count, num_items in unique_counts.items(): # ここを修正
            ranks[count] = rank
            rank += num_items/count
        return series.map(ranks)
        

    # アーティストと曲のランキングを設定
    df_merged['rank_of_artist'] = custom_rank_artist(df_merged['rank_count_artist'])
    df_merged['rank_of_song'] = custom_rank_songs(df_merged['rank_count_song'])

    # 結果の表示
        
    st.markdown(f'<div class="stylish-text">Artist: <span class="black">{selected_artist}<span></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="stylish-text">Artist Rank:<span> <span class="black">#{df_merged[df_merged["artist"] == selected_artist]["rank_of_artist"].min()} (of {df_merged["rank_of_artist"].max()})<span></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="stylish-text">Highest ranked:<span> <span class="black">#{int(df_merged[df_merged["artist"] == selected_artist]["rank_of_song"].min())} (of {int(df_merged["rank_of_song"].max())})<span></div>', unsafe_allow_html=True)
    
    
    
    song_rank=df_merged[df_merged["artist"] == selected_artist]["rank_of_song"].min()
    original_url = df_merged[(df_merged["rank_of_song"] == song_rank) & (df_merged["artist"] == selected_artist)]["image"].iloc[0]
    processed_url = month_chart.extract_url_part(original_url, "melon/")    
    st.image(processed_url, caption=f'{df_merged[(df_merged["rank_of_song"] == song_rank) & (df_merged["artist"] == selected_artist)]["song"].iloc[0]}',width=400)   
    
    with st.expander("作品一覧"):
        # 選択されたアーティストの他の曲を抽出（選択された曲を除外）
        other_songs = df[(df['artist'].apply(lambda x: selected_artist in x))]
        # 表示された曲を追跡するためのリスト
        displayed_songs = []
        # 他の曲の情報を表示する
        for _, row in other_songs.iterrows():
            songname = row['song']
            song_image_url = row['image']
            # すでに表示された曲を除外
            if songname not in displayed_songs:
                processed_url = month_chart.extract_url_part(song_image_url, "melon/")
                col1, col2 = st.columns([1,1]) 
                if col1.button(songname):
                    st.session_state['selected_artist'] = selected_artist
                    st.session_state['selected_song'] = songname
                    st.session_state.page_switched_artist = "home_next"
                    st.experimental_rerun()
                col2.image(processed_url, caption=songname, width=300) 
                # 表示された曲リストに追加
                displayed_songs.append(songname)
    
    
    st.header("The List of CSV File")
    st.write(df_merged[df_merged['artist'].apply(lambda x: selected_artist in x)])
    
       


        
def ranking(df):
    html_content=custom_styles_html.custom_font_html()
    st.markdown(html_content,unsafe_allow_html=True)
    st.write("")
    
    
    file_path = 'melon_2024_3_top100.json'
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    #とりあえず全部数字型に変えとく     
    df = pd.DataFrame(data)
    df['year'] = pd.to_numeric(df['year'])
    df['month'] = pd.to_numeric(df['month'])
    df['rank'] = pd.to_numeric(df['rank'])
    df['year_month'] = df['year'].astype(str) + '/' + df['month'].astype(str)
    df['artist'] = df['artist'].apply(lambda x: ''.join(x) if isinstance(x, list) else x)
    
    artist_rank_count = df['artist'].value_counts().reset_index()
    artist_rank_count.columns = ['artist', 'rank_count']
    song_rank_count = df['song'].value_counts().reset_index()
    song_rank_count.columns = ['song', 'rank_count']

    # 元のデータフレームにランクイン回数をマージ
    df_merged = pd.merge(df, artist_rank_count, on='artist')
    df_merged = pd.merge(df_merged, song_rank_count, on='song', suffixes=('_artist', '_song'))

    # カスタムランキングロジック関数
    def custom_rank_artist(series):
        unique_counts = series.value_counts().sort_index(ascending=False)
        rank = 1
        ranks = {}
        for count, num_items in unique_counts.items(): # ここを修正
            ranks[count] = rank
            rank += int(num_items/count)
        return series.map(ranks)
    
    def custom_rank_songs(series):
        unique_counts = series.value_counts().sort_index(ascending=False)
        rank = 1
        ranks = {}
        for count, num_items in unique_counts.items(): # ここを修正
            ranks[count] = rank
            rank += num_items/count
        return series.map(ranks)
        

    # アーティストと曲のランキングを設定
    df_merged['rank_of_artist'] = custom_rank_artist(df_merged['rank_count_artist'])
    df_merged['rank_of_song'] = custom_rank_songs(df_merged['rank_count_song'])

    st.title('年別月間ランキング維持')

    # 年の選択肢を準備（すべて文字列型に変換）
    year_options = [str(year) for year in df_merged['year'].unique()]
    year_options.append('総合ランキング')
    year_options = sorted(year_options)  # 文字列としてソート

    # 年の選択ボックス
    selected_year = st.selectbox('年を選択してください:', year_options)
    
    overall_top_songs = df_merged.groupby('song').agg({'rank_count_song':'sum'}).reset_index().nlargest(50, 'rank_count_song')
    overall_top_artists = df_merged.groupby('artist').agg({'rank_count_artist':'sum'}).reset_index().nlargest(50, 'rank_count_artist')
    
    def display_stylish_text(rankings, rank_type='song'):
        i=0
        for index, row in rankings.iterrows():
            i+=1
            if rank_type == 'song':
                item = f"{row['song']} (Count: {row['rank_count_song']})"
            else:  # 'artist'
                item = f"{row['artist']} (Count: {row['rank_count_artist']})"
            st.markdown(f'<div class="stylish-text">{i}. <span class="black">{item}</span></div>', unsafe_allow_html=True)
            if rank_type=="song":
                original_url = df_merged[df_merged["song"]==row["song"]]["image"].iloc[0]
                processed_url = month_chart.extract_url_part(original_url, "melon/")    
                st.image(processed_url, caption=f'{row["song"]}',width=300)  
            else:
                original_url = df_merged[df_merged["artist"]==row["artist"]]["image"].iloc[0]
                processed_url = month_chart.extract_url_part(original_url, "melon/")    
                st.image(processed_url, caption=f'{row["artist"]}',width=300)  
                
                    

    # 選択された年が「総合ランキング」の場合の処理
    if selected_year == '総合ランキング':
        st.subheader("総合ランキングのトップ50曲")
        display_stylish_text(overall_top_songs)
        
        st.subheader("総合ランキングのトップ50アーティスト")
        display_stylish_text(overall_top_artists, rank_type='artist')
    else:
        # 選択された年に基づくトップ50曲とアーティストのフィルタリングと集計
        filtered_df = df_merged[df_merged['year'] == int(selected_year)]
        top_songs_by_year = filtered_df.groupby('song').agg({'rank_count_song':'sum'}).reset_index().nlargest(50, 'rank_count_song')
        top_artists_by_year = filtered_df.groupby('artist').agg({'rank_count_artist':'sum'}).reset_index().nlargest(50, 'rank_count_artist')

        # 結果の表示
        
        st.subheader(f"{selected_year}年のトップ50アーティスト")
        display_stylish_text(top_artists_by_year, rank_type='artist')
        st.subheader(f"{selected_year}年のトップ50曲")
        display_stylish_text(top_songs_by_year)
        

    
