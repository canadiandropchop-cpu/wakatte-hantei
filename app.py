import streamlit as st
import pandas as pd
from thefuzz import process
import urllib.parse

# ==========================================
# 0. ページ設定
# ==========================================
st.set_page_config(
    page_title="【検証】wakatte.tv風 学歴判定機",
    page_icon="📺",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 1. CSS注入（wakatte.tv風 赤×青デザイン）
# ==========================================
def local_css():
    st.markdown("""
        <style>
        body {
            font-family: "Helvetica Neue", Arial, "Hiragino Kaku Gothic ProN", "Hiragino Sans", Meiryo, sans-serif;
        }
        .main-title {
            font-weight: 900;
            font-size: 3em !important;
            color: #FF0000; /* 赤 */
            text-align: center;
            text-shadow: 3px 3px 0px #0000FF; /* 青の影 */
            margin-bottom: 0px;
        }
        .sub-title {
            font-weight: bold;
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }
        .result-box {
            border: 4px solid #FF0000;
            background-color: #f8f9fa;
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 8px 8px 0px #0000FF; /* 青い影 */
            margin-top: 20px;
            margin-bottom: 20px;
        }
        .univ-name-display {
            color: #0000FF; /* 青 */
            font-weight: 900;
            font-size: 2.2em;
            margin-bottom: 10px;
        }
        .deviation-display {
             font-size: 1.2em;
             font-weight: bold;
             color: #555;
             margin-bottom: 20px;
        }
        .comment-display {
            font-weight: bold;
            font-size: 1.6em;
            color: #FF0000; /* 赤 */
            line-height: 1.4;
        }
        /* アフィリエイトリンクのスタイル */
        .affiliate-box {
            background-color: #fff0f5; /* 薄い赤背景 */
            border: 2px dashed #FF0000;
            border-radius: 10px;
            padding: 15px;
            text-align: center;
            margin-bottom: 20px;
        }
        .affiliate-text {
            color: #333;
            font-weight: bold;
            font-size: 0.9em;
            margin-bottom: 5px;
        }
        .affiliate-link {
            color: #0000EE;
            font-weight: 900;
            font-size: 1.1em;
            text-decoration: underline;
        }
        
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display:none;}
        </style>
    """, unsafe_allow_html=True)

local_css()

# ==========================================
# 2. データの読み込み
# ==========================================
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("university_data_dummy.csv")
        return df
    except FileNotFoundError:
        st.error("エラー: CSVファイルが見つかりません。")
        return pd.DataFrame()

df = load_data()

# ==========================================
# 3. ロジック（判定＆収益化）
# ==========================================
def get_comment(dev_val, univ_name):
    if "帝京平成" in univ_name:
        return "ここがすごい！帝京平成大学！<br>（言いたいだけ）"
    if "日本体育" in univ_name:
        return "筋肉は裏切らない。<br>偏差値なんて気にするな。"

    if dev_val >= 70:
        return "【神の領域】<br>あなたは日本の宝です。将来、我々を養ってください。"
    elif dev_val >= 65:
        return "【エリート】<br>すごいですね。でも東大には勝てませんよ？"
    elif dev_val >= 60:
        return "【上位層】<br>まあまあ賢い。でも、上には上がいます。"
    elif dev_val >= 55:
        return "【凡人】<br>THE 普通。量産型大学生として日本を支えてください。"
    elif dev_val >= 50:
        return "【ギリギリ】<br>日東駒専レベル。遊んでないで資格の一つでも取ったら？"
    else:
        return "【Fラン（仮）】<br>wakatte.tvならマイクを向けられないレベルです。<br>バイトリーダー目指して頑張れ。"

# ★追加機能：偏差値に応じた商品を提案する関数（マネタイズエンジン）
def get_affiliate_link(dev_val):
    # ※Amazonアソシエイトに登録後、ここのURLをあなた専用のアフィリエイトリンクに差し替えてください。
    # 現在は「Amazonの検索結果」に飛ぶようになっています。
    
    if dev_val >= 65:
        # 難関大レベル -> 東大・難関大対策
        url = "https://www.amazon.co.jp/s?k=%E6%9D%B1%E5%A4%A7+%E8%B5%A4%E6%9C%AC" # 「東大 赤本」の検索結果
        text = "調子に乗るな。この「赤本」を解いてから言え。👉 Amazonを見る"
    elif dev_val >= 55:
        # 中堅～上位 -> MARCHレベル
        url = "https://www.amazon.co.jp/s?k=MARCH+%E9%81%8E%E5%8E%BB%E5%95%8F" # 「MARCH 過去問」
        text = "今のままじゃ落ちるぞ？この問題集を完璧にしろ。👉 Amazonを見る"
    elif dev_val >= 45:
        # 平均前後 -> 基礎固め
        url = "https://www.amazon.co.jp/s?k=%E5%A4%A7%E5%AD%A6%E5%8F%97%E9%A8%93+%E8%8B%B1%E5%8D%98%E8%AA%9E" # 「大学受験 英単語」
        text = "悪いことは言わない。単語からやり直して出直してこい。👉 Amazonを見る"
    else:
        # 低偏差値 -> マンガでわかる系
        url = "https://www.amazon.co.jp/s?k=%E4%B8%AD%E5%AD%A6%E5%BE%A9%E7%BF%92" # 「中学復習」
        text = "マジでヤバいぞ。中学レベルから復習したほうがいい。👉 Amazonを見る"
    
    return url, text

# ==========================================
# 4. Web画面構築
# ==========================================
st.markdown('<h1 class="main-title">📺 WAKATTE.TV風<br>学歴判定機</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">あなたの大学名を入力してください。偏差値で人を判断します。</p>', unsafe_allow_html=True)

user_input = st.text_input("", placeholder="例：早稲田、京大、日大...")

# ★追加：文理選択のラジオボタン
bunri_choice = st.radio(
    "あなたの専攻（学部）は？",
    ("文系", "理系"),
    horizontal=True # 横並びにする
)

if st.button("判定する", type="primary"):
    if user_input and not df.empty:
        # 曖昧検索
        all_univ_names = df['University'].tolist()
        match_result = process.extractOne(user_input, all_univ_names)
        best_match_name = match_result[0]
        score = match_result[1]

        if score < 60:
            st.warning(f"「{user_input}」に近い大学が見つかりません。もっと正確に入力して！")
        else:
            row = df[df['University'] == best_match_name].iloc[0]
            base_deviation = row['Deviation']
            univ_type = row['Type'] # CSVにある 'National'(国公立) か 'Private'(私立) を取得
            
            # --- ★wakatteルール適用（補正ロジック） ---
            final_deviation = base_deviation
            bonus_message = []

            # ルール1: 国公立なら +5
            if univ_type == "National":
                final_deviation += 5
                bonus_message.append("国公立補正+5")
            
            # ルール2: 理系なら +5
            if bunri_choice == "理系":
                final_deviation += 5
                bonus_message.append("理系補正+5")

            # 補正後の値を表示用変数に入れる
            deviation = final_deviation
            
            # コメント取得（補正後の偏差値で判定）
            comment = get_comment(deviation, best_match_name)
            
            # 補正があった場合のみ表示するテキスト作成
            bonus_text_display = " ".join(bonus_message)
            if bonus_text_display:
                bonus_text_display = f"<span style='font-size:0.8em; color:#ff4b4b;'>（{bonus_text_display}）</span>"

            # --- 結果表示 ---
            st.markdown(f"""
            <div class="result-box">
                <div class="univ-name-display">{best_match_name} <span style="font-size:0.5em; color:#333;">({bunri_choice})</span></div>
                <div class="deviation-display">
                    判定偏差値: {int(deviation)} 
                    {bonus_text_display}
                </div>
                <div class="comment-display">{comment}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # --- 結果表示 ---
            st.markdown(f"""
            <div class="result-box">
                <div class="univ-name-display">{best_match_name}</div>
                <div class="deviation-display">（推定偏差値: {deviation}）</div>
                <div class="comment-display">{comment}</div>
            </div>
            """, unsafe_allow_html=True)

            # --- ★収益化ポイント（アフィリエイト誘導） ---
            aff_url, aff_text = get_affiliate_link(deviation)
            st.markdown(f"""
            <div class="affiliate-box">
                <div class="affiliate-text">🔥 あなたへの処方箋</div>
                <a href="{aff_url}" target="_blank" class="affiliate-link">
                    {aff_text}
                </a>
            </div>
            """, unsafe_allow_html=True)

            # --- 拡散機能 ---
            share_comment = comment.replace("<br>", "\n")
            share_text = f"【学歴判定結果】\n大学名：{best_match_name}（偏差値{deviation}）\n判定：「{share_comment.splitlines()[0]}」\n\n📺 wakatte.tv風 学歴判定機\n#学歴フィルター #wakatte_tv"
            
            encoded_text = urllib.parse.quote(share_text)
            share_url = f"https://twitter.com/intent/tweet?text={encoded_text}&url="

            st.markdown(f"""
            <div style="text-align: center; margin-top: 10px;">
                <a href="{share_url}" target="_blank">
                    <img src="https://img.shields.io/badge/X%E3%81%A7%E7%B5%90%E6%9E%9C%E3%82%92%E6%9B%92%E3%81%99-000000?style=for-the-badge&logo=x&logoColor=white" alt="Xでシェア">
                </a>
            </div>
            """, unsafe_allow_html=True)

    elif df.empty:
        st.error("データが読み込めていません。")