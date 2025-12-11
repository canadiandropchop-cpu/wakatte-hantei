import streamlit as st
import pandas as pd
from thefuzz import process

# ==========================================
# 1. 資産（データ）の読み込み
# ==========================================
@st.cache_data # データをキャッシュして高速化（資産運用の効率化）
def load_data():
    try:
        # CSVファイルを読み込む
        df = pd.read_csv("university_data_dummy.csv")
        return df
    except FileNotFoundError:
        st.error("エラー: 'university_data_dummy.csv' が見つかりません。同じフォルダに置いてください。")
        return pd.DataFrame()

df = load_data()

# ==========================================
# 2. 判定ロジック（制御工学でいうコントローラー）
# ==========================================
def get_comment(dev_val, univ_name):
    # 特定の大学に対する「隠しコマンド」的処理（ネタ枠）
    if "帝京平成" in univ_name:
        return "ここがすごい！帝京平成大学！...って言いたいだけだろ？"
    if "日本体育" in univ_name:
        return "筋肉は裏切らない。偏差値なんて気にするな。"

    # 偏差値による階級判定（wakatte.tv風ヒエラルキー）
    if dev_val >= 70:
        return "【神】\nあなたは日本の宝です。将来、納税で我々を養ってください。"
    elif dev_val >= 65:
        return "【エリート】\nすごいですね。でも東大には勝てませんよ？"
    elif dev_val >= 60:
        return "【上位層】\nまあまあ賢い。でも、世の中には上がいます。"
    elif dev_val >= 55:
        return "【凡人】\nTHE 普通。量産型大学生として日本を支えてください。"
    elif dev_val >= 50:
        return "【ギリギリ】\n日東駒専レベル。遊んでないで資格の一つでも取ったら？"
    else:
        return "【Fラン（仮）】\nwakatte.tvならマイクを向けられないレベルです。バイトリーダー目指して頑張れ。"

# ==========================================
# 3. Web画面の構築（フロントエンド）
# ==========================================

# ページ設定
st.set_page_config(page_title="辛口！学歴判定機", page_icon="🎓")

# タイトル
st.title("🎓 学歴だけで人を判断するサイト")
st.markdown("あなたの出身大学（または志望校）を入力してください。\n**偏差値に基づいて、忖度なしのコメント**を返します。")

# ユーザー入力フォーム
user_input = st.text_input("大学名を入力（例：京大、早稲田）", "")

# ボタンが押されたら判定実行
if st.button("判定する"):
    if user_input and not df.empty:
        # A. 曖昧検索ロジック（入力された文字に一番近い大学を探す）
        # process.extractOne は (大学名, 一致度スコア) を返します
        all_univ_names = df['University'].tolist()
        match_result = process.extractOne(user_input, all_univ_names)
        
        best_match_name = match_result[0]
        score = match_result[1]

        # 一致度が低い（60点未満）場合は「見つからない」とする
        if score < 60:
            st.warning(f"「{user_input}」に近い大学が見つかりませんでした。もっと正確に入力して！")
        else:
            # B. データの抽出
            row = df[df['University'] == best_match_name].iloc[0]
            deviation = row['Deviation']
            
            # C. 結果の表示
            st.success(f"もしかして： **{best_match_name}** （偏差値: {deviation}）")
            
            # 辛口コメント表示（デカ文字で）
            comment = get_comment(deviation, best_match_name)
            st.markdown(f"### {comment}")



            # （前略）判定結果が表示された後の部分に追加

            # ... コメント表示の後 ...
            
            # E. 拡散機能（資産を増幅させるエンジン）
            # ユーザーが結果をツイートしやすいリンクを作成
            share_text = f"私の学歴は...【{best_match_name}（偏差値{deviation}）】でした！\n判定結果：「{comment.splitlines()[0]}」\n#学歴判定機 #wakatte_tv"
            share_url = f"https://twitter.com/intent/tweet?text={share_text}"
            
            st.markdown(f"[![Xでシェア](https://img.shields.io/badge/X-%E3%82%B7%E3%82%A7%E3%82%A2%E3%81%99%E3%82%8B-black?logo=x&style=for-the-badge)]({share_url})")

            # （後略）



            # D. 収益化ポイント（アフィリエイトリンクへの誘導枠）
            st.divider()
            st.info("💡 偏差値を上げたい？ なら、この参考書を買って勉強しろ。（ここにアフィリエイトリンクを貼る）")



    elif df.empty:
        st.error("データが読み込めていません。")
    else:
        st.write("大学名を入力してください。")

# フッター
st.write("---")
st.caption("※この偏差値はダミーデータに基づいています。ジョークサイトとしてお楽しみください。")