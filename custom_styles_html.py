#about html
def custom_font_html():
    return f"""
    <style>
    .custom-font {{
        font-size: 16px;
        background: linear-gradient(145deg, #ff79c6, #bd93f9);
        color: white;
        padding: 10px 20px;
        border-radius: 20px;
        box-shadow: 4px 4px 10px rgba(0, 0, 0, 0.5);
        display: inline-block;
    }}
    </style>
    
    <style>
    .stylish-text {{
        font-size: 20px;
        background: linear-gradient(145deg, #ff79c6, #bd93f9);
        color: white;
        padding: 10px 20px;
        border-radius: 20px;
        box-shadow: 4px 4px 10px rgba(0, 0, 0, 0.5);
        margin: 10px 0px;
        display: inline-block;
    }}
    .black{{
        color: #000000;
    }}
    .highlight {{
        color: #ED1A3D; /* ハイライト色 */
    }}
    </style>
    


    <div class="custom-font">
        Melonチャートで月間ランキングに載った曲を検索できます！
    </div>
    """